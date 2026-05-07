// Mobile menu toggle
document.getElementById('nqtMobileMenuBtn').addEventListener('click', () => {
    document.getElementById('nqtMobileMenu').classList.toggle('hidden');
});

// ── API helpers ──────────────────────────────────────────────────────────────
const API = '/api';

async function nqtFetch(path) {
    const res = await fetch(API + path);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
}

function nqtAvatarSvg(name, size = 80) {
    const limeShades = ['#1a1d11', '#1e2115', '#0d0f05', '#12121A', '#1C1C28'];
    const idx = (name || '').charCodeAt(0) % limeShades.length;
    const initials = (name || '?').split(' ').slice(0, 2).map(w => w[0] || '').join('').toUpperCase();
    return `<svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" xmlns="http://www.w3.org/2000/svg">
        <rect width="${size}" height="${size}" fill="${limeShades[idx]}"/>
        <text x="50%" y="50%" dominant-baseline="central" text-anchor="middle"
              fill="#C8F135" font-size="${size * 0.35}" font-weight="700" font-family="Inter,sans-serif">${initials}</text>
    </svg>`;
}

// ── Render Gói Tập ───────────────────────────────────────────────────────────
function nqtRenderGoiTap(items) {
    const container = document.getElementById('goiTapList');
    if (!items || items.length === 0) {
        container.innerHTML = '<p class="col-span-3 text-center text-text-secondary py-16">Chưa có gói tập nào.</p>';
        return;
    }
    container.innerHTML = items.map((goi, idx) => {
        const giaGoc = Number(goi.g6_gia || 0).toLocaleString('vi-VN');
        const giaKm = goi.g6_gia_khuyen_mai ? Number(goi.g6_gia_khuyen_mai).toLocaleString('vi-VN') : null;
        const isNoBat = goi.g6_la_noi_bat;

        const priceHtml = giaKm
            ? `<span class="font-mono text-2xl font-bold text-neon-lime">${giaKm}đ</span>
               <span class="text-sm text-text-muted line-through ml-2">${giaGoc}đ</span>`
            : `<span class="font-mono text-2xl font-bold ${isNoBat ? 'text-neon-lime' : 'text-text-primary'}">${giaGoc}đ</span>`;

        const featureLine = (icon, text) =>
            `<li class="flex items-center gap-2 text-sm text-text-secondary">
                <span class="material-symbols-outlined text-[16px] text-neon-lime">check_circle</span>${text}
             </li>`;

        return `
        <div class="relative flex flex-col bg-bg-elevated border rounded-xl p-7 transition-all duration-300
                    ${isNoBat
                        ? 'border-neon-lime/40 shadow-[0_0_40px_rgba(200,241,53,0.1)] scale-[1.02]'
                        : 'border-border-subtle hover:border-border-neon'}"
        >
            ${isNoBat ? `<div class="absolute -top-3 left-1/2 -translate-x-1/2 bg-neon-lime text-bg-main font-caps text-[10px] uppercase tracking-widest px-4 py-1 rounded-full">Phổ biến nhất</div>` : ''}

            <div class="mb-6">
                <h3 class="text-d-md text-text-primary mb-1">${goi.g6_ten_goi || goi.g6_ten || 'Gói tập'}</h3>
                <p class="text-sm text-text-secondary">${goi.g6_so_ngay || '?'} ngày</p>
            </div>

            <div class="mb-6 pb-6 border-b border-border-subtle">
                <div class="flex items-baseline gap-1">
                    ${priceHtml}
                </div>
                <span class="text-xs text-text-muted">/ ${goi.g6_so_ngay || '?'} ngày</span>
            </div>

            <ul class="space-y-3 mb-8 flex-1">
                ${featureLine('check_circle', 'Tập không giới hạn')}
                ${goi.g6_co_pt ? featureLine('check_circle', `${goi.g6_so_buoi_pt || 0} buổi PT`) : ''}
                ${goi.g6_co_sauna ? featureLine('check_circle', 'Phòng sauna') : ''}
            </ul>

            <a href="/src/pages/member/login.html"
               class="block w-full text-center py-3 rounded font-caps text-[11px] uppercase tracking-widest transition-all duration-300
                      ${isNoBat
                          ? 'bg-neon-lime text-bg-main hover:scale-105 hover:shadow-[0_0_20px_rgba(200,241,53,0.3)]'
                          : 'border border-border-subtle text-text-primary hover:border-neon-lime/40 hover:text-neon-lime'}"
            >
                Đăng ký ngay
            </a>
        </div>`;
    }).join('');
}

