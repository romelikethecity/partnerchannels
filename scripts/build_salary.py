# scripts/build_salary.py
# Salary section page generators. ~30 pages from comp_analysis.json.
# Called by build.py. Uses templates.py for HTML shell.

import os
import json

from nav_config import *
from templates import (get_page_wrapper, write_page, get_breadcrumb_schema,
                       get_faq_schema, breadcrumb_html, newsletter_cta_html,
                       faq_html)

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_FILE = os.path.join(PROJECT_DIR, "data", "comp_analysis.json")
JOBS_FILE = os.path.join(PROJECT_DIR, "data", "jobs.json")


def load_salary_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def load_jobs_data():
    """Return list of job dicts from jobs.json."""
    with open(JOBS_FILE, "r", encoding="utf-8") as f:
        return json.load(f).get("jobs", [])


# Substring keywords used to bucket job locations into our 11 metro buckets.
# Order matters: longer / more specific matches first. A job is assigned to
# the first metro whose keyword list matches its location string.
METRO_LOC_KEYWORDS = {
    "Boston": ["Boston", "Cambridge", "Waltham", "Newton, MA", "Burlington, MA", "Quincy, MA"],
    "Denver": ["Denver", "Boulder", "Aurora, CO", "Englewood, CO", "Westminster, CO", "Centennial, CO"],
    "Miami": ["Miami", "Coral Gables", "Aventura", "Doral", "Fort Lauderdale"],
    "Austin": ["Austin"],
    "Washington DC": ["Washington, DC", "Washington, D.C.", "Arlington, VA", "Bethesda", "McLean", "Reston", "Tysons"],
    "New York": ["New York", "Manhattan", "Brooklyn", "Long Island City", "Jersey City", "Hoboken"],
    "San Francisco": ["San Francisco", "Oakland", "Palo Alto", "Mountain View", "Sunnyvale", "Menlo Park", "Cupertino", "Redwood City", "South San Francisco", "Berkeley"],
    "Los Angeles": ["Los Angeles", "Santa Monica", "Culver City", "Pasadena", "El Segundo", "Burbank", "Glendale, CA", "Beverly Hills"],
    "Seattle": ["Seattle", "Bellevue", "Redmond", "Kirkland", "Bothell"],
    "Chicago": ["Chicago", "Evanston", "Schaumburg", "Naperville", "Oak Brook"],
}


def get_metro_jobs(jobs, metro_name):
    """Return jobs whose location string matches the metro's keyword list."""
    keys = METRO_LOC_KEYWORDS.get(metro_name, [])
    if not keys:
        return []
    out = []
    for j in jobs:
        loc = (j.get("location") or "")
        if any(k.lower() in loc.lower() for k in keys):
            out.append(j)
    return out


def fmt_salary(val):
    """Format a salary number as $XXXk or $XXX,XXX."""
    if val >= 1000:
        return f"${val:,.0f}"
    return f"${val:,.0f}"


def fmt_k(val):
    """Format as $120K style."""
    return f"${val / 1000:.0f}K"


def salary_range_str(d):
    """Given a dict with min_base_avg and max_base_avg, return range string."""
    return f"{fmt_k(d['min_base_avg'])} - {fmt_k(d['max_base_avg'])}"


def slug(name):
    return name.lower().replace(" ", "-").replace("/", "-")


# ---------------------------------------------------------------------------
# Stat card HTML helper
# ---------------------------------------------------------------------------

def stat_card(value, label):
    return f'''<div class="stat-block">
    <span class="stat-value">{value}</span>
    <span class="stat-label">{label}</span>
</div>'''


def salary_table(headers, rows):
    """Build a data-table. rows = list of lists matching headers."""
    ths = "".join(f"<th>{h}</th>" for h in headers)
    body = ""
    for row in rows:
        cells = ""
        for i, cell in enumerate(row):
            if i == 0:
                cells += f'<td style="font-weight:var(--pc-weight-semibold)">{cell}</td>'
            else:
                cells += f"<td>{cell}</td>"
        body += f"<tr>{cells}</tr>\n"
    return f'''<div class="table-wrap"><table class="data-table">
<thead><tr>{ths}</tr></thead>
<tbody>{body}</tbody>
</table></div>'''


# ---------------------------------------------------------------------------
# 1. Salary Index
# ---------------------------------------------------------------------------

def build_salary_index(data):
    title = "Partnership & Channel Sales Salary Data 2026"
    description = (
        "Salary benchmarks for partnerships and channel sales professionals."
        " 852 salary records across 8 seniority levels. Entry to SVP compensation data."
    )

    crumbs = [("Home", "/"), ("Salary Data", None)]
    bc_html = breadcrumb_html(crumbs)

    stats = data["salary_stats"]
    by_sen = data["by_seniority"]

    # Build seniority summary rows
    seniority_order = ["Entry", "Mid", "Senior", "Director", "Head of", "VP", "SVP"]
    sen_rows = []
    for s in seniority_order:
        if s in by_sen:
            d = by_sen[s]
            sen_rows.append([
                s,
                str(d["count"]),
                fmt_k(d["median"]),
                salary_range_str(d),
            ])

    # Top paying roles
    top_roles_html = ""
    for role in data["top_paying_roles"][:5]:
        company = role["company"] if role["company"] else "Confidential"
        top_roles_html += f'''<div class="card" style="margin-bottom:var(--pc-space-4)">
    <h4 style="margin-bottom:var(--pc-space-2)">{role["title"]}</h4>
    <p style="color:var(--pc-text-secondary);margin:0">{company}</p>
    <p style="margin:var(--pc-space-2) 0 0"><span class="stat-value" style="font-size:var(--pc-text-lg)">{fmt_salary(role["salary_min"])} - {fmt_salary(role["salary_max"])}</span></p>
</div>'''

    # Metro highlights
    metros = {k: v for k, v in data["by_metro"].items() if k != "Unknown"}
    sorted_metros = sorted(metros.items(), key=lambda x: x[1]["median"], reverse=True)

    metro_rows = []
    for name, d in sorted_metros:
        metro_rows.append([name, str(d["count"]), fmt_k(d["median"]), salary_range_str(d)])

    body = f'''{bc_html}
<section class="page-header">
    <h1>Partnership & Channel Salary Data</h1>
    <p style="color:var(--pc-text-secondary);font-size:var(--pc-text-lg);max-width:700px">
        Compensation benchmarks from {stats["count_with_salary"]:,} real job postings.
        Updated weekly from active partnership and channel sales listings.
    </p>
</section>

<div class="container">
    <div class="stat-grid" style="margin-bottom:var(--pc-space-12)">
        {stat_card(f"{stats['count_with_salary']:,}", "Salary Records")}
        {stat_card(fmt_k(stats['median']), "Median Base Salary")}
        {stat_card(fmt_k(stats['avg']), "Average Base Salary")}
        {stat_card(f"{fmt_k(stats['min'])} - {fmt_k(stats['max'])}", "Full Range")}
    </div>

    <h2>Salary by Seniority Level</h2>
    <p style="color:var(--pc-text-secondary)">Base salary ranges across {len(seniority_order)} seniority levels, from entry-level partner coordinators to SVP of partnerships.</p>
    {salary_table(["Seniority", "Postings", "Median", "Base Range"], sen_rows)}

    <div style="margin-top:var(--pc-space-4)">
        <a href="/salary/by-seniority/" class="btn btn--ghost">View all seniority breakdowns &rarr;</a>
    </div>

    <h2 style="margin-top:var(--pc-space-12)">Salary by Metro Area</h2>
    <p style="color:var(--pc-text-secondary)">Top-paying metro areas for partnerships professionals, ranked by median base salary.</p>
    {salary_table(["Metro", "Postings", "Median", "Base Range"], metro_rows)}

    <div style="margin-top:var(--pc-space-4)">
        <a href="/salary/by-location/" class="btn btn--ghost">View all location data &rarr;</a>
    </div>

    <h2 style="margin-top:var(--pc-space-12)">Highest-Paying Partnership Roles</h2>
    {top_roles_html}

    <h2 style="margin-top:var(--pc-space-12)">Explore Salary Data</h2>
    <div class="related-links-grid">
        <a href="/salary/by-seniority/" class="related-link-card">By Seniority Level</a>
        <a href="/salary/by-location/" class="related-link-card">By Metro Area</a>
        <a href="/salary/remote-vs-onsite/" class="related-link-card">Remote vs Onsite</a>
        <a href="/salary/calculator/" class="related-link-card">Salary Calculator</a>
        <a href="/salary/methodology/" class="related-link-card">Methodology</a>
        <a href="/salary/vs-account-executive/" class="related-link-card">Partner Manager vs AE</a>
        <a href="/salary/vs-bd-manager/" class="related-link-card">vs BD Manager</a>
        <a href="/salary/vs-marketing-manager/" class="related-link-card">vs Marketing Manager</a>
        <a href="/salary/vs-solutions-engineer/" class="related-link-card">vs Solutions Engineer</a>
        <a href="/salary/vs-customer-success-manager/" class="related-link-card">vs Customer Success</a>
    </div>

    <h2 style="margin-top:var(--pc-space-12)">Deeper Analysis</h2>
    <p style="color:var(--pc-text-secondary)">Long-form analyses built on the salary dataset above.</p>
    <div class="preview-grid">
        <a href="/insights/state-of-partner-manager-compensation-2026/" class="preview-card">
            <h3>State of Partner Manager Pay in 2026</h3>
            <p>The median is around $120,000. The top of the market clears $500,000. What the spread tells you about where to build a career.</p>
            <span class="preview-link">Read the analysis &rarr;</span>
        </a>
        <a href="/insights/vp-of-partnerships-compensation/" class="preview-card">
            <h3>VP of Partnerships Pay</h3>
            <p>What 35 disclosed VP postings show about the $170K floor, the $223K ceiling, and where the outlier roles cluster.</p>
            <span class="preview-link">Read the analysis &rarr;</span>
        </a>
        <a href="/insights/salary-disclosure-in-partnerships-roles/" class="preview-card">
            <h3>Why 1 in 3 Partner Jobs Hide Salary</h3>
            <p>The 32 percent hidden-band rate is a signal, not a quirk. Who hides pay, why, and what it predicts about the offer.</p>
            <span class="preview-link">Read the analysis &rarr;</span>
        </a>
    </div>
'''
    body += newsletter_cta_html("Get weekly salary data for partnerships professionals.")
    body += "\n</div>"

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/salary/",
        body_content=body, active_path="/salary/",
        extra_head=get_breadcrumb_schema(crumbs), body_class="page-inner",
    )
    write_page("salary/index.html", page)
    print(f"  Built: salary/index.html")


