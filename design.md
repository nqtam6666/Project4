# NQT Gym — Design System & UI Specification

## Design Philosophy

**Dark Luxury + Neon Accent** — Phong cách gym cao cấp quốc tế 2025.  
Tối giản, mạnh mẽ, mượt mà. Mỗi element đều có chủ đích.

---

## Color Palette

```css
:root {
    /* --- Nền --- */
    --nqt-den:        #0A0A0F;   /* Nền trang chính */
    --nqt-den-2:      #12121A;   /* Nền card, modal */
    --nqt-den-3:      #1C1C28;   /* Hover, border mờ */

    /* --- Accent --- */
    --nqt-neon:       #C8F135;   /* Lime neon - accent chính */
    --nqt-neon-dim:   #A8D120;   /* Neon tối hơn - hover */
    --nqt-neon-glow:  rgba(200, 241, 53, 0.15); /* Glow effect */

    /* --- Text --- */
    --nqt-trang:      #F5F5F0;   /* Text chính */
    --nqt-trang-2:    #A1A1AA;   /* Text phụ */
    --nqt-xam:        #52525B;   /* Text mờ, placeholder */

    /* --- Semantic --- */
    --nqt-do:         #EF4444;   /* Lỗi */
    --nqt-xanh-la:    #22C55E;   /* Thành công */
    --nqt-vang:       #F59E0B;   /* Cảnh báo */
    --nqt-xanh-duong: #3B82F6;   /* Info */

    /* --- Border --- */
    --nqt-border:     rgba(255, 255, 255, 0.06);
    --nqt-border-neon: rgba(200, 241, 53, 0.3);
}
```

> **Lưu ý**: Các giá trị trên là **fallback**. Màu sắc thực tế lấy từ `NqtDichVuCauHinh` qua API, gán vào CSS variables tại runtime.

---

## Typography

```css
/* Font */
--nqt-font-display: 'Inter', system-ui, sans-serif;
--nqt-font-mono:    'JetBrains Mono', monospace;  /* Giá, số liệu */

/* Scale */
--nqt-text-xs:   0.75rem;    /* 12px */
--nqt-text-sm:   0.875rem;   /* 14px */
--nqt-text-base: 1rem;       /* 16px */
--nqt-text-lg:   1.125rem;   /* 18px */
--nqt-text-xl:   1.25rem;    /* 20px */
--nqt-text-2xl:  1.5rem;     /* 24px */
--nqt-text-3xl:  1.875rem;   /* 30px */
--nqt-text-4xl:  2.25rem;    /* 36px */
--nqt-text-5xl:  3rem;       /* 48px */
--nqt-text-hero: 5.5rem;     /* 88px - Hero heading */

/* Weight */
--nqt-regular:   400;
--nqt-medium:    500;
--nqt-semibold:  600;
--nqt-bold:      700;
--nqt-black:     900;   /* Hero, display headings */

/* Hero heading */
.nqt-hero-title {
    font-size: var(--nqt-text-hero);
    font-weight: var(--nqt-black);
    letter-spacing: -3px;
    line-height: 0.95;
    text-transform: uppercase;
}
```

---

## Spacing & Border Radius

```css
/* Spacing scale (8px base) */
--nqt-sp-1:  0.25rem;   /* 4px  */
--nqt-sp-2:  0.5rem;    /* 8px  */
--nqt-sp-3:  0.75rem;   /* 12px */
--nqt-sp-4:  1rem;      /* 16px */
--nqt-sp-6:  1.5rem;    /* 24px */
--nqt-sp-8:  2rem;      /* 32px */
--nqt-sp-12: 3rem;      /* 48px */
--nqt-sp-16: 4rem;      /* 64px */
--nqt-sp-24: 6rem;      /* 96px */

/* Border radius */
--nqt-radius-sm: 8px;
--nqt-radius:    16px;
--nqt-radius-lg: 24px;
--nqt-radius-xl: 32px;
--nqt-radius-pill: 100px;
```

---

## Shadows & Glow

```css
/* Card shadow */
--nqt-shadow:      0 4px 24px rgba(0, 0, 0, 0.4);
--nqt-shadow-lg:   0 8px 48px rgba(0, 0, 0, 0.6);

/* Neon glow */
--nqt-glow-sm:   0 0 12px var(--nqt-neon-glow);
--nqt-glow:      0 0 24px var(--nqt-neon-glow);
--nqt-glow-lg:   0 0 48px var(--nqt-neon-glow);

/* Neon border glow */
.nqt-neon-border {
    border: 1px solid var(--nqt-border-neon);
    box-shadow: 0 0 24px var(--nqt-neon-glow),
                inset 0 0 24px rgba(200, 241, 53, 0.03);
}
```

---

## Components

### Button

