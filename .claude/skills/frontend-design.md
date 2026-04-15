---
name: frontend-design
description: Thiết kế frontend theo chuẩn shadcn/ui - component patterns, theming, dark mode, accessibility cho NQT Gym với TailwindCSS vanilla JS
---

# FRONTEND DESIGN - SHADCN/UI STYLE

Skill thiết kế frontend theo chuẩn **shadcn/ui**: clean, composable, accessible components với TailwindCSS.

ARGUMENTS: $ARGUMENTS

## Triết lý thiết kế (shadcn/ui Philosophy)

### Open Code
- Component code được copy trực tiếp, không phải import từ package
- Dễ dàng customize theo nhu cầu project
- AI-ready: code dễ đọc, dễ hiểu

### Composition Pattern
- Component nhỏ, tái sử dụng
- Interface nhất quán giữa các component
- Predictable behavior

### Styling Approach
- Sử dụng CSS Variables cho theming
- TailwindCSS utilities
- Semantic color tokens (background, foreground, primary, muted...)

---

## CSS Variables & Theming

### Base Theme Variables
```css
:root {
  /* Background & Foreground */
  --background: 0 0% 100%;
  --foreground: 222.2 84% 4.9%;

  /* Card */
  --card: 0 0% 100%;
  --card-foreground: 222.2 84% 4.9%;

  /* Popover */
  --popover: 0 0% 100%;
  --popover-foreground: 222.2 84% 4.9%;

  /* Primary - Main action color */
  --primary: 222.2 47.4% 11.2%;
  --primary-foreground: 210 40% 98%;

  /* Secondary */
  --secondary: 210 40% 96.1%;
  --secondary-foreground: 222.2 47.4% 11.2%;

  /* Muted - Subtle backgrounds */
  --muted: 210 40% 96.1%;
  --muted-foreground: 215.4 16.3% 46.9%;

  /* Accent - Hover states */
  --accent: 210 40% 96.1%;
  --accent-foreground: 222.2 47.4% 11.2%;

  /* Destructive - Error/Delete */
  --destructive: 0 84.2% 60.2%;
  --destructive-foreground: 210 40% 98%;

  /* Border & Input */
  --border: 214.3 31.8% 91.4%;
  --input: 214.3 31.8% 91.4%;
  --ring: 222.2 84% 4.9%;

  /* Radius */
  --radius: 0.5rem;
}

.dark {
  --background: 222.2 84% 4.9%;
  --foreground: 210 40% 98%;
  --card: 222.2 84% 4.9%;
  --card-foreground: 210 40% 98%;
  --popover: 222.2 84% 4.9%;
  --popover-foreground: 210 40% 98%;
  --primary: 210 40% 98%;
  --primary-foreground: 222.2 47.4% 11.2%;
  --secondary: 217.2 32.6% 17.5%;
  --secondary-foreground: 210 40% 98%;
  --muted: 217.2 32.6% 17.5%;
  --muted-foreground: 215 20.2% 65.1%;
  --accent: 217.2 32.6% 17.5%;
  --accent-foreground: 210 40% 98%;
  --destructive: 0 62.8% 30.6%;
  --destructive-foreground: 210 40% 98%;
  --border: 217.2 32.6% 17.5%;
  --input: 217.2 32.6% 17.5%;
  --ring: 212.7 26.8% 83.9%;
}
```

### NQT Gym Custom Theme (TailwindCSS Classes)
```css
/* Light Mode Colors - Use directly as Tailwind classes */
/* Background: bg-white, bg-[#FAFAF9], bg-slate-50 */
/* Text: text-[#191919], text-slate-600, text-slate-500 */
/* Border: border-[#e5e5e5], border-slate-200 */

/* Dark Mode - Add dark: prefix */
/* Background: dark:bg-[#1a1a1a], dark:bg-[#262626], dark:bg-slate-800 */
/* Text: dark:text-[#fafafa], dark:text-slate-300, dark:text-slate-400 */
/* Border: dark:border-[#404040], dark:border-slate-700 */
```

---

## Component Library (Vanilla JS + TailwindCSS)

