# IRON COMMAND — Style Guide

> Dark/Light fitness management UI. Tailwind CSS + Material Design 3 token system. Hỗ trợ light/dark toggle qua CSS custom properties.

---

## 1. Nguyên tắc thiết kế

- **Dark/Light mode** — toggle qua JS, lưu `localStorage('ic-theme')`. Không có `class="dark"` hardcoded trên `<html>`.
- **Primary là màu chủ đạo**: `#ce3b3b` (Đỏ) cho action, nav active, wordmark.
- **Secondary là màu phụ**: `#518bbd` (Xanh dương) cho accent, hover.
- **Các semantic khác**: xanh mint (positive/data) · cam đào (warning).
- **Góc vuông sắc bén** (border-radius 2–4px mặc định) — giao diện data-dense.
- **Material Design 3 surface layering** — các lớp card dùng `surface-container-*` tăng dần.
- **Không dùng shadow** ngoại trừ featured card, FAB, và hiệu ứng neon glow trên các yếu tố cần nhấn mạnh.
- **Hiệu ứng Neon (Glow)**: Sử dụng các lớp neon glow mờ (box-shadow/text-shadow) màu đỏ (`#ce3b3b`) quanh các CTA button, viền thẻ quan trọng (như thẻ Premium/Popular), và đôi chút ở tiêu đề chính để giao diện hiện đại. Mọi component cần sử dụng class `bg-primary`, `text-primary`, thay vì hardcode class màu mặc định của Tailwind.

---

## 2. Color Palette

### Surface tokens (nền theo độ sâu Z)

| Token | Hex | Dùng cho |
|---|---|---|
| `background` / `surface` / `surface-dim` | `#10131a` | Nền trang, deepest background |
| `surface-container-lowest` | `#0b0e15` | Section xen kẽ (homepage) |
| `surface-container-low` | `#191b23` | — |
| `surface-container` | `#1d2027` | Card, bảng, panel |
| `surface-container-high` | `#272a31` | Card header, elevated state |
| `surface-container-highest` / `surface-variant` | `#32353c` | Table thead, tooltip |
| `surface-bright` | `#363941` | Hover trên surface |

### Text & Border tokens

| Token | Hex | Dùng cho |
|---|---|---|
| `on-surface` | `#e1e2ec` | Body text chính |
| `on-surface-variant` | `#c2c6d6` | Text phụ |
| `outline` | `#8c909f` | Label mờ, secondary text |
| `outline-variant` | `#424754` | Border, divider |

### Accent tokens

| Token | Hex | Semantic |
|---|---|---|
| `primary` | `#ce3b3b` | Màu chủ đạo, số liệu, icon, active state |
| `primary-container` | `rgba(206,59,59,0.1)` | Badge nền, QR block |
| `secondary` | `#518bbd` | Màu phụ, accent, hover |
| `secondary-container` | `rgba(81,139,189,0.1)` | Container xanh dương |
| `tertiary` | `#ffb786` | Cam — warning, expiring, streak |
| `tertiary-container` | `#df7412` | Container cam đậm |
| `error` | `#ffb4ab` | Đỏ mềm — failed, full |
| `error-container` | `#93000a` | Container đỏ đậm |

### Tailwind raw colors (dùng trực tiếp)

| Class | Hex | Vai trò |
|---|---|---|
| `bg-primary` / `text-primary` | `#ce3b3b` | Brand, primary CTA, nav active |
| `bg-secondary` / `text-secondary`| `#518bbd` | Hover, accent |
| `gray-950` | `#030712` | Sidebar nền |
| `gray-900` | `#111827` | Sidebar hover |
| `gray-800` | `#1f2937` | Border chính (nav, sidebar) |

---

## 3. Typography

### Font families

| Mục đích | Family |
|---|---|
| Body, headline, display | **Inter** (wght 400–900) |
| Label caps | **Lexend** (wght 600) |
| Icon | **Material Symbols Outlined** (variable font) |

