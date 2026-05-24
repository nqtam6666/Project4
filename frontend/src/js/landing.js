// IRONCORE Landing Page Logic
const API = '/api/nqt-public';

async function nqtFetch(path) {
    const res = await fetch(API + path);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
}

// ── Render Helpers ───────────────────────────────────────────────────────────
function formatCurrency(val) {
    return Number(val || 0).toLocaleString('vi-VN');
}

// ── Stats Section ────────────────────────────────────────────────────────────
async function loadStats() {
    try {
        const res = await nqtFetch('/stats');
        if (res.nqt_thanh_cong) {
            const data = res.nqt_du_lieu;
            animateValue('stat-members', 0, data.total_members, 2000);
            animateValue('stat-trainers', 0, data.total_trainers, 2000);
            animateValue('stat-rating', 0, data.avg_rating, 2000, 1);
        }
    } catch (e) { console.error('Stats error:', e); }
}

function animateValue(id, start, end, duration, decimals = 0) {
    const obj = document.getElementById(id);
    if (!obj) return;
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        const val = progress * (end - start) + start;
        obj.innerHTML = decimals > 0 ? val.toFixed(decimals) : Math.floor(val);
        if (progress < 1) {
            window.requestAnimationFrame(step);
        } else {
            obj.innerHTML = decimals > 0 ? end.toFixed(decimals) : end;
        }
    };
    window.requestAnimationFrame(step);
}

// ── Services Section ─────────────────────────────────────────────────────────
async function loadServicesAndClasses() {
    try {
        const [servicesRes, classesRes] = await Promise.all([
            nqtFetch('/services'),
            nqtFetch('/classes')
        ]);

        const container = document.getElementById('servicesGrid');
        let html = '';

        if (servicesRes.nqt_thanh_cong) {
            servicesRes.nqt_du_lieu.slice(0, 3).forEach(s => {
                html += `
                <div class="service-card reveal h-[400px] relative overflow-hidden group border border-white/5 rounded-xl">
                    <img src="${s.g6_hinh_anh || 'https://images.unsplash.com/photo-1540497077202-7c8a3999166f?q=80&w=2070&auto=format&fit=crop'}" alt="${s.g6_ten_dich_vu}" class="w-full h-full object-cover grayscale brightness-50 group-hover:grayscale-0 group-hover:brightness-75 transition-all duration-700 group-hover:scale-110">
                    <div class="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent"></div>
                    <div class="absolute bottom-0 left-0 p-8">
                        <h3 class="text-3xl text-gold mb-2">${s.g6_ten_dich_vu}</h3>
                        <p class="text-muted line-clamp-2">${s.g6_mo_ta || ''}</p>
                    </div>
                </div>`;
            });
        }

        if (classesRes.nqt_thanh_cong) {
            classesRes.nqt_du_lieu.slice(0, 3).forEach(c => {
                html += `
                <div class="service-card reveal h-[400px] relative overflow-hidden group border border-white/5 rounded-xl">
                    <img src="${c.g6_hinh_anh || 'https://images.unsplash.com/photo-1518611012118-2960c8bad84a?q=80&w=2070&auto=format&fit=crop'}" alt="${c.g6_ten_lop}" class="w-full h-full object-cover grayscale brightness-50 group-hover:grayscale-0 group-hover:brightness-75 transition-all duration-700 group-hover:scale-110">
                    <div class="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent"></div>
                    <div class="absolute bottom-0 left-0 p-8">
                        <h3 class="text-3xl text-gold mb-2">${c.g6_ten_lop}</h3>
                        <p class="text-muted line-clamp-2">${c.g6_mo_ta || ''}</p>
                    </div>
                </div>`;
            });
        }

        if (html) {
            container.innerHTML = html;
            // Re-trigger reveal observer
            document.querySelectorAll('#servicesGrid .reveal').forEach(el => revealObserver.observe(el));
        }
    } catch (e) { console.error('Services error:', e); }
}

