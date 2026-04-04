# scripts/build_tools.py
# Tool review section page generators. ~40 pages from market_intelligence.json + curated data.
# Called by build.py. Uses templates.py for HTML shell.

import os
import json

from nav_config import *
from templates import (get_page_wrapper, write_page, get_breadcrumb_schema,
                       get_faq_schema, breadcrumb_html, newsletter_cta_html,
                       faq_html)

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_FILE = os.path.join(PROJECT_DIR, "data", "market_intelligence.json")


def load_tool_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Tool definitions (curated + mention data merged at build time)
# ---------------------------------------------------------------------------

CATEGORIES = {
    "prm": {
        "name": "PRM Platforms",
        "slug": "prm",
        "description": "Partner Relationship Management platforms help companies recruit, onboard, enable, and manage channel partners at scale. PRM is the system of record for partner programs.",
        "long_description": "PRM platforms are the backbone of structured partner programs. They handle partner recruitment and application workflows, training and certification, deal registration, lead distribution, MDF management, and performance analytics. For companies with more than 20 active partners, a dedicated PRM replaces the spreadsheets and ad-hoc processes that break at scale.",
    },
    "co-selling": {
        "name": "Co-Selling Tools",
        "slug": "co-selling",
        "description": "Co-selling and ecosystem mapping platforms that help partners identify overlap accounts, share data securely, and run joint pipeline.",
        "long_description": "Co-selling tools emerged from the ecosystem-led growth movement. They solve a fundamental problem: how do you identify mutual customers and prospects across partner CRMs without exposing sensitive data? These platforms use encrypted data matching to find account overlaps, then provide workflows for partner managers to collaborate on specific opportunities.",
    },
    "marketplace": {
        "name": "Marketplace Management",
        "slug": "marketplace",
        "description": "Cloud marketplace management platforms that help ISVs list, transact, and scale through AWS, Azure, and GCP marketplaces.",
        "long_description": "Cloud marketplace management tools help software vendors sell through AWS Marketplace, Azure Marketplace, and Google Cloud Marketplace. They handle listing management, co-sell registration with cloud providers, private offer creation, metering and billing, and procurement workflow automation. As enterprise buyers increasingly consolidate spend through cloud commits, marketplace management has become critical infrastructure for B2B SaaS companies.",
    },
    "crm": {
        "name": "CRM Platforms",
        "slug": "crm",
        "description": "CRM platforms used by partnerships teams to manage partner relationships, deal flow, and pipeline alongside direct sales.",
        "long_description": "While PRM handles the partner-facing side, CRM platforms remain the internal system of record for many partnership teams. Partner managers use CRM to track partner-sourced and partner-influenced deals, manage co-selling opportunities, and report on partner contribution to revenue. The best partner programs integrate PRM with CRM for a single view of partner impact.",
    },
    "analytics": {
        "name": "Analytics Platforms",
        "slug": "analytics",
        "description": "Business intelligence and analytics tools used by partnership teams to measure partner performance, attribution, and ecosystem health.",
        "long_description": "Analytics platforms help partnership leaders answer the questions that matter: which partners drive the most revenue, what is the true ROI of partner programs, and where should we invest next? These tools connect to CRM, PRM, and financial systems to build dashboards that quantify partner impact beyond simple deal registration counts.",
    },
}

