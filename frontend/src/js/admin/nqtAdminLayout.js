// nqtAdminLayout.js — shared admin shell for all Vite admin pages

export function nqtInitAdminLayout(activePage) {
    // Auth guard
    const token = localStorage.getItem('nqt_admin_token');
    if (!token) {
        window.location.href = '/admin/login';
        return;
    }

    // Inject global stylesheet to ensure Tailwind config and CSS variables are loaded
    if (!document.querySelector('link[href*="input.css"]')) {
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = '/src/css/input.css';
        document.head.appendChild(link);
    }
    
    // Inject fonts
    if (!document.querySelector('link[href*="fonts.googleapis.com"]')) {
        const fontLink = document.createElement('link');
        fontLink.rel = 'stylesheet';
        fontLink.href = 'https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@0,600;0,700;0,800;0,900;1,700&family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,400&family=Inter:wght@400;500;600;700;800;900&display=swap';
        document.head.appendChild(fontLink);
    }

    // Dynamic Theme Loader
    (async function() {
        function hexToRgb(hex) {
            const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
            return result ? parseInt(result[1], 16) + ', ' + parseInt(result[2], 16) + ', ' + parseInt(result[3], 16) : null;
        }
        
        function applyColor(type, hex) {
            if (!hex) return;
            document.documentElement.style.setProperty('--' + type + '-color', hex);
            const rgb = hexToRgb(hex);
            if (rgb) document.documentElement.style.setProperty('--' + type + '-rgb', rgb);
        }

        const cachedPrimary = localStorage.getItem('ic-primary-color');
        const cachedSecondary = localStorage.getItem('ic-secondary-color');
        if (cachedPrimary) applyColor('primary', cachedPrimary);
        if (cachedSecondary) applyColor('secondary', cachedSecondary);

        try {
            const res = await fetch('/api/nqt-public/cau-hinh-ui');
            if (!res.ok || !res.headers.get('content-type')?.includes('application/json')) throw new Error('Not JSON');
            const data = await res.json();
            if (data && data.nqt_thanh_cong) {
                let pColor = null, sColor = null;
                let configData = {};
                data.nqt_du_lieu.forEach(row => {
                    if (row.g6_khoa === 'g6_mau_chu_dao' && row.g6_gia_tri) pColor = row.g6_gia_tri;
                    if (row.g6_khoa === 'g6_mau_phu' && row.g6_gia_tri) sColor = row.g6_gia_tri;
                    configData[row.g6_khoa] = row.g6_gia_tri;
                });
                
                localStorage.setItem('ic-site-config', JSON.stringify(configData));

                if (pColor && pColor !== cachedPrimary) {
                    applyColor('primary', pColor);
                    localStorage.setItem('ic-primary-color', pColor);
                }
                if (sColor && sColor !== cachedSecondary) {
                    applyColor('secondary', sColor);
                    localStorage.setItem('ic-secondary-color', sColor);
                }
                
                applyConfigToAdminDOM(configData);
            }
        } catch(e) { console.error('Lỗi tải cấu hình:', e); }

        function applyConfigToAdminDOM(cfg) {
            if (cfg['g6_logo_url']) {
                const brandContainer = document.getElementById('ic-admin-brand-container');
                if (brandContainer) {
                    brandContainer.classList.remove('p-6');
                    brandContainer.classList.add('px-4', 'py-2');
                    brandContainer.innerHTML = `<img src="${cfg['g6_logo_url']}" style="width: 100%; height: 100%; max-height: 76px; object-fit: contain;" alt="Logo">`;
                }
            } else if (cfg['g6_ten_website']) {
                const brandEl = document.getElementById('ic-admin-brand');
                if (brandEl) brandEl.textContent = cfg['g6_ten_website'];
            }
            
            if (cfg['g6_ten_website']) {
                // Update page title suffix
                const activeItem = document.querySelector('.nqt-sidebar-item.active');
                if (activeItem) {
                    document.title = activeItem.querySelector('span').textContent + ' - ' + cfg['g6_ten_website'] + ' Admin';
                }
            }
            
            if (cfg['g6_favicon_url']) {
                let link = document.querySelector("link[rel~='icon']");
                if (!link) {
                    link = document.createElement('link');
                    link.rel = 'icon';
                    document.head.appendChild(link);
                }
                link.href = cfg['g6_favicon_url'];
            }
        }

        // Apply cached config
        const cachedConfigStr = localStorage.getItem('ic-site-config');
        if (cachedConfigStr) {
            try { 
                // We need to wait for DOM to be ready to apply brand name, but the layout is dynamically created!
                // Actually, nqtAdminLayout.js creates the DOM below. We should call applyConfigToAdminDOM AFTER DOM injection!
            } catch(e) {}
        }
    })();

    // Inject base styles — Premium Design System v2
    const style = document.createElement('style');
    style.textContent = `
        /* ===== BODY & LAYOUT ===== */
        body { 
            font-family: 'Inter', sans-serif; 
            
        }
        
        
        /* Glassmorphism sidebar overrides */
        .dark aside {
            background: rgba(9, 11, 15, 0.7) !important;
            backdrop-filter: blur(24px) saturate(180%) !important;
            -webkit-backdrop-filter: blur(24px) saturate(180%) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
        }
        
        /* Modernized scrollbars for layout sidebar list */
        aside *::-webkit-scrollbar {
            width: 4px;
        }
        aside *::-webkit-scrollbar-thumb {
            background: rgba(197, 160, 89, 0.2) !important;
            border-radius: 2px;
        }
        
        /* Glassmorphism headers */
        .dark header {
            background: rgba(9, 11, 15, 0.75) !important;
            backdrop-filter: blur(20px) !important;
            -webkit-backdrop-filter: blur(20px) !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.06) !important;
        }
    
/* ===== SIDEBAR — Industrial Solid ===== */
        aside {
            background: #090b0e !important;
            border-color: rgba(255, 255, 255, 0.05) !important;
            box-shadow: 10px 0 50px rgba(0,0,0,0.5) !important;
        }
        
        .dark aside {
            background: #090b0e !important;
        }

        aside > div:first-child::after {
            content: '';
            position: absolute;
            bottom: 0; left: 0; right: 0; height: 1px;
            background: linear-gradient(90deg, transparent, #C5A059, transparent);
        }

        /* ===== HEADER — Dark Glass ===== */
        header {
            background: rgba(10, 10, 10, 0.8) !important;
            backdrop-filter: blur(20px) !important;
            -webkit-backdrop-filter: blur(20px) !important;
            border-bottom: 1px solid rgba(197, 160, 89, 0.15) !important;
            box-shadow: 0 4px 30px rgba(0,0,0,0.3) !important;
        }
        header::after {
            content: '';
            position: absolute;
            bottom: -1px; left: 0; right: 0; height: 1px;
            background: linear-gradient(90deg, transparent 0%, #C5A059 50%, transparent 100%);
            opacity: 0.3;
        }

        /* ===== PRIMARY BUTTONS — Gold Industrial ===== */
        button[class*="bg-[#191919]"], 
        a[class*="bg-[#191919]"],
        button[type="submit"],
        .nqt-primary-btn {
            background: #C5A059 !important;
            color: #000000 !important;
            border: 1px solid #C5A059 !important;
            box-shadow: 0 0 20px rgba(197, 160, 89, 0.2) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            border-radius: 4px !important;
            font-weight: 800 !important;
            font-family: 'Barlow Condensed', sans-serif !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
        }
        button[class*="bg-[#191919]"]:hover, 
        a[class*="bg-[#191919]"]:hover,
        button[type="submit"]:hover {
            background: transparent !important;
            color: #C5A059 !important;
            box-shadow: 0 0 30px rgba(197, 160, 89, 0.4) !important;
            transform: translateY(-1px) !important;
        }

        /* ===== SIDEBAR ITEMS — Industrial Gold ===== */
        .nqt-sidebar-item {
            font-family: 'Barlow Condensed', sans-serif;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
            margin: 2px 12px !important;
            border-radius: 4px !important;
            transition: all 0.2s ease !important;
            color: var(--nqt-sidebar-text) !important;
        }
        .nqt-sidebar-item.active {
            background: #C5A059 !important;
            color: #000000 !important;
            font-weight: 800 !important;
            box-shadow: 0 4px 15px rgba(197, 160, 89, 0.3) !important;
        }
        .nqt-sidebar-item:not(.active):hover {
            background: rgba(255, 255, 255, 0.05) !important;
            color: #C5A059 !important;
        }
        .nqt-sidebar-item.active i, .nqt-sidebar-item.active span {
            color: #000000 !important;
        }
        .nqt-sidebar-item:not(.active) i {
            color: #C5A059 !important;
            opacity: 0.7;
        }
        .nqt-sidebar-item:not(.active) span {
            color: var(--nqt-sidebar-text) !important;
        }
        .nqt-sidebar-item:not(.active):hover span {
            color: #C5A059 !important;
        }

        :root {
            --nqt-bg: #F8F8F5;
            --nqt-surface: #FFFFFF;
            --nqt-text: #1A1A1A;
            --nqt-text-dim: #666666;
            --nqt-border: rgba(0,0,0,0.08);
            --nqt-gold: #C5A059;
            --nqt-gold-glow: rgba(197, 160, 89, 0.1);
            --nqt-sidebar: #FFFFFF; /* Light sidebar for Light Mode */
            --nqt-sidebar-text: #444444;
            --nqt-sidebar-border: rgba(0,0,0,0.05);
        }
        .dark {
            --nqt-bg: #000000;
            --nqt-surface: #090b0e;
            --nqt-text: #F5F5F0;
            --nqt-text-dim: rgba(255,255,255,0.5);
            --nqt-border: rgba(255,255,255,0.05);
            --nqt-gold: #C5A059;
            --nqt-gold-glow: rgba(197, 160, 89, 0.2);
            --nqt-sidebar: #090b0e; /* Dark sidebar for Dark Mode */
            --nqt-sidebar-text: rgba(255,255,255,0.6);
            --nqt-sidebar-border: rgba(255,255,255,0.05);
        }

        /* ===== GLOBAL THEME OVERRIDES ===== */
        body {
            background-color: var(--nqt-bg) !important;
            color: var(--nqt-text) !important;
        }
        
        #nqtAdminWrapper {
            background-color: var(--nqt-bg);
            color: var(--nqt-text);
        }

        header {
            background-color: var(--nqt-surface) !important;
            border-bottom: 1px solid var(--nqt-border) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
        }
        
        aside {
            background-color: var(--nqt-sidebar) !important;
            border-right: 1px solid var(--nqt-sidebar-border) !important;
            box-shadow: 4px 0 20px rgba(0,0,0,0.02) !important;
        }

        /* ===== LIGHT MODE COMPREHENSIVE FIXES ===== */
        /* 1. Override hardcoded dark backgrounds for Cards and Containers */
        html:not(.dark) .bg-\\[\\#1a1a1a\\],
        html:not(.dark) .bg-\\[\\#1c1c1c\\],
        html:not(.dark) .bg-\\[\\#191919\\],
        html:not(.dark) .bg-\\[\\#262626\\],
        html:not(.dark) .bg-zinc-900,
        html:not(.dark) .bg-neutral-900,
        html:not(.dark) .bg-gray-900,
        html:not(.dark) .bg-surface-container,
        html:not(.dark) .bg-surface-container-high {
            background-color: var(--nqt-surface) !important;
            border: 1px solid var(--nqt-border) !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
        }

        /* 2. Override hardcoded dark backgrounds for Inputs and deep elements */
        html:not(.dark) .bg-\\[\\#0a0a0a\\],
        html:not(.dark) .bg-\\[\\#000000\\],
        html:not(.dark) .bg-black,
        html:not(.dark) .bg-background,
        html:not(.dark) .bg-surface-bright {
            background-color: var(--nqt-bg) !important;
            border: 1px solid var(--nqt-border) !important;
        }

        /* 3. Text Color and Table Header Fixes */
        html:not(.dark) thead,
        html:not(.dark) thead tr,
        html:not(.dark) th,
        html:not(.dark) thead th {
            background-color: #f1f5f9 !important; /* Light gray for headers */
            color: var(--nqt-text) !important;
            font-weight: 800 !important;
            border-bottom: 2px solid var(--nqt-border) !important;
        }
        
        html:not(.dark) td {
            color: var(--nqt-text) !important;
            font-weight: 600 !important;
        }
        
        html:not(.dark) .nqt-card-theme p,
        html:not(.dark) .nqt-card-theme span {
            color: var(--nqt-text) !important;
        }
        
        /* Specific fix for dim texts and subtexts */
        html:not(.dark) td.text-\\[\\#666\\],
        html:not(.dark) .text-\\[\\#666\\],
        html:not(.dark) .text-white\\/40,
        html:not(.dark) .text-white\\/50,
        html:not(.dark) .text-white\\/60,
        html:not(.dark) .text-gray-300,
        html:not(.dark) .text-gray-400,
        html:not(.dark) .text-gray-500,
        html:not(.dark) .text-slate-300,
        html:not(.dark) .text-\\[\\#a3a3a3\\],
        html:not(.dark) .text-\\[\\#888\\] {
            color: var(--nqt-text-dim) !important;
        }
        
        /* Force white text classes to be dark */
        html:not(.dark) .text-white,
        html:not(.dark) .text-\\[\\#fafafa\\],
        html:not(.dark) .text-\\[\\#f5f5f5\\],
        html:not(.dark) .text-gray-100,
        html:not(.dark) .text-gray-200 {
            color: var(--nqt-text) !important;
        }

        /* ===== SIDEBAR ITEMS — Industrial Gold ===== */
        .nqt-sidebar-item {
            font-family: 'Barlow Condensed', sans-serif;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
            margin: 2px 12px !important;
            border-radius: 4px !important;
            transition: all 0.2s ease !important;
            color: var(--nqt-sidebar-text) !important;
        }
        .nqt-sidebar-item.active {
            background: #C5A059 !important;
            color: #000000 !important;
            font-weight: 800 !important;
            box-shadow: 0 4px 15px rgba(197, 160, 89, 0.3) !important;
        }
        .nqt-sidebar-item:not(.active):hover {
            background: rgba(var(--nqt-gold-rgb), 0.1) !important;
            color: var(--nqt-gold) !important;
        }
        .nqt-sidebar-item.active i, .nqt-sidebar-item.active span {
            color: #000000 !important;
        }
        .nqt-sidebar-item:not(.active) i {
            color: var(--nqt-gold) !important;
            opacity: 0.8;
        }
        .nqt-sidebar-item:not(.active) span {
            color: var(--nqt-sidebar-text) !important;
        }

        /* ===== TABLE CONTAINERS — Rounded & Elevated ===== */
        div[class*="bg-white"][class*="border"][class*="rounded"] {
            border-radius: 12px !important;
            overflow: hidden;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 4px 20px rgba(0,0,0,0.02);
        }
        .dark div[class*="bg-white"][class*="border"][class*="rounded"],
        .dark div[class*="dark:bg-[#262626]"][class*="border"][class*="rounded"] {
            box-shadow: 0 1px 3px rgba(0,0,0,0.15), 0 4px 20px rgba(0,0,0,0.08);
        }

        /* ===== TABLE ROWS — Gradient Hover ===== */
        /* ===== TABLES — High Contrast Dark ===== */
                table thead th {
            background: #f1f5f9 !important;
            color: var(--nqt-text) !important;
            font-family: 'Barlow Condensed', sans-serif !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
            font-weight: 700 !important;
            border-bottom: 2px solid var(--nqt-border) !important;
        }
        table tbody td {
            border-bottom: 1px solid var(--nqt-border) !important;
            color: var(--nqt-text) !important;
        }
        table tbody tr:hover {
            background: rgba(0, 0, 0, 0.015) !important;
        }
        .dark table thead th {
            background: #090b0e !important;
            color: #C5A059 !important;
            border-bottom: 2px solid rgba(197, 160, 89, 0.3) !important;
        }
        .dark table tbody td {
            border-bottom: 1px solid rgba(255, 255, 255, 0.03) !important;
            color: #F5F5F0 !important;
        }
        .dark table tbody tr:hover {
            background: rgba(197, 160, 89, 0.03) !important;
        }

        /* ===== TABS — Animated Indicator ===== */
        button[id^="nqtTab"] {
            transition: all 0.25s ease !important;
            border-radius: 8px 8px 0 0 !important;
        }
        button[id^="nqtTab"]:hover {
            background: rgba(var(--primary-rgb),0.04);
        }

        /* ===== MODALS — Spring animation ===== */
        .nqt-modal-backdrop { 
            transition: opacity 0.25s ease !important;
            backdrop-filter: blur(8px) saturate(120%);
            -webkit-backdrop-filter: blur(8px) saturate(120%);
        }
        .nqt-modal-backdrop.nqt-modal-hidden { opacity: 0; pointer-events: none; }
        .nqt-modal-panel { 
            transition: opacity 0.3s ease, transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
            border-radius: 16px !important;
            box-shadow: 0 25px 80px rgba(0,0,0,0.15), 0 0 0 1px rgba(var(--primary-rgb),0.05) !important;
        }
        .dark .nqt-modal-panel {
            box-shadow: 0 25px 80px rgba(0,0,0,0.5), 0 0 30px rgba(var(--primary-rgb),0.05) !important;
        }
        .nqt-modal-panel.nqt-modal-hidden { opacity: 0; transform: scale(0.92) translateY(-12px); }

        /* ===== CONTENT AREA ===== */
        #nqt-content-area { 
            transition: opacity 0.25s ease, transform 0.25s ease;
            position: relative;
            z-index: 1;
        }

        /* ===== BADGES & STATUS PILLS ===== */
        span[class*="rounded-full"][class*="text-xs"] {
            font-weight: 600 !important;
            letter-spacing: 0.02em !important;
            border-radius: 20px !important;
            padding: 3px 10px !important;
        }

        /* ===== MISC ===== */
        .nqt-row-selected { background-color: rgba(197, 160, 89, 0.12) !important; border-left: 3px solid var(--nqt-gold) !important; }
        .dark .nqt-row-selected { background-color: rgba(197, 160, 89, 0.25) !important; border-left: 3px solid var(--nqt-gold) !important; }
        tr:not(.nqt-row-selected) { border-left: 3px solid transparent; }
        
        #nqtCmdInput::placeholder { color: #a3a3a3; }
        .nqt-cmd-item.active { background: rgba(var(--primary-rgb),0.06) !important; border-left-color: var(--primary-color) !important; }
        .dark .nqt-cmd-item.active { background: rgba(var(--primary-rgb),0.1) !important; }
        
        #nqtNotifPanel { 
            animation: nqtSlideDown 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
            border-radius: 16px !important;
        }
        @keyframes nqtSlideDown { from { opacity:0; transform: translateY(-8px) scale(0.95); } to { opacity:1; transform: translateY(0) scale(1); } }

        /* ===== AMBIENT GLOW ORBS ===== */
        main {
            position: relative;
        }
        main::before {
            content: '';
            position: fixed;
            top: -30%;
            right: -15%;
            width: 500px;
            height: 500px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(var(--primary-rgb),0.035) 0%, transparent 70%);
            pointer-events: none;
            z-index: 0;
        }
        main::after {
            content: '';
            position: fixed;
            bottom: -25%;
            left: 5%;
            width: 400px;
            height: 400px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(var(--secondary-rgb, 81,139,189),0.03) 0%, transparent 70%);
            pointer-events: none;
            z-index: 0;
        }

        /* ===== STAT NUMBERS ENTRANCE ===== */
        @keyframes nqtFadeUp {
            from { opacity: 0; transform: translateY(6px); }
            to { opacity: 1; transform: translateY(0); }
        }
        p[id^="nqtStat"], span[id^="nqtStat"] {
            animation: nqtFadeUp 0.4s ease forwards;
        }

        /* ===== ACTION BUTTONS — Gold Industrial ===== */
        .nqt-action-btn, td button[title="Sửa"], td button[title="Xóa"], td button[title="Xoá"],
        td button[class*="fa-edit"], td button[class*="fa-trash"] {
            border: 1.5px solid var(--nqt-border) !important;
            border-radius: 4px !important;
            width: 34px !important;
            height: 34px !important;
            transition: all 0.2s ease !important;
            background: transparent !important;
            color: var(--nqt-text-dim) !important;
        }
        .text-gray-500, .text-slate-500, .text-on-surface-variant {
            color: var(--nqt-text-dim) !important;
        }
        
        /* ===== SHORTCUT KEYS (KBD) — Theme Aware ===== */
        kbd {
            background-color: var(--nqt-surface) !important;
            color: var(--nqt-text) !important;
            border: 1px solid var(--nqt-border) !important;
            border-bottom-width: 2px !important;
            border-radius: 4px !important;
            padding: 2px 6px !important;
            font-family: 'JetBrains Mono', 'Fira Code', monospace !important;
            font-size: 10px !important;
            font-weight: 700 !important;
            display: inline-flex !important;
            align-items: center !important;
            box-shadow: 0 1px 0 rgba(0,0,0,0.05) !important;
        }
        .dark kbd {
            box-shadow: 0 1px 0 rgba(255,255,255,0.05) !important;
        }
        
        /* ===== HEADER ELEMENTS — High Contrast ===== */
        header input::placeholder {
            color: var(--nqt-text-dim) !important;
            opacity: 0.7 !important;
        }
        header input {
            color: var(--nqt-text) !important;
        }
        
        #nqtDarkModeBtn i, #nqtNotifBtn i {
            color: var(--nqt-text) !important;
            opacity: 1 !important; /* Full opacity for bolder look */
            font-weight: 900 !important;
            transition: all 0.2s ease !important;
        }
        #nqtDarkModeBtn:hover i, #nqtNotifBtn:hover i {
            color: var(--nqt-gold) !important;
            transform: scale(1.1);
            filter: drop-shadow(0 0 8px var(--nqt-gold-glow));
        }
        
        #nqtNotifBadge {
            background-color: #EF4444 !important; /* Vibrant Red */
            color: white !important;
            border: 2px solid var(--nqt-surface) !important;
            box-shadow: 0 0 10px rgba(239, 68, 68, 0.4) !important;
            font-weight: 800 !important;
        }

        .dark header kbd {
            background-color: rgba(255, 255, 255, 0.08) !important;
            border-color: rgba(255, 255, 255, 0.15) !important;
            color: var(--nqt-gold) !important;
            font-weight: 800 !important;
        }
        
        /* ===== MODALS & COMMAND PALETTE — Theme Aware ===== */
        #nqtCmdOverlay, .nqt-modal-backdrop {
            background-color: rgba(0,0,0,0.5) !important;
            backdrop-filter: blur(8px) !important;
            -webkit-backdrop-filter: blur(8px) !important;
            z-index: 9999 !important;
        }
        
        #nqtCmdOverlay > div, .nqt-modal-panel {
            background-color: var(--nqt-surface) !important;
            border: 1px solid var(--nqt-border) !important;
            box-shadow: 0 20px 50px rgba(0,0,0,0.15) !important;
            color: var(--nqt-text) !important;
        }

        .nqt-cmd-item {
            color: var(--nqt-text) !important;
            border-left: 2px solid transparent !important;
            transition: all 0.2s ease !important;
        }
        .nqt-cmd-item:hover, .nqt-cmd-item.active {
            background: var(--nqt-gold-glow) !important;
            color: var(--nqt-gold) !important;
            border-left-color: var(--nqt-gold) !important;
        }
        
        #nqtCmdInput {
            background-color: var(--nqt-bg) !important;
            color: var(--nqt-text) !important;
            border: 1.5px solid var(--nqt-border) !important;
            border-radius: 8px !important;
        }
        #nqtCmdInput:focus {
            border-color: var(--nqt-gold) !important;
            box-shadow: 0 0 0 3px var(--nqt-gold-glow) !important;
            outline: none !important;
        }
        
        #nqtCmdResults {
            max-height: 400px;
            overflow-y: auto;
        }

        /* ===== NOTIFICATIONS PANEL — Theme Aware ===== */
        #nqtNotifPanel {
            background-color: var(--nqt-surface) !important;
            border: 1px solid var(--nqt-border) !important;
            box-shadow: 0 15px 40px rgba(0,0,0,0.15) !important;
            color: var(--nqt-text) !important;
        }
        
        #nqtNotifPanel > div:first-child, #nqtNotifPanel > div:last-child {
            background-color: rgba(var(--nqt-gold-rgb, 197, 160, 89), 0.03) !important;
            border-color: var(--nqt-border) !important;
        }

        #nqtNotifList button:hover {
            background-color: var(--nqt-gold-glow) !important;
        }

        #nqtNotifList p {
            color: var(--nqt-text) !important;
        }
        #nqtNotifList p.text-on-surface-variant {
            color: var(--nqt-text-dim) !important;
        }
        
        .nqt-notif-item-title {
            color: var(--nqt-text) !important;
            font-weight: 700 !important;
        }
        
        .nqt-notif-item-sub {
            color: var(--nqt-text-dim) !important;
        }
        .nqt-action-btn:hover, td button[title="Sửa"]:hover, td button[title="Xóa"]:hover, td button[title="Xoá"]:hover {
            transform: scale(1.05) !important;
            border-color: var(--nqt-gold) !important;
            color: var(--nqt-gold) !important;
            background: var(--nqt-gold-glow) !important;
            box-shadow: 0 0 15px var(--nqt-gold-glow) !important;
        }
        /* Old text-based delete buttons fallback */
        button[class*="text-[#dc2626]"]:not(.nqt-action-btn) {
            border-radius: 10px !important;
            transition: all 0.2s ease !important;
        }
        button[class*="text-[#dc2626]"]:not(.nqt-action-btn):hover {
            transform: scale(1.05) !important;
            box-shadow: 0 0 12px rgba(220,38,38,0.15) !important;
        }

        /* ===== INPUTS — Refined Focus ===== */
        input[class*="border"][class*="rounded"], 
        select[class*="border"][class*="rounded"],
        textarea[class*="border"][class*="rounded"] {
            border-radius: 10px !important;
            transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
        }
        input[class*="border"][class*="rounded"]:focus, 
        select[class*="border"][class*="rounded"]:focus,
        textarea[class*="border"][class*="rounded"]:focus {
            border-color: var(--primary-color) !important;
            box-shadow: 0 0 0 3px rgba(var(--primary-rgb),0.1), 0 0 15px rgba(var(--primary-rgb),0.05) !important;
        }

        /* ===== PAGINATION BUTTONS ===== */
        button[class*="bg-[#191919]"][class*="text-xs"],
        button[class*="dark:bg-[#fafafa]"][class*="text-xs"] {
            border-radius: 8px !important;
        }

        /* ===== PAGE HEADER TITLE ===== */
        #nqt-page-title {
            font-family: 'Barlow Condensed', sans-serif !important;
            text-transform: uppercase !important;
            letter-spacing: 2px !important;
            font-weight: 800 !important;
            font-size: 1.5rem !important;
            color: #C5A059 !important;
            text-shadow: 0 0 10px rgba(197, 160, 89, 0.2);
        }
        
        h2, h3, h4 {
            font-family: 'Barlow Condensed', sans-serif !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
            font-weight: 700 !important;
        }

        /* ===== SEARCH BUTTON (Ctrl+K) ===== */
        button[onclick="nqtAbrirComandos()"] {
            border-radius: 10px !important;
            transition: all 0.2s ease !important;
        }
        button[onclick="nqtAbrirComandos()"]:hover {
            border-color: rgba(var(--primary-rgb),0.3) !important;
            box-shadow: 0 0 15px rgba(var(--primary-rgb),0.06) !important;
        }

        /* ===== COMMAND PALETTE ===== */
        #nqtCmdOverlay > div {
            border-radius: 20px !important;
            box-shadow: 0 30px 100px rgba(0,0,0,0.3), 0 0 0 1px rgba(var(--primary-rgb),0.08) !important;
        }

        /* ===== SIDEBAR BRAND ICON ===== */
        aside > div:first-child .neon-button {
            border-radius: 8px !important;
            background: #C5A059 !important;
            color: #000000 !important;
            box-shadow: 0 0 15px rgba(197, 160, 89, 0.4) !important;
            animation: nqtBrandPulse 3s ease-in-out infinite;
        }
        @keyframes nqtBrandPulse {
            0%, 100% { box-shadow: 0 0 15px rgba(197, 160, 89, 0.4); }
            50% { box-shadow: 0 0 25px rgba(197, 160, 89, 0.6), 0 0 40px rgba(197, 160, 89, 0.2); }
        }

        /* ===== USER AVATAR — Ring Effect ===== */
        #nqt-user-avatar {
            border: 2px solid transparent !important;
            background-origin: border-box;
            background-clip: padding-box, border-box;
            transition: all 0.3s ease;
        }
        #nqt-user-avatar:hover {
            border-color: rgba(var(--primary-rgb),0.4) !important;
            box-shadow: 0 0 12px rgba(var(--primary-rgb),0.15);
        }

        /* ===== SMOOTH DARK MODE TRANSITION ===== */
        html {
            overflow-y: scroll; /* Keep scrollbar gutter consistent */
        }
        body {
            margin: 0 !important;
            padding: 0 !important;
            transition: background-color 0.3s ease, color 0.3s ease;
        }
        .bg-white, .dark\:bg-\[#090b0e\], .dark\:bg-\[#262626\], .bg-surface-container {
            transition: background-color 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
        }
        button, a, .nqt-sidebar-item {
            transition: background-color 0.2s ease, color 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
        }
    `;
    document.head.appendChild(style);

    // Build sidebar nav HTML
    const navItems = [
        { page: 'dashboard', title: 'Tổng quan', icon: 'fa-chart-line', perms: ['XEM_BAO_CAO', 'G6PT', 'G6QuanLy'] },
        { group: 'Quản lý' },
        { page: 'hoi-vien', title: 'Hội viên', icon: 'fa-users', perms: ['QL_HOI_VIEN', 'G6PT', 'G6QuanLy'] },
        { page: 'khach-hang', title: 'Khách hàng', icon: 'fa-user-tag', perms: ['QL_HOI_VIEN', 'G6QuanLy'] },
        { page: 'goi-tap', title: 'Gói tập', icon: 'fa-box', perms: ['QL_HOI_VIEN', 'G6QuanLy'] },
        { page: 'huan-luyen-vien', title: 'Huấn luyện viên', icon: 'fa-person-running', perms: ['QL_NHAN_VIEN', 'G6QuanLy'] },
        { page: 'lop-hoc', title: 'Lớp học', icon: 'fa-calendar-check', perms: ['QL_HOI_VIEN', 'G6PT', 'G6QuanLy'] },
        { group: 'Kinh doanh' },
        { page: 'don-hang', title: 'Đơn hàng', icon: 'fa-shopping-bag', perms: ['QL_KHO', 'G6QuanLy'] },
        { page: 'thanh-toan', title: 'Thanh toán', icon: 'fa-credit-card', perms: ['QL_KHO', 'G6QuanLy'] },
        { page: 'san-pham', title: 'Sản phẩm', icon: 'fa-tag', perms: ['QL_KHO', 'G6QuanLy'] },
        { page: 'khuyen-mai', title: 'Khuyến mãi', icon: 'fa-percent', perms: ['QL_HE_THONG', 'G6QuanLy'] },
        { page: 'su-kien', title: 'Sự kiện', icon: 'fa-bolt', perms: ['QL_HE_THONG', 'G6QuanLy'] },
        { group: 'Vận hành' },
        { page: 'chi-nhanh', title: 'Chi nhánh', icon: 'fa-store', perms: ['QL_HE_THONG', 'G6QuanLy'] },
        { page: 'nhan-vien', title: 'Nhân viên', icon: 'fa-id-badge', perms: ['QL_NHAN_VIEN', 'G6QuanLy'] },
        { page: 'bao-tri', title: 'Bảo trì thiết bị', icon: 'fa-wrench', perms: ['QL_HE_THONG', 'G6QuanLy'] },
        { page: 'van-chuyen', title: 'Vận chuyển', icon: 'fa-truck', perms: ['QL_KHO', 'G6QuanLy'] },
        { page: 'blog', title: 'Blog', icon: 'fa-newspaper', perms: ['QL_HE_THONG', 'G6QuanLy'] },
        { group: 'Hệ thống' },
        { page: 'bao-cao', title: 'Báo cáo', icon: 'fa-chart-bar', perms: ['XEM_BAO_CAO', 'G6QuanLy'] },
        { page: 'quan-tri', title: 'Quản trị', icon: 'fa-shield', perms: ['G6QuanTri'] },
        { page: 'phan-quyen', title: 'Phân quyền', icon: 'fa-user-shield', perms: ['G6QuanTri'] },
        { page: 'cau-hinh', title: 'Cấu hình', icon: 'fa-cog', perms: ['G6QuanTri'] },
    ];

    // Auth & Permission Filter
    let userRoles = [];
    let userPerms = [];
    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        userRoles = payload.g6_vai_tro || [];
        userPerms = payload.g6_quyen || [];
    } catch(e) {}

    const isAdmin = userRoles.includes('G6QuanTri');
    
    // Filter items based on permission
    const filteredNav = navItems.filter(item => {
        if (isAdmin) return true;
        if (item.group) return true; // Keep groups for now, we'll prune empty groups later
        if (!item.perms) return true;
        return item.perms.some(p => userPerms.includes(p) || userRoles.includes(p));
    });

    // Prune groups that have no items
    const finalNav = [];
    for (let i = 0; i < filteredNav.length; i++) {
        const item = filteredNav[i];
        if (item.group) {
            // Check if there are any non-group items before the next group
            let hasItems = false;
            for (let j = i + 1; j < filteredNav.length; j++) {
                if (filteredNav[j].group) break;
                hasItems = true;
                break;
            }
            if (hasItems) finalNav.push(item);
        } else {
            finalNav.push(item);
        }
    }

    const linkCls = `nqt-sidebar-item nqt-nav-link flex items-center space-x-2.5 px-4 py-2.5 rounded-lg text-sm text-on-surface-variant font-medium transition-colors hover:bg-surface-bright hover:text-on-surface [&.active]:bg-[rgba(var(--primary-rgb,206,59,59),0.15)] dark:[&.active]:bg-[rgba(var(--primary-rgb,206,59,59),0.25)] [&.active]:text-on-surface [&.active]:font-bold`;

    const navHtml = finalNav.map(item => {
        if (item.group) {
            return `<div class="pt-5 pb-2 px-4 text-[11px] font-bold text-outline uppercase tracking-wider">${item.group}</div>`;
        }
        const isActive = item.page === activePage ? ' active' : '';
        return `<a href="/admin/${item.page}" data-page="${item.page}" data-title="${item.title}" class="${linkCls}${isActive}">
            <i class="fas ${item.icon} w-5 text-center text-lg"></i>
            <span>${item.title}</span>
        </a>`;
    }).join('');

    // Build full shell HTML
    const shellHTML = `
    <aside class="w-64 bg-[#090b0e] border-r border-white/5 flex flex-col fixed left-0 top-0 h-full z-20 shadow-2xl">
        <a href="/admin/dashboard" id="ic-admin-brand-container" class="p-6 h-24 flex items-center justify-center border-b border-white/5 relative cursor-pointer hover:opacity-85 transition-opacity">
            <div id="ic-admin-brand-fallback" class="flex items-center space-x-3 w-full">
                <div id="ic-admin-brand-icon" class="w-10 h-10 bg-[#C5A059] text-[#000000] rounded-lg flex items-center justify-center shadow-[0_0_15px_rgba(197, 160, 89,0.3)] neon-button flex-shrink-0">
                    <i class="fas fa-dumbbell text-xl"></i>
                </div>
                <div class="flex flex-col overflow-hidden">
                    <span id="ic-admin-brand" class="text-xl font-header font-black tracking-widest text-[#C5A059] leading-none truncate">G6 GYM</span>
                    <span class="text-[9px] uppercase tracking-[3px] text-white/40 font-header mt-1 truncate">Admin Command</span>
                </div>
            </div>
        </a>
        <nav class="flex-1 py-6 space-y-1 overflow-y-auto">${navHtml}</nav>
        <div class="p-3 border-t border-outline-variant space-y-1">
            <a href="/home" class="w-full flex items-center space-x-3 px-4 py-2.5 rounded-lg text-sm text-[#C5A059] font-medium hover:bg-[#C5A059]/10 transition-colors">
                <i class="fas fa-home w-5 text-center text-lg"></i>
                <span>Về trang chủ</span>
            </a>
            <button onclick="nqtLogout()" class="w-full flex items-center space-x-3 px-4 py-2.5 rounded-lg text-sm text-error font-medium hover:bg-error/10 transition-colors">
                <i class="fas fa-sign-out-alt w-5 text-center text-lg"></i>
                <span>Đăng xuất</span>
            </button>
        </div>
    </aside>

    <main class="flex-1 pl-64 min-h-screen flex flex-col relative w-full">
        <header class="h-16 bg-surface-container-lowest/80 backdrop-blur-md border-b border-outline-variant flex items-center justify-between px-8 sticky top-0 z-10 shadow-sm">
            <div class="flex items-center space-x-4">
                <h1 id="nqt-page-title" class="text-base font-bold text-on-surface">Admin</h1>
            </div>
            <div class="flex items-center gap-2">
                <button onclick="nqtAbrirComandos()" title="Tìm kiếm nhanh (Ctrl+K)"
                    class="hidden sm:flex items-center gap-2 px-3 py-2 rounded-lg text-xs font-medium text-on-surface-variant border border-outline-variant hover:border-outline hover:text-on-surface bg-surface-bright transition-colors">
                    <i class="fas fa-search"></i>
                    <span>Tìm kiếm...</span>
                    <kbd class="hidden md:inline-flex items-center px-1.5 py-0.5 bg-background rounded text-[10px] font-mono border border-outline-variant">⌘K</kbd>
                </button>
                <div class="relative">
                    <button id="nqtNotifBtn" onclick="nqtToggleNotif()"
                        class="w-10 h-10 rounded-full flex items-center justify-center text-on-surface-variant hover:bg-surface-bright hover:text-on-surface transition-colors relative">
                        <span class="w-6 h-6 flex items-center justify-center">
                            <i class="fas fa-bell text-base"></i>
                        </span>
                        <span id="nqtNotifBadge" class="hidden absolute top-1 right-1 w-4 h-4 bg-error text-white text-[9px] font-bold rounded-full flex items-center justify-center border-2 border-surface-container-lowest"></span>
                    </button>
                    <div id="nqtNotifPanel" class="hidden absolute right-0 top-12 w-80 bg-surface-container border border-outline-variant rounded-xl shadow-xl z-50 overflow-hidden">
                        <div class="px-5 py-4 border-b border-outline-variant bg-surface-container-high flex items-center justify-between">
                            <span class="text-sm font-bold text-on-surface">Thông báo</span>
                            <button onclick="nqtDocTatCaThongBao()" class="text-xs font-medium text-on-surface-variant hover:text-on-surface transition-colors">Đánh dấu đã đọc</button>
                        </div>
                        <div id="nqtNotifList" class="max-h-72 overflow-y-auto divide-y divide-outline-variant">
                            <div class="px-5 py-8 text-center text-sm text-on-surface-variant">
                                <i class="fas fa-circle-notch fa-spin mb-3 block text-xl text-on-surface-variant"></i>Đang tải...
                            </div>
                        </div>
                        <div class="px-5 py-3 border-t border-outline-variant text-center bg-surface-container-high">
                            <button onclick="nqtNavigateTo('/admin/hoi-vien','Hội viên'); nqtDongNotif();" class="text-xs font-medium text-on-surface-variant hover:text-on-surface">Xem tất cả</button>
                        </div>
                    </div>
                </div>
                <button id="nqtDarkModeBtn" onclick="nqtToggleDarkMode()"
                    class="w-10 h-10 rounded-full flex items-center justify-center text-on-surface-variant hover:bg-surface-bright hover:text-on-surface transition-colors flex-shrink-0"
                    title="Chuyển đổi Dark/Light mode">
                    <span class="w-6 h-6 flex items-center justify-center">
                        <i id="nqtDarkModeIcon" class="fas fa-moon text-base"></i>
                    </span>
                </button>
                <div class="w-px h-6 bg-outline-variant mx-1"></div>
                <div class="flex items-center gap-3 cursor-pointer hover:opacity-80 transition-opacity">
                    <div class="text-right hidden sm:block">
                        <div id="nqt-user-name" class="text-sm font-bold text-on-surface">...</div>
                        <div id="nqt-user-role" class="text-xs text-on-surface-variant">Admin</div>
                    </div>
                    <div id="nqt-user-avatar" class="w-10 h-10 bg-surface-variant rounded-full flex items-center justify-center overflow-hidden flex-shrink-0 border border-outline-variant">
                        <i class="fas fa-user text-on-surface-variant text-sm"></i>
                    </div>
                </div>
            </div>
        </header>
        <div id="nqt-content-area" class="p-6 flex-1"></div>
    </main>

    <div id="nqt-toast-container" class="fixed bottom-4 right-4 z-[9999] space-y-2 pointer-events-none"></div>

    <div id="nqtCmdOverlay" class="hidden fixed inset-0 z-[9998] flex items-start justify-center pt-24 px-4" onclick="if(event.target===this) nqtInchideComenzi()">
        <div class="w-full max-w-2xl bg-surface-container rounded-2xl shadow-2xl border border-outline-variant overflow-hidden transform transition-all duration-300">
            <div class="p-4 border-b border-outline-variant flex items-center space-x-3 bg-surface-container-high">
                <i class="fas fa-search text-on-surface-variant"></i>
                <input type="text" id="nqtCmdInput" placeholder="Tìm trang, tính năng..." oninput="nqtLocLenh(this.value)" onkeydown="nqtCmdKeyDown(event)"
                    class="flex-1 bg-transparent border-0 focus:ring-0 text-sm placeholder-on-surface-variant/50">
                <div class="flex items-center space-x-1">
                    <kbd class="px-1.5 py-0.5 bg-background rounded text-[10px] font-mono border border-outline-variant text-outline">ESC</kbd>
                </div>
            </div>
            <div id="nqtCmdResults" class="max-h-[60vh] overflow-y-auto py-2 custom-scrollbar"></div>
            <div class="px-4 py-2 border-t border-outline-variant bg-surface-container-low flex items-center justify-between text-[10px] text-outline font-medium uppercase tracking-wider">
                <div class="flex items-center space-x-3">
                    <span class="flex items-center"><i class="fas fa-arrow-up mr-1"></i><i class="fas fa-arrow-down mr-1"></i> Di chuyển</span>
                    <span class="flex items-center"><i class="fas fa-level-down-alt fa-rotate-90 mr-1"></i> Chọn</span>
                </div>
                <span>Quick Actions</span>
            </div>
        </div>
    </div>`;

    // Inject into body before page content
    const wrapper = document.createElement('div');
    wrapper.id = 'nqtAdminWrapper';
    wrapper.className = 'bg-background text-on-surface min-h-screen flex transition-colors duration-200';
    wrapper.innerHTML = shellHTML;
    document.body.insertBefore(wrapper, document.body.firstChild);

    // Initialize specific page logics
    const titleMap = navItems.reduce((acc, item) => ({...acc, [item.page]: item.title}), {});
    const pTitle = titleMap[activePage] || 'Admin';
    document.getElementById('nqt-page-title').textContent = pTitle;
    
    // Set document title from config or default
    const cStr = localStorage.getItem('ic-site-config');
    let siteName = 'G6 GYM';
    if (cStr) {
        try {
            const cfg = JSON.parse(cStr);
            if (cfg['g6_ten_website']) siteName = cfg['g6_ten_website'];
            
            if (cfg['g6_logo_url']) {
                const brandContainer = document.getElementById('ic-admin-brand-container');
                if (brandContainer) {
                    brandContainer.classList.remove('p-6');
                    brandContainer.classList.add('px-4', 'py-2');
                    brandContainer.innerHTML = `<img src="${cfg['g6_logo_url']}" style="width: 100%; height: 100%; max-height: 76px; object-fit: contain;" alt="Logo">`;
                }
            } else if (cfg['g6_ten_website']) {
                const brandEl = document.getElementById('ic-admin-brand');
                if (brandEl) brandEl.textContent = siteName;
            }
            
            if (cfg['g6_favicon_url']) {
                let link = document.querySelector("link[rel~='icon']");
                if (!link) { link = document.createElement('link'); link.rel = 'icon'; document.head.appendChild(link); }
                link.href = cfg['g6_favicon_url'];
            }
        } catch(e) {}
    }
    document.title = `${pTitle} - ${siteName} Admin`;

    // Move page content into content area
    const contentArea = document.getElementById('nqt-content-area');
    const pageContent = document.getElementById('nqt-page-content');
    if (pageContent && contentArea) {
        contentArea.appendChild(pageContent);
        pageContent.style.display = '';
    }

    // Preserve Sidebar Scroll Position across page loads
    const sidebarNav = document.querySelector('aside nav');
    if (sidebarNav) {
        const savedScroll = sessionStorage.getItem('nqt_sidebar_scroll');
        if (savedScroll) {
            // Use requestAnimationFrame to ensure layout is calculated before setting scrollTop
            requestAnimationFrame(() => {
                sidebarNav.scrollTop = parseInt(savedScroll, 10);
            });
        }
    }
    
    // Save scroll position only when leaving the page to avoid scroll reset bugs on unload
    window.addEventListener('beforeunload', () => {
        const currentNav = document.querySelector('aside nav');
        if (currentNav) {
            sessionStorage.setItem('nqt_sidebar_scroll', currentNav.scrollTop);
        }
    });

    // Set body style
    document.body.className = 'bg-[#FAFAF9] dark:bg-[#1a1a1a]';

    // Init avatar generator
    (function() {
        function nqtStringHash(str) {
            let hash = 0;
            for (let i = 0; i < str.length; i++) {
                const char = str.charCodeAt(i);
                hash = ((hash << 5) - hash) + char;
                hash = hash & hash;
            }
            return Math.abs(hash);
        }
        const NQT_COLORS = [
            ['#667eea','#764ba2'],['#f093fb','#f5576c'],['#4facfe','#00f2fe'],
            ['#43e97b','#38f9d7'],['#fa709a','#fee140'],['#a8edea','#fed6e3'],
            ['#ffecd2','#fcb69f'],['#667eea','#764ba2'],['#ff9a9e','#fecfef'],['#a18cd1','#fbc2eb'],
        ];
        const NQT_EYES = [
            `<circle cx="14" cy="18" r="3" fill="currentColor"/><circle cx="26" cy="18" r="3" fill="currentColor"/>`,
            `<rect x="12" y="14" width="3" height="10" rx="1.5" fill="currentColor"/><rect x="9" y="17" width="9" height="3" rx="1.5" fill="currentColor"/><rect x="23" y="14" width="3" height="10" rx="1.5" fill="currentColor"/><rect x="20" y="17" width="9" height="3" rx="1.5" fill="currentColor"/>`,
            `<rect x="10" y="17" width="8" height="3" rx="1.5" fill="currentColor"/><rect x="22" y="17" width="8" height="3" rx="1.5" fill="currentColor"/>`,
            `<path d="M10 19c0-2 2-4 4-4s4 2 4 4" stroke="currentColor" stroke-width="2.5" fill="none" stroke-linecap="round"/><path d="M22 19c0-2 2-4 4-4s4 2 4 4" stroke="currentColor" stroke-width="2.5" fill="none" stroke-linecap="round"/>`,
        ];
        window.nqtTaoAvatar = function(name, size = 40) {
            if (!name) name = 'U';
            const hash = nqtStringHash(name);
            const colors = NQT_COLORS[hash % NQT_COLORS.length];
            const eyes = NQT_EYES[hash % NQT_EYES.length];
            const initial = name.trim().split(' ').pop()[0].toUpperCase();
            const gradientId = `nqtGrad${hash}`;
            const rotations = [{x:-5,y:5},{x:5,y:5},{x:5,y:0},{x:0,y:5},{x:-5,y:0},{x:0,y:0},{x:0,y:-5},{x:-5,y:-5},{x:5,y:-5}];
            const rot = rotations[hash % rotations.length];
            return `<svg width="${size}" height="${size}" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg" style="border-radius:50%;"><defs><linearGradient id="${gradientId}" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:${colors[0]}"/><stop offset="100%" style="stop-color:${colors[1]}"/></linearGradient><radialGradient id="${gradientId}h" cx="50%" cy="30%" r="60%"><stop offset="0%" style="stop-color:rgba(255,255,255,0.2)"/><stop offset="100%" style="stop-color:rgba(255,255,255,0)"/></radialGradient></defs><rect width="40" height="40" fill="url(#${gradientId})" rx="20"/><rect width="40" height="40" fill="url(#${gradientId}h)" rx="20"/><g transform="rotate(${rot.x} 20 20)" style="color:rgba(255,255,255,0.9)">${eyes}</g><text x="20" y="32" text-anchor="middle" fill="rgba(255,255,255,0.9)" font-size="10" font-weight="600" font-family="Inter,sans-serif">${initial}</text></svg>`;
        };
        window.nqtAvatarHtml = function(name, size = 40, className = '') {
            return `<div class="${className}" style="width:${size}px;height:${size}px;border-radius:50%;overflow:hidden;flex-shrink:0;">${nqtTaoAvatar(name, size)}</div>`;
        };
    })();

    // Dark mode
    window.nqtToggleDarkMode = function() {
        const html = document.documentElement;
        const icon = document.getElementById('nqtDarkModeIcon');
        const isDark = html.classList.toggle('dark');
        localStorage.setItem('nqt_dark_mode', isDark);
        if (icon) icon.className = isDark ? 'fas fa-sun text-base' : 'fas fa-moon text-base';
        
        // Notify pages about theme change so they can re-render charts without re-fetching
        window.dispatchEvent(new CustomEvent('nqt-theme-changed', { detail: { isDark } }));
    };
    (function() {
        const isDark = localStorage.getItem('nqt_dark_mode') !== 'false'; // Default to dark
        if (isDark) {
            document.documentElement.classList.add('dark');
            const icon = document.getElementById('nqtDarkModeIcon');
            if (icon) icon.className = 'fas fa-sun text-base';
        } else {
            document.documentElement.classList.remove('dark');
        }
    })();

    // Toast — Premium v2
    window.nqtToast = function(msg, type = 'success') {
        const container = document.getElementById('nqt-toast-container');
        const icons = { success:'fa-check-circle', error:'fa-times-circle', warn:'fa-exclamation-triangle', info:'fa-info-circle' };
        const iconColors = {
            success: 'background: linear-gradient(135deg, #10b981, #059669); color: #fff;',
            error: 'background: linear-gradient(135deg, #ef4444, #dc2626); color: #fff;',
            warn: 'background: linear-gradient(135deg, #f97316, #ea580c); color: #fff;',
            info: 'background: linear-gradient(135deg, var(--secondary-color), #3b82f6); color: #fff;',
        };
        const progressColors = { success: '#10b981', error: '#ef4444', warn: '#f97316', info: 'var(--secondary-color)' };
        const el = document.createElement('div');
        el.style.cssText = 'pointer-events:auto; display:flex; align-items:center; gap:12px; padding:14px 18px; border-radius:14px; font-size:14px; font-weight:600; box-shadow:0 8px 32px rgba(0,0,0,0.12), 0 0 0 1px rgba(255,255,255,0.06); background:var(--nqt-surface); color:var(--nqt-text); border:1px solid var(--nqt-border); position:relative; overflow:hidden; transform:translateX(40px); opacity:0; transition:all 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);';
        el.innerHTML = `<div style="width:32px;height:32px;border-radius:10px;display:flex;align-items:center;justify-content:center;flex-shrink:0;${iconColors[type]||iconColors.info}"><i class="fas ${icons[type]||'fa-info-circle'} text-sm"></i></div><span style="flex:1">${msg}</span><div style="position:absolute;bottom:0;left:0;right:0;height:3px;background:${progressColors[type]||progressColors.info};border-radius:0 0 14px 14px;animation:nqtToastProgress 3s linear forwards;"></div>`;
        // Inject keyframes if not exists
        if (!document.getElementById('nqtToastKF')) {
            const kf = document.createElement('style');
            kf.id = 'nqtToastKF';
            kf.textContent = '@keyframes nqtToastProgress { from { width: 100%; } to { width: 0%; } }';
            document.head.appendChild(kf);
        }
        container.appendChild(el);
        requestAnimationFrame(() => { el.style.transform = 'translateX(0)'; el.style.opacity = '1'; });
        setTimeout(() => { el.style.transform = 'translateX(40px)'; el.style.opacity = '0'; setTimeout(() => el.remove(), 350); }, 3000);
    };

    // API wrapper with Auto-Toast
    window.nqtApi = {
        async fetch(url, options = {}) {
            const method = (options.method || 'GET').toUpperCase();
            if (!options.headers) options.headers = {};
            options.headers['Accept'] = 'application/json';
            const adminToken = localStorage.getItem('nqt_admin_token');
            if (adminToken) options.headers['Authorization'] = 'Bearer ' + adminToken;
            options.credentials = 'include';
            
            if (options.body && typeof options.body === 'object' && !(options.body instanceof FormData)) {
                options.headers['Content-Type'] = 'application/json';
                options.body = JSON.stringify(options.body);
            } else if (method !== 'GET' && !options.body) {
                options.headers['Content-Type'] = 'application/json';
                options.body = '{}';
            }

            try {
                const response = await fetch(url, options);
                
                if (response.status === 401) {
                    localStorage.removeItem('nqt_admin_token');
                    window.location.href = '/admin/login';
                    return null;
                }

                const ct = response.headers.get('content-type') || '';
                if (!ct.includes('application/json')) {
                    return { nqt_thanh_cong: false, nqt_thong_diep: 'Phản hồi không hợp lệ' };
                }

                const data = await response.json();

                // Auto-Toast for non-GET success
                if (data.nqt_thanh_cong && method !== 'GET') {
                    let msg = data.nqt_thong_diep || 'Thao tác thành công';
                    if (method === 'POST') msg = data.nqt_thong_diep || 'Thêm mới thành công';
                    if (method === 'PUT') msg = data.nqt_thong_diep || 'Cập nhật thành công';
                    if (method === 'DELETE') msg = data.nqt_thong_diep || 'Xóa thành công';
                    nqtToast(msg, 'success');
                } else if (!data.nqt_thanh_cong && method !== 'GET') {
                    nqtToast(data.nqt_thong_diep || 'Có lỗi xảy ra', 'error');
                }

                return data;
            } catch (error) {
                console.error('API Error:', error);
                if (method !== 'GET') nqtToast('Lỗi kết nối máy chủ', 'error');
                return { nqt_thanh_cong: false, nqt_thong_diep: 'Lỗi kết nối máy chủ' };
            }
        }
    };

    // Button loading
    window.nqtBtnLoading = function(btn, msg = 'Đang xử lý...') {
        if (!btn) return () => {};
        const origText = btn.innerHTML, origDisabled = btn.disabled;
        btn.disabled = true;
        btn.innerHTML = `<i class="fas fa-circle-notch fa-spin text-xs mr-1.5"></i>${msg}`;
        btn.style.opacity = '0.75';
        return () => { btn.disabled = origDisabled; btn.innerHTML = origText; btn.style.opacity = ''; };
    };

    // Logout
    window.nqtLogout = function() {
        localStorage.removeItem('nqt_admin_token');
        window.location.href = '/admin/login';
    };

    // Global Modal Drag Protection
    window.nqtGlobalMousedownTarget = null;
    ['mousedown', 'touchstart'].forEach(evt => {
        document.addEventListener(evt, (e) => {
            window.nqtGlobalMousedownTarget = e.target;
        }, { passive: true });
    });

    // Modal helpers
    window.nqtMoModal = function(id) {
        const backdrop = document.getElementById(id);
        if (!backdrop) return;
        
        // Prevent layout shift by adding padding equal to scrollbar width
        const scrollbarWidth = window.innerWidth - document.documentElement.clientWidth;
        
        backdrop.classList.remove('hidden');
        backdrop.classList.add('nqt-modal-backdrop','nqt-modal-hidden');
        const panel = backdrop.querySelector(':scope > div');
        if (panel) panel.classList.add('nqt-modal-panel','nqt-modal-hidden');
        
        if (scrollbarWidth > 0) {
            document.body.style.paddingRight = `${scrollbarWidth}px`;
            const header = document.querySelector('header');
            if (header) header.style.paddingRight = `calc(2rem + ${scrollbarWidth}px)`; // 2rem is px-8 default
        }
        document.body.style.overflow = 'hidden';
        
        backdrop.getBoundingClientRect();
        backdrop.classList.remove('nqt-modal-hidden');
        if (panel) panel.classList.remove('nqt-modal-hidden');
    };
    window.nqtDongModal = function(id) {
        // Prevent closing if user dragged from inside the modal to the backdrop
        if (window.event && window.event.type === 'click') {
            const e = window.event;
            // If the user clicked exactly on the backdrop element
            if (e.target && e.target.id === id) {
                const mousedownTarget = window.nqtGlobalMousedownTarget;
                // If the drag started on an element INSIDE the modal, block the close
                if (mousedownTarget && mousedownTarget !== e.target && e.target.contains(mousedownTarget)) {
                    return;
                }
            }
        }
        
        const backdrop = document.getElementById(id);
        if (!backdrop) return;
        backdrop.classList.add('nqt-modal-backdrop','nqt-modal-hidden');
        const panel = backdrop.querySelector(':scope > div');
        if (panel) panel.classList.add('nqt-modal-panel','nqt-modal-hidden');
        setTimeout(() => {
            backdrop.classList.add('hidden');
            backdrop.classList.remove('nqt-modal-backdrop','nqt-modal-hidden');
            if (panel) panel.classList.remove('nqt-modal-panel','nqt-modal-hidden');
            
            document.body.style.overflow = '';
            document.body.style.paddingRight = '';
            const header = document.querySelector('header');
            if (header) header.style.paddingRight = '';
        }, 180);
    };

    // Notifications
    let nqtNotifOpen = false, nqtNotifData = [];
    window.nqtToggleNotif = function() {
        nqtNotifOpen = !nqtNotifOpen;
        const panel = document.getElementById('nqtNotifPanel');
        if (nqtNotifOpen) {
            panel.classList.remove('hidden');
            nqtTaiThongBao();
            setTimeout(() => document.addEventListener('click', nqtCloseNotifOutside), 10);
        } else { nqtDongNotif(); }
    };
    window.nqtDongNotif = function() {
        nqtNotifOpen = false;
        document.getElementById('nqtNotifPanel').classList.add('hidden');
        document.removeEventListener('click', nqtCloseNotifOutside);
    };
    function nqtCloseNotifOutside(e) {
        const btn = document.getElementById('nqtNotifBtn');
        const panel = document.getElementById('nqtNotifPanel');
        if (!btn?.contains(e.target) && !panel?.contains(e.target)) nqtDongNotif();
    }
    async function nqtTaiThongBao() {
        const list = document.getElementById('nqtNotifList');
        const [resHv, resTT] = await Promise.all([
            nqtApi.fetch('/api/nqt-hoi-vien?g6_sap_het_han=7&g6_gioi_han=5'),
            nqtApi.fetch('/api/nqt-thanh-toan?g6_trang_thai=cho_xu_ly&g6_gioi_han=5'),
        ]);
        nqtNotifData = [];
        if (resHv?.nqt_thanh_cong) {
            (resHv.nqt_du_lieu.g6_danh_sach || []).forEach(hv => {
                nqtNotifData.push({ type:'warning', icon:'fa-clock', title:`${hv.g6_ho_ten} — sắp hết hạn`, sub:'Gói tập', url:'/admin/hoi-vien' });
            });
        }
        if (resTT?.nqt_thanh_cong) {
            const count = resTT.nqt_du_lieu.g6_tong || 0;
            if (count > 0) nqtNotifData.push({ type:'info', icon:'fa-credit-card', title:`${count} thanh toán chờ xác nhận`, sub:'Thanh toán', url:'/admin/thanh-toan' });
        }
        const badge = document.getElementById('nqtNotifBadge');
        if (nqtNotifData.length > 0) { badge.textContent = nqtNotifData.length > 9 ? '9+' : nqtNotifData.length; badge.classList.remove('hidden'); }
        else badge.classList.add('hidden');
        if (nqtNotifData.length === 0) {
            list.innerHTML = `<div class="px-5 py-8 text-center text-sm text-on-surface-variant"><i class="fas fa-check-circle text-on-surface-variant opacity-50 text-2xl mb-3 block"></i>Không có thông báo mới</div>`;
            return;
        }
        const typeColors = { 
            warning: 'text-orange-500 bg-orange-500/10 dark:bg-orange-500/20', 
            info: 'text-secondary bg-[rgba(var(--secondary-rgb,81,139,189),0.15)] dark:bg-[rgba(var(--secondary-rgb,81,139,189),0.25)]' 
        };
        list.innerHTML = nqtNotifData.map(n => `
            <button onclick="window.location.href='${n.url}'; nqtDongNotif();" class="w-full flex items-start space-x-4 px-5 py-3 hover:bg-surface-bright transition-colors text-left border-b border-outline-variant/50 last:border-0 group">
                <div class="w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5 ${typeColors[n.type]||typeColors.info}">
                    <i class="fas ${n.icon} text-sm"></i>
                </div>
                <div class="flex-1 min-w-0">
                    <p class="text-sm font-bold text-on-surface nqt-notif-item-title">${n.title}</p>
                    <p class="text-xs text-on-surface-variant mt-0.5 nqt-notif-item-sub">${n.sub}</p>
                </div>
            </button>
        `).join('');
    }
    window.nqtDocTatCaThongBao = function() {
        document.getElementById('nqtNotifBadge').classList.add('hidden');
        document.getElementById('nqtNotifList').innerHTML = `<div class="px-5 py-8 text-center text-sm text-on-surface-variant"><i class="fas fa-check-circle text-on-surface-variant opacity-50 text-2xl mb-3 block"></i>Không có thông báo mới</div>`;
    };
    setInterval(() => {
        if (!document.hidden) {
            nqtApi.fetch('/api/nqt-thanh-toan?g6_trang_thai=cho_xu_ly&g6_gioi_han=1').then(res => {
                if (!res?.nqt_thanh_cong) return;
                const count = res.nqt_du_lieu.g6_tong || 0;
                const badge = document.getElementById('nqtNotifBadge');
                if (badge) { if (count > 0) { badge.textContent = count > 9 ? '9+' : count; badge.classList.remove('hidden'); } else badge.classList.add('hidden'); }
            }).catch(() => {});
        }
    }, 60000);

    // Command palette
    const rawTrangLenh = [
        { label:'Tổng quan', sub:'Dashboard', icon:'fa-chart-line', url:'/admin/dashboard', perms: ['XEM_BAO_CAO', 'G6PT', 'G6QuanLy'] },
        { label:'Hội viên', sub:'Quản lý', icon:'fa-users', url:'/admin/hoi-vien', perms: ['QL_HOI_VIEN', 'G6PT', 'G6QuanLy'] },
        { label:'Khách hàng', sub:'Quản lý', icon:'fa-user-tag', url:'/admin/khach-hang', perms: ['QL_HOI_VIEN', 'G6QuanLy'] },
        { label:'Gói tập', sub:'Quản lý', icon:'fa-box', url:'/admin/goi-tap', perms: ['QL_HOI_VIEN', 'G6QuanLy'] },
        { label:'Đơn hàng', sub:'Kinh doanh', icon:'fa-shopping-bag', url:'/admin/don-hang', perms: ['QL_KHO', 'G6QuanLy'] },
        { label:'Thanh toán', sub:'Kinh doanh', icon:'fa-credit-card', url:'/admin/thanh-toan', perms: ['QL_KHO', 'G6QuanLy'] },
        { label:'Chi nhánh', sub:'Vận hành', icon:'fa-store', url:'/admin/chi-nhanh', perms: ['QL_HE_THONG', 'G6QuanLy'] },
        { label:'Nhân viên', sub:'Vận hành', icon:'fa-id-badge', url:'/admin/nhan-vien', perms: ['QL_NHAN_VIEN', 'G6QuanLy'] },
        { label:'Cấu hình', sub:'Hệ thống', icon:'fa-cog', url:'/admin/cau-hinh', perms: ['G6QuanTri'] },
        { label:'Phân quyền', sub:'Hệ thống', icon:'fa-user-shield', url:'/admin/phan-quyen', perms: ['G6QuanTri'] },
        { label:'Đăng xuất', sub:'Tài khoản', icon:'fa-sign-out-alt', action:'nqtLogout()' },
    ];

    const nqtTrangLenh = rawTrangLenh.filter(item => {
        if (isAdmin) return true;
        if (!item.perms) return true;
        return item.perms.some(p => userPerms.includes(p) || userRoles.includes(p));
    });
    let nqtCmdActive = 0, nqtCmdFiltered = [...nqtTrangLenh];
    window.nqtAbrirComandos = function() {
        nqtCmdFiltered = [...nqtTrangLenh]; nqtCmdActive = 0;
        document.getElementById('nqtCmdOverlay').classList.remove('hidden');
        const inp = document.getElementById('nqtCmdInput'); inp.value = ''; nqtRenderCmdResults();
        setTimeout(() => inp.focus(), 50);
    };
    window.nqtInchideComenzi = function() { document.getElementById('nqtCmdOverlay').classList.add('hidden'); };
    window.nqtLocLenh = function(query) {
        const q = query.toLowerCase().trim();
        nqtCmdFiltered = q ? nqtTrangLenh.filter(t => t.label.toLowerCase().includes(q)||t.sub.toLowerCase().includes(q)) : [...nqtTrangLenh];
        nqtCmdActive = 0; nqtRenderCmdResults();
    };
    function nqtRenderCmdResults() {
        const el = document.getElementById('nqtCmdResults');
        if (nqtCmdFiltered.length === 0) { el.innerHTML = `<div class="px-5 py-8 text-center text-sm text-on-surface-variant font-medium">Không tìm thấy kết quả</div>`; return; }
        el.innerHTML = nqtCmdFiltered.map((t,i) => `
            <button class="nqt-cmd-item w-full flex items-center space-x-4 px-5 py-3 transition-colors hover:bg-surface-bright ${i===nqtCmdActive?'bg-surface-bright border-l-2 border-primary':'border-l-2 border-transparent'}" onclick="nqtCmdSelect(${i})">
                <div class="w-8 h-8 rounded-lg bg-surface-container-high border border-outline-variant flex items-center justify-center flex-shrink-0">
                    <i class="fas ${t.icon} text-sm text-on-surface-variant"></i>
                </div>
                <div class="flex-1 text-left"><p class="text-sm font-bold text-on-surface">${t.label}</p></div>
                <span class="text-xs text-outline font-medium">${t.sub}</span>
            </button>`).join('');
    }
    window.nqtCmdKeyDown = function(e) {
        if (e.key==='ArrowDown'){e.preventDefault();nqtCmdActive=Math.min(nqtCmdActive+1,nqtCmdFiltered.length-1);nqtRenderCmdResults();}
        else if(e.key==='ArrowUp'){e.preventDefault();nqtCmdActive=Math.max(nqtCmdActive-1,0);nqtRenderCmdResults();}
        else if(e.key==='Enter'){e.preventDefault();nqtCmdSelect(nqtCmdActive);}
        else if(e.key==='Escape'){nqtInchideComenzi();}
    };
    window.nqtCmdSelect = function(i) {
        const t = nqtCmdFiltered[i]; if(!t) return;
        nqtInchideComenzi();
        if(t.action) eval(t.action); else window.location.href = t.url;
    };
    document.addEventListener('keydown', e => {
        if((e.ctrlKey||e.metaKey)&&e.key==='k'){e.preventDefault();const o=document.getElementById('nqtCmdOverlay');o.classList.contains('hidden')?nqtAbrirComandos():nqtInchideComenzi();}
        if(e.key==='Escape'){
            if(!document.getElementById('nqtCmdOverlay').classList.contains('hidden')){nqtInchideComenzi();return;}
            if(nqtNotifOpen){nqtDongNotif();return;}
        }
    });

    // Load user info from JWT
    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        const hoTen = payload.g6_ho_ten || 'User';
        const nameEl = document.getElementById('nqt-user-name');
        const roleEl = document.getElementById('nqt-user-role');
        const avatarEl = document.getElementById('nqt-user-avatar');
        if(nameEl) nameEl.textContent = hoTen;
        const roleMap = {
            'G6QuanTri': 'Quản trị viên',
            'G6QuanLy': 'Quản lý',
            'G6PT': 'Huấn luyện viên',
            'G6HuanLuyenVien': 'Huấn luyện viên',
            'G6NhanVien': 'Nhân viên',
            'G6LeTan': 'Lễ tân'
        };
        if(roleEl) roleEl.textContent = roleMap[payload.g6_vai_tro?.[0]] || 'Thành viên';
        if(avatarEl) avatarEl.innerHTML = nqtTaoAvatar(hoTen, 32);
    } catch(e) {}


    // Load notifications badge
    setTimeout(() => { if(localStorage.getItem('nqt_admin_token')) nqtTaiThongBao(); }, 1500);


    // Toast System
    window.nqtShowToast = function(message, type = 'success') {
        const container = document.getElementById('nqt-toast-container') || nqtCreateToastContainer();
        const toast = document.createElement('div');
        
        // Style based on type
        const typeConfig = {
            success: { icon: 'fa-check-circle', color: '#C5A059', bg: 'rgba(197, 160, 89,0.1)' },
            error: { icon: 'fa-exclamation-circle', color: '#ef4444', bg: 'rgba(239,68,68,0.1)' },
            info: { icon: 'fa-info-circle', color: '#3b82f6', bg: 'rgba(59,130,246,0.1)' }
        };
        const config = typeConfig[type] || typeConfig.success;

        toast.className = 'nqt-toast-item nqt-toast-enter';
        toast.innerHTML = `
            <div class="flex items-center space-x-3 px-5 py-4 bg-[#141720]/90 backdrop-blur-xl border border-white/5 rounded-2xl shadow-[0_8px_32px_rgba(0,0,0,0.5)] min-w-[300px]">
                <div class="w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0" style="background: ${config.bg}; color: ${config.color}">
                    <i class="fas ${config.icon} text-sm"></i>
                </div>
                <div class="flex-1">
                    <p class="text-sm font-bold text-[#F5F5F0]">${message}</p>
                </div>
                <button onclick="this.parentElement.parentElement.remove()" class="text-white/20 hover:text-white/50 transition-colors">
                    <i class="fas fa-times text-xs"></i>
                </button>
            </div>
            <div class="nqt-toast-progress" style="background: ${config.color}"></div>
        `;

        container.appendChild(toast);

        // Auto remove
        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(20px)';
            setTimeout(() => toast.remove(), 300);
        }, 4000);
    };

    function nqtCreateToastContainer() {
        const container = document.createElement('div');
        container.id = 'nqt-toast-container';
        container.style.cssText = 'position: fixed; top: 24px; right: 24px; z-index: 9999; display: flex; flex-direction: column; gap: 12px; pointer-events: none;';
        document.body.appendChild(container);
        
        // Add required CSS
        const style = document.createElement('style');
        style.textContent = `
            .nqt-toast-item { 
                pointer-events: auto; 
                position: relative; 
                overflow: hidden; 
                border-radius: 16px;
                transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
            }
            .nqt-toast-enter { animation: nqtToastSlideIn 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) forwards; }
            @keyframes nqtToastSlideIn {
                from { opacity: 0; transform: translateX(30px) scale(0.9); }
                to { opacity: 1; transform: translateX(0) scale(1); }
            }
            .nqt-toast-progress {
                position: absolute;
                bottom: 0; left: 0; height: 2px;
                width: 100%;
                animation: nqtToastProgress 4s linear forwards;
            }
            @keyframes nqtToastProgress {
                from { width: 100%; }
                to { width: 0%; }
            }
        `;
        document.head.appendChild(style);
        return container;
    }

    // Export logut globally
    window.nqtLogout = function() {
        localStorage.removeItem('nqt_admin_token');
        nqtShowToast('Đang đăng xuất...', 'info');
        setTimeout(() => window.location.href = '/admin/login', 500);
    };
}
