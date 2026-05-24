import React, { useState, useEffect, useRef } from 'react';
import { Camera, LogOut, UserCircle2, ArrowLeft, CheckCircle2, ShieldCheck } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const PtDashboard = () => {
  const [loading, setLoading] = useState(true);
  const [profile, setProfile] = useState(null);
  const [error, setError] = useState('');
  const [uploading, setUploading] = useState(false);
  const [notification, setNotification] = useState(null);
  const fileInputRef = useRef(null);

  const token = localStorage.getItem('nqt_admin_token');

  const [siteConfig, setSiteConfig] = useState({
    g6_ten_website: "G6 GYM",
    g6_logo_url: "",
    g6_favicon_url: ""
  });

  useEffect(() => {
    if (!token) {
      window.location.href = '/admin/login';
      return;
    }
    fetchProfile();

    const loadSiteConfig = async () => {
      try {
        const res = await fetch("/api/nqt-public/cau-hinh-ui");
        const data = await res.json();
        if (data && data.nqt_thanh_cong) {
          const config = {};
          data.nqt_du_lieu.forEach(row => {
            config[row.g6_khoa] = row.g6_gia_tri;
          });
          setSiteConfig(prev => ({ ...prev, ...config }));
          if (config.g6_ten_website) {
            document.title = `${config.g6_ten_website} | Trainer Portal`;
          }
          if (config.g6_favicon_url) {
            let link = document.querySelector("link[rel~='icon']");
            if (!link) {
              link = document.createElement('link');
              link.rel = 'icon';
              document.head.appendChild(link);
            }
            link.href = config.g6_favicon_url;
          }
        }
      } catch (e) {
        console.error("Config fetch error:", e);
      }
    };
    loadSiteConfig();
  }, []);

  const fetchProfile = async () => {
    try {
      const res = await fetch('/api/nxv-hlv/me', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      const data = await res.json();
      if (res.ok && data.nqt_thanh_cong) {
        setProfile(data.nqt_du_lieu);
      } else {
        setError(data.nqt_thong_diep || 'Không thể lấy thông tin. Bạn có phải là PT?');
      }
    } catch (err) {
      setError('Lỗi kết nối máy chủ');
    } finally {
      setLoading(false);
    }
  };

  const showToast = (type, message) => {
    setNotification({ type, message });
    setTimeout(() => setNotification(null), 3000);
  };

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    // 1. Upload file
    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const upRes = await fetch('/api/nqt-upload', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` },
        body: formData
      });
      const upData = await upRes.json();
      if (!upRes.ok || !upData.nqt_thanh_cong) {
        showToast('error', upData.nqt_thong_diep || 'Lỗi upload ảnh');
        setUploading(false);
        return;
      }
      
      const imgUrl = upData.nqt_du_lieu.g6_url;

      // 2. Cập nhật avatar
      const updateRes = await fetch('/api/nxv-hlv/me/avatar', {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ g6_hinh_anh: imgUrl })
      });
      const updateData = await updateRes.json();
      
      if (updateRes.ok && updateData.nqt_thanh_cong) {
        setProfile(prev => ({ ...prev, g6_hinh_anh: imgUrl }));
        showToast('success', 'Cập nhật ảnh đại diện thành công!');
      } else {
        showToast('error', updateData.nqt_thong_diep || 'Lỗi cập nhật');
      }
    } catch (err) {
      showToast('error', 'Có lỗi xảy ra');
    } finally {
      setUploading(false);
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('nqt_admin_token');
    window.location.href = '/admin/login';
  };

  if (loading) return <div className="min-h-screen bg-[#0A0A0A] flex items-center justify-center text-[#F5F5F0] font-['Barlow_Condensed'] text-2xl tracking-widest uppercase font-black">Loading...</div>;

  if (error) return (
    <div className="min-h-screen bg-[#0A0A0A] flex flex-col items-center justify-center text-[#F5F5F0] font-sans p-4">
      <div className="bg-[#1C1C1C] p-8 rounded-3xl border border-red-500/30 max-w-md w-full text-center">
        <div className="w-16 h-16 rounded-full bg-red-500/10 text-red-500 flex items-center justify-center mx-auto mb-4">
          <ShieldCheck size={32} />
        </div>
        <h2 className="text-xl font-bold mb-2">Truy Cập Từ Chối</h2>
        <p className="text-[#A1A1AA] mb-8">{error}</p>
        <button onClick={handleLogout} className="px-6 py-3 bg-white/5 hover:bg-white/10 rounded-xl transition-all font-bold w-full">
          Quay lại đăng nhập
        </button>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-[#0A0A0A] text-[#F5F5F0] font-sans overflow-x-hidden">
      {/* Toast Notifications */}
      <AnimatePresence>
        {notification && (
          <motion.div 
            initial={{ opacity: 0, y: -50, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9, transition: { duration: 0.2 } }}
            className="fixed top-10 z-[100] flex items-center justify-center w-full px-4 pointer-events-none"
          >
            <div className={`pointer-events-auto px-8 py-4 bg-[#1C1C1C] border ${notification.type === 'success' ? 'border-[#C9A84C]' : 'border-red-500'} shadow-[0_20px_50px_rgba(0,0,0,0.5)] flex items-center space-x-4 rounded-xl`}>
              <div className={`w-10 h-10 rounded-full flex items-center justify-center ${notification.type === 'success' ? 'bg-[#C9A84C]/10 text-[#C9A84C]' : 'bg-red-500/10 text-red-500'}`}>
                {notification.type === 'success' ? <CheckCircle2 size={20} /> : <UserCircle2 size={20} />}
              </div>
              <div>
                <p className="font-bold tracking-widest text-lg leading-none uppercase text-[#F5F5F0] font-['Barlow_Condensed']">
                  {notification.type === 'success' ? 'Thành công' : 'Lỗi'}
                </p>
                <p className="text-sm text-[#A1A1AA] mt-1">{notification.message}</p>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Header */}
      <header className="fixed top-0 w-full z-50 bg-[#0A0A0A]/80 backdrop-blur-xl border-b border-white/5">
        <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <a href="/admin" className="w-10 h-10 rounded-full bg-white/5 hover:bg-white/10 flex items-center justify-center transition-all text-[#C9A84C]">
              <ArrowLeft size={18} />
            </a>
            {siteConfig.g6_logo_url ? (
              <img src={siteConfig.g6_logo_url} className="max-h-12 object-contain" alt="Logo" />
            ) : (
              <h1 className="text-2xl font-black tracking-[4px] text-[#C9A84C] font-['Cormorant_Garamond'] uppercase">
                {siteConfig.g6_ten_website.toUpperCase()} PT
              </h1>
            )}
          </div>
          <button onClick={handleLogout} className="flex items-center space-x-2 px-4 py-2 bg-red-500/10 hover:bg-red-500/20 text-red-500 rounded-xl transition-all text-sm font-bold">
            <LogOut size={16} /> <span className="hidden sm:inline">Đăng xuất</span>
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="pt-32 pb-20 px-4">
        <div className="max-w-3xl mx-auto">
          
          <div className="bg-[#1C1C1C] border border-white/5 rounded-3xl p-8 relative overflow-hidden shadow-[0_30px_60px_rgba(0,0,0,0.5)]">
            <div className="absolute top-0 left-0 w-full h-32 bg-gradient-to-r from-[#C9A84C]/20 to-transparent opacity-30 pointer-events-none"></div>
            
            <div className="flex flex-col md:flex-row items-center md:items-start space-y-8 md:space-y-0 md:space-x-12 relative z-10">
              
              {/* Avatar Section */}
              <div className="flex flex-col items-center group relative">
                <div className="relative w-40 h-40 rounded-full p-1 bg-gradient-to-b from-[#C9A84C] to-[#C9A84C]/10 mb-4">
                  <div className="w-full h-full rounded-full bg-[#0A0A0A] overflow-hidden relative">
                    <img 
                      src={profile.g6_hinh_anh || "https://ui-avatars.com/api/?name="+encodeURIComponent(profile.g6_ho_ten)+"&background=1C1C1C&color=C9A84C"} 
                      className={`w-full h-full object-cover transition-opacity duration-300 ${uploading ? 'opacity-50' : 'opacity-100 group-hover:opacity-60'}`}
                      alt={profile.g6_ho_ten}
                    />
                    <div className="absolute inset-0 flex flex-col items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300 bg-black/40 cursor-pointer" onClick={() => fileInputRef.current.click()}>
                      {uploading ? (
                        <div className="w-8 h-8 border-2 border-t-[#C9A84C] border-r-[#C9A84C] border-b-transparent border-l-transparent rounded-full animate-spin"></div>
                      ) : (
                        <>
                          <Camera className="text-[#F5F5F0] mb-2" size={24} />
                          <span className="text-xs font-bold text-[#F5F5F0] tracking-widest uppercase">Thay đổi</span>
                        </>
                      )}
                    </div>
                  </div>
                </div>
                <input 
                  type="file" 
                  ref={fileInputRef} 
                  onChange={handleFileChange} 
                  accept="image/*" 
                  className="hidden" 
                />
                <span className="px-3 py-1 bg-[#C9A84C]/10 text-[#C9A84C] text-[10px] uppercase tracking-widest font-bold rounded-full border border-[#C9A84C]/30">
                  {profile.g6_thu_hang} Sao
                </span>
              </div>

              {/* Info Section */}
              <div className="flex-1 text-center md:text-left">
                <h2 className="text-4xl font-black text-[#F5F5F0] mb-2 font-['Barlow_Condensed'] uppercase tracking-wide">
                  {profile.g6_ho_ten}
                </h2>
                <p className="text-[#C9A84C] font-bold tracking-widest uppercase text-sm mb-6">
                  {profile.g6_chuyen_mon || 'Personal Trainer'}
                </p>

                <div className="grid grid-cols-2 gap-4 mb-8">
                  <div className="bg-white/5 p-4 rounded-2xl border border-white/5 hover:border-white/10 transition-colors">
                    <p className="text-[10px] text-[#A1A1AA] uppercase font-bold tracking-widest mb-1">Kinh nghiệm</p>
                    <p className="font-bold text-lg">{profile.g6_so_nam_kinh_nghiem} năm</p>
                  </div>
                  <div className="bg-white/5 p-4 rounded-2xl border border-white/5 hover:border-white/10 transition-colors">
                    <p className="text-[10px] text-[#A1A1AA] uppercase font-bold tracking-widest mb-1">Học viên tối đa</p>
                    <p className="font-bold text-lg">{profile.g6_so_hoi_vien_hien_tai} / {profile.g6_toi_da_hoi_vien}</p>
                  </div>
                  <div className="bg-white/5 p-4 rounded-2xl border border-white/5 hover:border-white/10 transition-colors">
                    <p className="text-[10px] text-[#A1A1AA] uppercase font-bold tracking-widest mb-1">Bằng cấp</p>
                    <p className="font-bold text-lg">{profile.g6_cap_chung_chi || `${siteConfig.g6_ten_website || 'G6 GYM'} Cert`}</p>
                  </div>
                  <div className="bg-white/5 p-4 rounded-2xl border border-white/5 hover:border-white/10 transition-colors">
                    <p className="text-[10px] text-[#A1A1AA] uppercase font-bold tracking-widest mb-1">Mức phí</p>
                    <p className="font-bold text-lg text-[#C9A84C]">{profile.g6_gia_theo_buoi ? profile.g6_gia_theo_buoi.toLocaleString() : 'Liên hệ'}đ / buổi</p>
                  </div>
                </div>

                <div>
                  <h3 className="text-sm text-[#A1A1AA] uppercase font-bold tracking-widest mb-3 border-b border-white/5 pb-2">Tiểu sử</h3>
                  <p className="text-sm text-[#F5F5F0]/80 leading-relaxed bg-white/5 p-4 rounded-2xl">
                    {profile.g6_tieu_su || 'Chưa cập nhật tiểu sử. Vui lòng liên hệ quản trị viên để cập nhật nội dung này.'}
                  </p>
                </div>

              </div>
            </div>
          </div>
          
        </div>
      </main>
    </div>
  );
};

export default PtDashboard;
