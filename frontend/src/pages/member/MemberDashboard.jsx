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
  ShoppingBag,
  ShoppingCart,
  CreditCard,
  Mail,
  MapPin,
  Lock,
  Key,
  Shield,
  Phone,
  Trash2,
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
import { nqtApi, nqtRequireAuth } from "../../js/member/auth";

// Timezone and format helper for naive UTC datetime strings from backend
const formatToLocalTimezone = (dateStr, type = "datetime") => {
  if (!dateStr) return "";
  // If the date string doesn't specify UTC offset, append 'Z' since the backend stores UTC times
  const normalizedStr = dateStr.endsWith("Z") || dateStr.includes("+") || (dateStr.includes("-") && dateStr.lastIndexOf("-") > 7)
    ? dateStr
    : dateStr + "Z";
  const d = new Date(normalizedStr);
  if (isNaN(d.getTime())) return dateStr;
  
  if (type === "time") {
    return d.toLocaleTimeString("vi-VN", {
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    });
  } else if (type === "date") {
    return d.toLocaleDateString("vi-VN", {
      weekday: "long",
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  } else {
    // datetime
    return d.toLocaleString("vi-VN", {
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    });
  }
};

/**
 * IRONCORE GYM - Member Dashboard
 * Aesthetic: Luxury Glassmorphism
 * Theme: Gold / Deep Black
 */

const MemberDashboard = () => {
  const [activeTab, setActiveTab] = useState(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const tabParam = urlParams.get("tab");
    if (tabParam) return tabParam;
    return localStorage.getItem("nqt_member_active_tab") || "dashboard";
  });
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
  
  const [siteConfig, setSiteConfig] = useState({
    g6_ten_website: "G6 GYM",
    g6_logo_url: "",
    g6_favicon_url: ""
  });

  const [isGuest, setIsGuest] = useState(false);
  const [cart, setCart] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem("nqt_cart") || "[]");
    } catch (e) {
      return [];
    }
  });
  const [products, setProducts] = useState([]);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    localStorage.setItem("nqt_cart", JSON.stringify(cart));
  }, [cart]);

  useEffect(() => {
    localStorage.setItem("nqt_member_active_tab", activeTab);
    const url = new URL(window.location.href);
    url.searchParams.set("tab", activeTab);
    window.history.replaceState(null, "", url.toString());
  }, [activeTab]);

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
  // States for real data
  const [profile, setProfile] = useState({});
  const [activePackage, setActivePackage] = useState(null);
  const [attendance, setAttendance] = useState([]);
  const [metrics, setMetrics] = useState([]);

  // Chatbot states
  const [showChatbot, setShowChatbot] = useState(false);
  const [chatbotMessages, setChatbotMessages] = useState([
    {
      id: "welcome",
      sender: "bot",
      text: "Xin chào! Tôi là Trợ lý ảo thông minh của G6 Gym. Hôm nay tôi có thể giúp gì cho bạn? 💪",
      time: new Date().toLocaleTimeString("vi-VN", { hour: "2-digit", minute: "2-digit" }),
    }
  ]);
  const [chatbotInput, setChatbotInput] = useState("");
  const [isChatbotTyping, setIsChatbotTyping] = useState(false);

  const handleSendChatbotMessage = async (textToSend = null) => {
    const text = (textToSend || chatbotInput).trim();
    if (!text) return;

    if (!textToSend) {
      setChatbotInput("");
    }

    const timeString = new Date().toLocaleTimeString("vi-VN", { hour: "2-digit", minute: "2-digit" });
    const userMsg = {
      id: Math.random().toString(),
      sender: "user",
      text: text,
      time: timeString,
    };

    setChatbotMessages((prev) => [...prev, userMsg]);
    setIsChatbotTyping(true);

    try {
      const res = await nqtApi("/api/nqt-chatbot", {
        method: "POST",
        body: JSON.stringify({ message: text }),
      });
      const data = await res.json();
      
      let botResponse = "Không có phản hồi từ trợ lý ảo.";
      let action = null;

      if (data.nqt_thanh_cong && data.nqt_du_lieu) {
        botResponse = data.nqt_du_lieu.text || botResponse;
        action = data.nqt_du_lieu.action || null;
      } else {
        botResponse = data.nqt_thong_diep || botResponse;
      }

      setTimeout(() => {
        const botMsg = {
          id: Math.random().toString(),
          sender: "bot",
          text: botResponse,
          time: new Date().toLocaleTimeString("vi-VN", { hour: "2-digit", minute: "2-digit" }),
          action: action,
        };
        setChatbotMessages((prev) => [...prev, botMsg]);
        setIsChatbotTyping(false);
      }, 600);
    } catch (err) {
      setTimeout(() => {
        const botMsg = {
          id: Math.random().toString(),
          sender: "bot",
          text: "Xin lỗi, đã xảy ra lỗi kết nối với máy chủ của G6 Gym.",
          time: new Date().toLocaleTimeString("vi-VN", { hour: "2-digit", minute: "2-digit" }),
        };
        setChatbotMessages((prev) => [...prev, botMsg]);
        setIsChatbotTyping(false);
      }, 600);
    }
  };

  // Persist chatbot messages per user
  useEffect(() => {
    if (profile.g6_ma_nguoi_dung) {
      const savedMessages = localStorage.getItem(`g6_chatbot_messages_${profile.g6_ma_nguoi_dung}`);
      if (savedMessages) {
        try {
          setChatbotMessages(JSON.parse(savedMessages));
        } catch (e) {
          console.error("Failed to parse saved chatbot messages", e);
        }
      }
    }
  }, [profile.g6_ma_nguoi_dung]);

  useEffect(() => {
    if (profile.g6_ma_nguoi_dung && chatbotMessages.length > 0) {
      localStorage.setItem(`g6_chatbot_messages_${profile.g6_ma_nguoi_dung}`, JSON.stringify(chatbotMessages));
    }
  }, [chatbotMessages, profile.g6_ma_nguoi_dung]);

  const chatbotEndRef = useRef(null);

  useEffect(() => {
    if (showChatbot) {
      const timer = setTimeout(() => {
        chatbotEndRef.current?.scrollIntoView({ behavior: "smooth" });
      }, 80);
      return () => clearTimeout(timer);
    }
  }, [chatbotMessages, isChatbotTyping, showChatbot]);

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
    const hasAuth = nqtRequireAuth();
    if (!hasAuth) return;

    const handlePageShow = () => {
      if (!localStorage.getItem('nqt_token')) {
        window.location.replace('/login');
      }
    };
    window.addEventListener('pageshow', handlePageShow);
    return () => {
      window.removeEventListener('pageshow', handlePageShow);
    };
  }, []);

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
            document.title = `${config.g6_ten_website} | Member Dashboard`;
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
          const resClasses = await fetch("/api/nqt-public/classes");
          if (resClasses.ok) {
            const dataClasses = await resClasses.json();
            if (dataClasses.nqt_thanh_cong) {
              setClasses(dataClasses.nqt_du_lieu || []);
            }
          }
        } catch (e) {}

        setLoading(false);
      } catch (error) {
        setIsGuest(true);
        setProfile({ g6_ho_ten: "Khách vãng lai", g6_email: "guest@g6gym.com" });
        try {
          const resClasses = await fetch("/api/nqt-public/classes");
          if (resClasses.ok) {
            const dataClasses = await resClasses.json();
            if (dataClasses.nqt_thanh_cong) {
              setClasses(dataClasses.g6_danh_sach || dataClasses.nqt_du_lieu || []);
            }
          }
        } catch (e) {}
        setLoading(false);
      }
    };

    fetchRealData();
  }, [isDarkMode]);

  useEffect(() => {
    if (isGuest) {
      const fetchGuestStorefrontData = async () => {
        try {
          const resProds = await fetch("/api/nxv-san-pham");
          if (resProds.ok) {
            const j = await resProds.json();
            setProducts(j.nqt_du_lieu && Array.isArray(j.nqt_du_lieu.g6_danh_sach) ? j.nqt_du_lieu.g6_danh_sach : (Array.isArray(j.nqt_du_lieu) ? j.nqt_du_lieu : []));
          }
          const resPkgs = await fetch("/api/nqt-public/goi-tap");
          if (resPkgs.ok) {
            const j = await resPkgs.json();
            setPackages((prev) => ({ ...prev, available: j.nqt_thanh_cong ? j.g6_danh_sach || j.nqt_du_lieu : [] }));
          }
          const resPt = await fetch("/api/nqt-public/huan-luyen-vien");
          if (resPt.ok) {
            const j = await resPt.json();
            setPts((prev) => ({ ...prev, available: j.nqt_thanh_cong ? j.g6_danh_sach || j.g6_du_lieu || j.nqt_du_lieu : [] }));
          }
        } catch (e) {
          console.error(e);
        }
      };
      fetchGuestStorefrontData();
    }
  }, [isGuest]);

  useEffect(() => {
    if (activeTab === "dashboard") return;
    const fetchTabData = async () => {
      setTabLoading(true);
      try {
        if (activeTab === "history") {
          if (isGuest) return;
          const res = await nqtApi("/api/nqt-hoi-vien/diem-danh");
          const data = await res.json();
          if (data.nqt_thanh_cong) setFullHistory(data.nqt_du_lieu || []);
        } else if (activeTab === "packages") {
          let myPkgs = [];
          if (!isGuest) {
            try {
              const resMyPkgs = await nqtApi("/api/nqt-dang-ky-goi-tap");
              const dataMy = await resMyPkgs.json();
              if (dataMy.nqt_thanh_cong) myPkgs = dataMy.nqt_du_lieu?.g6_danh_sach || dataMy.nqt_du_lieu || [];
            } catch (e) {}
          }
          const resAllPkgs = await fetch("/api/nqt-public/goi-tap");
          const dataAll = await resAllPkgs.json();
          setPackages({
            active: myPkgs,
            available: dataAll.nqt_thanh_cong ? dataAll.nqt_du_lieu : [],
          });
        } else if (activeTab === "classes") {
          const res = await fetch("/api/nqt-public/classes");
          const data = await res.json();
          if (data.nqt_thanh_cong) setClasses(data.g6_danh_sach || data.nqt_du_lieu || []);
        } else if (activeTab === "pt") {
          let myPt = null;
          if (!isGuest) {
            try {
              const resMyPt = await nqtApi("/api/nxv-dang-ky-pt");
              const dataMy = await resMyPt.json();
              if (dataMy.nqt_thanh_cong) {
                const list =
                  dataMy.nqt_du_lieu?.g6_danh_sach || dataMy.nqt_du_lieu;
                if (list && list.length > 0) myPt = list[0];
              }
            } catch (e) {}
          }
          const resAllPt = await fetch("/api/nqt-public/huan-luyen-vien");
          const dataAll = await resAllPt.json();
          setPts({
            active: myPt,
            available: dataAll.nqt_thanh_cong ? dataAll.nqt_du_lieu : [],
          });
        } else if (activeTab === "shop") {
          const res = await fetch("/api/nxv-san-pham");
          if (res.ok) {
            const j = await res.json();
            const list = j.nqt_du_lieu && Array.isArray(j.nqt_du_lieu.g6_danh_sach) ? j.nqt_du_lieu.g6_danh_sach : (Array.isArray(j.nqt_du_lieu) ? j.nqt_du_lieu : (Array.isArray(j) ? j : []));
            setProducts(list);
          }
        } else if (activeTab === "orders") {
          let url = "/api/nqt-don-hang";
          if (isGuest) {
            const guestOrders = JSON.parse(localStorage.getItem("nqt_guest_orders") || "[]");
            if (guestOrders.length > 0) {
              url += `?g6_ma_don_hang_list=${guestOrders.join(",")}`;
            } else {
              setOrders([]);
              setTabLoading(false);
              return;
            }
          }
          const res = await fetch(url, {
            headers: {
              ...(localStorage.getItem("nqt_token") ? { Authorization: `Bearer ${localStorage.getItem("nqt_token")}` } : {})
            }
          });
          if (res.ok) {
            const j = await res.json();
            const list = Array.isArray(j.nqt_du_lieu?.g6_danh_sach) ? j.nqt_du_lieu.g6_danh_sach : (Array.isArray(j.nqt_du_lieu) ? j.nqt_du_lieu : (Array.isArray(j) ? j : []));
            setOrders(list.sort((a, b) => new Date(b.g6_ngay_tao) - new Date(a.g6_ngay_tao)));
          }
        }
      } catch (e) {
        console.error("Fetch Error:", e);
      }
      setTabLoading(false);
    };
    fetchTabData();
  }, [activeTab, isGuest]);

  const handleSubscribePackage = async (pkgId) => {
    if (isGuest) {
      showToast("info", "Vui lòng đăng nhập để đăng ký gói tập!");
      return;
    }
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
    if (isGuest) {
      showToast("info", "Vui lòng đăng nhập để đăng ký HLV!");
      return;
    }
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
    if (isGuest) {
      showToast("info", "Vui lòng đăng nhập để tham gia lớp học!");
      return;
    }
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
    if (isGuest) {
      showToast("info", "Vui lòng đăng nhập để đặt lịch PT!");
      return;
    }
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
          <a href="/home" className="block hover:opacity-85 transition-opacity">
            {siteConfig.g6_logo_url ? (
              <img src={siteConfig.g6_logo_url} className="mx-auto max-h-16 object-contain" alt="Logo" />
            ) : (
              <h1 className="text-3xl font-black tracking-[4px] text-[#C9A84C] font-['Cormorant_Garamond']">
                {(siteConfig.g6_ten_website || "G6 GYM").toUpperCase()}
              </h1>
            )}
          </a>
          <p className="text-[10px] uppercase tracking-[3px] text-gray-500 dark:text-[#A1A1AA] font-bold mt-2">
            Hội viên Portal
          </p>
        </div>

        <div className="px-6 py-4">
          <div className="bg-gradient-to-br from-white to-gray-50/50 dark:from-white/[0.04] dark:to-white/[0.01] shadow-[0_8px_32px_0_rgba(0,0,0,0.04)] dark:shadow-none rounded-2xl p-4 border border-gray-100 dark:border-white/10 group transition-all duration-300 hover:shadow-[0_8px_30px_rgb(197,160,89,0.06)] hover:border-[#C9A84C]/20">
            <div className="flex items-center space-x-3">
              <img
                src={
                  profile.g6_anh_the ||
                  "https://ui-avatars.com/api/?name=" +
                    encodeURIComponent(profile.g6_ho_ten || "HV") +
                    "&background=C9A84C&color=000"
                }
                className="w-12 h-12 rounded-xl object-cover border border-[#C9A84C]/20 shadow-sm"
              />
              <div className="overflow-hidden">
                <h3 className="font-bold text-sm leading-tight text-slate-800 dark:text-[#F5F5F0] truncate">
                  {profile.g6_ho_ten || "Hội viên"}
                </h3>
                <p className="text-[10px] text-slate-400 dark:text-[#A1A1AA] font-mono mt-1">
                  {isGuest ? "GUEST USER" : `ID: #${String(profile.g6_ma_nguoi_dung).padStart(5, '0')}`}
                </p>
              </div>
            </div>
            {!isGuest ? (
              <>
                <div className="border-t border-gray-100 dark:border-white/5 my-3"></div>
                <button
                  onClick={() => setShowQR(true)}
                  className="w-full flex items-center justify-between px-3 py-2 bg-[#C9A84C]/5 hover:bg-[#C9A84C]/10 border border-[#C9A84C]/20 hover:border-[#C9A84C]/50 rounded-xl transition-all duration-300 group/qr active:scale-[0.98]"
                >
                  <div className="flex items-center space-x-2">
                    <QrCode size={16} className="text-[#C9A84C] group-hover/qr:rotate-6 transition-transform" />
                    <span className="text-[10px] font-bold text-[#C9A84C] tracking-wider uppercase font-caps">
                      Mã QR Check-in
                    </span>
                  </div>
                  <div className="w-7 h-7 rounded bg-white p-0.5 shadow-sm overflow-hidden flex items-center justify-center transition-transform group-hover/qr:scale-105">
                    <img
                      src={
                        profile.g6_ma_nguoi_dung
                          ? generateQrSvg(
                              profile.g6_ma_qr || String(profile.g6_ma_nguoi_dung),
                              28,
                            )
                          : ""
                      }
                      className="w-full h-full object-contain"
                      alt="QR"
                    />
                  </div>
                </button>
              </>
            ) : (
              <a
                href="/login"
                className="w-full mt-3 py-2.5 bg-[#C9A84C] text-[#0A0A0A] hover:bg-black hover:text-[#C9A84C] border border-[#C9A84C] rounded-xl font-bold text-[10px] tracking-widest uppercase flex items-center justify-center transition-all no-underline shadow-[0_4px_15px_rgba(201,168,76,0.15)]"
              >
                Đăng nhập ngay
              </a>
            )}
          </div>
        </div>

        <nav className="flex-1 px-4 space-y-1 overflow-y-auto max-h-[calc(100vh-280px)] custom-scrollbar">
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
          <NavItem
            icon={<ShoppingBag size={20} />}
            label="Cửa hàng"
            active={activeTab === "shop"}
            onClick={() => setActiveTab("shop")}
          />
          <NavItem
            icon={<ShoppingCart size={20} />}
            label="Giỏ hàng"
            active={activeTab === "cart"}
            onClick={() => setActiveTab("cart")}
          />
          <NavItem
            icon={<CreditCard size={20} />}
            label="Đơn hàng"
            active={activeTab === "orders"}
            onClick={() => setActiveTab("orders")}
          />
          <NavItem
            icon={<User size={20} />}
            label="Cá nhân"
            active={activeTab === "profile"}
            onClick={() => setActiveTab("profile")}
          />
        </nav>

        <div className="p-4 space-y-2 border-t border-gray-50 dark:border-white/5 ">
          

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

          {isGuest ? (
            <a
              href="/login"
              className="w-full flex items-center space-x-3 px-4 py-3 rounded-xl transition-all font-bold text-xs uppercase tracking-widest text-[#C9A84C] hover:bg-[#C9A84C]/10 no-underline"
            >
              <User className="w-5 h-5" />
              <span>Đăng nhập</span>
            </a>
          ) : (
            <button
              onClick={handleLogout}
              className="w-full flex items-center space-x-3 px-4 py-3 rounded-xl transition-all font-bold text-xs uppercase tracking-widest text-[#ef4444] hover:bg-[#ef4444]/10"
            >
              <LogOut className="w-5 h-5" />
              <span>Đăng xuất</span>
            </button>
          )}
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
            {activeTab === "history" && (
              isGuest ? (
                <LockedScreen
                  title="Lịch Sử Điểm Danh"
                  message="Vui lòng đăng nhập để xem chi tiết thời gian check-in và check-out tập luyện của bạn tại Ironcore Gym."
                />
              ) : (
                <HistoryView history={fullHistory} />
              )
            )}
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
            {activeTab === "shop" && (
              <ShopView
                products={products}
                cart={cart}
                setCart={setCart}
                showToast={showToast}
                setSelectedProduct={setSelectedProduct}
              />
            )}
            {activeTab === "cart" && (
              <CartView
                cart={cart}
                setCart={setCart}
                profile={profile}
                isGuest={isGuest}
                showToast={showToast}
                setActiveTab={setActiveTab}
              />
            )}
            {activeTab === "orders" && (
              <OrdersView
                orders={orders}
                setOrders={setOrders}
                isGuest={isGuest}
                showToast={showToast}
              />
            )}
            {activeTab === "profile" && (
              <ProfileView
                profile={profile}
                isGuest={isGuest}
                showToast={showToast}
                setProfile={setProfile}
              />
            )}

            {activeTab === "dashboard" && (
              isGuest ? (
                <GuestDashboardView
                  products={products}
                  packages={packages}
                  pts={pts}
                  classes={classes}
                  setActiveTab={setActiveTab}
                  setCart={setCart}
                  showToast={showToast}
                />
              ) : (
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
                                  ? formatToLocalTimezone(item.g6_thoi_gian_vao)
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
                                ? formatToLocalTimezone(item.g6_thoi_gian_ra)
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
              )
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

        {/* Product Detail Modal */}
        {selectedProduct && (
          <div
            className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm"
            onClick={() => setSelectedProduct(null)}
          >
            <div
              className="bg-white dark:bg-[#1C1C1C] border border-[#C9A84C]/30 rounded-3xl w-full max-w-2xl overflow-hidden shadow-[0_0_50px_rgba(201,168,76,0.2)] flex flex-col md:flex-row max-h-[85vh]"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="md:w-1/2 bg-gray-50 dark:bg-white/5 flex items-center justify-center p-8 relative">
                <Activity className="w-24 h-24 text-gray-300 dark:text-white/10" />
                <button
                  onClick={() => setSelectedProduct(null)}
                  className="md:hidden absolute top-4 right-4 w-8 h-8 rounded-full bg-white dark:bg-white/5 shadow flex items-center justify-center text-gray-500"
                >
                  ✕
                </button>
              </div>

              <div className="md:w-1/2 p-8 flex flex-col justify-between overflow-y-auto">
                <div>
                  <div className="flex justify-between items-start mb-2 hidden md:flex">
                    <span className="text-[10px] text-gray-500 dark:text-[#A1A1AA] font-bold tracking-widest uppercase">
                      {selectedProduct.g6_thuong_hieu?.g6_ten_thuong_hieu || "Supplement"}
                    </span>
                    <button
                      onClick={() => setSelectedProduct(null)}
                      className="text-gray-500 hover:text-white font-bold"
                    >
                      ✕
                    </button>
                  </div>
                  <h3 className="text-xl font-black text-[#0A0A0A] dark:text-[#F5F5F0] mb-2 leading-snug">
                    {selectedProduct.g6_ten_san_pham}
                  </h3>
                  <div className="text-2xl font-black text-[#9E7A24] dark:text-[#C9A84C] mb-4">
                    {(selectedProduct.g6_gia_ban || 0).toLocaleString("vi-VN")}₫
                  </div>
                  
                  {selectedProduct.g6_doi_tuong_dung && (
                    <div className="text-xs text-gray-500 dark:text-[#A1A1AA] mb-4">
                      <span className="font-bold text-gray-700 dark:text-gray-300 uppercase tracking-wider block mb-1">Phù hợp:</span>
                      {selectedProduct.g6_doi_tuong_dung}
                    </div>
                  )}

                  {selectedProduct.g6_thanh_phan_dinh_duong && Object.keys(selectedProduct.g6_thanh_phan_dinh_duong).length > 0 && (
                    <div className="mb-6">
                      <span className="text-[10px] text-gray-500 dark:text-[#A1A1AA] font-bold tracking-widest uppercase block mb-2">
                        Thành phần dinh dưỡng
                      </span>
                      <div className="grid grid-cols-3 gap-2">
                        {[
                          { k: "calo", l: "Calo" },
                          { k: "protein", l: "Protein" },
                          { k: "tinh_bot", l: "Tinh bột" },
                          { k: "chat_beo", l: "Chất béo" },
                          { k: "bcaa", l: "BCAA" },
                          { k: "creatine", l: "Creatine" }
                        ]
                          .filter((x) => selectedProduct.g6_thanh_phan_dinh_duong["g6_" + x.k])
                          .map((x) => (
                            <div key={x.k} className="bg-gray-50 dark:bg-white/5 border border-gray-100 dark:border-white/10 rounded-xl p-2 text-center">
                              <div className="text-[#9E7A24] dark:text-[#C9A84C] font-mono font-bold text-sm">
                                {selectedProduct.g6_thanh_phan_dinh_duong["g6_" + x.k]}
                              </div>
                              <div className="text-gray-400 text-[8px] font-bold uppercase tracking-wider mt-0.5">{x.l}</div>
                            </div>
                          ))}
                      </div>
                    </div>
                  )}

                  {selectedProduct.g6_mo_ta && (
                    <div className="text-xs text-gray-500 dark:text-[#A1A1AA] leading-relaxed mb-6">
                      <span className="font-bold text-gray-700 dark:text-gray-300 uppercase tracking-wider block mb-1">Mô tả sản phẩm:</span>
                      {selectedProduct.g6_mo_ta}
                    </div>
                  )}
                </div>

                <button
                  onClick={() => {
                    const price = selectedProduct.g6_gia_ban || 0;
                    const variantId = selectedProduct.g6_sku || selectedProduct.g6_ma_san_pham;
                    
                    const newCart = [...cart];
                    const idx = newCart.findIndex((i) => i.id === variantId);
                    if (idx >= 0) {
                      newCart[idx].qty += 1;
                    } else {
                      newCart.push({
                        id: variantId,
                        variantId,
                        name: selectedProduct.g6_ten_san_pham,
                        price,
                        qty: 1,
                      });
                    }
                    setCart(newCart);
                    setSelectedProduct(null);
                    showToast("success", `Đã thêm ${selectedProduct.g6_ten_san_pham} vào giỏ hàng`);
                  }}
                  className="w-full py-3.5 bg-[#C9A84C] text-[#0A0A0A] hover:bg-black hover:text-[#C9A84C] border border-[#C9A84C] rounded-2xl font-black uppercase tracking-widest transition-all text-xs shadow-[0_4px_15px_rgba(201,168,76,0.2)]"
                >
                  Thêm vào giỏ hàng
                </button>
              </div>
            </div>
          </div>
        )}

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

      {/* --- Chatbot virtual assistant widget --- */}
      <div className="fixed bottom-6 right-6 z-[99]">
        {/* Floating Bubble Button */}
        {!showChatbot && (
          <motion.button
            initial={{ scale: 0, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => setShowChatbot(true)}
            className="w-14 h-14 rounded-full bg-[#C9A84C] text-[#0A0A0A] flex items-center justify-center shadow-[0_4px_25px_rgba(201,168,76,0.4)] relative group focus:outline-none"
          >
            {/* Pulsing ring animation */}
            <span className="absolute inset-0 rounded-full bg-[#C9A84C]/40 animate-ping opacity-75"></span>
            <MessageSquare size={26} className="relative z-10 group-hover:rotate-6 transition-transform" />
          </motion.button>
        )}

        {/* Chatbot Window */}
        <AnimatePresence>
          {showChatbot && (
            <motion.div
              initial={{ opacity: 0, y: 50, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: 50, scale: 0.95 }}
              className="bg-white dark:bg-[#121212]/95 backdrop-blur-2xl border border-gray-100 dark:border-white/10 rounded-3xl w-[370px] h-[520px] shadow-[0_12px_40px_rgba(0,0,0,0.15)] dark:shadow-[0_12px_45px_rgba(201,168,76,0.1)] flex flex-col overflow-hidden"
            >
              {/* Chat Header */}
              <div className="p-4 bg-gradient-to-r from-[#2c2d30] via-[#1E1E1E] to-[#2c2d30] border-b border-white/5 flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="w-9 h-9 rounded-xl bg-[#C9A84C]/10 border border-[#C9A84C]/30 flex items-center justify-center text-[#C9A84C]">
                    <Zap size={18} />
                  </div>
                  <div>
                    <h3 className="font-bold text-xs uppercase tracking-wider text-[#C9A84C]">G6 GYM ASSISTANT</h3>
                    <p className="text-[10px] text-emerald-400 font-bold flex items-center mt-0.5">
                      <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 mr-1.5 animate-pulse"></span>
                      Trực tuyến
                    </p>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <button
                    onClick={() => {
                      if (window.confirm("Bạn có chắc chắn muốn xóa lịch sử trò chuyện?")) {
                        const defaultWelcome = [
                          {
                            id: "welcome",
                            sender: "bot",
                            text: "Xin chào! Tôi là Trợ lý ảo thông minh của G6 Gym. Hôm nay tôi có thể giúp gì cho bạn? 💪",
                            time: new Date().toLocaleTimeString("vi-VN", { hour: "2-digit", minute: "2-digit" }),
                          }
                        ];
                        setChatbotMessages(defaultWelcome);
                        if (profile.g6_ma_nguoi_dung) {
                          localStorage.setItem(`g6_chatbot_messages_${profile.g6_ma_nguoi_dung}`, JSON.stringify(defaultWelcome));
                        }
                      }
                    }}
                    title="Xóa lịch sử chat"
                    className="w-7 h-7 rounded-lg bg-white/5 hover:bg-white/10 flex items-center justify-center transition-colors"
                    style={{ color: '#A1A1AA' }}
                    onMouseEnter={(e) => e.currentTarget.style.color = '#F87171'}
                    onMouseLeave={(e) => e.currentTarget.style.color = '#A1A1AA'}
                  >
                    <Trash2 size={13} style={{ color: 'inherit' }} />
                  </button>
                  <button
                    onClick={() => setShowChatbot(false)}
                    className="w-7 h-7 rounded-lg bg-white/5 hover:bg-white/10 flex items-center justify-center transition-colors"
                    style={{ color: '#A1A1AA' }}
                    onMouseEnter={(e) => e.currentTarget.style.color = '#FFFFFF'}
                    onMouseLeave={(e) => e.currentTarget.style.color = '#A1A1AA'}
                  >
                    ✕
                  </button>
                </div>
              </div>

              {/* Chat Body */}
              <div className="flex-1 p-4 overflow-y-auto custom-scrollbar flex flex-col space-y-4 bg-gray-50/50 dark:bg-black/20">
                {chatbotMessages.map((msg) => (
                  <div
                    key={msg.id}
                    className={`flex items-start space-x-2 ${
                      msg.sender === "user" ? "flex-row-reverse space-x-reverse" : ""
                    }`}
                  >
                    {msg.sender === "bot" && (
                      <div className="w-7 h-7 rounded-lg bg-[#C9A84C]/10 border border-[#C9A84C]/20 flex items-center justify-center text-[#C9A84C] shrink-0 text-xs font-bold">
                        G6
                      </div>
                    )}
                    <div className="flex flex-col">
                      <div
                        className={`p-3 rounded-2xl max-w-[250px] shadow-sm text-xs leading-relaxed ${
                          msg.sender === "user"
                            ? "bg-[#C9A84C] text-[#0A0A0A] rounded-tr-none font-medium"
                            : "bg-white dark:bg-white/[0.03] text-slate-800 dark:text-[#F5F5F0] border border-gray-100 dark:border-white/5 rounded-tl-none"
                        }`}
                      >
                        <p>{msg.text}</p>

                        {/* Special Navigation Button within bot response */}
                        {msg.action && (
                          <button
                            onClick={() => {
                              setActiveTab(msg.action.target);
                              showToast("success", `Đã chuyển đến tab ${msg.action.label}`);
                            }}
                            className="mt-2.5 w-full py-1.5 px-3 bg-black/10 hover:bg-black/20 dark:bg-white/10 dark:hover:bg-white/20 rounded-lg text-[10px] font-bold uppercase tracking-wider transition-all flex items-center justify-center space-x-1 text-slate-800 dark:text-white"
                          >
                            <span>{msg.action.label}</span>
                            <ChevronRight size={10} />
                          </button>
                        )}
                      </div>
                      <span
                        className={`text-[9px] text-gray-400 mt-1 ${
                          msg.sender === "user" ? "text-right" : "text-left"
                        }`}
                      >
                        {msg.time}
                      </span>
                    </div>
                  </div>
                ))}

                {/* Bot Typing Indicator */}
                {isChatbotTyping && (
                  <div className="flex items-start space-x-2">
                    <div className="w-7 h-7 rounded-lg bg-[#C9A84C]/10 border border-[#C9A84C]/20 flex items-center justify-center text-[#C9A84C] shrink-0 text-xs font-bold animate-pulse">
                      G6
                    </div>
                    <div className="bg-white dark:bg-white/[0.03] border border-gray-100 dark:border-white/5 rounded-2xl rounded-tl-none p-3 flex space-x-1.5 items-center">
                      <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "0ms" }}></span>
                      <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "150ms" }}></span>
                      <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "300ms" }}></span>
                    </div>
                  </div>
                )}
                <div ref={chatbotEndRef} />
              </div>

              {/* Suggestions Panel */}
              <div className="px-3 py-2 bg-gray-100/50 dark:bg-white/[0.02] border-t border-gray-100 dark:border-white/5 overflow-x-auto whitespace-nowrap flex space-x-2 custom-scrollbar">
                {[
                  { label: "Mua gói tập 🛒", query: "Mua gói tập" },
                  { label: "Đặt lịch PT 📅", query: "Đặt lịch PT" },
                  { label: "Dinh dưỡng 🍏", query: "Tư vấn dinh dưỡng" },
                  { label: "Giờ mở cửa 🕒", query: "Giờ mở cửa" },
                  { label: "Địa chỉ 📍", query: "Địa chỉ phòng tập" },
                ].map((sug, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleSendChatbotMessage(sug.query)}
                    className="inline-block px-3 py-1 bg-white dark:bg-white/5 border border-gray-200/60 dark:border-white/5 rounded-full text-[10px] text-gray-600 dark:text-[#A1A1AA] hover:border-[#C9A84C]/45 hover:text-[#C9A84C] transition-all font-sans"
                  >
                    {sug.label}
                  </button>
                ))}
              </div>

              {/* Chat Input */}
              <form
                onSubmit={(e) => {
                  e.preventDefault();
                  handleSendChatbotMessage();
                }}
                className="p-3 border-t border-gray-100 dark:border-white/5 flex items-center space-x-2 bg-white dark:bg-[#121212]"
              >
                <input
                  type="text"
                  value={chatbotInput}
                  onChange={(e) => setChatbotInput(e.target.value)}
                  placeholder="Nhập câu hỏi của bạn..."
                  className="flex-1 bg-gray-50 dark:bg-white/[0.02] border border-gray-200/60 dark:border-white/5 rounded-xl px-4 py-2.5 text-xs text-[#0A0A0A] dark:text-[#F5F5F0] placeholder-gray-400 focus:outline-none focus:border-[#C9A84C]/50 transition-colors"
                />
                <button
                  type="submit"
                  className="w-9 h-9 rounded-xl bg-[#C9A84C] hover:bg-[#E5C76B] flex items-center justify-center text-[#0A0A0A] transition-colors shadow-sm shrink-0 animate-pulse"
                >
                  <ArrowRight size={16} />
                </button>
              </form>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      <style
        dangerouslySetInnerHTML={{
          __html: `
 .custom-scrollbar::-webkit-scrollbar { width: 4px; height: 4px; }
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
    className={`w-full flex items-center space-x-3.5 px-5 py-3 rounded-xl transition-all duration-300 relative group overflow-hidden ${
      active
        ? "text-[#C9A84C] bg-[#C9A84C]/5 font-bold"
        : "text-gray-500 dark:text-gray-400 hover:text-black dark:hover:text-[#F5F5F0] hover:bg-black/[0.02] dark:hover:bg-white/[0.02]"
    }`}
  >
    {active && (
      <>
        {/* Left glowing gold indicator stripe */}
        <div className="absolute left-0 top-0 bottom-0 w-1 bg-gradient-to-b from-[#C9A84C] to-amber-500 rounded-r-full z-20"></div>
        <motion.div
          layoutId="activeNav"
          className="absolute inset-0 bg-[#C9A84C]/10 rounded-xl"
        />
      </>
    )}
    <div
      className={`relative z-10 transition-transform duration-300 group-hover:scale-105 ${
        active ? "text-[#C9A84C] drop-shadow-[0_0_8px_rgba(201,168,76,0.3)]" : ""
      }`}
    >
      {icon}
    </div>
    <span className="relative z-10 font-bold text-xs uppercase tracking-wider">
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
        ĐANG XÁC THỰC HỘI VIÊN...
      </p>
    </div>
  </div>
);

// --- Sub-Views ---

const HistoryView = ({ history }) => {
  const getDuration = (start, end) => {
    if (!start || !end) return null;
    const s = new Date(start.endsWith("Z") ? start : start + "Z");
    const e = new Date(end.endsWith("Z") ? end : end + "Z");
    const diffMs = e - s;
    if (diffMs <= 0) return null;
    const diffMins = Math.floor(diffMs / 60000);
    const hrs = Math.floor(diffMins / 60);
    const mins = diffMins % 60;
    if (hrs > 0) {
      return `${hrs} giờ ${mins} phút`;
    }
    return `${mins} phút`;
  };

  const formatDate = (dateStr) => {
    return formatToLocalTimezone(dateStr, "date");
  };

  const formatTime = (dateStr) => {
    return formatToLocalTimezone(dateStr, "time");
  };

  // Calculate some stats
  const totalSessions = history.length;
  const sessionsThisWeek = history.filter(item => {
    if (!item.g6_thoi_gian_vao) return false;
    const dateStr = item.g6_thoi_gian_vao;
    const d = new Date(dateStr.endsWith("Z") ? dateStr : dateStr + "Z");
    const diffTime = Math.abs(new Date() - d);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays <= 7;
  }).length;

  let totalMins = 0;
  let sessionsWithDuration = 0;
  history.forEach(item => {
    if (item.g6_thoi_gian_vao && item.g6_thoi_gian_ra) {
      const start = item.g6_thoi_gian_vao;
      const end = item.g6_thoi_gian_ra;
      const diff = new Date(end.endsWith("Z") ? end : end + "Z") - new Date(start.endsWith("Z") ? start : start + "Z");
      if (diff > 0) {
        totalMins += Math.floor(diff / 60000);
        sessionsWithDuration++;
      }
    }
  });
  const avgMins = sessionsWithDuration > 0 ? Math.round(totalMins / sessionsWithDuration) : 0;
  const avgDurationStr = avgMins > 0 ? (avgMins >= 60 ? `${Math.floor(avgMins / 60)}h ${avgMins % 60}m` : `${avgMins} phút`) : "--";

  return (
    <div className="space-y-8">
      {/* Title */}
      <div className="flex justify-between items-center">
        <h2 className="text-3xl font-black tracking-tight flex items-center">
          <History size={28} className="mr-4 text-[#C9A84C] drop-shadow-[0_0_15px_rgba(201,168,76,0.4)]" />
          Lịch sử <span className="text-[#C9A84C] ml-2 font-['Cormorant_Garamond'] italic">Điểm Danh</span>
        </h2>
      </div>

      {/* Stats row inside history tab */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)] dark:shadow-none dark:bg-white/5 backdrop-blur-xl border border-gray-100 dark:border-white/10 p-6 rounded-3xl relative overflow-hidden group">
          <h4 className="text-gray-500 dark:text-[#A1A1AA] text-[10px] font-bold uppercase tracking-[2px] mb-1">
            Tổng số buổi tập
          </h4>
          <div className="text-3xl font-black text-[#0A0A0A] dark:text-[#F5F5F0]">
            {totalSessions} <span className="text-xs text-gray-500 dark:text-[#A1A1AA] font-normal uppercase tracking-wider ml-1">Buổi</span>
          </div>
          <p className="text-[10px] text-gray-500 dark:text-[#A1A1AA] font-medium mt-1">
            Tất cả các lượt check-in ghi nhận
          </p>
        </div>

        <div className="bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)] dark:shadow-none dark:bg-white/5 backdrop-blur-xl border border-gray-100 dark:border-white/10 p-6 rounded-3xl relative overflow-hidden group">
          <h4 className="text-gray-500 dark:text-[#A1A1AA] text-[10px] font-bold uppercase tracking-[2px] mb-1">
            Tập luyện tuần này
          </h4>
          <div className="text-3xl font-black text-[#C9A84C]">
            {sessionsThisWeek} <span className="text-xs text-[#C9A84C]/80 font-normal uppercase tracking-wider ml-1">Buổi</span>
          </div>
          <p className="text-[10px] text-gray-500 dark:text-[#A1A1AA] font-medium mt-1">
            Ghi nhận trong 7 ngày qua
          </p>
        </div>

        <div className="bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)] dark:shadow-none dark:bg-white/5 backdrop-blur-xl border border-gray-100 dark:border-white/10 p-6 rounded-3xl relative overflow-hidden group">
          <h4 className="text-gray-500 dark:text-[#A1A1AA] text-[10px] font-bold uppercase tracking-[2px] mb-1">
            Thời lượng trung bình
          </h4>
          <div className="text-3xl font-black text-[#0A0A0A] dark:text-[#F5F5F0]">
            {avgDurationStr}
          </div>
          <p className="text-[10px] text-gray-500 dark:text-[#A1A1AA] font-medium mt-1">
            Tính trên các buổi hoàn thành
          </p>
        </div>
      </div>

      {/* Main List */}
      <div className="bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)] dark:shadow-none dark:bg-white/5 backdrop-blur-xl border border-gray-100 dark:border-white/10 rounded-3xl p-8">
        {history.length === 0 ? (
          <div className="text-center py-16">
            <History size={48} className="mx-auto text-gray-300 dark:text-white/10 mb-4" />
            <p className="text-gray-500 dark:text-[#A1A1AA] italic">
              Bạn chưa có lịch sử điểm danh nào.
            </p>
          </div>
        ) : (
          <div className="relative border-l-2 border-dashed border-[#C9A84C]/30 ml-4 md:ml-6 space-y-8 py-4">
            {history.map((item, idx) => {
              const dur = getDuration(item.g6_thoi_gian_vao, item.g6_thoi_gian_ra);
              const dateVal = item.g6_thoi_gian_vao || item.g6_thoi_gian_ra;
              const dateStr = formatDate(dateVal);
              const checkinTime = formatTime(item.g6_thoi_gian_vao);
              const checkoutTime = formatTime(item.g6_thoi_gian_ra);
              const isTraining = !item.g6_thoi_gian_ra;

              return (
                <div key={idx} className="relative pl-8 md:pl-10 group">
                  {/* Timeline dot */}
                  <div className={`absolute left-[-9px] top-1.5 w-4 h-4 rounded-full border-2 border-[#0A0A0A] dark:border-[#1C1C1C] transition-all duration-300 group-hover:scale-125 ${isTraining ? 'bg-emerald-400 shadow-[0_0_10px_#34d399]' : 'bg-[#C9A84C] group-hover:bg-[#E5C76B]'}`}></div>

                  <div className="bg-[#FAFAFA] dark:bg-white/5 border border-gray-100 dark:border-white/10 rounded-3xl p-6 hover:border-[#C9A84C]/30 transition-all shadow-[0_4px_20px_rgba(0,0,0,0.02)] flex flex-col md:flex-row md:items-center justify-between gap-4">
                    <div className="space-y-2">
                      <span className="text-[10px] bg-[#C9A84C]/10 border border-[#C9A84C]/20 text-[#C9A84C] font-bold uppercase tracking-wider px-3 py-1 rounded-full">
                        {dateStr}
                      </span>
                      <h4 className="text-base font-black text-[#0A0A0A] dark:text-[#F5F5F0] mt-2 flex items-center gap-2">
                        <span>Check-in:</span>
                        <span className="text-[#C9A84C] font-mono">{checkinTime}</span>
                      </h4>
                      {dur && (
                        <p className="text-xs text-gray-500 dark:text-[#A1A1AA] flex items-center gap-1.5 font-bold">
                          <Activity size={12} className="text-[#C9A84C]" />
                          Thời lượng tập: <span className="text-[#0A0A0A] dark:text-[#F5F5F0]">{dur}</span>
                        </p>
                      )}
                    </div>

                    <div className="flex flex-col items-start md:items-end justify-between gap-2">
                      {isTraining ? (
                        <span className="px-3.5 py-1.5 bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-[10px] font-bold uppercase tracking-widest rounded-full animate-pulse flex items-center gap-1.5">
                          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping"></span>
                          Đang tập luyện
                        </span>
                      ) : (
                        <div className="space-y-1 text-left md:text-right">
                          <p className="text-[10px] text-gray-500 dark:text-[#A1A1AA] uppercase tracking-wider font-bold">Check-out</p>
                          <p className="text-sm font-bold text-gray-500 dark:text-[#A1A1AA] font-mono">{checkoutTime}</p>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
};

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
                  className="px-6 py-2 bg-[#C9A84C] text-[#0A0A0A] hover:bg-black hover:text-[#C9A84C] border border-[#C9A84C] rounded-xl transition-all font-bold text-xs uppercase tracking-widest shadow-[0_4px_15px_rgba(201,168,76,0.15)]"
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
          <p className="text-[#9E7A24] dark:text-[#C9A84C] font-bold uppercase tracking-widest text-sm mb-6">
            {pts.active.g6_chuyen_mon || "Fitness Expert"} —{" "}
            {pts.active.g6_ten_goi}
          </p>
          <div className="flex space-x-4">
            <button
              onClick={() => onBook(pts.active.g6_ma_dang_ky_pt)}
              className="px-6 py-3 bg-[#C9A84C] text-[#0A0A0A] hover:bg-black hover:text-[#C9A84C] border border-[#C9A84C] font-bold rounded-xl shadow-[0_0_15px_rgba(201,168,76,0.3)] transition-all flex items-center space-x-2"
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
                "&background=F4F4F5&color=C9A84C"
            }
            className="w-24 h-24 mx-auto rounded-full object-cover border-2 border-gray-100 dark:border-white/10 group-hover:border-[#C9A84C] transition-colors mb-4"
          />
          <h4 className="font-black text-lg text-[#0A0A0A] dark:text-[#F5F5F0] mb-1">
            {pt.g6_ho_ten || "Coach"}
          </h4>
          <p className="text-[#9E7A24] dark:text-[#C9A84C] text-xs font-bold uppercase tracking-widest mb-6">
            {pt.g6_chuyen_mon || "Personal Trainer"}
          </p>
          <button
            onClick={() => onSubscribe(pt.g6_ma_hlv)}
            className="w-full py-2 bg-[#C9A84C] text-[#0A0A0A] hover:bg-black hover:text-[#C9A84C] border border-[#C9A84C] rounded-xl transition-all font-bold text-xs uppercase tracking-widest shadow-[0_4px_15px_rgba(201,168,76,0.15)]"
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


// --- Guest & Storefront Components ---

const LockedScreen = ({ title, message }) => (
  <div className="h-full flex flex-col items-center justify-center p-8 text-center bg-white dark:bg-white/5 backdrop-blur-xl border border-gray-100 dark:border-white/10 rounded-3xl relative overflow-hidden max-w-2xl mx-auto my-12 shadow-[0_8px_30px_rgb(0,0,0,0.04)]">
    <div className="absolute inset-0 bg-[#C9A84C]/5 blur-3xl pointer-events-none"></div>
    <div className="w-16 h-16 bg-[#C9A84C]/10 rounded-full flex items-center justify-center text-[#C9A84C] mb-6">
      <ShieldCheck size={32} />
    </div>
    <h3 className="text-2xl font-black mb-4 uppercase tracking-widest text-[#0A0A0A] dark:text-[#F5F5F0]">
      {title}
    </h3>
    <p className="text-gray-500 dark:text-[#A1A1AA] text-sm max-w-md mx-auto mb-8 leading-relaxed">
      {message}
    </p>
    <a
      href="/login"
      className="bg-[#C9A84C] hover:bg-[#E5C76B] text-[#0A0A0A] px-8 py-3.5 rounded-2xl font-black uppercase tracking-widest transition-all shadow-[0_0_30px_rgba(201,168,76,0.3)] no-underline text-xs"
    >
      ĐĂNG NHẬP NGAY
    </a>
  </div>
);

const ShopView = ({
  products,
  cart,
  setCart,
  showToast,
  setSelectedProduct,
}) => {
  const [search, setSearch] = useState("");
  const [selectedCat, setSelectedCat] = useState("");
  const [sort, setSort] = useState("");

  const handleAddToCart = (product, e) => {
    e.stopPropagation();
    const price = product.g6_gia_ban || 0;
    const variantId = product.g6_sku || product.g6_ma_san_pham;
    
    const newCart = [...cart];
    const idx = newCart.findIndex((i) => i.id === variantId);
    if (idx >= 0) {
      newCart[idx].qty += 1;
    } else {
      newCart.push({
        id: variantId,
        variantId,
        name: product.g6_ten_san_pham,
        price,
        image: product.g6_hinh_anh,
        qty: 1,
      });
    }
    setCart(newCart);
    showToast("success", `Đã thêm ${product.g6_ten_san_pham} vào giỏ hàng`);
  };

  const categories = [];
  const seenCats = new Set();
  products.forEach((p) => {
    if (p.g6_danh_muc && !seenCats.has(p.g6_ma_danh_muc)) {
      seenCats.add(p.g6_ma_danh_muc);
      categories.push({
        id: p.g6_ma_danh_muc,
        name: p.g6_danh_muc.g6_ten_danh_muc || "Khác",
      });
    }
  });

  const filtered = products.filter((p) => {
    const matchSearch =
      !search ||
      p.g6_ten_san_pham.toLowerCase().includes(search.toLowerCase());
    const matchCat = !selectedCat || p.g6_ma_danh_muc === selectedCat;
    return matchSearch && matchCat;
  });

  if (sort === "price_asc") {
    filtered.sort(
      (a, b) =>
        (a.g6_gia_ban || 0) - (b.g6_gia_ban || 0),
    );
  } else if (sort === "price_desc") {
    filtered.sort(
      (a, b) =>
        (b.g6_gia_ban || 0) - (a.g6_gia_ban || 0),
    );
  } else if (sort === "name") {
    filtered.sort((a, b) => a.g6_ten_san_pham.localeCompare(b.g6_ten_san_pham));
  }

  return (
    <div className="space-y-6">
      <h2 className="text-3xl font-black tracking-tight flex items-center mb-8">
        <ShoppingBag size={28} className="mr-4 text-[#C9A84C]" />
        Cửa Hàng <span className="text-[#C9A84C] ml-2">Ironcore Supplement</span>
      </h2>

      <div className="flex flex-col md:flex-row md:items-center gap-4 bg-white dark:bg-white/5 border border-gray-100 dark:border-white/10 p-6 rounded-3xl shadow-[0_8px_30px_rgb(0,0,0,0.04)]">
        <div className="relative flex-1 min-w-[200px]">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 w-4 h-4" />
          <input
            type="text"
            placeholder="Tìm sản phẩm..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full bg-[#FAFAFA] dark:bg-white/5 border border-gray-100 dark:border-white/10 rounded-2xl pl-10 pr-4 py-2.5 text-sm text-[#0A0A0A] dark:text-[#F5F5F0] focus:outline-none focus:border-[#C9A84C]/50 transition-colors"
          />
        </div>
        
        <select
          value={sort}
          onChange={(e) => setSort(e.target.value)}
          className="bg-[#FAFAFA] dark:bg-white/5 border border-gray-100 dark:border-white/10 rounded-2xl px-4 py-2.5 text-sm text-gray-500 dark:text-[#A1A1AA] focus:outline-none focus:border-[#C9A84C]/50 transition-colors cursor-pointer"
        >
          <option value="">Sắp xếp</option>
          <option value="price_asc">Giá tăng dần</option>
          <option value="price_desc">Giá giảm dần</option>
          <option value="name">Tên A-Z</option>
        </select>

        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => setSelectedCat("")}
            className={`px-4 py-2 rounded-2xl text-xs font-bold uppercase tracking-wider transition-all ${
              selectedCat === ""
                ? "bg-[#C9A84C] text-[#0A0A0A] shadow-[0_0_15px_rgba(201,168,76,0.3)]"
                : "border border-gray-100 dark:border-white/10 text-gray-500 dark:text-[#A1A1AA] hover:text-[#0A0A0A] dark:hover:text-white"
            }`}
          >
            Tất cả
          </button>
          {categories.map((cat) => (
            <button
              key={cat.id}
              onClick={() => setSelectedCat(cat.id)}
              className={`px-4 py-2 rounded-2xl text-xs font-bold uppercase tracking-wider transition-all ${
                selectedCat === cat.id
                  ? "bg-[#C9A84C] text-[#0A0A0A] shadow-[0_0_15px_rgba(201,168,76,0.3)]"
                  : "border border-gray-100 dark:border-white/10 text-gray-500 dark:text-[#A1A1AA] hover:text-[#0A0A0A] dark:hover:text-white"
              }`}
            >
              {cat.name}
            </button>
          ))}
        </div>
      </div>

      {filtered.length === 0 ? (
        <div className="text-center py-20 bg-white dark:bg-white/5 border border-gray-100 dark:border-white/10 rounded-3xl">
          <Search className="mx-auto w-12 h-12 text-gray-400 mb-4" />
          <p className="text-gray-500 dark:text-[#A1A1AA] italic">Không tìm thấy sản phẩm nào.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {filtered.map((p) => {
            const price = p.g6_gia_ban || 0;
            return (
              <div
                key={p.g6_ma_san_pham}
                onClick={() => setSelectedProduct(p)}
                className="bg-white dark:bg-white/5 border border-gray-100 dark:border-white/10 rounded-3xl overflow-hidden hover:border-[#C9A84C]/50 transition-all flex flex-col group cursor-pointer shadow-[0_8px_30px_rgb(0,0,0,0.04)]"
              >
                <div className="aspect-square bg-gray-50 dark:bg-white/5 flex items-center justify-center relative overflow-hidden">
                  <Activity className="w-16 h-16 text-gray-300 dark:text-white/10 group-hover:scale-110 group-hover:text-[#C9A84C]/50 transition-all duration-500" />
                  {p.g6_hinh_anh && (
                    <img
                      src={p.g6_hinh_anh}
                      className="absolute inset-0 w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                      alt={p.g6_ten_san_pham}
                    />
                  )}
                  {p.g6_la_ban_chay && (
                    <div className="absolute top-4 left-4 bg-orange-500 text-white text-[9px] font-bold uppercase tracking-widest px-2.5 py-1 rounded-full shadow-lg">
                      Hot
                    </div>
                  )}
                  {p.g6_la_noi_bat && (
                    <div className="absolute top-4 right-4 bg-[#C9A84C] text-[#0A0A0A] text-[9px] font-bold uppercase tracking-widest px-2.5 py-1 rounded-full shadow-lg">
                      Nổi bật
                    </div>
                  )}
                </div>
                <div className="p-6 flex flex-col flex-1">
                  <span className="text-[10px] text-gray-500 dark:text-[#A1A1AA] font-bold tracking-widest uppercase mb-1">
                    {p.g6_thuong_hieu?.g6_ten_thuong_hieu || "Supplement"}
                  </span>
                  <h4 className="font-bold text-sm text-[#0A0A0A] dark:text-[#F5F5F0] line-clamp-2 leading-snug group-hover:text-[#C9A84C] transition-colors mb-3 flex-1">
                    {p.g6_ten_san_pham}
                  </h4>
                  <div className="text-xl font-black text-[#C9A84C] mb-4">
                    {price.toLocaleString("vi-VN")}₫
                  </div>
                  <button
                    onClick={(e) => handleAddToCart(p, e)}
                    className="w-full py-2.5 bg-[#C9A84C] text-[#0A0A0A] hover:bg-black hover:text-[#C9A84C] border border-[#C9A84C] rounded-2xl text-xs font-bold uppercase tracking-widest transition-all flex items-center justify-center gap-2 group/btn shadow-[0_4px_15px_rgba(201,168,76,0.15)]"
                  >
                    Thêm vào giỏ
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

const CartView = ({
  cart,
  setCart,
  profile,
  isGuest,
  showToast,
  setActiveTab,
}) => {
  const [hoTen, setHoTen] = useState(profile.g6_ho_ten || "");
  const [sdt, setSdt] = useState(profile.g6_so_dien_thoai || "");
  const [diaChi, setDiaChi] = useState("");
  const [tinh, setTinh] = useState("");
  const [ghiChu, setGhiChu] = useState("");
  const [payMethod, setPayMethod] = useState("tien_mat");
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    if (profile.g6_ho_ten && profile.g6_ho_ten !== "Khách vãng lai") {
      setHoTen(profile.g6_ho_ten);
    } else {
      const guestInfo = JSON.parse(localStorage.getItem("nqt_guest_info") || "{}");
      if (guestInfo.hoTen) setHoTen(guestInfo.hoTen);
      if (guestInfo.sdt) setSdt(guestInfo.sdt);
      if (guestInfo.diaChi) setDiaChi(guestInfo.diaChi);
      if (guestInfo.tinh) setTinh(guestInfo.tinh);
    }
    if (profile.g6_so_dien_thoai) {
      setSdt(profile.g6_so_dien_thoai);
    }
  }, [profile]);

  const updateQty = (idx, delta) => {
    const newCart = [...cart];
    newCart[idx].qty = Math.max(1, newCart[idx].qty + delta);
    setCart(newCart);
  };

  const removeProduct = (idx) => {
    const newCart = [...cart];
    newCart.splice(idx, 1);
    setCart(newCart);
  };

  const subtotal = cart.reduce((acc, item) => acc + item.price * item.qty, 0);

  const handleCheckout = async (e) => {
    e.preventDefault();
    if (!hoTen.trim() || !sdt.trim() || !diaChi.trim()) {
      showToast("error", "Vui lòng điền đầy đủ họ tên, số điện thoại và địa chỉ nhận hàng.");
      return;
    }
    setIsSubmitting(true);
    const token = localStorage.getItem("nqt_token");
    try {
      const res = await fetch("/api/nqt-don-hang", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
        body: JSON.stringify({
          g6_ho_ten_nguoi_nhan: hoTen,
          g6_so_dien_thoai_nguoi_nhan: sdt,
          g6_dia_chi_giao_hang: `${diaChi}, ${tinh}`.trim().replace(/,\s*$/, ""),
          g6_phuong_thuc_thanh_toan: payMethod,
          g6_ghi_chu: ghiChu,
          g6_chi_tiet: cart.map((i) => ({
            g6_ma_bien_the: i.variantId || i.id,
            g6_so_luong: i.qty,
            g6_don_gia: i.price,
            g6_ten_san_pham: i.name,
          })),
          g6_tong_tam_tinh: subtotal,
          g6_phi_van_chuyen: 0,
          g6_tong_thanh_toan: subtotal,
        }),
      });

      if (res.ok) {
        const resData = await res.json();
        const orderId = resData.nqt_du_lieu?.g6_ma_don_hang;
        if (isGuest && orderId) {
          const guestOrders = JSON.parse(localStorage.getItem("nqt_guest_orders") || "[]");
          guestOrders.push(orderId);
          localStorage.setItem("nqt_guest_orders", JSON.stringify(guestOrders));
        }
        if (isGuest) {
          localStorage.setItem("nqt_guest_info", JSON.stringify({ hoTen, sdt, diaChi, tinh }));
        }
        setCart([]);
        showToast("success", "Đặt hàng thành công!");

        // Redirect directly to the orders tab with the orderId in the URL!
        const url = new URL(window.location.href);
        url.searchParams.set("tab", "orders");
        url.searchParams.set("orderId", orderId);
        window.history.replaceState(null, "", url.toString());
        setActiveTab("orders");
      } else {
        const data = await res.json();
        showToast("error", data.nqt_thong_diep || "Đặt hàng thất bại.");
      }
    } catch (err) {
      showToast("error", "Lỗi kết nối máy chủ.");
    } finally {
      setIsSubmitting(false);
    }
  };


  if (cart.length === 0) {
    return (
      <div className="text-center py-20 bg-white dark:bg-white/5 border border-gray-100 dark:border-white/10 rounded-3xl shadow-[0_8px_30px_rgb(0,0,0,0.04)] max-w-xl mx-auto">
        <ShoppingCart className="mx-auto w-12 h-12 text-gray-400 mb-4" />
        <p className="text-gray-500 dark:text-[#A1A1AA] italic mb-6">Giỏ hàng của bạn đang trống.</p>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <h2 className="text-3xl font-black tracking-tight flex items-center mb-8">
        <ShoppingCart size={28} className="mr-4 text-[#C9A84C]" />
        Giỏ Hàng <span className="text-[#C9A84C] ml-2">Của Tôi</span>
      </h2>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-4">
          {cart.map((item, idx) => (
            <div
              key={item.id}
              className="bg-white dark:bg-white/5 border border-gray-100 dark:border-white/10 rounded-3xl p-5 flex items-center gap-4 hover:border-[#C9A84C]/30 transition-all shadow-[0_8px_30px_rgb(0,0,0,0.04)]"
            >
              <div className="w-16 h-16 bg-[#FAFAFA] dark:bg-white/5 rounded-2xl flex items-center justify-center flex-shrink-0 relative overflow-hidden">
                <Activity className="text-gray-400" />
                {item.image && (
                  <img
                    src={item.image}
                    className="absolute inset-0 w-full h-full object-cover rounded-2xl"
                    alt={item.name}
                  />
                )}
              </div>
              <div className="flex-1 min-w-0">
                <h4 className="font-bold text-white text-sm truncate">{item.name}</h4>
                <p className="text-[#C9A84C] text-sm font-mono font-bold mt-1">
                  {item.price.toLocaleString("vi-VN")}₫
                </p>
              </div>
              <div className="flex items-center gap-2 flex-shrink-0">
                <button
                  onClick={() => updateQty(idx, -1)}
                  className="w-8 h-8 rounded-xl border border-gray-200 dark:border-white/10 text-gray-500 hover:border-[#C9A84C] hover:text-[#C9A84C] transition-colors flex items-center justify-center text-lg"
                >
                  −
                </button>
                <span className="font-bold font-mono text-white w-6 text-center">{item.qty}</span>
                <button
                  onClick={() => updateQty(idx, 1)}
                  className="w-8 h-8 rounded-xl border border-gray-200 dark:border-white/10 text-gray-500 hover:border-[#C9A84C] hover:text-[#C9A84C] transition-colors flex items-center justify-center text-lg"
                >
                  +
                </button>
              </div>
              <div className="text-right flex-shrink-0 ml-4">
                <div className="font-bold font-mono text-white text-sm">
                  {(item.price * item.qty).toLocaleString("vi-VN")}₫
                </div>
                <button
                  onClick={() => removeProduct(idx)}
                  className="text-red-500 hover:text-red-600 text-xs font-bold uppercase tracking-widest mt-1 block"
                >
                  Xoá
                </button>
              </div>
            </div>
          ))}
        </div>

        <div className="lg:col-span-1">
          <div className="bg-white dark:bg-white/5 border border-gray-100 dark:border-white/10 rounded-3xl p-6 sticky top-24 shadow-[0_8px_30px_rgb(0,0,0,0.04)]">
            <h3 className="font-bold text-lg text-white mb-5 uppercase tracking-widest">
              Thông tin giao hàng
            </h3>
            <form onSubmit={handleCheckout} className="space-y-4">
              <div>
                <label className="block text-gray-500 dark:text-[#A1A1AA] text-[10px] font-bold uppercase tracking-wider mb-1.5">
                  Họ tên người nhận
                </label>
                <input
                  type="text"
                  required
                  value={hoTen}
                  onChange={(e) => setHoTen(e.target.value)}
                  className="w-full bg-[#FAFAFA] dark:bg-white/5 border border-gray-100 dark:border-white/10 rounded-xl px-4 py-2.5 text-sm text-[#0A0A0A] dark:text-white focus:outline-none focus:border-[#C9A84C]/50 transition-colors"
                />
              </div>

              <div>
                <label className="block text-gray-500 dark:text-[#A1A1AA] text-[10px] font-bold uppercase tracking-wider mb-1.5">
                  Số điện thoại
                </label>
                <input
                  type="tel"
                  required
                  value={sdt}
                  onChange={(e) => setSdt(e.target.value)}
                  className="w-full bg-[#FAFAFA] dark:bg-white/5 border border-gray-100 dark:border-white/10 rounded-xl px-4 py-2.5 text-sm text-[#0A0A0A] dark:text-white focus:outline-none focus:border-[#C9A84C]/50 transition-colors"
                />
              </div>

              <div>
                <label className="block text-gray-500 dark:text-[#A1A1AA] text-[10px] font-bold uppercase tracking-wider mb-1.5">
                  Địa chỉ giao hàng
                </label>
                <input
                  type="text"
                  required
                  placeholder="Số nhà, tên đường..."
                  value={diaChi}
                  onChange={(e) => setDiaChi(e.target.value)}
                  className="w-full bg-[#FAFAFA] dark:bg-white/5 border border-gray-100 dark:border-white/10 rounded-xl px-4 py-2.5 text-sm text-[#0A0A0A] dark:text-white placeholder:text-gray-400 dark:placeholder:text-[#52525B] focus:outline-none focus:border-[#C9A84C]/50 transition-colors"
                />
              </div>

              <div>
                <label className="block text-gray-500 dark:text-[#A1A1AA] text-[10px] font-bold uppercase tracking-wider mb-1.5">
                  Tỉnh / Thành phố
                </label>
                <input
                  type="text"
                  required
                  value={tinh}
                  onChange={(e) => setTinh(e.target.value)}
                  className="w-full bg-[#FAFAFA] dark:bg-white/5 border border-gray-100 dark:border-white/10 rounded-xl px-4 py-2.5 text-sm text-[#0A0A0A] dark:text-white focus:outline-none focus:border-[#C9A84C]/50 transition-colors"
                />
              </div>

              <div>
                <label className="block text-gray-500 dark:text-[#A1A1AA] text-[10px] font-bold uppercase tracking-wider mb-1.5">
                  Ghi chú
                </label>
                <textarea
                  rows="2"
                  value={ghiChu}
                  onChange={(e) => setGhiChu(e.target.value)}
                  className="w-full bg-[#FAFAFA] dark:bg-white/5 border border-gray-100 dark:border-white/10 rounded-xl px-4 py-2 text-sm text-[#0A0A0A] dark:text-white focus:outline-none focus:border-[#C9A84C]/50 transition-colors resize-none"
                />
              </div>

              <div className="space-y-2 pt-2">
                <label className="block text-gray-500 dark:text-[#A1A1AA] text-[10px] font-bold uppercase tracking-wider">
                  Phương thức thanh toán
                </label>
                <div className="flex gap-2">
                  <button
                    type="button"
                    onClick={() => setPayMethod("tien_mat")}
                    className={`flex-1 py-2.5 border rounded-xl text-xs font-bold uppercase tracking-wider transition-all ${
                      payMethod === "tien_mat"
                        ? "border-[#C9A84C] text-[#C9A84C] bg-[#C9A84C]/10"
                        : "border-gray-100 dark:border-white/10 text-gray-500 dark:text-[#A1A1AA]"
                    }`}
                  >
                    COD (Tiền mặt)
                  </button>
                  <button
                    type="button"
                    onClick={() => setPayMethod("chuyen_khoan")}
                    className={`flex-1 py-2.5 border rounded-xl text-xs font-bold uppercase tracking-wider transition-all ${
                      payMethod === "chuyen_khoan"
                        ? "border-[#C9A84C] text-[#C9A84C] bg-[#C9A84C]/10"
                        : "border-gray-100 dark:border-white/10 text-gray-500 dark:text-[#A1A1AA]"
                    }`}
                  >
                    Chuyển khoản
                  </button>
                </div>
              </div>

              {payMethod === "chuyen_khoan" && (
                <div className="bg-amber-500/10 border border-amber-500/20 p-4 rounded-2xl mt-4 text-xs text-amber-500 leading-relaxed font-bold tracking-wide">
                  <div className="flex justify-between mb-1">
                    <span>Ngân hàng:</span>
                    <span>MB BANK</span>
                  </div>
                  <div className="flex justify-between mb-1">
                    <span>Số tài khoản:</span>
                    <span>188806789</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Chủ tài khoản:</span>
                    <span>NGUYEN QUANG TAM</span>
                  </div>
                </div>
              )}

              <div className="border-t border-gray-100 dark:border-white/10 pt-4 mt-6">
                <div className="flex justify-between items-center mb-6">
                  <span className="font-bold text-[#0A0A0A] dark:text-[#F5F5F0]">Tổng cộng:</span>
                  <span className="text-[#C9A84C] font-black text-xl font-mono">
                    {subtotal.toLocaleString("vi-VN")}₫
                  </span>
                </div>
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="w-full py-4 bg-[#C9A84C] text-[#0A0A0A] hover:bg-black hover:text-[#C9A84C] border border-[#C9A84C] rounded-2xl font-black uppercase tracking-widest transition-all shadow-[0_0_20px_rgba(201,168,76,0.3)] disabled:opacity-50 text-xs"
                >
                  {isSubmitting ? "Đang xử lý..." : "Đặt hàng"}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

const OrdersView = ({ orders, setOrders, isGuest, showToast }) => {
  const [selectedOrder, setSelectedOrder] = useState(null);
  const [sdtLookup, setSdtLookup] = useState("");
  const [isSearching, setIsSearching] = useState(false);
  const [zoomQr, setZoomQr] = useState(false);

  const ST = {
    cho_xac_nhan: { l: "Chờ xác nhận", c: "text-amber-500 border-amber-500/30 bg-amber-500/10" },
    dang_xu_ly: { l: "Đang xử lý", c: "text-blue-500 border-blue-500/30 bg-blue-500/10" },
    dang_giao: { l: "Đang giao", c: "text-sky-500 border-sky-500/30 bg-sky-500/10" },
    da_giao: { l: "Đã giao", c: "text-emerald-500 border-emerald-500/30 bg-emerald-500/10" },
    da_huy: { l: "Đã huỷ", c: "text-rose-500 border-rose-500/30 bg-rose-500/10" },
  };

  const handleSetSelectedOrder = (o) => {
    setSelectedOrder(o);
    const url = new URL(window.location.href);
    if (o) {
      url.searchParams.set("orderId", o.g6_ma_don_hang);
    } else {
      url.searchParams.delete("orderId");
    }
    window.history.replaceState(null, "", url.toString());
  };

  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const orderIdParam = urlParams.get("orderId");
    if (orderIdParam) {
      const match = orders.find((o) => String(o.g6_ma_don_hang) === orderIdParam);
      if (match) {
        setSelectedOrder(match);
      } else {
        const fetchSingleOrder = async () => {
          try {
            const token = localStorage.getItem("nqt_token");
            const r = await fetch(`/api/nqt-don-hang/${orderIdParam}`, {
              headers: token ? { Authorization: `Bearer ${token}` } : {},
            });
            if (r.ok) {
              const j = await r.json();
              if (j.nqt_du_lieu) {
                setSelectedOrder(j.nqt_du_lieu);
              }
            }
          } catch (e) {
            console.error("Error fetching single order from URL param:", e);
          }
        };
        fetchSingleOrder();
      }
    } else {
      setSelectedOrder(null);
    }
  }, [orders]);

  useEffect(() => {
    let intervalId;
    if (selectedOrder && selectedOrder.g6_phuong_thuc_thanh_toan === "chuyen_khoan" && selectedOrder.g6_trang_thai === "cho_xac_nhan") {
      const checkOrderStatus = async () => {
        try {
          const token = localStorage.getItem("nqt_token");
          const r = await fetch(`/api/nqt-don-hang/${selectedOrder.g6_ma_don_hang}`, {
            headers: token ? { Authorization: `Bearer ${token}` } : {},
          });
          if (r.ok) {
            const j = await r.json();
            const updatedOrder = j.nqt_du_lieu;
            if (updatedOrder) {
              const status = updatedOrder.g6_trang_thai;
              if (status === "dang_xu_ly" || status === "da_giao" || status === "dang_giao") {
                showToast("success", "Hệ thống đã nhận được tiền thanh toán!");
                setOrders((prev) => prev.map((o) => o.g6_ma_don_hang === updatedOrder.g6_ma_don_hang ? updatedOrder : o));
                setSelectedOrder(updatedOrder);
                clearInterval(intervalId);
              }
            }
          }
        } catch (err) {
          console.error("Error polling order status inside modal:", err);
        }
      };

      intervalId = setInterval(checkOrderStatus, 3000);
      checkOrderStatus();
    }

    return () => {
      if (intervalId) clearInterval(intervalId);
    };
  }, [selectedOrder]);

  const handleLookup = async (e) => {
    e.preventDefault();
    if (!sdtLookup.trim()) return;
    setIsSearching(true);
    try {
      const res = await fetch(`/api/nqt-don-hang?g6_so_dien_thoai=${encodeURIComponent(sdtLookup)}`);
      if (res.ok) {
        const j = await res.json();
        const list = Array.isArray(j.nqt_du_lieu?.g6_danh_sach) ? j.nqt_du_lieu.g6_danh_sach : (Array.isArray(j.nqt_du_lieu) ? j.nqt_du_lieu : (Array.isArray(j) ? j : []));
        setOrders(list.sort((a, b) => new Date(b.g6_ngay_tao) - new Date(a.g6_ngay_tao)));
        showToast("success", `Tìm thấy ${list.length} đơn hàng!`);
      } else {
        showToast("error", "Tra cứu đơn hàng thất bại.");
      }
    } catch (e) {
      showToast("error", "Lỗi kết nối máy chủ.");
    } finally {
      setIsSearching(false);
    }
  };

  return (
    <div className="space-y-6">
      <h2 className="text-3xl font-black tracking-tight flex items-center mb-8">
        <History size={28} className="mr-4 text-[#C9A84C]" />
        Đơn Hàng <span className="text-[#C9A84C] ml-2">Của Tôi</span>
      </h2>

      {isGuest && (
        <div className="bg-white dark:bg-[#1C1C1C] border border-gray-100 dark:border-white/10 rounded-3xl p-6 mb-8 max-w-xl shadow-xl">
          <h3 className="font-bold text-sm uppercase tracking-wider text-[#C9A84C] mb-4">
            Tra cứu đơn hàng bằng số điện thoại
          </h3>
          <form onSubmit={handleLookup} className="flex gap-4">
            <input
              type="tel"
              required
              placeholder="Nhập số điện thoại mua hàng..."
              value={sdtLookup}
              onChange={(e) => setSdtLookup(e.target.value)}
              className="flex-1 bg-[#FAFAFA] dark:bg-white/5 border border-gray-100 dark:border-white/10 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-[#C9A84C]"
            />
            <button
              type="submit"
              disabled={isSearching}
              className="bg-[#C9A84C] hover:bg-[#E5C76B] text-[#0A0A0A] px-6 py-3 rounded-xl font-bold uppercase tracking-wider text-xs transition-all disabled:opacity-50"
            >
              {isSearching ? "Đang tìm..." : "Tra cứu"}
            </button>
          </form>
        </div>
      )}

      {orders.length === 0 ? (
        <div className="text-center py-20 bg-white dark:bg-white/5 border border-gray-100 dark:border-white/10 rounded-3xl shadow-[0_8px_30px_rgb(0,0,0,0.04)]">
          <History className="mx-auto w-12 h-12 text-gray-400 mb-4" />
          <p className="text-gray-500 dark:text-[#A1A1AA] italic">Bạn chưa đặt đơn hàng supplement nào.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {orders.map((o) => {
            const s = ST[o.g6_trang_thai] || ST.cho_xac_nhan;
            return (
              <div
                key={o.g6_ma_don_hang}
                className="bg-white dark:bg-white/5 border border-gray-100 dark:border-white/10 rounded-3xl p-6 hover:border-[#C9A84C]/30 transition-all shadow-[0_8px_30px_rgb(0,0,0,0.04)] flex flex-col justify-between"
              >
                <div>
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <span className="text-[10px] text-gray-500 dark:text-[#A1A1AA] font-bold tracking-widest uppercase">
                        Mã đơn hàng
                      </span>
                      <h4 className="font-bold text-white font-mono">#{o.g6_ma_don_hang}</h4>
                    </div>
                    <span className={`border text-[10px] font-bold uppercase tracking-widest px-3 py-1 rounded-full ${s.c}`}>
                      {s.l}
                    </span>
                  </div>
                  <div className="flex justify-between text-sm text-gray-500 dark:text-[#A1A1AA] mb-4 font-bold">
                    <span>
                      {new Date(o.g6_ngay_tao).toLocaleDateString("vi-VN")} · {o.g6_phuong_thuc_thanh_toan === "tien_mat" ? "COD" : "Chuyển khoản"}
                    </span>
                    <span className="text-[#C9A84C] font-mono text-base font-black">
                      {o.g6_tong_thanh_toan.toLocaleString("vi-VN")}₫
                    </span>
                  </div>
                </div>
                <button
                  onClick={() => handleSetSelectedOrder(o)}
                  className="w-full py-2.5 border border-gray-100 dark:border-white/10 text-gray-500 dark:text-[#A1A1AA] hover:text-[#0A0A0A] dark:hover:text-white rounded-xl text-xs font-bold uppercase tracking-widest hover:bg-white dark:hover:bg-white/5 transition-all"
                >
                  Xem chi tiết
                </button>
              </div>
            );
          })}
        </div>
      )}

      {selectedOrder && (
        <div
          className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm"
          onClick={() => handleSetSelectedOrder(null)}
        >
          <div
            className="bg-white dark:bg-[#1C1C1C] border border-[#C9A84C]/30 rounded-3xl w-full max-w-lg overflow-hidden shadow-[0_0_50px_rgba(201,168,76,0.2)] flex flex-col max-h-[85vh]"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="p-6 border-b border-gray-100 dark:border-white/10 flex justify-between items-center bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)] dark:shadow-none dark:bg-white/5">
              <h4 className="font-bold text-xl uppercase tracking-widest text-[#0A0A0A] dark:text-[#F5F5F0]">
                Chi tiết đơn hàng
              </h4>
              <button
                onClick={() => handleSetSelectedOrder(null)}
                className="w-8 h-8 rounded-full bg-[#FAFAFA] dark:bg-white/5 hover:bg-black/10 dark:bg-white/10 flex items-center justify-center text-gray-500 dark:text-[#A1A1AA] hover:text-[#0A0A0A]"
              >
                ✕
              </button>
            </div>
            <div className="flex-1 p-6 overflow-y-auto space-y-6">
              <div className="flex justify-between items-center">
                <div>
                  <span className="text-[10px] text-gray-500 dark:text-[#A1A1AA] font-bold tracking-widest uppercase">
                    Mã đơn hàng
                  </span>
                  <h4 className="font-bold text-lg text-white font-mono">#{selectedOrder.g6_ma_don_hang}</h4>
                </div>
                <span className={`border text-[10px] font-bold uppercase tracking-widest px-3 py-1 rounded-full ${ST[selectedOrder.g6_trang_thai]?.c}`}>
                  {ST[selectedOrder.g6_trang_thai]?.l}
                </span>
              </div>

              <div className="space-y-3">
                <span className="text-[10px] text-gray-500 dark:text-[#A1A1AA] font-bold tracking-widest uppercase block mb-1">
                  Mặt hàng
                </span>
                {(selectedOrder.g6_chi_tiet || []).map((item, idx) => (
                  <div key={idx} className="flex justify-between text-sm">
                    <span className="text-gray-500 dark:text-[#A1A1AA] font-semibold">
                      {item.g6_ten_san_pham} <span className="text-gray-400">×{item.g6_so_luong}</span>
                    </span>
                    <span className="font-bold font-mono text-[#0A0A0A] dark:text-[#F5F5F0]">
                      {item.g6_thanh_tien.toLocaleString("vi-VN")}₫
                    </span>
                  </div>
                ))}
              </div>

              <div className="border-t border-gray-100 dark:border-white/10 pt-4 space-y-2 text-sm">
                <div className="flex justify-between text-gray-500 dark:text-[#A1A1AA] font-semibold">
                  <span>Phí giao hàng</span>
                  <span className="font-mono">0₫</span>
                </div>
                <div className="flex justify-between font-black text-white text-base">
                  <span>Tổng tiền</span>
                  <span className="text-[#C9A84C] font-mono">
                    {selectedOrder.g6_tong_thanh_toan.toLocaleString("vi-VN")}₫
                  </span>
                </div>
              </div>

              <div className="border-t border-gray-100 dark:border-white/10 pt-4 space-y-2 text-xs font-bold text-gray-500 dark:text-[#A1A1AA] leading-relaxed">
                <div>
                  <span className="text-[9px] uppercase tracking-wider text-gray-400 mr-2">Người nhận:</span>
                  <span className="text-white">{selectedOrder.g6_ho_ten_nguoi_nhan}</span>
                </div>
                <div>
                  <span className="text-[9px] uppercase tracking-wider text-gray-400 mr-2">Số điện thoại:</span>
                  <span className="text-white">{selectedOrder.g6_so_dien_thoai || selectedOrder.g6_so_dien_thoai_nguoi_nhan}</span>
                </div>
                <div>
                  <span className="text-[9px] uppercase tracking-wider text-gray-400 mr-2">Địa chỉ giao:</span>
                  <span className="text-white">{selectedOrder.g6_dia_chi_giao_hang || "—"}</span>
                </div>
                <div>
                  <span className="text-[9px] uppercase tracking-wider text-gray-400 mr-2">Phương thức:</span>
                  <span className="text-white">
                    {selectedOrder.g6_phuong_thuc_thanh_toan === "tien_mat" ? "Tiền mặt (COD)" : "Chuyển khoản"}
                  </span>
                </div>
                <div>
                  <span className="text-[9px] uppercase tracking-wider text-gray-400 mr-2">Ngày đặt:</span>
                  <span className="text-white">
                    {new Date(selectedOrder.g6_ngay_tao).toLocaleString("vi-VN")}
                  </span>
                </div>
                <div>
                  <span className="text-[9px] uppercase tracking-wider text-gray-400 mr-2">Ghi chú:</span>
                  <span className="text-white italic">{selectedOrder.g6_ghi_chu || "—"}</span>
                </div>
              </div>

              {selectedOrder.g6_phuong_thuc_thanh_toan === "chuyen_khoan" && (
                <div className="border-t border-gray-100 dark:border-white/10 pt-6 mt-6 space-y-4">
                  {selectedOrder.g6_trang_thai === "cho_xac_nhan" ? (
                    <>
                      <h5 className="font-bold text-xs uppercase tracking-widest text-[#C9A84C] text-center">
                        Thông Tin Thanh Toán Chuyển Khoản
                      </h5>
                      <div 
                        className="bg-white p-4 rounded-2xl border border-gray-100 dark:border-white/10 shadow-sm flex flex-col items-center max-w-[240px] mx-auto cursor-zoom-in transition-all hover:scale-105 active:scale-95"
                        onClick={() => setZoomQr(true)}
                        title="Click để phóng to ảnh QR"
                      >
                        <img
                          src={`https://img.vietqr.io/image/MB-188806789-compact2.png?amount=${selectedOrder.g6_tong_thanh_toan}&addInfo=DH${selectedOrder.g6_ma_don_hang}&accountName=NGUYEN%20QUANG%20TAM`}
                          alt="VietQR MBBank"
                          className="w-full h-auto object-contain"
                        />
                      </div>
                      
                      <div className="w-full bg-[#FAFAFA] dark:bg-white/5 border border-gray-100 dark:border-white/10 rounded-2xl p-4 text-xs space-y-2">
                        <div className="flex justify-between">
                          <span className="text-gray-400 font-semibold">Ngân hàng:</span>
                          <span className="font-bold text-[#0A0A0A] dark:text-white">MB BANK</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-400 font-semibold">Số tài khoản:</span>
                          <span className="font-bold text-[#0A0A0A] dark:text-white">188806789</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-400 font-semibold">Chủ tài khoản:</span>
                          <span className="font-bold text-[#0A0A0A] dark:text-white">NGUYEN QUANG TAM</span>
                        </div>
                        <div className="flex justify-between border-t border-gray-200/50 dark:border-white/10 pt-2">
                          <span className="text-gray-400 font-semibold">Số tiền:</span>
                          <span className="font-bold font-mono text-[#C9A84C] text-sm">
                            {selectedOrder.g6_tong_thanh_toan.toLocaleString("vi-VN")}₫
                          </span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-400 font-semibold">Nội dung chuyển khoản:</span>
                          <span className="font-mono font-bold bg-[#C9A84C]/10 text-[#C9A84C] px-2 py-0.5 rounded text-sm select-all">
                            DH{selectedOrder.g6_ma_don_hang}
                          </span>
                        </div>
                      </div>
        
                      <div className="flex items-center justify-center gap-2 text-gray-500 dark:text-[#A1A1AA] text-[11px] font-bold">
                        <div className="w-2 h-2 bg-amber-500 rounded-full animate-ping"></div>
                        <span>Đang chờ hệ thống duyệt thanh toán tự động...</span>
                      </div>
                    </>
                  ) : (
                    <div className="bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-2xl p-4 flex items-center gap-3">
                      <CheckCircle2 className="w-5 h-5 flex-shrink-0" />
                      <div>
                        <div className="font-black text-xs uppercase tracking-wider">Đã Thanh Toán Thành Công</div>
                        <p className="text-[11px] text-emerald-400/80 mt-0.5">Hệ thống đã nhận được tiền và đang chuẩn bị giao hàng.</p>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
            <div className="p-6 bg-white dark:bg-white/5 border-t border-gray-100 dark:border-white/10 flex justify-end">
              <button
                onClick={() => handleSetSelectedOrder(null)}
                className="bg-[#C9A84C] text-[#0A0A0A] px-6 py-2.5 rounded-xl font-bold uppercase tracking-widest text-xs"
              >
                Đóng
              </button>
            </div>
          </div>
        </div>
      )}

      {zoomQr && selectedOrder && (
        <div
          className="fixed inset-0 z-[200] flex items-center justify-center p-4 bg-black/90 backdrop-blur-md cursor-zoom-out"
          onClick={() => setZoomQr(false)}
        >
          <div 
            className="relative max-w-sm w-full bg-white p-6 rounded-3xl shadow-2xl flex flex-col items-center justify-center animate-in fade-in zoom-in-95 duration-200"
            onClick={(e) => e.stopPropagation()}
          >
            <button 
              onClick={() => setZoomQr(false)}
              className="absolute top-4 right-4 w-8 h-8 rounded-full bg-gray-100 hover:bg-gray-200 flex items-center justify-center text-gray-800 font-bold"
            >
              ✕
            </button>
            <img
              src={`https://img.vietqr.io/image/MB-188806789-compact2.png?amount=${selectedOrder.g6_tong_thanh_toan}&addInfo=DH${selectedOrder.g6_ma_don_hang}&accountName=NGUYEN%20QUANG%20TAM`}
              alt="VietQR MBBank Phóng To"
              className="w-full h-auto object-contain"
            />
            <p className="text-gray-500 text-xs mt-4 font-bold uppercase tracking-wider text-center">
              Quét mã để thanh toán tự động
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

const ProfileView = ({ profile, isGuest, showToast, setProfile }) => {
  const [hoTen, setHoTen] = useState("");
  const [sdt, setSdt] = useState("");
  const [diaChi, setDiaChi] = useState("");
  const [tinh, setTinh] = useState("");

  const [memberHoTen, setMemberHoTen] = useState(profile.g6_ho_ten || "");
  const [memberEmail, setMemberEmail] = useState(profile.g6_email || "");
  const [memberDiaChi, setMemberDiaChi] = useState(profile.g6_dia_chi || "");
  const [memberNgaySinh, setMemberNgaySinh] = useState(profile.g6_ngay_sinh || "");
  const [memberGioiTinh, setMemberGioiTinh] = useState(profile.g6_gioi_tinh || "nam");

  const [passwordCu, setPasswordCu] = useState("");
  const [passwordMoi, setPasswordMoi] = useState("");

  useEffect(() => {
    if (isGuest) {
      const guestInfo = JSON.parse(localStorage.getItem("nqt_guest_info") || "{}");
      setHoTen(guestInfo.hoTen || "");
      setSdt(guestInfo.sdt || "");
      setDiaChi(guestInfo.diaChi || "");
      setTinh(guestInfo.tinh || "");
    } else {
      setMemberHoTen(profile.g6_ho_ten || "");
      setMemberEmail(profile.g6_email || "");
      setMemberDiaChi(profile.g6_dia_chi || "");
      setMemberNgaySinh(profile.g6_ngay_sinh || "");
      setMemberGioiTinh(profile.g6_gioi_tinh || "nam");
    }
  }, [profile, isGuest]);

  const handleSaveGuestInfo = (e) => {
    e.preventDefault();
    localStorage.setItem("nqt_guest_info", JSON.stringify({ hoTen, sdt, diaChi, tinh }));
    showToast("success", "Đã cập nhật thông tin mua hàng!");
  };

  const handleUpdateMemberProfile = async (e) => {
    e.preventDefault();
    try {
      const res = await nqtApi("/api/nqt-hoi-vien/toi", {
        method: "PUT",
        body: JSON.stringify({
          g6_ho_ten: memberHoTen,
          g6_email: memberEmail,
          g6_dia_chi: memberDiaChi,
          g6_ngay_sinh: memberNgaySinh,
          g6_gioi_tinh: memberGioiTinh,
        }),
      });
      const data = await res.json();
      if (data.nqt_thanh_cong) {
        setProfile(data.nqt_du_lieu.nqt_hoi_vien);
        showToast("success", "Cập nhật thông tin thành công!");
      } else {
        showToast("error", data.nqt_thong_diep || "Lỗi cập nhật");
      }
    } catch (err) {
      showToast("error", "Lỗi kết nối máy chủ");
    }
  };

  const handleChangePassword = async (e) => {
    e.preventDefault();
    if (!passwordCu || !passwordMoi) {
      showToast("error", "Vui lòng nhập đầy đủ mật khẩu");
      return;
    }
    try {
      const res = await nqtApi("/api/nqt-hoi-vien/doi-mat-khau", {
        method: "PUT",
        body: JSON.stringify({
          nqt_mat_khau_cu: passwordCu,
          nqt_mat_khau_moi: passwordMoi,
        }),
      });
      const data = await res.json();
      if (data.nqt_thanh_cong) {
        showToast("success", "Đổi mật khẩu thành công!");
        setPasswordCu("");
        setPasswordMoi("");
      } else {
        showToast("error", data.nqt_thong_diep || "Mật khẩu cũ không đúng");
      }
    } catch (err) {
      showToast("error", "Lỗi kết nối máy chủ");
    }
  };

  return (
    <div className="space-y-8 max-w-5xl mx-auto px-4 pb-12">
      {/* Profile Header Hero Card */}
      <div className="relative overflow-hidden bg-gradient-to-r from-[#2c2d30] via-[#1E1E1E] to-[#2c2d30] rounded-3xl p-8 border border-gray-200/10 dark:border-white/5 shadow-[0_20px_50px_rgba(0,0,0,0.06)] dark:shadow-none flex flex-col md:flex-row items-center md:justify-between gap-6 group">
        {/* Decorative gold gradient mesh background */}
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_30%,rgba(201,168,76,0.08),transparent_50%)] pointer-events-none"></div>
        <div className="absolute -right-16 -top-16 w-48 h-48 bg-[#C9A84C]/5 rounded-full blur-3xl group-hover:bg-[#C9A84C]/10 transition-colors duration-500"></div>

        <div className="flex flex-col md:flex-row items-center gap-6 relative z-10">
          {/* Avatar with luxury golden ring */}
          <div className="relative">
            <div className="absolute inset-0 bg-gradient-to-tr from-[#C9A84C] to-amber-300 rounded-2xl blur-sm opacity-50 group-hover:opacity-75 transition-opacity"></div>
            <img
              src={
                profile.g6_anh_the ||
                "https://ui-avatars.com/api/?name=" +
                  encodeURIComponent(profile.g6_ho_ten || "HV") +
                  "&background=C9A84C&color=000"
              }
              className="w-20 h-20 rounded-2xl object-cover border-2 border-[#C9A84C] relative z-10 shadow-md group-hover:scale-[1.02] transition-transform duration-300"
              alt="Avatar"
            />
          </div>

          <div className="text-center md:text-left">
            <div className="flex flex-col md:flex-row items-center gap-2 md:gap-3">
              <h2 className="text-2xl md:text-3xl font-black tracking-wide font-['Barlow_Condensed'] uppercase" style={{ color: '#FFFFFF' }}>
                {profile.g6_ho_ten || "Hội viên"}
              </h2>
              {!isGuest && (
                <span className="px-3 py-1 bg-[#C9A84C]/10 border border-[#C9A84C]/40 text-[#C9A84C] text-[10px] font-bold tracking-widest rounded-full uppercase flex items-center gap-1.5 shadow-[0_2px_10px_rgba(201,168,76,0.1)]">
                  <ShieldCheck size={12} className="text-[#C9A84C]" />
                  Hội viên chính thức
                </span>
              )}
            </div>
            <p className="text-sm mt-1.5" style={{ color: '#A1A1AA' }}>
              {isGuest
                ? "Guest portal • Mua sắm vãng lai"
                : `Mã số tài khoản: #${String(profile.g6_ma_nguoi_dung || 0).padStart(5, '0')}`}
            </p>
          </div>
        </div>

        {!isGuest && (
          <div className="flex items-center gap-8 border-t md:border-t-0 md:border-l border-gray-200/20 dark:border-white/10 pt-4 md:pt-0 md:pl-8 relative z-10 w-full md:w-auto justify-around md:justify-start">
            <div className="text-center md:text-left">
              <span className="text-[10px] font-bold uppercase tracking-wider block" style={{ color: '#71717A' }}>
                Ngày tham gia
              </span>
              <span className="text-sm font-bold mt-1 block" style={{ color: '#F5F5F0' }}>
                {profile.g6_ngay_tao ? new Date(profile.g6_ngay_tao).toLocaleDateString("vi-VN") : "Hôm nay"}
              </span>
            </div>
            <div className="text-center md:text-left">
              <span className="text-[10px] font-bold uppercase tracking-wider block" style={{ color: '#71717A' }}>
                Trạng thái gói
              </span>
              <span className="text-sm font-bold mt-1 block flex items-center gap-1.5" style={{ color: '#4ADE80' }}>
                <span className="w-2 h-2 rounded-full animate-pulse" style={{ backgroundColor: '#4ADE80' }}></span>
                Đang hoạt động
              </span>
            </div>
          </div>
        )}
      </div>

      {isGuest ? (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="md:col-span-1 bg-gradient-to-br from-white to-gray-50/50 dark:from-[#121212]/30 dark:to-[#0A0A0A]/30 border border-gray-100 dark:border-white/5 rounded-3xl p-6 flex flex-col items-center text-center justify-center shadow-lg group">
            <div className="w-16 h-16 rounded-2xl bg-[#C9A84C]/10 border border-[#C9A84C]/20 flex items-center justify-center mb-4 text-[#C9A84C] group-hover:scale-110 transition-transform">
              <User size={32} />
            </div>
            <h4 className="font-bold text-lg text-[#0A0A0A] dark:text-[#F5F5F0]">Khách Vãng Lai</h4>
            <p className="text-xs text-gray-400 mt-2 mb-6 leading-relaxed">
              Bạn đang sử dụng ứng dụng không cần đăng nhập. Thiết lập thông tin ở đây để tự động điền vào hóa đơn mua hàng.
            </p>
            <a
              href="/login"
              className="w-full py-3 bg-[#C9A84C] text-[#0A0A0A] hover:bg-black hover:text-[#C9A84C] border border-[#C9A84C] transition-all rounded-xl font-bold uppercase tracking-wider text-xs no-underline block text-center shadow-[0_4px_15px_rgba(201,168,76,0.15)]"
            >
              Đăng nhập / Đăng ký
            </a>
          </div>

          <div className="md:col-span-2 bg-white dark:bg-[#121212]/30 border border-gray-100 dark:border-white/5 rounded-3xl p-6 shadow-xl">
            <h4 className="font-bold text-lg mb-6 uppercase tracking-wider text-[#C9A84C] flex items-center gap-2">
              <Shield size={18} />
              Thông tin giao hàng mặc định
            </h4>
            <form onSubmit={handleSaveGuestInfo} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="text-[10px] text-gray-500 font-bold uppercase tracking-wider block mb-1.5 ml-1">
                    Họ tên người nhận
                  </label>
                  <div className="relative">
                    <User size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" />
                    <input
                      type="text"
                      required
                      value={hoTen}
                      onChange={(e) => setHoTen(e.target.value)}
                      placeholder="Nguyễn Văn A"
                      className="w-full bg-[#FAFAFA] dark:bg-white/[0.02] border border-gray-200 dark:border-white/5 rounded-xl pl-11 pr-4 py-3 text-sm focus:outline-none focus:border-[#C9A84C] text-[#0A0A0A] dark:text-[#F5F5F0]"
                    />
                  </div>
                </div>
                <div>
                  <label className="text-[10px] text-gray-500 font-bold uppercase tracking-wider block mb-1.5 ml-1">
                    Số điện thoại
                  </label>
                  <div className="relative">
                    <Phone size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" />
                    <input
                      type="tel"
                      required
                      value={sdt}
                      onChange={(e) => setSdt(e.target.value)}
                      placeholder="0987654321"
                      className="w-full bg-[#FAFAFA] dark:bg-white/[0.02] border border-gray-200 dark:border-white/5 rounded-xl pl-11 pr-4 py-3 text-sm focus:outline-none focus:border-[#C9A84C] text-[#0A0A0A] dark:text-[#F5F5F0]"
                    />
                  </div>
                </div>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="text-[10px] text-gray-500 font-bold uppercase tracking-wider block mb-1.5 ml-1">
                    Địa chỉ chi tiết
                  </label>
                  <div className="relative">
                    <MapPin size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" />
                    <input
                      type="text"
                      required
                      value={diaChi}
                      onChange={(e) => setDiaChi(e.target.value)}
                      placeholder="Số 123 Đường ABC"
                      className="w-full bg-[#FAFAFA] dark:bg-white/[0.02] border border-gray-200 dark:border-white/5 rounded-xl pl-11 pr-4 py-3 text-sm focus:outline-none focus:border-[#C9A84C] text-[#0A0A0A] dark:text-[#F5F5F0]"
                    />
                  </div>
                </div>
                <div>
                  <label className="text-[10px] text-gray-500 font-bold uppercase tracking-wider block mb-1.5 ml-1">
                    Tỉnh / Thành phố
                  </label>
                  <div className="relative">
                    <MapPin size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" />
                    <input
                      type="text"
                      required
                      value={tinh}
                      onChange={(e) => setTinh(e.target.value)}
                      placeholder="Hà Nội"
                      className="w-full bg-[#FAFAFA] dark:bg-white/[0.02] border border-gray-200 dark:border-white/5 rounded-xl pl-11 pr-4 py-3 text-sm focus:outline-none focus:border-[#C9A84C] text-[#0A0A0A] dark:text-[#F5F5F0]"
                    />
                  </div>
                </div>
              </div>
              <button
                type="submit"
                className="bg-[#C9A84C] text-[#0A0A0A] px-6 py-3 rounded-xl font-bold uppercase tracking-wider text-xs hover:bg-[#E5C76B] transition-all duration-300 shadow-[0_4px_15px_rgba(201,168,76,0.2)]"
              >
                Lưu cài đặt
              </button>
            </form>
          </div>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Account Details Form */}
          <div className="md:col-span-2 bg-gradient-to-br from-white to-gray-50/50 dark:from-[#121212]/30 dark:to-[#0A0A0A]/30 border border-gray-200/50 dark:border-white/5 rounded-3xl p-6 md:p-8 shadow-[0_10px_30px_rgba(0,0,0,0.01)]">
            <h4 className="font-bold text-lg mb-6 uppercase tracking-wider text-[#C9A84C] flex items-center gap-2">
              <User size={18} />
              Thông tin tài khoản
            </h4>
            <form onSubmit={handleUpdateMemberProfile} className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="text-[10px] text-gray-400 dark:text-gray-500 font-bold uppercase tracking-wider block mb-1.5 ml-1">
                    Họ tên hội viên
                  </label>
                  <div className="relative">
                    <User size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" />
                    <input
                      type="text"
                      required
                      value={memberHoTen}
                      onChange={(e) => setMemberHoTen(e.target.value)}
                      className="w-full bg-[#FAFAFA] dark:bg-white/[0.02] border border-gray-200 dark:border-white/5 rounded-xl pl-11 pr-4 py-3 text-sm focus:outline-none focus:border-[#C9A84C] text-[#0A0A0A] dark:text-[#F5F5F0] transition-all duration-300 focus:ring-1 focus:ring-[#C9A84C]/25"
                    />
                  </div>
                </div>
                <div>
                  <label className="text-[10px] text-gray-400 dark:text-gray-500 font-bold uppercase tracking-wider block mb-1.5 ml-1">
                    Địa chỉ Email
                  </label>
                  <div className="relative">
                    <Mail size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" />
                    <input
                      type="email"
                      value={memberEmail}
                      onChange={(e) => setMemberEmail(e.target.value)}
                      placeholder="your-email@g6gym.com"
                      className="w-full bg-[#FAFAFA] dark:bg-white/[0.02] border border-gray-200 dark:border-white/5 rounded-xl pl-11 pr-4 py-3 text-sm focus:outline-none focus:border-[#C9A84C] text-[#0A0A0A] dark:text-[#F5F5F0] transition-all duration-300 focus:ring-1 focus:ring-[#C9A84C]/25"
                    />
                  </div>
                </div>
              </div>

              <div>
                <label className="text-[10px] text-gray-400 dark:text-gray-500 font-bold uppercase tracking-wider block mb-1.5 ml-1">
                  Địa chỉ thường trú
                </label>
                <div className="relative">
                  <MapPin size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" />
                  <input
                    type="text"
                    value={memberDiaChi}
                    onChange={(e) => setMemberDiaChi(e.target.value)}
                    className="w-full bg-[#FAFAFA] dark:bg-white/[0.02] border border-gray-200 dark:border-white/5 rounded-xl pl-11 pr-4 py-3 text-sm focus:outline-none focus:border-[#C9A84C] text-[#0A0A0A] dark:text-[#F5F5F0] transition-all duration-300 focus:ring-1 focus:ring-[#C9A84C]/25"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="text-[10px] text-gray-400 dark:text-gray-500 font-bold uppercase tracking-wider block mb-1.5 ml-1">
                    Ngày sinh
                  </label>
                  <div className="relative">
                    <Calendar size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" />
                    <input
                      type="date"
                      value={memberNgaySinh ? memberNgaySinh.substring(0, 10) : ""}
                      onChange={(e) => setMemberNgaySinh(e.target.value)}
                      className="w-full bg-[#FAFAFA] dark:bg-white/[0.02] border border-gray-200 dark:border-white/5 rounded-xl pl-11 pr-4 py-3 text-sm focus:outline-none focus:border-[#C9A84C] text-[#0A0A0A] dark:text-[#F5F5F0] transition-all duration-300 focus:ring-1 focus:ring-[#C9A84C]/25"
                    />
                  </div>
                </div>
                <div>
                  <label className="text-[10px] text-gray-400 dark:text-gray-500 font-bold uppercase tracking-wider block mb-1.5 ml-1">
                    Giới tính
                  </label>
                  <div className="relative">
                    <User size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" />
                    <select
                      value={memberGioiTinh}
                      onChange={(e) => setMemberGioiTinh(e.target.value)}
                      className="w-full bg-[#FAFAFA] dark:bg-white/[0.02] border border-gray-200 dark:border-white/5 rounded-xl pl-11 pr-4 py-3 text-sm focus:outline-none focus:border-[#C9A84C] text-[#0A0A0A] dark:text-[#F5F5F0] appearance-none transition-all duration-300 focus:ring-1 focus:ring-[#C9A84C]/25"
                    >
                      <option value="nam">Nam</option>
                      <option value="nu">Nữ</option>
                      <option value="khac">Khác</option>
                    </select>
                    <div className="pointer-events-none absolute right-4 top-1/2 -translate-y-1/2 text-gray-400">
                      <ChevronRight size={16} className="rotate-90" />
                    </div>
                  </div>
                </div>
              </div>

              <div className="pt-2">
                <button
                  type="submit"
                  className="bg-[#C9A84C] hover:bg-black hover:text-[#C9A84C] text-[#0A0A0A] px-8 py-3.5 border border-[#C9A84C] rounded-xl font-bold uppercase tracking-widest text-[10px] transition-all duration-300 shadow-[0_8px_20px_rgba(201,168,76,0.15)] active:scale-95 cursor-pointer"
                >
                  Cập nhật thông tin
                </button>
              </div>
            </form>
          </div>

          {/* Change Password Form */}
          <div className="md:col-span-1 bg-gradient-to-br from-white to-gray-50/50 dark:from-[#121212]/30 dark:to-[#0A0A0A]/30 border border-gray-200/50 dark:border-white/5 rounded-3xl p-6 shadow-[0_10px_30px_rgba(0,0,0,0.01)] flex flex-col justify-between">
            <div>
              <h4 className="font-bold text-lg mb-6 uppercase tracking-wider text-[#C9A84C] flex items-center gap-2">
                <Key size={18} />
                Đổi mật khẩu
              </h4>
              <form onSubmit={handleChangePassword} className="space-y-5">
                <div>
                  <label className="text-[10px] text-gray-400 dark:text-gray-500 font-bold uppercase tracking-wider block mb-1.5 ml-1">
                    Mật khẩu hiện tại
                  </label>
                  <div className="relative">
                    <Lock size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" />
                    <input
                      type="password"
                      required
                      value={passwordCu}
                      onChange={(e) => setPasswordCu(e.target.value)}
                      className="w-full bg-[#FAFAFA] dark:bg-white/[0.02] border border-gray-200 dark:border-white/5 rounded-xl pl-11 pr-4 py-3 text-sm focus:outline-none focus:border-[#C9A84C] text-[#0A0A0A] dark:text-[#F5F5F0] transition-all duration-300"
                    />
                  </div>
                </div>
                <div>
                  <label className="text-[10px] text-gray-400 dark:text-gray-500 font-bold uppercase tracking-wider block mb-1.5 ml-1">
                    Mật khẩu mới
                  </label>
                  <div className="relative">
                    <Lock size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" />
                    <input
                      type="password"
                      required
                      value={passwordMoi}
                      onChange={(e) => setPasswordMoi(e.target.value)}
                      className="w-full bg-[#FAFAFA] dark:bg-white/[0.02] border border-gray-200 dark:border-white/5 rounded-xl pl-11 pr-4 py-3 text-sm focus:outline-none focus:border-[#C9A84C] text-[#0A0A0A] dark:text-[#F5F5F0] transition-all duration-300"
                    />
                  </div>
                </div>
                <button
                  type="submit"
                  className="w-full bg-[#C9A84C]/5 hover:bg-[#C9A84C] hover:text-[#0A0A0A] text-[#C9A84C] border border-[#C9A84C]/30 hover:border-[#C9A84C] py-3.5 rounded-xl font-bold uppercase tracking-widest text-[10px] transition-all duration-300 shadow-sm active:scale-95 mt-4 cursor-pointer"
                >
                  Xác nhận đổi
                </button>
              </form>
            </div>
            
            {/* Lock/Security illustration badge */}
            <div className="mt-8 pt-6 border-t border-gray-200/50 dark:border-white/5 flex items-center gap-3 text-gray-400">
              <ShieldCheck size={28} className="text-[#C9A84C]/40 flex-shrink-0" />
              <p className="text-[10px] leading-relaxed">
                Mật khẩu của bạn được mã hóa an toàn 2 đầu. Tránh tiết lộ mật khẩu cho người khác để bảo vệ tài khoản.
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

const GuestDashboardView = ({ products, packages, pts, classes, setActiveTab, setCart, showToast }) => {
  const featuredProducts = (products || []).slice(0, 4);
  const featuredPackages = ((packages && packages.available) || []).slice(0, 3);
  const featuredPts = ((pts && pts.available) || []).slice(0, 3);

  const handleAddToCart = (prod) => {
    const variantId = prod.g6_sku || prod.g6_ma_san_pham;
    
    setCart((prev) => {
      const idx = prev.findIndex((i) => i.id === prod.g6_ma_san_pham && i.variantId === variantId);
      if (idx !== -1) {
        const copy = [...prev];
        copy[idx].qty += 1;
        return copy;
      } else {
        return [
          ...prev,
          {
            id: prod.g6_ma_san_pham,
            variantId: variantId,
            name: prod.g6_ten_san_pham,
            price: prod.g6_gia_ban || 0,
            image: prod.g6_hinh_anh,
            qty: 1,
          },
        ];
      }
    });
    showToast("success", `Đã thêm ${prod.g6_ten_san_pham} vào giỏ hàng!`);
  };

  return (
    <div className="space-y-12">
      <div className="relative rounded-[32px] overflow-hidden bg-gradient-to-r from-black to-[#1a1a1a] border border-[#C9A84C]/20 p-8 md:p-12 flex flex-col md:flex-row items-center justify-between shadow-[0_0_60px_rgba(201,168,76,0.1)]">
        <div className="md:w-2/3 space-y-6">
          <span className="bg-[#C9A84C]/10 text-[#C9A84C] border border-[#C9A84C]/30 text-[10px] font-bold tracking-widest uppercase px-3 py-1.5 rounded-full">
            Ironcore Fitness & Store
          </span>
          <h1 className="text-4xl md:text-5xl font-black tracking-tight text-white leading-tight uppercase font-mono">
            Nâng Tầm Thể Chất <br />
            <span className="text-gradient bg-clip-text text-transparent bg-gradient-to-r from-[#C9A84C] to-[#E5C76B]">
              Đẳng Cấp Thượng Lưu
            </span>
          </h1>
          <p className="text-slate-400 text-sm max-w-lg leading-relaxed">
            Chào mừng bạn đến với hệ thống CLB thể hình cao cấp và phân phối thực phẩm bổ sung chính hãng Ironcore Gym. Đăng ký tập luyện hoặc mua sắm ngay hôm nay để nhận ưu đãi đặc biệt!
          </p>
          <div className="flex flex-wrap gap-4 pt-2">
            <button
              onClick={() => setActiveTab("shop")}
              className="bg-[#C9A84C] hover:bg-[#E5C76B] text-[#0A0A0A] px-8 py-3.5 rounded-2xl font-black uppercase tracking-widest text-xs shadow-[0_0_30px_rgba(201,168,76,0.3)] transition-all"
            >
              Mua Supplement ngay
            </button>
            <button
              onClick={() => setActiveTab("packages")}
              className="bg-white/5 border border-white/10 hover:bg-white/10 text-white px-8 py-3.5 rounded-2xl font-black uppercase tracking-widest text-xs transition-all"
            >
              Xem gói tập
            </button>
          </div>
        </div>
        <div className="md:w-1/3 mt-8 md:mt-0 flex justify-center relative">
          <div className="absolute w-48 h-48 bg-[#C9A84C]/20 blur-[80px] rounded-full pointer-events-none"></div>
          <Zap size={150} className="text-[#C9A84C] animate-pulse relative z-10" />
        </div>
      </div>

      <div className="space-y-6">
        <div className="flex justify-between items-end">
          <div>
            <h2 className="text-2xl font-black uppercase tracking-wider text-[#C9A84C]">
              Sản phẩm bán chạy
            </h2>
            <p className="text-xs text-gray-500 dark:text-[#A1A1AA] mt-1">
              Thực phẩm bổ sung, vitamins và phụ kiện luyện tập cao cấp
            </p>
          </div>
          <button
            onClick={() => setActiveTab("shop")}
            className="text-xs text-[#C9A84C] hover:underline uppercase tracking-widest font-black"
          >
            Tất cả sản phẩm &rarr;
          </button>
        </div>
        
        {featuredProducts.length === 0 ? (
          <div className="py-12 text-center text-gray-500 italic">Đang tải sản phẩm...</div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {featuredProducts.map((p) => {
              const price = p.g6_gia_ban || 0;
              return (
                <div
                  key={p.g6_ma_san_pham}
                  className="bg-white dark:bg-white/5 border border-gray-100 dark:border-white/10 rounded-3xl p-5 flex flex-col justify-between hover:border-[#C9A84C]/30 hover:scale-[1.02] transition-all group"
                >
                  <div>
                    <div className="bg-[#FAFAFA] dark:bg-white/5 rounded-2xl p-6 mb-4 flex items-center justify-center relative aspect-square">
                      <Activity className="w-12 h-12 text-[#C9A84C]/25" />
                      {p.g6_hinh_anh && (
                        <img
                          src={p.g6_hinh_anh}
                          className="absolute inset-0 w-full h-full object-cover rounded-2xl group-hover:scale-105 transition-transform"
                          alt={p.g6_ten_san_pham}
                        />
                      )}
                    </div>
                    <span className="text-[9px] font-bold text-gray-400 uppercase tracking-widest block mb-1">
                      {p.g6_ten_danh_muc || "Supplement"}
                    </span>
                    <h3 className="font-bold text-sm text-gray-800 dark:text-white line-clamp-2 leading-snug mb-2 min-h-[40px]">
                      {p.g6_ten_san_pham}
                    </h3>
                  </div>
                  <div className="mt-4 space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-[#C9A84C] font-mono text-sm font-black">
                        {price.toLocaleString("vi-VN")}₫
                      </span>
                    </div>
                    <button
                      onClick={() => handleAddToCart(p)}
                      className="w-full bg-[#C9A84C] text-[#0A0A0A] hover:bg-black hover:text-[#C9A84C] border border-[#C9A84C] py-2.5 rounded-xl text-xs font-bold uppercase tracking-wider transition-all shadow-[0_4px_15px_rgba(201,168,76,0.15)]"
                    >
                      Thêm vào giỏ
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      <div className="space-y-6">
        <div className="flex justify-between items-end">
          <div>
            <h2 className="text-2xl font-black uppercase tracking-wider text-[#C9A84C]">
              Gói tập thịnh hành
            </h2>
            <p className="text-xs text-gray-500 dark:text-[#A1A1AA] mt-1">
              Gói dịch vụ luyện tập tại các chi nhánh cao cấp của Ironcore Gym
            </p>
          </div>
          <button
            onClick={() => setActiveTab("packages")}
            className="text-xs text-[#C9A84C] hover:underline uppercase tracking-widest font-black"
          >
            Xem bảng giá &rarr;
          </button>
        </div>

        {featuredPackages.length === 0 ? (
          <div className="py-12 text-center text-gray-500 italic">Đang tải gói tập...</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {featuredPackages.map((pkg) => {
              const price = parseFloat(pkg.g6_gia_khuyen_mai || pkg.g6_gia || 0);
              return (
                <div
                  key={pkg.g6_ma_goi_tap}
                  className="bg-white dark:bg-white/5 border border-gray-100 dark:border-white/10 rounded-3xl p-6 flex flex-col justify-between hover:border-[#C9A84C]/30 transition-all relative overflow-hidden group"
                >
                  {pkg.g6_gia_khuyen_mai && (
                    <span className="absolute top-4 right-4 bg-red-500 text-white font-black text-[9px] uppercase tracking-wider px-2 py-1 rounded-full">
                      Sale
                    </span>
                  )}
                  <div>
                    <h3 className="text-lg font-black uppercase tracking-widest text-[#0A0A0A] dark:text-[#F5F5F0] mb-2">
                      {pkg.g6_ten_goi}
                    </h3>
                    <p className="text-xs text-gray-400 mb-6">
                      Thời hạn: {pkg.g6_so_ngay} ngày
                    </p>
                    <div className="text-3xl font-mono font-black text-[#C9A84C] mb-6">
                      {price.toLocaleString("vi-VN")}₫
                    </div>
                    <ul className="text-xs space-y-2.5 text-gray-500 dark:text-[#A1A1AA] mb-8 font-semibold">
                      <li className="flex items-center">&bull; Tập luyện tại chi nhánh đăng ký</li>
                      <li className="flex items-center">&bull; Đầy đủ trang thiết bị cao cấp</li>
                      <li className="flex items-center">&bull; Đo chỉ số InBody miễn phí hàng tháng</li>
                    </ul>
                  </div>
                  <button
                    onClick={() => setActiveTab("packages")}
                    className="w-full py-3 bg-[#C9A84C] text-[#0A0A0A] hover:bg-black hover:text-[#C9A84C] border border-[#C9A84C] rounded-xl text-xs font-bold uppercase tracking-widest transition-all shadow-[0_4px_15px_rgba(201,168,76,0.15)]"
                  >
                    Đăng ký tập
                  </button>
                </div>
              );
            })}
          </div>
        )}
      </div>

      <div className="space-y-6">
        <div className="flex justify-between items-end">
          <div>
            <h2 className="text-2xl font-black uppercase tracking-wider text-[#C9A84C]">
              Đội ngũ huấn luyện viên
            </h2>
            <p className="text-xs text-gray-500 dark:text-[#A1A1AA] mt-1">
              Đội ngũ HLV chuyên nghiệp, giàu kinh nghiệm đồng hành cùng mục tiêu của bạn
            </p>
          </div>
          <button
            onClick={() => setActiveTab("pt")}
            className="text-xs text-[#C9A84C] hover:underline uppercase tracking-widest font-black"
          >
            Đăng ký PT &rarr;
          </button>
        </div>

        {featuredPts.length === 0 ? (
          <div className="py-12 text-center text-gray-500 italic">Đang tải danh sách Coach...</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {featuredPts.map((pt) => (
              <div
                key={pt.g6_ma_hlv}
                className="bg-white dark:bg-white/5 border border-gray-100 dark:border-white/10 rounded-3xl p-5 text-center flex flex-col justify-between hover:border-[#C9A84C]/30 transition-all group"
              >
                <div className="flex flex-col items-center">
                  <div className="relative mb-4">
                    <img
                      src={
                        pt.g6_hinh_anh ||
                        pt.g6_anh_dai_dien ||
                        "https://ui-avatars.com/api/?name=" +
                          encodeURIComponent(pt.g6_ho_ten || "PT") +
                          "&background=C9A84C&color=000"
                      }
                      className="w-20 h-20 rounded-full object-cover border-2 border-[#C9A84C]/20 shadow-[0_0_20px_rgba(201,168,76,0.15)] group-hover:scale-105 transition-transform"
                    />
                  </div>
                  <h3 className="font-black text-base text-[#0A0A0A] dark:text-[#F5F5F0] mb-1">
                    {pt.g6_ho_ten || "Coach"}
                  </h3>
                  <span className="text-[10px] text-[#9E7A24] dark:text-[#C9A84C] font-bold uppercase tracking-wider bg-[#C9A84C]/10 border border-[#C9A84C]/20 px-2 py-0.5 rounded-full mb-4">
                    {pt.g6_chuyen_mon || "Fitness Coach"}
                  </span>
                  <p className="text-xs text-gray-500 dark:text-[#A1A1AA] italic leading-relaxed max-w-[200px] mb-4">
                    "Cam kết mang lại hiệu quả thay đổi vóc dáng tốt nhất cho bạn."
                  </p>
                </div>
                <button
                  onClick={() => setActiveTab("pt")}
                  className="w-full py-2.5 bg-[#C9A84C] text-[#0A0A0A] hover:bg-black hover:text-[#C9A84C] border border-[#C9A84C] rounded-xl text-xs font-bold uppercase tracking-widest transition-all shadow-[0_4px_15px_rgba(201,168,76,0.15)]"
                >
                  Đăng ký PT ngay
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};


export default MemberDashboard;