# ---------------------------------------------------------------------------
# 2. By Seniority (index + individual levels)
# ---------------------------------------------------------------------------

SENIORITY_ORDER = ["Entry", "Mid", "Senior", "Director", "Head of", "VP", "SVP"]
SENIORITY_DESCRIPTIONS = {
    "Entry": "Entry-level partnership roles including Partner Coordinators, Partner Associates, and junior Channel Sales Representatives. Typically 0-2 years of experience.",
    "Mid": "Mid-level partnership professionals including Partner Managers, Channel Account Managers, and Alliance Managers. Usually 2-5 years in partner ecosystems.",
    "Senior": "Senior partnership professionals including Senior Partner Managers, Senior Channel Managers, and Senior Alliance Managers. 5-8 years of experience with proven partner revenue track records.",
    "Director": "Director-level partnership leaders including Director of Partnerships, Director of Channel Sales, and Director of Alliances. 8-12 years experience, managing partner teams and P&L.",
    "Head of": "Head of Partnerships roles, typically reporting to VP or C-suite. Leading the entire partner function at growth-stage companies. Strategic ownership of partner revenue.",
    "VP": "Vice President of Partnerships, VP of Channel Sales, VP of Alliances. Executive leadership over partner ecosystems, typically at companies with $50M+ in partner-influenced revenue.",
    "SVP": "Senior Vice President of Partnerships and Global Alliances. The most senior partnership executives at enterprise companies. Leading global partner ecosystems with 50+ direct and indirect reports.",
}

SENIORITY_TITLES = {
    "Entry": ["Partner Coordinator", "Channel Sales Representative", "Partner Associate", "Junior Alliance Associate", "Partner Program Coordinator"],
    "Mid": ["Partner Manager", "Channel Account Manager", "Alliance Manager", "Partner Development Manager", "Channel Sales Manager"],
    "Senior": ["Senior Partner Manager", "Senior Channel Manager", "Senior Alliance Manager", "Senior Partner Development Manager"],
    "Director": ["Director of Partnerships", "Director of Channel Sales", "Director of Alliances", "Director of Partner Development", "Director of Strategic Partnerships"],
    "Head of": ["Head of Partnerships", "Head of Channel Sales", "Head of Alliances", "Head of Partner Ecosystem"],
    "VP": ["VP of Partnerships", "VP of Channel Sales", "VP of Alliances", "VP of Partner Ecosystem", "VP of Strategic Partnerships"],
    "SVP": ["SVP of Global Partnerships", "SVP of Alliances", "SVP of Channel Sales", "SVP of Partner Ecosystem"],
}


def build_seniority_index(data):
    title = "Partnership Salary by Seniority Level (2026)"
    description = (
        "Partnership and channel sales compensation broken down by seniority."
        " Entry to SVP salary ranges from 852 real job postings. Updated weekly."
    )
    crumbs = [("Home", "/"), ("Salary Data", "/salary/"), ("By Seniority", None)]
    bc_html = breadcrumb_html(crumbs)
    by_sen = data["by_seniority"]

    cards_html = ""
    for s in SENIORITY_ORDER:
        if s not in by_sen:
            continue
        d = by_sen[s]
        s_slug = slug(s)
        cards_html += f'''<a href="/salary/by-seniority/{s_slug}/" class="card" style="text-decoration:none;display:block;margin-bottom:var(--pc-space-4)">
    <h3 style="margin-bottom:var(--pc-space-2)">{s}</h3>
    <div class="stat-grid" style="text-align:left">
        {stat_card(fmt_k(d['median']), "Median")}
        {stat_card(salary_range_str(d), "Base Range")}
        {stat_card(str(d['count']), "Postings")}
    </div>
</a>'''

    body = f'''{bc_html}
<section class="page-header">
    <h1>Partnership Salary by Seniority Level</h1>
    <p style="color:var(--pc-text-secondary);font-size:var(--pc-text-lg)">
        Compensation data across {len(SENIORITY_ORDER)} seniority levels, from Entry to SVP.
    </p>
</section>
<div class="container">
    {cards_html}
'''
    body += newsletter_cta_html()
    body += "\n</div>"

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/salary/by-seniority/",
        body_content=body, active_path="/salary/",
        extra_head=get_breadcrumb_schema(crumbs), body_class="page-inner",
    )
    write_page("salary/by-seniority/index.html", page)
    print(f"  Built: salary/by-seniority/index.html")


def build_seniority_page(level, d, data):
    s_slug = slug(level)
    title = f"{level} Partnership Salary Data (2026)"
    description = f"{level}-level partnership salary: {fmt_k(d['median'])} median from {d['count']} postings. Base range {salary_range_str(d)}. Updated weekly."

    crumbs = [("Home", "/"), ("Salary Data", "/salary/"), ("By Seniority", "/salary/by-seniority/"), (level, None)]
    bc_html = breadcrumb_html(crumbs)

    desc_text = SENIORITY_DESCRIPTIONS.get(level, "")
    titles = SENIORITY_TITLES.get(level, [])
    titles_html = ""
    if titles:
        titles_html = "<h3>Common Titles at This Level</h3><ul>"
        for t in titles:
            titles_html += f"<li>{t}</li>"
        titles_html += "</ul>"

    # Navigation to other levels
    nav_html = '<div class="related-links-grid" style="margin-top:var(--pc-space-8)">'
    for s in SENIORITY_ORDER:
        if s != level and s in data["by_seniority"]:
            nav_html += f'<a href="/salary/by-seniority/{slug(s)}/" class="related-link-card">{s} Salary</a>'
    nav_html += "</div>"

    faq_pairs = [
        (f"What is the median salary for {level} partnership roles?",
         f"The median base salary for {level}-level partnership professionals is {fmt_k(d['median'])}, based on {d['count']} job postings with disclosed compensation."),
        (f"What is the salary range for {level} partnership jobs?",
         f"{level}-level partnership roles typically pay between {salary_range_str(d)} in base salary, depending on location, company size, and specialization."),
    ]

    body = f'''{bc_html}
<section class="page-header">
    <h1>{level}-Level Partnership Salary</h1>
</section>
<div class="container">
    <div class="stat-grid" style="margin-bottom:var(--pc-space-12)">
        {stat_card(fmt_k(d['median']), "Median Base Salary")}
        {stat_card(salary_range_str(d), "Base Range")}
        {stat_card(str(d['count']), "Job Postings")}
    </div>

    <p style="color:var(--pc-text-secondary);font-size:var(--pc-text-lg)">{desc_text}</p>

    {titles_html}

    <h2 style="margin-top:var(--pc-space-12)">How {level} Compares</h2>
    <p style="color:var(--pc-text-secondary)">
        The overall median for all partnership roles is {fmt_k(data['salary_stats']['median'])}.
        {level}-level roles {"pay above" if d['median'] >= data['salary_stats']['median'] else "pay below"} the market median
        by {fmt_k(abs(d['median'] - data['salary_stats']['median']))}.
    </p>

    <h2 style="margin-top:var(--pc-space-12)">Other Seniority Levels</h2>
    {nav_html}

    {faq_html(faq_pairs)}
'''
    body += newsletter_cta_html()
    body += "\n</div>"

    page = get_page_wrapper(
        title=title, description=description, canonical_path=f"/salary/by-seniority/{s_slug}/",
        body_content=body, active_path="/salary/",
        extra_head=get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs),
        body_class="page-inner",
    )
    write_page(f"salary/by-seniority/{s_slug}/index.html", page)
    print(f"  Built: salary/by-seniority/{s_slug}/index.html")