// ── Pricing Section ──────────────────────────────────────────────────────────
async function loadPricing() {
    try {
        const res = await nqtFetch('/goi-tap');
        if (res.nqt_thanh_cong) {
            const container = document.getElementById('goiTapList');
            container.innerHTML = res.nqt_du_lieu.map(goi => {
                const isNoBat = goi.g6_la_noi_bat;
                return `
                <div class="pricing-card ${isNoBat ? 'featured' : ''} reveal bg-surface p-12 border border-white/5 text-center relative transition-all duration-500 hover:-translate-y-2">
                    <h3 class="text-4xl mb-5">${goi.g6_ten_goi}</h3>
                    <div class="text-[3.5rem] font-header text-gold mb-8">${formatCurrency(goi.g6_gia)}<span class="text-base text-muted normal-case">/${goi.g6_so_ngay} ngày</span></div>
                    <ul class="list-none text-left mb-10 space-y-4">
                        <li class="flex items-center gap-4 text-lg"><i class="fas fa-check text-gold"></i> Tập luyện không giới hạn</li>
                        <li class="flex items-center gap-4 text-lg ${goi.g6_co_sauna ? '' : 'opacity-30'}"><i class="fas ${goi.g6_co_sauna ? 'fa-check' : 'fa-times'} text-gold"></i> Dịch vụ Sauna & Pool</li>
                        <li class="flex items-center gap-4 text-lg ${goi.g6_co_pt ? '' : 'opacity-30'}"><i class="fas ${goi.g6_co_pt ? 'fa-check' : 'fa-times'} text-gold"></i> ${goi.g6_so_buoi_pt || 0} buổi PT cá nhân</li>
                    </ul>
                    <a href="/login" class="cta-btn w-full">ĐĂNG KÝ NGAY</a>
                </div>`;
            }).join('');
            document.querySelectorAll('#goiTapList .reveal').forEach(el => revealObserver.observe(el));
        }
    } catch (e) { console.error('Pricing error:', e); }
}

// ── Trainers Section ─────────────────────────────────────────────────────────
async function loadTrainers() {
    try {
        const res = await nqtFetch('/huan-luyen-vien');
        if (res.nqt_thanh_cong) {
            const container = document.getElementById('hlvList');
            container.innerHTML = res.nqt_du_lieu.map(hlv => {
                return `
                <div class="min-w-[320px] bg-surface border border-white/5 rounded-xl overflow-hidden group">
                    <div class="h-[400px] overflow-hidden relative">
                        <img src="${hlv.g6_anh_dai_dien || 'https://images.unsplash.com/photo-1594381898411-846e7d193883?w=500&auto=format&fit=crop&q=60'}" class="w-full h-full object-cover grayscale group-hover:grayscale-0 transition-all duration-700 scale-105 group-hover:scale-110">
                        <div class="absolute top-4 right-4 bg-black/80 px-3 py-1 rounded-full text-gold font-bold text-sm">★ ${hlv.g6_thu_hang || 5.0}</div>
                    </div>
                    <div class="p-8">
                        <h3 class="text-2xl mb-2">${hlv.g6_ho_ten}</h3>
                        <p class="text-gold font-header tracking-wider uppercase text-sm mb-4">${Array.isArray(hlv.g6_chuyen_mon) ? hlv.g6_chuyen_mon.join(' · ') : (hlv.g6_chuyen_mon || 'Expert')}</p>
                        <p class="text-muted text-sm italic">"Sẵn sàng đồng hành cùng bạn trên hành trình kiến tạo di sản."</p>
                    </div>
                </div>`;
            }).join('');
            initDragScroll();
        }
    } catch (e) { console.error('Trainers error:', e); }
}

function initDragScroll() {
    const slider = document.getElementById('hlvList');
    let isDown = false;
    let startX;
    let scrollLeft;

    slider.addEventListener('mousedown', (e) => {
        isDown = true;
        slider.classList.add('active');
        startX = e.pageX - slider.offsetLeft;
        scrollLeft = slider.scrollLeft;
    });
    slider.addEventListener('mouseleave', () => {
        isDown = false;
        slider.classList.remove('active');
    });
    slider.addEventListener('mouseup', () => {
        isDown = false;
        slider.classList.remove('active');
    });
    slider.addEventListener('mousemove', (e) => {
        if (!isDown) return;
        e.preventDefault();
        const x = e.pageX - slider.offsetLeft;
        const walk = (x - startX) * 2;
        slider.scrollLeft = scrollLeft - walk;
    });
}