TOOLS = {
    # PRM
    "partnerstack": {
        "name": "PartnerStack",
        "slug": "partnerstack",
        "category": "prm",
        "website": "partnerstack.com",
        "tagline": "The partnerships platform for SaaS",
        "description": "PartnerStack is a PRM and partner ecosystem platform designed for B2B SaaS companies. It combines partner management, marketplace distribution, and automated payouts in a single platform.",
        "founded": "2015",
        "hq": "Toronto, Canada",
        "pricing": "Custom pricing based on partner count and features. Starts around $500/month for smaller programs.",
        "best_for": "B2B SaaS companies running affiliate, referral, and reseller programs. Particularly strong for companies with 50-500 partners.",
        "strengths": [
            "Built-in marketplace for partner discovery and recruitment",
            "Automated partner payouts and commission tracking",
            "Strong API and integration ecosystem",
            "Purpose-built for SaaS partner programs",
            "Self-serve partner onboarding workflows",
        ],
        "weaknesses": [
            "Less suited for large enterprise channel programs with complex tiers",
            "Limited MDF (Market Development Fund) management compared to enterprise PRMs",
            "Reporting can be basic for complex multi-touch attribution",
        ],
        "ideal_company_size": "50-5,000 employees",
        "rating": 4.3,
    },
    "impartner": {
        "name": "Impartner",
        "slug": "impartner",
        "category": "prm",
        "website": "impartner.com",
        "tagline": "The enterprise partner management platform",
        "description": "Impartner is an enterprise-grade PRM platform that handles the full partner lifecycle from recruitment through revenue. Built for companies with complex, multi-tier channel programs.",
        "founded": "2008",
        "hq": "Salt Lake City, Utah",
        "pricing": "Enterprise pricing, typically $2,000-10,000+/month depending on partner count and modules.",
        "best_for": "Enterprise companies with 100+ partners and complex channel programs requiring tiered structures, MDF management, and deep CRM integration.",
        "strengths": [
            "Most comprehensive enterprise PRM feature set on the market",
            "Deep Salesforce native integration",
            "Advanced MDF and co-op fund management",
            "Multi-tier partner program support",
            "Strong deal registration and lead distribution workflows",
        ],
        "weaknesses": [
            "Higher price point excludes smaller companies",
            "Implementation can take 3-6 months for full deployment",
            "UI can feel dated compared to newer platforms",
        ],
        "ideal_company_size": "1,000+ employees",
        "rating": 4.1,
    },
    "allbound": {
        "name": "Allbound",
        "slug": "allbound",
        "category": "prm",
        "website": "allbound.com",
        "tagline": "Partner enablement and channel management",
        "description": "Allbound is a PRM focused on partner enablement, training, and content management. It emphasizes making partners productive through structured onboarding and learning paths.",
        "founded": "2014",
        "hq": "Atlanta, Georgia",
        "pricing": "Mid-market pricing, typically $1,000-5,000/month.",
        "best_for": "Companies that prioritize partner enablement and training over deal registration and complex channel operations.",
        "strengths": [
            "Excellent partner learning and certification engine",
            "Clean, modern interface that partners actually use",
            "Strong content management for co-branded materials",
            "Good Salesforce and HubSpot integrations",
        ],
        "weaknesses": [
            "Less robust deal registration than Impartner",
            "Limited marketplace distribution capabilities",
            "Smaller customer base means fewer peer benchmarks",
        ],
        "ideal_company_size": "200-5,000 employees",
        "rating": 4.0,
    },
    "kiflo": {
        "name": "Kiflo",
        "slug": "kiflo",
        "category": "prm",
        "website": "kiflo.com",
        "tagline": "PRM for growing partner programs",
        "description": "Kiflo is a lightweight PRM designed for companies launching or scaling their first partner program. Affordable entry point with the core features needed to manage partners without enterprise complexity.",
        "founded": "2020",
        "hq": "Paris, France",
        "pricing": "Starts at $199/month. Transparent pricing tiers based on features and partner count.",
        "best_for": "Startups and SMBs launching their first formal partner program. Companies with 5-50 partners who have outgrown spreadsheets.",
        "strengths": [
            "Most affordable PRM on the market",
            "Fast implementation (days, not months)",
            "Intuitive interface with minimal training needed",
            "Good for affiliate, referral, and reseller programs",
            "Transparent pricing without enterprise sales cycles",
        ],
        "weaknesses": [
            "Limited advanced features for complex channel programs",
            "Fewer integrations than established platforms",
            "Relatively new platform with smaller customer base",
        ],
        "ideal_company_size": "10-500 employees",
        "rating": 4.2,
    },
    "channeltivity": {
        "name": "Channeltivity",
        "slug": "channeltivity",
        "category": "prm",
        "website": "channeltivity.com",
        "tagline": "Simple, powerful partner management",
        "description": "Channeltivity is a mid-market PRM that balances feature depth with usability. Known for strong deal registration, partner portals, and HubSpot integration.",
        "founded": "2012",
        "hq": "Raleigh, North Carolina",
        "pricing": "Mid-market pricing, typically $1,000-3,000/month.",
        "best_for": "HubSpot-centric companies that need solid deal registration and partner portal capabilities without enterprise PRM complexity.",
        "strengths": [
            "Best-in-class HubSpot integration",
            "Strong deal registration workflows",
            "Clean partner portal experience",
            "Good balance of features and usability",
        ],
        "weaknesses": [
            "Salesforce integration not as deep as Impartner",
            "Limited marketplace capabilities",
            "Smaller ecosystem of add-ons and extensions",
        ],
        "ideal_company_size": "100-2,000 employees",
        "rating": 4.1,
    },
    # Co-Selling
    "crossbeam": {
        "name": "Crossbeam",
        "slug": "crossbeam",
        "category": "co-selling",
        "website": "crossbeam.com",
        "tagline": "Ecosystem-led growth platform",
        "description": "Crossbeam is the leading ecosystem data sharing and co-selling platform. It lets companies securely compare CRM data with partners to find mutual customers, prospects, and opportunities without exposing raw data.",
        "founded": "2018",
        "hq": "Philadelphia, Pennsylvania",
        "pricing": "Free tier available. Paid plans start around $500/month for advanced features and more partner connections.",
        "best_for": "B2B SaaS companies with 5+ technology or channel partners who want to identify overlap accounts and run co-selling plays.",
        "strengths": [
            "Pioneer and market leader in ecosystem data sharing",
            "Largest network of connected companies",
            "Free tier makes it accessible for early-stage partner programs",
            "Strong Salesforce and HubSpot integrations",
            "Account mapping is fast and intuitive",
            "Recently merged with Reveal, expanding capabilities",
        ],
        "weaknesses": [
            "Value depends on partners also being on the platform",
            "Advanced co-selling workflows require paid tier",
            "Can create data overload without clear co-selling process",
        ],
        "ideal_company_size": "50-10,000 employees",
        "rating": 4.5,
    },
    "reveal": {
        "name": "Reveal",
        "slug": "reveal",
        "category": "co-selling",
        "website": "reveal.co",
        "tagline": "Nearbound revenue platform",
        "description": "Reveal (now merged with Crossbeam) is a co-selling platform focused on the 'nearbound' approach to B2B sales. It helps companies leverage partner ecosystems to warm up cold accounts and accelerate deals.",
        "founded": "2019",
        "hq": "Paris, France",
        "pricing": "Free tier available. Paid plans for advanced features.",
        "best_for": "Companies adopting a nearbound strategy who want to use partner relationships to influence pipeline. European companies with GDPR requirements.",
        "strengths": [
            "Strong nearbound methodology and content leadership",
            "Good European market presence and GDPR compliance",
            "Clean UI focused on actionable insights",
            "Merged with Crossbeam creating the largest co-selling network",
        ],
        "weaknesses": [
            "Platform transition from standalone to Crossbeam merger ongoing",
            "Feature overlap with Crossbeam may cause confusion during integration",
            "Smaller standalone network before merger",
        ],
        "ideal_company_size": "50-5,000 employees",
        "rating": 4.2,
    },
    "partnertap": {
        "name": "PartnerTap",
        "slug": "partnertap",
        "category": "co-selling",
        "website": "partnertap.com",
        "tagline": "Enterprise partner ecosystem platform",
        "description": "PartnerTap is an enterprise co-selling platform focused on large companies with complex partner ecosystems. It specializes in account mapping and partner pipeline management for enterprise channel teams.",
        "founded": "2017",
        "hq": "Seattle, Washington",
        "pricing": "Enterprise pricing. Contact for custom quotes.",
        "best_for": "Enterprise companies with large partner ecosystems that need enterprise-grade security, compliance, and account mapping at scale.",
        "strengths": [
            "Built for enterprise-scale partner ecosystems",
            "Strong data security and compliance features",
            "Good for companies with hundreds of partners",
            "Deep Salesforce integration",
        ],
        "weaknesses": [
            "Less accessible for smaller companies",
            "Smaller partner network than Crossbeam",
            "Enterprise sales cycle for procurement",
        ],
        "ideal_company_size": "1,000+ employees",
        "rating": 3.9,
    },
    # Marketplace
    "tackle": {
        "name": "Tackle.io",
        "slug": "tackle-io",
        "category": "marketplace",
        "website": "tackle.io",
        "tagline": "Cloud marketplace platform",
        "description": "Tackle.io helps software companies list and sell through AWS Marketplace, Azure Marketplace, and Google Cloud Marketplace. It handles listing creation, private offers, co-sell registration, and transaction management.",
        "founded": "2016",
        "hq": "Boise, Idaho",
        "pricing": "Custom pricing based on marketplace transaction volume. Typically a percentage of marketplace revenue.",
        "best_for": "B2B SaaS companies that want to sell through cloud marketplaces to tap into customer cloud commits and simplify procurement.",
        "strengths": [
            "Supports all three major cloud marketplaces (AWS, Azure, GCP)",
            "Strong co-sell registration with cloud providers",
            "Private offer creation and management",
            "Metering and usage-based billing support",
            "Large customer base with proven playbooks",
        ],
        "weaknesses": [
            "Revenue-share pricing model can get expensive at scale",
            "Marketplace operations still requires internal champion",
            "Limited PRM functionality outside of marketplace context",
        ],
        "ideal_company_size": "200-10,000 employees",
        "rating": 4.3,
    },
    "appdirect": {
        "name": "AppDirect",
        "slug": "appdirect",
        "category": "marketplace",
        "website": "appdirect.com",
        "tagline": "B2B commerce platform",
        "description": "AppDirect is a B2B subscription commerce platform that powers partner marketplaces and app stores for distributors, telcos, and technology companies.",
        "founded": "2009",
        "hq": "San Francisco, California",
        "pricing": "Enterprise pricing based on marketplace volume and features.",
        "best_for": "Large distributors, telcos, and technology companies that want to build their own partner marketplace or app store.",
        "strengths": [
            "White-label marketplace platform for building branded ecosystems",
            "Strong billing, provisioning, and subscription management",
            "Mature platform with large enterprise customers",
            "Good for complex distribution and reseller models",
        ],
        "weaknesses": [
            "Not designed for direct cloud marketplace selling (AWS/Azure/GCP)",
            "Enterprise-only pricing and sales cycle",
            "Implementation complexity for full platform deployment",
        ],
        "ideal_company_size": "5,000+ employees",
        "rating": 3.8,
    },
    # CRM
    "salesforce": {
        "name": "Salesforce",
        "slug": "salesforce",
        "category": "crm",
        "website": "salesforce.com",
        "tagline": "The world's #1 CRM",
        "description": "Salesforce is the dominant CRM platform for partnerships teams, offering native partner management capabilities through Salesforce PRM (Experience Cloud) alongside the core sales, service, and marketing clouds.",
        "founded": "1999",
        "hq": "San Francisco, California",
        "pricing": "CRM starts at $25/user/month. PRM (Experience Cloud) is additional. Enterprise agreements vary widely.",
        "best_for": "Companies already on Salesforce that want native partner management without adding a separate PRM. Large enterprises with complex partner programs.",
        "strengths": [
            "Largest CRM ecosystem with extensive AppExchange",
            "Native PRM capabilities through Experience Cloud",
            "Most partnership tools integrate with Salesforce first",
            "Deep customization and automation via Flow and Apex",
            "Dominant in enterprise B2B, so partners are familiar with it",
        ],
        "weaknesses": [
            "PRM features are less specialized than dedicated PRMs like Impartner",
            "Can be expensive when adding PRM licenses to existing CRM contracts",
            "Complexity requires dedicated admin resources",
            "Partner portal experience can feel generic without customization",
        ],
        "ideal_company_size": "50-100,000+ employees",
        "rating": 4.4,
    },
    "hubspot": {
        "name": "HubSpot",
        "slug": "hubspot",
        "category": "crm",
        "website": "hubspot.com",
        "tagline": "The CRM platform for scaling companies",
        "description": "HubSpot CRM is increasingly used by partnerships teams, especially at growth-stage SaaS companies. While it lacks native PRM, its ecosystem of partner management integrations and clean UI make it a popular choice.",
        "founded": "2006",
        "hq": "Cambridge, Massachusetts",
        "pricing": "Free CRM tier available. Paid plans from $45/month. Enterprise from $1,200/month.",
        "best_for": "Growth-stage SaaS companies that want a unified CRM for sales and partnerships without the complexity of Salesforce.",
        "strengths": [
            "Intuitive UI that requires minimal training",
            "Strong partner tool integrations (Channeltivity, PartnerStack, Crossbeam)",
            "Free tier is genuinely useful for small partner programs",
            "Excellent marketing automation for partner campaigns",
            "Growing partner ecosystem of its own",
        ],
        "weaknesses": [
            "No native PRM capabilities",
            "Less customizable than Salesforce for complex partner workflows",
            "Enterprise features can get expensive quickly",
            "Reporting less flexible for partner-specific metrics",
        ],
        "ideal_company_size": "10-5,000 employees",
        "rating": 4.3,
    },
    "dynamics365": {
        "name": "Dynamics 365",
        "slug": "dynamics-365",
        "category": "crm",
        "website": "microsoft.com/dynamics365",
        "tagline": "Microsoft's enterprise CRM and ERP",
        "description": "Microsoft Dynamics 365 is the CRM of choice for companies in the Microsoft ecosystem. Its partner management capabilities are enhanced by integration with Microsoft's own partner programs and Azure Marketplace.",
        "founded": "2003",
        "hq": "Redmond, Washington",
        "pricing": "Starts at $65/user/month for Sales Professional. Enterprise plans from $95/user/month.",
        "best_for": "Companies deeply invested in the Microsoft ecosystem (Azure, Teams, Office 365) that want CRM integration with existing infrastructure.",
        "strengths": [
            "Native integration with Microsoft ecosystem (Azure, Teams, Power BI)",
            "Strong in manufacturing, distribution, and traditional channel sales",
            "Good for companies already using Microsoft Business Applications",
            "LinkedIn Sales Navigator integration",
        ],
        "weaknesses": [
            "Smaller partner tool ecosystem than Salesforce",
            "UI less intuitive than HubSpot or modern SaaS tools",
            "Partner management features require additional customization",
            "Less common in SaaS-native companies",
        ],
        "ideal_company_size": "500-50,000+ employees",
        "rating": 3.9,
    },
    # Analytics
    "tableau": {
        "name": "Tableau",
        "slug": "tableau",
        "category": "analytics",
        "website": "tableau.com",
        "tagline": "Visual analytics platform",
        "description": "Tableau is the leading visual analytics platform used by partnerships teams to build partner performance dashboards, attribution reports, and ecosystem health scorecards.",
        "founded": "2003",
        "hq": "Seattle, Washington (Salesforce company)",
        "pricing": "Creator from $75/user/month. Explorer from $42/user/month. Viewer from $15/user/month.",
        "best_for": "Partnerships teams at Salesforce-centric companies that need advanced visualization and interactive dashboards for partner data.",
        "strengths": [
            "Best-in-class data visualization capabilities",
            "Native Salesforce integration (same parent company)",
            "Large community with partner-specific dashboard templates",
            "Strong for executive-level partner program reporting",
            "Handles large datasets well",
        ],
        "weaknesses": [
            "Learning curve for building dashboards from scratch",
            "Can be expensive for small teams",
            "Requires clean data from CRM/PRM to be effective",
        ],
        "ideal_company_size": "200-100,000+ employees",
        "rating": 4.4,
    },
    "looker": {
        "name": "Looker",
        "slug": "looker",
        "category": "analytics",
        "website": "cloud.google.com/looker",
        "tagline": "Google Cloud's BI platform",
        "description": "Looker (now part of Google Cloud) is a business intelligence platform that partnerships teams use for data modeling, partner metrics, and embedded analytics in partner portals.",
        "founded": "2012",
        "hq": "Santa Cruz, California (Google Cloud)",
        "pricing": "Custom enterprise pricing through Google Cloud.",
        "best_for": "Data-driven partnerships teams at companies using Google Cloud or BigQuery that want modeled, governed metrics rather than ad-hoc dashboards.",
        "strengths": [
            "LookML modeling language ensures consistent metrics definitions",
            "Strong embedded analytics for partner portals",
            "Native Google Cloud and BigQuery integration",
            "Good for building self-serve partner analytics",
        ],
        "weaknesses": [
            "Steeper learning curve than Tableau for non-technical users",
            "Requires data engineering support for LookML modeling",
            "Less visual flexibility than Tableau for one-off analysis",
        ],
        "ideal_company_size": "500-50,000+ employees",
        "rating": 4.1,
    },
    "powerbi": {
        "name": "Power BI",
        "slug": "power-bi",
        "category": "analytics",
        "website": "powerbi.microsoft.com",
        "tagline": "Microsoft's business analytics service",
        "description": "Power BI is Microsoft's business intelligence tool, widely used by partnerships teams in Microsoft-centric organizations for partner reporting and dashboard creation.",
        "founded": "2015",
        "hq": "Redmond, Washington",
        "pricing": "Power BI Pro from $10/user/month. Premium from $20/user/month. Free desktop version available.",
        "best_for": "Partnerships teams at Microsoft-centric organizations that want affordable BI integrated with Dynamics 365, Azure, and Excel.",
        "strengths": [
            "Most affordable enterprise BI tool on the market",
            "Native integration with Microsoft ecosystem",
            "Free desktop version for individual analysis",
            "DAX language is powerful for complex calculations",
            "Good Excel integration for teams transitioning from spreadsheets",
        ],
        "weaknesses": [
            "Visualization options less polished than Tableau",
            "Sharing requires Power BI Pro or Premium licenses",
            "Less common in SaaS-native companies using Salesforce",
        ],
        "ideal_company_size": "100-100,000+ employees",
        "rating": 4.2,
    },
}

