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

// ── Google Translate Languages ────────────────────────────────────────────────
const NQT_LANGUAGES = {
  'vi': { flag: '🇻🇳', name: 'Tiếng Việt' },
  'en': { flag: '🇺🇸', name: 'English' },
  'zh-CN': { flag: '🇨🇳', name: '简体中文' },
  'zh-TW': { flag: '🇹🇼', name: '繁體中文' },
  'ja': { flag: '🇯🇵', name: '日本語' },
  'ko': { flag: '🇰🇷', name: '한국어' },
  'ru': { flag: '🇷🇺', name: 'Русский' },
  'es': { flag: '🇪🇸', name: 'Español' },
  'fr': { flag: '🇫🇷', name: 'Français' },
  'de': { flag: '🇩🇪', name: 'Deutsch' },
  'hi': { flag: '🇮🇳', name: 'हिन्दी' },
  'it': { flag: '🇮🇹', name: 'Italiano' },
  'pt': { flag: '🇵🇹', name: 'Português' },
  'tr': { flag: '🇹🇷', name: 'Türkçe' },
  'ar': { flag: '🇸🇦', name: 'العربية' },
  'th': { flag: '🇹🇭', name: 'ภาษาไทย' },
  'id': { flag: '🇮🇩', name: 'Bahasa Indonesia' },
  'nl': { flag: '🇳🇱', name: 'Nederlands' },
  'pl': { flag: '🇵🇱', name: 'Polski' },
  'ms': { flag: '🇲🇾', name: 'Bahasa Melayu' },
  'tl': { flag: '🇵🇭', name: 'Filipino' },
  'km': { flag: '🇰🇭', name: 'ភាសាខ្មែរ' },
  'lo': { flag: '🇱🇦', name: 'ພາສາລາວ' },
  'my': { flag: '🇲🇲', name: 'မြန်မာဘာသာ' },
  'bn': { flag: '🇧🇩', name: 'বাংলা' },
  'fa': { flag: '🇮🇷', name: 'فارسی' },
  'uk': { flag: '🇺🇦', name: 'Українська' },
  'sv': { flag: '🇸🇪', name: 'Svenska' },
  'no': { flag: '🇳🇴', name: 'Norsk' },
  'da': { flag: '🇩🇰', name: 'Dansk' },
  'fi': { flag: '🇫🇮', name: 'Suomi' },
  'el': { flag: '🇬🇷', name: 'Ελληνικά' },
  'he': { flag: '🇮🇱', name: 'עברית' },
  'cs': { flag: '🇨🇿', name: 'Čeština' },
  'ro': { flag: '🇷🇴', name: 'Română' }
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

  const savedLang = localStorage.getItem('website_lang') || 'vi';
  const currentLang = NQT_LANGUAGES[savedLang] || NQT_LANGUAGES['vi'];
  const codeLabel = (savedLang === 'zh-CN' || savedLang === 'zh-TW') ? 'ZH' : savedLang.toUpperCase();

  const langDropdownHtml = `
  <div class="lang-dropdown-popover relative">
    <button onclick="toggleLangPopover(event)" class="flex items-center gap-2.5 px-4 py-1.5 rounded-full border border-border-subtle bg-white/5 hover:bg-white/10 text-text-secondary hover:text-text-primary transition-all duration-200 select-none">
      <span id="currentLangFlag" class="text-[10px] font-bold tracking-wider text-text-secondary/70">${codeLabel}</span>
      <span id="currentLangName" class="text-xs font-medium">${currentLang.name}</span>
      <svg class="w-3.5 h-3.5 opacity-60 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M19 9l-7 7-7-7"></path></svg>
    </button>
    <div id="langPopoverMenu" class="absolute right-0 mt-2 w-64 bg-bg-card border border-border-subtle rounded-xl shadow-2xl overflow-hidden hidden flex-col z-50">
      <div class="p-3 border-b border-border-subtle bg-bg-elevated">
        <input type="text" id="langSearchInput" onkeyup="filterLanguages()" class="w-full px-3 py-1.5 text-xs bg-bg-main border border-border-subtle rounded-lg text-text-primary placeholder-text-muted focus:outline-none focus:border-border-neon" placeholder="Tìm kiếm ngôn ngữ...">
      </div>
      <div class="max-h-60 overflow-y-auto py-1 divide-y divide-border-subtle/50">
        ${Object.entries(NQT_LANGUAGES).map(([code, l]) => `
          <button onclick="changeLanguage('${code}')" class="lang-popover-item w-full px-4 py-2 text-left hover:bg-bg-elevated hover:text-neon-lime flex items-center gap-2.5 transition-colors duration-150">
            <span class="text-sm">${l.flag}</span>
            <span class="lang-name text-xs font-medium text-text-secondary hover:text-neon-lime">${l.name}</span>
          </button>
        `).join('')}
      </div>
    </div>
  </div>`;

  const nav = document.createElement('nav');
  nav.className = 'bg-bg-main/80 backdrop-blur-lg fixed top-0 w-full z-50 border-b border-border-subtle shadow-[0_8px_48px_rgba(0,0,0,0.6)]';
  nav.innerHTML = `
    <div class="flex items-center justify-between h-18 px-6 md:px-10 max-w-screen-xl mx-auto" style="height:72px">
      <a href="/" class="font-caps text-xl font-black text-white tracking-tight">NQT <span class="text-neon-lime">GYM</span></a>
      <div class="hidden lg:flex items-center gap-8">${navLinks}</div>
      <div class="flex items-center gap-4">
        ${langDropdownHtml}
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

// ── Language Popover Functions ───────────────────────────────────────────────
window.toggleLangPopover = function(event) {
  event.stopPropagation();
  const popover = document.getElementById('langPopoverMenu');
  const wrapper = document.querySelector('.lang-dropdown-popover');
  if (!popover || !wrapper) return;
  
  popover.classList.toggle('hidden');
  popover.classList.toggle('flex');
  wrapper.classList.toggle('active');

  if (popover.classList.contains('flex')) {
    const searchInput = document.getElementById('langSearchInput');
    if (searchInput) {
      searchInput.value = '';
      window.filterLanguages();
      setTimeout(() => searchInput.focus(), 50);
    }
  }
};

window.filterLanguages = function() {
  const input = document.getElementById('langSearchInput');
  if (!input) return;
  
  const cleanStr = (str) => {
    if (!str) return '';
    return str
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .replace(/đ/g, "d")
      .replace(/Đ/g, "d")
      .toLowerCase()
      .trim();
  };
  
  const filter = cleanStr(input.value);
  const items = document.querySelectorAll('.lang-popover-item');
  
  items.forEach(item => {
    const nameSpan = item.querySelector('.lang-name');
    if (nameSpan) {
      const text = cleanStr(nameSpan.textContent);
      const onclickAttr = item.getAttribute('onclick') || '';
      const langCodeMatch = onclickAttr.match(/'([^']+)'/);
      const langCode = langCodeMatch ? cleanStr(langCodeMatch[1]) : '';
      
      if (text.includes(filter) || langCode.includes(filter)) {
        item.style.display = '';
      } else {
        item.style.display = 'none';
      }
    }
  });
};

window.changeLanguage = function(langCode) {
  function eraseCookie(name) {
    document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    const host = window.location.hostname;
    const parts = host.split('.');
    for (let i = 0; i < parts.length; i++) {
      const domain = parts.slice(i).join('.');
      if (domain) {
        document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; domain=' + domain + ';';
        document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; domain=.' + domain + ';';
      }
    }
  }

  eraseCookie('googtrans');

  const cookieValue = langCode === 'vi' ? "/vi/vi" : "/vi/" + langCode;
  const host = window.location.hostname;
  const parts = host.split('.');
  
  document.cookie = "googtrans=" + cookieValue + "; path=/;";
  for (let i = 0; i < parts.length; i++) {
    const domain = parts.slice(i).join('.');
    if (domain) {
      document.cookie = "googtrans=" + cookieValue + "; path=/; domain=" + domain + ";";
      document.cookie = "googtrans=" + cookieValue + "; path=/; domain=." + domain + ";";
    }
  }
  
  localStorage.setItem('website_lang', langCode);
  location.reload();
};

// Close popover when clicking anywhere outside
window.addEventListener('click', function(event) {
  const popover = document.getElementById('langPopoverMenu');
  const wrapper = document.querySelector('.lang-dropdown-popover');
  
  if (popover && !popover.classList.contains('hidden')) {
    const isClickInside = wrapper?.contains(event.target);
    if (!isClickInside) {
      popover.classList.add('hidden');
      popover.classList.remove('flex');
      wrapper?.classList.remove('active');
    }
  }
});

// Dynamic script injection for Google Translate
if (typeof window !== 'undefined' && !window.googleTranslateElementInit) {
  window.googleTranslateElementInit = function() {
    new google.translate.TranslateElement({pageLanguage: 'vi'}, 'google_translate_element');
  };

  const gDiv = document.createElement('div');
  gDiv.id = 'google_translate_element';
  gDiv.style.display = 'none';
  document.body.appendChild(gDiv);

  const style = document.createElement('style');
  style.innerHTML = `
    iframe.goog-te-banner-frame,
    .VIpgJd-ZVi9od-ORHb-OEVmcd,
    .VIpgJd-ZVi9od-l4eHX-hSRGPd,
    .VIpgJd-yAWNEb-L7lbkb,
    iframe.skiptranslate,
    #goog-gt-tt { display: none !important; }
    body { top: 0px !important; }
    html { margin-top: 0px !important; }
    .goog-logo-link { display: none !important; }
    .goog-te-gadget { color: transparent !important; font-size: 0px !important; }
    .goog-te-gadget .goog-te-combo { display: none !important; }
    .goog-te-balloon-frame { display: none !important; }
    .goog-tooltip { display: none !important; }
    .goog-tooltip:hover { display: none !important; }
    .goog-text-highlight { background-color: transparent !important; border: none !important; box-shadow: none !important; }
    
    .lang-dropdown-popover button {
      cursor: pointer;
      background: transparent;
      transition: all 0.2s ease;
    }
    .lang-dropdown-popover.active button {
      border-color: rgba(200, 241, 53, 0.5) !important;
      background-color: rgba(200, 241, 53, 0.05) !important;
      color: #C8F135 !important;
    }
    #langPopoverMenu {
      backdrop-filter: blur(16px);
      background: rgba(18, 18, 26, 0.95);
      border: 1px solid rgba(255, 255, 255, 0.08);
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
      min-width: 240px;
      border-radius: 12px;
    }
    .lang-popover-item {
      transition: background-color 0.15s ease, color 0.15s ease;
    }
  `;
  document.head.appendChild(style);

  const script = document.createElement('script');
  script.src = 'https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
  script.async = true;
  document.head.appendChild(script);
}