**Brand wordmark:** `font-black italic tracking-tighter text-blue-500`

### Font size scale (custom Tailwind tokens)

| Token | Size | Weight | Line Height | Letter Spacing |
|---|---|---|---|---|
| `display-xl` | 36px | 800 | 1.2 | -0.02em |
| `headline-lg` | 24px | 700 | 1.3 | -0.01em |
| `headline-md` | 20px | 600 | 1.4 | — |
| `body-base` | 16px | 400 | 1.6 | — |
| `body-sm` | 14px | 400 | 1.5 | — |
| `label-caps` | 12px | 600 | 1 | +0.05em |

> **Label Caps convention:** Tất cả column header, stat label, nav sub-item, tag đều dùng Lexend 12px/600 `uppercase tracking-wide`. Class: `font-label-caps`.

### Hero heading (public pages)

```
text-[48px] md:text-[72px] font-black italic leading-tight tracking-tighter
```

---

## 4. Spacing System (custom Tailwind tokens)

| Token | Value | Dùng cho |
|---|---|---|
| `xs` / `base` | 4px | Khoảng cách nhỏ nhất |
| `sm` | 8px | Padding icon, gap nhỏ |
| `md` | 16px | Padding card |
| `lg` | 24px | Gap giữa section |
| `gutter` | 20px | Gap giữa grid card |
| `xl` | 32px | Padding section lớn |
| `margin` | 40px | Padding ngang trang (md+) |

Page gutter: `px-6` (mobile) → `md:px-margin` (desktop)

---

## 5. Border Radius

| Token | Value | Dùng cho |
|---|---|---|
| `rounded` (DEFAULT) | 2px | Phần lớn admin component |
| `rounded-lg` | 4px | Card admin, input |
| `rounded-xl` | 8px | Card public pages |
| `rounded-full` | 12px | Pill badge |
| `rounded-3xl` (Tailwind default) | 24px | Hero CTA block, image container |

---

## 6. Layout

### Admin layout (tất cả inner pages)

```
Fixed sidebar:  w-60 (240px)  bg-gray-950  border-r border-gray-800
Fixed topbar:   h-16 (64px)   bg-black     border-b border-gray-800  z-40
Main content:   ml-60 pt-16   max-w-7xl mx-auto
```

### Public homepage layout

```
Fixed nav:      h-16  bg-black/95 backdrop-blur
Hero:           min-h-[85vh]  .hero-gradient (ảnh gym + overlay)
Sections:       xen kẽ bg-background (#10131a) và bg-surface-container-lowest (#0b0e15)
```

### Grid patterns

| Mục đích | Grid |
|---|---|
| KPI stat cards | `grid-cols-1 md:grid-cols-4 gap-gutter` |
| Bento grid | `grid-cols-1 lg:grid-cols-12 gap-gutter` với `col-span-4/8` |
| Pricing cards | `grid-cols-1 md:grid-cols-3 gap-8` |
| Schedule weekly | `grid-cols-7 gap-base` |

---

## 7. Components

### Navbar (top bar)

```
bg-black  h-16  border-b border-gray-800  fixed  z-40
Brand: text-blue-500 text-xl font-black italic tracking-tighter
Links: text-gray-400 hover:text-blue-400 transition-colors
```

### Sidebar

```
bg-gray-950  w-60  border-r border-gray-800  fixed  flex-col

Inactive: text-gray-400 px-6 py-3 hover:bg-gray-800 hover:text-white transition-all
Active:   bg-blue-500/10 text-blue-500 border-r-2 border-blue-500
```

### Bottom nav (mobile only)

```
fixed bottom-0  bg-black/95 backdrop-blur-md  border-t border-gray-800  h-16

Active tab:   text-blue-500 bg-blue-500/10 rounded-xl py-1 px-3
Inactive tab: text-gray-500
Label:        text-[10px] uppercase font-bold
```

---

### Buttons

