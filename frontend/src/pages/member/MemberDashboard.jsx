import React, { useState, useEffect } from 'react';
import { 
  LayoutDashboard, Calendar, History, Package, User, 
  Bell, LogOut, CheckCircle2, TrendingUp, Activity, 
  QrCode, UserCircle2, MessageSquare, Info, Zap
} from 'lucide-react';
import { 
  AreaChart, Area, XAxis, YAxis, CartesianGrid, 
  Tooltip, ResponsiveContainer, LineChart, Line 
} from 'recharts';
import { motion, AnimatePresence } from 'framer-motion';

/**
 * IRONCORE GYM - Member Dashboard
 * Aesthetic: Luxury Glassmorphism
 * Theme: Gold / Deep Black
 */

const MemberDashboard = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [loading, setLoading] = useState(true);

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

  // Mock fallbacks for missing APIs
  const mockTrainer = {
    g6_ho_ten: "Chưa đăng ký",
    g6_chuyen_mon: "Vui lòng chọn HLV",
    g6_anh_the: "https://ui-avatars.com/api/?name=PT&background=0D8ABC&color=fff"
  };

  useEffect(() => {
    const fetchRealData = async () => {
      const token = localStorage.getItem('nqt_access_token');
      if (!token) {
        window.location.href = '/login';
        return;
      }

      const headers = {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      };

      try {
        // Fetch Profile & Package
        const resProfile = await fetch('/api/nqt-hoi-vien/toi', { headers });
        if (resProfile.status === 401) throw new Error('Unauthorized');
        const dataProfile = await resProfile.json();
        if (dataProfile.nqt_thanh_cong) {
          setProfile(dataProfile.nqt_du_lieu.nqt_hoi_vien || {});
          setActivePackage(dataProfile.nqt_du_lieu.nqt_goi_hien_tai || null);
        }

        // Fetch Attendance
        const resAtt = await fetch('/api/nqt-hoi-vien/diem-danh?g6_gioi_han=5', { headers });
        const dataAtt = await resAtt.json();
        if (dataAtt.nqt_thanh_cong) setAttendance(dataAtt.nqt_du_lieu || []);

        // Fetch Metrics
        const resMetrics = await fetch('/api/nqt-hoi-vien/toi/nqt-chi-so', { headers });
        const dataMetrics = await resMetrics.json();
        if (dataMetrics.nqt_thanh_cong) {
          // Format for Recharts: newest last
          const formattedMetrics = (dataMetrics.nqt_du_lieu || [])
            .reverse()
            .map(m => ({
              name: m.g6_ngay_do.substring(5, 10), // MM-DD
              weight: m.g6_can_nang,
              fat: m.g6_ty_le_mo || 0
            }));
          setMetrics(formattedMetrics);
        }

        setLoading(false);
      } catch (error) {
        // Handle 401 or error
        localStorage.removeItem('nqt_access_token');
        localStorage.removeItem('nqt_refresh_token');
        window.location.href = '/login';
      }
    };

    fetchRealData();
  }, []);

  useEffect(() => {
    if (activeTab === 'dashboard') return;
    const fetchTabData = async () => {
      setTabLoading(true);
      const token = localStorage.getItem('nqt_access_token');
      const headers = { 'Authorization': `Bearer ${token}` };
      
      try {
        if (activeTab === 'history') {
          const res = await fetch('/api/nqt-hoi-vien/diem-danh', { headers });
          const data = await res.json();
          if (data.nqt_thanh_cong) setFullHistory(data.nqt_du_lieu || []);
        } else if (activeTab === 'packages') {
          const resMyPkgs = await fetch('/api/nqt-dang-ky-goi-tap', { headers });
          const resAllPkgs = await fetch('/api/nqt-goi-tap');
          const dataMy = await resMyPkgs.json();
          const dataAll = await resAllPkgs.json();
          setPackages({
            active: dataMy.nqt_thanh_cong ? dataMy.nqt_du_lieu : [],
            available: dataAll.nqt_thanh_cong ? dataAll.nqt_du_lieu : []
          });
        } else if (activeTab === 'classes') {
          const res = await fetch('/api/nxv-lich-lop-hoc');
          const data = await res.json();
          if (data.nqt_thanh_cong) setClasses(data.nqt_du_lieu || []);
        } else if (activeTab === 'pt') {
          const resMyPt = await fetch('/api/nxv-dang-ky-pt', { headers });
          const resAllPt = await fetch('/api/nxv-hlv');
          const dataMy = await resMyPt.json();
          const dataAll = await resAllPt.json();
          setPts({
            active: dataMy.nqt_thanh_cong && dataMy.nqt_du_lieu.length > 0 ? dataMy.nqt_du_lieu[0] : null,
            available: dataAll.nqt_thanh_cong ? dataAll.nqt_du_lieu : []
          });
        }
      } catch (e) {
        console.error(e);
      }
      setTabLoading(false);
    };
    fetchTabData();
  }, [activeTab]);

  if (loading) return <SkeletonLoader />;

  // Calculate days left
  let daysLeft = 'Hết hạn';
  if (activePackage && activePackage.g6_ngay_het_han) {
    const end = new Date(activePackage.g6_ngay_het_han);
    const now = new Date();
    const diffTime = end - now;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    daysLeft = diffDays > 0 ? `${diffDays} ngày` : 'Đã hết hạn';
  }

  return (
    <div className="min-h-screen bg-[#0A0A0A] text-[#F5F5F0] font-sans selection:bg-[#C9A84C]/30 overflow-hidden flex">
      
      {/* --- Sidebar --- */}
      <aside className="w-72 bg-white/5 backdrop-blur-2xl border-r border-white/10 flex flex-col h-screen sticky top-0 z-50">
        <div className="p-8 border-b border-white/5 text-center">
          <h1 className="text-3xl font-black tracking-[4px] text-[#C9A84C]">IRONCORE</h1>
          <p className="text-[10px] uppercase tracking-[3px] text-[#A1A1AA] font-bold mt-1">Member Portal</p>
        </div>

        {/* Profile Card */}
        <div className="p-6">
          <div className="bg-white/5 rounded-2xl p-4 border border-white/10 hover:border-[#C9A84C]/30 transition-all group">
            <div className="flex items-center space-x-3 mb-4">
              <img src={profile.g6_anh_the || "https://ui-avatars.com/api/?name="+encodeURIComponent(profile.g6_ho_ten||'HV')+"&background=1C1C1C&color=C9A84C"} className="w-12 h-12 rounded-xl object-cover border border-[#C9A84C]/20 group-hover:scale-105 transition-transform" />
              <div>
                <h3 className="font-bold text-sm leading-none">{profile.g6_ho_ten || 'Hội viên'}</h3>
                <p className="text-[10px] text-slate-500 mt-1">{profile.g6_ma_qr || `ID: ${profile.g6_ma_hoi_vien}`}</p>
              </div>
            </div>
            <div className="flex justify-between items-center bg-[#C9A84C]/5 rounded-lg p-2 border border-[#C9A84C]/10">
              <QrCode size={16} className="text-[#C9A84C]" />
              <span className="text-[9px] font-bold text-[#C9A84C] tracking-widest">SHOW QR CODE</span>
            </div>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 px-4 space-y-1">
          <NavItem icon={<LayoutDashboard size={20}/>} label="Dashboard" active={activeTab === 'dashboard'} onClick={() => setActiveTab('dashboard')} />
          <NavItem icon={<Calendar size={20}/>} label="Lịch tập" active={activeTab === 'classes'} onClick={() => setActiveTab('classes')} />
          <NavItem icon={<History size={20}/>} label="Lịch sử" active={activeTab === 'history'} onClick={() => setActiveTab('history')} />
          <NavItem icon={<Package size={20}/>} label="Gói tập" active={activeTab === 'packages'} onClick={() => setActiveTab('packages')} />
          <NavItem icon={<UserCircle2 size={20}/>} label="PT Cá nhân" active={activeTab === 'pt'} onClick={() => setActiveTab('pt')} />
        </nav>

        <div className="p-6 border-t border-white/5">
          <button 
            onClick={() => {
              localStorage.removeItem('nqt_access_token');
              localStorage.removeItem('nqt_refresh_token');
              window.location.href = '/login';
            }}
            className="w-full flex items-center space-x-3 px-4 py-3 rounded-xl text-slate-400 hover:bg-red-500/10 hover:text-red-400 transition-all text-sm font-bold"
          >
            <LogOut size={18} />
            <span>Đăng xuất</span>
          </button>
        </div>
      </aside>

      {/* --- Main Content --- */}
      <main className="flex-1 p-8 overflow-y-auto h-screen custom-scrollbar relative">
        
        {/* Ambient Glows */}
        <div className="fixed top-[-10%] right-[-10%] w-[50%] h-[50%] bg-[#C9A84C]/5 blur-[120px] rounded-full pointer-events-none"></div>
        <div className="fixed bottom-[-10%] left-[-10%] w-[40%] h-[40%] bg-[#C9A84C]/5 blur-[120px] rounded-full pointer-events-none"></div>

        {tabLoading && activeTab !== 'dashboard' ? (
          <div className="h-full flex flex-col items-center justify-center text-center">
            <div className="w-12 h-12 border-4 border-[#C9A84C]/20 border-t-[#C9A84C] rounded-full animate-spin mb-4"></div>
            <p className="text-[#C9A84C] font-bold uppercase tracking-widest text-sm">Đang tải dữ liệu...</p>
          </div>
        ) : (
          <>
            {activeTab === 'history' && <HistoryView history={fullHistory} />}
            {activeTab === 'packages' && <PackagesView packages={packages} />}
            {activeTab === 'classes' && <ClassesView classes={classes} />}
            {activeTab === 'pt' && <PTView pts={pts} />}
            
            {activeTab === 'dashboard' && (
              <>
            {/* Header */}
            <header className="flex justify-between items-end mb-10 relative z-10">
          <div>
            <h2 className="text-3xl font-black tracking-tight flex items-center">
              Chào ngày mới, <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#C9A84C] to-[#E5C76B] ml-2">{profile.g6_ho_ten || 'bạn'}</span>
              <Zap className="ml-3 text-[#C9A84C] fill-[#C9A84C]/20" size={24} />
            </h2>
            <p className="text-[#A1A1AA] mt-1 font-medium italic">"The only bad workout is the one that didn't happen."</p>
          </div>
          
          <div className="flex items-center space-x-4">
            <div className="relative">
              <button className="w-12 h-12 bg-white/5 rounded-2xl flex items-center justify-center border border-white/10 hover:bg-white/10 transition-all relative">
                <Bell size={20} className="text-[#A1A1AA]" />
                <span className="absolute top-3 right-3 w-2 h-2 bg-[#C9A84C] rounded-full shadow-[0_0_10px_#C9A84C]"></span>
              </button>
            </div>
          </div>
        </header>

        {/* Stats Row */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
          <StatCard title="Hạn hội viên" value={daysLeft} sub={`Hết hạn: ${activePackage ? activePackage.g6_ngay_het_han : 'Chưa đăng ký'}`} icon={<Calendar className="text-[#C9A84C]" />} cyan />
          <StatCard title="Check-in gần đây" value={attendance.length} sub="Lượt điểm danh" icon={<CheckCircle2 className="text-[#C9A84C]" />} />
          <StatCard title="Điểm tích lũy" value={profile.g6_tong_diem || 0} sub="Tích lũy từ giao dịch" icon={<Zap className="text-[#C9A84C]" />} />
          <StatCard title="BMI mới nhất" value={metrics.length ? (metrics[metrics.length-1].weight / Math.pow(profile.g6_chieu_cao||1.7, 2)).toFixed(1) : '--'} sub="Dựa trên chỉ số gần nhất" icon={<Activity className="text-[#C9A84C]" />} />
        </div>

        {/* Center Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-10">
          {/* Calendar Widget */}
          <div className="lg:col-span-2 bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl p-8 relative overflow-hidden">
            <div className="flex justify-between items-center mb-8">
              <h3 className="font-bold text-xl flex items-center"><Calendar size={20} className="mr-3 text-[#C9A84C]"/> Lịch tập tuần này</h3>
              <div className="flex bg-white/5 rounded-xl p-1 border border-white/10">
                <button className="px-4 py-1.5 rounded-lg text-xs font-bold bg-[#C9A84C] text-[#0A0A0A] shadow-[0_0_15px_rgba(201,168,76,0.4)]">Tất cả</button>
                <button className="px-4 py-1.5 rounded-lg text-xs font-bold text-[#A1A1AA] hover:text-[#F5F5F0] transition-colors">Lớp học</button>
              </div>
            </div>
            
            <div className="grid grid-cols-7 gap-4 text-center">
              {['T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'CN'].map((day, i) => (
                <div key={day} className="space-y-4">
                  <p className="text-[10px] font-bold text-[#A1A1AA] uppercase tracking-widest">{day}</p>
                  <div className={`h-24 rounded-2xl border flex flex-col items-center justify-center space-y-2 transition-all ${i === 2 ? 'bg-[#C9A84C]/10 border-[#C9A84C]/30' : 'bg-white/5 border-white/5 hover:border-white/10'}`}>
                    <span className="text-lg font-black">{12 + i}</span>
                    {i === 2 && <div className="w-1.5 h-1.5 bg-[#C9A84C] rounded-full shadow-[0_0_8px_#C9A84C]"></div>}
                    {i === 4 && <div className="w-1.5 h-1.5 bg-[#C9A84C] opacity-50 rounded-full"></div>}
                  </div>
                </div>
              ))}
            </div>

            <div className="mt-8 space-y-4">
              <EventItem time="17:30 - 18:30" title="Yoga Flow — Studio A" mentor="Coach Linh" type="class" />
              <EventItem time="19:00 - 20:00" title="PT Boxing — Zone 3" mentor="Coach Alex" type="pt" active />
            </div>
          </div>

          {/* Biểu đồ Recharts */}
          <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl p-8">
            <h3 className="font-bold text-xl mb-8 flex items-center"><TrendingUp size={20} className="mr-3 text-[#C9A84C]"/> Tiến trình cơ thể</h3>
            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={metrics}>
                  <defs>
                    <linearGradient id="colorWeight" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#C9A84C" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="#C9A84C" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                  <XAxis dataKey="name" stroke="#A1A1AA" fontSize={10} axisLine={false} tickLine={false} />
                  <YAxis hide domain={['dataMin - 2', 'dataMax + 2']} />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#1C1C1C', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '12px', fontSize: '12px' }}
                    itemStyle={{ color: '#C9A84C' }}
                  />
                  <Area type="monotone" dataKey="weight" stroke="#C9A84C" strokeWidth={3} fillOpacity={1} fill="url(#colorWeight)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
            <div className="mt-8 flex justify-between items-center p-4 bg-white/5 rounded-2xl border border-white/5">
              <div>
                <p className="text-[10px] text-slate-500 uppercase font-bold tracking-widest mb-1">Cân nặng mới nhất</p>
                <p className="text-xl font-black">{metrics.length > 0 ? metrics[metrics.length-1].weight : '--'} <span className="text-xs text-slate-500">KG</span></p>
              </div>
              <div className="text-right">
                <p className="text-[10px] text-slate-500 uppercase font-bold tracking-widest mb-1">Giảm tháng này</p>
                <p className="text-xl font-black text-emerald-400">-2.0 <span className="text-xs text-emerald-400/50">KG</span></p>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom Row */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 pb-10">
          {/* Attendance History */}
          <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl p-8">
            <h3 className="font-bold text-xl mb-8 flex items-center"><History size={20} className="mr-3 text-[#C9A84C]"/> Điểm danh gần đây</h3>
            <div className="space-y-4">
              {attendance.map((item, idx) => (
                <div key={item.g6_ma_diem_danh || idx} className="flex items-center justify-between p-4 bg-white/5 hover:bg-white/10 rounded-2xl transition-all border border-transparent hover:border-white/5">
                  <div className="flex items-center space-x-4">
                    <div className="w-10 h-10 bg-[#C9A84C]/10 rounded-full flex items-center justify-center text-[#C9A84C]">
                      <Activity size={18} />
                    </div>
                    <div>
                      <p className="text-sm font-bold text-[#F5F5F0]">{item.g6_thoi_gian_vao ? item.g6_thoi_gian_vao.replace('T', ' ') : '--'}</p>
                      <p className="text-[10px] text-[#A1A1AA] uppercase tracking-widest font-bold">Check-in</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-bold text-[#F5F5F0]">{item.g6_thoi_gian_ra ? item.g6_thoi_gian_ra.replace('T', ' ') : 'Đang tập'}</p>
                    <p className="text-[10px] text-[#A1A1AA] uppercase tracking-widest font-bold">Check-out</p>
                  </div>
                </div>
              ))}
              {attendance.length === 0 && (
                <p className="text-center text-[#A1A1AA] text-sm italic">Chưa có dữ liệu điểm danh</p>
              )}
            </div>
          </div>

          {/* Trainer Card */}
          <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl p-8 relative overflow-hidden group">
            <div className="absolute top-0 right-0 p-8 opacity-5 group-hover:rotate-12 transition-transform duration-500">
              <Zap size={120} className="text-[#C9A84C]" />
            </div>
            <h3 className="font-bold text-xl mb-8 flex items-center"><User size={20} className="mr-3 text-[#C9A84C]"/> Huấn luyện viên cá nhân</h3>
            <div className="flex flex-col items-center py-6">
              <div className="relative mb-6">
                <img src={mockTrainer.g6_anh_the} className="w-24 h-24 rounded-full object-cover border-4 border-[#C9A84C]/20 shadow-[0_0_30px_rgba(201,168,76,0.2)]" />
                <div className="absolute bottom-1 right-1 w-5 h-5 bg-[#C9A84C] rounded-full border-4 border-[#0A0A0A]"></div>
              </div>
              <h4 className="text-2xl font-black">{mockTrainer.g6_ho_ten}</h4>
              <p className="text-[#C9A84C] text-sm font-bold tracking-widest uppercase mt-2 mb-8">{mockTrainer.g6_chuyen_mon}</p>
              
              <div className="flex space-x-4 w-full max-w-xs relative z-10">
                <button className="flex-1 bg-white/5 hover:bg-white/10 border border-white/10 py-3 rounded-2xl flex items-center justify-center space-x-2 transition-all font-bold text-sm">
                  <MessageSquare size={18} />
                  <span>Nhắn tin</span>
                </button>
                <button className="flex-1 bg-[#C9A84C] hover:bg-[#E5C76B] text-[#0A0A0A] py-3 rounded-2xl flex items-center justify-center space-x-2 transition-all font-bold text-sm shadow-[0_0_20px_rgba(201,168,76,0.3)]">
                  <Calendar size={18} />
                  <span>Đặt lịch</span>
                </button>
              </div>
            </div>
          </div>
        </div>
          </>
        )}
          </>
        )}
      </main>

      <style dangerouslySetInnerHTML={{ __html: `
        .custom-scrollbar::-webkit-scrollbar { width: 4px; }
        .custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(201, 168, 76, 0.2); border-radius: 10px; }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover { background: rgba(201, 168, 76, 0.4); }
      `}} />
    </div>
  );
};