# ---------------------------------------------------------------------------
# Comparison definitions
# ---------------------------------------------------------------------------

TOOL_COMPARISONS = [
    {
        "slug": "crossbeam-vs-reveal",
        "tool_a": "crossbeam",
        "tool_b": "reveal",
        "title": "Crossbeam vs Reveal: Co-Selling Platform Comparison (2026)",
        "summary": "Crossbeam and Reveal have merged, but understanding their distinct origins matters. Crossbeam started as a data sharing platform focused on account mapping. Reveal pioneered the 'nearbound' methodology focused on using partner intel to warm up outbound. The combined platform brings both capabilities together.",
        "verdict": "With the merger complete, this is less of a choice and more of an understanding of which workflows you need. The combined Crossbeam+Reveal platform is the clear market leader in co-selling. If you are starting fresh, go with Crossbeam. If you were a Reveal customer, your workflows are being integrated.",
    },
    {
        "slug": "partnerstack-vs-impartner",
        "tool_a": "partnerstack",
        "tool_b": "impartner",
        "title": "PartnerStack vs Impartner: PRM Platform Comparison (2026)",
        "summary": "PartnerStack and Impartner represent two different approaches to PRM. PartnerStack is built for SaaS-native partner programs with automated payouts and a built-in partner marketplace. Impartner is an enterprise PRM designed for complex, multi-tier channel programs with deep Salesforce integration.",
        "verdict": "Choose PartnerStack if you are a B2B SaaS company running affiliate, referral, and reseller programs with under 500 partners. Choose Impartner if you are an enterprise company with 100+ partners, complex tier structures, and heavy Salesforce usage. The price difference is significant: PartnerStack starts around $500/month, Impartner typically runs $2,000-10,000+/month.",
    },
    {
        "slug": "salesforce-prm-vs-partnerstack",
        "tool_a": "salesforce",
        "tool_b": "partnerstack",
        "title": "Salesforce PRM vs PartnerStack: Which PRM for Your Partner Program? (2026)",
        "summary": "Salesforce PRM (built on Experience Cloud) and PartnerStack solve partner management differently. Salesforce PRM extends your existing CRM with partner portals and deal registration. PartnerStack is a standalone platform with its own partner marketplace and automated payouts.",
        "verdict": "Salesforce PRM makes sense if you are already a heavy Salesforce shop, your partners interact with your CRM, and you want a single platform. PartnerStack wins if you want a purpose-built partner experience with automated payouts, a partner marketplace for recruitment, and faster time-to-value without Salesforce customization.",
    },
    {
        "slug": "tableau-vs-power-bi",
        "tool_a": "tableau",
        "tool_b": "powerbi",
        "title": "Tableau vs Power BI for Partnership Analytics (2026)",
        "summary": "Tableau and Power BI are the two dominant BI platforms used by partnership teams. Tableau offers superior visualization and is native to the Salesforce ecosystem. Power BI is dramatically cheaper and integrates with Microsoft Dynamics 365 and the broader Microsoft stack.",
        "verdict": "If your CRM is Salesforce and you have budget for best-in-class visualization, choose Tableau. If your organization is Microsoft-centric or cost-sensitive, Power BI at $10/user/month delivers 80% of the capability at 15% of the cost. Many partnerships teams start with Power BI and graduate to Tableau as their analytics needs mature.",
    },
    {
        "slug": "crossbeam-vs-partnertap",
        "tool_a": "crossbeam",
        "tool_b": "partnertap",
        "title": "Crossbeam vs PartnerTap: Co-Selling Platform Comparison (2026)",
        "summary": "Crossbeam and PartnerTap both offer account mapping and co-selling capabilities, but target different segments. Crossbeam dominates the mid-market SaaS segment with a large network and free tier. PartnerTap focuses on enterprise companies with complex security and compliance requirements.",
        "verdict": "Most B2B SaaS companies should start with Crossbeam. Its free tier, larger partner network, and recent Reveal merger make it the default choice. PartnerTap is worth evaluating if you are an enterprise company with specific compliance requirements or need to map accounts across hundreds of partners simultaneously.",
    },
]

