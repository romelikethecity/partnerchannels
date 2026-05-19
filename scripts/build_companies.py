# scripts/build_companies.py
# Company pages generator: /companies/ index + /companies/{slug}/ detail pages.
# Reads jobs.json data and generates pages for companies with 2+ listings.

import os
import sys
import json
import re
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nav_config import *
from templates import (get_page_wrapper, write_page, get_breadcrumb_schema,
                       breadcrumb_html, newsletter_cta_html)

ROLE_NAME = "Partnerships"
CURRENT_YEAR = 2026


# Humanized descriptions for the structural signals extracted from JDs.
# Keys are normalized signal_value strings (matched case-insensitively).
SIGNAL_DESCRIPTIONS = {
    "build team": "Building out a partner team from scratch or scaling an existing one. Expect higher operational ownership.",
    "first hire": "First or among the first partner hires at this company. Greenfield work with executive air cover but no playbook.",
    "channel": "Indirect revenue motion through resellers, distributors, MSPs, or referral partners.",
    "direct": "Direct sales motion alongside the partner work; partner team is not the only revenue path.",
    "enterprise": "Enterprise segment focus, typical deal size in the $100K+ range.",
    "fortune 500": "Fortune 500 segment focus, longer sales cycles and larger deal sizes.",
    "smb": "Small-to-medium business segment focus, higher transaction volume.",
    "mid market": "Mid-market segment focus.",
    "enterprise deal": "Deal sizes regularly land in the enterprise range.",
    "seven figure": "Quota or revenue targets explicitly in the seven figures.",
    "transactional": "Transactional motion with shorter sales cycles.",
    "mid deal": "Mid-sized deal motion.",
    "global": "Global scope with multi-region partner coverage.",
    "north america": "North America regional focus.",
    "emea": "EMEA regional focus.",
    "apac": "APAC regional focus.",
    "latam": "Latin America regional focus.",
    "reports cro": "Partner leader reports directly to the CRO. Tightly tied to direct-sales motion and quota.",
    "reports ceo": "Partner leader reports to the CEO. Strategic / cross-functional positioning.",
    "reports vp": "Partner leader reports into a VP rather than CRO. Typically a sub-function rather than a top-line org.",
    "player coach": "Player-coach role: individual contribution plus team management.",
    "equity": "Equity compensation is part of the package.",
    "ote mentioned": "OTE structure (base + variable) is explicitly defined in the posting.",
    "uncapped": "Uncapped variable compensation.",
    "long": "Long sales cycle, multi-quarter or longer.",
    "short": "Short sales cycle, fast pipeline velocity.",
    "growth hire": "Growth-mode hire: company is expanding rather than backfilling.",
    "turnaround": "Turnaround context: prior partner program needs to be rebuilt or restructured.",
    "immediate": "Immediate-start signal; the company wants someone working in weeks, not quarters.",
    "solution selling": "Uses Solution Selling as the named methodology.",
    "value selling": "Uses Value Selling as the named methodology.",
    "meddic": "Uses MEDDIC qualification framework.",
    "miller heiman": "Uses Miller Heiman strategic selling.",
    "sandler": "Uses Sandler selling system.",
    "bant": "Uses BANT qualification.",
}


def slugify(text):
    """Convert text to URL slug."""
    s = text.lower().strip()
    s = re.sub(r'[^a-z0-9\s-]', '', s)
    s = re.sub(r'[\s]+', '-', s)
    s = re.sub(r'-+', '-', s)
    return s.strip('-')


def fmt_salary_range(job):
    """Format salary range from job data, or return empty string."""
    min_amt = job.get("min_amount")
    max_amt = job.get("max_amount")
    if min_amt and max_amt and min_amt > 0 and max_amt > 0:
        return f"${min_amt // 1000}K - ${max_amt // 1000}K"
    elif min_amt and min_amt > 0:
        return f"${min_amt // 1000}K+"
    elif max_amt and max_amt > 0:
        return f"Up to ${max_amt // 1000}K"
    return ""


