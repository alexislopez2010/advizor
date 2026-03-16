#!/bin/bash
# adviZor - Start both backend and frontend

echo ""
echo "  ██████╗ ██████╗  ██╗   ██╗██╗███████╗ ██████╗ ██████╗ "
echo "  ██╔══██╗╚════██╗ ██║   ██║██║╚════██║██╔═══██╗██╔══██╗"
echo "  ███████║ █████╔╝ ██║   ██║██║    ██╔╝██║   ██║██████╔╝"
echo "  ██╔══██║██╔═══╝  ╚██╗ ██╔╝██║   ██╔╝ ██║   ██║██╔══██╗"
echo "  ██║  ██║███████╗  ╚████╔╝ ██║   ██║  ╚██████╔╝██║  ██║"
echo "  ╚═╝  ╚═╝╚══════╝   ╚═══╝  ╚═╝   ╚═╝   ╚═════╝ ╚═╝  ╚═╝"
echo ""
echo "  AI Campaign Portfolio Advisor  |  Executive Demo"
echo ""

# Optional: set your API key here for live AI responses
# export ANTHROPIC_API_KEY="sk-ant-..."
# export OPENAI_API_KEY="sk-..."

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Start backend
echo "▶ Starting backend (FastAPI) on http://localhost:8000..."
cd "$SCRIPT_DIR/backend"
source venv/bin/activate
uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!

sleep 2

# Start frontend
echo "▶ Starting frontend (Next.js) on http://localhost:3000..."
cd "$SCRIPT_DIR/frontend"
npm run dev &
FRONTEND_PID=$!

echo ""
echo "  ✅ adviZor is running!"
echo "  🌐 Open: http://localhost:3000"
echo ""
echo "  Press Ctrl+C to stop both services."
echo ""

# Cleanup on exit
trap "echo ''; echo 'Shutting down...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM

wait