# ---------------------------------------------------------------------------
# 3. By Location (index + individual metros)
# ---------------------------------------------------------------------------

def build_location_index(data):
    title = "Partnership Salary by Location (2026)"
    description = (
        "Partnership and channel sales salary data by metro area."
        " Compare compensation across San Francisco, New York, Austin, and more."
    )
    crumbs = [("Home", "/"), ("Salary Data", "/salary/"), ("By Location", None)]
    bc_html = breadcrumb_html(crumbs)
    metros = {k: v for k, v in data["by_metro"].items() if k != "Unknown"}
    sorted_metros = sorted(metros.items(), key=lambda x: x[1]["median"], reverse=True)

    rows = []
    for name, d in sorted_metros:
        rows.append([
            f'<a href="/salary/by-location/{slug(name)}/">{name}</a>',
            str(d["count"]),
            fmt_k(d["median"]),
            salary_range_str(d),
        ])

    body = f'''{bc_html}
<section class="page-header">
    <h1>Partnership Salary by Metro Area</h1>
    <p style="color:var(--pc-text-secondary);font-size:var(--pc-text-lg)">
        Compensation data across {len(sorted_metros)} major metro areas, ranked by median base salary.
    </p>
</section>
<div class="container">
    {salary_table(["Metro", "Postings", "Median", "Base Range"], rows)}
'''
    body += newsletter_cta_html()
    body += "\n</div>"

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/salary/by-location/",
        body_content=body, active_path="/salary/",
        extra_head=get_breadcrumb_schema(crumbs), body_class="page-inner",
    )
    write_page("salary/by-location/index.html", page)
    print(f"  Built: salary/by-location/index.html")


METRO_CONTEXT = {
    "San Francisco": "San Francisco leads partnership compensation, driven by venture-backed SaaS companies and major tech platforms like Salesforce, Google, and Meta building partner ecosystems.",
    "New York": "New York is the largest market for partnership roles by volume, with strong representation from fintech, media, and enterprise software companies.",
    "Austin": "Austin has emerged as a major partnerships hub, with companies like Dell, Indeed, and a growing SaaS ecosystem offering competitive compensation with lower cost of living.",
    "Washington DC": "Washington DC partnership roles skew toward government channel sales, defense contractors, and GovTech companies with complex compliance requirements.",
    "Seattle": "Seattle partnership salaries reflect the influence of Amazon, Microsoft, and a mature cloud ecosystem where partner programs drive significant revenue.",
    "Los Angeles": "Los Angeles offers a diverse mix of entertainment, adtech, and SaaS partnership roles with compensation competitive to coastal markets.",
    "Chicago": "Chicago partnership roles are concentrated in enterprise software, fintech, and healthcare SaaS, with strong mid-market and enterprise channel programs.",
    "Boston": "Boston partnerships roles cluster around enterprise SaaS, biotech, and edtech companies, with strong compensation driven by the local tech ecosystem.",
    "Denver": "Denver is a growing partnerships market with competitive salaries and a concentration of cybersecurity, cloud, and SaaS channel programs.",
    "Miami": "Miami partnership roles span fintech, real estate tech, and Latin American market expansion, with growing tech migration driving up compensation.",
}


