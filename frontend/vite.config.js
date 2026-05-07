import { defineConfig } from 'vite';
import { resolve } from 'path';

function nqtAdminRewrite() {
  const adminPages = [
    'login','dashboard','hoi-vien','khach-hang','goi-tap','huan-luyen-vien',
    'lop-hoc','don-hang','thanh-toan','san-pham','khuyen-mai','su-kien',
    'chi-nhanh','nhan-vien','bao-tri','van-chuyen','blog','bao-cao','quan-tri','phan-quyen','cau-hinh',
  ];
  return {
    name: 'nqt-admin-rewrite',
    configureServer(server) {
      server.middlewares.use((req, _res, next) => {
        const matchAdmin = req.url.match(/^\/admin\/([^/?#]+)(\/)?(\?.*)?$/);
        if (matchAdmin) {
          const page = matchAdmin[1];
          if (adminPages.includes(page)) {
            req.url = `/src/pages/admin/${page}.html${matchAdmin[3] || ''}`;
          }
        } else if (req.url === '/admin' || req.url === '/admin/') {
          req.url = '/src/pages/admin/dashboard.html';
        } else {
          // Member routes
          const urlBase = req.url.split('?')[0];
          const query = req.url.split('?')[1] ? '?' + req.url.split('?')[1] : '';
          
          if (urlBase === '/login' || urlBase === '/login/') {
            req.url = '/src/pages/member/login.html' + query;
          } else if (urlBase === '/home' || urlBase === '/home/') {
            req.url = '/src/pages/member/dashboard.html' + query;
          } else if (urlBase === '/register' || urlBase === '/register/') {
            req.url = '/src/pages/member/register.html' + query;
          }
        }
        next();
      });
    },
  };
}

export default defineConfig({
  plugins: [nqtAdminRewrite()],
  root: '.',
  build: {
    outDir: 'dist',
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
        memberLogin: resolve(__dirname, 'src/pages/member/login.html'),
        memberDashboard: resolve(__dirname, 'src/pages/member/dashboard.html'),
        memberHoSo: resolve(__dirname, 'src/pages/member/ho_so.html'),
        goiTap: resolve(__dirname, 'src/pages/goi-tap.html'),
        huanLuyenVien: resolve(__dirname, 'src/pages/huan-luyen-vien.html'),
        lopHoc: resolve(__dirname, 'src/pages/lop-hoc.html'),
        blog: resolve(__dirname, 'src/pages/blog.html'),
        blogChiTiet: resolve(__dirname, 'src/pages/blog-chi-tiet.html'),
        suKien: resolve(__dirname, 'src/pages/su-kien.html'),
        shop: resolve(__dirname, 'src/pages/shop.html'),
        shopChiTiet: resolve(__dirname, 'src/pages/shop-chi-tiet.html'),
        memberGoiTap: resolve(__dirname, 'src/pages/member/goi-tap.html'),
        memberDiemDanh: resolve(__dirname, 'src/pages/member/diem-danh.html'),
        memberChiSo: resolve(__dirname, 'src/pages/member/chi-so.html'),
        memberLichTap: resolve(__dirname, 'src/pages/member/lich-tap.html'),
        memberDichVu: resolve(__dirname, 'src/pages/member/dich-vu.html'),
        memberRegister: resolve(__dirname, 'src/pages/member/register.html'),
        shopGioHang: resolve(__dirname, 'src/pages/shop/gio-hang.html'),
        shopThanhToan: resolve(__dirname, 'src/pages/shop/thanh-toan.html'),
        shopDonHang: resolve(__dirname, 'src/pages/shop/don-hang.html'),
      // Admin pages
      adminLogin: resolve(__dirname, 'src/pages/admin/login.html'),
      adminDashboard: resolve(__dirname, 'src/pages/admin/dashboard.html'),
      adminHoiVien: resolve(__dirname, 'src/pages/admin/hoi-vien.html'),
      adminKhachHang: resolve(__dirname, 'src/pages/admin/khach-hang.html'),
      adminGoiTap: resolve(__dirname, 'src/pages/admin/goi-tap.html'),
      adminHuanLuyenVien: resolve(__dirname, 'src/pages/admin/huan-luyen-vien.html'),
      adminLopHoc: resolve(__dirname, 'src/pages/admin/lop-hoc.html'),
      adminDonHang: resolve(__dirname, 'src/pages/admin/don-hang.html'),
      adminThanhToan: resolve(__dirname, 'src/pages/admin/thanh-toan.html'),
      adminSanPham: resolve(__dirname, 'src/pages/admin/san-pham.html'),
      adminKhuyenMai: resolve(__dirname, 'src/pages/admin/khuyen-mai.html'),
      adminSuKien: resolve(__dirname, 'src/pages/admin/su-kien.html'),
      adminChiNhanh: resolve(__dirname, 'src/pages/admin/chi-nhanh.html'),
      adminNhanVien: resolve(__dirname, 'src/pages/admin/nhan-vien.html'),
      adminBaoTri: resolve(__dirname, 'src/pages/admin/bao-tri.html'),
      adminVanChuyen: resolve(__dirname, 'src/pages/admin/van-chuyen.html'),
      adminBlog: resolve(__dirname, 'src/pages/admin/blog.html'),
      adminBaoCao: resolve(__dirname, 'src/pages/admin/bao-cao.html'),
      adminQuanTri: resolve(__dirname, 'src/pages/admin/quan-tri.html'),
      adminPhanQuyen: resolve(__dirname, 'src/pages/admin/phan-quyen.html'),
      adminCauHinh: resolve(__dirname, 'src/pages/admin/cau-hinh.html'),
      },
    },
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
    },
  },
});
