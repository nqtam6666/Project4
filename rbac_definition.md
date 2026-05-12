# Định nghĩa Hệ Thống Phân Quyền (RBAC - Role-Based Access Control)

Hệ thống phân quyền được thiết kế dựa trên mô hình RBAC, trong đó Người dùng (User) không được gán quyền (Permission) trực tiếp, mà sẽ được gán vào các Vai trò (Role). Các Vai trò này sẽ nắm giữ các Quyền hạn cụ thể.

## 1. Các Thực Thể Chính trong Database

*   **`G6NguoiDung` (Người dùng):** Các tài khoản sử dụng hệ thống (Quản trị viên, Nhân viên, Khách hàng, ...).
*   **`G6VaiTro` (Vai trò/Role):** Đại diện cho một nhóm quyền hạn, ví dụ: *Quản trị viên*, *Quản lý kho*, *Nhân viên bán hàng*. Bạn có thể tạo thêm bao nhiêu Vai trò tuỳ thích.
*   **`G6QuyenHan` (Quyền hạn/Permission):** Là các hành động cụ thể mà hệ thống cho phép. Ví dụ: `g6_them_san_pham`, `g6_xem_don_hang`. Các quyền hạn thường được code cứng (hard-coded) vào hệ thống dựa trên chức năng API có sẵn và được seed vào database.
*   **`G6VaiTroQuyen` (Vai trò - Quyền):** Bảng trung gian xác định Vai trò nào có Quyền nào.
*   **`G6NguoiDungVaiTro` (Người dùng - Vai trò):** Bảng trung gian xác định Người dùng nào được gán Vai trò nào (Một người dùng có thể có nhiều Vai trò).

## 2. Cách Sử Dụng Trong Source Code (Decorators)

Hệ thống sử dụng decorator `@nqt_yeu_cau_quyen` để kiểm tra quyền hạn trước khi cho phép gọi API.
Decorator này nằm ở `backend/app/utils/g6_xac_thuc.py`.

```python
from backend.app.utils.g6_xac_thuc import nqt_yeu_cau_quyen

# Yêu cầu người dùng phải có quyền "g6_them_san_pham" (hoặc là "G6QuanTri")
@app.route('/api/san-pham', methods=['POST'])
@nqt_yeu_cau_quyen('g6_them_san_pham')
def them_san_pham():
    # Logic thêm sản phẩm
    pass
```
*Lưu ý:* Hệ thống mặc định cấp toàn quyền cho vai trò có tên là `G6QuanTri` (bypass check permission). Do đó, User mang Role này có thể gọi bất kì API nào.

## 3. Cách "Thêm Tuỳ Thích Role"

Hệ thống cung cấp một bộ API (tại endpoint `/api/...`) cho phép bạn linh hoạt tạo mới Role và cấu hình Quyền cho Role đó. Quy trình chuẩn như sau:

1.  **Tạo một Vai trò mới (Role):** 
    Gọi API `POST /api/nqt-vai-tro` truyền lên `g6_ten_vai_tro` (Ví dụ: "Nhân viên Content") và `g6_mo_ta`.
2.  **Xem danh sách Quyền (Permission) có sẵn:**
    Gọi API `GET /api/nqt-quyen-han` để lấy toàn bộ các Quyền hệ thống đang hỗ trợ.
3.  **Gán Quyền cho Vai trò vừa tạo:**
    Gọi API `POST /api/nqt-vai-tro/<id_vai_tro_vua_tao>/nqt-phan-quyen`. Truyền lên một mảng các `g6_ma_quyen` mà bạn muốn vai trò này có.
4.  **Gán Vai trò cho Người dùng cụ thể:**
    Gọi API `POST /api/nqt-nguoi-dung/<id_nguoi_dung>/nqt-gan-vai-tro`. Truyền lên một mảng các `g6_ma_vai_tro` (Ví dụ bao gồm cả vai trò "Nhân viên Content" vừa tạo).

Khi Người dùng đăng nhập lại vào hệ thống, Access Token (JWT) mới của họ sẽ chứa thông tin về những Quyền mới này, và họ sẽ ngay lập tức có quyền thực thi các API tương ứng.

## 4. Danh Sách API Quản Lý RBAC

Các API này yêu cầu người gọi phải đã đăng nhập (`@nqt_yeu_cau_dang_nhap`) và có quyền `g6_quan_tri_he_thong`.

| Method | Endpoint | Mô tả | Payload (JSON) |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/nqt-quyen-han` | Lấy danh sách toàn bộ các quyền hạn hiện có trong hệ thống. | - |
| `GET` | `/api/nqt-vai-tro` | Lấy danh sách các vai trò (roles) | - |
| `POST` | `/api/nqt-vai-tro` | Tạo một vai trò mới | `{ "g6_ten_vai_tro": "...", "g6_mo_ta": "..." }` |
| `PUT` | `/api/nqt-vai-tro/<id>` | Cập nhật tên/mô tả của vai trò | `{ "g6_ten_vai_tro": "...", "g6_mo_ta": "..." }` |
| `DELETE` | `/api/nqt-vai-tro/<id>` | Xoá một vai trò khỏi hệ thống | - |
| `GET` | `/api/nqt-vai-tro/<id>/nqt-quyen`| Lấy danh sách quyền hiện tại của 1 vai trò | - |
| `POST` | `/api/nqt-vai-tro/<id>/nqt-phan-quyen`| Cập nhật lại danh sách quyền cho vai trò | `{ "danh_sach_quyen": [1, 2, 5, ...] }` |
| `POST` | `/api/nqt-nguoi-dung/<id>/nqt-gan-vai-tro`| Cập nhật lại các vai trò của một User | `{ "danh_sach_vai_tro": [1, 3] }` |