# Roundup definitions
ROUNDUPS = [
    {
        "slug": "best-prm-platforms",
        "title": "Best PRM Platforms for 2026: Complete Comparison",
        "description": "Compare the top PRM platforms for managing partner programs. PartnerStack, Impartner, Allbound, Kiflo, and Channeltivity reviewed with pricing, features, and ideal use cases.",
        "category": "prm",
        "tools": ["partnerstack", "impartner", "allbound", "kiflo", "channeltivity"],
        "intro": "Partner Relationship Management platforms are the operating system for modern channel programs. The right PRM makes the difference between a partner program that scales and one that collapses under manual processes. Here are the leading PRM platforms, ranked by fit for different company stages.",
    },
    {
        "slug": "best-co-selling-tools",
        "title": "Best Co-Selling & Ecosystem Tools for 2026",
        "description": "Compare the top co-selling platforms for ecosystem-led growth. Crossbeam, Reveal, and PartnerTap reviewed with real job posting data.",
        "category": "co-selling",
        "tools": ["crossbeam", "reveal", "partnertap"],
        "intro": "Co-selling tools have become essential for B2B companies that leverage partner ecosystems to accelerate deals. Account mapping and ecosystem data sharing help partner managers identify warm introductions and co-selling opportunities that would be invisible in a direct sales model.",
    },
    {
        "slug": "best-marketplace-management",
        "title": "Best Cloud Marketplace Management Platforms for 2026",
        "description": "Compare the top marketplace management platforms for selling through AWS, Azure, and GCP marketplaces. Tackle.io and AppDirect reviewed.",
        "category": "marketplace",
        "tools": ["tackle", "appdirect"],
        "intro": "Cloud marketplace is one of the fastest-growing channels in B2B software. Enterprise buyers are consolidating spend through cloud commits, making marketplace presence increasingly important for SaaS revenue. These platforms handle the operational complexity of listing, transacting, and scaling through cloud marketplaces.",
    },
]


