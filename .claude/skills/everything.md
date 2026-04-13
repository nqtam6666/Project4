---
name: everything
description: Chế độ EVERYTHING - kích hoạt toàn bộ khả năng Claude Code, tạo full-stack feature hoàn chỉnh từ DB đến UI trong một lần
---

# EVERYTHING MODE - NQT Gym Management

Chế độ **EVERYTHING**: Tạo feature hoàn chỉnh end-to-end — model, migration, service, route, frontend template, JS, CSS — tất cả trong một lần.

ARGUMENTS: $ARGUMENTS

## Cách dùng

```
/everything <tên_feature> [options]

Ví dụ:
/everything hoi-vien          → Full CRUD hội viên
/everything goi-tap           → Full CRUD gói tập
/everything bao-cao-doanh-thu → Trang báo cáo doanh thu
/everything check-in-qr       → Hệ thống check-in QR
```

## Pipeline EVERYTHING

Khi nhận ARGUMENTS, Claude sẽ tự động tạo **theo thứ tự**:

### BƯỚC 1: Database Layer
```sql
-- 1a. SQL migration script
-- 1b. Seed data mẫu (5-10 rows)
```

### BƯỚC 2: Backend Models
```python
# app/models/nqt_<feature>.py
# - SQLAlchemy model với đầy đủ columns
# - Relationships
# - Helper methods (nqt_lay_theo_xxx, nqt_tim_kiem...)
# - __repr__ cho debug
```

### BƯỚC 3: Services (Business Logic)
```python
# app/services/nqt_dich_vu_<feature>.py
# - CRUD operations
# - Validation logic
# - Business rules
# - Tích hợp NqtDichVuCauHinh cho dynamic config
```

### BƯỚC 4: API Routes
```python
# app/routes/nqt_<feature>_route.py
# - GET /nqt-<feature>/ (list + filter + pagination)
# - GET /nqt-<feature>/<id> (detail)
# - POST /nqt-<feature>/ (create)
# - PUT /nqt-<feature>/<id> (update)
# - DELETE /nqt-<feature>/<id> (soft delete)
# - JWT auth + RBAC decorators
# - Input validation
# - Standard response format
```

### BƯỚC 5: Frontend Templates
```html
<!-- frontend/templates/nqt_<feature>/ -->
<!-- - list.html: DataTable với search/filter/sort -->
<!-- - detail.html: Form xem/sửa -->
<!-- - TailwindCSS responsive layout -->
```

### BƯỚC 6: JavaScript Module
```javascript
// frontend/static/js/nqt<Feature>.js
// - Class NqtQuan Ly<Feature>
// - CRUD methods với fetch API
// - Form validation client-side
// - Toast notifications
// - Confirm dialogs cho delete
```

### BƯỚC 7: Integration
```python
# Đăng ký blueprint trong app/__init__.py
# Thêm nav link vào base template
# Cập nhật RBAC permissions
```

### BƯỚC 8: Summary Report
```
✅ Files created: X
✅ Endpoints: GET, POST, PUT, DELETE
✅ Rows to migrate: X
⚠️ Manual steps needed:
   1. Run: flask db migrate -m "add nqt_<feature>"
   2. Run: flask db upgrade
   3. Seed: flask seed nqt_<feature>
```

## Options

| Flag | Mô tả |
|------|-------|
| `--no-ui` | Chỉ tạo backend (model + service + route) |
| `--no-delete` | Bỏ qua delete endpoint |
| `--read-only` | Chỉ GET endpoints (báo cáo/xem) |
| `--admin-only` | Tất cả endpoints yêu cầu role Admin |
| `--with-export` | Thêm export Excel/CSV |
| `--with-search` | Thêm full-text search |

## Quy tắc EVERYTHING Mode
- Tất cả code tuân thủ naming `nqt_` prefix
- Không hardcode — dùng `NqtDichVuCauHinh`
- Mọi thay đổi DB đều qua Flask-Migrate
- Preview trước khi tạo file (confirm với user nếu > 5 files)
- Tạo theo đúng project structure trong CLAUDE.md
