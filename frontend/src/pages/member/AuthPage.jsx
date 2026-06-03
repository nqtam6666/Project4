import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

/**
 * IRONCORE GYM - Login & Registration Page
 * Style: Dark Industrial-Luxury
 */

const NQT_LANGUAGES = {
  'vi': { flag: '🇻🇳', name: 'Tiếng Việt' },
  'en': { flag: '🇺🇸', name: 'English' },
  'zh-CN': { flag: '🇨🇳', name: '简体中文' },
  'zh-TW': { flag: '🇹🇼', name: '繁體中文' },
  'ja': { flag: '🇯🇵', name: '日本語' },
  'ko': { flag: '🇰🇷', name: '한국어' }
};

const AuthPage = () => {
  const [activeTab, setActiveTab] = useState('login');
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [notification, setNotification] = useState(null);
  const [isDarkMode, setIsDarkMode] = useState(() => {
    return localStorage.getItem("nqt_theme") !== "light";
  });
  const [googleReady, setGoogleReady] = useState(false);
  const [loginData, setLoginData] = useState({ phone: '0961111101', password: '0961111101' });
  const [regData, setRegData] = useState({ name: '', phone: '', email: '', password: '', confirmPassword: '' });
  const [forgotEmail, setForgotEmail] = useState('');
  const [otpSent, setOtpSent] = useState(false);
  const [otpCode, setOtpCode] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [twoFactorPending, setTwoFactorPending] = useState(false);
  const [twoFactorToken, setTwoFactorToken] = useState('');
  const [twoFactorCode, setTwoFactorCode] = useState('');

  const [siteConfig, setSiteConfig] = useState({
    g6_ten_website: "G6 GYM",
    g6_slogan: "Forge Your Legacy",
    g6_logo_url: "",
    g6_favicon_url: ""
  });



  const showToast = (type, message) => {
    setNotification({ type, message });
    setTimeout(() => setNotification(null), 4000);
  };

  // Load Google GIS client script dynamically
  React.useEffect(() => {
    const scriptId = "google-gis-client";
    let script = document.getElementById(scriptId);
    
    const checkGoogleAndSetReady = () => {
      if (window.google && window.google.accounts && window.google.accounts.id) {
        setGoogleReady(true);
      } else {
        const interval = setInterval(() => {
          if (window.google && window.google.accounts && window.google.accounts.id) {
            setGoogleReady(true);
            clearInterval(interval);
          }
        }, 100);
        return interval;
      }
    };

    let intervalId;
    if (!script) {
      script = document.createElement("script");
      script.id = scriptId;
      script.src = "https://accounts.google.com/gsi/client";
      script.async = true;
      script.defer = true;
      script.onload = () => {
        intervalId = checkGoogleAndSetReady();
      };
      document.body.appendChild(script);
    } else {
      intervalId = checkGoogleAndSetReady();
    }

    return () => {
      if (intervalId) clearInterval(intervalId);
    };
  }, []);

  const handleGoogleLogin = async (response) => {
    setLoading(true);
    try {
      const res = await fetch('/api/nqt-hoi-vien/google-login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({
          credential: response.credential
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
        showToast('success', 'Đăng nhập Google thành công! Đang chuyển hướng...');
        setTimeout(() => window.location.href = '/home', 1000);
      } else {
        showToast('error', data.nqt_thong_diep || 'Đăng nhập Google thất bại');
      }
    } catch (e) {
      setLoading(false);
      showToast('error', 'Lỗi kết nối máy chủ');
    }
  };

  // Render Google button when config and GIS are ready using a callback ref
  const googleButtonRef = React.useCallback((node) => {
    if (node && siteConfig.g6_google_client_id && googleReady && window.google && window.google.accounts && window.google.accounts.id) {
      try {
        window.google.accounts.id.initialize({
          client_id: siteConfig.g6_google_client_id,
          callback: handleGoogleLogin
        });
        
        window.google.accounts.id.renderButton(
          node,
          { 
            theme: isDarkMode ? "filled_black" : "outline", 
            size: "large", 
            width: 350,
            text: "signin_with",
            shape: "square"
          }
        );
      } catch (e) {
        console.error("Google accounts initialize/render error:", e);
      }
    }
  }, [siteConfig.g6_google_client_id, googleReady, isDarkMode]);

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

  const handleAuth = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      if (activeTab === 'login') {
        if (twoFactorPending) {
          const res = await fetch('/api/nqt-hoi-vien/2fa/login-verify', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              nqt_2fa_token: twoFactorToken,
              g6_code: twoFactorCode
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
            showToast('success', 'Xác thực 2FA thành công! Đang chuyển hướng...');
            setTimeout(() => window.location.href = '/home', 1000);
          } else {
            showToast('error', data.nqt_thong_diep || 'Mã xác thực 2FA không chính xác');
          }
          return;
        }

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
          if (data.nqt_du_lieu && data.nqt_du_lieu.g6_la_xac_thuc_otp) {
            setTwoFactorPending(true);
            setTwoFactorToken(data.nqt_du_lieu.nqt_2fa_token);
            showToast('info', 'Tài khoản đã được bảo mật 2 lớp. Vui lòng nhập mã OTP để tiếp tục.');
            return;
          }
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
      } else if (activeTab === 'register') {
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
      } else if (activeTab === 'forgot') {
        if (!otpSent) {
          const res = await fetch('/api/nqt-hoi-vien/quen-mat-khau', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ g6_email: forgotEmail })
          });
          const data = await res.json();
          setLoading(false);
          if (data.nqt_thanh_cong) {
            setOtpSent(true);
            showToast('success', 'Mã OTP đã được gửi về email của bạn.');
          } else {
            showToast('error', data.nqt_thong_diep || 'Không gửi được mã OTP');
          }
        } else {
          const res = await fetch('/api/nqt-hoi-vien/dat-lai-mat-khau', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              g6_email: forgotEmail,
              g6_reset_token: otpCode,
              g6_mat_khau_moi: newPassword
            })
          });
          const data = await res.json();
          setLoading(false);
          if (data.nqt_thanh_cong) {
            showToast('success', 'Đặt lại mật khẩu thành công! Đang chuyển về trang đăng nhập...');
            setTimeout(() => {
              setActiveTab('login');
              setOtpSent(false);
              setOtpCode('');
              setNewPassword('');
              setForgotEmail('');
            }, 2000);
          } else {
            showToast('error', data.nqt_thong_diep || 'Đặt lại mật khẩu thất bại');
          }
        }
      }
    } catch (error) {
      setLoading(false);
      showToast('error', 'Lỗi kết nối máy chủ');
    }
  };

  const [showLangMenu, setShowLangMenu] = useState(false);
  const langRef = React.useRef(null);

  React.useEffect(() => {
    const handleOutsideClick = (e) => {
      if (langRef.current && !langRef.current.contains(e.target)) {
        setShowLangMenu(false);
      }
    };
    document.addEventListener("mousedown", handleOutsideClick);
    return () => document.removeEventListener("mousedown", handleOutsideClick);
  }, []);

  React.useEffect(() => {
    if (!window.googleTranslateElementInit) {
      window.googleTranslateElementInit = function() {
        new window.google.translate.TranslateElement({pageLanguage: 'vi'}, 'google_translate_element');
      };
      if (!document.getElementById('google_translate_element')) {
        const gDiv = document.createElement('div');
        gDiv.id = 'google_translate_element';
        gDiv.style.display = 'none';
        document.body.appendChild(gDiv);
      }
      const script = document.createElement('script');
      script.src = 'https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
      script.async = true;
      document.head.appendChild(script);
    }
    
    if (!document.getElementById('google-translate-overrides')) {
      const translateStyle = document.createElement('style');
      translateStyle.id = 'google-translate-overrides';
      translateStyle.textContent = `
        iframe.goog-te-banner-frame,
        .VIpgJd-ZVi9od-ORHb-OEVmcd,
        .VIpgJd-ZVi9od-l4eHX-hSRGPd,
        .VIpgJd-yAWNEb-L7lbkb,
        iframe.skiptranslate,
        #goog-gt-tt { display: none !important; }
        body { top: 0px !important; }
        html { margin-top: 0px !important; }
      `;
      document.head.appendChild(translateStyle);
    }
  }, []);

  const changeLanguage = (langCode) => {
    const eraseCookie = (name) => {
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
    };
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
    window.location.reload();
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

      {/* Floating Language Switcher */}
      <div ref={langRef} className="fixed top-6 right-20 z-50">
        <button 
          type="button"
          onClick={() => setShowLangMenu(!showLangMenu)}
          className="w-10 h-10 rounded-full bg-white dark:bg-[#1C1C1C] border border-gray-200 dark:border-white/10 flex items-center justify-center text-[#C9A84C] hover:text-[#E5C76B] transition-all shadow-md focus:outline-none"
          title="Chọn ngôn ngữ"
        >
          <i className="fas fa-globe text-lg"></i>
        </button>
        {showLangMenu && (
          <div className="absolute right-0 mt-2 w-56 bg-white dark:bg-[#1C1C1C] border border-gray-200 dark:border-white/10 rounded-xl shadow-2xl overflow-hidden py-1 flex flex-col z-50">
            {Object.entries(NQT_LANGUAGES).map(([code, l]) => (
              <button
                key={code}
                type="button"
                onClick={() => changeLanguage(code)}
                className="w-full px-4 py-2.5 text-left hover:bg-gray-50 dark:hover:bg-white/[0.02] hover:text-[#C9A84C] flex items-center space-x-3 transition-colors text-sm text-[#0A0A0A] dark:text-[#F5F5F0]"
              >
                <span className="text-base">{l.flag}</span>
                <span className="font-medium">{l.name}</span>
              </button>
            ))}
          </div>
        )}
      </div>

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
          {twoFactorPending ? (
            <div className="flex border-b border-gray-100 dark:border-white/5 bg-gray-50/50 dark:bg-white/[0.02] justify-center py-5">
              <span className="font-header text-lg tracking-widest text-[#C9A84C]">
                XÁC THỰC BẢO MẬT 2 LỚP
              </span>
            </div>
          ) : activeTab !== 'forgot' ? (
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
          ) : (
            <div className="flex border-b border-gray-100 dark:border-white/5 bg-gray-50/50 dark:bg-white/[0.02] justify-center py-5">
              <span className="font-header text-lg tracking-widest text-[#C9A84C]">
                {otpSent ? "ĐẶT LẠI MẬT KHẨU" : "QUÊN MẬT KHẨU"}
              </span>
            </div>
          )}

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

              {activeTab === 'login' && twoFactorPending ? (
                <div className="space-y-5">
                  <div className="text-center mb-4">
                    <div className="w-16 h-16 bg-[#C9A84C]/10 border border-[#C9A84C]/30 text-[#C9A84C] rounded-full flex items-center justify-center mx-auto mb-3 shadow-[0_0_15px_rgba(201,168,76,0.1)]">
                      <i className="fas fa-shield-alt text-2xl"></i>
                    </div>
                    <h3 className="font-header text-xl tracking-[1px] text-[#0A0A0A] dark:text-[#F5F5F0] uppercase">Mã Xác Thực 2FA</h3>
                    <p className="text-xs text-gray-500 dark:text-[#A1A1AA] mt-1">Vui lòng nhập mã 6 số từ ứng dụng Google Authenticator trên điện thoại của bạn.</p>
                  </div>
                  <div className="space-y-1 group">
                    <label className="text-xs uppercase tracking-widest text-gray-400 dark:text-[#A1A1AA] font-header group-focus-within:text-[#C9A84C] transition-colors">Mã bảo mật</label>
                    <div className="relative flex items-center">
                      <span className="absolute left-0 text-gray-400 dark:text-[#A1A1AA] w-6 flex justify-center"><i className="fas fa-key text-sm"></i></span>
                      <input 
                        type="text" 
                        inputMode="numeric"
                        pattern="[0-9]*"
                        maxLength="6"
                        placeholder="000000"
                        className="w-full bg-transparent border-b border-gray-200 dark:border-white/10 py-3 pl-8 outline-none focus:border-[#C9A84C] transition-all text-2xl tracking-[8px] text-center font-bold text-black dark:text-[#F5F5F0]"
                        value={twoFactorCode}
                        onChange={(e) => setTwoFactorCode(e.target.value.replace(/[^0-9]/g, ''))}
                        required
                        autoFocus
                      />
                    </div>
                  </div>
                  <div className="text-center pt-2">
                    <button 
                      type="button"
                      onClick={() => {
                        setTwoFactorPending(false);
                        setTwoFactorCode('');
                      }}
                      className="text-xs uppercase tracking-widest text-[#C9A84C] hover:text-[#E5C76B] transition-colors font-bold focus:outline-none"
                    >
                      <i className="fas fa-arrow-left mr-1.5"></i> Quay lại đăng nhập
                    </button>
                  </div>
                </div>
              ) : activeTab !== 'forgot' ? (
                <>
                  <div className="space-y-1 group">
                    <label className="text-xs uppercase tracking-widest text-gray-400 dark:text-[#A1A1AA] font-header group-focus-within:text-[#C9A84C] transition-colors">
                      {activeTab === 'login' ? 'Tài khoản, Email hoặc SĐT' : 'Địa chỉ Email'}
                    </label>
                    <div className="relative flex items-center">
                      <span className="absolute left-0 text-gray-400 dark:text-[#A1A1AA] w-6 flex justify-center">
                        <i className={activeTab === 'login' ? "far fa-user text-sm" : "far fa-envelope text-sm"}></i>
                      </span>
                      <input 
                        type={activeTab === 'login' ? "text" : "email"}
                        placeholder={activeTab === 'login' ? "Tên đăng nhập, Email hoặc SĐT" : "gym@g6gym.vn"}
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
                        <button 
                          type="button"
                          onClick={() => {
                            setActiveTab('forgot');
                            setOtpSent(false);
                          }}
                          className="text-[10px] uppercase tracking-widest text-[#C9A84C] hover:text-[#E5C76B] transition-colors font-bold focus:outline-none"
                        >
                          Quên?
                        </button>
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
                </>
              ) : (
                <>
                  <div className="space-y-1 group">
                    <label className="text-xs uppercase tracking-widest text-gray-400 dark:text-[#A1A1AA] font-header group-focus-within:text-[#C9A84C] transition-colors">Địa chỉ Email</label>
                    <div className="relative flex items-center">
                      <span className="absolute left-0 text-gray-400 dark:text-[#A1A1AA] w-6 flex justify-center"><i className="far fa-envelope text-sm"></i></span>
                      <input 
                        type="email" 
                        placeholder="gym@g6gym.vn"
                        className="w-full bg-transparent border-b border-gray-200 dark:border-white/10 py-3 pl-8 outline-none focus:border-[#C9A84C] transition-all text-lg text-black dark:text-[#F5F5F0]"
                        value={forgotEmail}
                        onChange={(e) => setForgotEmail(e.target.value)}
                        required
                        disabled={otpSent}
                      />
                    </div>
                  </div>

                  {otpSent && (
                    <>
                      <div className="space-y-1 group">
                        <label className="text-xs uppercase tracking-widest text-gray-400 dark:text-[#A1A1AA] font-header group-focus-within:text-[#C9A84C] transition-colors">Mã xác nhận OTP</label>
                        <div className="relative flex items-center">
                          <span className="absolute left-0 text-gray-400 dark:text-[#A1A1AA] w-6 flex justify-center"><i className="fas fa-key text-sm"></i></span>
                          <input 
                            type="text" 
                            placeholder="Nhập mã OTP gồm 6 số"
                            className="w-full bg-transparent border-b border-gray-200 dark:border-white/10 py-3 pl-8 outline-none focus:border-[#C9A84C] transition-all text-lg text-black dark:text-[#F5F5F0] tracking-widest font-bold"
                            value={otpCode}
                            onChange={(e) => setOtpCode(e.target.value)}
                            required
                          />
                        </div>
                      </div>

                      <div className="space-y-1 group">
                        <label className="text-xs uppercase tracking-widest text-gray-400 dark:text-[#A1A1AA] font-header group-focus-within:text-[#C9A84C] transition-colors">Mật khẩu mới</label>
                        <div className="relative flex items-center">
                          <span className="absolute left-0 text-gray-400 dark:text-[#A1A1AA] w-6 flex justify-center"><i className="fas fa-lock text-sm"></i></span>
                          <input 
                            type={showPassword ? "text" : "password"} 
                            placeholder="Tối thiểu 6 ký tự"
                            className="w-full bg-transparent border-b border-gray-200 dark:border-white/10 py-3 px-8 outline-none focus:border-[#C9A84C] transition-all text-lg text-black dark:text-[#F5F5F0] tracking-widest"
                            value={newPassword}
                            onChange={(e) => setNewPassword(e.target.value)}
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
                    </>
                  )}
                </>
              )}

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
                    <span className="mt-1">
                      {activeTab === 'login' ? (twoFactorPending ? 'XÁC THỰC 2FA' : 'ĐĂNG NHẬP') : activeTab === 'register' ? 'TẠO TÀI KHOẢN' : otpSent ? 'XÁC NHẬN ĐỔI MẬT KHẨU' : 'GỬI MÃ OTP'}
                    </span>
                    <i className="fas fa-arrow-right text-sm"></i>
                  </>
                )}
              </button>

              {activeTab !== 'forgot' && !twoFactorPending && siteConfig.g6_google_client_id && (
                <>
                  <div className="relative flex py-2 items-center">
                    <div className="flex-grow border-t border-gray-200 dark:border-white/10"></div>
                    <span className="flex-shrink mx-4 text-gray-400 text-[10px] font-header tracking-wider uppercase">Hoặc</span>
                    <div className="flex-grow border-t border-gray-200 dark:border-white/10"></div>
                  </div>

                    <div ref={googleButtonRef} className="flex justify-center w-full min-h-[40px]"></div>
                </>
              )}

            </form>
          </div>

          {!twoFactorPending && (
            <div className="p-6 bg-gray-50/50 dark:bg-black/20 text-center border-t border-gray-100 dark:border-white/5">
              <p className="text-xs text-gray-500 dark:text-[#A1A1AA]">
                {activeTab === 'login' ? "Chưa có tài khoản?" : activeTab === 'register' ? "Đã có tài khoản?" : "Đã nhớ mật khẩu?"} 
                <button 
                  onClick={() => {
                    if (activeTab === 'forgot') {
                      setActiveTab('login');
                      setOtpSent(false);
                      setOtpCode('');
                      setNewPassword('');
                      setForgotEmail('');
                    } else {
                      setActiveTab(activeTab === 'login' ? 'register' : 'login');
                    }
                  }}
                  className="text-[#C9A84C] ml-1 font-bold uppercase tracking-wider hover:underline"
                >
                  {activeTab === 'login' ? "Đăng ký ngay" : "Đăng nhập"}
                </button>
              </p>
            </div>
          )}

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