# ---------------------------------------------------------------------------
# HTML helpers
# ---------------------------------------------------------------------------

def star_rating_html(rating):
    full = int(rating)
    half = 1 if rating - full >= 0.3 else 0
    empty = 5 - full - half
    stars = '<span style="color:var(--pc-secondary)">' + ("&#9733;" * full)
    if half:
        stars += "&#9733;"  # half star shown as full for simplicity
    stars += '</span>'
    stars += '<span style="color:var(--pc-text-tertiary)">' + ("&#9734;" * empty) + '</span>'
    return f'{stars} <span style="color:var(--pc-text-secondary);font-size:var(--pc-text-sm)">{rating}/5</span>'


def mentions_badge(tool_key, tool_data):
    """Show mention count from market intelligence or 'Emerging' badge."""
    # Normalize tool name for lookup
    name = TOOLS[tool_key]["name"]
    count = tool_data.get(name, tool_data.get(name.title(), tool_data.get(name.lower(), 0)))
    if count > 0:
        return f'<span style="color:var(--pc-secondary);font-family:var(--pc-font-mono);font-weight:var(--pc-weight-bold)">{count}</span> mentions in job postings'
    return '<span style="background:var(--pc-secondary-subtle);color:var(--pc-secondary);padding:2px 8px;border-radius:var(--pc-radius-full);font-size:var(--pc-text-sm);font-weight:var(--pc-weight-semibold)">Emerging Tool</span> Niche but essential for partner teams'


# ---------------------------------------------------------------------------
# Tools Index Page
# ---------------------------------------------------------------------------

def build_tools_index(mi_data):
    title = "Partnership & Channel Sales Tool Reviews (2026)"
    description = (
        "Honest reviews of PRM platforms, co-selling tools, marketplace management,"
        " and analytics software for partnerships professionals. Updated regularly."
    )
    crumbs = [("Home", "/"), ("Tools", None)]
    bc_html = breadcrumb_html(crumbs)

    cat_cards = ""
    for cat_slug, cat in CATEGORIES.items():
        tool_count = len([t for t in TOOLS.values() if t["category"] == cat_slug])
        cat_cards += f'''<a href="/tools/category/{cat_slug}/" class="card" style="text-decoration:none;display:block;margin-bottom:var(--pc-space-4)">
    <h3 style="margin-bottom:var(--pc-space-2)">{cat["name"]}</h3>
    <p style="color:var(--pc-text-secondary);margin-bottom:var(--pc-space-2)">{cat["description"]}</p>
    <span style="color:var(--pc-accent);font-weight:var(--pc-weight-semibold);font-size:var(--pc-text-sm)">{tool_count} tools reviewed &rarr;</span>
</a>'''

    body = f'''{bc_html}
<section class="page-header">
    <h1>Partnership Tool Reviews</h1>
    <p style="color:var(--pc-text-secondary);font-size:var(--pc-text-lg);max-width:700px">
        Vendor-neutral reviews of the platforms that power partner ecosystems.
        PRM, co-selling, marketplace management, CRM, and analytics tools.
    </p>
</section>
<div class="container">
    <h2>Browse by Category</h2>
    {cat_cards}

    <h2 style="margin-top:var(--pc-space-12)">Tool Comparisons</h2>
    <div class="related-links-grid">'''

    for comp in TOOL_COMPARISONS:
        ta = TOOLS[comp["tool_a"]]["name"]
        tb = TOOLS[comp["tool_b"]]["name"]
        body += f'<a href="/tools/compare/{comp["slug"]}/" class="related-link-card">{ta} vs {tb}</a>'

    body += '''</div>

    <h2 style="margin-top:var(--pc-space-12)">Best-of Roundups</h2>
    <div class="related-links-grid">'''

    for r in ROUNDUPS:
        body += f'<a href="/tools/best/{r["slug"]}/" class="related-link-card">{r["title"].split(":")[0]}</a>'

    body += "</div>"
    body += newsletter_cta_html("Get weekly tool intel for partnerships professionals.")
    body += "\n</div>"

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/tools/",
        body_content=body, active_path="/tools/",
        extra_head=get_breadcrumb_schema(crumbs), body_class="page-inner",
    )
    write_page("tools/index.html", page)
    print(f"  Built: tools/index.html")