METRO_DEEP = {
    "Boston": {
        "sectors": "Boston's partner manager market is shaped by three industries operating in parallel: enterprise SaaS (HubSpot in Cambridge, Klaviyo, Toast, DataRobot), biotech and pharma (Takeda, Bayer, Vertex, Moderna with partner roles tied to scientific platform partnerships), and edtech (HEI's institutional partnerships, 2U-adjacent vendors). The biotech overlay is what differentiates Boston from any other US partner market. A meaningful share of Boston partner roles involve scientific or clinical co-marketing rather than channel resale, and the comp structure follows pharma norms (high base, lower variable) rather than SaaS norms.",
        "employers": "Datadog, HubSpot, Klaviyo, Takeda, Veracode, SAP, DraftKings, Wayfair, and Toast hire partner managers in greater Boston with some regularity. The biotech-adjacent partner roles cluster in Kendall Square and the I-95 belt; the SaaS partner roles cluster in the Seaport and Cambridge.",
        "negotiation": "Boston partner manager offers tend to anchor on base, with variable comp tighter than SF or NYC. If you are coming from a pharma-adjacent partnerships background, push for the SaaS-style variable structure when interviewing at HubSpot, Klaviyo, or Toast. The pay gap closes meaningfully when you carry quota explicitly tied to partner-sourced revenue.",
    },
    "Denver": {
        "sectors": "Denver's partner ecosystem skews cybersecurity (Ping Identity, Optiv, Arctic Wolf), cloud and infrastructure (DigitalOcean, JumpCloud, Pax8, Coalfire), and a growing fintech and edtech bench (Guild Education, Outdoorsy, Ibotta). The cybersecurity overlay matters because partner roles there often involve managing reseller and MSSP relationships rather than direct co-sell with software vendors, and the partner program economics reflect the security channel's tighter margin structure.",
        "employers": "Arrow Electronics, Pax8, Housecall Pro, Ookla, Transamerica, Xcel Energy, and Suntory Global Spirits show up in partner hiring data for greater Denver. Arrow and Pax8 in particular run formal partner channel programs that pull experienced channel account managers from across the cybersecurity and IT distribution markets.",
        "negotiation": "Denver partner manager comp tends to come in below the national median, partly because the metro's distributor and channel-heavy roles (Arrow, Pax8) carry lower base than venture-backed SaaS PM seats. If you are interviewing for a SaaS partner manager role in Denver and the offer comes in under the SF or NYC median, push back with the national benchmark and note that Boulder cost of living has climbed faster than salary bands.",
    },
    "Miami": {
        "sectors": "Miami's partner manager market is the most recent of the major US metros to mature. The dominant sectors are fintech (Ramp, Marqeta-adjacent, Bitwise), payments (Visa's Miami office for LatAm partnerships, Mastercard regional roles), real estate and proptech (UPSIDEHOM, Lennar partner programs), and a growing LatAm market expansion bench. Many Miami partner roles are explicitly bilingual and explicitly LatAm-coverage, which changes the candidate pool significantly.",
        "employers": "DoorDash, Visa, Mastercard, Amazon, Ramp, Elliptic, Legends Global, and Genentech run partner manager hiring in Miami at varying volumes. The LatAm partnerships seats at Visa and Mastercard pay above the metro median because of the regional coverage premium and language requirement.",
        "negotiation": "Miami partner manager pay sits below other coastal metros at the median, but the variance is large because of the regional roles. If your offer is for a LatAm coverage partner role, anchor on the role's regional scope, not the metro median. The Miami median includes US-only partner coordinators, which drags the number down.",
    },
    "Austin": {
        "sectors": "Austin's partner manager market spans three overlapping pools. The legacy enterprise hub (Dell partner programs, Indeed partnerships, Q2 Holdings, AT&T's enterprise channel), the SaaS growth wave (Braze, ShipperHQ, Dealerware, Auvik Networks), and the newer AI/agency partnerships emerging around TikTok's Austin office, AWS Partnerships in the Domain, and a growing AI-vendor presence. The metro's pay band runs higher than its sample size suggests because Austin attracts senior partner manager roles transferring from SF and NYC.",
        "employers": "TikTok, AWS, Dell, Indeed, Braze, ShipperHQ, ASSA ABLOY, Natera, and the Austin offices of major California-headquartered SaaS companies hire partner managers regularly. The pattern is high-quality, low-volume: fewer postings than NYC, but the postings that do appear are senior and well-compensated.",
        "negotiation": "Austin partner manager offers regularly come in at SF-adjacent pay without the SF cost of living, which is the main reason the metro continues to pull in senior partner talent. If your offer is below $130K base for a senior IC partner role, push back hard with reference to comparable SF, NYC, or Seattle bands. Austin partner pay is no longer the discount it was in 2020.",
    },
    "Washington DC": {
        "sectors": "DC partner manager hiring is driven by three pools: federal channel sales and GovTech (Carahsoft as the dominant federal channel distributor, Peraton, REI Systems, ServiceNow's federal partner team, Salesforce.gov, Microsoft Federal), enterprise SaaS with federal exposure (Dataminr, Snowflake's DC team, Asana's federal seat), and a non-profit and association partnerships layer (NPR, United Way, multilateral and policy organizations). The federal channel partner roles operate by different rules than commercial SaaS PM roles, including security clearances, GWAC contract structure familiarity, and SEWP/CIO-SP3 expertise.",
        "employers": "Thomson Reuters, Peraton, DAGA, Mastercard, Snowflake, NPR, Asana, Dataminr, The Carlyle Group, and Health Evolution show up in DC partner manager hiring data. For federal-specific channel roles, the dominant employer that does not appear directly in JD scrapes is Carahsoft, which runs the federal channel for hundreds of software vendors and is one of the largest single concentrations of federal channel talent in the country.",
        "negotiation": "DC partner manager comp varies more than any other US metro because of the federal-vs-commercial split. A federal channel partner role at Carahsoft, Salesforce.gov, or Microsoft Federal typically pays 10 to 20 percent above the commercial SaaS partner median for the same seniority because the role requires clearance maintenance and federal acquisition expertise that few candidates carry. If you are interviewing for a federal channel partner role, anchor on federal premium, not the DC commercial median.",
    },
    "New York": {
        "sectors": "New York is the largest US market for partner manager hiring by volume. The dominant sectors are fintech and payments (Visa, Mastercard, Ramp, Plaid, Stripe's NY office), media and adtech (NBCUniversal, Spotify, NPR's national programming, Roku, DoubleVerify), enterprise SaaS (Datadog, MongoDB, Asana's NY team), and the world's largest concentration of agency and ad-tech partnership roles.",
        "employers": "Visa, Mastercard, Datadog, MongoDB, Ramp, NBCUniversal, Spotify, Stripe, Asana, and the NY-based teams of every major SaaS vendor run partner manager hiring continuously. NYC also hosts the largest concentration of media partnership roles in the world, which significantly broadens the candidate pool.",
        "negotiation": "NYC partner manager median ($130K) sits close to the national median, but the spread is enormous. Top fintech partnership roles at Visa, Mastercard, and large card networks routinely clear $250K base. Media partnership roles at NBCUniversal, Spotify, and Roku pay in the $140K to $200K base range. If your NYC offer comes in at the metro median, you are probably looking at a generic SaaS partner role, not a fintech or media partnership seat. Push for the sector-specific band.",
    },
    "San Francisco": {
        "sectors": "San Francisco remains the highest-paying US metro for partner manager roles. The dominant employers are the major platform vendors (Salesforce, Snowflake, Databricks, OpenAI, Anthropic), enterprise SaaS partner programs (HubSpot's SF team, Asana, Notion), and a deep bench of venture-backed companies hiring their first partner manager. SF partner roles increasingly involve technology partnerships (ISV integrations, marketplace co-sell) more than traditional channel resale.",
        "employers": "Salesforce, Snowflake, Databricks, OpenAI, Anthropic, Google, Meta, Asana, Notion, Stripe, and a long tail of Series B to D venture-backed SaaS companies recruit partner managers regularly. The AI lab partner roles in particular are a recent and growing pool, and they pay above the SF SaaS median.",
        "negotiation": "SF partner manager comp pays a 41 percent premium over the national median at the metro level. Within SF, the AI lab partner roles (OpenAI, Anthropic) and the major platform partner roles (Salesforce, Snowflake, Databricks) are the highest-paying. If your SF offer comes in below the $160K base mark for a senior IC partner role, push back hard with the metro median ($169K) and the SF AI lab premium as benchmarks.",
    },
    "Los Angeles": {
        "sectors": "LA partner hiring spans entertainment and media partnerships (Disney, Warner Bros. Discovery, NBCUniversal LA team, Hulu, Roblox creator partnerships), adtech (Snap, TikTok, Trade Desk, Magnite), SaaS (Bird, ServiceTitan, ZipRecruiter), and a growing aerospace and direct-to-consumer brand partnerships layer. The entertainment partnership roles operate by different rules than tech partnerships and carry industry-specific compensation patterns.",
        "employers": "Snap, Trade Desk, Disney, NBCUniversal, ServiceTitan, ZipRecruiter, Roblox, and a long tail of adtech and entertainment companies hire partner managers regularly. The Disney and Warner Bros. Discovery partnership roles are often in distribution or licensing rather than SaaS channel sales.",
        "negotiation": "LA partner manager median ($120K) sits slightly above the national median. Entertainment-industry partnership roles often pay less in base but more in industry perks (premieres, screening access, brand connections). If you are coming from SaaS into an entertainment partnership role, expect a base cut and a different career economics. SaaS-to-SaaS moves within LA pay competitively against SF for senior IC roles.",
    },
    "Seattle": {
        "sectors": "Seattle partner manager hiring is dominated by Microsoft and Amazon (and AWS partner roles specifically), plus a growing layer of Microsoft-orbit companies (Smartsheet, Outreach, Auth0, Avalara). The AWS Partner Network alone hires more partner managers in Seattle than most metros hire across all employers combined. Microsoft's ISV and CSP partner programs hire continuously.",
        "employers": "AWS, Microsoft, Smartsheet, Outreach, Avalara, Auvik, Auth0, Tableau, Salesforce's Seattle office, and a long bench of Microsoft-ecosystem partner companies recruit partner managers regularly. Many roles require specific AWS or Azure partner program experience.",
        "negotiation": "Seattle partner manager median ($144K) has climbed faster than any other US metro in the past 12 months, mostly because AWS and Microsoft are expanding partner teams aggressively. If your Seattle offer is below $130K base for a mid-level partner role, push back hard. AWS and Microsoft pay above the metro median, and they set the band for the rest of the local market.",
    },
    "Chicago": {
        "sectors": "Chicago partner hiring spans enterprise SaaS (Salesforce Chicago, Trustwave, ServiceTitan partners), insurance and fintech (Allstate, CME Group, Discover, Morningstar), healthcare SaaS (Tempus, Sprout Social healthcare partnerships), and traditional B2B distribution (Grainger, Ulta Beauty partner programs). The mix gives Chicago a more diversified partner manager market than most metros, with fewer extreme outliers and tighter pay bands.",
        "employers": "Trustwave, CME Group, Discover, Tempus, Sprout Social, Salesforce's Chicago team, Grainger, Allstate, Ulta, and Morningstar hire partner managers in Chicago with some regularity. The financial services and insurance partner roles often involve regulatory complexity that adds to comp but lengthens hiring cycles.",
        "negotiation": "Chicago partner manager median ($115K) sits below the coastal metros. The cost-of-living adjustment partly justifies this, but the gap to SF and NYC is still meaningful. If you are interviewing for a SaaS partner role in Chicago after working in SF or NYC, push hard against the local band and reference the comparable national median. Insurance and fintech partner roles in Chicago can pay 15 to 20 percent above the SaaS metro median because the regulatory expertise carries a premium.",
    },
}


def _metro_companies_html(metro_name, all_jobs):
    """Return HTML listing top companies hiring partner managers in this metro."""
    metro_jobs = get_metro_jobs(all_jobs, metro_name)
    if not metro_jobs:
        return ""
    from collections import Counter
    cc = Counter((j.get("company") or "").strip() for j in metro_jobs if j.get("company"))
    top = [name for name, _ in cc.most_common(12)]
    if not top:
        return ""
    items = "".join(f'<li><a href="/companies/{slug(name)}/">{name}</a></li>' for name in top)
    return f'''
    <h2 style="margin-top:var(--pc-space-12)">Companies Hiring Partner Managers in {metro_name}</h2>
    <p style="color:var(--pc-text-secondary)">Top employers running partner manager and channel sales hiring in greater {metro_name}, ranked by recent posting volume.</p>
    <ul class="metro-employer-list">{items}</ul>
'''