// ── Render HLV ────────────────────────────────────────────────────────────────
function nqtRenderHLV(items) {
    const container = document.getElementById('hlvList');
    if (!items || items.length === 0) {
        container.innerHTML = '<p class="col-span-4 text-center text-text-secondary py-16">Chưa có huấn luyện viên nào.</p>';
        return;
    }
    container.innerHTML = items.map(hlv => {
        const chuyenMon = (Array.isArray(hlv.g6_chuyen_mon)
            ? hlv.g6_chuyen_mon
            : (hlv.g6_chuyen_mon ? [hlv.g6_chuyen_mon] : [])).slice(0, 2);

        const avatarHtml = hlv.g6_anh_dai_dien
            ? `<img src="${hlv.g6_anh_dai_dien}" alt="${hlv.g6_ho_ten}" class="w-full h-full object-cover grayscale group-hover:grayscale-0 transition-all duration-700">`
            : nqtAvatarSvg(hlv.g6_ho_ten, 80);

        return `
        <div class="group relative overflow-hidden rounded-xl aspect-[3/4] bg-surface-container-lowest border border-border-subtle hover:border-border-neon transition-colors duration-500 cursor-pointer">
            <div class="w-full h-full flex items-center justify-center text-text-muted overflow-hidden">
                ${avatarHtml}
            </div>
            <div class="absolute inset-0 bg-gradient-to-t from-bg-main via-bg-main/20 to-transparent opacity-90"></div>
            <div class="absolute bottom-0 left-0 p-5 transform translate-y-2 group-hover:translate-y-0 transition-transform duration-500">
                <h4 class="text-d-md text-text-primary text-xl font-bold mb-1">${hlv.g6_ho_ten || 'HLV'}</h4>
                <div class="flex flex-wrap gap-1 mb-1">
                    ${chuyenMon.map(c => `<span class="font-caps text-[10px] text-neon-lime uppercase tracking-widest">${c}</span>`).join('<span class="text-text-muted mx-1">·</span>')}
                </div>
                <p class="text-xs text-text-secondary">${hlv.g6_so_nam_kinh_nghiem || 0} năm kinh nghiệm</p>
            </div>
        </div>`;
    }).join('');
}

// ── Render Blog ────────────────────────────────────────────────────────────────
function nqtRenderBlog(items) {
    const container = document.getElementById('blogList');
    if (!items || items.length === 0) {
        container.innerHTML = '<p class="col-span-3 text-center text-text-secondary py-16">Chưa có bài viết nào.</p>';
        return;
    }
    container.innerHTML = items.map(baiviet => {
        const ngay = baiviet.g6_ngay_xuat_ban
            ? new Date(baiviet.g6_ngay_xuat_ban).toLocaleDateString('vi-VN')
            : '';
        const thumbHtml = baiviet.g6_hinh_dai_dien
            ? `<img src="${baiviet.g6_hinh_dai_dien}" alt="${baiviet.g6_tieu_de}" class="w-full h-full object-cover grayscale group-hover:grayscale-0 group-hover:scale-105 transition-all duration-700">`
            : `<div class="w-full h-full flex items-center justify-center">
                 <span class="material-symbols-outlined text-4xl text-text-muted">image</span>
               </div>`;

        return `
        <a href="#blog" class="group flex flex-col bg-bg-elevated border border-border-subtle rounded-xl overflow-hidden hover:border-border-neon transition-all duration-300">
            <div class="aspect-video overflow-hidden bg-surface-container-low">
                ${thumbHtml}
            </div>
            <div class="p-6 flex flex-col flex-1">
                <div class="flex items-center gap-3 mb-3">
                    <span class="font-caps text-[10px] text-text-muted uppercase tracking-widest">${ngay}</span>
                    <span class="flex items-center gap-1 font-caps text-[10px] text-text-muted uppercase tracking-widest">
                        <span class="material-symbols-outlined text-[13px]">visibility</span>
                        ${baiviet.g6_luot_xem || 0}
                    </span>
                </div>
                <h3 class="text-base font-bold text-text-primary group-hover:text-neon-lime transition-colors duration-300 line-clamp-2 mb-2">${baiviet.g6_tieu_de || 'Bài viết'}</h3>
                <p class="text-sm text-text-secondary line-clamp-3 flex-1">${baiviet.g6_mo_ta_ngan || ''}</p>
                <div class="flex items-center gap-1 mt-4 text-neon-lime font-caps text-[10px] uppercase tracking-widest">
                    <span>Đọc thêm</span>
                    <span class="material-symbols-outlined text-[14px] group-hover:translate-x-1 transition-transform duration-200">arrow_forward</span>
                </div>
            </div>
        </a>`;
    }).join('');
}

// ── Init ─────────────────────────────────────────────────────────────────────
(async () => {
    const [goiTap, hlv, blog] = await Promise.allSettled([
        nqtFetch('/nqt-public/goi-tap'),
        nqtFetch('/nqt-public/huan-luyen-vien'),
        nqtFetch('/nqt-public/blog'),
    ]);

    if (goiTap.status === 'fulfilled' && goiTap.value.nqt_thanh_cong) {
        nqtRenderGoiTap(goiTap.value.nqt_du_lieu);
    } else {
        const c = document.getElementById('goiTapList');
        c.innerHTML = '<p class="col-span-3 text-center text-text-secondary py-16">Chưa có gói tập nào.</p>';
    }

    if (hlv.status === 'fulfilled' && hlv.value.nqt_thanh_cong) {
        nqtRenderHLV(hlv.value.nqt_du_lieu);
    } else {
        const c = document.getElementById('hlvList');
        c.innerHTML = '<p class="col-span-4 text-center text-text-secondary py-16">Chưa có huấn luyện viên nào.</p>';
    }

    if (blog.status === 'fulfilled' && blog.value.nqt_thanh_cong) {
        nqtRenderBlog(blog.value.nqt_du_lieu);
    } else {
        const c = document.getElementById('blogList');
        c.innerHTML = '<p class="col-span-3 text-center text-text-secondary py-16">Chưa có bài viết nào.</p>';
    }
})();