# ---------------------------------------------------------------------------
# Category Pages
# ---------------------------------------------------------------------------

def build_category_page(cat_slug, cat, mi_data):
    tools_in_cat = {k: v for k, v in TOOLS.items() if v["category"] == cat_slug}
    title = f"Best {cat['name']} for Partnerships (2026)"
    description = f"Reviews of {cat['name'].lower()} for partnership and channel teams. {', '.join(t['name'] for t in tools_in_cat.values())} compared."

    crumbs = [("Home", "/"), ("Tools", "/tools/"), (cat["name"], None)]
    bc_html = breadcrumb_html(crumbs)

    tools_html = ""
    for tool_key, tool in sorted(tools_in_cat.items(), key=lambda x: x[1].get("rating", 0), reverse=True):
        mention_html = mentions_badge(tool_key, mi_data.get("tools", {}))
        strengths_html = "".join(f"<li>{s}</li>" for s in tool["strengths"][:3])

        tools_html += f'''<div class="card" style="margin-bottom:var(--pc-space-6)">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:var(--pc-space-2)">
        <div>
            <h3 style="margin-bottom:var(--pc-space-1)"><a href="/tools/review/{tool['slug']}/">{tool["name"]}</a></h3>
            <p style="color:var(--pc-text-tertiary);font-size:var(--pc-text-sm);margin:0">{tool["tagline"]}</p>
        </div>
        <div style="text-align:right">{star_rating_html(tool["rating"])}</div>
    </div>
    <p style="color:var(--pc-text-secondary);margin:var(--pc-space-4) 0">{tool["description"]}</p>
    <div style="margin-bottom:var(--pc-space-3);font-size:var(--pc-text-sm)">{mention_html}</div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:var(--pc-space-4);font-size:var(--pc-text-sm)">
        <div><strong>Best for:</strong> <span style="color:var(--pc-text-secondary)">{tool["ideal_company_size"]}</span></div>
        <div><strong>Pricing:</strong> <span style="color:var(--pc-text-secondary)">{tool["pricing"].split(".")[0]}</span></div>
    </div>
    <ul style="margin-top:var(--pc-space-3);color:var(--pc-text-secondary);font-size:var(--pc-text-sm)">{strengths_html}</ul>
    <a href="/tools/review/{tool['slug']}/" style="font-weight:var(--pc-weight-semibold);font-size:var(--pc-text-sm)">Full review &rarr;</a>
</div>'''

    body = f'''{bc_html}
<section class="page-header">
    <h1>{cat["name"]} for Partnership Teams</h1>
    <p style="color:var(--pc-text-secondary);font-size:var(--pc-text-lg);max-width:700px">{cat["description"]}</p>
</section>
<div class="container">
    <p style="color:var(--pc-text-secondary)">{cat["long_description"]}</p>

    <h2 style="margin-top:var(--pc-space-12)">{cat["name"]} Reviewed</h2>
    {tools_html}
'''
    body += newsletter_cta_html()
    body += "\n</div>"

    page = get_page_wrapper(
        title=title, description=description,
        canonical_path=f"/tools/category/{cat_slug}/",
        body_content=body, active_path="/tools/",
        extra_head=get_breadcrumb_schema(crumbs), body_class="page-inner",
    )
    write_page(f"tools/category/{cat_slug}/index.html", page)
    print(f"  Built: tools/category/{cat_slug}/index.html")


# ---------------------------------------------------------------------------
# Individual Tool Review Pages
# ---------------------------------------------------------------------------