```css
/* Base */
.nqt-btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 14px 28px;
    border-radius: var(--nqt-radius-pill);
    font-weight: var(--nqt-semibold);
    font-size: var(--nqt-text-sm);
    letter-spacing: 0.3px;
    cursor: pointer;
    transition: all 0.25s var(--nqt-transition);
    white-space: nowrap;
    border: none;
    outline: none;
}

/* Primary - Neon */
.nqt-btn-primary {
    background: var(--nqt-neon);
    color: #0A0A0F;
    font-weight: var(--nqt-bold);
}
.nqt-btn-primary:hover {
    background: var(--nqt-neon-dim);
    transform: scale(1.03);
    box-shadow: var(--nqt-glow);
}

/* Outline */
.nqt-btn-outline {
    background: transparent;
    color: var(--nqt-trang);
    border: 1px solid var(--nqt-border);
}
.nqt-btn-outline:hover {
    border-color: var(--nqt-neon);
    color: var(--nqt-neon);
    box-shadow: var(--nqt-glow-sm);
}

/* Ghost */
.nqt-btn-ghost {
    background: transparent;
    color: var(--nqt-trang-2);
}
.nqt-btn-ghost:hover {
    color: var(--nqt-trang);
    background: var(--nqt-den-3);
}
```

### Card

```css
.nqt-card {
    background: var(--nqt-den-2);
    border: 1px solid var(--nqt-border);
    border-radius: var(--nqt-radius-lg);
    padding: var(--nqt-sp-6);
    transition: all 0.3s var(--nqt-transition);
}
.nqt-card:hover {
    transform: translateY(-8px);
    border-color: var(--nqt-border-neon);
    box-shadow: var(--nqt-shadow-lg), var(--nqt-glow-sm);
}

/* Card featured (gói phổ biến) */
.nqt-card-featured {
    border-color: var(--nqt-neon);
    box-shadow: var(--nqt-glow);
    transform: scale(1.05);
}
```

### Badge

```css
.nqt-badge {
    display: inline-flex;
    align-items: center;
    padding: 4px 12px;
    border-radius: var(--nqt-radius-pill);
    font-size: var(--nqt-text-xs);
    font-weight: var(--nqt-semibold);
    letter-spacing: 0.5px;
    text-transform: uppercase;
}
.nqt-badge-neon {
    background: rgba(200, 241, 53, 0.1);
    color: var(--nqt-neon);
    border: 1px solid rgba(200, 241, 53, 0.3);
}
```

### Input (Floating Label)

```css
.nqt-field {
    position: relative;
    margin-bottom: var(--nqt-sp-6);
}
.nqt-input {
    width: 100%;
    background: transparent;
    border: none;
    border-bottom: 1px solid var(--nqt-border);
    color: var(--nqt-trang);
    padding: 20px 0 10px;
    font-size: var(--nqt-text-base);
    transition: border-color 0.25s;
    outline: none;
}
.nqt-input:focus {
    border-bottom-color: var(--nqt-neon);
    box-shadow: 0 1px 0 var(--nqt-neon);
}
.nqt-label {
    position: absolute;
    top: 20px;
    left: 0;
    color: var(--nqt-xam);
    font-size: var(--nqt-text-base);
    transition: all 0.2s var(--nqt-transition);
    pointer-events: none;
}
.nqt-input:focus ~ .nqt-label,
.nqt-input:not(:placeholder-shown) ~ .nqt-label {
    top: 0;
    font-size: var(--nqt-text-xs);
    color: var(--nqt-neon);
    letter-spacing: 0.5px;
}
```

---

## Animations

```css
/* Easing */
--nqt-transition: cubic-bezier(0.4, 0, 0.2, 1);
--nqt-spring:     cubic-bezier(0.34, 1.56, 0.64, 1);

/* Fade up - reveal khi scroll */
@keyframes nqtFadeUp {
    from { opacity: 0; transform: translateY(32px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* Glow pulse */
@keyframes nqtGlowPulse {
    0%, 100% { box-shadow: 0 0 20px var(--nqt-neon-glow); }
    50%       { box-shadow: 0 0 48px rgba(200, 241, 53, 0.3); }
}

/* Float lên xuống */
@keyframes nqtFloat {
    0%, 100% { transform: translateY(0); }
    50%       { transform: translateY(-12px); }
}

/* Gradient shift - hero background */
@keyframes nqtGradientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Marquee - testimonials */
@keyframes nqtMarquee {
    from { transform: translateX(0); }
    to   { transform: translateX(-50%); }
}
@keyframes nqtMarqueeReverse {
    from { transform: translateX(-50%); }
    to   { transform: translateX(0); }
}

/* Flip clock - countdown */
@keyframes nqtFlipDown {
    0%   { transform: rotateX(0deg); }
    100% { transform: rotateX(-90deg); }
}

/* Reveal class */
.nqt-reveal {
    opacity: 0;
    transform: translateY(32px);
    transition: opacity 0.6s var(--nqt-transition),
                transform 0.6s var(--nqt-transition);
}
.nqt-reveal.nqt-hien-thi { opacity: 1; transform: none; }

/* Stagger delays */
.nqt-reveal:nth-child(1) { transition-delay: 0ms; }
.nqt-reveal:nth-child(2) { transition-delay: 100ms; }
.nqt-reveal:nth-child(3) { transition-delay: 200ms; }
.nqt-reveal:nth-child(4) { transition-delay: 300ms; }
```

---

## Section Layouts