def load_jobs(project_dir):
    """Load jobs.json and return list of job dicts."""
    path = os.path.join(project_dir, "data", "jobs.json")
    with open(path, "r") as f:
        data = json.load(f)
    return data.get("jobs", [])


def get_company_data(jobs):
    """Group jobs by company. Returns dict of company_name -> list of jobs."""
    companies = defaultdict(list)
    for job in jobs:
        company = (job.get("company") or "").strip()
        if company:
            companies[company].append(job)
    return companies


def get_company_locations(jobs):
    """Extract unique locations from a company's jobs."""
    locations = set()
    for job in jobs:
        loc = (job.get("location") or "").strip()
        if loc:
            locations.add(loc)
    return sorted(locations)


# ---------------------------------------------------------------------------
# Per-company enrichment helpers
# ---------------------------------------------------------------------------

def load_comp_analysis(project_dir):
    """Load comp_analysis.json for national/seniority comparison context."""
    path = os.path.join(project_dir, "data", "comp_analysis.json")
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        return json.load(f)


_ABOUT_PATTERNS = [
    # Match "About <Company>" or "About Us" headings followed by a paragraph
    re.compile(r"(?:^|\n)\s*(?:#+\s*)?\**About\s+(?:Us|the\s+Role|the\s+Team|the\s+Position|the\s+Company|[A-Z][A-Za-z0-9&.\- ]{1,80})\**\s*\n+([^\n#][\s\S]{60,800}?)(?=\n\s*\n|\n#+|\n\*\*[A-Z])", re.IGNORECASE),
    re.compile(r"(?:^|\n)\s*\**Who\s+We\s+Are\**\s*\n+([^\n#][\s\S]{60,800}?)(?=\n\s*\n|\n#+|\n\*\*[A-Z])", re.IGNORECASE),
    re.compile(r"(?:^|\n)\s*\**What\s+We\s+Do\**\s*\n+([^\n#][\s\S]{60,800}?)(?=\n\s*\n|\n#+|\n\*\*[A-Z])", re.IGNORECASE),
    re.compile(r"(?:^|\n)\s*\**Our\s+Story\**\s*\n+([^\n#][\s\S]{60,800}?)(?=\n\s*\n|\n#+|\n\*\*[A-Z])", re.IGNORECASE),
    re.compile(r"(?:^|\n)\s*\**Company\s+Overview\**\s*\n+([^\n#][\s\S]{60,800}?)(?=\n\s*\n|\n#+|\n\*\*[A-Z])", re.IGNORECASE),
]


# Banned word patterns that should reject a JD excerpt rather than try to
# rewrite source quotes. Mirrors the ai-audit skill's HIGH-severity list.
_BANNED_WORD_RE = re.compile(
    r"\b(robust|leverage|utilize|synergy|holistic|cutting-edge|seamless|nuanced|"
    r"delve|foster|bolster|underscore|unveil|streamline|furthermore|moreover|"
    r"notwithstanding|game-changer|paradigm shift|game changer)\b",
    re.IGNORECASE,
)


def _clean_jd_excerpt(text):
    """Strip markdown, em dashes, link syntax, and excessive whitespace from a JD excerpt."""
    # Remove markdown bold/italic markers
    text = re.sub(r"\*+", "", text)
    # Remove escape backslashes Indeed/LinkedIn inject before punctuation
    text = re.sub(r"\\([\-\.\,\!\?\+\(\)])", r"\1", text)
    # Replace em/en dashes (used parenthetically in JDs) with a comma + space
    text = text.replace("—", ", ").replace("–", ", ")
    # Collapse whitespace and clean trailing punctuation
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"[\s•\-]+$", "", text).strip()
    # Collapse double commas introduced by the em-dash swap
    text = re.sub(r",\s*,", ",", text)
    return text


