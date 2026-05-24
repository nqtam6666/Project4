import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

/**
 * IRONCORE GYM - Login & Registration Page
 * Style: Dark Industrial-Luxury
 */

const AuthPage = () => {
  const [activeTab, setActiveTab] = useState('login');
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [notification, setNotification] = useState(null);
  const [isDarkMode, setIsDarkMode] = useState(() => {
    return localStorage.getItem("nqt_theme") !== "light";
  });

  // Sync dark mode class and storage
  React.useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add("dark");
      localStorage.setItem("nqt_theme", "dark");
      localStorage.setItem("nqt_dark_mode", "true");
    } else {
      document.documentElement.classList.remove("dark");
      localStorage.setItem("nqt_theme", "light");
      localStorage.setItem("nqt_dark_mode", "false");
    }
  }, [isDarkMode]);

  // Form states
  const [loginData, setLoginData] = useState({ phone: '0961111101', password: '0961111101' });
  const [regData, setRegData] = useState({ name: '', phone: '', email: '', password: '', confirmPassword: '' });

  const [siteConfig, setSiteConfig] = useState({
    g6_ten_website: "G6 GYM",
    g6_slogan: "Forge Your Legacy",
    g6_logo_url: "",
    g6_favicon_url: ""
  });

  React.useEffect(() => {
    const loadConfig = async () => {
      try {
        const res = await fetch('/api/nqt-public/cau-hinh-ui');
        const data = await res.json();
        if (data && data.nqt_thanh_cong) {
          const config = {};
          data.nqt_du_lieu.forEach(row => {
            config[row.g6_khoa] = row.g6_gia_tri;
          });
          setSiteConfig(prev => ({ ...prev, ...config }));
          if (config.g6_ten_website) {
            document.title = `${config.g6_ten_website} | Đăng nhập`;
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
    loadConfig();
  }, []);

  const showToast = (type, message) => {
    setNotification({ type, message });
    setTimeout(() => setNotification(null), 4000);
  };

  const handleAuth = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      if (activeTab === 'login') {
        const res = await fetch('/api/nqt-hoi-vien/dang-nhap', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include', // Cho phép nhận Cookie từ Server
          body: JSON.stringify({
            nqt_so_dien_thoai: loginData.phone,
            nqt_mat_khau: loginData.password
          })
        });
        const data = await res.json();
        setLoading(false);
        if (data.nqt_thanh_cong) {
          if (data.nqt_du_lieu && data.nqt_du_lieu.nqt_access_token) {
            localStorage.setItem('nqt_token', data.nqt_du_lieu.nqt_access_token);
            if (data.nqt_du_lieu.nqt_refresh_token) {
              localStorage.setItem('nqt_refresh_token', data.nqt_du_lieu.nqt_refresh_token);
            }
          }
          showToast('success', 'Đăng nhập thành công! Đang chuyển hướng...');
          setTimeout(() => window.location.href = '/home', 1000);
        } else {
          showToast('error', data.nqt_thong_diep || 'Đăng nhập thất bại');
        }
      } else {
        const res = await fetch('/api/nqt-hoi-vien/dang-ky', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
          body: JSON.stringify({
            nqt_ho_ten: regData.name,
            nqt_so_dien_thoai: regData.phone,
            nqt_email: regData.email,
            nqt_mat_khau: regData.password
          })
        });
        const data = await res.json();
        setLoading(false);
        if (data.nqt_thanh_cong) {
          if (data.nqt_du_lieu && data.nqt_du_lieu.nqt_access_token) {
            localStorage.setItem('nqt_token', data.nqt_du_lieu.nqt_access_token);
            if (data.nqt_du_lieu.nqt_refresh_token) {
              localStorage.setItem('nqt_refresh_token', data.nqt_du_lieu.nqt_refresh_token);
            }
          }
          showToast('success', 'Tạo tài khoản thành công! Hãy đăng nhập.');
          setActiveTab('login');
        } else {
          showToast('error', data.nqt_thong_diep || 'Đăng ký thất bại');
        }
      }
    } catch (error) {
      setLoading(false);
      showToast('error', 'Lỗi kết nối máy chủ');
    }
  };

  return (
    <div className="min-h-screen bg-[#FAFAFA] dark:bg-[#0A0A0A] text-[#0A0A0A] dark:text-[#F5F5F0] font-body flex items-center justify-center relative overflow-hidden transition-colors duration-300">
      
      {/* Floating Theme Switcher */}
      <button 
        type="button"
        onClick={() => setIsDarkMode(!isDarkMode)}
        className="fixed top-6 right-6 w-10 h-10 rounded-full bg-white dark:bg-[#1C1C1C] border border-gray-200 dark:border-white/10 flex items-center justify-center text-[#C9A84C] hover:text-[#E5C76B] transition-all shadow-md z-50 focus:outline-none"
        title={isDarkMode ? "Chuyển sang chế độ sáng" : "Chuyển sang chế độ tối"}
      >
        <i className={`fas ${isDarkMode ? 'fa-sun' : 'fa-moon'} text-lg`}></i>
      </button>

      {/* --- Notifications --- */}
      <AnimatePresence>
        {notification && (
          <motion.div 
            initial={{ opacity: 0, y: -50, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9, transition: { duration: 0.2 } }}
            className="fixed top-10 z-[100] flex items-center justify-center w-full px-4 pointer-events-none"
          >
            <div className={`pointer-events-auto px-8 py-4 bg-white dark:bg-[#1C1C1C] border ${notification.type === 'success' ? 'border-[#C9A84C]' : 'border-red-500'} shadow-[0_20px_50px_rgba(0,0,0,0.05)] dark:shadow-[0_20px_50px_rgba(0,0,0,0.5)] flex items-center space-x-4 rounded-xl`}>
              <div className={`w-10 h-10 rounded-full flex items-center justify-center ${notification.type === 'success' ? 'bg-[#C9A84C]/10 text-[#C9A84C]' : 'bg-red-500/10 text-red-500'}`}>
                <i className={`fas ${notification.type === 'success' ? 'fa-check' : 'fa-exclamation-circle'} text-xl`}></i>
              </div>
              <div>
                <p className="font-header tracking-widest text-lg leading-none uppercase">{notification.type === 'success' ? 'Thành công' : 'Lỗi'}</p>
                <p className="text-sm text-gray-500 dark:text-[#A1A1AA] mt-1">{notification.message}</p>
              </div>
              <button onClick={() => setNotification(null)} className="ml-4 text-gray-400 dark:text-[#52525B] hover:text-black dark:hover:text-[#F5F5F0]">
                <i className="fas fa-times"></i>
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* --- Background Decorative Elements --- */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-[#C9A84C] opacity-[0.03] dark:opacity-5 blur-[120px] rounded-full"></div>
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-[#C9A84C] opacity-[0.03] dark:opacity-5 blur-[120px] rounded-full"></div>
      
      <div className="container mx-auto px-4 z-10 flex flex-col items-center">
        
        {/* --- Logo --- */}
        <div className="mb-8 text-center">
          <a href="/home" className="block hover:opacity-85 transition-opacity">
            {siteConfig.g6_logo_url ? (
              <img src={siteConfig.g6_logo_url} className="mx-auto max-h-16 object-contain" alt="Logo" />
            ) : (
              <h1 className="font-header text-5xl tracking-[4px] text-[#C9A84C]">{(siteConfig.g6_ten_website || "G6 GYM").toUpperCase()}</h1>
            )}
          </a>
          <p className="uppercase tracking-[2px] text-xs text-gray-500 dark:text-[#A1A1AA] mt-2 font-header">{siteConfig.g6_slogan}</p>
        </div>

        {/* --- Auth Card --- */}
        <div className="w-full max-w-md bg-white dark:bg-[#1C1C1C] border border-gray-100 dark:border-white/5 rounded-2xl overflow-hidden shadow-[0_20px_50px_rgba(0,0,0,0.05)] dark:shadow-2xl relative transition-all duration-300">
          
          <div className="absolute top-0 left-0 w-full h-[2px] bg-gradient-to-r from-transparent via-[#C9A84C] to-transparent"></div>

          {/* Tabs */}
          <div className="flex border-b border-gray-100 dark:border-white/5">
            <button 
              onClick={() => setActiveTab('login')}
              className={`flex-1 py-5 font-header text-lg tracking-widest transition-all ${activeTab === 'login' ? 'text-[#C9A84C] bg-gray-50/50 dark:bg-white/[0.02]' : 'text-gray-400 dark:text-[#A1A1AA] hover:text-black dark:hover:text-[#F5F5F0]'}`}
            >
              ĐĂNG NHẬP
            </button>
            <button 
              onClick={() => setActiveTab('register')}
              className={`flex-1 py-5 font-header text-lg tracking-widest transition-all ${activeTab === 'register' ? 'text-[#C9A84C] bg-gray-50/50 dark:bg-white/[0.02]' : 'text-gray-400 dark:text-[#A1A1AA] hover:text-black dark:hover:text-[#F5F5F0]'}`}
            >
              ĐĂNG KÝ
            </button>
          </div>

          {/* Form Content */}
          <div className="p-8 md:p-10">
            <form onSubmit={handleAuth} className="space-y-6">
              
              {activeTab === 'register' && (
                <div className="space-y-1 group">
                  <label className="text-xs uppercase tracking-widest text-gray-400 dark:text-[#A1A1AA] font-header group-focus-within:text-[#C9A84C] transition-colors">Họ và tên</label>
                  <div className="relative flex items-center">
                    <span className="absolute left-0 text-gray-400 dark:text-[#A1A1AA] w-6 flex justify-center"><i className="far fa-user text-sm"></i></span>
                    <input 
                      type="text" 
                      placeholder="Nguyễn Văn A"
                      className="w-full bg-transparent border-b border-gray-200 dark:border-white/10 py-3 pl-8 outline-none focus:border-[#C9A84C] transition-all text-lg text-black dark:text-[#F5F5F0]"
                      value={regData.name}
                      onChange={(e) => setRegData({...regData, name: e.target.value})}
                      required
                    />
                  </div>
                </div>
              )}

              <div className="space-y-1 group">
                <label className="text-xs uppercase tracking-widest text-gray-400 dark:text-[#A1A1AA] font-header group-focus-within:text-[#C9A84C] transition-colors">
                  {activeTab === 'login' ? 'Số điện thoại' : 'Địa chỉ Email'}
                </label>
                <div className="relative flex items-center">
                  <span className="absolute left-0 text-gray-400 dark:text-[#A1A1AA] w-6 flex justify-center">
                    <i className={activeTab === 'login' ? "fas fa-phone-alt text-sm" : "far fa-envelope text-sm"}></i>
                  </span>
                  <input 
                    type={activeTab === 'login' ? "tel" : "email"}
                    placeholder={activeTab === 'login' ? "09xx xxx xxx" : "gym@g6gym.vn"}
                    className="w-full bg-transparent border-b border-gray-200 dark:border-white/10 py-3 pl-8 outline-none focus:border-[#C9A84C] transition-all text-lg text-black dark:text-[#F5F5F0]"
                    value={activeTab === 'login' ? loginData.phone : regData.email}
                    onChange={(e) => activeTab === 'login' ? setLoginData({...loginData, phone: e.target.value}) : setRegData({...regData, email: e.target.value})}
                    required
                  />
                </div>
              </div>

              {activeTab === 'register' && (
                <div className="space-y-1 group">
                  <label className="text-xs uppercase tracking-widest text-gray-400 dark:text-[#A1A1AA] font-header group-focus-within:text-[#C9A84C] transition-colors">Số điện thoại</label>
                  <div className="relative flex items-center">
                    <span className="absolute left-0 text-gray-400 dark:text-[#A1A1AA] w-6 flex justify-center"><i className="fas fa-phone-alt text-sm"></i></span>
                    <input 
                      type="tel" 
                      placeholder="09xx xxx xxx"
                      className="w-full bg-transparent border-b border-gray-200 dark:border-white/10 py-3 pl-8 outline-none focus:border-[#C9A84C] transition-all text-lg text-black dark:text-[#F5F5F0]"
                      value={regData.phone}
                      onChange={(e) => setRegData({...regData, phone: e.target.value})}
                      required
                    />
                  </div>
                </div>
              )}

              <div className="space-y-1 group">
                <div className="flex justify-between items-center">
                  <label className="text-xs uppercase tracking-widest text-gray-400 dark:text-[#A1A1AA] font-header group-focus-within:text-[#C9A84C] transition-colors">Mật khẩu</label>
                  {activeTab === 'login' && (
                    <a href="#" className="text-[10px] uppercase tracking-widest text-[#C9A84C] hover:text-[#E5C76B] transition-colors font-bold">Quên?</a>
                  )}
                </div>
                <div className="relative flex items-center">
                  <span className="absolute left-0 text-gray-400 dark:text-[#A1A1AA] w-6 flex justify-center"><i className="fas fa-lock text-sm"></i></span>
                  <input 
                    type={showPassword ? "text" : "password"} 
                    placeholder="••••••••"
                    className="w-full bg-transparent border-b border-gray-200 dark:border-white/10 py-3 px-8 outline-none focus:border-[#C9A84C] transition-all text-lg text-black dark:text-[#F5F5F0] tracking-widest"
                    value={activeTab === 'login' ? loginData.password : regData.password}
                    onChange={(e) => activeTab === 'login' ? setLoginData({...loginData, password: e.target.value}) : setRegData({...regData, password: e.target.value})}
                    required
                  />
                  <button 
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-0 text-gray-400 dark:text-[#A1A1AA] hover:text-[#C9A84C] w-8 h-full flex items-center justify-center"
                  >
                    <i className={`far ${showPassword ? 'fa-eye-slash' : 'fa-eye'} text-sm`}></i>
                  </button>
                </div>
              </div>

              {/* Submit Button */}
              <button 
                type="submit"
                disabled={loading}
                className="w-full py-4 bg-[#C9A84C] hover:bg-[#E5C76B] text-[#0A0A0A] font-header text-xl tracking-[2px] transition-all flex items-center justify-center space-x-2 shadow-[0_10px_30px_rgba(201,168,76,0.2)]"
              >
                {loading ? (
                  <i className="fas fa-spinner fa-spin"></i>
                ) : (
                  <>
                    <span className="mt-1">{activeTab === 'login' ? 'ĐĂNG NHẬP' : 'TẠO TÀI KHOẢN'}</span>
                    <i className="fas fa-arrow-right text-sm"></i>
                  </>
                )}
              </button>

            </form>
          </div>

          <div className="p-6 bg-gray-50/50 dark:bg-black/20 text-center border-t border-gray-100 dark:border-white/5">
            <p className="text-xs text-gray-500 dark:text-[#A1A1AA]">
              {activeTab === 'login' ? "Chưa có tài khoản?" : "Đã có tài khoản?"} 
              <button 
                onClick={() => setActiveTab(activeTab === 'login' ? 'register' : 'login')}
                className="text-[#C9A84C] ml-1 font-bold uppercase tracking-wider hover:underline"
              >
                {activeTab === 'login' ? "Đăng ký ngay" : "Đăng nhập"}
              </button>
            </p>
          </div>

        </div>

        <a href="/" className="mt-8 text-gray-400 dark:text-[#A1A1AA] hover:text-[#C9A84C] transition-all text-xs uppercase tracking-[2px] flex items-center space-x-2">
          <i className="fas fa-chevron-left text-[10px]"></i>
          <span>Quay lại trang chủ</span>
        </a>

      </div>

      <style>{`
        /* Autofill Styling */
        input:-webkit-autofill,
        input:-webkit-autofill:hover, 
        input:-webkit-autofill:focus,
        input:-internal-autofill-selected {
          -webkit-text-fill-color: #000000 !important;
          -webkit-box-shadow: 0 0 0px 1000px #FFFFFF inset !important;
          background-clip: content-box !important;
          transition: background-color 5000s ease-in-out 0s;
        }
        .dark input:-webkit-autofill,
        .dark input:-webkit-autofill:hover, 
        .dark input:-webkit-autofill:focus,
        .dark input:-internal-autofill-selected {
          -webkit-text-fill-color: #F5F5F0 !important;
          -webkit-box-shadow: 0 0 0px 1000px #1C1C1C inset !important;
        }
        input::placeholder { color: #A1A1AA; opacity: 1; font-size: 15px; }
        .dark input::placeholder { color: #71717A; }
      `}</style>

    </div>
  );
};

export default AuthPage;
