// ── Shared Tailwind Config ───────────────────────────────────────────────────
export const NQT_TW_CONFIG = {
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        "neon-lime": "#C8F135",
        "neon-dim":  "#A8D120",
        "bg-main":   "#0A0A0F",
        "bg-card":   "#12121A",
        "bg-elevated": "#1C1C28",
        "text-primary":   "#F5F5F0",
        "text-secondary": "#A1A1AA",
        "text-muted":     "#52525B",
        "border-subtle":  "rgba(255,255,255,0.06)",
        "border-neon":    "rgba(200,241,53,0.3)",
        "neon-glow":      "rgba(200,241,53,0.15)",
        "success": "#22C55E",
        "error":   "#EF4444",
        "warning": "#F59E0B",
        "info":    "#3B82F6",
      },
      fontFamily: {
        "sans": ["Inter", "sans-serif"],
        "mono": ["JetBrains Mono", "monospace"],
        "caps": ["Space Grotesk", "sans-serif"],
      },
    }
  }
};

// ── Admin Role Check ─────────────────────────────────────────────────────────
function nqtIsAdminUser() {
  const token = localStorage.getItem('nqt_admin_token');
  if (!token) return false;
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    if (payload.g6_loai !== 'nhan_vien') return false;
    const roles = payload.g6_vai_tro || [];
    return roles.some(r => ['G6QuanTri', 'G6QuanLy', 'G6HuanLuyenVien', 'G6LeTan'].includes(r));
  } catch { return false; }
}