def _metro_sample_roles_html(metro_name, all_jobs, limit=5):
    """Return HTML showing a few real open roles in this metro with salary if disclosed."""
    metro_jobs = get_metro_jobs(all_jobs, metro_name)
    if not metro_jobs:
        return ""
    # Prefer postings with disclosed salary, then trim to limit
    disclosed = [j for j in metro_jobs if j.get("min_amount") and j.get("max_amount") and j["min_amount"] > 0 and j["max_amount"] > 0]
    sample = (disclosed or metro_jobs)[:limit]
    if not sample:
        return ""
    rows = ""
    for j in sample:
        title = (j.get("title") or "Untitled").strip()
        co = (j.get("company") or "").strip()
        loc = (j.get("location") or "").strip()
        min_a, max_a = j.get("min_amount"), j.get("max_amount")
        salary = ""
        if min_a and max_a and min_a > 0 and max_a > 0:
            salary = f"${int(min_a)//1000}K to ${int(max_a)//1000}K"
        salary_cell = f'<td>{salary}</td>' if salary else '<td>Not disclosed</td>'
        rows += f"<tr><td>{title}</td><td>{co}</td><td>{loc}</td>{salary_cell}</tr>"
    return f'''
    <h2 style="margin-top:var(--pc-space-12)">Open Partner Manager Roles in {metro_name}</h2>
    <p style="color:var(--pc-text-secondary)">A small live sample of partner manager and channel sales postings tracked in greater {metro_name}.</p>
    <table class="salary-table">
        <thead><tr><th>Role</th><th>Company</th><th>Location</th><th>Posted Salary</th></tr></thead>
        <tbody>{rows}</tbody>
    </table>
'''


def build_location_page(name, d, data, all_jobs=None):
    m_slug = slug(name)
    title = f"Partnership Salary in {name} (2026)"
    description = f"Partnership salary in {name}: {fmt_k(d['median'])} median from {d['count']} postings. Range {salary_range_str(d)}."
    crumbs = [("Home", "/"), ("Salary Data", "/salary/"), ("By Location", "/salary/by-location/"), (name, None)]
    bc_html = breadcrumb_html(crumbs)

    context = METRO_CONTEXT.get(name, f"{name} is a growing market for partnership and channel sales professionals.")
    overall_median = data["salary_stats"]["median"]
    diff = d["median"] - overall_median
    diff_text = f"{fmt_k(abs(diff))} {'above' if diff > 0 else 'below'} the national median of {fmt_k(overall_median)}"

    deep = METRO_DEEP.get(name, {})
    sectors_html = f'''
    <h2 style="margin-top:var(--pc-space-12)">What Drives Partner Hiring in {name}</h2>
    <p>{deep["sectors"]}</p>''' if deep.get("sectors") else ""
    employers_html = f'''
    <h2 style="margin-top:var(--pc-space-12)">Where the Hiring Concentrates</h2>
    <p>{deep["employers"]}</p>''' if deep.get("employers") else ""
    negotiation_html = f'''
    <h2 style="margin-top:var(--pc-space-12)">How to Negotiate in {name}</h2>
    <p>{deep["negotiation"]}</p>
    <p>For a fuller framework, see our <a href="/careers/negotiating-partner-manager-offer/">guide to negotiating a partner manager offer</a> and the <a href="/insights/state-of-partner-manager-compensation-2026/">state-of-partner-manager-compensation analysis</a>.</p>''' if deep.get("negotiation") else ""

    live_companies_html = _metro_companies_html(name, all_jobs or [])
    live_roles_html = _metro_sample_roles_html(name, all_jobs or [])

    # Other metros navigation
    metros = {k: v for k, v in data["by_metro"].items() if k != "Unknown" and k != name}
    sorted_m = sorted(metros.items(), key=lambda x: x[1]["median"], reverse=True)
    nav_html = '<div class="related-links-grid" style="margin-top:var(--pc-space-4)">'
    for mn, md in sorted_m:
        nav_html += f'<a href="/salary/by-location/{slug(mn)}/" class="related-link-card">{mn}</a>'
    nav_html += "</div>"

    faq_pairs = [
        (f"What is the average partnership salary in {name}?",
         f"The median base salary for partnership roles in {name} is {fmt_k(d['median'])}, based on {d['count']} job postings. The typical range is {salary_range_str(d)}."),
        (f"How does {name} partnership pay compare to the national average?",
         f"{name} partnership compensation is {diff_text}."),
        (f"Which companies hire partner managers in {name}?",
         f"Major employers actively hiring partner managers in greater {name} include {', '.join(METRO_DEEP.get(name, {}).get('employers', '').split(',')[:5]).strip() if METRO_DEEP.get(name, {}).get('employers') else 'a mix of established enterprise SaaS, fintech, and emerging technology companies'}."),
    ]

    body = f'''{bc_html}
<section class="page-header">
    <h1>Partnership Salary in {name}</h1>
</section>
<div class="container">
    <div class="stat-grid" style="margin-bottom:var(--pc-space-12)">
        {stat_card(fmt_k(d['median']), "Median Base Salary")}
        {stat_card(salary_range_str(d), "Base Range")}
        {stat_card(str(d['count']), "Job Postings")}
    </div>

    <p style="color:var(--pc-text-secondary);font-size:var(--pc-text-lg)">{context}</p>

    <h2 style="margin-top:var(--pc-space-12)">How {name} Compares Nationally</h2>
    <p>
        {name} partnership salaries are {diff_text}. With {d['count']} active postings,
        {name} represents {d['count'] / data['salary_stats']['count_with_salary'] * 100:.1f} percent of the national disclosed partner manager market.
        The spread between the 25th and 75th percentile for {name} runs {salary_range_str(d)}, which is wider than most comparable metros at this sample size.
    </p>
    {sectors_html}
    {employers_html}
    {live_companies_html}
    {live_roles_html}
    {negotiation_html}

    <h2 style="margin-top:var(--pc-space-12)">Other Metro Areas</h2>
    {nav_html}

    {faq_html(faq_pairs)}
'''
    body += newsletter_cta_html()
    body += "\n</div>"

    page = get_page_wrapper(
        title=title, description=description, canonical_path=f"/salary/by-location/{m_slug}/",
        body_content=body, active_path="/salary/",
        extra_head=get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs),
        body_class="page-inner",
    )
    write_page(f"salary/by-location/{m_slug}/index.html", page)
    print(f"  Built: salary/by-location/{m_slug}/index.html")


# ---------------------------------------------------------------------------
# 4. Remote vs Onsite
# ---------------------------------------------------------------------------