### Button Variants
```html
<!-- Default -->
<button class="inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 bg-[#191919] text-white shadow hover:bg-[#191919]/90 dark:bg-[#fafafa] dark:text-[#191919] dark:hover:bg-[#fafafa]/90 h-9 px-4 py-2">
  Button
</button>

<!-- Secondary -->
<button class="inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 bg-[#f5f5f5] text-[#191919] shadow-sm hover:bg-[#e5e5e5] dark:bg-[#262626] dark:text-[#fafafa] dark:hover:bg-[#333] h-9 px-4 py-2">
  Secondary
</button>

<!-- Outline -->
<button class="inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 border border-[#e5e5e5] bg-transparent shadow-sm hover:bg-[#f5f5f5] hover:text-[#191919] dark:border-[#404040] dark:hover:bg-[#262626] dark:hover:text-[#fafafa] h-9 px-4 py-2">
  Outline
</button>

<!-- Ghost -->
<button class="inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 hover:bg-[#f5f5f5] hover:text-[#191919] dark:hover:bg-[#262626] dark:hover:text-[#fafafa] h-9 px-4 py-2">
  Ghost
</button>

<!-- Destructive -->
<button class="inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 bg-[#dc2626] text-white shadow-sm hover:bg-[#dc2626]/90 h-9 px-4 py-2">
  Delete
</button>

<!-- Icon Button -->
<button class="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 hover:bg-[#f5f5f5] dark:hover:bg-[#262626] h-9 w-9">
  <i class="fas fa-plus"></i>
</button>
```

### Card
```html
<div class="rounded-lg border border-[#e5e5e5] dark:border-[#404040] bg-white dark:bg-[#262626] text-[#191919] dark:text-[#fafafa] shadow-sm">
  <div class="flex flex-col space-y-1.5 p-6">
    <h3 class="font-semibold leading-none tracking-tight">Card Title</h3>
    <p class="text-sm text-[#666] dark:text-[#888]">Card description</p>
  </div>
  <div class="p-6 pt-0">
    <!-- Content -->
  </div>
  <div class="flex items-center p-6 pt-0">
    <!-- Footer -->
  </div>
</div>
```

### Input
```html
<input type="text"
  class="flex h-9 w-full rounded-md border border-[#e5e5e5] dark:border-[#404040] bg-transparent px-3 py-1 text-sm shadow-sm transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-[#a3a3a3] focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-[#191919] dark:focus-visible:ring-[#fafafa] disabled:cursor-not-allowed disabled:opacity-50 dark:text-[#fafafa]"
  placeholder="Enter text...">
```

### Select
```html
<select class="flex h-9 w-full items-center justify-between whitespace-nowrap rounded-md border border-[#e5e5e5] dark:border-[#404040] bg-transparent px-3 py-2 text-sm shadow-sm ring-offset-background placeholder:text-[#a3a3a3] focus:outline-none focus:ring-1 focus:ring-[#191919] dark:focus:ring-[#fafafa] disabled:cursor-not-allowed disabled:opacity-50 dark:text-[#fafafa]">
  <option value="">Select option...</option>
  <option value="1">Option 1</option>
  <option value="2">Option 2</option>
</select>
```

### Dialog/Modal
```html
<div class="fixed inset-0 z-50 bg-black/80 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0" id="nqtOverlay"></div>
<div class="fixed left-[50%] top-[50%] z-50 grid w-full max-w-lg translate-x-[-50%] translate-y-[-50%] gap-4 border border-[#e5e5e5] dark:border-[#404040] bg-white dark:bg-[#262626] p-6 shadow-lg duration-200 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[state=closed]:slide-out-to-left-1/2 data-[state=closed]:slide-out-to-top-[48%] data-[state=open]:slide-in-from-left-1/2 data-[state=open]:slide-in-from-top-[48%] sm:rounded-lg">
  <div class="flex flex-col space-y-1.5 text-center sm:text-left">
    <h2 class="text-lg font-semibold leading-none tracking-tight text-[#191919] dark:text-[#fafafa]">Dialog Title</h2>
    <p class="text-sm text-[#666] dark:text-[#888]">Dialog description</p>
  </div>
  <div class="grid gap-4 py-4">
    <!-- Content -->
  </div>
  <div class="flex flex-col-reverse sm:flex-row sm:justify-end sm:space-x-2">
    <button class="...">Cancel</button>
    <button class="...">Save</button>
  </div>
  <button class="absolute right-4 top-4 rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:pointer-events-none">
    <i class="fas fa-times h-4 w-4"></i>
    <span class="sr-only">Close</span>
  </button>
</div>
```

