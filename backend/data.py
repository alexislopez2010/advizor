"""
adviZor - Demo Data
Fictional client + fictional ad services for executive demo.
"""

SERVICES = {
    "precision_ott": {
        "id": "precision_ott",
        "name": "PrecisionOTT",
        "tagline": "Connected TV & Streaming Audience Targeting",
        "description": "Programmatic CTV/OTT inventory across 200+ streaming apps with real-time audience segmentation, co-viewing detection, and cross-device attribution.",
        "capabilities": ["ctv", "ott", "connected_tv", "streaming", "video", "cord_cutters", "cross_device", "attribution"],
        "best_for": ["brand awareness", "video campaigns", "reaching cord-cutters", "upper funnel", "mass reach"],
        "monthly_cost_usd": 3500,
        "tiers": ["Starter ($3,500/mo)", "Growth ($7,500/mo)", "Enterprise (custom)"],
        "kpis": ["VCR", "Reach", "Frequency", "Brand Lift"],
        "avg_roi_narrative": "Clients typically see a 35–55% lift in unaided brand awareness within 90 days. CTV reach often fills gaps left by traditional linear TV at 40% lower CPM."
    },
    "insight360": {
        "id": "insight360",
        "name": "Insight360",
        "tagline": "AI-Powered Audience Intelligence & Predictive Analytics",
        "description": "Real-time 1st- and 3rd-party data enrichment, predictive audience modeling, lookalike expansion, and campaign performance dashboards with automated weekly reports.",
        "capabilities": ["audience_intelligence", "data_enrichment", "lookalike", "predictive_modeling", "analytics", "reporting", "first_party_data", "third_party_data"],
        "best_for": ["audience insights", "data-driven campaigns", "lookalike audiences", "campaign optimization", "reporting"],
        "monthly_cost_usd": 2800,
        "tiers": ["Core ($2,800/mo)", "Pro ($5,200/mo)", "Enterprise (custom)"],
        "kpis": ["Audience Match Rate", "Lookalike Expansion Rate", "CPA", "LTV"],
        "avg_roi_narrative": "Brands using Insight360 report 28% improvement in CPA within 60 days through better audience segmentation. Lookalike models typically expand qualified reach by 3–5x."
    },
    "amplify_ai": {
        "id": "amplify_ai",
        "name": "AmplifyAI",
        "tagline": "AI Creative Optimization & Personalization at Scale",
        "description": "Dynamic creative optimization (DCO), AI-generated ad variant testing, personalized messaging by segment, and creative performance scoring across display, social, and native.",
        "capabilities": ["creative_optimization", "dco", "personalization", "ai_creative", "ab_testing", "display", "social", "native", "performance_creative"],
        "best_for": ["creative testing", "personalization", "lower funnel", "conversion", "retargeting", "display campaigns"],
        "monthly_cost_usd": 4200,
        "tiers": ["Launch ($4,200/mo)", "Scale ($8,500/mo)", "Enterprise (custom)"],
        "kpis": ["CTR", "CVR", "ROAS", "Creative Score"],
        "avg_roi_narrative": "DCO-enabled campaigns average 42% higher CTR and 31% better ROAS vs. static creative. AI variant testing reduces creative production costs by up to 60%."
    }
}

CLIENT = {
    "id": "novapulse",
    "name": "NovaPulse Energy",
    "industry": "Renewable Energy / Consumer Brand",
    "description": "NovaPulse is a fast-growing residential solar and home energy storage brand operating in 22 US markets. They're expanding into 8 new markets in 2027 and launching a new EV home-charging product line.",
    "current_subscriptions": ["insight360"],
    "annual_ad_budget_usd": 4200000,
    "current_spend_on_services_monthly": 2800,
    "contacts": {
        "marketing_lead": "Jordan Reyes, VP Marketing",
        "media_buyer": "Priya Shah, Director of Paid Media"
    },
    "campaign_goals_2027": [
        "Drive brand awareness in 8 new expansion markets (TX, AZ, CO, NC, OH, VA, MN, WI)",
        "Launch NovaPulse EV HomeCharge — new product, zero current awareness",
        "Improve conversion rates on solar consultations (currently 4.2%, target 7%)",
        "Reduce cost-per-acquisition (CPA) for residential solar installs from $480 to $340",
        "Build retargeting audiences from site visitors and past customers",
        "Personalize messaging by homeowner segment (first-time solar, upgrade buyers, EV owners)"
    ],
    "current_challenges": [
        "Low unaided brand awareness outside current markets",
        "Static ad creative across all segments — no personalization",
        "No CTV/streaming presence despite audience shift away from linear TV",
        "Lookalike audiences not yet activated despite having rich CRM data"
    ]
}
