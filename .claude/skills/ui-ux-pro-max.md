---
name: ui-ux-pro-max
description: Chế độ UI/UX Pro Max - thiết kế và implement giao diện chuyên nghiệp với TailwindCSS, animations, dark mode, responsive cho NQT Gym
---

# UI/UX PRO MAX MODE - NQT Gym Management

Chế độ **UI/UX PRO MAX**: Implement giao diện đẹp, chuyên nghiệp, accessible và performant với TailwindCSS.

ARGUMENTS: $ARGUMENTS

## Design System NQT Gym

### Bảng màu (lấy từ NqtCauHinh)
```javascript
// Primary: nqt_mau_chu_dao (default: #4CAF50 - Green)
// Secondary: nqt_mau_phu (default: #2196F3 - Blue)
// Neutral: slate-900 / slate-100
// Success: green-500, Warning: amber-500, Error: red-500
```

### Typography Scale
```html
<!-- Heading: font-bold text-2xl md:text-3xl text-slate-900 dark:text-white -->
<!-- Subheading: font-semibold text-lg text-slate-700 dark:text-slate-300 -->
<!-- Body: text-sm text-slate-600 dark:text-slate-400 -->
<!-- Caption: text-xs text-slate-500 -->
```

### Component Library (Copy-paste ready)

#### Card Component
```html
<div class="bg-white dark:bg-slate-800 rounded-2xl shadow-sm border border-slate-200 dark:border-slate-700 p-6 hover:shadow-md transition-shadow">
  <!-- content -->
</div>
```

#### Primary Button
```html
<button class="inline-flex items-center gap-2 px-4 py-2.5 bg-green-600 hover:bg-green-700 active:scale-95 text-white text-sm font-medium rounded-xl transition-all duration-150 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed">
  <svg class="w-4 h-4">...</svg>
  Thêm mới
</button>
```

#### Data Table
```html
<div class="overflow-x-auto rounded-2xl border border-slate-200 dark:border-slate-700">
  <table class="w-full text-sm">
    <thead class="bg-slate-50 dark:bg-slate-900">
      <tr>
        <th class="px-4 py-3 text-left font-semibold text-slate-600 dark:text-slate-400 whitespace-nowrap">
          Tên cột
        </th>
      </tr>
    </thead>
    <tbody class="divide-y divide-slate-100 dark:divide-slate-700">
      <tr class="hover:bg-slate-50 dark:hover:bg-slate-700/50 transition-colors">
        <td class="px-4 py-3 text-slate-800 dark:text-slate-200">...</td>
      </tr>
    </tbody>
  </table>
</div>
```

#### Status Badge
```html
<!-- Active -->
<span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400">
  <span class="w-1.5 h-1.5 rounded-full bg-green-500"></span>
  Hoạt động
</span>
<!-- Inactive -->
<span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium bg-slate-100 text-slate-600 dark:bg-slate-700 dark:text-slate-400">
  Không hoạt động
</span>
```

#### Modal
```html
<div class="fixed inset-0 z-50 flex items-center justify-center p-4" id="nqt-modal">
  <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" onclick="nqtDongModal()"></div>
  <div class="relative bg-white dark:bg-slate-800 rounded-2xl shadow-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto">
    <div class="flex items-center justify-between p-6 border-b border-slate-200 dark:border-slate-700">
      <h3 class="text-lg font-semibold text-slate-900 dark:text-white">Tiêu đề Modal</h3>
      <button onclick="nqtDongModal()" class="p-2 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors">
        <svg class="w-5 h-5 text-slate-500">...</svg>
      </button>
    </div>
    <div class="p-6"><!-- content --></div>
  </div>
</div>
```

#### Toast Notification
```javascript
function nqtHienThiToast(nqtThongDiep, nqtLoai = 'success') {
  const nqtMauSac = {
    success: 'bg-green-600',
    error: 'bg-red-600',
    warning: 'bg-amber-500',
    info: 'bg-blue-600'
  };
  
  const nqtToast = document.createElement('div');
  nqtToast.className = `fixed bottom-4 right-4 z-50 flex items-center gap-3 px-4 py-3 ${nqtMauSac[nqtLoai]} text-white text-sm font-medium rounded-xl shadow-lg translate-y-2 opacity-0 transition-all duration-300`;
  nqtToast.innerHTML = `<span>${nqtThongDiep}</span>`;
  document.body.appendChild(nqtToast);
  
  requestAnimationFrame(() => {
    nqtToast.classList.remove('translate-y-2', 'opacity-0');
  });
  
  setTimeout(() => {
    nqtToast.classList.add('translate-y-2', 'opacity-0');
    setTimeout(() => nqtToast.remove(), 300);
  }, 3000);
}
```

