"""
High-level API to process an input image:
- Loads image (path/file-like/PIL) -> PIL
- Preprocesses for ResNet -> tensor
- Runs YOLOv8 for detections and ResNet50 for classification
- Normalizes detections and renders annotated image
"""

from typing import Any, Dict, List
from PIL import ImageDraw, ImageFont, Image

from backend.utils.visualization import annotate_image
from backend.utils.data_processing import load_image
from backend.utils.image_preprocessing import preprocess_image
from backend.utils.labels import get_detection_label_map
from backend.utils.llm import diagnosis_to_text, generate_advice
from backend.models.yolov8_model import YOLOv8Model
from backend.models.resnet50_model import ResNet50Model


# Instantiate models once (CPU-safe by default)
yolo_model = YOLOv8Model()
resnet_model = ResNet50Model()


def _normalize_detections(dets: Any) -> List[Dict[str, Any]]:
    """
    Normalize various detection outputs to a list of dicts with keys:
    - xcenter, ycenter, width, height, confidence (optional), class (int), name (str optional)

    Supports:
    - list[dict] in YOLO-like format
    - pandas.DataFrame with columns like ['xcenter','ycenter','width','height','confidence','class','name']
    - list of DataFrames (take the first)
    """
    if dets is None:
        return []

    # Already normalized list of dicts
    if isinstance(dets, list) and (len(dets) == 0 or isinstance(dets[0], dict)):
        out: List[Dict[str, Any]] = []
        for d in dets:
            try:
                out.append({
                    "xcenter": float(d.get("xcenter", d.get("x", 0.0))),
                    "ycenter": float(d.get("ycenter", d.get("y", 0.0))),
                    "width": float(d.get("width", d.get("w", 0.0))),
                    "height": float(d.get("height", d.get("h", 0.0))),
                    "confidence": (None if d.get("confidence") is None else float(d.get("confidence"))),
                    "class": int(d.get("class", -1)) if d.get("class") is not None else -1,
                    "name": d.get("name") or d.get("label"),
                })
            except Exception:
                continue
        return out

    # Pandas DataFrame or compatible (duck-typing)
    def _from_df(df) -> List[Dict[str, Any]]:
        cols = {c.lower(): c for c in getattr(df, "columns", [])}
        rows: List[Dict[str, Any]] = []
        try:
            iterator = df.iterrows() if hasattr(df, "iterrows") else []
        except Exception:
            iterator = []
        for _, row in iterator:
            def _get(keys, default=None):
                for k in keys:
                    c = cols.get(k)
                    if c is not None:
                        v = row.get(c, None)
                        if v is not None:
                            return v
                return default

            xc = _get(["xcenter", "x"], 0.0)
            yc = _get(["ycenter", "y"], 0.0)
            w = _get(["width", "w"], 0.0)
            h = _get(["height", "h"], 0.0)
            conf = _get(["confidence", "conf"], None)
            cls_id = _get(["class", "cls"], -1)
            name = _get(["name", "label"], None)
            try:
                rows.append({
                    "xcenter": float(xc),
                    "ycenter": float(yc),
                    "width": float(w),
                    "height": float(h),
                    "confidence": (None if conf is None else float(conf)),
                    "class": int(cls_id) if cls_id is not None else -1,
                    "name": None if name is None else str(name),
                })
            except Exception:
                continue
        return rows

    # Single DataFrame
    if hasattr(dets, "iterrows") and hasattr(dets, "columns"):
        return _from_df(dets)

    # List with first element a DataFrame
    if isinstance(dets, list) and len(dets) > 0 and hasattr(dets[0], "iterrows"):
        return _from_df(dets[0])

    # Unknown format
    return []

def process_image(image_input):
    """
    Nhận ảnh từ Streamlit UploadedFile, đường dẫn, file-like hoặc PIL.Image.
    Trả về dict:
      - diagnosis: nhãn dự đoán từ ResNet50
      - detections: kết quả phát hiện của YOLO (định dạng phụ thuộc mô hình)
    """
    # 1) Tải ảnh thành PIL để dùng cho YOLO
    pil_img = load_image(image_input)

    # 2) Tiền xử lý riêng cho ResNet (tensor)
    img_tensor = preprocess_image(pil_img)

    # 3) Chạy hai mô hình
    detections_raw = yolo_model.detect(pil_img)
    detections = _normalize_detections(detections_raw)
    diagnosis = resnet_model.predict(img_tensor)
    probabilities = resnet_model.predict_proba(img_tensor)

    # 4) Tạo ảnh gắn bbox để hiển thị ở tab Kết quả
    annotated = annotate_image(
        pil_img,
        detections,
        label_map=get_detection_label_map(),
        min_conf=0.25,
        box_color=(255, 255, 0),  # Màu vàng cho bounding box
        text_fg=(255, 255, 255),  # Màu chữ trắng
        text_bg=(0, 0, 0),        # Nền chữ đen để dễ đọc
    )

    # Vẽ nhãn chẩn đoán tổng thể lên ảnh (góc trên trái)
    try:
        label_text = diagnosis_to_text(diagnosis)
        draw = ImageDraw.Draw(annotated)
        try:
            font = ImageFont.load_default()
        except Exception:
            font = None
        text = f"Chẩn đoán: {label_text}"
        if font:
            # Tính kích thước chữ tương thích Pillow mới/cũ
            try:
                bbox = draw.textbbox((0, 0), text, font=font)
                tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
            except Exception:
                try:
                    tw, th = draw.textsize(text, font=font)
                except Exception:
                    tw, th = (len(text) * 6, 12)
        else:
            # Ước lượng thô nếu không lấy được font
            tw, th = (len(text) * 6, 12)
        pad = 6
        bg_rect = [(5, 5), (5 + tw + 2 * pad, 5 + th + 2 * pad)]
        draw.rectangle(bg_rect, fill=(0, 0, 0))  # Vẽ nền đen cho nhãn
        draw.text((5 + pad, 5 + pad), text, fill=(255, 255, 255), font=font)
    except Exception:
        label_text = diagnosis_to_text(diagnosis)

    return {
        "diagnosis": diagnosis,              # int
        "probabilities": probabilities,      # list[float]
        "detections": detections,            # list[dict]
        "annotated_image": annotated,        # PIL.Image
        "label": label_text,
        "advice": generate_advice(diagnosis, detections),
    }