### Navbar — Glassmorphism
- `backdrop-filter: blur(20px)` + `background: rgba(10,10,15,0.8)`
- `border-bottom: 1px solid var(--nqt-border)`
- Sticky, scroll > 80px: thu nhỏ padding + tăng blur
- Mobile: hamburger → slide-down menu với stagger animation

### Hero — Full Viewport
- Min-height: `100dvh`
- Background: animated mesh gradient
- Ảnh VĐV: `clip-path: polygon(8% 0, 100% 0, 100% 100%, 0% 100%)` — lệch chéo
- 20 floating particles bằng CSS (`position: absolute`, random animation-delay)
- Counter animate `0 → giá trị thực` với `requestAnimationFrame`

### Gói Tập — Bento Grid
- Desktop: 3 cột, card giữa scale 1.05 + neon border
- Mobile: 1 cột, featured card first
- Toggle Monthly/Yearly: pill switch, giá đổi với transition

### Huấn Luyện Viên — Drag Scroll
- `overflow-x: hidden`, inner track `display: flex`
- Drag: `pointerdown/pointermove/pointerup` events
- `cursor: grab` → `cursor: grabbing` khi kéo
- Ảnh: `filter: grayscale(1)` → `grayscale(0)` khi hover

### Testimonials — Infinite Marquee
- 2 hàng chạy ngược chiều
- Duplicate content để loop liền mạch (nối 2 lần)
- `animation-play-state: paused` khi hover

### Form Liên Hệ
- Floating label animate
- Validate client-side trước `fetch POST`
- Success: checkmark SVG stroke-dashoffset animation

---

## Glassmorphism Pattern

```css
.nqt-glass {
    background: rgba(18, 18, 26, 0.7);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: var(--nqt-radius-lg);
}
```

---

## Responsive Breakpoints (Mobile-First)

```css
/* Tailwind custom config */
screens: {
    'sm':  '640px',
    'md':  '768px',
    'lg':  '1024px',
    'xl':  '1280px',
    '2xl': '1536px',
}

/* Hero font scale */
@media (max-width: 768px) {
    .nqt-hero-title { font-size: 3rem; letter-spacing: -1px; }
}
@media (min-width: 768px) and (max-width: 1024px) {
    .nqt-hero-title { font-size: 4.5rem; letter-spacing: -2px; }
}
```

---

## Performance Rules

| Rule | Áp dụng |
|------|---------|
| `will-change: transform` | Chỉ cho animated elements, bỏ sau khi xong |
| `loading="lazy"` | Tất cả ảnh dưới fold |
| IntersectionObserver | Thay scroll event listener |
| `requestAnimationFrame` | CountUp counter |
| CSS animation ưu tiên | Thay JS animation khi có thể |
| Font preload | Inter từ Google Fonts |
| `overflow: hidden` trên container | Trước khi scale ảnh khi hover |

---

## File Structure

```
frontend/
├── static/
│   ├── css/
│   │   ├── input.css        # @tailwind directives + custom CSS vars
│   │   └── output.css       # Generated — không commit
│   ├── js/
│   │   ├── nqtLandingPage.js      # Entry point, init
│   │   ├── nqtAnimations.js       # IntersectionObserver, countUp, reveal
│   │   ├── nqtComponents.js       # Navbar, drag scroll, marquee
│   │   └── nqtApi.js              # Fetch wrappers, error handling
│   └── uploads/
│       ├── avatars/
│       ├── products/
│       ├── branches/
│       └── logo/
└── templates/
    └── nqt_landing.html
```

---

## API Calls — Landing Page

| Section | Endpoint | Method |
|---------|----------|--------|
| Config/Theme | `/nqt-cau-hinh` | GET |
| Gói tập | `/nqt-goi-tap?nqt_trang_thai=active` | GET |
| Huấn luyện viên | `/nxv-huan-luyen-vien?nqt_gioi_thieu=true` | GET |
| Chi nhánh | `/nqt-chi-nhanh` | GET |
| Khuyến mãi | `/nqt-khuyen-mai?nqt_trang_thai=active` | GET |
| Blog | `/nqt-blog?nqt_gioi_han=3` | GET |
| Đánh giá | `/nqt-danh-gia?nqt_hien_thi=true` | GET |
| Liên hệ | `/nqt-lien-he` | POST |

### Response format chuẩn

```json
{
  "nqt_thanh_cong": true,
  "nqt_du_lieu": [],
  "nqt_thong_diep": "Thành công",
  "nqt_loi": []
}
```

---

## Checklist trước khi build

- [ ] Không dùng ảnh placeholder URL ngoài (`placehold.co`, `picsum`, v.v.)
- [ ] Không hardcode tên phòng gym, SĐT, địa chỉ — đọc từ API
- [ ] Tất cả biến JS prefix `nqt`, hàm `nqtTenHam()`
- [ ] Loading skeleton cho mỗi section khi fetch
- [ ] Fallback UI khi API lỗi — không crash trang
- [ ] Test mobile: 375px, 390px, 430px
- [ ] Test tablet: 768px, 1024px
- [ ] Lighthouse score: Performance ≥ 90
