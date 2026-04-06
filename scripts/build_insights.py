# scripts/build_insights.py
# Insights hub page and /blog/ redirect.
# Called by build.py. Uses templates.py for HTML shell.

import os

from nav_config import *
from templates import (get_page_wrapper, write_page, get_breadcrumb_schema,
                       breadcrumb_html, newsletter_cta_html)


# ---------------------------------------------------------------------------
# Insights Hub
# ---------------------------------------------------------------------------

def build_insights_hub():
    title = "Partner & Channel Sales Insights"
    description = (
        "Analysis and trends for partnerships and channel sales professionals."
        " Data-backed insights on partner programs, ecosystem strategy, and the channel market."
    )

    crumbs = [("Home", "/"), ("Insights", None)]
    bc_html = breadcrumb_html(crumbs)

    body = f'''{bc_html}
<section class="page-header">
    <h1>Partner &amp; Channel Sales Insights</h1>
    <p class="page-header-subtitle">Analysis and trends shaping the partnerships landscape.</p>
</section>
<div class="container">

    <p>Insights is where we publish analysis on the partnerships and channel sales market. Every piece is grounded in data from job postings, salary benchmarks, tool adoption patterns, and practitioner interviews.</p>

    <p>No thought leadership for the sake of thought leadership. If we publish something here, it is because the data says something worth paying attention to.</p>

    <h2>What We Cover</h2>

    <ul>
        <li><strong>Compensation trends:</strong> How partner manager salaries are shifting by role, seniority, location, and company stage</li>
        <li><strong>Tool adoption:</strong> Which PRM, co-selling, and marketplace platforms are gaining or losing traction in the market</li>
        <li><strong>Hiring patterns:</strong> Where companies are investing in their partner teams and what that signals about market direction</li>
        <li><strong>Program strategy:</strong> What separates partner programs that drive real revenue from those that exist on paper</li>
        <li><strong>Ecosystem shifts:</strong> How cloud marketplaces, co-selling platforms, and ecosystem-led growth are changing the rules</li>
    </ul>

    <h2>Coming Soon</h2>

    <p>We are building out the insights section now. First articles will cover:</p>

    <ul>
        <li>The state of partner manager compensation in 2026</li>
        <li>PRM adoption rates by company size and industry</li>
        <li>Cloud marketplace co-sell: what the data shows about which vendors are winning</li>
        <li>Partner-sourced vs. partner-influenced revenue: why the distinction matters for your career</li>
    </ul>

    <p>Want to know when new insights drop? Subscribe to <a href="/newsletter/">The Weekly Brief</a> and we will send them straight to your inbox.</p>

    <h2>Explore Other Sections</h2>

    <div class="preview-grid">
        <a href="/salary/" class="preview-card">
            <h3>Salary Data</h3>
            <p>Compensation benchmarks by seniority, location, and company stage.</p>
            <span class="preview-link">Browse salary data &rarr;</span>
        </a>
        <a href="/tools/" class="preview-card">
            <h3>Tool Reviews</h3>
            <p>PRM platforms, co-selling tools, and marketplace management software.</p>
            <span class="preview-link">Browse tools &rarr;</span>
        </a>
        <a href="/careers/" class="preview-card">
            <h3>Career Guides</h3>
            <p>Paths into partnerships, job market data, and advancement strategies.</p>
            <span class="preview-link">Browse guides &rarr;</span>
        </a>
        <a href="/glossary/" class="preview-card">
            <h3>Glossary</h3>
            <p>Clear definitions for partnerships and channel sales terminology.</p>
            <span class="preview-link">Browse glossary &rarr;</span>
        </a>
    </div>

</div>
'''
    body += newsletter_cta_html("Analysis for partnership professionals, every Monday.")

    page = get_page_wrapper(
        title=title,
        description=description,
        canonical_path="/insights/",
        body_content=body,
        active_path="/insights/",
        extra_head=get_breadcrumb_schema(crumbs),
        body_class="page-inner",
    )
    write_page("insights/index.html", page)
    print(f"  Built: insights/index.html")


# ---------------------------------------------------------------------------
# Blog redirect -> /insights/
# ---------------------------------------------------------------------------

def build_blog_redirect():
    """Generate /blog/ as a meta-refresh redirect to /insights/."""
    html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="0;url=/insights/">
    <link rel="canonical" href="https://partnerchannels.com/insights/">
    <title>Redirecting to Insights</title>
</head>
<body>
    <p>Redirecting to <a href="/insights/">Insights</a>.</p>
</body>
</html>'''

    out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output")
    blog_dir = os.path.join(out_dir, "blog")
    os.makedirs(blog_dir, exist_ok=True)
    with open(os.path.join(blog_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    # Do NOT add to ALL_PAGES (redirect should not be in sitemap)
    print(f"  Built: blog/index.html (redirect to /insights/)")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def build_all_insights_pages():
    print("\n  Building insights pages...")
    build_insights_hub()
    build_blog_redirect()