def build_remote_vs_onsite(data):
    title = "Remote vs Onsite Partnership Salary (2026)"
    description = (
        "Compare remote and onsite partnership salaries."
        " Remote partnerships roles pay differently. See the data from 852 job postings."
    )
    crumbs = [("Home", "/"), ("Salary Data", "/salary/"), ("Remote vs Onsite", None)]
    bc_html = breadcrumb_html(crumbs)

    remote = data["by_remote"]["remote"]
    onsite = data["by_remote"]["onsite"]
    diff = onsite["median"] - remote["median"]

    faq_pairs = [
        ("Do remote partnership roles pay less than onsite?",
         f"On average, yes. Onsite partnership roles have a median salary of {fmt_k(onsite['median'])}, while remote roles have a median of {fmt_k(remote['median'])}. That is a {fmt_k(diff)} difference."),
        ("What percentage of partnership jobs are remote?",
         f"About {remote['count'] / (remote['count'] + onsite['count']) * 100:.0f}% of partnership postings with salary data are listed as remote. The remaining {onsite['count'] / (remote['count'] + onsite['count']) * 100:.0f}% require onsite or hybrid attendance."),
        ("Are remote partnership jobs growing?",
         "Remote partnership roles have grown significantly since 2022, though many companies are returning to hybrid models. Channel sales roles that require in-person partner meetings tend to remain onsite."),
    ]

    body = f'''{bc_html}
<section class="page-header">
    <h1>Remote vs Onsite Partnership Salary</h1>
    <p style="color:var(--pc-text-secondary);font-size:var(--pc-text-lg)">
        How work arrangement affects partnership compensation.
    </p>
</section>
<div class="container">
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:var(--pc-space-6);margin-bottom:var(--pc-space-12)">
        <div class="card">
            <h3 style="margin-bottom:var(--pc-space-4)">Onsite / Hybrid</h3>
            <div class="stat-grid">
                {stat_card(fmt_k(onsite['median']), "Median")}
                {stat_card(salary_range_str(onsite), "Range")}
                {stat_card(str(onsite['count']), "Postings")}
            </div>
        </div>
        <div class="card">
            <h3 style="margin-bottom:var(--pc-space-4)">Remote</h3>
            <div class="stat-grid">
                {stat_card(fmt_k(remote['median']), "Median")}
                {stat_card(salary_range_str(remote), "Range")}
                {stat_card(str(remote['count']), "Postings")}
            </div>
        </div>
    </div>

    <h2>Key Findings</h2>
    <ul style="color:var(--pc-text-secondary);line-height:1.8">
        <li>Onsite partnership roles pay a <strong style="color:var(--pc-secondary)">{fmt_k(diff)}</strong> premium over remote roles at the median</li>
        <li>Remote roles make up <strong>{remote['count'] / (remote['count'] + onsite['count']) * 100:.0f}%</strong> of postings with disclosed salary</li>
        <li>The gap narrows at senior levels where companies compete nationally for talent</li>
        <li>Channel sales roles with in-person partner meeting requirements tend to command higher comp</li>
    </ul>

    <h2 style="margin-top:var(--pc-space-12)">Why the Gap Exists</h2>
    <p style="color:var(--pc-text-secondary)">
        Partnership roles are inherently relationship-driven. Companies building partner ecosystems
        often value in-person presence for QBRs, partner events, and co-selling motions. Remote roles
        tend to cluster in partner operations, enablement, and program management rather than
        revenue-carrying channel sales positions.
    </p>
    <p style="color:var(--pc-text-secondary)">
        Geographic salary adjustment also plays a role. Remote roles draw from a national talent pool,
        while onsite roles in high-cost metros like San Francisco and New York push median compensation higher.
    </p>

    {faq_html(faq_pairs)}
'''
    body += newsletter_cta_html()
    body += "\n</div>"

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/salary/remote-vs-onsite/",
        body_content=body, active_path="/salary/",
        extra_head=get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs),
        body_class="page-inner",
    )
    write_page("salary/remote-vs-onsite/index.html", page)
    print(f"  Built: salary/remote-vs-onsite/index.html")


# ---------------------------------------------------------------------------
# 5. Salary Calculator (email-gated)
# ---------------------------------------------------------------------------

def build_calculator(data):
    title = "Partnership Salary Calculator (2026)"
    description = (
        "Estimate your partnership or channel sales salary based on seniority, location, and work arrangement."
        " Data from 852 real job postings. Free calculator."
    )
    crumbs = [("Home", "/"), ("Salary Data", "/salary/"), ("Calculator", None)]
    bc_html = breadcrumb_html(crumbs)

    # Build JS data object for calculator
    sen_data = {}
    for s in SENIORITY_ORDER:
        if s in data["by_seniority"]:
            d = data["by_seniority"][s]
            sen_data[s] = {"median": d["median"], "min": d["min_base_avg"], "max": d["max_base_avg"]}

    metros = {k: v for k, v in data["by_metro"].items() if k != "Unknown"}
    metro_data = {}
    for name, d in metros.items():
        metro_data[name] = {"median": d["median"], "min": d["min_base_avg"], "max": d["max_base_avg"]}

    overall_median = data["salary_stats"]["median"]
    remote_data = {
        "remote": {"median": data["by_remote"]["remote"]["median"]},
        "onsite": {"median": data["by_remote"]["onsite"]["median"]},
    }

    seniority_options = ""
    for s in SENIORITY_ORDER:
        if s in data["by_seniority"]:
            seniority_options += f'<option value="{s}">{s}</option>'

    metro_options = '<option value="national">National Average</option>'
    for name in sorted(metros.keys()):
        metro_options += f'<option value="{name}">{name}</option>'

    body = f'''{bc_html}
<section class="page-header">
    <h1>Partnership Salary Calculator</h1>
    <p style="color:var(--pc-text-secondary);font-size:var(--pc-text-lg)">
        Estimate your market rate based on seniority, location, and work arrangement.
    </p>
</section>
<div class="container" style="max-width:700px">
    <div id="calculator-gate" class="card" style="text-align:center;padding:var(--pc-space-12)">
        <h2 style="margin-bottom:var(--pc-space-4)">Unlock the Salary Calculator</h2>
        <p style="color:var(--pc-text-secondary);margin-bottom:var(--pc-space-6)">Enter your email to access the calculator and get weekly salary updates.</p>
        <form class="newsletter-cta-form" id="calc-gate-form" onsubmit="return false;" style="max-width:400px;margin:0 auto">
            <input type="email" placeholder="Your work email" aria-label="Email address" required>
            <button type="submit" class="btn btn--primary">Unlock</button>
        </form>
    </div>

    <div id="calculator-app" style="display:none">
        <div class="card" style="margin-bottom:var(--pc-space-6)">
            <div style="margin-bottom:var(--pc-space-6)">
                <label style="display:block;font-weight:var(--pc-weight-semibold);margin-bottom:var(--pc-space-2)">Seniority Level</label>
                <select id="calc-seniority" style="width:100%;padding:var(--pc-space-3);border-radius:var(--pc-radius-md);border:1px solid var(--pc-border-strong);background:var(--pc-bg-primary);color:var(--pc-text-primary);font-size:var(--pc-text-base)">
                    {seniority_options}
                </select>
            </div>
            <div style="margin-bottom:var(--pc-space-6)">
                <label style="display:block;font-weight:var(--pc-weight-semibold);margin-bottom:var(--pc-space-2)">Location</label>
                <select id="calc-location" style="width:100%;padding:var(--pc-space-3);border-radius:var(--pc-radius-md);border:1px solid var(--pc-border-strong);background:var(--pc-bg-primary);color:var(--pc-text-primary);font-size:var(--pc-text-base)">
                    {metro_options}
                </select>
            </div>
            <div style="margin-bottom:var(--pc-space-6)">
                <label style="display:block;font-weight:var(--pc-weight-semibold);margin-bottom:var(--pc-space-2)">Work Arrangement</label>
                <select id="calc-remote" style="width:100%;padding:var(--pc-space-3);border-radius:var(--pc-radius-md);border:1px solid var(--pc-border-strong);background:var(--pc-bg-primary);color:var(--pc-text-primary);font-size:var(--pc-text-base)">
                    <option value="onsite">Onsite / Hybrid</option>
                    <option value="remote">Remote</option>
                </select>
            </div>
        </div>

        <div class="card" id="calc-result" style="text-align:center">
            <h3 style="margin-bottom:var(--pc-space-4)">Your Estimated Salary Range</h3>
            <div class="stat-grid">
                <div class="stat-block">
                    <span class="stat-value" id="calc-low">--</span>
                    <span class="stat-label">Low End</span>
                </div>
                <div class="stat-block">
                    <span class="stat-value" id="calc-mid">--</span>
                    <span class="stat-label">Median</span>
                </div>
                <div class="stat-block">
                    <span class="stat-value" id="calc-high">--</span>
                    <span class="stat-label">High End</span>
                </div>
            </div>
            <p style="color:var(--pc-text-tertiary);font-size:var(--pc-text-sm);margin-top:var(--pc-space-4)">Based on {data['salary_stats']['count_with_salary']:,} salary records from real job postings.</p>
        </div>
    </div>

    <div class="source-citation" style="margin-top:var(--pc-space-8)">
        <strong>Methodology:</strong> This calculator uses median salary data segmented by seniority, location, and work arrangement.
        Location adjustments are applied as ratios against the national median. See our <a href="/salary/methodology/">full methodology</a>.
    </div>
</div>

<script>
(function() {{
    var SEN = {json.dumps(sen_data)};
    var METRO = {json.dumps(metro_data)};
    var REMOTE = {json.dumps(remote_data)};
    var OVERALL = {overall_median};

    var gate = document.getElementById('calculator-gate');
    var app = document.getElementById('calculator-app');
    var gateForm = document.getElementById('calc-gate-form');

    if (localStorage.getItem('pc_calc_unlocked')) {{
        gate.style.display = 'none';
        app.style.display = 'block';
        calc();
    }}

    gateForm.onsubmit = function(e) {{
        e.preventDefault();
        var email = gateForm.querySelector('input').value.trim();
        if (!email) return;
        localStorage.setItem('pc_calc_unlocked', '1');
        gate.style.display = 'none';
        app.style.display = 'block';
        calc();
    }};

    function fmt(n) {{
        return '$' + Math.round(n / 1000) + 'K';
    }}

    function calc() {{
        var sen = document.getElementById('calc-seniority').value;
        var loc = document.getElementById('calc-location').value;
        var remote = document.getElementById('calc-remote').value;

        var base = SEN[sen] || {{median: OVERALL, min: OVERALL * 0.8, max: OVERALL * 1.2}};

        // Location adjustment
        var locAdj = 1.0;
        if (loc !== 'national' && METRO[loc]) {{
            locAdj = METRO[loc].median / OVERALL;
        }}

        // Remote adjustment
        var remoteAdj = 1.0;
        if (remote === 'remote') {{
            remoteAdj = REMOTE.remote.median / REMOTE.onsite.median;
        }}

        var low = base.min * locAdj * remoteAdj;
        var mid = base.median * locAdj * remoteAdj;
        var high = base.max * locAdj * remoteAdj;

        document.getElementById('calc-low').textContent = fmt(low);
        document.getElementById('calc-mid').textContent = fmt(mid);
        document.getElementById('calc-high').textContent = fmt(high);
    }}

    document.getElementById('calc-seniority').onchange = calc;
    document.getElementById('calc-location').onchange = calc;
    document.getElementById('calc-remote').onchange = calc;
}})();
</script>
'''

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/salary/calculator/",
        body_content=body, active_path="/salary/",
        extra_head=get_breadcrumb_schema(crumbs), body_class="page-inner",
    )
    write_page("salary/calculator/index.html", page)
    print(f"  Built: salary/calculator/index.html")


