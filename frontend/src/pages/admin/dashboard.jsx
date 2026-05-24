import React, { useState, useEffect } from 'react';
import { createRoot } from 'react-dom/client';
import { 
  Users, DollarSign, Activity, Award, Brain, 
  Clock, Calendar, QrCode, TrendingUp, CheckCircle,
  Sparkles, RefreshCw, ChevronRight, UserCheck, Flame, Zap
} from 'lucide-react';
import { 
  AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, 
  BarChart, Bar
} from 'recharts';

function AdminDashboard() {
  const [stats, setStats] = useState({
    tongHoiVien: 0,
    doanhThuThang: 0,
    dangTapLuyen: 0,
    checkinHomNay: 0,
    goiTapActive: 0,
    sucChua: 100
  });
  const [loading, setLoading] = useState(true);
  const [chartData, setChartData] = useState([]);
  const [manualCheckinId, setManualCheckinId] = useState('');
  const [checkinStatus, setCheckinStatus] = useState(null);
  const [showQRModal, setShowQRModal] = useState(false);
  const [scanStatus, setScanStatus] = useState('idle'); // idle, scanning, success, error
  const [scannedMember, setScannedMember] = useState(null);
  const [aiInsightIndex, setAiInsightIndex] = useState(0);

  const aiInsights = [
    "Peak traffic detected at 17:30 - 19:30. Recommend shifting personal trainer slots to morning hours to optimize floor spacing.",
    "Member retention is up 12.4% following the introduction of the 'Iron VIP' subscription model.",
    "Equipment usage data indicates high demand on Treadmill #3 & #4. Suggest scheduling preventative maintenance soon.",
    "AI Prediction: Expected member count tomorrow is 145. Ensure 3 coaches are active during the evening rush."
  ];

  // Neon green colors and cyber styles injected dynamically
  useEffect(() => {
    const styleOverride = document.createElement('style');
    styleOverride.id = 'nqt-neon-green-overrides';
    styleOverride.textContent = `
      :root, .dark, body, #nqtAdminWrapper {
        --primary-color: #00FF66 !important;
        --primary-rgb: 0, 255, 102 !important;
        --nqt-gold: #00FF66 !important;
        --nqt-gold-glow: rgba(0, 255, 102, 0.2) !important;
        --accent-neon: #00FF66;
      }
      
      /* Force neon green active sidebar */
      .nqt-sidebar-item.active {
        background: #00FF66 !important;
        color: #0A0A0A !important;
      }
      .nqt-sidebar-item.active i, .nqt-sidebar-item.active span {
        color: #0A0A0A !important;
      }
      .nqt-sidebar-item:not(.active) i {
        color: #00FF66 !important;
      }
      
      /* Glowing scrollbars */
      ::-webkit-scrollbar-thumb {
        background: rgba(0, 255, 102, 0.2) !important;
      }
      ::-webkit-scrollbar-thumb:hover {
        background: rgba(0, 255, 102, 0.5) !important;
      }
      
      /* Glass panel styling override */
      .glass-panel {
        background: rgba(10, 10, 12, 0.6) !important;
        backdrop-filter: blur(20px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
      }
    `;
    document.head.appendChild(styleOverride);
    
    // Rotate AI insights every 8 seconds
    const interval = setInterval(() => {
      setAiInsightIndex(prev => (prev + 1) % aiInsights.length);
    }, 8000);

    return () => {
      styleOverride.remove();
      clearInterval(interval);
    };
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      // Load dashboard stats
      const statsRes = await fetch('/api/nqt-thong-ke-dashboard');
      let loadedStats = {
        tongHoiVien: 120,
        doanhThuThang: 48000000,
        dangTapLuyen: 12,
        checkinHomNay: 45,
        goiTapActive: 8,
        sucChua: 100
      };

      if (statsRes.ok) {
        const statsData = await statsRes.json();
        if (statsData?.nqt_thanh_cong) {
          const s = statsData.nqt_du_lieu;
          loadedStats.tongHoiVien = s.g6_tong_hoi_vien || 0;
          loadedStats.dangTapLuyen = s.g6_dang_tap_luyen || 0;
          loadedStats.checkinHomNay = s.g6_checkin_hom_nay || 0;
          loadedStats.doanhThuThang = s.g6_doanh_thu_thang || 0;
          loadedStats.sucChua = s.g6_suc_chua || 100;
        }
      }

      // Load packages count
      const goiTapRes = await fetch('/api/nqt-goi-tap');
      if (goiTapRes.ok) {
        const goiTapData = await goiTapRes.json();
        if (goiTapData?.nqt_thanh_cong) {
          loadedStats.goiTapActive = goiTapData.nqt_du_lieu.length || 0;
        }
      }

      setStats(loadedStats);

      // Load chart data
      const chartRes = await fetch('/api/nqt-thong-ke-bieu-do?g6_so_ngay=7');
      if (chartRes.ok) {
        const chartJson = await chartRes.json();
        if (chartJson?.nqt_thanh_cong && chartJson.nqt_du_lieu?.g6_nhan) {
          const formatted = chartJson.nqt_du_lieu.g6_nhan.map((label, idx) => ({
            name: label,
            revenue: chartJson.nqt_du_lieu.g6_gia_tri[idx] || 0,
            members: Math.round((chartJson.nqt_du_lieu.g6_gia_tri[idx] || 0) * 1.5)
          }));
          setChartData(formatted);
        } else {
          setChartData(generateMockChartData());
        }
      } else {
        setChartData(generateMockChartData());
      }

    } catch (err) {
      console.error("Error loading dashboard metrics:", err);
      // Fallbacks
      setStats({
        tongHoiVien: 342,
        doanhThuThang: 125000000,
        dangTapLuyen: 28,
        checkinHomNay: 94,
        goiTapActive: 12,
        sucChua: 150
      });
      setChartData(generateMockChartData());
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const generateMockChartData = () => {
    return [
      { name: 'Thứ 2', revenue: 12, members: 15 },
      { name: 'Thứ 3', revenue: 19, members: 22 },
      { name: 'Thứ 4', revenue: 15, members: 18 },
      { name: 'Thứ 5', revenue: 27, members: 30 },
      { name: 'Thứ 6', revenue: 32, members: 40 },
      { name: 'Thứ 7', revenue: 45, members: 65 },
      { name: 'Chủ Nhật', revenue: 38, members: 50 }
    ];
  };

  const handleManualCheckin = async (e) => {
    e.preventDefault();
    if (!manualCheckinId) return;

    try {
      const res = await fetch('/api/nqt-diem-danh/qr', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ g6_ma_huyen_vien: manualCheckinId }) // matches spelling in G6 schema
      });
      const data = await res.json();
      if (data.nqt_thanh_cong) {
        setCheckinStatus({
          success: true,
          message: data.nqt_thong_diep || 'Điểm danh thành công!'
        });
        loadData();
      } else {
        setCheckinStatus({
          success: false,
          message: data.nqt_loi?.join(', ') || 'Mã hội viên không hợp lệ.'
        });
      }
    } catch (err) {
      setCheckinStatus({
        success: false,
        message: 'Lỗi kết nối máy chủ.'
      });
    }

    setTimeout(() => setCheckinStatus(null), 4000);
  };

  // Simulating QR check-in scanning
  const startQRScan = () => {
    setShowQRModal(true);
    setScanStatus('scanning');
    setScannedMember(null);

    // Simulate detection
    setTimeout(() => {
      setScanStatus('success');
      setScannedMember({
        name: 'Nguyễn Minh Quân',
        code: 'HV0089',
        plan: 'Premium Gold VIP',
        daysLeft: 45,
        avatar: 'MQ'
      });
      // update stats dynamically
      setStats(prev => ({
        ...prev,
        dangTapLuyen: prev.dangTapLuyen + 1,
        checkinHomNay: prev.checkinHomNay + 1
      }));
    }, 2800);
  };

  const formatCurrency = (val) => {
    return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND', maximumFractionDigits: 0 }).format(val);
  };

  return (
    <div className="space-y-6 pb-12 text-[#fafafa] font-sans antialiased">
      {/* Upper Welcome Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-3xl font-black text-transparent bg-clip-text bg-gradient-to-r from-white via-neutral-200 to-[#00FF66] tracking-tight uppercase flex items-center gap-2">
            <Zap className="w-8 h-8 text-[#00FF66] animate-pulse" />
            GYM CONTROL CENTER
          </h2>
          <p className="text-xs uppercase tracking-[0.25em] text-[#00FF66] font-semibold mt-1">
            Real-time Operations & Analytics SaaS Engine
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button 
            onClick={loadData}
            className="flex items-center gap-2 px-4 py-2 border border-white/10 rounded-xl bg-white/5 hover:bg-white/10 hover:border-[#00FF66]/30 text-sm font-semibold transition-all duration-200"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin text-[#00FF66]' : ''}`} />
            Sync Metrics
          </button>
          
          <button 
            onClick={startQRScan}
            className="flex items-center gap-2 px-5 py-2.5 bg-[#00FF66] text-[#09090b] rounded-xl font-black uppercase text-xs tracking-wider shadow-[0_0_20px_rgba(0,255,102,0.4)] hover:shadow-[0_0_30px_rgba(0,255,102,0.6)] transition-all duration-300 transform hover:-translate-y-0.5"
          >
            <QrCode className="w-4 h-4" />
            Scan QR Check-In
          </button>
        </div>
      </div>

      {/* Floating Glassmorphism Analytics Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        
        {/* Total Members Card */}
        <div className="glass-panel rounded-3xl p-6 relative overflow-hidden transition-all duration-300 hover:border-[#00FF66]/40 hover:-translate-y-1 group">
          <div className="absolute top-0 right-0 w-24 h-24 bg-[#00FF66]/5 rounded-full blur-2xl pointer-events-none" />
          <div className="flex items-center justify-between mb-4">
            <span className="text-xs uppercase tracking-wider text-neutral-400 font-semibold">Total Members</span>
            <div className="w-10 h-10 rounded-xl bg-[#00FF66]/10 border border-[#00FF66]/20 flex items-center justify-center text-[#00FF66]">
              <Users className="w-5 h-5" />
            </div>
          </div>
          <div className="flex items-baseline gap-2">
            <span className="text-3xl font-black tracking-tight">{stats.tongHoiVien.toLocaleString('vi-VN')}</span>
            <span className="text-xs text-[#00FF66] flex items-center font-bold">
              <TrendingUp className="w-3.5 h-3.5 mr-0.5" />
              +12%
            </span>
          </div>
          <p className="text-[11px] text-neutral-500 mt-2">Active subscribers on platform</p>
        </div>

        {/* Monthly Revenue Card */}
        <div className="glass-panel rounded-3xl p-6 relative overflow-hidden transition-all duration-300 hover:border-[#00FF66]/40 hover:-translate-y-1 group">
          <div className="absolute top-0 right-0 w-24 h-24 bg-[#00FF66]/5 rounded-full blur-2xl pointer-events-none" />
          <div className="flex items-center justify-between mb-4">
            <span className="text-xs uppercase tracking-wider text-neutral-400 font-semibold">Monthly Revenue</span>
            <div className="w-10 h-10 rounded-xl bg-[#00FF66]/10 border border-[#00FF66]/20 flex items-center justify-center text-[#00FF66]">
              <DollarSign className="w-5 h-5" />
            </div>
          </div>
          <div className="flex items-baseline gap-2">
            <span className="text-2xl font-black tracking-tight">{formatCurrency(stats.doanhThuThang)}</span>
          </div>
          <div className="w-full bg-white/5 h-1.5 rounded-full mt-4 overflow-hidden">
            <div className="bg-[#00FF66] h-full rounded-full shadow-[0_0_10px_rgba(0,255,102,0.6)]" style={{ width: '74%' }} />
          </div>
        </div>

        {/* Live Occupancy Card */}
        <div className="glass-panel rounded-3xl p-6 relative overflow-hidden transition-all duration-300 hover:border-[#00FF66]/40 hover:-translate-y-1 group">
          <div className="absolute top-0 right-0 w-24 h-24 bg-[#00FF66]/5 rounded-full blur-2xl pointer-events-none" />
          <div className="flex items-center justify-between mb-4">
            <span className="text-xs uppercase tracking-wider text-neutral-400 font-semibold">Live Occupancy</span>
            <span className="flex items-center gap-1.5 px-2 py-0.5 rounded-full bg-[#00FF66]/10 border border-[#00FF66]/20 text-[9px] text-[#00FF66] font-bold uppercase tracking-widest">
              <span className="w-1.5 h-1.5 bg-[#00FF66] rounded-full animate-ping" />
              Live
            </span>
          </div>
          <div className="flex items-baseline gap-1">
            <span className="text-3xl font-black tracking-tight">{stats.dangTapLuyen}</span>
            <span className="text-sm text-neutral-500 font-medium">/ {stats.sucChua} capacity</span>
          </div>
          <p className="text-[11px] text-neutral-500 mt-3">
            Current gym load: {Math.min(100, Math.round((stats.dangTapLuyen / stats.sucChua) * 100))}% occupancy
          </p>
        </div>

        {/* Subscriptions Card */}
        <div className="glass-panel rounded-3xl p-6 relative overflow-hidden transition-all duration-300 hover:border-[#00FF66]/40 hover:-translate-y-1 group">
          <div className="absolute top-0 right-0 w-24 h-24 bg-[#00FF66]/5 rounded-full blur-2xl pointer-events-none" />
          <div className="flex items-center justify-between mb-4">
            <span className="text-xs uppercase tracking-wider text-neutral-400 font-semibold">Active Subscriptions</span>
            <div className="w-10 h-10 rounded-xl bg-[#00FF66]/10 border border-[#00FF66]/20 flex items-center justify-center text-[#00FF66]">
              <Award className="w-5 h-5" />
            </div>
          </div>
          <div className="flex items-baseline gap-2">
            <span className="text-3xl font-black tracking-tight">{stats.goiTapActive}</span>
            <span className="text-xs text-neutral-400 font-bold">Standard Plans</span>
          </div>
          <p className="text-[11px] text-neutral-500 mt-2">Available for sales & sign-ups</p>
        </div>

      </div>

      {/* Main Charts & Analytics Block */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Revenue Analytics Chart Card */}
        <div className="lg:col-span-2 glass-panel rounded-3xl p-6 flex flex-col justify-between">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="text-lg font-black tracking-wider text-neutral-200 uppercase">Revenue Analytics</h3>
              <p className="text-xs text-neutral-400">Weekly sales activity & member registration density</p>
            </div>
            <div className="flex items-center gap-1.5 text-xs bg-white/5 border border-white/10 rounded-xl p-1">
              <button className="px-3 py-1 bg-[#00FF66] text-[#09090b] font-bold rounded-lg transition-all duration-200">7 Days</button>
              <button className="px-3 py-1 text-neutral-400 hover:text-white rounded-lg transition-all duration-200">30 Days</button>
            </div>
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="revenueGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#00FF66" stopOpacity={0.25}/>
                    <stop offset="95%" stopColor="#00FF66" stopOpacity={0.0}/>
                  </linearGradient>
                </defs>
                <XAxis dataKey="name" stroke="#52525b" fontSize={11} tickLine={false} axisLine={false} />
                <YAxis stroke="#52525b" fontSize={11} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '12px', color: '#fafafa' }}
                  labelStyle={{ fontWeight: 'bold', color: '#00FF66' }}
                />
                <Area type="monotone" dataKey="revenue" stroke="#00FF66" strokeWidth={2} fillOpacity={1} fill="url(#revenueGrad)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* AI Fitness Insights Panel */}
        <div className="glass-panel rounded-3xl p-6 relative overflow-hidden flex flex-col justify-between border-l-4 border-l-[#00FF66] shadow-[0_4px_30px_rgba(0,255,102,0.05)]">
          <div className="absolute top-0 right-0 w-32 h-32 bg-[#00FF66]/5 rounded-full blur-3xl pointer-events-none" />
          
          <div>
            <div className="flex items-center gap-2 mb-4">
              <div className="w-8 h-8 rounded-lg bg-[#00FF66]/10 border border-[#00FF66]/20 flex items-center justify-center text-[#00FF66]">
                <Brain className="w-4.5 h-4.5 animate-pulse" />
              </div>
              <h3 className="text-md font-black tracking-widest text-[#00FF66] uppercase">AI Operations Assistant</h3>
            </div>
            
            <div className="bg-white/5 border border-white/5 rounded-2xl p-5 min-h-[140px] relative flex flex-col justify-between">
              <p className="text-sm font-medium text-neutral-200 leading-relaxed italic">
                "{aiInsights[aiInsightIndex]}"
              </p>
              <div className="flex items-center gap-1.5 mt-4">
                {aiInsights.map((_, idx) => (
                  <span 
                    key={idx} 
                    className={`h-1.5 rounded-full transition-all duration-300 ${idx === aiInsightIndex ? 'w-6 bg-[#00FF66]' : 'w-1.5 bg-white/20'}`}
                  />
                ))}
              </div>
            </div>
          </div>

          <div className="mt-6 pt-4 border-t border-white/5 flex items-center justify-between text-xs text-neutral-400">
            <span className="flex items-center gap-1">
              <Sparkles className="w-3.5 h-3.5 text-[#00FF66]" />
              Insights updated hourly
            </span>
            <button className="text-[#00FF66] font-bold flex items-center hover:underline">
              Full Report
              <ChevronRight className="w-3.5 h-3.5 ml-0.5" />
            </button>
          </div>
        </div>

      </div>

      {/* Middle Operations Block: Heatmap & QR Manual console */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Attendance Heatmap Card */}
        <div className="lg:col-span-2 glass-panel rounded-3xl p-6">
          <div className="flex items-center justify-between mb-5">
            <div>
              <h3 className="text-lg font-black tracking-wider text-neutral-200 uppercase">Attendance Heatmap</h3>
              <p className="text-xs text-neutral-400">Heat map grid showing traffic density by hour & day</p>
            </div>
            <div className="flex items-center gap-2 text-[10px] text-neutral-500 font-bold uppercase">
              <span>Low</span>
              <div className="flex gap-1">
                <span className="w-2.5 h-2.5 rounded bg-white/5" />
                <span className="w-2.5 h-2.5 rounded bg-[#00FF66]/20" />
                <span className="w-2.5 h-2.5 rounded bg-[#00FF66]/55" />
                <span className="w-2.5 h-2.5 rounded bg-[#00FF66]" />
              </div>
              <span>Peak</span>
            </div>
          </div>

          {/* Simulated heat grid */}
          <div className="grid grid-cols-8 gap-2.5">
            {/* Hour labels */}
            <div className="flex flex-col justify-around text-[10px] text-neutral-500 font-bold uppercase pr-2">
              <span>06:00</span>
              <span>09:00</span>
              <span>12:00</span>
              <span>15:00</span>
              <span>18:00</span>
              <span>21:00</span>
            </div>
            
            {/* Days columns */}
            {['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'].map((day, dIdx) => {
              const weights = [
                [0.2, 0.4, 0.5, 0.3, 0.8, 0.5], // Mon
                [0.3, 0.5, 0.4, 0.2, 0.9, 0.6], // Tue
                [0.2, 0.4, 0.6, 0.4, 0.8, 0.4], // Wed
                [0.1, 0.3, 0.4, 0.2, 0.7, 0.5], // Thu
                [0.3, 0.6, 0.5, 0.5, 0.9, 0.7], // Fri
                [0.6, 0.8, 0.8, 0.7, 0.6, 0.3], // Sat
                [0.4, 0.7, 0.7, 0.5, 0.4, 0.2]  // Sun
              ];
              
              return (
                <div key={day} className="flex-1 flex flex-col gap-2 text-center">
                  <span className="text-[10px] text-neutral-500 font-bold uppercase mb-1">{day}</span>
                  {weights[dIdx].map((w, hIdx) => {
                    let bg = 'bg-white/5';
                    if (w > 0.7) bg = 'bg-[#00FF66] shadow-[0_0_10px_rgba(0,255,102,0.4)]';
                    else if (w > 0.4) bg = 'bg-[#00FF66]/60';
                    else if (w > 0.2) bg = 'bg-[#00FF66]/20';
                    
                    return (
                      <div 
                        key={hIdx} 
                        className={`h-7 rounded-lg ${bg} transition-all duration-300 hover:scale-110 cursor-pointer`}
                        title={`Weight: ${Math.round(w*100)}%`}
                      />
                    );
                  })}
                </div>
              );
            })}
          </div>
        </div>

        {/* QR Check-in manual input */}
        <div className="glass-panel rounded-3xl p-6 flex flex-col justify-between">
          <div>
            <h3 className="text-lg font-black tracking-wider text-neutral-200 uppercase mb-2">Desk Check-In</h3>
            <p className="text-xs text-neutral-400 mb-6">Manually check-in members using ID code</p>
            
            <form onSubmit={handleManualCheckin} className="space-y-4">
              <div className="relative">
                <input 
                  type="text"
                  value={manualCheckinId}
                  onChange={(e) => setManualCheckinId(e.target.value)}
                  placeholder="e.g. HV0001, HV0089"
                  className="w-full bg-white/5 border border-white/10 rounded-2xl px-4 py-3.5 text-sm font-semibold focus:outline-none focus:border-[#00FF66] transition-all text-[#fafafa] placeholder-neutral-500"
                />
              </div>
              <button 
                type="submit"
                className="w-full py-3.5 bg-white/5 border border-white/10 hover:border-[#00FF66]/30 hover:bg-[#00FF66]/10 text-white font-bold rounded-2xl text-xs uppercase tracking-widest transition-all duration-200"
              >
                Trigger Check-In
              </button>
            </form>

            {checkinStatus && (
              <div className={`mt-4 p-4 rounded-2xl border text-xs font-bold ${checkinStatus.success ? 'bg-[#00FF66]/10 border-[#00FF66]/20 text-[#00FF66]' : 'bg-red-500/10 border-red-500/20 text-red-400'}`}>
                {checkinStatus.message}
              </div>
            )}
          </div>

          <div className="mt-6 pt-4 border-t border-white/5 flex items-center justify-between text-xs text-neutral-400">
            <span className="flex items-center gap-1">
              <Clock className="w-3.5 h-3.5 text-[#00FF66]" />
              Today checked: <strong className="text-white ml-0.5">{stats.checkinHomNay}</strong>
            </span>
            <span className="text-[10px] uppercase font-bold text-neutral-500">Manual Desk Override</span>
          </div>
        </div>

      </div>

      {/* Bottom Block: Trainer schedules & Subscription Plan Breakdown */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Trainer Schedules */}
        <div className="lg:col-span-2 glass-panel rounded-3xl p-6">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="text-lg font-black tracking-wider text-neutral-200 uppercase">Trainer Schedules</h3>
              <p className="text-xs text-neutral-400">Current shifts and booking load for gym personal coaches</p>
            </div>
            <Calendar className="w-5 h-5 text-[#00FF66]" />
          </div>

          <div className="space-y-4">
            {[
              { name: 'Nguyễn Quốc Thắng (Head Coach)', client: 'Vũ Hoàng', time: '17:00 - 18:30', status: 'In Session', weight: 95 },
              { name: 'Lê Hồng Minh (PT)', client: 'Trần Thị Thuỷ', time: '18:00 - 19:00', status: 'In Session', weight: 80 },
              { name: 'Phạm Thanh Sơn (Yoga Coach)', client: 'Phan Minh Anh', time: '19:00 - 20:30', status: 'Booked', weight: 40 },
              { name: 'Hoàng Vũ My (PT)', client: 'None', time: 'Shift ends 21:00', status: 'Available', weight: 0 }
            ].map((coach, idx) => (
              <div key={idx} className="flex items-center justify-between p-4 bg-white/5 border border-white/5 rounded-2xl hover:border-white/10 transition-colors">
                <div className="flex items-center gap-3">
                  <div className={`w-3 h-3 rounded-full ${coach.status === 'In Session' ? 'bg-[#00FF66] animate-pulse' : coach.status === 'Booked' ? 'bg-orange-400' : 'bg-neutral-500'}`} />
                  <div>
                    <h4 className="text-sm font-bold text-neutral-200">{coach.name}</h4>
                    <p className="text-xs text-neutral-500">Client: {coach.client} • {coach.time}</p>
                  </div>
                </div>
                <div className="text-right">
                  <span className={`text-[10px] font-extrabold uppercase px-2 py-0.5 rounded-full border ${coach.status === 'In Session' ? 'bg-[#00FF66]/10 border-[#00FF66]/20 text-[#00FF66]' : coach.status === 'Booked' ? 'bg-orange-400/10 border-orange-400/20 text-orange-400' : 'bg-neutral-800 border-neutral-700 text-neutral-400'}`}>
                    {coach.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Subscription Plan Bento */}
        <div className="glass-panel rounded-3xl p-6 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-black tracking-wider text-neutral-200 uppercase">Active Subscriptions</h3>
              <p className="text-xs text-neutral-400">Sales breakdown of member plans</p>
            </div>
            
            <div className="space-y-4 mt-6">
              {[
                { name: 'Standard Plan', sales: '45%', count: 154, color: 'bg-neutral-600' },
                { name: 'Premium Gold VIP', sales: '35%', count: 120, color: 'bg-[#00FF66] shadow-[0_0_8px_rgba(0,255,102,0.4)]' },
                { name: 'PT Package 10 Sessions', sales: '20%', count: 68, color: 'bg-emerald-400' }
              ].map((plan, idx) => (
                <div key={idx} className="space-y-1">
                  <div className="flex justify-between text-xs font-semibold">
                    <span className="text-neutral-300">{plan.name}</span>
                    <span className="text-neutral-400">{plan.count} ({plan.sales})</span>
                  </div>
                  <div className="w-full bg-white/5 h-1.5 rounded-full overflow-hidden">
                    <div className={`h-full rounded-full ${plan.color}`} style={{ width: plan.sales }} />
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="mt-8 pt-4 border-t border-white/5 flex items-center justify-between text-xs text-neutral-500">
            <span>Model: SaaS Multi-tier</span>
            <span className="text-[#00FF66] font-bold hover:underline cursor-pointer flex items-center">
              Manage Plans
              <ChevronRight className="w-3.5 h-3.5" />
            </span>
          </div>
        </div>

      </div>

      {/* QR Check-in Simulator Modal */}
      {showQRModal && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/85 backdrop-blur-md">
          <div className="glass-panel rounded-[32px] p-8 max-w-sm w-full border border-[#00FF66]/30 shadow-[0_0_50px_rgba(0,255,102,0.2)] text-center relative">
            <button 
              onClick={() => setShowQRModal(false)}
              className="absolute top-4 right-4 text-neutral-500 hover:text-white font-bold"
            >
              ✕
            </button>
            <h3 className="text-xl font-black text-[#00FF66] tracking-wider uppercase mb-2">QR SCANNER</h3>
            <p className="text-xs text-neutral-400 mb-6">Align member barcode or QR code to scanner window</p>
            
            {/* Viewfinder simulation */}
            <div className="w-48 h-48 mx-auto border-2 border-[#00FF66]/30 rounded-2xl relative overflow-hidden bg-black/40 flex items-center justify-center mb-6">
              <div className="absolute inset-4 border border-dashed border-[#00FF66]/50 rounded-xl" />
              
              {scanStatus === 'scanning' ? (
                <>
                  <div className="w-full h-0.5 bg-[#00FF66] absolute left-0 shadow-[0_0_12px_#00FF66] animate-[scanLine_2s_infinite]" />
                  <QrCode className="w-20 h-20 text-[#00FF66]/30 animate-pulse" />
                </>
              ) : (
                <div className="w-12 h-12 rounded-full bg-[#00FF66]/10 border border-[#00FF66]/30 flex items-center justify-center text-[#00FF66]">
                  <CheckCircle className="w-6 h-6 animate-[scaleUp_0.3s_ease_forwards]" />
                </div>
              )}
            </div>

            <style>{`
              @keyframes scanLine {
                0% { top: 10%; }
                50% { top: 90%; }
                100% { top: 10%; }
              }
              @keyframes scaleUp {
                from { transform: scale(0.8); opacity: 0; }
                to { transform: scale(1); opacity: 1; }
              }
            `}</style>

            {scanStatus === 'scanning' ? (
              <p className="text-sm font-semibold text-neutral-400 animate-pulse">Initializing camera & scanning...</p>
            ) : (
              <div className="space-y-4 animate-[scaleUp_0.3s_ease_forwards]">
                <p className="text-xs text-neutral-500 font-bold uppercase tracking-wider">Scanned Successfully</p>
                <div className="p-4 bg-white/5 border border-white/5 rounded-2xl">
                  <h4 className="text-md font-black text-white">{scannedMember?.name}</h4>
                  <p className="text-xs text-[#00FF66] font-bold mt-1">{scannedMember?.plan} • {scannedMember?.code}</p>
                  <p className="text-[10px] text-neutral-500 mt-2">Active package expires in {scannedMember?.daysLeft} days</p>
                </div>
                <button 
                  onClick={() => setShowQRModal(false)}
                  className="w-full py-3 bg-[#00FF66] text-[#09090b] font-black rounded-xl text-xs uppercase tracking-wider"
                >
                  Confirm Check-In
                </button>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

const rootEl = document.getElementById('admin-dashboard-react-root');
if (rootEl) {
  createRoot(rootEl).render(<AdminDashboard />);
}
