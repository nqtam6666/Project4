import json
import os

def generate_openapi():
    spec = {
      "openapi": "3.0.0",
      "info": {
        "title": "G6 Gym Management System API",
        "version": "1.0.0",
        "description": "Tài liệu API đầy đủ cho Hệ thống Quản lý Phòng Gym G6 (Fitness SaaS - B2B). \n\n### Tiền tố bắt buộc: `nqt` / `g6` / `nxv` \nCác API đều có cấu trúc phản hồi chuẩn:\n```json\n{\n  \"nqt_thanh_cong\": true,\n  \"nqt_du_lieu\": {},\n  \"nqt_thong_diep\": \"Thành công\",\n  \"nqt_loi\": []\n}\n```",
        "contact": {
          "name": "Nguyễn Quang Tâm",
          "email": "nguyenquangtam6666@gmail.com"
        }
      },
      "servers": [
        {
          "url": "/api",
          "description": "API Gateway (Vite Proxy)"
        },
        {
          "url": "http://localhost:5000/api",
          "description": "Flask Backend trực tiếp"
        }
      ],
      "components": {
        "securitySchemes": {
          "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Điền Access Token nhận được sau khi đăng nhập."
          }
        },
        "schemas": {
          "StandardResponse": {
            "type": "object",
            "properties": {
              "nqt_thanh_cong": { "type": "boolean", "example": True },
              "nqt_du_lieu": { "type": "object", "nullable": True },
              "nqt_thong_diep": { "type": "string", "example": "Thao tác thành công" },
              "nqt_loi": { "type": "array", "items": { "type": "string" }, "example": [] }
            }
          },
          "NguoiDung": {
            "type": "object",
            "properties": {
              "g6_ma_nguoi_dung": { "type": "integer", "example": 1 },
              "g6_ho_ten": { "type": "string", "example": "Nguyễn Thị Hoa" },
              "g6_so_dien_thoai": { "type": "string", "example": "0987654321" },
              "g6_email": { "type": "string", "example": "hoa.nguyen@gmail.com" },
              "g6_anh_dai_dien": { "type": "string", "nullable": True },
              "g6_la_hoi_vien": { "type": "boolean", "example": True },
              "g6_la_hoat_dong": { "type": "boolean", "example": True }
            }
          },
          "SanPham": {
            "type": "object",
            "properties": {
              "nxv_ma_san_pham": { "type": "integer", "example": 101 },
              "nxv_ten_san_pham": { "type": "string", "example": "Whey Protein Isolate" },
              "nxv_mo_ta": { "type": "string", "example": "Whey tinh khiết hấp thụ nhanh" },
              "nxv_gia": { "type": "number", "example": 1250000 },
              "nxv_hinh_anh": { "type": "string", "example": "/uploads/products/whey.jpg" }
            }
          }
        }
      },
      "paths": {}
    }

    # Helper function to add a path
    def add_path(route, method, tags, summary, description="", security=False, parameters=None, request_body=None, responses=None):
        if route not in spec["paths"]:
          spec["paths"][route] = {}
        
        path_detail = {
          "tags": tags,
          "summary": summary,
          "description": description
        }
        
        if security:
          path_detail["security"] = [{"BearerAuth": []}]
          
        if parameters:
          path_detail["parameters"] = parameters
          
        if request_body:
          path_detail["requestBody"] = request_body
          
        if responses:
          path_detail["responses"] = responses
        else:
          path_detail["responses"] = {
            "200": {
              "description": "Thành công",
              "content": {
                "application/json": {
                  "schema": {
                    "$ref": "#/components/schemas/StandardResponse"
                  }
                }
              }
            }
          }
          
        spec["paths"][route][method.lower()] = path_detail

    # --- AUTHENTICATION ---
    add_path("/nqt-dang-nhap", "POST", ["Authentication (Quản trị/Nhân viên)"], "Đăng nhập hệ thống quản trị/nhân viên",
             request_body={
               "required": True,
               "content": {
                 "application/json": {
                   "schema": {
                     "type": "object",
                     "required": ["g6_ten_dang_nhap", "g6_mat_khau"],
                     "properties": {
                       "g6_ten_dang_nhap": { "type": "string", "example": "admin" },
                       "g6_mat_khau": { "type": "string", "format": "password", "example": "123456" }
                     }
                   }
                 }
               }
             })

    add_path("/nqt-lam-moi-token", "POST", ["Authentication (Quản trị/Nhân viên)"], "Làm mới Access Token", 
             description="Yêu cầu gửi kèm Refresh Token trong Cookies.")
             
    add_path("/nqt-dang-xuat", "POST", ["Authentication (Quản trị/Nhân viên)"], "Đăng xuất hệ thống")
    
    add_path("/nqt-toi", "GET", ["Authentication (Quản trị/Nhân viên)"], "Lấy thông tin tài khoản nhân viên hiện tại", security=True)

    # --- HỘI VIÊN (PORTAL) ---
    add_path("/nqt-hoi-vien/dang-ky", "POST", ["Hội viên (Portal)"], "Đăng ký tài khoản hội viên mới",
             request_body={
               "required": True,
               "content": {
                 "application/json": {
                   "schema": {
                     "type": "object",
                     "required": ["nqt_ho_ten", "nqt_so_dien_thoai", "nqt_mat_khau"],
                     "properties": {
                       "nqt_ho_ten": { "type": "string", "example": "Nguyễn Văn A" },
                       "nqt_so_dien_thoai": { "type": "string", "example": "0912345678" },
                       "nqt_email": { "type": "string", "example": "member.a@gmail.com" },
                       "nqt_mat_khau": { "type": "string", "example": "123456" },
                       "nqt_ma_chi_nhanh": { "type": "integer", "default": 1 }
                     }
                   }
                 }
               }
             })

    add_path("/nqt-hoi-vien/dang-nhap", "POST", ["Hội viên (Portal)"], "Đăng nhập hội viên",
             request_body={
               "required": True,
               "content": {
                 "application/json": {
                   "schema": {
                     "type": "object",
                     "required": ["nqt_so_dien_thoai", "nqt_mat_khau"],
                     "properties": {
                       "nqt_so_dien_thoai": { "type": "string", "example": "0912345678" },
                       "nqt_mat_khau": { "type": "string", "example": "123456" }
                     }
                   }
                 }
               }
             })

    add_path("/nqt-hoi-vien/google-login", "POST", ["Hội viên (Portal)"], "Đăng nhập bằng Google",
             request_body={
               "required": True,
               "content": {
                 "application/json": {
                   "schema": {
                     "type": "object",
                     "required": ["credential"],
                     "properties": {
                       "credential": { "type": "string", "description": "Google ID Token" }
                     }
                   }
                 }
               }
             })

    add_path("/nqt-hoi-vien/toi", "GET", ["Hội viên (Portal)"], "Lấy hồ sơ cá nhân hội viên", security=True)
    add_path("/nqt-hoi-vien/toi", "PUT", ["Hội viên (Portal)"], "Cập nhật hồ sơ cá nhân hội viên", security=True,
             request_body={
               "required": True,
               "content": {
                 "application/json": {
                   "schema": {
                     "type": "object",
                     "properties": {
                       "g6_ho_ten": { "type": "string", "example": "Nguyễn Văn A" },
                       "g6_email": { "type": "string", "example": "a.nguyen@gmail.com" },
                       "g6_dia_chi": { "type": "string", "example": "123 Cầu Giấy, Hà Nội" },
                       "g6_ngay_sinh": { "type": "string", "format": "date", "example": "1998-05-15" },
                       "g6_gioi_tinh": { "type": "string", "example": "Nam" }
                     }
                   }
                 }
               }
             })

    add_path("/nqt-hoi-vien/toi/nqt-chi-so", "GET", ["Hội viên (Portal)"], "Lấy lịch sử chỉ số cơ thể", security=True,
             parameters=[{
               "name": "g6_gioi_han",
               "in": "query",
               "schema": { "type": "integer", "default": 10 }
             }])

    add_path("/nqt-hoi-vien/diem-danh", "GET", ["Hội viên (Portal)"], "Xem lịch sử điểm danh của tôi", security=True)

    add_path("/nqt-dang-ky-goi-tap", "GET", ["Hội viên (Portal)"], "Lịch sử đăng ký gói tập của tôi", security=True)
    add_path("/nqt-mua-goi-tap", "POST", ["Hội viên (Portal)"], "Đăng ký mua gói tập thành viên", security=True,
             request_body={
               "required": True,
               "content": {
                 "application/json": {
                   "schema": {
                     "type": "object",
                     "required": ["g6_ma_goi_tap"],
                     "properties": {
                       "g6_ma_goi_tap": { "type": "integer", "example": 2 }
                     }
                   }
                 }
               }
             })

    add_path("/nqt-mua-goi-pt", "POST", ["Hội viên (Portal)"], "Đăng ký mua gói PT", security=True,
             request_body={
               "required": True,
               "content": {
                 "application/json": {
                   "schema": {
                     "type": "object",
                     "properties": {
                       "g6_ma_hlv": { "type": "integer", "example": 1 },
                       "g6_ma_goi_pt": { "type": "integer", "example": 1 }
                     }
                   }
                 }
               }
             })

    add_path("/nqt-dat-cho-lop", "POST", ["Hội viên (Portal)"], "Đặt chỗ tham gia lớp học nhóm", security=True,
             request_body={
               "required": True,
               "content": {
                 "application/json": {
                   "schema": {
                     "type": "object",
                     "properties": {
                       "g6_ma_lop_hoc": { "type": "integer", "example": 3 },
                       "g6_ma_lich_lop": { "type": "integer", "example": 5 },
                       "g6_ngay_tap": { "type": "string", "format": "date", "example": "2026-06-03" }
                     }
                   }
                 }
               }
             })

    add_path("/nqt-chatbot", "POST", ["Hội viên (Portal)"], "Trò chuyện với Chatbot hỗ trợ G6 Gym", security=True,
             request_body={
               "required": True,
               "content": {
                 "application/json": {
                   "schema": {
                     "type": "object",
                     "required": ["message"],
                     "properties": {
                       "message": { "type": "string", "example": "Giá gói tập gym 1 tháng là bao nhiêu?" }
                     }
                   }
                 }
               }
             })

    # --- HỘI VIÊN (ADMIN MANAGEMENT) ---
    add_path("/nqt-hoi-vien", "GET", ["Hội viên (Admin/Staff)"], "Lấy danh sách tất cả hội viên (Có phân trang & bộ lọc)", security=True,
             parameters=[
               { "name": "g6_trang", "in": "query", "schema": { "type": "integer", "default": 1 } },
               { "name": "g6_gioi_han", "in": "query", "schema": { "type": "integer", "default": 20 } },
               { "name": "g6_tim_kiem", "in": "query", "schema": { "type": "string" } },
               { "name": "g6_ma_chi_nhanh", "in": "query", "schema": { "type": "integer" } },
               { "name": "g6_trang_thai", "in": "query", "schema": { "type": "string", "example": "true" } }
             ])
    add_path("/nqt-hoi-vien", "POST", ["Hội viên (Admin/Staff)"], "Tạo mới tài khoản hội viên", security=True,
             request_body={
               "required": True,
               "content": {
                 "application/json": {
                   "schema": {
                     "type": "object",
                     "required": ["g6_ho_ten", "g6_so_dien_thoai", "g6_ma_chi_nhanh"],
                     "properties": {
                       "g6_ho_ten": { "type": "string", "example": "Trần Văn B" },
                       "g6_so_dien_thoai": { "type": "string", "example": "0988776655" },
                       "g6_ma_chi_nhanh": { "type": "integer", "example": 1 }
                     }
                   }
                 }
               }
             })
    add_path("/nqt-hoi-vien/{nqt_id}", "GET", ["Hội viên (Admin/Staff)"], "Lấy chi tiết một hội viên", security=True,
             parameters=[{ "name": "nqt_id", "in": "path", "required": True, "schema": { "type": "integer" } }])
    add_path("/nqt-hoi-vien/{nqt_id}", "PUT", ["Hội viên (Admin/Staff)"], "Cập nhật tài khoản hội viên", security=True,
             parameters=[{ "name": "nqt_id", "in": "path", "required": True, "schema": { "type": "integer" } }])
    add_path("/nqt-hoi-vien/{nqt_id}", "DELETE", ["Hội viên (Admin/Staff)"], "Xóa hội viên", security=True,
             parameters=[{ "name": "nqt_id", "in": "path", "required": True, "schema": { "type": "integer" } }])

    # --- DỊCH VỤ CỬA HÀNG / SHOP (PRODUCTS) ---
    add_path("/nxv-danh-muc", "GET", ["Shop & Sản phẩm"], "Danh sách danh mục sản phẩm")
    add_path("/nxv-danh-muc", "POST", ["Shop & Sản phẩm"], "Tạo danh mục mới (Admin)", security=True,
             request_body={
               "required": True,
               "content": {
                 "application/json": {
                   "schema": {
                     "type": "object",
                     "required": ["nxv_ten_danh_muc"],
                     "properties": {
                       "nxv_ten_danh_muc": { "type": "string", "example": "Thực phẩm bổ sung" }
                     }
                   }
                 }
               }
             })

    add_path("/nxv-san-pham", "GET", ["Shop & Sản phẩm"], "Lấy danh sách sản phẩm cửa hàng",
             parameters=[
               { "name": "nxv_danh_muc_id", "in": "query", "schema": { "type": "integer" } },
               { "name": "nxv_tim_kiem", "in": "query", "schema": { "type": "string" } }
             ])
    add_path("/nxv-san-pham", "POST", ["Shop & Sản phẩm"], "Tạo sản phẩm mới (Admin)", security=True)
    add_path("/nxv-san-pham/{nxv_id}", "GET", ["Shop & Sản phẩm"], "Chi tiết sản phẩm",
             parameters=[{ "name": "nxv_id", "in": "path", "required": True, "schema": { "type": "integer" } }])
    add_path("/nxv-san-pham/{nxv_id}", "PUT", ["Shop & Sản phẩm"], "Cập nhật sản phẩm", security=True,
             parameters=[{ "name": "nxv_id", "in": "path", "required": True, "schema": { "type": "integer" } }])
    add_path("/nxv-san-pham/{nxv_id}", "DELETE", ["Shop & Sản phẩm"], "Xóa sản phẩm", security=True,
             parameters=[{ "name": "nxv_id", "in": "path", "required": True, "schema": { "type": "integer" } }])

    # --- ĐƠN HÀNG (ORDERS) ---
    add_path("/nqt-don-hang", "GET", ["Shop & Đơn hàng"], "Lấy lịch sử đơn hàng của tôi", security=True)
    add_path("/nqt-don-hang", "POST", ["Shop & Đơn hàng"], "Tạo đơn mua hàng mới", security=True,
             request_body={
               "required": True,
               "content": {
                 "application/json": {
                   "schema": {
                     "type": "object",
                     "required": ["nxv_chi_tiet"],
                     "properties": {
                       "nxv_ma_khuyen_mai": { "type": "string", "example": "G6NEWYEAR" },
                       "nxv_chi_tiet": {
                         "type": "array",
                         "items": {
                           "type": "object",
                           "properties": {
                             "nxv_ma_bien_the": { "type": "integer", "example": 201 },
                             "nxv_so_luong": { "type": "integer", "example": 2 }
                           }
                         }
                       }
                     }
                   }
                 }
               }
             })

    # --- KHUYẾN MÃI (DISCOUNTS & BANNERS) ---
    add_path("/nqt-ma-giam-gia", "GET", ["Khuyến mãi & Banner"], "Lấy danh sách mã giảm giá hoạt động")
    add_path("/nqt-ma-giam-gia/nqt-kiem-tra", "POST", ["Khuyến mãi & Banner"], "Kiểm tra tính hợp lệ của mã giảm giá", security=True,
             request_body={
               "required": True,
               "content": {
                 "application/json": {
                   "schema": {
                     "type": "object",
                     "required": ["g6_ma_code", "g6_tong_tien"],
                     "properties": {
                       "g6_ma_code": { "type": "string", "example": "G6NEW" },
                       "g6_tong_tien": { "type": "number", "example": 500000 }
                     }
                   }
                 }
               }
             })

    # --- LỚP HỌC & HUẤN LUYỆN VIÊN (CLASSES & TRAINERS) ---
    add_path("/nxv-huan-luyen-vien", "GET", ["Lớp học & HLV (PT)"], "Danh sách PT / Huấn luyện viên")
    add_path("/nxv-lop-hoc", "GET", ["Lớp học & HLV (PT)"], "Danh sách lớp học nhóm")
    add_path("/nxv-su-kien", "GET", ["Sự kiện"], "Danh sách sự kiện tại trung tâm G6 Gym")

    # --- HỆ THỐNG VÀ CẤU HÌNH (ADMIN/STAFF SYSTEM) ---
    add_path("/nqt-cau-hinh", "GET", ["Cấu hình hệ thống"], "Xem toàn bộ cấu hình hệ thống", security=True)
    add_path("/nqt-cau-hinh", "PUT", ["Cấu hình hệ thống"], "Cập nhật cấu hình hàng loạt", security=True)
    add_path("/nqt-cau-hinh/{nqt_khoa}", "GET", ["Cấu hình hệ thống"], "Lấy cấu hình chi tiết theo khóa", security=True,
             parameters=[{ "name": "nqt_khoa", "in": "path", "required": True, "schema": { "type": "string" } }])

    # --- BÁO CÁO & THỐNG KÊ (REPORTS) ---
    add_path("/nqt-thong-ke-dashboard", "GET", ["Báo cáo & Thống kê"], "Xem số liệu tổng quan Dashboard", security=True)
    add_path("/nqt-thong-ke-bieu-do", "GET", ["Báo cáo & Thống kê"], "Dữ liệu biểu đồ tăng trưởng hội viên", security=True,
             parameters=[{ "name": "g6_so_ngay", "in": "query", "schema": { "type": "integer", "default": 7 } }])

    # Write the expanded JSON file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'nqt_openapi.json')
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(spec, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully generated expanded openapi spec at {json_path}")

if __name__ == "__main__":
    generate_openapi()