# ---------------------------------------------------------------------------
# 6. Methodology
# ---------------------------------------------------------------------------

def build_methodology(data):
    title = "Salary Data Methodology"
    description = (
        "How Partner Channels collects and analyzes partnership salary data."
        " Sources, methodology, and limitations of our compensation benchmarks."
    )
    crumbs = [("Home", "/"), ("Salary Data", "/salary/"), ("Methodology", None)]
    bc_html = breadcrumb_html(crumbs)

    body = f'''{bc_html}
<section class="page-header">
    <h1>Salary Data Methodology</h1>
</section>
<div class="container" style="max-width:800px">
    <p style="color:var(--pc-text-secondary);font-size:var(--pc-text-lg)">
        Transparency matters. Here is exactly how we collect, process, and present partnership salary data.
    </p>

    <h2 style="margin-top:var(--pc-space-12)">Data Sources</h2>
    <p style="color:var(--pc-text-secondary)">
        Our salary data comes from real job postings collected from major job boards, company career pages,
        and recruiting platforms. We focus exclusively on roles in partnerships, channel sales, alliances,
        and partner ecosystem management.
    </p>

    <h2 style="margin-top:var(--pc-space-8)">Current Dataset</h2>
    <div class="stat-grid" style="margin:var(--pc-space-6) 0">
        {stat_card(f"{data['total_records']:,}", "Total Job Postings")}
        {stat_card(f"{data['records_with_salary']:,}", "With Salary Data")}
        {stat_card(f"{data['disclosure_rate']:.1f}%", "Disclosure Rate")}
    </div>

    <h2 style="margin-top:var(--pc-space-8)">Seniority Classification</h2>
    <p style="color:var(--pc-text-secondary)">
        We classify roles into 8 seniority levels based on job title, reporting structure, and
        job description keywords. The levels are: Entry, Mid, Senior, Director, Head of, VP, SVP,
        and Unknown (when the title is ambiguous).
    </p>

    <h2 style="margin-top:var(--pc-space-8)">Location Classification</h2>
    <p style="color:var(--pc-text-secondary)">
        Job postings are mapped to metro areas based on the listed location. Remote roles are
        classified separately. Postings that list multiple locations or vague geographic descriptions
        are classified as Unknown and excluded from metro-specific analysis.
    </p>

    <h2 style="margin-top:var(--pc-space-8)">Salary Reporting</h2>
    <p style="color:var(--pc-text-secondary)">
        We report base salary only. When a job posting lists a range, we use the minimum and maximum.
        When only a single figure is listed, it is used as both min and max. OTE (on-target earnings),
        equity, and bonuses are tracked separately as compensation signals but are not included in
        base salary calculations.
    </p>

    <h2 style="margin-top:var(--pc-space-8)">Statistical Methods</h2>
    <ul style="color:var(--pc-text-secondary);line-height:1.8">
        <li><strong>Median:</strong> The middle value when all salaries are sorted. Less sensitive to extreme outliers than averages.</li>
        <li><strong>Average range:</strong> The mean of reported salary minimums and maximums within each segment.</li>
        <li><strong>Count:</strong> The number of job postings with disclosed salary data in each category.</li>
    </ul>

    <h2 style="margin-top:var(--pc-space-8)">Limitations</h2>
    <ul style="color:var(--pc-text-secondary);line-height:1.8">
        <li>Only {data['disclosure_rate']:.0f}% of postings disclose salary, creating selection bias toward companies in states with pay transparency laws</li>
        <li>Base salary does not reflect total compensation, which can include 20-50% variable pay at senior levels</li>
        <li>Small sample sizes in some metro areas and seniority levels mean wider confidence intervals</li>
        <li>Data is refreshed weekly but reflects a point-in-time snapshot of the job market</li>
    </ul>

    <h2 style="margin-top:var(--pc-space-8)">Update Frequency</h2>
    <p style="color:var(--pc-text-secondary)">
        Data is collected and processed weekly. All figures on the site reflect the most recent
        data collection cycle.
    </p>

    <div class="source-citation" style="margin-top:var(--pc-space-8)">
        Questions about our methodology? Contact <a href="mailto:rome@getprovyx.com">rome@getprovyx.com</a>.
    </div>
'''
    body += newsletter_cta_html()
    body += "\n</div>"

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/salary/methodology/",
        body_content=body, active_path="/salary/",
        extra_head=get_breadcrumb_schema(crumbs), body_class="page-inner",
    )
    write_page("salary/methodology/index.html", page)
    print(f"  Built: salary/methodology/index.html")


# ---------------------------------------------------------------------------
# 7. Comparison Pages
# ---------------------------------------------------------------------------

