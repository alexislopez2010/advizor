# adviZor — AI Campaign Portfolio Advisor

Executive demo for advertising teams. Analyzes a client's current ad tool subscriptions, identifies gaps against their campaign goals, and recommends upsells with detailed ROI reasoning.

---

## Quick Start

```bash
cd ~/openclaw-projects/adviZor
./start.sh
```

Then open: **http://localhost:3000**

---

## Features

| Feature | Description |
|---|---|
| Auto-Analysis | One-click full portfolio gap analysis with exec summary |
| Chat Mode | Conversational AI advisor for Q&A about the client |
| PDF Export | Branded executive brief, download-ready |
| Mock Data | Fully fictional client + services — no real data needed |

---

## Demo Scenario

**Client:** NovaPulse Energy  
- Residential solar + home battery brand  
- Expanding into 8 new US markets in 2027  
- Launching new EV HomeCharge product  

**Services:**

| Service | Description | Cost |
|---|---|---|
| Insight360 ✓ | AI audience intelligence & analytics | $2,800/mo |
| PrecisionOTT | CTV/streaming targeting & attribution | $3,500–7,500/mo |
| AmplifyAI | Dynamic creative optimization & personalization | $4,200–8,500/mo |

---

## Adding a Live AI

The demo runs on high-quality pre-built responses by default. To enable live AI:

1. Open `start.sh`
2. Uncomment and set your API key:
   ```bash
   export ANTHROPIC_API_KEY="sk-ant-..."
   # or
   export OPENAI_API_KEY="sk-..."
   ```

---

## Structure

```
adviZor/
├── start.sh              # One-command launcher
├── backend/
│   ├── main.py           # FastAPI routes
│   ├── analyzer.py       # Gap analysis + LLM reasoning
│   ├── pdf_generator.py  # ReportLab PDF export
│   └── data.py           # Demo client + services data
└── frontend/
    ├── app/page.tsx       # Main app shell
    └── components/
        ├── AnalysisView.tsx  # Auto-analysis tab
        └── ChatView.tsx      # Chat tab
```