**Primary (solid blue):**
```html
bg-blue-500 text-white px-4 py-2 rounded-lg font-bold active:scale-95 duration-100
```

**Primary hero CTA:**
```html
bg-blue-600 hover:bg-blue-500 px-8 py-4 rounded-xl font-headline-lg
shadow-[0_0_15px_rgba(59,130,246,0.3)]
```

**Secondary (outline):**
```html
border border-blue-500 text-blue-500 rounded-lg hover:bg-blue-500/10 transition-colors
```

**Ghost / neutral:**
```html
bg-surface-container border border-outline-variant hover:bg-surface-variant rounded-lg
```

**Filter chip (active):**
```html
bg-blue-500/10 text-blue-500 border border-blue-500/50 rounded-sm text-xs font-bold
```

**FAB:**
```html
w-14 h-14 rounded-full bg-secondary text-on-secondary-container
shadow-2xl hover:scale-110 active:scale-95 transition-all duration-150
```

---

### KPI / Stat Cards

```html
bg-surface-container border border-outline-variant p-md rounded-lg
flex flex-col justify-between h-32

Label:  font-label-caps text-[10px] text-outline uppercase
Number: font-display-xl text-primary  (xanh dương)
                       text-secondary (mint/tích cực)
                       text-tertiary  (cam/cảnh báo)
Delta:  text-secondary text-xs font-bold (positive)
        text-tertiary  text-xs font-bold (warning)
```

### Content Cards

```html
bg-surface-container border border-outline-variant rounded-lg overflow-hidden
hover:border-blue-500 transition-all

Card header: p-md border-b border-outline-variant flex justify-between items-center
```

**Featured / highlighted card:**
```html
bg-surface-container-high border-2 border-blue-500 p-8 rounded-xl
scale-105 shadow-2xl relative

Badge "POPULAR": absolute bg-blue-500 text-white px-4 py-1 rounded-full text-[10px]
```

---

### Tables

```html
Container: bg-surface-container border border-outline-variant overflow-hidden

thead:  bg-surface-container-highest/20
        font-label-caps text-gray-400 uppercase tracking-widest

tbody:  divide-y divide-outline-variant
        hover:bg-gray-900/40 transition-colors

Action icon: p-1.5 text-gray-500 hover:text-blue-500 hover:bg-blue-500/10 rounded transition-colors
```

---

### Status Badges / Pills

```html
-- Active:    bg-secondary/10 text-secondary border border-secondary/20
-- Warning:   bg-tertiary/10  text-tertiary  border border-tertiary/20
-- Error:     bg-error/10     text-error     border border-error/20
-- Inactive:  bg-gray-800     text-gray-500  border border-gray-700

Tất cả: px-2 py-1 rounded-sm text-[10px] font-black uppercase
```

---

### Schedule Event Cards

```html
-- Standard: bg-surface-container border-l-4 border-primary p-sm rounded-sm
-- Active:   bg-secondary/10      border-l-4 border-secondary
-- Today:    bg-blue-600/10       border-l-4 border-blue-500
-- Empty:    bg-surface p-sm border border-dashed border-outline-variant

Time label: text-xs font-bold text-primary (hoặc màu accent tương ứng)
```

---

### Progress Bars

```html
h-1.5 w-full bg-background rounded-full overflow-hidden

Fill: bg-primary h-full   (hoặc bg-secondary, bg-blue-500)
```

---

### Search Input

```html
bg-background border border-outline-variant text-xs rounded-lg
px-8 py-1.5 focus:border-primary focus:ring-1 focus:ring-primary outline-none

Icon "search" (Material Symbols) absolute, căn trái trong input
```

---

### Avatars

| Variant | Style |
|---|---|
| Table | `w-10 h-10 rounded-sm border border-gray-800 object-cover` |
| Nav/sidebar | `w-10 h-10 rounded-full border border-blue-500` |
| Initials fallback | `w-8 h-8 rounded-full bg-primary-container font-bold text-xs` |
| Online dot | `w-3 h-3 bg-secondary rounded-full border-2 border-surface-container` (absolute -bottom-1 -right-1) |

