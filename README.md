# Demo SQL Injection với FastAPI

Dự án này minh họa sự khác biệt giữa cách truy vấn cơ sở dữ liệu **an toàn** và **không an toàn** trong FastAPI, đặc biệt tập trung vào lỗ hổng SQL Injection.

## 📋 Mô tả dự án

Ứng dụng FastAPI này cung cấp hai endpoint:
- **Endpoint an toàn**: Sử dụng parameter binding để tránh SQL injection
- **Endpoint không an toàn**: Sử dụng string concatenation, dễ bị tấn công SQL injection

## 🔧 Yêu cầu hệ thống

- Python 3.12 hoặc cao hơn
- Conda hoặc pip để quản lý package

## 🚀 Cài đặt và chạy ứng dụng

### Phương pháp 1: Sử dụng Conda Environment (Khuyến nghị)

1. **Tạo môi trường từ file environment.yml:**
   ```bash
   conda env create -f environment.yml
   ```

2. **Kích hoạt môi trường:**
   ```bash
   conda activate demo
   ```

3. **Chạy ứng dụng:**
   ```bash
   python app.py
   ```

### Phương pháp 2: Tạo môi trường Conda mới và sử dụng pip

1. **Tạo môi trường conda mới rỗng:**
   ```bash
   conda create -n demo python=3.12
   ```

2. **Kích hoạt môi trường:**
   ```bash
   conda activate demo
   ```

3. **Cài đặt dependencies bằng pip:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Chạy ứng dụng:**
   ```bash
   python app.py
   ```

## 📊 Cơ sở dữ liệu

Dự án sử dụng SQLite với bảng `students`:

| Cột | Kiểu dữ liệu | Mô tả |
|-----|-------------|-------|
| id  | INTEGER PRIMARY KEY | ID sinh viên (tự động tăng) |
| name | TEXT | Tên sinh viên |
| age | INTEGER | Tuổi sinh viên |

**Dữ liệu mẫu:**
- ID: 1, Tên: Alice, Tuổi: 20
- ID: 2, Tên: Bob, Tuổi: 22

## 🌐 API Endpoints

Sau khi chạy ứng dụng, truy cập: `http://localhost:8000`

### 0. Root Endpoint (Kiểm tra trạng thái)
```
GET /
```

**Mô tả:**
- Kiểm tra xem API có hoạt động hay không
- Trả về thông báo xác nhận

**Response:**
```json
{
  "message": "API is working!"
}
```

### 1. Endpoint AN TOÀN
```
GET /students/{student_id}
```

**Ví dụ:**
- `GET /students/1` - Lấy thông tin sinh viên ID = 1

**Đặc điểm:**
- ✅ Sử dụng parameter binding
- ✅ An toàn khỏi SQL injection
- ✅ Validate input là số nguyên

### 2. Endpoint KHÔNG AN TOÀN (Chỉ cho mục đích demo)
```
GET /students-unsafe/?student_id={id}
```

**Ví dụ:**
- **Truy vấn bình thường:** `GET /students-unsafe/?student_id=1`
- **SQL Injection:** `GET /students-unsafe/?student_id=1 OR 1=1`

**⚠️ CẢNH BÁO:**
- ❌ Dễ bị tấn công SQL injection
- ❌ Không validate input
- ❌ Chỉ sử dụng cho mục đích học tập

## 🔍 Demo SQL Injection

### Truy vấn bình thường:
```
GET /students-unsafe/?student_id=1
```
**SQL được thực thi:** `SELECT name, age FROM students WHERE id = 1`

### Tấn công SQL Injection:
```
GET /students-unsafe/?student_id=1 OR 1=1
```
**SQL được thực thi:** `SELECT name, age FROM students WHERE id = 1 OR 1=1`

Điều này sẽ trả về **tất cả** sinh viên trong database thay vì chỉ một sinh viên cụ thể.

## 📖 Interactive API Documentation

FastAPI tự động tạo documentation:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

## 🛡️ Bài học an toàn

### ✅ Cách ĐÚNG (Parameter Binding):
```python
cursor.execute("SELECT name, age FROM students WHERE id = ?", (student_id,))
```

### ❌ Cách SAI (String Concatenation):
```python
query = f"SELECT name, age FROM students WHERE id = {student_id_str}"
cursor.execute(query)
```

## 🏗️ Cấu trúc dự án

```
demoAI1/
├── app.py              # Ứng dụng FastAPI chính
├── students.db         # Cơ sở dữ liệu SQLite
├── environment.yml     # Conda environment file
├── requirements.txt    # Python dependencies
└── README.md          # Tài liệu dự án
```

## 🔧 Dependencies chính

- **FastAPI**: Web framework hiện đại cho Python
- **Uvicorn**: ASGI server để chạy FastAPI
- **SQLite3**: Database engine (built-in Python)
- **Pydantic**: Data validation và serialization

## 🎯 Mục đích giáo dục

Dự án này được tạo ra để:
1. **Hiểu rõ SQL Injection**: Cách thức hoạt động và tác hại
2. **Học cách phòng chống**: Sử dụng parameter binding
3. **Thực hành FastAPI**: Tạo API endpoints an toàn
4. **So sánh phương pháp**: An toàn vs không an toàn

## ⚠️ Lưu ý quan trọng

- **KHÔNG BAO GIỜ** sử dụng endpoint không an toàn trong production
- Endpoint `/students-unsafe/` chỉ dành cho mục đích demo và học tập
- Luôn sử dụng parameter binding khi làm việc với database
- Validate và sanitize tất cả input từ người dùng

## 📝 License

Dự án này được tạo ra cho mục đích giáo dục và có thể sử dụng tự do.

---

**Tác giả:** cuongphamduc  
**Thời gian tạo:** 2025  
**Mục đích:** Giáo dục về SQL Injection Security