// ── Public Navbar HTML ───────────────────────────────────────────────────────
export function nqtRenderPublicNav(activePage = '') {
  const links = [
    { href: '/',                              label: 'Trang chủ',  key: 'home' },
    { href: '/home1/goi-tap',                 label: 'Gói tập',   key: 'goi-tap' },
    { href: '/home1/huan-luyen-vien',         label: 'Huấn luyện viên', key: 'hlv' },
    { href: '/home1/lop-hoc',                 label: 'Lớp học',   key: 'lop-hoc' },
    { href: '/home1/shop',                    label: 'Shop',      key: 'shop' },
    { href: '/home1/blog',                    label: 'Blog',      key: 'blog' },
    { href: '/home1/su-kien',                 label: 'Sự kiện',   key: 'su-kien' },
  ];
  const user = nqtGetUser();
  const isAdmin = nqtIsAdminUser();

  const adminBtn = isAdmin
    ? `<a href="/src/pages/admin/dashboard.html" class="flex items-center gap-1.5 border border-border-neon text-neon-lime px-3 py-1.5 rounded hover:bg-neon-glow transition-colors">
        <span class="material-symbols-outlined" style="font-size:16px">admin_panel_settings</span>
        <span class="font-caps text-xs uppercase tracking-wide font-semibold">Admin</span>
      </a>`
    : '';
  const navLinks = links.map(l => `
    <a href="${l.href}" class="${l.key === activePage
      ? 'text-neon-lime border-b-2 border-neon-lime pb-1'
      : 'text-text-secondary hover:text-neon-lime'} transition-colors duration-200 text-xs font-caps uppercase tracking-wide font-semibold">
      ${l.label}
    </a>`).join('');

  const authBtn = user
    ? `<a href="/home" class="flex items-center gap-2 text-text-secondary hover:text-neon-lime transition-colors text-sm">
        <span class="material-symbols-outlined text-base">account_circle</span>
        <span class="hidden sm:inline font-caps text-xs uppercase tracking-wide">${user.nqt_ho_ten || 'Member'}</span>
      </a>`
    : `<a href="/login" class="bg-neon-lime text-bg-main font-caps text-xs uppercase tracking-wide font-semibold px-5 py-2 rounded hover:bg-neon-dim transition-colors">
        Đăng nhập
      </a>`;

  const cartIcon = `<a href="/home?tab=cart" class="text-text-secondary hover:text-neon-lime transition-colors relative" id="nqtCartIcon">
    <span class="material-symbols-outlined text-xl">shopping_cart</span>
    <span id="nqtCartBadge" class="hidden absolute -top-1 -right-1 bg-neon-lime text-bg-main text-[10px] font-bold w-4 h-4 rounded-full flex items-center justify-center"></span>
  </a>`;

  const mobileMenuBtn = `<button id="nqtMobileMenuBtn" class="lg:hidden text-text-secondary hover:text-neon-lime transition-colors">
    <span class="material-symbols-outlined">menu</span>
  </button>`;

  const mobileMenu = `
  <div id="nqtMobileMenu" class="hidden lg:hidden fixed inset-0 z-50 bg-bg-main/95 backdrop-blur-lg flex flex-col">
    <div class="flex items-center justify-between px-6 h-20 border-b border-border-subtle">
      <span class="font-caps text-xl font-black text-white tracking-tight">NQT <span class="text-neon-lime">GYM</span></span>
      <button id="nqtMobileMenuClose" class="text-text-secondary hover:text-neon-lime">
        <span class="material-symbols-outlined">close</span>
      </button>
    </div>
    <nav class="flex flex-col gap-1 p-6">
      ${links.map(l => `<a href="${l.href}" class="flex items-center gap-3 px-4 py-3 rounded-lg ${l.key === activePage ? 'bg-neon-glow text-neon-lime' : 'text-text-secondary hover:bg-bg-card hover:text-text-primary'} transition-colors font-caps text-sm uppercase tracking-wide font-semibold">${l.label}</a>`).join('')}
    </nav>
    <div class="px-6 mt-auto pb-8 flex flex-col gap-3">
      ${isAdmin
        ? `<a href="/src/pages/admin/dashboard.html" class="block w-full text-center border border-border-neon text-neon-lime py-3 rounded-lg font-caps text-sm uppercase tracking-wide font-semibold hover:bg-neon-glow transition-colors flex items-center justify-center gap-2"><span class="material-symbols-outlined text-base">admin_panel_settings</span> Admin Panel</a>`
        : ''
      }
      ${user
        ? `<a href="/home" class="block w-full text-center bg-bg-card border border-border-subtle text-text-primary py-3 rounded-lg font-caps text-sm uppercase tracking-wide font-semibold">Dashboard</a>`
        : `<a href="/login" class="block w-full text-center bg-neon-lime text-bg-main py-3 rounded-lg font-caps text-sm uppercase tracking-wide font-semibold hover:bg-neon-dim transition-colors">Đăng nhập</a>`
      }
    </div>
  </div>`;

  const nav = document.createElement('nav');
  nav.className = 'bg-bg-main/80 backdrop-blur-lg fixed top-0 w-full z-50 border-b border-border-subtle shadow-[0_8px_48px_rgba(0,0,0,0.6)]';
  nav.innerHTML = `
    <div class="flex items-center justify-between h-18 px-6 md:px-10 max-w-screen-xl mx-auto" style="height:72px">
      <a href="/" class="font-caps text-xl font-black text-white tracking-tight">NQT <span class="text-neon-lime">GYM</span></a>
      <div class="hidden lg:flex items-center gap-8">${navLinks}</div>
      <div class="flex items-center gap-4">
        ${cartIcon}
        ${adminBtn}
        <div class="hidden lg:block">${authBtn}</div>
        ${mobileMenuBtn}
      </div>
    </div>
    ${mobileMenu}
  `;
  document.body.prepend(nav);

  // Mobile menu toggle
  document.getElementById('nqtMobileMenuBtn')?.addEventListener('click', () => {
    document.getElementById('nqtMobileMenu')?.classList.remove('hidden');
  });
  document.getElementById('nqtMobileMenuClose')?.addEventListener('click', () => {
    document.getElementById('nqtMobileMenu')?.classList.add('hidden');
  });

  // Cart badge
  nqtUpdateCartBadge();
}