def _excerpt_passes_audit(text):
    """Return True if the cleaned excerpt is free of HIGH-severity AI tells."""
    if not text:
        return False
    if _BANNED_WORD_RE.search(text):
        return False
    return True


def _extract_about_paragraph(jobs, company_name):
    """Pull an 'About X' paragraph from one of the company's JDs.

    Returns a cleaned 1-3 sentence excerpt that passes the AI audit, or
    None if no usable text found.
    """
    for job in jobs:
        desc = job.get("description") or ""
        if not desc:
            continue
        for pat in _ABOUT_PATTERNS:
            m = pat.search(desc)
            if m:
                excerpt = _clean_jd_excerpt(m.group(1))
                if 60 <= len(excerpt) <= 700 and _excerpt_passes_audit(excerpt):
                    return excerpt
    # Fallback: pull the first non-empty paragraph that mentions the company name
    for job in jobs:
        desc = job.get("description") or ""
        paras = re.split(r"\n\s*\n", desc)
        for p in paras[:5]:
            cleaned = _clean_jd_excerpt(p)
            if 80 <= len(cleaned) <= 500 and company_name.lower()[:8] in cleaned.lower() and _excerpt_passes_audit(cleaned):
                return cleaned
    return None


def _compute_compensation_context(jobs, comp_data):
    """Return a dict with company-vs-market salary comparison numbers."""
    disclosed = [(j.get("min_amount", 0) or 0, j.get("max_amount", 0) or 0, j.get("seniority", ""))
                 for j in jobs if (j.get("min_amount") or 0) > 0 and (j.get("max_amount") or 0) > 0]
    if not disclosed:
        return None
    # Company midpoint
    midpoints = [(mn + mx) / 2 for mn, mx, _ in disclosed]
    company_median = sorted(midpoints)[len(midpoints) // 2]
    # Find most common seniority in disclosed roles for the comparison anchor
    from collections import Counter
    sen_counts = Counter(s for _, _, s in disclosed if s)
    top_sen = sen_counts.most_common(1)[0][0] if sen_counts else ""
    market_median = None
    if comp_data and top_sen and top_sen in comp_data.get("by_seniority", {}):
        market_median = comp_data["by_seniority"][top_sen].get("median")
    return {
        "company_median": company_median,
        "disclosed_count": len(disclosed),
        "top_seniority": top_sen,
        "market_median": market_median,
    }


def _signal_counts(jobs):
    """Count signals across a company's jobs. Returns Counter keyed by lowercase signal_value."""
    from collections import Counter
    c = Counter()
    for j in jobs:
        for s in (j.get("signals") or []):
            v = (s.get("signal_value") or "").strip().lower()
            if v:
                c[v] += 1
    return c


def _tool_counts(jobs):
    """Count named tools across a company's jobs."""
    from collections import Counter
    c = Counter()
    for j in jobs:
        for t in (j.get("tools") or []):
            name = t.get("tool_name") if isinstance(t, dict) else str(t)
            if name:
                c[name] += 1
    return c


def _seniority_distribution(jobs):
    """Return ordered list of (seniority, count) tuples for non-empty seniority."""
    from collections import Counter
    sen_order = ["Entry", "Mid", "Senior", "Director", "Head of", "VP", "SVP"]
    c = Counter(j.get("seniority", "").strip() for j in jobs if j.get("seniority"))
    return [(s, c[s]) for s in sen_order if s in c] + [(s, n) for s, n in c.items() if s not in sen_order]


def _function_distribution(jobs):
    """Return list of (function_category, count) tuples."""
    from collections import Counter
    c = Counter(j.get("function_category", "").strip() for j in jobs if j.get("function_category"))
    return c.most_common()


def _signals_html(signal_counts):
    """Render the partner-program signals block, only including signals we have descriptions for."""
    if not signal_counts:
        return ""
    items = []
    # Prioritize the most informative signals first
    priority = [
        "build team", "first hire", "channel", "direct", "enterprise", "fortune 500", "smb",
        "mid market", "global", "north america", "emea", "apac", "latam",
        "reports cro", "reports ceo", "reports vp", "player coach",
        "seven figure", "enterprise deal", "long", "short",
        "equity", "uncapped", "ote mentioned",
        "solution selling", "value selling", "meddic", "miller heiman", "sandler", "bant",
        "growth hire", "turnaround", "immediate",
    ]
    seen = set()
    for key in priority:
        if key in signal_counts and key in SIGNAL_DESCRIPTIONS:
            items.append(f'<li><strong>{key.title()}:</strong> {SIGNAL_DESCRIPTIONS[key]}</li>')
            seen.add(key)
    # Add any remaining signals with descriptions that weren't in priority order
    for key in signal_counts:
        if key not in seen and key in SIGNAL_DESCRIPTIONS:
            items.append(f'<li><strong>{key.title()}:</strong> {SIGNAL_DESCRIPTIONS[key]}</li>')
    if not items:
        return ""
    return f'''
    <h2>Partner Program Signals</h2>
    <p>Structural signals extracted from this company's open partner job descriptions:</p>
    <ul class="company-signals-list">
        {"".join(items[:8])}
    </ul>'''


def _tools_html(tool_counts):
    """Render the tool stack block."""
    if not tool_counts:
        return ""
    top_tools = tool_counts.most_common(10)
    chips = "".join(f'<span class="tool-chip">{name} ({n})</span>' for name, n in top_tools)
    return f'''
    <h2>Tool Stack Mentioned in Postings</h2>
    <p>Named tools and platforms that appear in this company's partner manager job descriptions, weighted by mention count.</p>
    <div class="tool-chip-grid">{chips}</div>'''


def _comp_context_html(comp_ctx, comp_data, company_name):
    """Render compensation context block."""
    if not comp_ctx:
        return ""
    cm = comp_ctx["company_median"]
    market_m = comp_ctx.get("market_median")
    top_sen = comp_ctx.get("top_seniority")
    if market_m and top_sen:
        diff = cm - market_m
        pct = (diff / market_m) * 100
        direction = "above" if diff > 0 else "below"
        comparison = (
            f"This company's median disclosed compensation for {top_sen.lower()} partner roles is "
            f"${int(cm)//1000}K. The national median for {top_sen.lower()} partner manager roles in our dataset "
            f"is ${int(market_m)//1000}K, meaning {company_name} posts roughly "
            f"{abs(pct):.0f} percent {direction} the national median for this seniority."
        )
    else:
        comparison = (
            f"This company's median disclosed midpoint across {comp_ctx['disclosed_count']} "
            f"partner postings is ${int(cm)//1000}K."
        )
    return f'''
    <h2>Compensation Context</h2>
    <p>{comparison}</p>
    <p>For the full seniority-by-seniority comparison, see our <a href="/insights/state-of-partner-manager-compensation-2026/">state of partner manager compensation analysis</a>.</p>'''


def _seniority_html(seniority_dist, company_name):
    """Render seniority distribution block."""
    if not seniority_dist:
        return ""
    items = ", ".join(f"{s.lower()} ({n})" for s, n in seniority_dist)
    sen_levels = [s for s, _ in seniority_dist]
    if len(sen_levels) == 1:
        sentence = f"All open partner roles at {company_name} target the {sen_levels[0].lower()} level."
    else:
        sentence = f"Open partner roles at {company_name} span the {', '.join(s.lower() for s in sen_levels[:-1])} and {sen_levels[-1].lower()} bands ({items})."
    return f'''
    <h2>Seniority Mix</h2>
    <p>{sentence} The seniority breakdown shapes whether the company is building a partner org (more director-and-above hiring) or staffing it out (more mid-level hiring).</p>'''


def _locations_html(locations, jobs):
    """Render where-they-hire block with metro links where possible."""
    from collections import Counter
    counts = Counter((j.get("location") or "").strip() for j in jobs if j.get("location"))
    if not counts:
        return ""
    items = "".join(f'<li>{loc} ({n})</li>' for loc, n in counts.most_common(8))
    return f'''
    <h2>Where They Hire</h2>
    <p>Open partner postings appear in the following locations:</p>
    <ul class="company-loc-list">{items}</ul>'''


def _resource_links_html(signal_counts, tool_counts):
    """Render contextual cross-links to insights and glossary based on what signals appeared."""
    links = []
    if "channel" in signal_counts:
        links.append(('/glossary/channel-sales/', 'Channel sales defined'))
    if "build team" in signal_counts or "first hire" in signal_counts:
        links.append(('/careers/how-to-become-partner-manager/', 'How to become a partner manager'))
    if "ote mentioned" in signal_counts or "uncapped" in signal_counts:
        links.append(('/careers/negotiating-partner-manager-offer/', 'Negotiating a partner manager offer'))
    if any(k in signal_counts for k in ["reports cro", "reports ceo", "reports vp"]):
        links.append(('/insights/vp-of-partnerships-compensation/', 'VP of partnerships pay'))
    if tool_counts and any(name in tool_counts for name in ['Salesforce', 'HubSpot']):
        links.append(('/insights/prm-adoption-channel-tool-stack/', 'PRM adoption across 1,154 partner JDs'))
    # Always include
    links.append(('/insights/state-of-partner-manager-compensation-2026/', 'State of partner manager pay'))
    links.append(('/insights/salary-disclosure-in-partnerships-roles/', 'Why 1 in 3 partner jobs hide salary'))
    # Dedupe preserving order
    seen = set()
    out = []
    for url, label in links:
        if url not in seen:
            out.append((url, label))
            seen.add(url)
    items = "".join(f'<li><a href="{url}">{label}</a></li>' for url, label in out)
    return f'''
    <h2>Related Reading</h2>
    <p>Analyses on partnerchannels.com that are relevant given this company's hiring patterns:</p>
    <ul class="company-link-list">{items}</ul>'''


def build_company_page(company_name, jobs, all_companies, comp_data=None):
    """Generate a single enriched company detail page.

    Pulls a unique About excerpt from one of the company's JDs, computes
    compensation comparison vs the national median for the dominant
    seniority, surfaces partner-program signals + tool stack extracted
    from the JDs, and adds contextual cross-links to insights.
    """
    slug = slugify(company_name)
    canonical = f"/companies/{slug}/"
    n_jobs = len(jobs)
    locations = get_company_locations(jobs)
    location_str = ", ".join(locations[:5])
    if len(locations) > 5:
        location_str += f" and {len(locations) - 5} more"

    title = f"{company_name} {ROLE_NAME} Jobs"
    meta_title = f"{company_name} {ROLE_NAME} Jobs & Salary ({CURRENT_YEAR})"

    # Pull enrichment artifacts
    about = _extract_about_paragraph(jobs, company_name)
    comp_ctx = _compute_compensation_context(jobs, comp_data)
    signal_counts = _signal_counts(jobs)
    tool_counts = _tool_counts(jobs)
    sen_dist = _seniority_distribution(jobs)
    func_dist = _function_distribution(jobs)

    # Build the meta description from the richest available signal,
    # padded to land in the 150-158 char SEO sweet spot.
    if comp_ctx and comp_ctx.get("market_median"):
        cm_k = int(comp_ctx["company_median"]) // 1000
        mm_k = int(comp_ctx["market_median"]) // 1000
        top_sen = (comp_ctx.get("top_seniority") or "").lower()
        direction = "above" if cm_k > mm_k else "below" if cm_k < mm_k else "in line with"
        description = (
            f"{company_name} partnerships salary and open roles in 2026: "
            f"{n_jobs} positions, ${cm_k}K median {direction} the ${mm_k}K national {top_sen} median. Signals, tools, locations."
        )
    elif comp_ctx:
        cm_k = int(comp_ctx["company_median"]) // 1000
        description = (
            f"{company_name} has {n_jobs} open {ROLE_NAME.lower()} positions in 2026 with a ${cm_k}K median disclosed midpoint. "
            f"Roles, locations, signals, and tool stack."
        )
    else:
        description = (
            f"{company_name} has {n_jobs} open {ROLE_NAME.lower()} positions in 2026. "
            f"Browse open roles, locations, hiring signals, tool stack, and comparison to the national partner manager market."
        )
    if len(description) > 158:
        description = description[:155].rstrip() + "..."

    crumbs = [("Home", "/"), ("Companies", "/companies/"), (company_name, None)]

    # Job listings table
    rows = ""
    for job in sorted(jobs, key=lambda j: j.get("title", "")):
        # Sanitize em/en dashes in titles that come from upstream sources
        job_title = (job.get("title", "Untitled") or "").replace("—", ", ").replace("–", ", ")
        job_loc = (job.get("location", "Not specified") or "").replace("—", ", ").replace("–", ", ")
        salary = fmt_salary_range(job)
        seniority = job.get("seniority", "")
        source_url = job.get("source_url", "")

        title_cell = f'<a href="{source_url}" target="_blank" rel="noopener">{job_title}</a>' if source_url else job_title
        rows += f"""<tr>
    <td>{title_cell}</td>
    <td>{job_loc}</td>
    <td>{salary if salary else '<span class="text-muted">Not disclosed</span>'}</td>
    <td>{seniority if seniority else '<span class="text-muted">--</span>'}</td>
</tr>
"""

    # Related companies (5 others with most jobs)
    related_html = ""
    related = []
    for c_name, c_jobs in sorted(all_companies.items(), key=lambda x: -len(x[1])):
        if c_name != company_name and len(c_jobs) >= 2:
            related.append((c_name, len(c_jobs)))
        if len(related) >= 6:
            break
    if related:
        related_items = "".join(
            f'<li><a href="/companies/{slugify(r_name)}/">{r_name}</a> ({r_count} open positions)</li>\n'
            for r_name, r_count in related
        )
        related_html = f"""<section class="related-companies" style="margin-top: 2rem;">
    <h2>Other Companies Hiring Partner Managers</h2>
    <ul class="company-related-list">{related_items}</ul>
</section>"""

    about_html = ""
    if about:
        about_html = f'''
        <section class="company-overview">
            <h2>About {company_name}</h2>
            <p>{about}</p>
            <p class="company-source-note">Excerpted from one of {company_name}\'s open partner manager postings.</p>
        </section>'''
    else:
        about_html = f'''
        <section class="company-overview">
            <h2>About {company_name}</h2>
            <p>{company_name} runs an active partner manager and channel sales hiring pipeline. Use the open roles and signals below to evaluate fit for your background.</p>
        </section>'''

    signals_html = _signals_html(signal_counts)
    tools_html = _tools_html(tool_counts)
    seniority_html = _seniority_html(sen_dist, company_name)
    locations_section_html = _locations_html(locations, jobs)
    comp_ctx_html = _comp_context_html(comp_ctx, comp_data, company_name)
    resources_html = _resource_links_html(signal_counts, tool_counts)

    body = f"""<div class="container">
    <div class="page-header">
        {breadcrumb_html(crumbs)}
        <h1>{company_name} Partner Manager Jobs & Salary</h1>
        <p class="page-subtitle">{n_jobs} open {ROLE_NAME.lower()} {'position' if n_jobs == 1 else 'positions'} {('in ' + location_str) if location_str else ''}</p>
    </div>

    <div class="salary-content company-enriched">
        {about_html}
        {comp_ctx_html}
        {seniority_html}
        {signals_html}
        {tools_html}
        {locations_section_html}

        <section class="company-jobs">
            <h2>Open Partner Manager Roles at {company_name}</h2>
            <div class="table-wrapper" style="overflow-x: auto;">
                <table class="data-table" style="width: 100%; border-collapse: collapse;">
                    <thead>
                        <tr>
                            <th>Title</th>
                            <th>Location</th>
                            <th>Salary Range</th>
                            <th>Seniority</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows}
                    </tbody>
                </table>
            </div>
        </section>

        {resources_html}
        {related_html}
    </div>
</div>
"""
    body += newsletter_cta_html(f"Get partner manager job alerts in your inbox.")

    extra_head = get_breadcrumb_schema(crumbs)
    page = get_page_wrapper(
        title=meta_title, description=description,
        canonical_path=canonical, body_content=body,
        active_path="/companies/", extra_head=extra_head,
    )
    write_page(f"companies/{slug}/index.html", page)


def build_companies_index(all_companies):
    """Generate /companies/ index page listing all companies."""
    title = f"Companies Hiring {ROLE_NAME} Professionals ({CURRENT_YEAR})"
    description = (
        f"Browse companies actively hiring {ROLE_NAME.lower()} professionals. "
        f"Sorted by number of open positions with salary data and locations."
    )
    canonical = "/companies/"
    crumbs = [("Home", "/"), ("Companies", None)]

    # Sort by job count descending
    sorted_companies = sorted(all_companies.items(), key=lambda x: -len(x[1]))

    rows = ""
    for company_name, jobs in sorted_companies:
        if len(jobs) < 2:
            continue
        slug = slugify(company_name)
        n_jobs = len(jobs)
        locations = get_company_locations(jobs)
        loc_str = ", ".join(locations[:3])
        if len(locations) > 3:
            loc_str += f" +{len(locations) - 3} more"

        rows += f"""<tr>
    <td><a href="/companies/{slug}/">{company_name}</a></td>
    <td>{n_jobs}</td>
    <td>{loc_str if loc_str else 'Not specified'}</td>
</tr>
"""

    # Count companies with 2+ jobs
    qualified_count = sum(1 for jobs in all_companies.values() if len(jobs) >= 2)

    body = f"""<div class="container">
    <div class="page-header">
        {breadcrumb_html(crumbs)}
        <h1>Companies Hiring {ROLE_NAME} Professionals</h1>
        <p class="page-subtitle">{qualified_count} companies with multiple open positions</p>
    </div>

    <div class="salary-content">
        <div class="table-wrapper" style="overflow-x: auto;">
            <table class="data-table" style="width: 100%; border-collapse: collapse;">
                <thead>
                    <tr>
                        <th>Company</th>
                        <th>Open Positions</th>
                        <th>Locations</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </div>
    </div>
</div>
"""
    body += newsletter_cta_html(f"Get {ROLE_NAME.lower()} job alerts in your inbox.")

    extra_head = get_breadcrumb_schema(crumbs)
    page = get_page_wrapper(
        title=title, description=description,
        canonical_path=canonical, body_content=body,
        active_path="/companies/", extra_head=extra_head
    )
    write_page("companies/index.html", page)


def build_all_company_pages(project_dir):
    """Main entry point: build company index + detail pages."""
    jobs = load_jobs(project_dir)
    companies = get_company_data(jobs)
    comp_data = load_comp_analysis(project_dir)

    # Filter to companies with 2+ jobs
    qualified = {k: v for k, v in companies.items() if len(v) >= 2}

    if not qualified:
        print(f"  Skipping company pages (no companies with 2+ jobs)")
        return

    print(f"\n  Building enriched company pages ({len(qualified)} companies)...")
    build_companies_index(companies)
    print(f"  Built: companies/index.html")

    for company_name, jobs in sorted(qualified.items()):
        build_company_page(company_name, jobs, companies, comp_data=comp_data)

    print(f"  Built: {len(qualified)} enriched company detail pages")
