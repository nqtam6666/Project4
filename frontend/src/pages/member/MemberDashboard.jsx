import React, { useState, useEffect, useRef } from "react";
import {
  LayoutDashboard,
  Calendar,
  History,
  Package,
  User,
  Bell,
  LogOut,
  CheckCircle2,
  TrendingUp,
  Activity,
  ChevronRight,
  Search,
  Filter,
  Plus,
  QrCode,
  UserCircle2,
  ShieldCheck,
  Moon,
  Sun,
  ArrowRight,
  Zap,
  MessageSquare,
  Info,
} from "lucide-react";
import { generateQrSvg } from "../../js/nqtQrHelper";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  LineChart,
  Line,
} from "recharts";
import { motion, AnimatePresence } from "framer-motion";
import { nqtApi } from "../../js/member/auth";

/**
 * IRONCORE GYM - Member Dashboard
 * Aesthetic: Luxury Glassmorphism
 * Theme: Gold / Deep Black
 */

const MemberDashboard = () => {
  const [activeTab, setActiveTab] = useState("dashboard");
  const [loading, setLoading] = useState(true);
  const [showQR, setShowQR] = useState(false);
  const [showChat, setShowChat] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(
    localStorage.getItem("nqt_theme") !== "light",
  );
  const [isAdmin, setIsAdmin] = useState(false); // Default to false
  const [notification, setNotification] = useState(null);
  const [notificationsData, setNotificationsData] = useState([]);
  const [showNotifications, setShowNotifications] = useState(false);
  const unreads = notificationsData.filter((n) => !n.g6_la_da_doc).length;

  const handleMarkAsRead = async (id) => {
    try {
      await nqtApi(`/api/nqt-thong-bao/${id}/nqt-doc`, { method: "PUT" });
      setNotificationsData((prev) =>
        prev.map((n) =>
          n.g6_ma_thong_bao === id ? { ...n, g6_la_da_doc: true } : n,
        ),
      );
    } catch (e) {}
  };

  const showToast = (type, message) => {
    setNotification({ type, message });
    setTimeout(() => setNotification(null), 3000);
  };

  const handleFeatureInDev = () => {
    showToast("info", "Tính năng đang được phát triển!");
  };

  // States for real data
  const [profile, setProfile] = useState({});
  const [activePackage, setActivePackage] = useState(null);
  const [attendance, setAttendance] = useState([]);
  const [metrics, setMetrics] = useState([]);

  // States for sub-tabs
  const [fullHistory, setFullHistory] = useState([]);
  const [packages, setPackages] = useState({ active: [], available: [] });
  const [classes, setClasses] = useState([]);
  const [pts, setPts] = useState({ active: null, available: [] });
  const [tabLoading, setTabLoading] = useState(false);

  const qrRef = useRef(null);
  const modalQrRef = useRef(null);

  const handleLogout = async () => {
    try {
      await nqtApi("/api/nqt-hoi-vien/dang-xuat", { method: "POST" });
    } catch (e) {}
    localStorage.removeItem("nqt_access_token");
    localStorage.removeItem("nqt_refresh_token");
    localStorage.removeItem("nqt_admin_token");
    localStorage.removeItem("nqt_token");
    window.location.href = "/login";
  };

  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add("dark");
      localStorage.setItem("nqt_theme", "dark");
    } else {
      document.documentElement.classList.remove("dark");
      localStorage.setItem("nqt_theme", "light");
    }

    if (!document.getElementById("nqt-portal-fonts")) {
      const link = document.createElement("link");
      link.id = "nqt-portal-fonts";
      link.rel = "stylesheet";
      link.href =
        "https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@0,600;0,700;0,800;0,900;1,700&family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,400&display=swap";
      document.head.appendChild(link);
    }

    const fetchRealData = async () => {
      try {
        const resProfile = await nqtApi("/api/nqt-hoi-vien/toi");
        if (resProfile.status === 401) throw new Error("Unauthorized");
        const dataProfile = await resProfile.json();
        if (dataProfile.nqt_thanh_cong) {
          const p = dataProfile.nqt_du_lieu.nqt_hoi_vien || {};
          setProfile(p);
          setActivePackage(dataProfile.nqt_du_lieu.nqt_goi_hien_tai || null);

          if (localStorage.getItem("nqt_admin_token")) {
            setIsAdmin(true);
          }

          try {
            const resNotif = await nqtApi(
              `/api/nqt-thong-bao?g6_loai_nguoi_nhan=hoi_vien&g6_ma_nguoi_nhan=${p.g6_ma_nguoi_dung}`,
            );
            const dataNotif = await resNotif.json();
            if (dataNotif.nqt_thanh_cong)
              setNotificationsData(dataNotif.nqt_du_lieu);
          } catch (e) {}
        }

        const resAtt = await nqtApi(
          "/api/nqt-hoi-vien/diem-danh?g6_gioi_han=5",
        );
        const dataAtt = await resAtt.json();
        if (dataAtt.nqt_thanh_cong) setAttendance(dataAtt.nqt_du_lieu || []);

        const resMetrics = await nqtApi("/api/nqt-hoi-vien/toi/nqt-chi-so");
        const dataMetrics = await resMetrics.json();
        if (dataMetrics.nqt_thanh_cong) {
          const formattedMetrics = (dataMetrics.nqt_du_lieu || [])
            .reverse()
            .map((m) => ({
              name: m.g6_ngay_do.substring(5, 10),
              weight: m.g6_can_nang,
              fat: m.g6_ty_le_mo || 0,
            }));
          setMetrics(formattedMetrics);
        }

        try {
          const resPt = await nqtApi(
            "/api/nxv-dang-ky-pt?g6_trang_thai=dang_dung",
          );
          if (resPt.ok) {
            const dataPt = await resPt.json();
            const ptList =
              dataPt.nqt_du_lieu?.g6_danh_sach || dataPt.nqt_du_lieu || [];
            if (dataPt.nqt_thanh_cong && ptList.length > 0) {
              setPts((prev) => ({ ...prev, active: ptList[0] }));
            }
          }
        } catch (e) {}

        // Fetch classes for calendar
        try {
          const resClasses = await nqtApi("/api/nqt-public/classes");
          if (resClasses.ok) {
            const dataClasses = await resClasses.json();
            if (dataClasses.nqt_thanh_cong) {
              setClasses(dataClasses.nqt_du_lieu || []);
            }
          }
        } catch (e) {}

        setLoading(false);
      } catch (error) {
        handleLogout();
      }
    };

    fetchRealData();
  }, [isDarkMode]);

  useEffect(() => {
    if (activeTab === "dashboard") return;
    const fetchTabData = async () => {
      setTabLoading(true);
      try {
        if (activeTab === "history") {
          const res = await nqtApi("/api/nqt-hoi-vien/diem-danh");
          const data = await res.json();
          if (data.nqt_thanh_cong) setFullHistory(data.nqt_du_lieu || []);
        } else if (activeTab === "packages") {
          const resMyPkgs = await nqtApi("/api/nqt-dang-ky-goi-tap");
          const resAllPkgs = await nqtApi("/api/nqt-public/goi-tap");
          const dataMy = await resMyPkgs.json();
          const dataAll = await resAllPkgs.json();
          setPackages({
            active: dataMy.nqt_thanh_cong
              ? dataMy.nqt_du_lieu?.g6_danh_sach || dataMy.nqt_du_lieu
              : [],
            available: dataAll.nqt_thanh_cong ? dataAll.nqt_du_lieu : [],
          });
        } else if (activeTab === "classes") {
          // Already fetched in dashboard, but fetch again to be sure
          const res = await nqtApi("/api/nqt-public/classes");
          const data = await res.json();
          if (data.nqt_thanh_cong) setClasses(data.nqt_du_lieu || []);
        } else if (activeTab === "pt") {
          let myPt = null;
          try {
            const resMyPt = await nqtApi("/api/nxv-dang-ky-pt");
            const dataMy = await resMyPt.json();
            if (dataMy.nqt_thanh_cong) {
              const list =
                dataMy.nqt_du_lieu?.g6_danh_sach || dataMy.nqt_du_lieu;
              if (list && list.length > 0) myPt = list[0];
            }
          } catch (e) {}
          const resAllPt = await nqtApi("/api/nqt-public/huan-luyen-vien");
          const dataAll = await resAllPt.json();
          setPts({
            active: myPt,
            available: dataAll.nqt_thanh_cong ? dataAll.nqt_du_lieu : [],
          });
        }
      } catch (e) {
        console.error("Fetch Error:", e);
      }
      setTabLoading(false);
    };
    fetchTabData();
  }, [activeTab]);

  const handleSubscribePackage = async (pkgId) => {
    try {
      const res = await nqtApi("/api/nqt-mua-goi-tap", {
        method: "POST",
        body: JSON.stringify({ g6_ma_goi_tap: pkgId }),
      });
      const data = await res.json();
      if (data.nqt_thanh_cong) {
        showToast("success", "Đăng ký gói tập thành công!");
      } else {
        showToast("error", data.nqt_thong_diep || "Lỗi khi đăng ký gói tập");
      }
    } catch (err) {
      showToast("error", "Không thể kết nối đến máy chủ");
    }
  };

  const handleSubscribePT = async (hlvId) => {
    try {
      const res = await nqtApi("/api/nqt-mua-goi-pt", {
        method: "POST",
        body: JSON.stringify({ g6_ma_hlv: hlvId }),
      });
      const data = await res.json();
      if (data.nqt_thanh_cong) {
        showToast("success", "Đăng ký PT thành công!");
      } else {
        showToast("error", data.nqt_thong_diep || "Lỗi khi đăng ký PT");
      }
    } catch (err) {
      showToast("error", "Không thể kết nối đến máy chủ");
    }
  };

  const handleJoinClass = async (lopId) => {
    try {
      const res = await nqtApi("/api/nqt-dat-cho-lop", {
        method: "POST",
        body: JSON.stringify({ g6_ma_lop_hoc: lopId }),
      });
      const data = await res.json();
      if (data.nqt_thanh_cong) {
        showToast("success", "Đặt chỗ lớp học thành công!");
      } else {
        showToast("error", data.nqt_thong_diep || "Lỗi khi đặt chỗ");
      }
    } catch (err) {
      showToast("error", "Không thể kết nối đến máy chủ");
    }
  };

  const handleBookPT = async (dangKyId) => {
    try {
      const res = await nqtApi("/api/nqt-dat-lich-pt", {
        method: "POST",
        body: JSON.stringify({ g6_ma_dang_ky_pt: dangKyId }),
      });
      const data = await res.json();
      if (data.nqt_thanh_cong) {
        showToast("success", "Đặt lịch tập PT thành công!");
      } else {
        showToast("error", data.nqt_thong_diep || "Lỗi khi đặt lịch");
      }
    } catch (err) {
      showToast("error", "Không thể kết nối đến máy chủ");
    }
  };

  if (loading)
    return (
      <div className="min-h-screen bg-[#FAFAFA] dark:bg-[#0A0A0A] flex items-center justify-center">
        Loading...
      </div>
    );

  let daysLeft = "Hết hạn";
  if (activePackage && activePackage.g6_ngay_het_han) {
    const end = new Date(activePackage.g6_ngay_het_han);
    const now = new Date();
    const diffTime = end - now;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    daysLeft = diffDays > 0 ? `${diffDays} ngày` : "Đã hết hạn";
  }

  return (
    <div className="min-h-screen bg-[#FAFAFA] dark:bg-[#0A0A0A] text-[#0A0A0A] dark:text-[#F5F5F0] font-['Barlow_Condensed'] transition-colors duration-500 flex">
      {/* --- Notifications --- */}
      <AnimatePresence>
        {notification && (
          <motion.div
            initial={{ opacity: 0, y: -50, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9, transition: { duration: 0.2 } }}
            className="fixed top-10 z-[100] flex items-center justify-center w-full px-4 pointer-events-none"
          >
            <div
              className={`pointer-events-auto px-8 py-4 bg-white dark:bg-[#1C1C1C] border ${notification.type === "success" ? "border-[#C9A84C]" : notification.type === "info" ? "border-blue-500" : "border-red-500"} shadow-[0_20px_50px_rgba(0,0,0,0.5)] flex items-center space-x-4 rounded-xl`}
            >
              <div
                className={`w-10 h-10 rounded-full flex items-center justify-center ${notification.type === "success" ? "bg-[#C9A84C]/10 text-[#C9A84C]" : notification.type === "info" ? "bg-blue-500/10 text-blue-500" : "bg-red-500/10 text-red-500"}`}
              >
                <i
                  className={`fas ${notification.type === "success" ? "fa-check" : notification.type === "info" ? "fa-info-circle" : "fa-exclamation-circle"} text-xl`}
                ></i>
              </div>
              <div>
                <p className="font-bold tracking-widest text-lg leading-none uppercase text-[#0A0A0A] dark:text-[#F5F5F0]">
                  {notification.type === "success"
                    ? "Thành công"
                    : notification.type === "info"
                      ? "Thông báo"
                      : "Lỗi"}
                </p>
                <p className="text-sm text-gray-500 dark:text-[#A1A1AA] mt-1">
                  {notification.message}
                </p>
              </div>
              <button
                onClick={() => setNotification(null)}
                className="ml-4 text-[#52525B] hover:text-[#0A0A0A] dark:text-[#F5F5F0]"
              >
                <i className="fas fa-times"></i>
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <aside className="w-72 bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)] dark:shadow-none dark:bg-white/5 backdrop-blur-2xl border-r border-gray-100 dark:border-white/10 flex flex-col h-screen sticky top-0 z-50">
        <div className="p-8 border-b border-gray-50 dark:border-white/5 text-center">
          <h1 className="text-3xl font-black tracking-[4px] text-[#C9A84C] font-['Cormorant_Garamond']">
            IRONCORE
          </h1>
          <p className="text-[10px] uppercase tracking-[3px] text-gray-500 dark:text-[#A1A1AA] font-bold mt-1">
            Member Portal
          </p>
        </div>

        <div className="p-6">
          <div className="bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)] dark:shadow-none dark:bg-white/5 rounded-2xl p-4 border border-gray-100 dark:border-white/10 group">
            <div className="flex items-center space-x-3 mb-4">
              <img
                src={
                  profile.g6_anh_the ||
                  "https://ui-avatars.com/api/?name=" +
                    encodeURIComponent(profile.g6_ho_ten || "HV") +
                    "&background=C9A84C&color=000"
                }
                className="w-12 h-12 rounded-xl object-cover border border-[#C9A84C]/20"
              />
              <div>
                <h3 className="font-bold text-sm leading-none">
                  {profile.g6_ho_ten || "Hội viên"}
                </h3>
                <p className="text-[10px] text-slate-500 mt-1">
                  ID: {profile.g6_ma_nguoi_dung}
                </p>
              </div>
            </div>
            <img
              src={
                profile.g6_ma_nguoi_dung
                  ? generateQrSvg(
                      profile.g6_ma_qr || String(profile.g6_ma_nguoi_dung),
                      40,
                    )
                  : ""
              }
              className="w-10 h-10 rounded bg-white p-0.5"
            />
            <span className="text-[9px] font-bold text-[#C9A84C] tracking-widest">
              SHOW QR CODE
            </span>
          </div>
        </div>

        <nav className="flex-1 px-4 space-y-1">
          <NavItem
            icon={<LayoutDashboard size={20} />}
            label="Dashboard"
            active={activeTab === "dashboard"}
            onClick={() => setActiveTab("dashboard")}
          />
          <NavItem
            icon={<Calendar size={20} />}
            label="Lịch tập"
            active={activeTab === "classes"}
            onClick={() => setActiveTab("classes")}
          />
          <NavItem
            icon={<History size={20} />}
            label="Lịch sử"
            active={activeTab === "history"}
            onClick={() => setActiveTab("history")}
          />
          <NavItem
            icon={<Package size={20} />}
            label="Gói tập"
            active={activeTab === "packages"}
            onClick={() => setActiveTab("packages")}
          />
          <NavItem
            icon={<UserCircle2 size={20} />}
            label="PT Cá nhân"
            active={activeTab === "pt"}
            onClick={() => setActiveTab("pt")}
          />
        </nav>

        <div className="p-4 space-y-2 border-t border-gray-50 dark:border-white/5 ">
          {isAdmin && (
            <button
              onClick={() => (window.location.href = "/admin/dashboard")}
              className="w-full flex items-center space-x-3 px-4 py-3 rounded-xl transition-all font-bold text-xs uppercase tracking-widest bg-[#C9A84C]/10 text-[#C9A84C] border border-[#C9A84C]/20 hover:bg-[#C9A84C] hover:text-[#0A0A0A]"
            >
              <Zap className="w-5 h-5" />
              <span>Quản trị hệ thống</span>
            </button>
          )}

          <button
            onClick={() => setIsDarkMode(!isDarkMode)}
            className="w-full flex items-center space-x-3 px-4 py-3 rounded-xl transition-all font-bold text-xs uppercase tracking-widest bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)] dark:shadow-none dark:bg-white/5 text-gray-500 dark:text-[#A1A1AA] hover:bg-black/10 dark:bg-white/10 hover:text-[#0A0A0A] dark:text-[#F5F5F0] "
          >
            {isDarkMode ? (
              <Bell className="w-5 h-5" />
            ) : (
              <Zap className="w-5 h-5" />
            )}
            <span>{isDarkMode ? "Chế độ Sáng" : "Chế độ Tối"}</span>
          </button>

          <button
            onClick={handleLogout}
            className="w-full flex items-center space-x-3 px-4 py-3 rounded-xl transition-all font-bold text-xs uppercase tracking-widest text-[#ef4444] hover:bg-[#ef4444]/10"
          >
            <LogOut className="w-5 h-5" />
            <span>Đăng xuất</span>
          </button>
        </div>
      </aside>

      {/* --- Main Content --- */}
      <main className="flex-1 p-8 overflow-y-auto h-screen custom-scrollbar relative">
        {/* Ambient Glows */}
        <div className="fixed top-[-10%] right-[-10%] w-[50%] h-[50%] bg-[#C9A84C]/5 blur-[120px] rounded-full pointer-events-none"></div>
        <div className="fixed bottom-[-10%] left-[-10%] w-[40%] h-[40%] bg-[#C9A84C]/5 blur-[120px] rounded-full pointer-events-none"></div>

        {tabLoading && activeTab !== "dashboard" ? (
          <div className="h-full flex flex-col items-center justify-center text-center">
            <div className="w-12 h-12 border-4 border-[#C9A84C]/20 border-t-[#C9A84C] rounded-full animate-spin mb-4"></div>
            <p className="text-[#C9A84C] font-bold uppercase tracking-widest text-sm">
              Đang tải dữ liệu...
            </p>
          </div>
        ) : (
          <>
            {activeTab === "history" && <HistoryView history={fullHistory} />}
            {activeTab === "packages" && (
              <PackagesView
                packages={packages}
                onAction={handleFeatureInDev}
                onSubscribe={handleSubscribePackage}
              />
            )}
            {activeTab === "classes" && (
              <ClassesView
                classes={classes}
                onAction={handleFeatureInDev}
                onJoin={handleJoinClass}
              />
            )}
            {activeTab === "pt" && (
              <PTView
                pts={pts}
                onAction={() => setShowChat(true)}
                onSubscribe={handleSubscribePT}
                onBook={handleBookPT}
              />
            )}

            {activeTab === "dashboard" && (
              <>
                {/* Header */}
                <header className="flex justify-between items-center mb-8">
                  <div>
                    <h2 className="text-2xl font-black tracking-tight flex items-center">
                      Chào buổi tối,{" "}
                      <span className="text-[#C9A84C] ml-2">
                        {profile.g6_ho_ten
                          ? profile.g6_ho_ten.split(" ").pop()
                          : "bạn"}
                      </span>
                      <motion.div
                        animate={{ rotate: [0, 10, -10, 0] }}
                        transition={{ repeat: Infinity, duration: 2 }}
                        className="ml-2"
                      >
                        <Zap
                          size={24}
                          className="text-[#C9A84C] fill-[#C9A84C]"
                        />
                      </motion.div>
                    </h2>
                    <p className="text-sm text-gray-500 dark:text-[#A1A1AA] italic font-bold">
                      "Mỗi bước tập luyện đều đưa bạn gần hơn tới phiên bản tốt
                      nhất của chính mình."
                    </p>
                  </div>

                  <div className="flex space-x-4">
                    <button
                      onClick={handleFeatureInDev}
                      className="w-12 h-12 rounded-full bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)] dark:shadow-none dark:bg-white/5 border border-gray-100 dark:border-white/10 flex items-center justify-center hover:bg-[#C9A84C] hover:text-[#0A0A0A] hover:border-[#C9A84C] transition-all group"
                    >
                      <Search
                        size={20}
                        className="group-hover:scale-110 transition-transform"
                      />
                    </button>
                    <div className="relative">
                      <button
                        onClick={() => setShowNotifications(!showNotifications)}
                        className="w-12 h-12 rounded-full bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)] dark:shadow-none dark:bg-white/5 border border-gray-100 dark:border-white/10 flex items-center justify-center hover:bg-[#C9A84C] hover:text-[#0A0A0A] hover:border-[#C9A84C] transition-all group relative z-10"
                      >
                        {unreads > 0 && (
                          <div className="absolute top-3 right-3 w-2 h-2 bg-red-500 rounded-full border border-[#0A0A0A]"></div>
                        )}
                        <Bell
                          size={20}
                          className="group-hover:scale-110 transition-transform"
                        />
                      </button>
                      {showNotifications && (
                        <div className="absolute top-14 right-0 w-80 bg-white dark:bg-[#1C1C1C] border border-gray-100 dark:border-white/10 rounded-2xl shadow-[0_0_50px_rgba(0,0,0,0.5)] z-50 overflow-hidden">
                          <div className="p-4 border-b border-gray-100 dark:border-white/10 flex justify-between items-center bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)] dark:shadow-none dark:bg-white/5">
                            <h4 className="font-bold text-[#0A0A0A] dark:text-[#F5F5F0]">
                              Thông báo
                            </h4>
                            <span className="text-xs bg-[#C9A84C] text-[#0A0A0A] px-2 py-0.5 rounded-full font-bold">
                              {unreads} mới
                            </span>
                          </div>
                          <div className="max-h-80 overflow-y-auto custom-scrollbar">
                            {notificationsData.length === 0 ? (
                              <div className="p-8 text-center text-gray-500 dark:text-[#A1A1AA] text-sm italic">
                                Không có thông báo nào
                              </div>
                            ) : (
                              notificationsData.map((n) => (
                                <div
                                  key={n.g6_ma_thong_bao}
                                  onClick={() => {
                                    if (!n.g6_la_da_doc)
                                      handleMarkAsRead(n.g6_ma_thong_bao);
                                  }}
                                  className={`p-4 border-b border-gray-50 dark:border-white/5 cursor-pointer transition-all ${!n.g6_la_da_doc ? "bg-[#C9A84C]/10 hover:bg-[#C9A84C]/20" : "hover:bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)] dark:shadow-none dark:bg-white/5"}`}
                                >
                                  <div className="flex justify-between items-start mb-1">
                                    <h5
                                      className={`text-sm ${!n.g6_la_da_doc ? "font-black text-[#C9A84C]" : "font-bold text-[#0A0A0A] dark:text-[#F5F5F0]"}`}
                                    >
                                      {n.g6_tieu_de}
                                    </h5>
                                    {!n.g6_la_da_doc && (
                                      <div className="w-2 h-2 bg-[#C9A84C] rounded-full mt-1.5 shadow-[0_0_8px_rgba(201,168,76,0.8)]"></div>
                                    )}
                                  </div>
                                  <p className="text-xs text-gray-500 dark:text-[#A1A1AA] line-clamp-2 leading-relaxed">
                                    {n.g6_noi_dung}
                                  </p>
                                  <p className="text-[10px] text-[#666] mt-2 font-bold tracking-widest uppercase">
                                    {new Date(n.g6_ngay_tao).toLocaleString()}
                                  </p>
                                </div>
                              ))
                            )}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                </header>

                {/* Stats Row */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
                  <StatCard
                    title="Hạn hội viên"
                    value={daysLeft}
                    sub={`Hết hạn: ${activePackage ? activePackage.g6_ngay_het_han : "Chưa đăng ký"}`}
                    icon={<Calendar className="text-[#C9A84C]" />}
                    cyan
                  />
                  <StatCard
                    title="Check-in gần đây"
                    value={attendance.length}
                    sub="Lượt điểm danh"
                    icon={<CheckCircle2 className="text-[#C9A84C]" />}
                  />
                  <StatCard
                    title="Điểm tích lũy"
                    value={profile.g6_tong_diem || 0}
                    sub="Tích lũy từ giao dịch"
                    icon={<Zap className="text-[#C9A84C]" />}
                  />
                  <StatCard
                    title="BMI mới nhất"
                    value={
                      metrics.length
                        ? (
                            metrics[metrics.length - 1].weight /
                            Math.pow(profile.g6_chieu_cao || 1.7, 2)
                          ).toFixed(1)
                        : "--"
                    }
                    sub="Dựa trên chỉ số gần nhất"
                    icon={<Activity className="text-[#C9A84C]" />}
                  />
                </div>

                {/* Center Grid */}
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-10">
                  {/* Calendar Widget */}
                  <div className="lg:col-span-2 bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)] dark:shadow-none dark:bg-white/5 backdrop-blur-xl border border-gray-100 dark:border-white/10 rounded-3xl p-8 relative overflow-hidden">
                    <div className="flex justify-between items-center mb-8">
                      <h3 className="font-bold text-xl flex items-center">
                        <Calendar size={20} className="mr-3 text-[#C9A84C]" />{" "}
                        Lịch tập tuần này
                      </h3>
                      <div className="flex bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)] dark:shadow-none dark:bg-white/5 rounded-xl p-1 border border-gray-100 dark:border-white/10">
                        <button className="px-4 py-1.5 rounded-lg text-xs font-bold bg-[#C9A84C] text-[#0A0A0A] shadow-[0_0_15px_rgba(201,168,76,0.4)]">
                          Tất cả
                        </button>
                        <button className="px-4 py-1.5 rounded-lg text-xs font-bold text-gray-500 dark:text-[#A1A1AA] hover:text-[#0A0A0A] dark:text-[#F5F5F0] transition-colors">
                          Lớp học
                        </button>
                      </div>
                    </div>

                    <div className="grid grid-cols-7 gap-4 text-center">
                      {(() => {
                        const today = new Date();
                        const dayOfWeek = today.getDay(); // 0 is Sunday, 1 is Monday
                        const diff =
                          today.getDate() -
                          dayOfWeek +
                          (dayOfWeek === 0 ? -6 : 1); // Monday
                        const monday = new Date(today.setDate(diff));

                        const days = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"];
                        return days.map((dayLabel, i) => {
                          const currentDate = new Date(monday);
                          currentDate.setDate(monday.getDate() + i);
                          const isToday =
                            new Date().toDateString() ===
                            currentDate.toDateString();

                          return (
                            <div key={dayLabel} className="space-y-4">
                              <p className="text-[10px] font-bold text-gray-500 dark:text-[#A1A1AA] uppercase tracking-widest">
                                {dayLabel}
                              </p>
                              <div
                                className={`h-24 rounded-2xl border flex flex-col items-center justify-center space-y-2 transition-all ${isToday ? "bg-[#C9A84C]/10 border-[#C9A84C]/30" : "bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)] dark:shadow-none dark:bg-white/5 border-gray-50 dark:border-white/5 hover:border-gray-100 dark:border-white/10"}`}
                              >
                                <span className="text-lg font-black">
                                  {currentDate.getDate()}
                                </span>
                                {isToday && (
                                  <div className="w-1.5 h-1.5 bg-[#C9A84C] rounded-full shadow-[0_0_8px_#C9A84C]"></div>
                                )}
                              </div>
                            </div>
                          );
                        });
                      })()}
                    </div>

                    <div className="mt-8 space-y-4">
                      {classes.length > 0 ? (
                        classes
                          .slice(0, 3)
                          .map((cls, idx) => (
                            <EventItem
                              key={`class-${idx}`}
                              time={
                                cls.g6_gio_bat_dau
                                  ? `${cls.g6_gio_bat_dau.substring(0, 5)}`
                                  : "18:00"
                              }
                              title={`${cls.g6_ten_lop || "Lớp học"} — ${cls.g6_phong_tap || "Studio"}`}
                              mentor={cls.g6_ten_hlv || "HLV Ironcore"}
                              type="class"
                              onAction={() =>
                                handleJoinClass(cls.g6_ma_lop_hoc)
                              }
                            />
                          ))
                      ) : (
                        <p className="text-center text-gray-500 dark:text-[#A1A1AA] text-sm italic">
                          Chưa có lớp học nào sắp tới
                        </p>
                      )}
                    </div>
                  </div>

                  {/* Biểu đồ Recharts */}
                  <div className="bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)] dark:shadow-none dark:bg-white/5 backdrop-blur-xl border border-gray-100 dark:border-white/10 rounded-3xl p-8">
                    <h3 className="font-bold text-xl mb-8 flex items-center">
                      <TrendingUp size={20} className="mr-3 text-[#C9A84C]" />{" "}
                      Tiến trình cơ thể
                    </h3>
                    <div className="h-64 w-full">
                      <ResponsiveContainer width="100%" height="100%">
                        <AreaChart data={metrics}>
                          <defs>
                            <linearGradient
                              id="colorWeight"
                              x1="0"
                              y1="0"
                              x2="0"
                              y2="1"
                            >
                              <stop
                                offset="5%"
                                stopColor="#C9A84C"
                                stopOpacity={0.3}
                              />
                              <stop
                                offset="95%"
                                stopColor="#C9A84C"
                                stopOpacity={0}
                              />
                            </linearGradient>
                          </defs>
                          <CartesianGrid
                            strokeDasharray="3 3"
                            stroke="rgba(255,255,255,0.05)"
                            vertical={false}
                          />
                          <XAxis
                            dataKey="name"
                            stroke="#A1A1AA"
                            fontSize={10}
                            axisLine={false}
                            tickLine={false}
                          />
                          <YAxis hide domain={["dataMin - 2", "dataMax + 2"]} />
                          <Tooltip
                            contentStyle={{
                              backgroundColor: "#1C1C1C",
                              border: "1px solid rgba(255,255,255,0.1)",
                              borderRadius: "12px",
                              fontSize: "12px",
                            }}
                            itemStyle={{ color: "#C9A84C" }}
                          />
                          <Area
                            type="monotone"
                            dataKey="weight"
                            stroke="#C9A84C"
                            strokeWidth={3}
                            fillOpacity={1}
                            fill="url(#colorWeight)"
                          />
                        </AreaChart>
                      </ResponsiveContainer>
                    </div>
                    <div className="mt-8 flex justify-between items-center p-4 bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)] dark:shadow-none dark:bg-white/5 rounded-2xl border border-gray-50 dark:border-white/5">
                      <div>
                        <p className="text-[10px] text-slate-500 uppercase font-bold tracking-widest mb-1">
                          Cân nặng mới nhất
                        </p>
                        <p className="text-xl font-black">
                          {metrics.length > 0
                            ? metrics[metrics.length - 1].weight
                            : "--"}{" "}
                          <span className="text-xs text-slate-500">KG</span>
                        </p>
                      </div>
                      <div className="text-right">
                        <p className="text-[10px] text-slate-500 uppercase font-bold tracking-widest mb-1">
                          Thay đổi gần đây
                        </p>
                        <p
                          className={`text-xl font-black ${metrics.length > 1 && metrics[metrics.length - 1].weight < metrics[0].weight ? "text-emerald-400" : "text-gray-500 dark:text-[#A1A1AA]"}`}
                        >
                          {metrics.length > 1
                            ? (
                                metrics[metrics.length - 1].weight -
                                metrics[0].weight
                              ).toFixed(1)
                            : "0.0"}{" "}
                          <span
                            className={`text-xs ${metrics.length > 1 && metrics[metrics.length - 1].weight < metrics[0].weight ? "text-emerald-400/50" : "text-slate-500"}`}
                          >
                            KG
                          </span>
                        </p>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Bottom Row */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 pb-10">
                  {/* Attendance History */}
                  <div className="bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)] dark:shadow-none dark:bg-white/5 backdrop-blur-xl border border-gray-100 dark:border-white/10 rounded-3xl p-8">
                    <h3 className="font-bold text-xl mb-8 flex items-center">
                      <History size={20} className="mr-3 text-[#C9A84C]" /> Điểm
                      danh gần đây
                    </h3>
                    <div className="space-y-4">
                      {attendance.map((item, idx) => (
                        <div
                          key={item.g6_ma_diem_danh || idx}
                          className="flex items-center justify-between p-4 bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)] dark:shadow-none dark:bg-white/5 hover:bg-black/10 dark:bg-white/10 rounded-2xl transition-all border border-transparent hover:border-gray-50 dark:border-white/5"
                        >
                          <div className="flex items-center space-x-4">
                            <div className="w-10 h-10 bg-[#C9A84C]/10 rounded-full flex items-center justify-center text-[#C9A84C]">
                              <Activity size={18} />
                            </div>
                            <div>
                              <p className="text-sm font-bold text-[#0A0A0A] dark:text-[#F5F5F0]">
                                {item.g6_thoi_gian_vao
                                  ? item.g6_thoi_gian_vao.replace("T", " ")
                                  : "--"}
                              </p>
                              <p className="text-[10px] text-gray-500 dark:text-[#A1A1AA] uppercase tracking-widest font-bold">
                                Check-in
                              </p>
                            </div>
                          </div>
                          <div className="text-right">
                            <p className="text-sm font-bold text-[#0A0A0A] dark:text-[#F5F5F0]">
                              {item.g6_thoi_gian_ra
                                ? item.g6_thoi_gian_ra.replace("T", " ")
                                : "Đang tập"}
                            </p>
                            <p className="text-[10px] text-gray-500 dark:text-[#A1A1AA] uppercase tracking-widest font-bold">
                              Check-out
                            </p>
                          </div>
                        </div>
                      ))}
                      {attendance.length === 0 && (
                        <p className="text-center text-gray-500 dark:text-[#A1A1AA] text-sm italic">
                          Chưa có dữ liệu điểm danh
                        </p>
                      )}
                    </div>
                  </div>

                  {/* Trainer Card */}
                  <div className="bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)] dark:shadow-none dark:bg-white/5 backdrop-blur-xl border border-gray-100 dark:border-white/10 rounded-3xl p-8 relative overflow-hidden group">
                    <div className="absolute top-0 right-0 p-8 opacity-5 group-hover:rotate-12 transition-transform duration-500">
                      <Zap size={120} className="text-[#C9A84C]" />
                    </div>
                    <h3 className="font-bold text-xl mb-8 flex items-center">
                      <User size={20} className="mr-3 text-[#C9A84C]" /> Huấn
                      luyện viên cá nhân
                    </h3>
                    <div className="flex flex-col items-center py-6 text-center">
                      {pts.active ? (
                        <>
                          <div className="relative mb-6">
                            <img
                              src={
                                pts.active.g6_hinh_anh ||
                                "https://ui-avatars.com/api/?name=" +
                                  encodeURIComponent(
                                    pts.active.g6_ten_hlv || "PT",
                                  ) +
                                  "&background=C9A84C&color=000"
                              }
                              className="w-24 h-24 rounded-full object-cover border-4 border-[#C9A84C]/20 shadow-[0_0_30px_rgba(201,168,76,0.2)]"
                            />
                            <div className="absolute bottom-1 right-1 w-5 h-5 bg-[#C9A84C] rounded-full border-4 border-[#0A0A0A]"></div>
                          </div>
                          <h4 className="text-2xl font-black">
                            {pts.active.g6_ten_hlv}
                          </h4>
                          <p className="text-[#C9A84C] text-sm font-bold tracking-widest uppercase mt-2 mb-8">
                            {pts.active.g6_chuyen_mon || "Fitness Expert"}
                          </p>

                          <div className="flex space-x-4 w-full max-w-xs relative z-10">
                            <button
                              onClick={() => setShowChat(true)}
                              className="flex-1 bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)] dark:shadow-none dark:bg-white/5 hover:bg-black/10 dark:bg-white/10 border border-gray-100 dark:border-white/10 py-3 rounded-2xl flex items-center justify-center space-x-2 transition-all font-bold text-sm"
                            >
                              <MessageSquare size={18} />
                              <span>Nhắn tin</span>
                            </button>
                            <button
                              onClick={() =>
                                handleBookPT(pts.active.g6_ma_dang_ky_pt)
                              }
                              className="flex-1 bg-[#C9A84C] hover:bg-[#E5C76B] text-[#0A0A0A] py-3 rounded-2xl flex items-center justify-center space-x-2 transition-all font-bold text-sm shadow-[0_0_20px_rgba(201,168,76,0.3)]"
                            >
                              <Calendar size={18} />
                              <span>Đặt lịch</span>
                            </button>
                          </div>
                        </>
                      ) : (
                        <div className="py-10">
                          <UserCircle2
                            size={64}
                            className="mx-auto text-slate-700 mb-6"
                          />
                          <p className="text-slate-400 mb-8 italic">
                            Bạn chưa đăng ký HLV cá nhân
                          </p>
                          <button
                            onClick={() => setActiveTab("pt")}
                            className="bg-[#C9A84C] text-[#0A0A0A] px-8 py-3 rounded-2xl font-black uppercase tracking-widest hover:bg-[#E5C76B] transition-all"
                          >
                            Tìm Coach Ngay
                          </button>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              </>
            )}
          </>
        )}

        {/* QR Modal */}
        <AnimatePresence>
          {showQR && (
            <div className="fixed inset-0 z-[100] flex items-center justify-center p-4">
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                onClick={() => setShowQR(false)}
                className="absolute inset-0 bg-white/80 dark:bg-black/80 backdrop-blur-md"
              />
              <motion.div
                initial={{ scale: 0.9, opacity: 0, y: 20 }}
                animate={{ scale: 1, opacity: 1, y: 0 }}
                exit={{ scale: 0.9, opacity: 0, y: 20 }}
                className="bg-white dark:bg-[#1C1C1C] border border-[#C9A84C]/30 rounded-[40px] p-10 max-w-sm w-full relative z-10 text-center shadow-[0_0_50px_rgba(201,168,76,0.2)]"
              >
                <div className="mb-6">
                  <h3 className="text-2xl font-black text-[#C9A84C] tracking-widest uppercase mb-2">
                    Member QR
                  </h3>
                  <p className="text-slate-500 text-xs font-bold uppercase tracking-widest">
                    Dùng để điểm danh tại quầy
                  </p>
                </div>
                {/* QR Code Image */}
                <div className="bg-white p-6 rounded-3xl mb-8 shadow-inner flex justify-center">
                  <img
                    src={
                      profile.g6_ma_nguoi_dung
                        ? generateQrSvg(
                            profile.g6_ma_qr ||
                              String(profile.g6_ma_nguoi_dung),
                            250,
                          )
                        : ""
                    }
                    className="w-60 h-60"
                    alt="Member QR"
                  />
                </div>
                <div className="space-y-2 mb-8">
                  <p className="text-xl font-black">{profile.g6_ho_ten}</p>
                  <p className="text-[#C9A84C] text-sm font-bold tracking-widest">
                    {profile.g6_ma_qr || `ID: ${profile.g6_ma_nguoi_dung}`}
                  </p>
                </div>

                <button
                  onClick={() => setShowQR(false)}
                  className="w-full bg-[#C9A84C] text-[#0A0A0A] py-4 rounded-2xl font-black uppercase tracking-widest hover:bg-[#E5C76B] transition-all"
                >
                  Đóng
                </button>
              </motion.div>
            </div>
          )}
        </AnimatePresence>

        {/* Chat Modal */}
        <AnimatePresence>
          {showChat && pts.active && (
            <div className="fixed inset-0 z-[100] flex items-center justify-center p-4">
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                onClick={() => setShowChat(false)}
                className="absolute inset-0 bg-white/80 dark:bg-black/80 backdrop-blur-md"
              />
              <motion.div
                initial={{ scale: 0.9, opacity: 0, y: 20 }}
                animate={{ scale: 1, opacity: 1, y: 0 }}
                exit={{ scale: 0.9, opacity: 0, y: 20 }}
                className="bg-white dark:bg-[#1C1C1C] border border-[#C9A84C]/30 rounded-3xl w-full max-w-md relative z-10 shadow-[0_0_50px_rgba(201,168,76,0.2)] flex flex-col h-[600px]"
              >
                {/* Chat Header */}
                <div className="p-4 border-b border-gray-100 dark:border-white/10 flex items-center space-x-4">
                  <img
                    src={
                      pts.active.g6_hinh_anh ||
                      "https://ui-avatars.com/api/?name=" +
                        encodeURIComponent(pts.active.g6_ten_hlv || "PT") +
                        "&background=C9A84C&color=000"
                    }
                    className="w-12 h-12 rounded-full object-cover border border-[#C9A84C]"
                  />
                  <div className="flex-1">
                    <h3 className="font-bold text-[#0A0A0A] dark:text-[#F5F5F0]">
                      {pts.active.g6_ten_hlv}
                    </h3>
                    <p className="text-xs text-emerald-400 font-medium flex items-center">
                      <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 mr-1.5"></span>{" "}
                      Online
                    </p>
                  </div>
                  <button
                    onClick={() => setShowChat(false)}
                    className="w-8 h-8 rounded-full bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)] dark:shadow-none dark:bg-white/5 hover:bg-black/10 dark:bg-white/10 flex items-center justify-center text-gray-500 dark:text-[#A1A1AA] hover:text-[#0A0A0A] dark:text-[#F5F5F0]"
                  >
                    ✕
                  </button>
                </div>

                {/* Chat Body */}
                <div className="flex-1 p-4 overflow-y-auto custom-scrollbar flex flex-col space-y-4">
                  <div className="text-center">
                    <span className="text-[10px] text-gray-500 dark:text-[#A1A1AA] uppercase font-bold tracking-widest bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)] dark:shadow-none dark:bg-white/5 px-3 py-1 rounded-full">
                      Hôm nay
                    </span>
                  </div>
                  <div className="flex items-start space-x-2">
                    <img
                      src={
                        pts.active.g6_hinh_anh ||
                        "https://ui-avatars.com/api/?name=" +
                          encodeURIComponent(pts.active.g6_ten_hlv || "PT") +
                          "&background=C9A84C&color=000"
                      }
                      className="w-8 h-8 rounded-full object-cover"
                    />
                    <div className="bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)] dark:shadow-none dark:bg-white/5 border border-gray-100 dark:border-white/10 rounded-2xl rounded-tl-sm p-3 max-w-[80%]">
                      <p className="text-sm text-[#0A0A0A] dark:text-[#F5F5F0]">
                        Chào{" "}
                        {profile.g6_ho_ten
                          ? profile.g6_ho_ten.split(" ").pop()
                          : "bạn"}
                        , hôm nay chúng ta tập lưng xô nhé. Nhớ khởi động kỹ
                        trước khi tới phòng nha! 💪
                      </p>
                      <p className="text-[10px] text-gray-500 dark:text-[#A1A1AA] text-right mt-1">
                        08:30
                      </p>
                    </div>
                  </div>
                  <div className="flex items-start space-x-2 flex-row-reverse space-x-reverse">
                    <div className="bg-[#C9A84C] text-[#0A0A0A] rounded-2xl rounded-tr-sm p-3 max-w-[80%] shadow-[0_5px_15px_rgba(201,168,76,0.2)]">
                      <p className="text-sm font-medium">
                        Dạ vâng coach. Khoảng 15p nữa em tới ạ.
                      </p>
                      <p className="text-[10px] text-[#0A0A0A]/60 text-right mt-1">
                        08:32
                      </p>
                    </div>
                  </div>
                </div>

                {/* Chat Input */}
                <div className="p-4 border-t border-gray-100 dark:border-white/10 flex items-center space-x-2">
                  <button className="w-10 h-10 rounded-full bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)] dark:shadow-none dark:bg-white/5 hover:bg-black/10 dark:bg-white/10 flex items-center justify-center text-[#C9A84C] transition-colors">
                    <Plus size={20} />
                  </button>
                  <input
                    type="text"
                    placeholder="Nhập tin nhắn..."
                    className="flex-1 bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)] dark:shadow-none dark:bg-white/5 border border-gray-100 dark:border-white/10 rounded-full px-4 py-2 text-sm text-[#0A0A0A] dark:text-[#F5F5F0] placeholder:text-gray-500 dark:text-[#A1A1AA] focus:outline-none focus:border-[#C9A84C]/50 transition-colors"
                  />
                  <button
                    onClick={handleFeatureInDev}
                    className="w-10 h-10 rounded-full bg-[#C9A84C] hover:bg-[#E5C76B] flex items-center justify-center text-[#0A0A0A] transition-colors shadow-[0_0_15px_rgba(201,168,76,0.3)]"
                  >
                    <svg
                      width="18"
                      height="18"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2.5"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    >
                      <line x1="22" y1="2" x2="11" y2="13"></line>
                      <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                    </svg>
                  </button>
                </div>
              </motion.div>
            </div>
          )}
        </AnimatePresence>
      </main>

      <style
        dangerouslySetInnerHTML={{
          __html: `
 .custom-scrollbar::-webkit-scrollbar { width: 4px; }
 .custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
 .custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(201, 168, 76, 0.2); border-radius: 10px; }
 .custom-scrollbar::-webkit-scrollbar-thumb:hover { background: rgba(201, 168, 76, 0.4); }
 `,
        }}
      />
    </div>
  );
};

// --- Sub-components ---

const NavItem = ({ icon, label, active, onClick }) => (
  <button
    onClick={onClick}
    className={`w-full flex items-center space-x-4 px-6 py-4 rounded-2xl transition-all duration-300 relative group ${active ? "text-[#C9A84C]" : "text-gray-500 dark:text-[#A1A1AA] hover:text-[#0A0A0A] dark:text-[#F5F5F0] hover:bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)] dark:shadow-none dark:bg-white/5"}`}
  >
    {active && (
      <motion.div
        layoutId="activeNav"
        className="absolute inset-0 bg-[#C9A84C]/10 border border-[#C9A84C]/20 rounded-2xl"
      />
    )}
    <div
      className={`relative z-10 transition-transform duration-300 group-hover:scale-110 ${active ? "text-[#C9A84C] drop-shadow-[0_0_8px_rgba(201,168,76,0.5)]" : ""}`}
    >
      {icon}
    </div>
    <span className="relative z-10 font-bold text-sm uppercase tracking-widest">
      {label}
    </span>
  </button>
);

const StatCard = ({ title, value, sub, icon, cyan }) => (
  <div
    className={`bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)] dark:shadow-none dark:bg-white/5 backdrop-blur-xl border border-gray-100 dark:border-white/10 p-6 rounded-3xl relative overflow-hidden group hover:border-white/20 transition-all ${cyan ? "shadow-[0_0_30px_rgba(201,168,76,0.05)]" : ""}`}
  >
    <div className="flex justify-between items-start mb-4">
      <div className="p-3 bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)] dark:shadow-none dark:bg-white/5 rounded-2xl border border-gray-50 dark:border-white/5 group-hover:bg-black/10 dark:bg-white/10 transition-all">
        {icon}
      </div>
      <Info
        size={14}
        className="text-gray-500 dark:text-[#A1A1AA] hover:text-[#0A0A0A] dark:text-[#F5F5F0] cursor-help"
      />
    </div>
    <h4 className="text-gray-500 dark:text-[#A1A1AA] text-[10px] font-bold uppercase tracking-[2px] mb-1">
      {title}
    </h4>
    <div className="text-3xl font-black mb-1 text-[#0A0A0A] dark:text-[#F5F5F0]">
      {value}
    </div>
    <p className="text-[10px] text-gray-500 dark:text-[#A1A1AA] font-medium italic">
      {sub}
    </p>
    <div
      className={`absolute bottom-0 left-0 h-1 bg-gradient-to-r from-transparent via-[#C9A84C]/30 to-transparent w-0 group-hover:w-full transition-all duration-700`}
    ></div>
  </div>
);

const EventItem = ({ time, title, mentor, type, active, onAction }) => (
  <div
    className={`p-4 rounded-2xl border transition-all flex items-center justify-between group ${active ? "bg-[#C9A84C]/10 border-[#C9A84C]/30" : "bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)] dark:shadow-none dark:bg-white/5 border-gray-50 dark:border-white/5 hover:border-gray-100 dark:border-white/10"}`}
  >
    <div className="flex items-center space-x-4">
      <div
        className={`w-2 h-10 rounded-full ${active ? "bg-[#C9A84C]" : "bg-black/10 dark:bg-white/10"}`}
      ></div>
      <div>
        <p
          className={`text-[10px] font-bold uppercase tracking-widest ${active ? "text-[#C9A84C]" : "text-gray-500 dark:text-[#A1A1AA]"}`}
        >
          {time}
        </p>
        <h4 className="text-sm font-black text-[#0A0A0A] dark:text-[#F5F5F0]">
          {title}
        </h4>
        <p className="text-xs text-gray-500 dark:text-[#A1A1AA]">{mentor}</p>
      </div>
    </div>
    <button
      onClick={() => {
        if (onAction) onAction();
      }}
      className={`p-2 rounded-xl border transition-all ${active ? "bg-[#C9A84C] text-[#0A0A0A] border-[#C9A84C]" : "border-gray-100 dark:border-white/10 text-gray-500 dark:text-[#A1A1AA] hover:text-[#0A0A0A] dark:text-[#F5F5F0]"}`}
    >
      <motion.div whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.9 }}>
        <MessageSquare size={16} />
      </motion.div>
    </button>
  </div>
);

const SkeletonLoader = () => (
  <div className="min-h-screen bg-[#FAFAFA] dark:bg-[#0A0A0A] p-8 flex items-center justify-center">
    <div className="flex flex-col items-center space-y-4">
      <div className="w-16 h-16 border-4 border-[#C9A84C]/20 border-t-[#C9A84C] rounded-full animate-spin"></div>
      <p className="text-[#C9A84C] font-header tracking-widest animate-pulse uppercase font-black italic">
        IRONCORE AUTHENTICATING...
      </p>
    </div>
  </div>
);

// --- Sub-Views ---

const HistoryView = ({ history }) => (
  <div className="space-y-6">
    <h2 className="text-3xl font-black tracking-tight flex items-center mb-8">
      <History size={28} className="mr-4 text-[#C9A84C]" />
      Lịch sử <span className="text-[#C9A84C] ml-2">Điểm Danh</span>
    </h2>
    <div className="bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)] dark:shadow-none dark:bg-white/5 backdrop-blur-xl border border-gray-100 dark:border-white/10 rounded-3xl p-8">
      {history.length === 0 ? (
        <p className="text-gray-500 dark:text-[#A1A1AA] italic text-center py-10">
          Bạn chưa có lịch sử điểm danh nào.
        </p>
      ) : (
        <div className="space-y-4">
          {history.map((item, idx) => (
            <div
              key={idx}
              className="flex items-center justify-between p-6 bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)] dark:shadow-none dark:bg-white/5 hover:bg-black/10 dark:bg-white/10 rounded-2xl transition-all border border-transparent hover:border-gray-50 dark:border-white/5"
            >
              <div className="flex items-center space-x-6">
                <div className="w-12 h-12 bg-[#C9A84C]/10 rounded-full flex items-center justify-center text-[#C9A84C]">
                  <Activity size={20} />
                </div>
                <div>
                  <p className="text-lg font-bold text-[#0A0A0A] dark:text-[#F5F5F0]">
                    {item.g6_thoi_gian_vao
                      ? item.g6_thoi_gian_vao.replace("T", " ")
                      : "--"}
                  </p>
                  <p className="text-xs text-gray-500 dark:text-[#A1A1AA] uppercase tracking-widest font-bold mt-1">
                    Giờ Vào (Check-in)
                  </p>
                </div>
              </div>
              <div className="text-right">
                <p className="text-lg font-bold text-[#0A0A0A] dark:text-[#F5F5F0]">
                  {item.g6_thoi_gian_ra
                    ? item.g6_thoi_gian_ra.replace("T", " ")
                    : "Đang tập"}
                </p>
                <p className="text-xs text-gray-500 dark:text-[#A1A1AA] uppercase tracking-widest font-bold mt-1">
                  Giờ Ra (Check-out)
                </p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  </div>
);

const PackagesView = ({ packages, onAction, onSubscribe }) => (
  <div className="space-y-8">
    <h2 className="text-3xl font-black tracking-tight flex items-center mb-8">
      <Package size={28} className="mr-4 text-[#C9A84C]" />
      Gói tập <span className="text-[#C9A84C] ml-2">Của Tôi</span>
    </h2>

    <div className="bg-gradient-to-r from-[#C9A84C]/20 to-transparent p-[1px] rounded-3xl">
      <div className="bg-white dark:bg-[#1C1C1C] rounded-3xl p-8 border border-gray-50 dark:border-white/5 relative overflow-hidden">
        <Zap
          className="absolute top-4 right-4 text-[#C9A84C] opacity-20"
          size={100}
        />
        {packages.active.length > 0 ? (
          packages.active.map((pkg, idx) => (
            <div key={idx} className="relative z-10">
              <h3 className="text-2xl font-black mb-2 text-[#C9A84C] uppercase tracking-widest">
                {pkg.g6_ten_goi_tap || "Gói Hội Viên"}
              </h3>
              <p className="text-gray-500 dark:text-[#A1A1AA] mb-6">
                Trạng thái:{" "}
                <span className="text-emerald-400 font-bold">
                  Đang kích hoạt
                </span>
              </p>
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)] dark:shadow-none dark:bg-white/5 p-4 rounded-xl border border-gray-50 dark:border-white/5">
                  <p className="text-[10px] text-gray-500 dark:text-[#A1A1AA] uppercase font-bold tracking-widest mb-1">
                    Ngày đăng ký
                  </p>
                  <p className="font-bold">{pkg.g6_ngay_bat_dau}</p>
                </div>
                <div className="bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)] dark:shadow-none dark:bg-white/5 p-4 rounded-xl border border-gray-50 dark:border-white/5">
                  <p className="text-[10px] text-gray-500 dark:text-[#A1A1AA] uppercase font-bold tracking-widest mb-1">
                    Ngày hết hạn
                  </p>
                  <p className="font-bold text-[#0A0A0A] dark:text-[#F5F5F0]">
                    {pkg.g6_ngay_het_han}
                  </p>
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="relative z-10 text-center py-8">
            <p className="text-gray-500 dark:text-[#A1A1AA] italic mb-4">
              Bạn chưa đăng ký gói tập nào hoặc gói đã hết hạn.
            </p>
          </div>
        )}
      </div>
    </div>

    <h3 className="text-xl font-bold mt-12 mb-6 uppercase tracking-widest text-gray-500 dark:text-[#A1A1AA]">
      Mua thêm / Gia hạn
    </h3>
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      {packages.available.map((pkg, idx) => (
        <div
          key={idx}
          className="bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)] dark:shadow-none dark:bg-white/5 backdrop-blur-xl border border-gray-100 dark:border-white/10 rounded-2xl p-6 hover:border-[#C9A84C]/50 transition-all flex flex-col h-full group"
        >
          <h4 className="font-black text-lg mb-2 text-[#0A0A0A] dark:text-[#F5F5F0]">
            {pkg.g6_ten_goi}
          </h4>
          <p className="text-2xl font-black text-[#C9A84C] mb-4">
            {parseInt(pkg.g6_gia || pkg.g6_gia_tien || 0).toLocaleString()}đ
          </p>
          <div className="flex-1">
            <p className="text-sm text-gray-500 dark:text-[#A1A1AA] mb-6">
              {pkg.g6_mo_ta || "Gói tập tiêu chuẩn tại hệ thống Ironcore Gym."}
            </p>
          </div>
          <button
            onClick={() => onSubscribe(pkg.g6_ma_goi_tap)}
            className="w-full py-3 bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)] dark:shadow-none dark:bg-white/5 hover:bg-[#C9A84C] hover:text-[#0A0A0A] border border-gray-100 dark:border-white/10 rounded-xl transition-all font-bold text-sm tracking-widest uppercase"
          >
            Đăng ký ngay
          </button>
        </div>
      ))}
      {packages.available.length === 0 && (
        <p className="text-gray-500 dark:text-[#A1A1AA] italic">
          Không có gói tập nào đang mở bán.
        </p>
      )}
    </div>
  </div>
);

const ClassesView = ({ classes, onAction, onJoin }) => (
  <div className="space-y-6">
    <h2 className="text-3xl font-black tracking-tight flex items-center mb-8">
      <Calendar size={28} className="mr-4 text-[#C9A84C]" />
      Lớp Học <span className="text-[#C9A84C] ml-2">Tại Gym</span>
    </h2>
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      {classes.length === 0 ? (
        <p className="text-gray-500 dark:text-[#A1A1AA] italic">
          Chưa có lớp học nào được lên lịch.
        </p>
      ) : (
        classes.map((cls, idx) => (
          <div
            key={idx}
            className="bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)] dark:shadow-none dark:bg-white/5 backdrop-blur-xl border border-gray-100 dark:border-white/10 rounded-3xl p-6 hover:border-white/20 transition-all flex items-start space-x-6 relative overflow-hidden group"
          >
            <div className="w-1.5 absolute top-0 bottom-0 left-0 bg-[#C9A84C]"></div>
            <div className="flex-1 pl-4">
              <div className="flex justify-between items-start mb-2">
                <h3 className="font-black text-xl text-[#0A0A0A] dark:text-[#F5F5F0]">
                  {cls.g6_ten_lop || "Lớp GroupX"}
                </h3>
                <span className="px-3 py-1 bg-[#C9A84C]/20 text-[#C9A84C] rounded-lg text-[10px] font-bold uppercase tracking-widest border border-[#C9A84C]/30">
                  {cls.g6_loai_lop || "Class"}
                </span>
              </div>
              <p className="text-gray-500 dark:text-[#A1A1AA] text-sm mb-4">
                {cls.g6_mo_ta || "Lớp tập nhóm tại hệ thống IronCore Gym"}
              </p>
              <div className="flex justify-between items-center mt-6">
                <div className="flex items-center space-x-2">
                  <div className="w-8 h-8 rounded-full bg-black/10 dark:bg-white/10 flex items-center justify-center text-xs font-bold">
                    <User size={12} />
                  </div>
                  <span className="text-sm font-bold text-gray-500 dark:text-[#A1A1AA]">
                    Tối đa {cls.g6_so_hoc_vien_toi_da || "--"} học viên
                  </span>
                </div>
                <button
                  onClick={() => onJoin(cls.g6_ma_lop_hoc)}
                  className="px-6 py-2 bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)] dark:shadow-none dark:bg-white/5 hover:bg-[#C9A84C] hover:text-[#0A0A0A] border border-gray-100 dark:border-white/10 rounded-xl transition-all font-bold text-xs uppercase tracking-widest"
                >
                  Tham gia
                </button>
              </div>
            </div>
          </div>
        ))
      )}
    </div>
  </div>
);

const PTView = ({ pts, onAction, onSubscribe, onBook }) => (
  <div className="space-y-8">
    <h2 className="text-3xl font-black tracking-tight flex items-center mb-8">
      <UserCircle2 size={28} className="mr-4 text-[#C9A84C]" />
      Huấn Luyện Viên <span className="text-[#C9A84C] ml-2">Của Tôi</span>
    </h2>

    {pts.active ? (
      <div className="bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)] dark:shadow-none dark:bg-white/5 backdrop-blur-xl border border-gray-100 dark:border-white/10 rounded-3xl p-8 relative overflow-hidden flex items-center space-x-8">
        <Zap
          className="absolute top-[-20px] right-[-20px] text-[#C9A84C] opacity-10"
          size={150}
        />
        <img
          src={
            pts.active.g6_hinh_anh ||
            "https://ui-avatars.com/api/?name=" +
              encodeURIComponent(pts.active.g6_ten_hlv || "PT") +
              "&background=C9A84C&color=000"
          }
          className="w-32 h-32 rounded-2xl object-cover border-4 border-[#C9A84C]/20 relative z-10"
        />
        <div className="relative z-10 flex-1">
          <p className="text-[10px] text-gray-500 dark:text-[#A1A1AA] font-bold uppercase tracking-[3px] mb-1">
            HLV CÁ NHÂN
          </p>
          <h3 className="text-3xl font-black text-[#0A0A0A] dark:text-[#F5F5F0] mb-2">
            {pts.active.g6_ten_hlv || "Coach Iron"}
          </h3>
          <p className="text-[#C9A84C] font-bold uppercase tracking-widest text-sm mb-6">
            {pts.active.g6_chuyen_mon || "Fitness Expert"} —{" "}
            {pts.active.g6_ten_goi}
          </p>
          <div className="flex space-x-4">
            <button
              onClick={() => onBook(pts.active.g6_ma_dang_ky_pt)}
              className="px-6 py-3 bg-[#C9A84C] text-[#0A0A0A] font-bold rounded-xl shadow-[0_0_15px_rgba(201,168,76,0.3)] hover:scale-105 transition-transform flex items-center space-x-2"
            >
              <Calendar size={18} />
              <span>Đặt lịch</span>
            </button>
            <button
              onClick={() => setShowChat(true)}
              className="px-6 py-3 bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)] dark:shadow-none dark:bg-white/5 text-[#0A0A0A] dark:text-[#F5F5F0] border border-gray-100 dark:border-white/10 font-bold rounded-xl hover:bg-black/10 dark:bg-white/10 transition-all flex items-center space-x-2"
            >
              <MessageSquare size={18} />
              <span>Nhắn tin</span>
            </button>
          </div>
        </div>
      </div>
    ) : (
      <div className="bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)] dark:shadow-none dark:bg-white/5 backdrop-blur-xl border border-gray-100 dark:border-white/10 rounded-3xl p-8 text-center">
        <p className="text-gray-500 dark:text-[#A1A1AA] italic mb-4">
          Bạn chưa có Huấn Luyện Viên cá nhân.
        </p>
      </div>
    )}

    <h3 className="text-xl font-bold mt-12 mb-6 uppercase tracking-widest text-gray-500 dark:text-[#A1A1AA]">
      Đội ngũ Ironcore Coach
    </h3>
    <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6">
      {pts.available.map((pt, idx) => (
        <div
          key={idx}
          className="bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)] dark:shadow-none dark:bg-white/5 backdrop-blur-xl border border-gray-100 dark:border-white/10 rounded-3xl p-6 text-center hover:border-white/20 transition-all group"
        >
          <img
            src={
              pt.g6_hinh_anh ||
              "https://ui-avatars.com/api/?name=" +
                encodeURIComponent(pt.g6_ho_ten || "PT") +
                "&background=1C1C1C&color=C9A84C"
            }
            className="w-24 h-24 mx-auto rounded-full object-cover border-2 border-gray-100 dark:border-white/10 group-hover:border-[#C9A84C] transition-colors mb-4"
          />
          <h4 className="font-black text-lg text-[#0A0A0A] dark:text-[#F5F5F0] mb-1">
            {pt.g6_ho_ten || "Coach"}
          </h4>
          <p className="text-[#C9A84C] text-xs font-bold uppercase tracking-widest mb-6">
            {pt.g6_chuyen_mon || "Personal Trainer"}
          </p>
          <button
            onClick={() => onSubscribe(pt.g6_ma_hlv)}
            className="w-full py-2 bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)] dark:shadow-none dark:bg-white/5 hover:bg-[#C9A84C] hover:text-[#0A0A0A] border border-gray-100 dark:border-white/10 rounded-xl transition-all font-bold text-xs uppercase tracking-widest"
          >
            Đăng ký
          </button>
        </div>
      ))}
      {pts.available.length === 0 && (
        <p className="text-gray-500 dark:text-[#A1A1AA] italic">
          Đang cập nhật danh sách HLV.
        </p>
      )}
    </div>
  </div>
);

export default MemberDashboard;