// ── Testimonials Section ─────────────────────────────────────────────────────
async function loadTestimonials() {
    try {
        const res = await nqtFetch('/testimonials');
        if (res.nqt_thanh_cong) {
            const container = document.getElementById('testimonialsList');
            if (res.nqt_du_lieu.length === 0) return;
            
            container.innerHTML = res.nqt_du_lieu.map((t, idx) => `
                <div class="testimonial-item ${idx === 0 ? 'active' : ''}">
                    <div class="text-gold text-2xl mb-6">
                        ${'<i class="fas fa-star mx-1"></i>'.repeat(t.nxv_sao)}
                    </div>
                    <p class="text-3xl italic text-main mb-8 leading-relaxed">"${t.nxv_noi_dung}"</p>
                    <h4 class="text-2xl font-header tracking-widest text-gold">— Hội viên ẩn danh</h4>
                </div>
            `).join('');
            
            startTestimonialCycle();
        }
    } catch (e) { console.error('Testimonials error:', e); }
}

function startTestimonialCycle() {
    let current = 0;
    const items = document.querySelectorAll('.testimonial-item');
    if (items.length <= 1) return;
    
    setInterval(() => {
        items[current].classList.remove('active');
        current = (current + 1) % items.length;
        items[current].classList.add('active');
    }, 5000);
}

// ── Config & Branches ────────────────────────────────────────────────────────
async function loadConfig() {
    try {
        const res = await nqtFetch('/cau-hinh-ui');
        if (res.nqt_thanh_cong) {
            let tenWebsite = '';
            let faviconUrl = '';
            let logoUrl = '';
            res.nqt_du_lieu.forEach(c => {
                const els = document.querySelectorAll(`[data-config="${c.g6_khoa.replace('g6_', '')}"]`);
                els.forEach(el => {
                    if (el.tagName === 'IMG') el.src = c.g6_gia_tri;
                    else el.textContent = c.g6_gia_tri;
                });
                if (c.g6_khoa === 'g6_ten_website') tenWebsite = c.g6_gia_tri;
                if (c.g6_khoa === 'g6_favicon_url') faviconUrl = c.g6_gia_tri;
                if (c.g6_logo_url) logoUrl = c.g6_gia_tri;
            });

            if (tenWebsite) {
                document.title = `${tenWebsite} | Hệ thống phòng tập cao cấp`;
                
                // Replace hardcoded footer
                const footerText = document.querySelector('footer p');
                if (footerText && footerText.textContent.includes('IRONCORE')) {
                    footerText.textContent = `© 2024 ${tenWebsite.toUpperCase()}. BẢO LƯU MỌI QUYỀN.`;
                }
            }

            if (logoUrl) {
                const brandLink = document.querySelector('[data-config="ten_website"]');
                if (brandLink) {
                    brandLink.innerHTML = `<img src="${logoUrl}" alt="${tenWebsite || 'Logo'}" class="h-10 w-auto object-contain">`;
                }
            }

            if (faviconUrl) {
                let link = document.querySelector("link[rel~='icon']");
                if (!link) {
                    link = document.createElement('link');
                    link.rel = 'icon';
                    document.head.appendChild(link);
                }
                link.href = faviconUrl;
            }
        }
    } catch (e) { console.error('Config error:', e); }
}

async function loadBranches() {
    try {
        const res = await nqtFetch('/branches');
        if (res.nqt_thanh_cong) {
            const container = document.getElementById('branchesList');
            container.innerHTML = res.nqt_du_lieu.map(b => `
                <li><i class="fas fa-map-marker-alt mr-3 text-gold"></i> ${b.g6_ten_chi_nhanh} - ${b.g6_dia_chi}</li>
            `).join('');
        }
    } catch (e) { console.error('Branches error:', e); }
}

// ── Init All ─────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    loadConfig();
    loadStats();
    loadServicesAndClasses();
    loadPricing();
    loadTrainers();
    loadTestimonials();
    loadBranches();
});
