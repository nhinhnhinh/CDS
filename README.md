<div align="center">
  <p align="center">
    <img src="LTM/src/assets/aiotlab_logo.png" alt="AIoTLab Logo" width="160"/>
    <img src="LTM/src/assets/fitdnu_logo.png" alt="FIT DNU Logo" width="180"/>
    <img src="LTM/src/assets/dnu_logo.png" alt="DaiNam University Logo" width="200"/>
  </p>
</div>

<h2 align="center">
  <a href="https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin">
    🎓 Faculty of Information Technology (DaiNam University)
  </a>
</h2>

<h2 align="center">
  Hệ thống chẩn đoán X-quang phổi hỗ trợ AI (X-ray Diagnosis System)
</h2>

<div align="center">
  <p align="center">
    [![AIoTLab](https://img.shields.io/badge/AIoTLab-green?style=for-the-badge)](https://www.facebook.com/DNUAIoTLab)
    [![Faculty of Information Technology](https://img.shields.io/badge/FIT-DNU-blue?style=for-the-badge)](https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin)
    [![DaiNam University](https://img.shields.io/badge/DaiNam%20University-orange?style=for-the-badge)](https://dainam.edu.vn)
  </p>
</div>

---

## 📖 1. Giới thiệu hệ thống

Hệ thống chẩn đoán X-quang phổi sử dụng trí tuệ nhân tạo (AI) để phân tích ảnh X-quang phổi, phát hiện các tổn thương và cung cấp tư vấn y khoa tự động. Hệ thống bao gồm các mô hình AI tiên tiến như **ResNet50** cho phân loại bệnh lý, **YOLOv8** cho phát hiện tổn thương, và **Gemini AI** để sinh tư vấn y khoa chi tiết. Các tính năng chính của hệ thống bao gồm:

📸 Phân tích ảnh X-quang để nhận diện bệnh lý phổi  
🔍 Phát hiện tổn thương trong phổi (ví dụ: khối u, viêm phổi)  
📊 Cung cấp các báo cáo về tình trạng bệnh và hướng điều trị  
📤 Sinh tư vấn y khoa hỗ trợ bác sĩ trong quá trình ra quyết định điều trị  

### 🏗️ Cấu trúc hệ thống
Hệ thống bao gồm các thành phần chính:

📹 **Camera**: Hệ thống nhận ảnh X-quang từ các thiết bị chẩn đoán  
🖥️ **Xử lý ảnh và AI**: Dùng YOLOv8 để phát hiện tổn thương và ResNet50 để phân loại bệnh lý  
💾 **Cơ sở dữ liệu**: Lưu trữ thông tin bệnh nhân và kết quả phân tích vào cơ sở dữ liệu  

---

## 🛠️ Công cụ sử dụng

Python 🐍 (OpenCV, YOLOv8, ResNet50, Gemini AI, SQLite)  
Thư viện hỗ trợ: Numpy, Pandas, Ultralytics, Plotly...  
Mô hình AI: **ResNet50** cho phân loại bệnh, **YOLOv8** cho phát hiện tổn thương  
Cơ sở dữ liệu: **SQLite/MySQL** để lưu trữ dữ liệu bệnh nhân và kết quả phân tích  
Tư vấn y khoa: **Gemini AI**  

---

## 🚀 Hướng dẫn cài đặt và chạy

### 1. Cài đặt thư viện

Cài đặt Python 3.7+  
Sau đó cài đặt các thư viện trong file `requirements.txt` với câu lệnh sau:

```bash
pip install -r requirements.txt
Tạo môi trường ảo (tùy chọn)

bash
Copy code
python -m venv venv
source venv/bin/activate  # Trên macOS/Linux
.\venv\Scripts\activate  # Trên Windows
Tạo cơ sở dữ liệu

python
Copy code
import sqlite3
conn = sqlite3.connect("patient_data.db")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                age INTEGER,
                gender TEXT,
                symptoms TEXT,
                diagnosis TEXT,
                exam_date TEXT)''')
conn.commit()
Chạy hệ thống

bash
Copy code
python xray_diagnosis_system.py
📖 Hướng dẫn sử dụng

Mở giao diện và chọn file ảnh X-quang cần phân tích.

Nhấn nút "Phân tích" để hệ thống xử lý.

Kiểm tra kết quả trên màn hình hoặc xuất báo cáo dưới dạng PDF/Excel.

⚙️ Cấu hình & Ghi chú

Cấu hình đường dẫn ảnh X-quang trong xray_diagnosis_system.py.
Tùy chỉnh các mô hình phân tích trong model_config.py.

🧬 Tư vấn Y khoa
Hệ thống cung cấp tư vấn y khoa tự động dựa trên kết quả phân tích ảnh và các triệu chứng bệnh nhân. Một số nội dung tư vấn bao gồm:

Chẩn đoán: Tình trạng bệnh phổi dựa trên kết quả phân tích

Điều trị: Khuyến nghị các phương pháp điều trị

Cận lâm sàng: Các xét nghiệm bổ sung cần thực hiện

Tiên lượng: Dự đoán về khả năng phục hồi của bệnh nhân

Lối sống: Hướng dẫn chăm sóc sức khỏe và phòng ngừa

📊 Báo cáo & Thống kê
Hệ thống lưu thông tin phân tích vào cơ sở dữ liệu và hỗ trợ xuất báo cáo thống kê dưới dạng bảng hoặc đồ thị. Các báo cáo bao gồm:

Số lượng bệnh nhân phân tích: Bao gồm thông tin về bệnh lý và các tổn thương phát hiện.

Tỷ lệ chính xác của mô hình: Hiển thị độ chính xác trong phân loại và phát hiện tổn thương.

📈 Biểu đồ phân loại bệnh lý
Hệ thống hiển thị các biểu đồ thống kê về tỷ lệ các bệnh lý phát hiện được, ví dụ:

Phân loại bệnh (Top-5)

Phân loại tổn thương (detected lesions)

Tỷ lệ độ tin cậy của mô hình phân tích

💾 Lưu trữ dữ liệu
Dữ liệu phân tích được lưu vào cơ sở dữ liệu SQLite, bao gồm các thông tin sau:

ID bệnh nhân

Tên bệnh nhân

Triệu chứng

Chẩn đoán

Ngày khám

📄 Xem lại dữ liệu
Để xem lại dữ liệu đã lưu, sử dụng câu lệnh sau:

bash
Copy code
python view_patient_data.py
🎓 Kết luận
Hệ thống chẩn đoán X-quang phổi hỗ trợ AI của chúng tôi giúp bác sĩ phân tích ảnh X-quang nhanh chóng và chính xác, đồng thời cung cấp các tư vấn y khoa tự động. Hệ thống có thể phát hiện các tổn thương phổi, phân loại bệnh lý, và cung cấp các khuyến nghị điều trị hiệu quả.
