"""
adviZor - Gap Analysis & Recommendation Engine
Uses LLM (Anthropic Claude) with deterministic pre-analysis for reliable demo output.
Falls back to high-quality mock output if no API key is set.
"""

import os
import json
from data import SERVICES, CLIENT

try:
    import anthropic
    ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    HAS_ANTHROPIC = bool(ANTHROPIC_KEY)
except ImportError:
    HAS_ANTHROPIC = False

try:
    from openai import OpenAI
    OPENAI_KEY = os.getenv("OPENAI_API_KEY", "")
    HAS_OPENAI = bool(OPENAI_KEY)
except ImportError:
    HAS_OPENAI = False


def analyze_client(client: dict, goals_override: str = None) -> dict:
    """
    Run gap analysis + recommendations for a client.
    Returns structured recommendation dict.
    """
    subscribed = set(client["current_subscriptions"])
    not_subscribed = [s for s in SERVICES if s not in subscribed]
    subscribed_services = {k: SERVICES[k] for k in subscribed if k in SERVICES}
    gap_services = {k: SERVICES[k] for k in not_subscribed}

    goals = goals_override or "\n".join(f"- {g}" for g in client["campaign_goals_2027"])

    # Build recommendations with LLM or deterministic fallback
    if HAS_ANTHROPIC:
        reasoning = _llm_reasoning_anthropic(client, subscribed_services, gap_services, goals)
    elif HAS_OPENAI:
        reasoning = _llm_reasoning_openai(client, subscribed_services, gap_services, goals)
    else:
        reasoning = _mock_reasoning(client, subscribed_services, gap_services, goals)

    return {
        "client": client,
        "current_subscriptions": [SERVICES[k] for k in subscribed if k in SERVICES],
        "gap_services": list(gap_services.values()),
        "recommendations": reasoning["recommendations"],
        "executive_summary": reasoning["executive_summary"],
        "total_additional_investment": sum(SERVICES[k]["monthly_cost_usd"] for k in not_subscribed),
        "goals_analyzed": client["campaign_goals_2027"],
    }


def chat_with_agent(user_message: str, history: list) -> str:
    """Conversational mode — answer questions about the client portfolio."""
    context = f"""
You are adviZor, an AI advertising strategist for a top media agency.
You have deep expertise in ad tech, campaign planning, and ROI analysis.

CLIENT PROFILE:
{json.dumps(CLIENT, indent=2)}

AVAILABLE SERVICES:
{json.dumps(SERVICES, indent=2)}

Your job: help the user understand what services their client needs, why, and what value they'll get.
Be concise, sharp, and executive-ready. Use real numbers where possible.
If asked about pricing, reference the service tier data.
Always tie recommendations back to the client's specific 2027 goals.
"""
    messages = [{"role": "system", "content": context}]
    for h in history:
        messages.append(h)
    messages.append({"role": "user", "content": user_message})

    if HAS_ANTHROPIC:
        client_ai = anthropic.Anthropic(api_key=ANTHROPIC_KEY)
        # Claude uses system prompt differently
        sys_prompt = messages[0]["content"]
        chat_msgs = messages[1:]
        resp = client_ai.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            system=sys_prompt,
            messages=chat_msgs
        )
        return resp.content[0].text
    elif HAS_OPENAI:
        ai = OpenAI(api_key=OPENAI_KEY)
        resp = ai.chat.completions.create(model="gpt-4o", messages=messages, max_tokens=1024)
        return resp.choices[0].message.content
    else:
        return _mock_chat(user_message)


def _build_prompt(client, subscribed_services, gap_services, goals):
    return f"""
You are adviZor, an AI advertising strategist. Analyze this client and provide recommendations.

CLIENT: {client['name']} ({client['industry']})
{client['description']}

CURRENT SUBSCRIPTIONS:
{json.dumps(list(subscribed_services.values()), indent=2)}

SERVICES NOT YET SUBSCRIBED:
{json.dumps(list(gap_services.values()), indent=2)}

2027 CAMPAIGN GOALS:
{goals}

CURRENT CHALLENGES:
{chr(10).join(f'- {c}' for c in client['current_challenges'])}

Return a JSON object with this exact structure:
{{
  "executive_summary": "2-3 sentence sharp exec summary of the opportunity",
  "recommendations": [
    {{
      "service_id": "<id from gap services>",
      "service_name": "<name>",
      "priority": "High|Medium|Low",
      "goals_addressed": ["<goal 1>", "..."],
      "reasoning": "2-3 sentence explanation of why this service is needed for this client",
      "expected_value": "Specific projected impact with numbers (reach, CPA improvement, ROAS lift, etc.)",
      "recommended_tier": "<tier name and price>",
      "time_to_impact": "Estimated time to see measurable results"
    }}
  ]
}}

Return ONLY valid JSON. No markdown, no extra text.
"""


def _llm_reasoning_anthropic(client, subscribed_services, gap_services, goals):
    ai = anthropic.Anthropic(api_key=ANTHROPIC_KEY)
    prompt = _build_prompt(client, subscribed_services, gap_services, goals)
    resp = ai.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}]
    )
    text = resp.content[0].text.strip()
    # Strip markdown code fences if present
    if text.startswith("```"):
        text = text.split("```", 2)[1]
        if text.startswith("json"):
            text = text[4:]
        text = text.rsplit("```", 1)[0].strip()
    return json.loads(text)


def _llm_reasoning_openai(client, subscribed_services, gap_services, goals):
    ai = OpenAI(api_key=OPENAI_KEY)
    prompt = _build_prompt(client, subscribed_services, gap_services, goals)
    resp = ai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2048,
        response_format={"type": "json_object"}
    )
    return json.loads(resp.choices[0].message.content)


