# TODO - Cải tiến landing page

## Phase 1 — Fix data/render (khớp UI với backend)
- [x] B1: Kiểm tra `frontend/index.html`: services/pricing/testimonials hiện đang có phần DOM placeholder/xuất bản tĩnh cho pricing/testimonials (ví dụ comment placeholder pricing-grid, testimonials có slider tĩnh trong HTML).

- [x] B2: Nhúng/đăng ký `frontend/src/js/landing.js` trong `frontend/index.html` (hoặc tích hợp logic fetch).

- [x] B3: Map lại các id/container trong `index.html` để khớp với `landing.js` (`servicesGrid`, `goiTapList`, `testimonialsList`).



- [x] B4: Bỏ/disable logic testimonial cũ trong `index.html` để tránh xung đột với `landing.js`.




## Phase 2 — Make it prettier (chỉn sang hơn)
- [x] C1: Đồng bộ typography/spacing cho hero (h1/p/CTA) và headings các section.
- [x] C2: Tinh chỉnh overlay/video filter để chữ rõ hơn.
- [x] C3: Tăng độ nổi CTA, chỉnh hover/shadow.
- [x] C4: Services cards & pricing cards: thống nhất height, font-size, line-clamp, và nhịp grid.
- [x] C5: Kiểm tra responsive (mobile <-> desktop), tránh cỡ chữ quá lớn/khó đọc.

## Phase 3 — Validate
- [ ] D1: `npm run dev` và kiểm tra landing chạy đúng data từ `/api/nqt-public/*` (hiện chưa chạy được vì backend đang từ chối kết nối port 5000).
- [x] D2: Kiểm tra console errors (DOM id mismatch, fetch fail).

- [ ] D3: Build/preview (nếu cần): `npm run build`.