COMPARISONS = [
    {
        "slug": "vs-account-executive",
        "title": "Partner Manager vs Account Executive Salary (2026)",
        "role_a": "Partner Manager",
        "role_b": "Account Executive",
        "role_b_median": 95000,
        "role_b_range": "$70K - $140K",
        "role_b_description": "Account Executives focus on direct sales to end customers, carrying individual quotas and managing the full sales cycle from prospecting to close.",
        "key_differences": [
            "Partner Managers build scalable revenue through third-party relationships; AEs close individual deals directly",
            "AE comp is typically 50/50 base/variable; Partner Managers lean 70/30 or 80/20",
            "Partner Managers have longer ramp times (6-12 months) vs AEs (3-6 months)",
            "AE roles are more common at every company; Partner Manager roles require existing partner programs",
            "Partner Manager career ceiling (VP/SVP Partnerships) often reports to CRO alongside VP Sales",
        ],
        "why_switch": "Partners professionals often earn more in base salary with lower variable risk. The career path to VP of Partnerships is less crowded than VP of Sales, though it requires patience building ecosystems that take quarters to generate revenue.",
    },
    {
        "slug": "vs-bd-manager",
        "title": "Partner Manager vs Business Development Manager Salary (2026)",
        "role_a": "Partner Manager",
        "role_b": "Business Development Manager",
        "role_b_median": 88000,
        "role_b_range": "$65K - $130K",
        "role_b_description": "Business Development Managers source and qualify new business opportunities, often focused on outbound prospecting and market expansion.",
        "key_differences": [
            "BD Managers focus on net-new opportunity creation; Partner Managers focus on ecosystem-led revenue through existing partnerships",
            "BD roles are typically earlier in career and feed the sales pipeline; Partner roles manage ongoing relationships",
            "Partner Managers often need cross-functional skills (marketing, product, sales) that BD roles do not require",
            "BD comp is more heavily weighted toward variable; Partner Manager base is typically higher",
            "BD managers work a single company's pipeline; Partner Managers influence revenue across multiple partner organizations",
        ],
        "why_switch": "Partnership roles offer higher base salary, more strategic influence, and a clearer path to executive leadership. The trade-off is longer time-to-impact and less immediate feedback than BD roles.",
    },
    {
        "slug": "vs-marketing-manager",
        "title": "Partner Manager vs Marketing Manager Salary (2026)",
        "role_a": "Partner Manager",
        "role_b": "Marketing Manager",
        "role_b_median": 92000,
        "role_b_range": "$65K - $135K",
        "role_b_description": "Marketing Managers plan and execute campaigns, manage channels, and drive brand awareness and demand generation for products and services.",
        "key_differences": [
            "Partner Managers carry revenue targets; Marketing Managers typically own pipeline or MQL metrics",
            "Marketing Manager roles exist at every company; Partner Manager roles require mature partner programs",
            "Partner Managers have variable compensation (commissions/bonuses); Marketing Managers rarely do",
            "Partner Management requires strong sales skills alongside marketing knowledge",
            "Marketing career paths lead to CMO; Partnership paths lead to VP Partnerships or Chief Partner Officer",
        ],
        "why_switch": "Partner Marketing is a natural bridge role. Many Partner Managers come from marketing backgrounds and find the combination of strategic thinking and revenue ownership appealing. The higher comp reflects the added accountability.",
    },
    {
        "slug": "vs-solutions-engineer",
        "title": "Partner Manager vs Solutions Engineer Salary (2026)",
        "role_a": "Partner Manager",
        "role_b": "Solutions Engineer",
        "role_b_median": 130000,
        "role_b_range": "$95K - $180K",
        "role_b_description": "Solutions Engineers (SE / Pre-Sales Engineers) provide technical expertise during the sales process, running demos, building POCs, and bridging product capability with customer requirements.",
        "key_differences": [
            "Solutions Engineers earn higher base salary but have less variable upside than Partner Managers",
            "SE roles require deep technical skills; Partner Managers need relationship and business development skills",
            "Partner Managers have more strategic autonomy; SEs support the sales process directed by AEs",
            "SE roles have clearer daily workflows; Partner Manager roles are more ambiguous and self-directed",
            "Partner career paths lead to executive roles; SE paths lead to SE Leadership or Solutions Architect",
        ],
        "why_switch": "Partner Solutions Engineers (Partner SEs) is a growing hybrid role that combines both skill sets. For SEs wanting business-side influence and for Partner Managers wanting to go deeper technically, this bridge role is worth watching.",
    },
    {
        "slug": "vs-customer-success-manager",
        "title": "Partner Manager vs Customer Success Manager Salary (2026)",
        "role_a": "Partner Manager",
        "role_b": "Customer Success Manager",
        "role_b_median": 85000,
        "role_b_range": "$60K - $125K",
        "role_b_description": "Customer Success Managers (CSMs) manage post-sale customer relationships, driving adoption, retention, and expansion revenue.",
        "key_differences": [
            "CSMs manage individual customer accounts; Partner Managers manage relationships that influence many accounts",
            "Partner Managers typically earn more at equivalent seniority levels due to revenue attribution",
            "CSM comp is mostly base with retention bonuses; Partner Manager comp includes meaningful variable",
            "CSM roles are post-sale; Partner Manager roles span the full lifecycle from recruitment to co-selling",
            "Both roles are relationship-driven, making CSM-to-Partner Manager a common career transition",
        ],
        "why_switch": "Customer Success to Partner Management is one of the most natural career transitions in SaaS. The relationship skills transfer directly, and the jump in comp reflects the broader scope of influence.",
    },
]


def build_comparison_page(comp, data):
    pm_median = data["by_seniority"]["Mid"]["median"]  # Use Mid-level as "Partner Manager" proxy
    title = comp["title"]
    s = comp["slug"]
    description = f"Compare {comp['role_a']} and {comp['role_b']} salary, career path, and compensation structure. Real data from 2026 job postings."

    crumbs = [("Home", "/"), ("Salary Data", "/salary/"), (f"{comp['role_a']} vs {comp['role_b']}", None)]
    bc_html = breadcrumb_html(crumbs)

    diff = pm_median - comp["role_b_median"]
    diff_pct = diff / comp["role_b_median"] * 100

    diffs_html = ""
    for d in comp["key_differences"]:
        diffs_html += f"<li>{d}</li>"

    # Other comparisons nav
    other_comps = [c for c in COMPARISONS if c["slug"] != s]
    nav_html = '<div class="related-links-grid" style="margin-top:var(--pc-space-4)">'
    for c in other_comps:
        nav_html += f'<a href="/salary/{c["slug"]}/" class="related-link-card">{c["role_a"]} vs {c["role_b"]}</a>'
    nav_html += "</div>"

    faq_pairs = [
        (f"Who earns more: {comp['role_a']} or {comp['role_b']}?",
         f"At the mid-level, {comp['role_a']}s earn a median of {fmt_k(pm_median)} vs {fmt_k(comp['role_b_median'])} for {comp['role_b']}s. That is a {fmt_k(abs(diff))} {'premium' if diff > 0 else 'deficit'} for partnership roles."),
        (f"Should I switch from {comp['role_b']} to {comp['role_a']}?",
         comp["why_switch"]),
    ]

    body = f'''{bc_html}
<section class="page-header">
    <h1>{comp['role_a']} vs {comp['role_b']} Salary</h1>
</section>
<div class="container">
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:var(--pc-space-6);margin-bottom:var(--pc-space-12)">
        <div class="card" style="text-align:center">
            <h3 style="margin-bottom:var(--pc-space-4)">{comp['role_a']}</h3>
            <span class="stat-value" style="font-size:var(--pc-text-2xl)">{fmt_k(pm_median)}</span>
            <span class="stat-label">Median Base Salary</span>
        </div>
        <div class="card" style="text-align:center">
            <h3 style="margin-bottom:var(--pc-space-4)">{comp['role_b']}</h3>
            <span class="stat-value" style="font-size:var(--pc-text-2xl)">{fmt_k(comp['role_b_median'])}</span>
            <span class="stat-label">Median Base Salary</span>
        </div>
    </div>

    <div class="card" style="text-align:center;margin-bottom:var(--pc-space-8)">
        <span class="stat-value" style="font-size:var(--pc-text-xl)">{"+" if diff > 0 else ""}{fmt_k(diff)} ({diff_pct:+.0f}%)</span>
        <span class="stat-label">{comp['role_a']} {"premium" if diff > 0 else "deficit"} vs {comp['role_b']}</span>
    </div>

    <h2>What Does a {comp['role_b']} Do?</h2>
    <p style="color:var(--pc-text-secondary)">{comp['role_b_description']}</p>

    <h2 style="margin-top:var(--pc-space-8)">Key Differences</h2>
    <ul style="color:var(--pc-text-secondary);line-height:1.8">
        {diffs_html}
    </ul>

    <h2 style="margin-top:var(--pc-space-8)">Career Transition Outlook</h2>
    <p style="color:var(--pc-text-secondary)">{comp['why_switch']}</p>

    <h2 style="margin-top:var(--pc-space-12)">More Salary Comparisons</h2>
    {nav_html}

    {faq_html(faq_pairs)}
'''
    body += newsletter_cta_html()
    body += "\n</div>"

    page = get_page_wrapper(
        title=title, description=description, canonical_path=f"/salary/{s}/",
        body_content=body, active_path="/salary/",
        extra_head=get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs),
        body_class="page-inner",
    )
    write_page(f"salary/{s}/index.html", page)
    print(f"  Built: salary/{s}/index.html")


# ---------------------------------------------------------------------------
# Main entry point (called by build.py)
# ---------------------------------------------------------------------------

def build_all_salary_pages():
    data = load_salary_data()
    all_jobs = load_jobs_data()
    print("\n  Building salary pages...")

    # 1. Index
    build_salary_index(data)

    # 2. Seniority index + individual levels
    build_seniority_index(data)
    for level in SENIORITY_ORDER:
        if level in data["by_seniority"]:
            build_seniority_page(level, data["by_seniority"][level], data)

    # 3. Location index + individual metros (with live company + role data)
    build_location_index(data)
    for name, d in data["by_metro"].items():
        if name != "Unknown":
            build_location_page(name, d, data, all_jobs=all_jobs)

    # 4. Remote vs Onsite
    build_remote_vs_onsite(data)

    # 5. Calculator
    build_calculator(data)

    # 6. Methodology
    build_methodology(data)

    # 7. Comparisons
    for comp in COMPARISONS:
        build_comparison_page(comp, data)

    count = 1 + 1 + len([s for s in SENIORITY_ORDER if s in data["by_seniority"]]) + \
            1 + len([k for k in data["by_metro"] if k != "Unknown"]) + \
            1 + 1 + 1 + len(COMPARISONS)
    print(f"  Salary section complete: {count} pages")