### Notification dot

```html
absolute top-0 right-0 w-2 h-2 bg-blue-500 rounded-full border-2 border-black
```

---

### CTA / Newsletter Section

```html
bg-blue-600 rounded-3xl p-12 md:p-20 relative overflow-hidden

Input:  bg-blue-700/50 border-none text-white placeholder:text-blue-300
        rounded-xl px-6 py-4 focus:ring-2 focus:ring-white

Button: bg-white text-blue-600 px-8 py-4 rounded-xl font-headline-lg
```

---

### Footer

```html
bg-black border-t border-gray-900 py-12 px-6

Brand:     text-blue-500 font-black italic tracking-tighter text-2xl
Links:     text-gray-500 hover:text-white transition-colors text-sm
Copyright: text-gray-600 text-xs uppercase tracking-widest
```

---

## 8. Hero Section (Public pages)

```css
.hero-gradient {
    background: linear-gradient(to bottom, rgba(0,0,0,0.4), rgba(16,19,26,1)),
                url('<gym-photo>') center / cover no-repeat;
}
```

Overlay fade từ semi-transparent → `#10131a` để blend liền mạch vào nội dung trang.

---

## 9. Icons

**Material Symbols Outlined** — variable font.

```css
.material-symbols-outlined {
    font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
}
```

Dùng filled variant bằng inline style:
```html
<span class="material-symbols-outlined" style="font-variation-settings:'FILL' 1">icon_name</span>
```

Background watermark icon:
```html
absolute opacity-10 text-[120px] (decorative, không tương tác)
```

Live indicator:
```html
w-2 h-2 bg-secondary rounded-full animate-pulse
```

---

## 10. Animation & Interaction