#### Stats Card (Dashboard)
```html
<div class="bg-white dark:bg-slate-800 rounded-2xl p-6 border border-slate-200 dark:border-slate-700">
  <div class="flex items-start justify-between">
    <div>
      <p class="text-sm text-slate-500 dark:text-slate-400">Hội viên active</p>
      <p class="text-3xl font-bold text-slate-900 dark:text-white mt-1">1,234</p>
      <p class="text-xs text-green-600 mt-2 flex items-center gap-1">
        <svg class="w-3 h-3"><!-- arrow up --></svg>
        +12% so với tháng trước
      </p>
    </div>
    <div class="p-3 bg-green-100 dark:bg-green-900/30 rounded-xl">
      <svg class="w-6 h-6 text-green-600 dark:text-green-400"><!-- icon --></svg>
    </div>
  </div>
</div>
```

#### Form Input
```html
<div class="space-y-1.5">
  <label class="text-sm font-medium text-slate-700 dark:text-slate-300">
    Họ tên <span class="text-red-500">*</span>
  </label>
  <input 
    type="text" 
    class="w-full px-3.5 py-2.5 text-sm bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-600 rounded-xl text-slate-900 dark:text-white placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all"
    placeholder="Nguyễn Văn A"
  >
  <p class="text-xs text-red-500 hidden" id="nqt-error-ho-ten">Vui lòng nhập họ tên</p>
</div>
```

## Layout Patterns

### Sidebar + Main Content
```html
<div class="flex h-screen bg-slate-100 dark:bg-slate-900">
  <!-- Sidebar -->
  <aside class="w-64 bg-white dark:bg-slate-800 border-r border-slate-200 dark:border-slate-700 flex-shrink-0">
    <!-- nav items -->
  </aside>
  
  <!-- Main -->
  <main class="flex-1 overflow-auto">
    <div class="p-6 max-w-7xl mx-auto">
      <!-- content -->
    </div>
  </main>
</div>
```

### Page Header
```html
<div class="flex items-center justify-between mb-6">
  <div>
    <h1 class="text-2xl font-bold text-slate-900 dark:text-white">Quản lý Hội viên</h1>
    <p class="text-sm text-slate-500 mt-1">Tổng: 1,234 hội viên</p>
  </div>
  <button class="...">Thêm hội viên</button>
</div>
```

## Dark Mode Support

Tất cả components phải có `dark:` variants. Dùng class `dark` trên `<html>`:
```javascript
// Toggle dark mode
function nqtToggleDarkMode() {
  document.documentElement.classList.toggle('dark');
  localStorage.setItem('nqtDarkMode', 
    document.documentElement.classList.contains('dark'));
}

// Init on load
if (localStorage.getItem('nqtDarkMode') === 'true') {
  document.documentElement.classList.add('dark');
}
```

## Accessibility Checklist
- [ ] `aria-label` trên icon-only buttons
- [ ] `role="dialog"` và `aria-modal="true"` trên modals
- [ ] Focus trap trong modals
- [ ] `alt` text trên images
- [ ] Color contrast ratio ≥ 4.5:1
- [ ] Keyboard navigable (Tab, Enter, Escape)
- [ ] `sr-only` cho screen readers

## Performance
- Lazy load images: `loading="lazy"`
- Debounce search inputs: 300ms
- Virtualize lists > 100 items
- Skeleton loading states thay vì spinner

## Quy tắc UI/UX Pro Max
- Mobile-first: thiết kế mobile trước, expand lên desktop
- Consistent spacing: dùng Tailwind spacing scale (4, 6, 8, 12...)
- Micro-interactions: hover, focus, active states cho mọi interactive element
- Empty states: UI đẹp khi không có data
- Error states: thông báo lỗi rõ ràng, actionable
- Loading states: skeleton screens thay vì blank space
