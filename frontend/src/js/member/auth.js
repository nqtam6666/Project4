// ── Auth guard: redirect if not logged in ────────────────────────────────────
export function nqtRequireAuth(redirectTo = '/login') {
    const token = localStorage.getItem('nqt_token');
    if (!token) {
        window.location.href = redirectTo;
        return false;
    }
    return true;
}

// ── API fetch with Bearer token ─────────────────────────────────────────────
export async function nqtApi(path, options = {}) {
    const token = localStorage.getItem('nqt_token');
    const headers = {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
        ...options.headers,
    };
    return fetch(path, { ...options, headers });
}

// ── Logout ───────────────────────────────────────────────────────────────────
export function nqtLogout() {
    localStorage.removeItem('nqt_token');
    localStorage.removeItem('nqt_refresh_token');
    localStorage.removeItem('nqt_user');
    window.location.href = '/login';
}

// ── SVG avatar generator ─────────────────────────────────────────────────────
export function nqtAvatarSvg(name = '', size = 40) {
    const colors = ['#191919', '#dc2626', '#2563eb', '#16a34a', '#d97706', '#7c3aed'];
    const idx = (name || '?').charCodeAt(0) % colors.length;
    const initials = (name || '?').split(' ').slice(0, 2).map(w => (w[0] || '')).join('').toUpperCase();
    return `<svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" xmlns="http://www.w3.org/2000/svg">
        <rect width="${size}" height="${size}" fill="${colors[idx]}" rx="${size / 2}"/>
        <text x="50%" y="50%" dominant-baseline="central" text-anchor="middle"
              fill="white" font-size="${size * 0.38}" font-weight="600" font-family="Inter,sans-serif">${initials}</text>
    </svg>`;
}

// ── Toast notification (inline, no deps) ─────────────────────────────────────
export function nqtToast(msg, type = 'info') {
    const colors = {
        success: 'bg-green-600',
        error: 'bg-[#dc2626]',
        info: 'bg-[#191919] dark:bg-white dark:text-[#191919]',
    };
    const icons = { success: 'fa-check', error: 'fa-exclamation', info: 'fa-info' };
    const el = document.createElement('div');
    el.className = `fixed top-4 right-4 z-[9999] ${colors[type] || colors.info} text-white px-4 py-3 rounded-md shadow-lg text-sm flex items-center gap-2 animate-fade-in`;
    el.innerHTML = `<i class="fas ${icons[type] || icons.info}"></i><span>${msg}</span>`;
    document.body.appendChild(el);
    setTimeout(() => el.remove(), 3500);
}