# 📋 HƯỚNG DẪN LÀM VIỆC NHÓM VỚI GIT

## Mục lục
- [1. Clone Project](#1-clone-project)
- [2. Workflow làm việc với Branch](#2-workflow-làm-việc-với-branch)
- [3. Quy tắc đặt tên Branch](#3-quy-tắc-đặt-tên-branch)
- [4. Xử lý Conflict](#4-xử-lý-conflict)
- [5. Lệnh Git thường dùng](#5-lệnh-git-thường-dùng)
- [6. Quy trình Review Code](#6-quy-trình-review-code)

---

## 1. Clone Project

```bash
git clone https://github.com/nqtam6666/Project4.git
cd Project4
```

---

## 2. Workflow làm việc với Branch

> **⚠️ QUAN TRỌNG: KHÔNG BAO GIỜ push trực tiếp lên `main`!**

### Bước 1: Tạo branch mới trước khi code

```bash
# Cập nhật main trước
git checkout main
git pull origin main

# Tạo branch theo format: [tên]-[loại]-[mô tả ngắn]
git checkout -b vtq-feature-dang-nhap
```

### Bước 2: Code và commit thường xuyên

```bash
# Add từng file cụ thể (khuyến khích)
git add ten-file.py
git commit -m "Thêm chức năng đăng nhập"

# Hoặc add tất cả thay đổi
git add .
git commit -m "Hoàn thành form đăng nhập"
```

### Bước 3: Push branch lên GitHub

```bash
git push -u origin vtq-feature-dang-nhap
```

### Bước 4: Tạo Pull Request (PR) trên GitHub

1. Vào GitHub → Repository → Tab **"Pull requests"**
2. Click **"New pull request"**
3. Chọn branch của bạn → `main`
4. Viết mô tả những gì đã làm
5. Assign người review

### Bước 5: Sau khi PR được approve và merge

```bash
# Quay về main và cập nhật
git checkout main
git pull origin main

# Xóa branch cũ (optional)
git branch -d vtq-feature-dang-nhap
```

---

## 3. Quy tắc đặt tên Branch

| Loại | Format | Ví dụ |
|------|--------|-------|
| Feature mới | `[tên]-feature-[mô tả]` | `vtq-feature-quan-ly-hoi-vien` |
| Sửa bug | `[tên]-fix-[mô tả]` | `pnm-fix-loi-check-in` |
| Refactor | `[tên]-refactor-[mô tả]` | `nqt-refactor-api-response` |
| Hotfix | `[tên]-hotfix-[mô tả]` | `abc-hotfix-login-crash` |
| Docs | `[tên]-docs-[mô tả]` | `nqt-docs-api-guide` |

**Quy tắc:**
- Dùng chữ thường, không dấu tiếng Việt
- Dùng dấu `-` thay vì `_` hoặc space
- Ngắn gọn, dễ hiểu

---

## 4. Xử lý Conflict

### Khi có conflict với main

```bash
# Đang ở branch của mình
git fetch origin
git merge origin/main

# Nếu có conflict, Git sẽ báo file nào bị conflict
# Mở file đó, tìm và sửa các đoạn:
# <<<<<<< HEAD
# Code của bạn
# =======
# Code từ main
# >>>>>>> origin/main

# Sau khi sửa xong:
git add .
git commit -m "Resolve conflict với main"
git push
```

### Tips tránh conflict

- Pull main thường xuyên vào branch của mình
- Chia nhỏ task, merge sớm
- Communicate với team khi sửa cùng file

---

## 5. Lệnh Git thường dùng

### Xem trạng thái

```bash
git status                    # Xem file đã thay đổi
git log --oneline -10         # Xem 10 commit gần nhất
git diff                      # Xem chi tiết thay đổi
git branch -a                 # Xem tất cả branch
```

### Làm việc với branch

```bash
git checkout main             # Chuyển về main
git checkout ten-branch       # Chuyển sang branch khác
git checkout -b new-branch    # Tạo và chuyển sang branch mới
git branch -d ten-branch      # Xóa branch local
```

### Cập nhật code

```bash
git fetch origin              # Lấy thông tin từ remote
git pull origin main          # Pull code từ main
git pull origin ten-branch    # Pull code từ branch cụ thể
```

### Hoàn tác thay đổi

```bash
# Hoàn tác file chưa stage
git checkout -- ten-file

# Hoàn tác file đã stage
git reset HEAD ten-file

# Sửa commit message cuối (chưa push)
git commit --amend -m "Message mới"
```

---

## 6. Quy trình Review Code

### Cho Author (người tạo PR)

1. **Tạo PR** với tiêu đề rõ ràng
2. **Mô tả** những gì đã làm, tại sao
3. **Self-review** trước khi request review
4. **Respond** feedback từ reviewer

### Cho Reviewer

1. **Check code** theo quy tắc trong `CLAUDE.md`:
   - Tiền tố `nqt_` cho code mới
   - Không sửa tiền tố của người khác
   - Clean code, không hardcode config
2. **Test** nếu cần thiết
3. **Comment** góp ý hoặc **Approve**

### Checklist Review

- [ ] Code chạy được, không có lỗi
- [ ] Đúng naming convention (tiền tố nqt_)
- [ ] Không hardcode config values
- [ ] Không commit file nhạy cảm (.env, secrets)
- [ ] Code dễ đọc, có comment nếu cần

---

## 7. Cấu trúc Commit Message

```
[Loại]: Mô tả ngắn gọn

Ví dụ:
feat: Thêm chức năng đăng nhập
fix: Sửa lỗi không gửi được email
refactor: Tách service xử lý hội viên
docs: Cập nhật hướng dẫn API
style: Format lại code theo chuẩn
```

---

## 8. Các file quan trọng

| File | Mô tả |
|------|-------|
| `CLAUDE.md` | Quy tắc code, naming convention |
| `.gitignore` | Danh sách file không commit |
| `.env.example` | Template cho file .env |
| `GIT_WORKFLOW.md` | File này |

---

## 9. Liên hệ hỗ trợ

- **Repository**: https://github.com/nqtam6666/Project4
- **Owner**: nqtam6666

---

> **Lưu ý**: Đọc kỹ `CLAUDE.md` trước khi code để nắm rõ quy tắc đặt tên và coding convention của project.
