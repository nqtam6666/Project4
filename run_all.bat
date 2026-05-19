@echo off
npx --yes concurrently -c "blue,magenta" -n "BACKEND,FRONTEND" "cd backend && python run.py" "cd frontend && npm run dev"