| Pattern | Class |
|---|---|
| Button press | `active:scale-95 duration-100` |
| Color transition | `transition-colors` |
| General transition | `transition-all duration-200` |
| Card border hover | `hover:border-blue-500 transition-all` |
| Image B&W reveal | `grayscale hover:grayscale-0 transition-all duration-700` |
| FAB hover | `hover:scale-110 active:scale-95 transition-all duration-150` |
| Live dot | `animate-pulse` |
| Theme transition | `transition: background-color 0.25s, color 0.25s` |
| Neon Glow Button | Thêm class `.neon-button` (tạo box-shadow 15-25px màu primary #ce3b3b) |
| Neon Glow Text | Thêm class `.neon-text` (tạo text-shadow 10px màu primary) |
| Neon Glow Border | Thêm class `.neon-border` (tạo box-shadow viền màu primary) |

---

## 11. Light / Dark Mode

### Cơ chế

- **CSS Custom Properties** — `:root` định nghĩa light values, `.dark` (trên `<html>`) override sang dark values.
- **Không dùng Tailwind `dark:` prefix** — thay vào đó, dùng CSS var overrides với `!important` để ghi đè các class Tailwind hardcoded.
- **Lưu preference**: `localStorage.getItem('ic-theme')` → `'light'` | `'dark'`.
- **OS fallback**: `window.matchMedia('(prefers-color-scheme: dark)')` nếu chưa có saved preference.
- **No FOUC**: IIFE script chạy trước khi DOM render, set `.dark` class ngay lập tức.

### CSS Variable System

```css
:root {
    --bg-page: #f0f2f5;
    --bg-sidebar: #ffffff;
    --bg-header: rgba(255,255,255,0.97);
    --bg-surface: #ffffff;
    --bg-surface-low: #f5f6fa;
    --bg-surface-high: #eaecf0;
    --bg-surface-highest: #dde0e7;
    --text-main: #111827;
    --text-secondary: #4b5563;
    --text-muted: #9ca3af;
    --border-main: #e5e7eb;
    --border-muted: #d1d5db;
    --primary-color: #3b82f6;
    --sidebar-border: #e5e7eb;
    --nav-text: #374151;
    --nav-text-muted: #9ca3af;
    --nav-active-bg: rgba(59,130,246,0.1);
    --nav-active-text: #1d4ed8;
    --nav-hover-bg: #f3f4f6;
    --nav-hover-text: #111827;
    --accent-green: #10b981;
    --accent-orange: #f97316;
    --accent-red: #ef4444;
}
.dark {
    --bg-page: #10131a;
    --bg-sidebar: #0f1117;
    --bg-header: rgba(0,0,0,0.95);
    --bg-surface: #1d2027;
    --bg-surface-low: #191b23;
    --bg-surface-high: #272a31;
    --bg-surface-highest: #32353c;
    --text-main: #e1e2ec;
    --text-secondary: #c2c6d6;
    --text-muted: #8c909f;
    --border-main: #32353c;
    --border-muted: #424754;
    --primary-color: #adc6ff;
    --sidebar-border: #1f2937;
    --nav-text: #9ca3af;
    --nav-text-muted: #6b7280;
    --nav-active-bg: rgba(59,130,246,0.1);
    --nav-active-text: #60a5fa;
    --nav-hover-bg: rgba(255,255,255,0.05);
    --nav-hover-text: #e5e7eb;
    --accent-green: #4edea3;
    --accent-orange: #ffb786;
    --accent-red: #ffb4ab;
}
body {
    background-color: var(--bg-page) !important;
    color: var(--text-main) !important;
    transition: background-color 0.25s, color 0.25s;
}
/* Override hardcoded Tailwind classes */
aside { background-color: var(--bg-sidebar) !important; border-right-color: var(--sidebar-border) !important; }
header { background-color: var(--bg-header) !important; border-bottom-color: var(--border-main) !important; }
.bg-black { background-color: var(--bg-sidebar) !important; }
.bg-black\/95, .bg-black\/90 { background-color: var(--bg-header) !important; }
.bg-gray-950 { background-color: var(--bg-sidebar) !important; }
.bg-gray-900 { background-color: var(--bg-surface-high) !important; }
.bg-gray-800 { background-color: var(--bg-surface-highest) !important; }
.border-gray-800, .border-gray-900 { border-color: var(--border-main) !important; }
.text-white { color: var(--text-main) !important; }
.text-gray-400 { color: var(--text-secondary) !important; }
.text-gray-500, .text-gray-600 { color: var(--text-muted) !important; }
```

### Toggle Script (IIFE — đặt trước `</head>`)

```html
<script>
(function(){
  var saved = localStorage.getItem('ic-theme');
  var prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  if (saved === 'dark' || (!saved && prefersDark)) {
    document.documentElement.classList.add('dark');
  }
  document.addEventListener('DOMContentLoaded', function() {
    var toggleBtn = document.createElement('button');
    toggleBtn.id = 'ic-theme-toggle';
    toggleBtn.title = 'Toggle light/dark mode';
    toggleBtn.className = 'material-symbols-outlined hover:text-blue-400 transition-colors cursor-pointer';
    toggleBtn.textContent = 'contrast';
    toggleBtn.style.cssText = 'background:none;border:none;padding:0;font-size:24px;color:var(--nav-text-muted)';
    toggleBtn.addEventListener('click', function() {
      document.documentElement.classList.toggle('dark');
      localStorage.setItem('ic-theme', document.documentElement.classList.contains('dark') ? 'dark' : 'light');
    });
    var header = document.querySelector('header');
    if (header) {
      var notifBtn = header.querySelector('.material-symbols-outlined');
      if (notifBtn && notifBtn.parentElement) {
        notifBtn.parentElement.insertBefore(toggleBtn, notifBtn);
      } else { header.appendChild(toggleBtn); }
    }
  });
})();
</script>
```

### Toggle Button

```
Icon: Material Symbols — `contrast`
Vị trí: inject vào header, trước notification icon
Style: background:none; font-size:24px; color:var(--nav-text-muted)
```

