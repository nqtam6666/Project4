import sys
import os

# Thêm thư mục gốc project vào path để import được package 'backend'
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import nqt_tao_app

app = nqt_tao_app()

if __name__ == '__main__':
    app.run(debug=True)