### Table
```html
<div class="relative w-full overflow-auto">
  <table class="w-full caption-bottom text-sm">
    <thead class="[&_tr]:border-b border-[#e5e5e5] dark:border-[#404040]">
      <tr class="border-b transition-colors hover:bg-[#f5f5f5]/50 dark:hover:bg-[#262626]/50">
        <th class="h-10 px-4 text-left align-middle font-medium text-[#666] dark:text-[#888]">Name</th>
        <th class="h-10 px-4 text-left align-middle font-medium text-[#666] dark:text-[#888]">Status</th>
        <th class="h-10 px-4 text-right align-middle font-medium text-[#666] dark:text-[#888]">Actions</th>
      </tr>
    </thead>
    <tbody class="[&_tr:last-child]:border-0">
      <tr class="border-b border-[#e5e5e5] dark:border-[#404040] transition-colors hover:bg-[#f5f5f5]/50 dark:hover:bg-[#262626]/50">
        <td class="p-4 align-middle text-[#191919] dark:text-[#fafafa]">Item</td>
        <td class="p-4 align-middle">
          <span class="inline-flex items-center rounded-md bg-green-50 dark:bg-green-500/10 px-2 py-1 text-xs font-medium text-green-700 dark:text-green-400 ring-1 ring-inset ring-green-600/20">Active</span>
        </td>
        <td class="p-4 align-middle text-right">
          <button class="..."><i class="fas fa-edit"></i></button>
        </td>
      </tr>
    </tbody>
  </table>
</div>
```

### Badge
```html
<!-- Default -->
<span class="inline-flex items-center rounded-md border border-[#e5e5e5] dark:border-[#404040] px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 text-[#191919] dark:text-[#fafafa]">
  Badge
</span>

<!-- Success -->
<span class="inline-flex items-center rounded-md bg-green-50 dark:bg-green-500/10 px-2.5 py-0.5 text-xs font-semibold text-green-700 dark:text-green-400 ring-1 ring-inset ring-green-600/20">
  Active
</span>

<!-- Warning -->
<span class="inline-flex items-center rounded-md bg-yellow-50 dark:bg-yellow-500/10 px-2.5 py-0.5 text-xs font-semibold text-yellow-700 dark:text-yellow-400 ring-1 ring-inset ring-yellow-600/20">
  Pending
</span>

<!-- Destructive -->
<span class="inline-flex items-center rounded-md bg-red-50 dark:bg-red-500/10 px-2.5 py-0.5 text-xs font-semibold text-red-700 dark:text-red-400 ring-1 ring-inset ring-red-600/20">
  Error
</span>
```

### Skeleton Loading
```html
<div class="space-y-3">
  <div class="h-4 w-3/4 animate-pulse rounded-md bg-[#e5e5e5] dark:bg-[#404040]"></div>
  <div class="h-4 w-1/2 animate-pulse rounded-md bg-[#e5e5e5] dark:bg-[#404040]"></div>
  <div class="h-4 w-5/6 animate-pulse rounded-md bg-[#e5e5e5] dark:bg-[#404040]"></div>
</div>
```

### Avatar
```html
<div class="relative flex h-10 w-10 shrink-0 overflow-hidden rounded-full">
  <img class="aspect-square h-full w-full" src="/avatar.jpg" alt="Avatar">
</div>

<!-- Fallback với initials -->
<div class="relative flex h-10 w-10 shrink-0 overflow-hidden rounded-full bg-[#f5f5f5] dark:bg-[#262626]">
  <span class="flex h-full w-full items-center justify-center rounded-full bg-inherit text-sm font-medium text-[#191919] dark:text-[#fafafa]">NT</span>
</div>
```

### Tabs
```html
<div class="inline-flex h-9 items-center justify-center rounded-lg bg-[#f5f5f5] dark:bg-[#262626] p-1 text-[#666] dark:text-[#888]">
  <button class="inline-flex items-center justify-center whitespace-nowrap rounded-md px-3 py-1 text-sm font-medium ring-offset-background transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 data-[state=active]:bg-white dark:data-[state=active]:bg-[#1a1a1a] data-[state=active]:text-[#191919] dark:data-[state=active]:text-[#fafafa] data-[state=active]:shadow" data-state="active">
    Tab 1
  </button>
  <button class="inline-flex items-center justify-center whitespace-nowrap rounded-md px-3 py-1 text-sm font-medium ring-offset-background transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50" data-state="inactive">
    Tab 2
  </button>
</div>
```