// --- Sub-components ---

const NavItem = ({ icon, label, active, onClick }) => (
  <button 
    onClick={onClick}
    className={`w-full flex items-center space-x-4 px-6 py-4 rounded-2xl transition-all duration-300 relative group ${active ? 'text-[#C9A84C]' : 'text-[#A1A1AA] hover:text-[#F5F5F0] hover:bg-white/5'}`}
  >
    {active && <motion.div layoutId="activeNav" className="absolute inset-0 bg-[#C9A84C]/10 border border-[#C9A84C]/20 rounded-2xl" />}
    <div className={`relative z-10 transition-transform duration-300 group-hover:scale-110 ${active ? 'text-[#C9A84C] drop-shadow-[0_0_8px_rgba(201,168,76,0.5)]' : ''}`}>
      {icon}
    </div>
    <span className="relative z-10 font-bold text-sm uppercase tracking-widest">{label}</span>
  </button>
);

const StatCard = ({ title, value, sub, icon, cyan }) => (
  <div className={`bg-white/5 backdrop-blur-xl border border-white/10 p-6 rounded-3xl relative overflow-hidden group hover:border-white/20 transition-all ${cyan ? 'shadow-[0_0_30px_rgba(201,168,76,0.05)]' : ''}`}>
    <div className="flex justify-between items-start mb-4">
      <div className="p-3 bg-white/5 rounded-2xl border border-white/5 group-hover:bg-white/10 transition-all">
        {icon}
      </div>
      <Info size={14} className="text-[#A1A1AA] hover:text-[#F5F5F0] cursor-help" />
    </div>
    <h4 className="text-[#A1A1AA] text-[10px] font-bold uppercase tracking-[2px] mb-1">{title}</h4>
    <div className="text-3xl font-black mb-1 text-[#F5F5F0]">{value}</div>
    <p className="text-[10px] text-[#A1A1AA] font-medium italic">{sub}</p>
    <div className={`absolute bottom-0 left-0 h-1 bg-gradient-to-r from-transparent via-[#C9A84C]/30 to-transparent w-0 group-hover:w-full transition-all duration-700`}></div>
  </div>
);