def build_tool_review(tool_key, tool, mi_data):
    cat = CATEGORIES[tool["category"]]
    title = f"{tool['name']} Review for Partner Teams (2026)"
    description = f"{tool['name']} review: {tool['tagline']}. Pricing, strengths, weaknesses, and who should use it. For partnerships and channel professionals."

    crumbs = [("Home", "/"), ("Tools", "/tools/"), (cat["name"], f"/tools/category/{tool['category']}/"), (tool["name"], None)]
    bc_html = breadcrumb_html(crumbs)

    mention_html = mentions_badge(tool_key, mi_data.get("tools", {}))
    strengths_html = "".join(f"<li>{s}</li>" for s in tool["strengths"])
    weaknesses_html = "".join(f"<li>{s}</li>" for s in tool["weaknesses"])

    # Find related tools in same category
    related = {k: v for k, v in TOOLS.items() if v["category"] == tool["category"] and k != tool_key}
    related_html = '<div class="related-links-grid" style="margin-top:var(--pc-space-4)">'
    for rk, rv in related.items():
        related_html += f'<a href="/tools/review/{rv["slug"]}/" class="related-link-card">{rv["name"]} Review</a>'
    related_html += "</div>"

    # Find comparisons involving this tool
    comp_html = ""
    for comp in TOOL_COMPARISONS:
        if comp["tool_a"] == tool_key or comp["tool_b"] == tool_key:
            ta = TOOLS[comp["tool_a"]]["name"]
            tb = TOOLS[comp["tool_b"]]["name"]
            comp_html += f'<a href="/tools/compare/{comp["slug"]}/" class="related-link-card">{ta} vs {tb}</a>'
    if comp_html:
        comp_html = f'<h2 style="margin-top:var(--pc-space-12)">Comparisons</h2><div class="related-links-grid" style="margin-top:var(--pc-space-4)">{comp_html}</div>'

    faq_pairs = [
        (f"How much does {tool['name']} cost?",
         f"{tool['pricing']}"),
        (f"Who should use {tool['name']}?",
         f"{tool['best_for']}"),
        (f"What are the main strengths of {tool['name']}?",
         f"Key strengths include: {', '.join(tool['strengths'][:3])}."),
    ]

    body = f'''{bc_html}
<section class="page-header">
    <h1>{tool["name"]} Review</h1>
    <p style="color:var(--pc-text-secondary);font-size:var(--pc-text-lg)">{tool["tagline"]}</p>
</section>
<div class="container">
    <div class="card" style="margin-bottom:var(--pc-space-8)">
        <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(200px, 1fr));gap:var(--pc-space-4)">
            <div>
                <span style="font-size:var(--pc-text-sm);color:var(--pc-text-tertiary)">Rating</span><br>
                {star_rating_html(tool["rating"])}
            </div>
            <div>
                <span style="font-size:var(--pc-text-sm);color:var(--pc-text-tertiary)">Category</span><br>
                <a href="/tools/category/{tool['category']}/">{cat["name"]}</a>
            </div>
            <div>
                <span style="font-size:var(--pc-text-sm);color:var(--pc-text-tertiary)">Founded</span><br>
                <span style="color:var(--pc-text-primary)">{tool["founded"]}</span>
            </div>
            <div>
                <span style="font-size:var(--pc-text-sm);color:var(--pc-text-tertiary)">HQ</span><br>
                <span style="color:var(--pc-text-primary)">{tool["hq"]}</span>
            </div>
        </div>
        <div style="margin-top:var(--pc-space-4);font-size:var(--pc-text-sm)">{mention_html}</div>
    </div>

    <h2>Overview</h2>
    <p style="color:var(--pc-text-secondary)">{tool["description"]}</p>

    <h2 style="margin-top:var(--pc-space-8)">Who Should Use {tool["name"]}</h2>
    <p style="color:var(--pc-text-secondary)">{tool["best_for"]}</p>
    <p style="color:var(--pc-text-secondary)"><strong>Ideal company size:</strong> {tool["ideal_company_size"]}</p>

    <h2 style="margin-top:var(--pc-space-8)">Pricing</h2>
    <p style="color:var(--pc-text-secondary)">{tool["pricing"]}</p>

    <div style="display:grid;grid-template-columns:1fr 1fr;gap:var(--pc-space-6);margin-top:var(--pc-space-8)">
        <div>
            <h2>Strengths</h2>
            <ul style="color:var(--pc-text-secondary);line-height:1.8">{strengths_html}</ul>
        </div>
        <div>
            <h2>Weaknesses</h2>
            <ul style="color:var(--pc-text-secondary);line-height:1.8">{weaknesses_html}</ul>
        </div>
    </div>

    {comp_html}

    <h2 style="margin-top:var(--pc-space-12)">Other {cat["name"]}</h2>
    {related_html}

    {faq_html(faq_pairs)}

    <div class="source-citation" style="margin-top:var(--pc-space-8)">
        <strong>Website:</strong> <a href="https://{tool['website']}" target="_blank" rel="noopener">{tool['website']}</a>
    </div>
'''
    body += newsletter_cta_html()
    body += "\n</div>"

    page = get_page_wrapper(
        title=title, description=description,
        canonical_path=f"/tools/review/{tool['slug']}/",
        body_content=body, active_path="/tools/",
        extra_head=get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs),
        body_class="page-inner",
    )
    write_page(f"tools/review/{tool['slug']}/index.html", page)
    print(f"  Built: tools/review/{tool['slug']}/index.html")


# ---------------------------------------------------------------------------
# Comparison Pages
# ---------------------------------------------------------------------------

def build_tool_comparison(comp, mi_data):
    ta = TOOLS[comp["tool_a"]]
    tb = TOOLS[comp["tool_b"]]
    title = comp["title"]
    description = f"Compare {ta['name']} and {tb['name']} for partnership teams. Pricing, features, strengths, and which is right for your partner program."

    crumbs = [("Home", "/"), ("Tools", "/tools/"), (f"{ta['name']} vs {tb['name']}", None)]
    bc_html = breadcrumb_html(crumbs)

    ta_strengths = "".join(f"<li>{s}</li>" for s in ta["strengths"][:4])
    tb_strengths = "".join(f"<li>{s}</li>" for s in tb["strengths"][:4])
    ta_weaknesses = "".join(f"<li>{s}</li>" for s in ta["weaknesses"][:3])
    tb_weaknesses = "".join(f"<li>{s}</li>" for s in tb["weaknesses"][:3])

    faq_pairs = [
        (f"Which is better: {ta['name']} or {tb['name']}?",
         comp["verdict"]),
        (f"How do {ta['name']} and {tb['name']} pricing compare?",
         f"{ta['name']}: {ta['pricing'].split('.')[0]}. {tb['name']}: {tb['pricing'].split('.')[0]}."),
    ]

    body = f'''{bc_html}
<section class="page-header">
    <h1>{ta["name"]} vs {tb["name"]}</h1>
</section>
<div class="container">
    <p style="color:var(--pc-text-secondary);font-size:var(--pc-text-lg)">{comp["summary"]}</p>

    <div style="display:grid;grid-template-columns:1fr 1fr;gap:var(--pc-space-6);margin:var(--pc-space-8) 0">
        <div class="card">
            <h3 style="margin-bottom:var(--pc-space-2)">{ta["name"]}</h3>
            <p style="color:var(--pc-text-tertiary);font-size:var(--pc-text-sm);margin-bottom:var(--pc-space-2)">{ta["tagline"]}</p>
            <div style="margin-bottom:var(--pc-space-3)">{star_rating_html(ta["rating"])}</div>
            <div style="font-size:var(--pc-text-sm);margin-bottom:var(--pc-space-2)"><strong>Pricing:</strong> <span style="color:var(--pc-text-secondary)">{ta["pricing"].split(".")[0]}</span></div>
            <div style="font-size:var(--pc-text-sm);margin-bottom:var(--pc-space-4)"><strong>Best for:</strong> <span style="color:var(--pc-text-secondary)">{ta["ideal_company_size"]}</span></div>
            <h4>Strengths</h4>
            <ul style="color:var(--pc-text-secondary);font-size:var(--pc-text-sm)">{ta_strengths}</ul>
            <h4>Weaknesses</h4>
            <ul style="color:var(--pc-text-secondary);font-size:var(--pc-text-sm)">{ta_weaknesses}</ul>
            <a href="/tools/review/{ta['slug']}/" style="font-weight:var(--pc-weight-semibold);font-size:var(--pc-text-sm)">Full review &rarr;</a>
        </div>
        <div class="card">
            <h3 style="margin-bottom:var(--pc-space-2)">{tb["name"]}</h3>
            <p style="color:var(--pc-text-tertiary);font-size:var(--pc-text-sm);margin-bottom:var(--pc-space-2)">{tb["tagline"]}</p>
            <div style="margin-bottom:var(--pc-space-3)">{star_rating_html(tb["rating"])}</div>
            <div style="font-size:var(--pc-text-sm);margin-bottom:var(--pc-space-2)"><strong>Pricing:</strong> <span style="color:var(--pc-text-secondary)">{tb["pricing"].split(".")[0]}</span></div>
            <div style="font-size:var(--pc-text-sm);margin-bottom:var(--pc-space-4)"><strong>Best for:</strong> <span style="color:var(--pc-text-secondary)">{tb["ideal_company_size"]}</span></div>
            <h4>Strengths</h4>
            <ul style="color:var(--pc-text-secondary);font-size:var(--pc-text-sm)">{tb_strengths}</ul>
            <h4>Weaknesses</h4>
            <ul style="color:var(--pc-text-secondary);font-size:var(--pc-text-sm)">{tb_weaknesses}</ul>
            <a href="/tools/review/{tb['slug']}/" style="font-weight:var(--pc-weight-semibold);font-size:var(--pc-text-sm)">Full review &rarr;</a>
        </div>
    </div>

    <div class="card" style="border-color:var(--pc-accent)">
        <h2 style="margin-bottom:var(--pc-space-4)">Our Verdict</h2>
        <p style="color:var(--pc-text-secondary)">{comp["verdict"]}</p>
    </div>

    {faq_html(faq_pairs)}
'''
    body += newsletter_cta_html()
    body += "\n</div>"

    page = get_page_wrapper(
        title=title, description=description,
        canonical_path=f"/tools/compare/{comp['slug']}/",
        body_content=body, active_path="/tools/",
        extra_head=get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs),
        body_class="page-inner",
    )
    write_page(f"tools/compare/{comp['slug']}/index.html", page)
    print(f"  Built: tools/compare/{comp['slug']}/index.html")