// ── Public Footer ────────────────────────────────────────────────────────────
export function nqtRenderFooter() {
  const footer = document.createElement('footer');
  footer.className = 'bg-bg-card border-t border-border-subtle mt-20';
  footer.innerHTML = `
    <div class="max-w-screen-xl mx-auto px-6 md:px-10 py-14 grid grid-cols-1 md:grid-cols-4 gap-10">
      <div>
        <div class="font-caps text-2xl font-black text-white tracking-tight mb-3">NQT <span class="text-neon-lime">GYM</span></div>
        <p class="text-text-secondary text-sm leading-relaxed">Nền tảng quản lý phòng gym B2B hàng đầu. Nâng tầm trải nghiệm thành viên.</p>
      </div>
      <div>
        <div class="font-caps text-xs uppercase tracking-widest text-neon-lime font-semibold mb-4">Dịch vụ</div>
        <ul class="space-y-2 text-sm text-text-secondary">
          <li><a href="/home1/goi-tap" class="hover:text-neon-lime transition-colors">Gói tập</a></li>
          <li><a href="/home1/huan-luyen-vien" class="hover:text-neon-lime transition-colors">Huấn luyện viên</a></li>
          <li><a href="/home1/lop-hoc" class="hover:text-neon-lime transition-colors">Lớp học</a></li>
          <li><a href="/home1/su-kien" class="hover:text-neon-lime transition-colors">Sự kiện</a></li>
        </ul>
      </div>
      <div>
        <div class="font-caps text-xs uppercase tracking-widest text-neon-lime font-semibold mb-4">Shop</div>
        <ul class="space-y-2 text-sm text-text-secondary">
          <li><a href="/home1/shop" class="hover:text-neon-lime transition-colors">Thực phẩm chức năng</a></li>
          <li><a href="/home?tab=cart" class="hover:text-neon-lime transition-colors">Giỏ hàng</a></li>
          <li><a href="/src/pages/shop/don-hang.html" class="hover:text-neon-lime transition-colors">Đơn hàng của tôi</a></li>
        </ul>
      </div>
      <div>
        <div class="font-caps text-xs uppercase tracking-widest text-neon-lime font-semibold mb-4">Tài khoản</div>
        <ul class="space-y-2 text-sm text-text-secondary">
          <li><a href="/login" class="hover:text-neon-lime transition-colors">Đăng nhập</a></li>
          <li><a href="/register" class="hover:text-neon-lime transition-colors">Đăng ký</a></li>
          <li><a href="/home" class="hover:text-neon-lime transition-colors">Dashboard</a></li>
        </ul>
      </div>
    </div>
    <div class="border-t border-border-subtle py-5 text-center text-text-muted text-xs">
      © 2026 NQT GYM. All rights reserved.
    </div>
  `;
  document.body.append(footer);
}