### Toast (JavaScript)
```javascript
function nqtToast(message, type = 'default') {
  const container = document.getElementById('nqt-toast-container') || createToastContainer();

  const styles = {
    default: 'bg-white dark:bg-[#262626] border-[#e5e5e5] dark:border-[#404040] text-[#191919] dark:text-[#fafafa]',
    success: 'bg-white dark:bg-[#262626] border-green-500 text-[#191919] dark:text-[#fafafa]',
    error: 'bg-white dark:bg-[#262626] border-red-500 text-[#191919] dark:text-[#fafafa]',
    warning: 'bg-white dark:bg-[#262626] border-yellow-500 text-[#191919] dark:text-[#fafafa]'
  };

  const toast = document.createElement('div');
  toast.className = `pointer-events-auto flex w-full max-w-md rounded-lg border shadow-lg ${styles[type]} p-4 transition-all duration-300 translate-y-2 opacity-0`;
  toast.innerHTML = `
    <div class="flex-1">
      <p class="text-sm font-medium">${message}</p>
    </div>
    <button class="ml-4 inline-flex shrink-0 rounded-md text-[#666] dark:text-[#888] hover:text-[#191919] dark:hover:text-[#fafafa]" onclick="this.parentElement.remove()">
      <i class="fas fa-times"></i>
    </button>
  `;

  container.appendChild(toast);
  requestAnimationFrame(() => {
    toast.classList.remove('translate-y-2', 'opacity-0');
  });

  setTimeout(() => {
    toast.classList.add('translate-y-2', 'opacity-0');
    setTimeout(() => toast.remove(), 300);
  }, 5000);
}

function createToastContainer() {
  const container = document.createElement('div');
  container.id = 'nqt-toast-container';
  container.className = 'fixed bottom-4 right-4 z-[100] flex flex-col gap-2 pointer-events-none';
  document.body.appendChild(container);
  return container;
}
```

---

## Typography

```html
<!-- Heading 1 -->
<h1 class="scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-5xl text-[#191919] dark:text-[#fafafa]">
  Heading 1
</h1>

<!-- Heading 2 -->
<h2 class="scroll-m-20 border-b border-[#e5e5e5] dark:border-[#404040] pb-2 text-3xl font-semibold tracking-tight first:mt-0 text-[#191919] dark:text-[#fafafa]">
  Heading 2
</h2>

<!-- Heading 3 -->
<h3 class="scroll-m-20 text-2xl font-semibold tracking-tight text-[#191919] dark:text-[#fafafa]">
  Heading 3
</h3>

<!-- Heading 4 -->
<h4 class="scroll-m-20 text-xl font-semibold tracking-tight text-[#191919] dark:text-[#fafafa]">
  Heading 4
</h4>

<!-- Paragraph -->
<p class="leading-7 [&:not(:first-child)]:mt-6 text-[#666] dark:text-[#888]">
  Paragraph text
</p>

<!-- Muted text -->
<p class="text-sm text-[#a3a3a3] dark:text-[#666]">
  Muted text
</p>
```

---

## Spacing & Layout

### Consistent Spacing Scale
```
space-1 = 0.25rem (4px)
space-2 = 0.5rem (8px)
space-3 = 0.75rem (12px)
space-4 = 1rem (16px)
space-6 = 1.5rem (24px)
space-8 = 2rem (32px)
```

### Container
```html
<div class="container mx-auto px-4 md:px-6 lg:px-8 max-w-7xl">
  <!-- Content -->
</div>
```

### Grid Layouts
```html
<!-- 2 columns -->
<div class="grid grid-cols-1 md:grid-cols-2 gap-4">...</div>

<!-- 3 columns -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">...</div>

<!-- 4 columns -->
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">...</div>
```

---

## Accessibility

### Focus States
```css
/* Tất cả interactive elements phải có focus-visible */
focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#191919] dark:focus-visible:ring-[#fafafa] focus-visible:ring-offset-2
```

### Screen Reader Only
```html
<span class="sr-only">Close</span>
```

### ARIA Labels
```html
<button aria-label="Close dialog">
  <i class="fas fa-times"></i>
</button>
```

### Keyboard Navigation
- Tab: Navigate between elements
- Enter/Space: Activate buttons
- Escape: Close modals/dropdowns
- Arrow keys: Navigate lists/menus

---

## Dark Mode Implementation

```javascript
// Check system preference + localStorage
function initDarkMode() {
  if (localStorage.getItem('theme') === 'dark' ||
      (!localStorage.getItem('theme') && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    document.documentElement.classList.add('dark');
  }
}

// Toggle
function toggleDarkMode() {
  const isDark = document.documentElement.classList.toggle('dark');
  localStorage.setItem('theme', isDark ? 'dark' : 'light');
}
```

---

## Best Practices

1. **Mobile-first**: Thiết kế mobile trước, scale lên desktop
2. **Consistent spacing**: Sử dụng Tailwind spacing scale
3. **Semantic colors**: Dùng semantic tokens (primary, muted, destructive)
4. **Focus states**: Tất cả interactive elements phải có focus indicator
5. **Loading states**: Skeleton screens thay vì spinner khi load data
6. **Empty states**: UI đẹp khi không có data
7. **Error handling**: Thông báo lỗi rõ ràng, actionable
8. **Micro-interactions**: Hover, focus, active states cho mọi element
9. **Responsive**: Test trên mobile, tablet, desktop
10. **Dark mode**: Tất cả components phải có dark: variants