# ---------------------------------------------------------------------------
# Roundup Pages
# ---------------------------------------------------------------------------

def build_roundup(roundup, mi_data):
    title = roundup["title"]
    description = roundup["description"]
    cat = CATEGORIES[roundup["category"]]

    crumbs = [("Home", "/"), ("Tools", "/tools/"), (title.split(":")[0], None)]
    bc_html = breadcrumb_html(crumbs)

    tools_html = ""
    for i, tool_key in enumerate(roundup["tools"], 1):
        tool = TOOLS[tool_key]
        mention_html = mentions_badge(tool_key, mi_data.get("tools", {}))
        strengths = "".join(f"<li>{s}</li>" for s in tool["strengths"][:3])

        tools_html += f'''<div class="card" style="margin-bottom:var(--pc-space-6)">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:var(--pc-space-2)">
        <h3 style="margin-bottom:var(--pc-space-1)">#{i}. <a href="/tools/review/{tool['slug']}/">{tool["name"]}</a></h3>
        <div>{star_rating_html(tool["rating"])}</div>
    </div>
    <p style="color:var(--pc-text-tertiary);font-size:var(--pc-text-sm);margin-bottom:var(--pc-space-3)">{tool["tagline"]}</p>
    <p style="color:var(--pc-text-secondary)">{tool["description"]}</p>
    <div style="margin:var(--pc-space-3) 0;font-size:var(--pc-text-sm)">{mention_html}</div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:var(--pc-space-4);font-size:var(--pc-text-sm);margin-bottom:var(--pc-space-3)">
        <div><strong>Ideal for:</strong> <span style="color:var(--pc-text-secondary)">{tool["ideal_company_size"]}</span></div>
        <div><strong>Pricing:</strong> <span style="color:var(--pc-text-secondary)">{tool["pricing"].split(".")[0]}</span></div>
    </div>
    <h4>Key Strengths</h4>
    <ul style="color:var(--pc-text-secondary);font-size:var(--pc-text-sm)">{strengths}</ul>
    <a href="/tools/review/{tool['slug']}/" style="font-weight:var(--pc-weight-semibold);font-size:var(--pc-text-sm)">Full review &rarr;</a>
</div>'''

    body = f'''{bc_html}
<section class="page-header">
    <h1>{title}</h1>
</section>
<div class="container">
    <p style="color:var(--pc-text-secondary);font-size:var(--pc-text-lg)">{roundup["intro"]}</p>

    <h2 style="margin-top:var(--pc-space-12)">The Rankings</h2>
    {tools_html}

    <h2 style="margin-top:var(--pc-space-12)">How to Choose</h2>
    <p style="color:var(--pc-text-secondary)">
        The right {cat["name"].lower()} depends on your company size, partner program maturity, and existing tech stack.
        Consider these factors: current partner count and growth trajectory, CRM platform (Salesforce vs HubSpot vs Dynamics),
        budget constraints, and implementation timeline. Start with our individual reviews for detailed analysis.
    </p>
'''
    body += newsletter_cta_html()
    body += "\n</div>"

    page = get_page_wrapper(
        title=title, description=description,
        canonical_path=f"/tools/best/{roundup['slug']}/",
        body_content=body, active_path="/tools/",
        extra_head=get_breadcrumb_schema(crumbs), body_class="page-inner",
    )
    write_page(f"tools/best/{roundup['slug']}/index.html", page)
    print(f"  Built: tools/best/{roundup['slug']}/index.html")


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def build_all_tools_pages():
    mi_data = load_tool_data()
    print("\n  Building tool pages...")

    # Tools index
    build_tools_index(mi_data)

    # Category pages
    for cat_slug, cat in CATEGORIES.items():
        build_category_page(cat_slug, cat, mi_data)

    # Individual tool reviews
    for tool_key, tool in TOOLS.items():
        build_tool_review(tool_key, tool, mi_data)

    # Comparisons
    for comp in TOOL_COMPARISONS:
        build_tool_comparison(comp, mi_data)

    # Roundups
    for roundup in ROUNDUPS:
        build_roundup(roundup, mi_data)

    count = 1 + len(CATEGORIES) + len(TOOLS) + len(TOOL_COMPARISONS) + len(ROUNDUPS)
    print(f"  Tools section complete: {count} pages")
