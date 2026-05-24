const fs = require('fs');
const path = require('path');

console.log("==================================================");
console.log("          TYPEUI SKILL DEPLOYER - DASHBOARD        ");
console.log("==================================================");

const dashboardHtmlPath = path.resolve(__dirname, 'frontend/src/pages/admin/dashboard.html');
const neonHtmlPath = path.resolve(__dirname, 'dashboard_neon.html');
const layoutJsPath = path.resolve(__dirname, 'frontend/src/js/admin/nqtAdminLayout.js');

// 1. Copy dashboard
try {
    const dashboardHtml = fs.readFileSync(neonHtmlPath, 'utf8');
    fs.writeFileSync(dashboardHtmlPath, dashboardHtml, 'utf8');
    console.log("[OK] dashboard.html modern dark template injected successfully.");
} catch (e) {
    console.error("Failed to copy dashboard HTML:", e);
}

// 2. Read & process layout JS
try {
    let layoutContent = fs.readFileSync(layoutJsPath, 'utf8');

    // Remove the hardcoded dark body background style so it follows the CSS variables (var(--nqt-bg))
    layoutContent = layoutContent.replace(/background:\s*#0A0A0A\s*!important;\s*color:\s*#F5F5F0\s*!important;/g, '');

    // Make tables theme-aware
    const newTableStyles = `        table thead th {
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
        }`;

    layoutContent = layoutContent.replace(/table\s+thead\s+th\s*\{[^}]*background:\s*#121212[^}]*\}\s*table\s+tbody\s+td\s*\{[^}]*color:\s*#F5F5F0[^}]*\}\s*table\s+tbody\s+tr:hover\s*\{[^}]*\}/g, newTableStyles);

    // Make sidebar item text theme-aware
    layoutContent = layoutContent
        .replace(/color:\s*rgba\(255,\s*255,\s*255,\s*0\.6\)\s*!important;\s*\/\*\s*Force\s*light\s*text\s*on\s*dark\s*sidebar\s*\*\//g, 'color: var(--nqt-sidebar-text) !important;')
        .replace(/color:\s*rgba\(255,\s*255,\s*255,\s*0\.7\)\s*!important;/g, 'color: var(--nqt-sidebar-text) !important;');

    // Global gold to refined Champagne Gold replacements for classes, borders, states
    layoutContent = layoutContent
        .replace(/#C9A84C/g, '#C5A059')
        .replace(/#c9a84c/g, '#C5A059')
        .replace(/201,\s*168,\s*76/g, '197, 160, 89')
        .replace(/rgba\(201,\s*168,\s*76/g, 'rgba(197, 160, 89')
        .replace(/#E5C76B/g, '#D8BC7E') // Gold-bright to Pale Champagne
        .replace(/#1C1C1C/g, '#090b0e') // Sleeker, darker surface colors in dark mode
        .replace(/#121212/g, '#090b0e')
        .replace(/#0A0A0A/g, '#000000')
        .replace(/border-bottom:\s*1px\s*solid\s*rgba\(201,\s*168,\s*76,\s*0.15\)\s*!important;/g, 'border-bottom: 1px solid rgba(197, 160, 89, 0.15) !important;')
        .replace(/linear-gradient\(90deg,\s*transparent,\s*#C9A84C,\s*transparent\)/g, 'linear-gradient(90deg, transparent, #C5A059, transparent)')
        .replace(/linear-gradient\(90deg,\s*transparent\s*0%,\s*#C9A84C\s*50%,\s*transparent\s*100%\)/g, 'linear-gradient(90deg, transparent 0%, #C5A059 50%, transparent 100%)');

    const styleOverride = `
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
    `;

    // Only inject override if it wasn't injected yet
    if (!layoutContent.includes('Glassmorphism sidebar overrides')) {
        layoutContent = layoutContent.replace('/* ===== SIDEBAR — Industrial Solid ===== */', styleOverride + '\n/* ===== SIDEBAR — Industrial Solid ===== */');
    }

    fs.writeFileSync(layoutJsPath, layoutContent, 'utf8');
    console.log("[OK] nqtAdminLayout.js layout file modern color replacement complete.");
} catch (e) {
    console.error("Failed to process layout JS:", e);
}

console.log("==================================================");
console.log("             SKILL PULL COMPLETED SUCCESSFULLY    ");
console.log("==================================================");