// ── Member Sidebar ───────────────────────────────────────────────────────────
export function nqtRenderSidebar(activePage = '') {
  const items = [
    { href: '/src/pages/member/dashboard.html', label: 'Tổng quan',   icon: 'dashboard',      key: 'dashboard' },
    { href: '/src/pages/member/ho_so.html',     label: 'Hồ sơ',       icon: 'person',         key: 'ho-so' },
    { href: '/src/pages/member/goi-tap.html',   label: 'Gói tập',     icon: 'card_membership',key: 'goi-tap' },
    { href: '/src/pages/member/diem-danh.html', label: 'Điểm danh',   icon: 'qr_code_scanner',key: 'diem-danh' },
    { href: '/src/pages/member/chi-so.html',    label: 'Chỉ số cơ thể',icon: 'monitor_weight', key: 'chi-so' },
    { href: '/src/pages/member/lich-tap.html',  label: 'Lịch tập',    icon: 'calendar_month', key: 'lich-tap' },
    { href: '/src/pages/member/dich-vu.html',   label: 'Dịch vụ phụ', icon: 'spa',            key: 'dich-vu' },
    { href: '/src/pages/shop/don-hang.html',    label: 'Đơn hàng',    icon: 'inventory_2',    key: 'don-hang' },
  ];

  const user = nqtGetUser();
  const initials = (user?.nqt_ho_ten || 'M').split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase();

  const sidebarHtml = `
  <aside class="fixed top-0 left-0 w-64 h-screen bg-zinc-950 border-r border-border-subtle flex flex-col z-40 hidden lg:flex">
    <div class="flex items-center gap-3 px-6 h-20 border-b border-border-subtle flex-shrink-0">
      <div class="w-9 h-9 bg-neon-lime rounded-lg flex items-center justify-center">
        <span class="material-symbols-outlined text-bg-main text-lg font-bold">fitness_center</span>
      </div>
      <div>
        <div class="font-caps text-sm font-black text-white tracking-tight">NQT GYM</div>
        <div class="text-text-muted text-[10px] font-caps uppercase tracking-widest">Member Portal</div>
      </div>
    </div>
    <nav class="flex-1 overflow-y-auto py-4 px-3">
      ${items.map(it => `
      <a href="${it.href}" class="flex items-center gap-3 px-3 py-2.5 rounded-lg mb-0.5 transition-all duration-200 ${it.key === activePage
        ? 'bg-neon-glow text-neon-lime border border-border-neon'
        : 'text-text-secondary hover:bg-bg-card hover:text-text-primary'}">
        <span class="material-symbols-outlined text-[18px]">${it.icon}</span>
        <span class="font-caps text-xs uppercase tracking-wide font-semibold">${it.label}</span>
      </a>`).join('')}
    </nav>
    <div class="border-t border-border-subtle p-4">
      <div class="flex items-center gap-3 px-3 py-2 rounded-lg bg-bg-card">
        <div class="w-8 h-8 rounded-full bg-neon-lime flex items-center justify-center text-bg-main text-xs font-bold font-caps flex-shrink-0">${initials}</div>
        <div class="flex-1 min-w-0">
          <div class="text-text-primary text-xs font-semibold truncate">${user?.nqt_ho_ten || 'Hội viên'}</div>
          <div class="text-text-muted text-[10px] truncate">${user?.nqt_email || ''}</div>
        </div>
        <button onclick="nqtLogoutAction()" class="text-text-muted hover:text-error transition-colors flex-shrink-0">
          <span class="material-symbols-outlined text-base">logout</span>
        </button>
      </div>
    </div>
  </aside>`;

  const mobileTopBar = `
  <div class="lg:hidden fixed top-0 left-0 right-0 z-40 bg-zinc-950 border-b border-border-subtle flex items-center justify-between px-4 h-16">
    <a href="/" class="font-caps text-lg font-black text-white tracking-tight">NQT <span class="text-neon-lime">GYM</span></a>
    <button id="nqtSidebarToggle" class="text-text-secondary hover:text-neon-lime transition-colors">
      <span class="material-symbols-outlined">menu</span>
    </button>
  </div>
  <div id="nqtMobileSidebar" class="hidden lg:hidden fixed inset-0 z-50 bg-bg-main/95 backdrop-blur-lg flex flex-col">
    <div class="flex items-center justify-between px-6 h-16 border-b border-border-subtle">
      <span class="font-caps text-lg font-black text-white">NQT <span class="text-neon-lime">GYM</span></span>
      <button id="nqtSidebarClose" class="text-text-secondary hover:text-neon-lime">
        <span class="material-symbols-outlined">close</span>
      </button>
    </div>
    <nav class="flex-1 p-4 overflow-y-auto">
      ${items.map(it => `
      <a href="${it.href}" class="flex items-center gap-3 px-4 py-3 rounded-lg mb-1 ${it.key === activePage
        ? 'bg-neon-glow text-neon-lime'
        : 'text-text-secondary hover:bg-bg-card hover:text-text-primary'} transition-colors">
        <span class="material-symbols-outlined text-lg">${it.icon}</span>
        <span class="font-caps text-sm uppercase tracking-wide font-semibold">${it.label}</span>
      </a>`).join('')}
    </nav>
    <div class="p-4 border-t border-border-subtle">
      <button onclick="nqtLogoutAction()" class="w-full flex items-center gap-2 justify-center text-error py-3 font-caps text-sm uppercase tracking-wide font-semibold">
        <span class="material-symbols-outlined text-base">logout</span> Đăng xuất
      </button>
    </div>
  </div>`;

  document.body.insertAdjacentHTML('afterbegin', sidebarHtml + mobileTopBar);

  document.getElementById('nqtSidebarToggle')?.addEventListener('click', () => {
    document.getElementById('nqtMobileSidebar')?.classList.remove('hidden');
  });
  document.getElementById('nqtSidebarClose')?.addEventListener('click', () => {
    document.getElementById('nqtMobileSidebar')?.classList.add('hidden');
  });
}

// ── Helpers ──────────────────────────────────────────────────────────────────
export function nqtGetUser() {
  try { return JSON.parse(localStorage.getItem('nqt_user') || 'null'); }
  catch { return null; }
}

export function nqtUpdateCartBadge() {
  const cart = nqtGetCart();
  const badge = document.getElementById('nqtCartBadge');
  if (!badge) return;
  const count = cart.reduce((s, i) => s + (i.qty || 1), 0);
  if (count > 0) {
    badge.textContent = count > 9 ? '9+' : count;
    badge.classList.remove('hidden');
    badge.classList.add('flex');
  } else {
    badge.classList.add('hidden');
  }
}

export function nqtGetCart() {
  try { return JSON.parse(localStorage.getItem('nqt_cart') || '[]'); }
  catch { return []; }
}

export function nqtSaveCart(cart) {
  localStorage.setItem('nqt_cart', JSON.stringify(cart));
  nqtUpdateCartBadge();
}

export function nqtFormatPrice(n) {
  return Number(n || 0).toLocaleString('vi-VN') + '₫';
}

export function nqtFormatDate(d) {
  if (!d) return '—';
  return new Date(d).toLocaleDateString('vi-VN', { day: '2-digit', month: '2-digit', year: 'numeric' });
}

// exposed globally for onclick handlers
window.nqtLogoutAction = function () {
  localStorage.removeItem('nqt_token');
  localStorage.removeItem('nqt_refresh_token');
  localStorage.removeItem('nqt_user');
  window.location.href = '/login';
};