const EventItem = ({ time, title, mentor, type, active }) => (
  <div className={`p-4 rounded-2xl border transition-all flex items-center justify-between group ${active ? 'bg-[#C9A84C]/10 border-[#C9A84C]/30' : 'bg-white/5 border-white/5 hover:border-white/10'}`}>
    <div className="flex items-center space-x-4">
      <div className={`w-2 h-10 rounded-full ${active ? 'bg-[#C9A84C]' : 'bg-white/10'}`}></div>
      <div>
        <p className={`text-[10px] font-bold uppercase tracking-widest ${active ? 'text-[#C9A84C]' : 'text-[#A1A1AA]'}`}>{time}</p>
        <h4 className="text-sm font-black text-[#F5F5F0]">{title}</h4>
        <p className="text-xs text-[#A1A1AA]">{mentor}</p>
      </div>
    </div>
    <button className={`p-2 rounded-xl border transition-all ${active ? 'bg-[#C9A84C] text-[#0A0A0A] border-[#C9A84C]' : 'border-white/10 text-[#A1A1AA] hover:text-[#F5F5F0]'}`}>
      <motion.div whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.9 }}>
        <MessageSquare size={16} />
      </motion.div>
    </button>
  </div>
);

const SkeletonLoader = () => (
  <div className="min-h-screen bg-[#0A0A0A] p-8 flex items-center justify-center">
    <div className="flex flex-col items-center space-y-4">
      <div className="w-16 h-16 border-4 border-[#C9A84C]/20 border-t-[#C9A84C] rounded-full animate-spin"></div>
      <p className="text-[#C9A84C] font-header tracking-widest animate-pulse uppercase font-black italic">IRONCORE AUTHENTICATING...</p>
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
    <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl p-8">
      {history.length === 0 ? (
        <p className="text-[#A1A1AA] italic text-center py-10">Bạn chưa có lịch sử điểm danh nào.</p>
      ) : (
        <div className="space-y-4">
          {history.map((item, idx) => (
            <div key={idx} className="flex items-center justify-between p-6 bg-white/5 hover:bg-white/10 rounded-2xl transition-all border border-transparent hover:border-white/5">
              <div className="flex items-center space-x-6">
                <div className="w-12 h-12 bg-[#C9A84C]/10 rounded-full flex items-center justify-center text-[#C9A84C]">
                  <Activity size={20} />
                </div>
                <div>
                  <p className="text-lg font-bold text-[#F5F5F0]">{item.g6_thoi_gian_vao ? item.g6_thoi_gian_vao.replace('T', ' ') : '--'}</p>
                  <p className="text-xs text-[#A1A1AA] uppercase tracking-widest font-bold mt-1">Giờ Vào (Check-in)</p>
                </div>
              </div>
              <div className="text-right">
                <p className="text-lg font-bold text-[#F5F5F0]">{item.g6_thoi_gian_ra ? item.g6_thoi_gian_ra.replace('T', ' ') : 'Đang tập'}</p>
                <p className="text-xs text-[#A1A1AA] uppercase tracking-widest font-bold mt-1">Giờ Ra (Check-out)</p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  </div>
);

const PackagesView = ({ packages }) => (
  <div className="space-y-8">
    <h2 className="text-3xl font-black tracking-tight flex items-center mb-8">
      <Package size={28} className="mr-4 text-[#C9A84C]" />
      Gói tập <span className="text-[#C9A84C] ml-2">Của Tôi</span>
    </h2>
    
    <div className="bg-gradient-to-r from-[#C9A84C]/20 to-transparent p-[1px] rounded-3xl">
      <div className="bg-[#1C1C1C] rounded-3xl p-8 border border-white/5 relative overflow-hidden">
        <Zap className="absolute top-4 right-4 text-[#C9A84C] opacity-20" size={100} />
        {packages.active.length > 0 ? packages.active.map((pkg, idx) => (
          <div key={idx} className="relative z-10">
            <h3 className="text-2xl font-black mb-2 text-[#C9A84C] uppercase tracking-widest">{pkg.g6_ten_goi_tap || 'Gói Hội Viên'}</h3>
            <p className="text-[#A1A1AA] mb-6">Trạng thái: <span className="text-emerald-400 font-bold">Đang kích hoạt</span></p>
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-white/5 p-4 rounded-xl border border-white/5">
                <p className="text-[10px] text-[#A1A1AA] uppercase font-bold tracking-widest mb-1">Ngày đăng ký</p>
                <p className="font-bold">{pkg.g6_ngay_dang_ky}</p>
              </div>
              <div className="bg-white/5 p-4 rounded-xl border border-white/5">
                <p className="text-[10px] text-[#A1A1AA] uppercase font-bold tracking-widest mb-1">Ngày hết hạn</p>
                <p className="font-bold text-[#F5F5F0]">{pkg.g6_ngay_het_han}</p>
              </div>
            </div>
          </div>
        )) : (
          <div className="relative z-10 text-center py-8">
            <p className="text-[#A1A1AA] italic mb-4">Bạn chưa đăng ký gói tập nào hoặc gói đã hết hạn.</p>
          </div>
        )}
      </div>
    </div>

    <h3 className="text-xl font-bold mt-12 mb-6 uppercase tracking-widest text-[#A1A1AA]">Mua thêm / Gia hạn</h3>
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      {packages.available.map((pkg, idx) => (
        <div key={idx} className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-6 hover:border-[#C9A84C]/50 transition-all flex flex-col h-full group">
          <h4 className="font-black text-lg mb-2 text-[#F5F5F0]">{pkg.g6_ten_goi}</h4>
          <p className="text-2xl font-black text-[#C9A84C] mb-4">{parseInt(pkg.g6_gia_tien).toLocaleString()}đ</p>
          <div className="flex-1">
            <p className="text-sm text-[#A1A1AA] mb-6">{pkg.g6_mo_ta || 'Gói tập tiêu chuẩn tại hệ thống Ironcore Gym.'}</p>
          </div>
          <button className="w-full py-3 bg-white/5 hover:bg-[#C9A84C] hover:text-[#0A0A0A] border border-white/10 rounded-xl transition-all font-bold text-sm tracking-widest uppercase">
            Đăng ký ngay
          </button>
        </div>
      ))}
      {packages.available.length === 0 && <p className="text-[#A1A1AA] italic">Không có gói tập nào đang mở bán.</p>}
    </div>
  </div>
);

const ClassesView = ({ classes }) => (
  <div className="space-y-6">
    <h2 className="text-3xl font-black tracking-tight flex items-center mb-8">
      <Calendar size={28} className="mr-4 text-[#C9A84C]" />
      Lịch <span className="text-[#C9A84C] ml-2">Lớp Học</span>
    </h2>
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      {classes.length === 0 ? (
        <p className="text-[#A1A1AA] italic">Chưa có lớp học nào được lên lịch.</p>
      ) : classes.map((cls, idx) => (
        <div key={idx} className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl p-6 hover:border-white/20 transition-all flex items-start space-x-6 relative overflow-hidden group">
          <div className="w-1.5 absolute top-0 bottom-0 left-0 bg-[#C9A84C]"></div>
          <div className="flex-1 pl-4">
            <div className="flex justify-between items-start mb-2">
              <h3 className="font-black text-xl text-[#F5F5F0]">{cls.nxv_ten_lop_hoc || cls.g6_ten_lop || 'Lớp GroupX'}</h3>
              <span className="px-3 py-1 bg-[#C9A84C]/20 text-[#C9A84C] rounded-lg text-[10px] font-bold uppercase tracking-widest border border-[#C9A84C]/30">{cls.nxv_loai_lop || 'Class'}</span>
            </div>
            <p className="text-[#A1A1AA] text-sm mb-4"><Calendar size={14} className="inline mr-2" /> {cls.nxv_ngay_hoc || cls.nxv_thoi_gian_bat_dau || '--'} | {cls.nxv_gio_bat_dau || ''} - {cls.nxv_gio_ket_thuc || ''}</p>
            <div className="flex justify-between items-center mt-6">
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 rounded-full bg-white/10 flex items-center justify-center text-xs font-bold"><User size={12}/></div>
                <span className="text-sm font-bold text-[#A1A1AA]">{cls.nxv_huan_luyen_vien || 'Coach'}</span>
              </div>
              <button className="px-6 py-2 bg-white/5 hover:bg-[#C9A84C] hover:text-[#0A0A0A] border border-white/10 rounded-xl transition-all font-bold text-xs uppercase tracking-widest">
                Tham gia
              </button>
            </div>
          </div>
        </div>
      ))}
    </div>
  </div>
);

const PTView = ({ pts }) => (
  <div className="space-y-8">
    <h2 className="text-3xl font-black tracking-tight flex items-center mb-8">
      <UserCircle2 size={28} className="mr-4 text-[#C9A84C]" />
      Huấn Luyện Viên <span className="text-[#C9A84C] ml-2">Của Tôi</span>
    </h2>
    
    {pts.active ? (
      <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl p-8 relative overflow-hidden flex items-center space-x-8">
        <Zap className="absolute top-[-20px] right-[-20px] text-[#C9A84C] opacity-10" size={150} />
        <img src={pts.active.nxv_anh_the || "https://ui-avatars.com/api/?name=PT&background=C9A84C&color=000"} className="w-32 h-32 rounded-2xl object-cover border-4 border-[#C9A84C]/20 relative z-10" />
        <div className="relative z-10 flex-1">
          <p className="text-[10px] text-[#A1A1AA] font-bold uppercase tracking-[3px] mb-1">HLV CÁ NHÂN</p>
          <h3 className="text-3xl font-black text-[#F5F5F0] mb-2">{pts.active.nxv_ho_ten || 'Coach Iron'}</h3>
          <p className="text-[#C9A84C] font-bold uppercase tracking-widest text-sm mb-6">{pts.active.nxv_chuyen_mon || 'Fitness Expert'}</p>
          <div className="flex space-x-4">
            <button className="px-6 py-3 bg-[#C9A84C] text-[#0A0A0A] font-bold rounded-xl shadow-[0_0_15px_rgba(201,168,76,0.3)] hover:scale-105 transition-transform flex items-center space-x-2">
              <Calendar size={18} /><span>Đặt lịch</span>
            </button>
            <button className="px-6 py-3 bg-white/5 text-[#F5F5F0] border border-white/10 font-bold rounded-xl hover:bg-white/10 transition-all flex items-center space-x-2">
              <MessageSquare size={18} /><span>Nhắn tin</span>
            </button>
          </div>
        </div>
      </div>
    ) : (
      <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl p-8 text-center">
        <p className="text-[#A1A1AA] italic mb-4">Bạn chưa có Huấn Luyện Viên cá nhân.</p>
      </div>
    )}

    <h3 className="text-xl font-bold mt-12 mb-6 uppercase tracking-widest text-[#A1A1AA]">Đội ngũ Ironcore Coach</h3>
    <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6">
      {pts.available.map((pt, idx) => (
        <div key={idx} className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl p-6 text-center hover:border-white/20 transition-all group">
          <img src={pt.nxv_anh_the || "https://ui-avatars.com/api/?name=PT&background=1C1C1C&color=C9A84C"} className="w-24 h-24 mx-auto rounded-full object-cover border-2 border-white/10 group-hover:border-[#C9A84C] transition-colors mb-4" />
          <h4 className="font-black text-lg text-[#F5F5F0] mb-1">{pt.nxv_ho_ten || 'Coach'}</h4>
          <p className="text-[#C9A84C] text-xs font-bold uppercase tracking-widest mb-6">{pt.nxv_chuyen_mon || 'Personal Trainer'}</p>
          <button className="w-full py-2 bg-white/5 hover:bg-[#C9A84C] hover:text-[#0A0A0A] border border-white/10 rounded-xl transition-all font-bold text-xs uppercase tracking-widest">
            Đăng ký
          </button>
        </div>
      ))}
      {pts.available.length === 0 && <p className="text-[#A1A1AA] italic">Đang cập nhật danh sách HLV.</p>}
    </div>
  </div>
);

export default MemberDashboard;