def _mock_reasoning(client, subscribed_services, gap_services, goals):
    """High-quality deterministic fallback for demo without API key."""
    return {
        "executive_summary": (
            "NovaPulse Energy's 2027 expansion into 8 new markets and EV HomeCharge launch require "
            "a full-funnel ad stack upgrade. While Insight360 provides strong audience intelligence, "
            "critical gaps in CTV reach and creative personalization are limiting brand awareness growth "
            "and conversion performance. Adding PrecisionOTT and AmplifyAI closes these gaps and "
            "positions NovaPulse to hit their CPA reduction target of $340 and 7% consultation close rate."
        ),
        "recommendations": [
            {
                "service_id": "precision_ott",
                "service_name": "PrecisionOTT",
                "priority": "High",
                "goals_addressed": [
                    "Drive brand awareness in 8 new expansion markets",
                    "Launch NovaPulse EV HomeCharge — new product, zero current awareness"
                ],
                "reasoning": (
                    "NovaPulse is entering 8 markets with zero brand recognition and launching a brand-new "
                    "product. CTV/OTT is the highest-reach upper-funnel channel available, especially among "
                    "homeowners aged 30–55 who have shifted away from linear TV. PrecisionOTT's geo-targeting "
                    "allows precise activation market-by-market as NovaPulse rolls out, with cross-device "
                    "attribution linking CTV exposure to site visits and consultation bookings."
                ),
                "expected_value": (
                    "Projected 40–55% increase in unaided brand awareness in new markets within 90 days. "
                    "EV HomeCharge launch reach estimated at 2.1M qualified households across expansion "
                    "markets in Q1 2027. CPM ~40% below equivalent linear TV placements."
                ),
                "recommended_tier": "Growth ($7,500/mo) — covers multi-market simultaneous activation",
                "time_to_impact": "45–60 days for measurable brand lift; attribution data in 30 days"
            },
            {
                "service_id": "amplify_ai",
                "service_name": "AmplifyAI",
                "priority": "High",
                "goals_addressed": [
                    "Improve conversion rates on solar consultations (4.2% → 7%)",
                    "Reduce CPA from $480 to $340",
                    "Personalize messaging by homeowner segment (first-time solar, upgrade buyers, EV owners)"
                ],
                "reasoning": (
                    "NovaPulse is currently running identical static creative across all segments — "
                    "a major conversion drag. With Insight360 already identifying rich audience segments "
                    "(first-time solar, upgrade buyers, EV owners), AmplifyAI can activate personalized "
                    "dynamic creative for each segment without manual production overhead. DCO-powered "
                    "retargeting directly addresses the consultation close rate and CPA goals."
                ),
                "expected_value": (
                    "DCO personalization projected to lift consultation conversion rate from 4.2% to "
                    "6.8–7.4% within 60 days. CPA reduction from $480 to $310–$350 (exceeding $340 target). "
                    "Creative production cost savings estimated at $85,000–$120,000 annually vs. manual variants. "
                    "ROAS improvement of 28–35% on retargeting campaigns."
                ),
                "recommended_tier": "Scale ($8,500/mo) — supports multi-segment DCO + 3 product lines",
                "time_to_impact": "30 days for first variant tests; full optimization in 60–75 days"
            }
        ]
    }


def _mock_chat(user_message: str) -> str:
    msg = user_message.lower()
    if any(w in msg for w in ["what", "recommend", "suggest", "need", "should"]):
        return (
            "Based on NovaPulse Energy's 2027 goals, I recommend two additions to their current Insight360 subscription:\n\n"
            "**PrecisionOTT (High Priority)** — Their expansion into 8 new markets requires upper-funnel brand reach. "
            "CTV/OTT reaches cord-cutters (their core homeowner demographic) at ~40% lower CPM than linear TV, "
            "with precise geo-targeting per market rollout.\n\n"
            "**AmplifyAI (High Priority)** — NovaPulse is running static creative across all segments. "
            "With Insight360 already segmenting their audience, AmplifyAI activates that data through "
            "personalized dynamic creative — projecting a 42% CTR lift and CPA drop from $480 to ~$330.\n\n"
            "Combined additional investment: $16,000/mo. Projected CPA savings alone recover that in under 45 days."
        )
    elif any(w in msg for w in ["cost", "price", "invest", "budget", "much"]):
        return (
            "Here's the investment picture for NovaPulse:\n\n"
            "• **Current:** Insight360 Core — $2,800/mo\n"
            "• **Recommended add:** PrecisionOTT Growth — $7,500/mo\n"
            "• **Recommended add:** AmplifyAI Scale — $8,500/mo\n"
            "• **New total:** $18,800/mo ($225,600/yr)\n\n"
            "Against a $4.2M annual ad budget, this is a 5.4% stack investment — well within industry benchmarks "
            "of 8–12%. Projected CPA improvement ($480 → $340) on their volume translates to ~$840K in annual "
            "acquisition cost savings."
        )
    elif any(w in msg for w in ["ctv", "ott", "streaming", "tv", "video"]):
        return (
            "PrecisionOTT is the right fit for NovaPulse's awareness goals. Their target homeowner demographic "
            "(ages 35–60, HHI $80K+) is one of the fastest-shifting segments away from linear TV. "
            "PrecisionOTT covers 200+ streaming apps with co-viewing detection and cross-device attribution — "
            "so when a household sees the NovaPulse ad on their smart TV, we can track the downstream "
            "site visit and consultation booking. Growth tier ($7,500/mo) supports simultaneous activation "
            "across all 8 new markets."
        )
    else:
        return (
            "I can help you analyze NovaPulse Energy's 2027 campaign portfolio. "
            "Ask me about specific goals, service recommendations, pricing, or expected ROI — "
            "or run the **Auto-Analyze** to get the full executive brief."
        )
