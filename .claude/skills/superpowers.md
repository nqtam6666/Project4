---
name: superpowers
description: Kích hoạt chế độ siêu năng lực - tối ưu code quality, phân tích sâu, và đề xuất nâng cấp toàn diện cho codebase NQT Gym
---

# SUPERPOWERS MODE - NQT Gym Management

Bạn đang ở chế độ **SIÊU NĂNG LỰC**. Áp dụng toàn bộ best practices cho dự án NQT Gym.

ARGUMENTS: $ARGUMENTS

## Quy trình thực hiện

### 1. PHÂN TÍCH TOÀN DIỆN
Trước khi làm bất cứ điều gì, hãy:
- Đọc context từ ARGUMENTS (nếu có) để hiểu scope
- Scan codebase liên quan (models, routes, services, frontend)
- Phát hiện: code smells, security holes, performance bottlenecks, UX issues
- Kiểm tra tuân thủ naming convention `nqt_` / `Nqt` / `nqt-`

### 2. CHECKLIST SIÊU NĂNG LỰC

#### Backend (Flask)
- [ ] Tất cả routes có JWT auth đúng chỗ
- [ ] Validate input tại mọi endpoint (không trust client)
- [ ] SQL injection prevention (dùng ORM parameterized queries)
- [ ] Không hardcode config - dùng `NqtDichVuCauHinh.nqt_lay()`
- [ ] Error handling nhất quán theo format `nqt_thanh_cong / nqt_loi`
- [ ] Logging cho mọi operation quan trọng
- [ ] Rate limiting trên auth endpoints
- [ ] Bcrypt cho mật khẩu

#### Frontend (TailwindCSS + Vanilla JS)
- [ ] Responsive trên mobile/tablet/desktop
- [ ] Loading states cho mọi async operation
- [ ] Error messages thân thiện với user
- [ ] XSS prevention (escape HTML output)
- [ ] CSRF tokens trên forms
- [ ] Accessible (aria-label, keyboard nav)

#### Database (SQL Server)
- [ ] Indexes trên columns thường query
- [ ] Foreign key constraints đúng
- [ ] Naming: `NqtXxx` tables, `nqt_xxx` columns

#### Code Quality
- [ ] Naming convention nhất quán (tiền tố `nqt_`)
- [ ] Không duplicate logic - DRY principle
- [ ] Functions nhỏ, single responsibility
- [ ] Comments cho business logic phức tạp

### 3. OUTPUT FORMAT

Sau khi phân tích, báo cáo theo format:

```
## SUPERPOWERS REPORT

### Vấn đề nghiêm trọng (fix ngay)
- [file:line] Mô tả vấn đề + cách fix

### Cải thiện đề xuất
- [file:line] Mô tả + lợi ích

### Quick wins
- [file:line] Thay đổi nhỏ, impact lớn

### Tổng điểm: X/100
```

### 4. TỰ ĐỘNG FIX
Nếu ARGUMENTS chứa `--fix` hoặc `--auto`:
- Áp dụng tất cả fixes an toàn tự động
- Preview trước mỗi thay đổi > 20 dòng
- Skip những gì cần business decision

## Nguyên tắc Superpowers
- **Không bao giờ** làm hỏng code đang chạy
- **Luôn** giữ naming convention của project
- **Ưu tiên** security > performance > readability
- **Preview** mọi thay đổi lớn trước khi apply
