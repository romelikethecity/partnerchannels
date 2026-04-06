# scripts/build.py
# Main build pipeline: generates all pages, sitemap, robots, CNAME.
# Data + page generators live here. HTML shell lives in templates.py.
# Site constants live in nav_config.py.

import os
import sys
import re
import shutil
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nav_config import *
import templates
from templates import (get_page_wrapper, write_page, get_homepage_schema,
                       get_breadcrumb_schema, get_faq_schema,
                       get_article_schema,
                       breadcrumb_html, newsletter_cta_html, faq_html, ALL_PAGES)
from build_salary import build_all_salary_pages
from build_tools import build_all_tools_pages
from build_glossary import build_all_glossary_pages

# OG image generation state
SKIP_OG = "--skip-og" in sys.argv


# ---------------------------------------------------------------------------
# Path constants
# ---------------------------------------------------------------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(PROJECT_DIR, "output")
ASSETS_DIR = os.path.join(PROJECT_DIR, "assets")
BUILD_DATE = datetime.now().strftime("%Y-%m-%d")

# Wire up templates module
templates.OUTPUT_DIR = OUTPUT_DIR
templates.SKIP_OG = SKIP_OG


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def pad_description(desc, target_min=150, target_max=158):
    """Ensure description is within 150-158 chars by appending filler."""
    suffixes = [" Updated weekly.", " Independent.", " Free.", " No ads."]
    used = set()
    for suffix in suffixes:
        if target_min <= len(desc) <= target_max:
            return desc
        if suffix in used:
            continue
        new = desc + suffix
        if len(new) <= target_max:
            desc = new
            used.add(suffix)
    if len(desc) > target_max:
        desc = desc[:target_max - 1].rstrip() + "."
    return desc


# ---------------------------------------------------------------------------
# Page generators: Homepage
# ---------------------------------------------------------------------------

def build_homepage():
    """Generate the homepage with Organization+WebSite schema."""
    title = "Partner & Channel Sales Career Intelligence"
    description = (
        "Salary benchmarks, tool reviews, and career data for partnerships and channel professionals."
        " PRM platforms, co-selling tools, and ecosystem strategy. Updated weekly."
    )

    body = '''<section class="hero">
    <div class="hero-inner">
        <h1>Partnerships &amp; Channel, Finally Mapped Out</h1>
        <p class="hero-subtitle">Salary data, PRM reviews, career paths, and job listings for the professionals who build partner ecosystems.</p>
        <div class="stat-grid">
            <div class="stat-block">
                <span class="stat-value">12,000+</span>
                <span class="stat-label">Roles Tracked</span>
            </div>
            <div class="stat-block">
                <span class="stat-value">$85K&#8209;$300K+</span>
                <span class="stat-label">Salary Range</span>
            </div>
            <div class="stat-block">
                <span class="stat-value">45%</span>
                <span class="stat-label">YoY Growth</span>
            </div>
        </div>
        <form class="hero-signup" onsubmit="return false;">
            <input type="email" placeholder="Your email" aria-label="Email address" required>
            <button type="submit" class="btn btn--primary">Get the Weekly Brief</button>
        </form>
        <p class="hero-signup-note">Free weekly newsletter. Partner trends, salary data, tool intel.</p>
    </div>
</section>

<section class="logo-bar">
    <p class="logo-bar-label">Tracking partner programs at companies like</p>
    <div class="logo-bar-row">
        <span class="logo-name">PartnerStack</span>
        <span class="logo-name">Crossbeam</span>
        <span class="logo-name">Reveal</span>
        <span class="logo-name">Salesforce</span>
        <span class="logo-name">HubSpot</span>
        <span class="logo-name">AWS</span>
        <span class="logo-name">Microsoft</span>
        <span class="logo-name">Impartner</span>
        <span class="logo-name">Impact.com</span>
        <span class="logo-name">Tackle.io</span>
    </div>
</section>

<section class="section-previews">
    <h2 class="section-previews-heading">Explore Partner Channel Intelligence</h2>
    <div class="preview-grid">
        <a href="/salary/" class="preview-card">
            <div class="preview-icon"><span class="preview-emoji">&#128176;</span></div>
            <h3>Salary Data</h3>
            <p>Breakdowns by seniority, location, and company stage. Partner Manager to VP of Partnerships compensation.</p>
            <span class="preview-link">Browse salary data &rarr;</span>
        </a>
        <a href="/tools/" class="preview-card">
            <div class="preview-icon"><span class="preview-emoji">&#128295;</span></div>
            <h3>Tool Reviews</h3>
            <p>PRM platforms, co-selling tools, and marketplace management software. Honest reviews from practitioners.</p>
            <span class="preview-link">Browse tools &rarr;</span>
        </a>
        <a href="/careers/" class="preview-card">
            <div class="preview-icon"><span class="preview-emoji">&#128200;</span></div>
            <h3>Career Guides</h3>
            <p>How to break into partnerships, level up from partner manager to channel chief, and negotiate comp.</p>
            <span class="preview-link">Browse guides &rarr;</span>
        </a>
        <a href="/glossary/" class="preview-card">
            <div class="preview-icon"><span class="preview-emoji">&#128218;</span></div>
            <h3>Glossary</h3>
            <p>Clear definitions for partnerships terms. Co-sell, near-bound, ecosystem-led growth, and more.</p>
            <span class="preview-link">Browse glossary &rarr;</span>
        </a>
        <a href="/jobs/" class="preview-card">
            <div class="preview-icon"><span class="preview-emoji">&#128188;</span></div>
            <h3>Job Board</h3>
            <p>Curated partner and channel roles from top SaaS companies. Updated twice a week.</p>
            <span class="preview-link">View all jobs &rarr;</span>
        </a>
        <a href="/newsletter/" class="preview-card">
            <div class="preview-icon"><span class="preview-emoji">&#128232;</span></div>
            <h3>Weekly Brief</h3>
            <p>Partner program trends, salary shifts, and hiring signals delivered every Monday.</p>
            <span class="preview-link">Get the weekly brief &rarr;</span>
        </a>
    </div>
</section>

'''
    body += newsletter_cta_html()

    page = get_page_wrapper(
        title=title,
        description=description,
        canonical_path="/",
        body_content=body,
        active_path="/",
        extra_head=get_homepage_schema(),
        body_class="page-home",
    )
    write_page("index.html", page)
    print(f"  Built: index.html")


# ---------------------------------------------------------------------------
# About page
# ---------------------------------------------------------------------------

def build_about_page():
    """Generate the about page."""
    title = "About Partner Channels: Independent Data"
    description = (
        "Partner Channels offers vendor-neutral salary benchmarks, PRM reviews,"
        " and career guides for partnerships and channel sales professionals."
    )
    description = pad_description(description)

    crumbs = [("Home", "/"), ("About", None)]
    bc_html = breadcrumb_html(crumbs)

    body = f'''{bc_html}
<section class="page-header">
    <h1>About Partner Channels</h1>
</section>
<div class="container">
    <p>Partner Channels is an independent resource for partnerships and channel sales professionals. We track salary data, review PRM platforms and co-selling tools, and analyze the job market so you can make informed career decisions.</p>
    <p>Every data point comes from real job postings and practitioner surveys. No vendor affiliations drive our rankings. No pay-to-play reviews.</p>
    <h2>What you will find here</h2>
    <ul>
        <li><strong><a href="/salary/">Salary benchmarks</a></strong> broken down by seniority, location, and company stage</li>
        <li><strong><a href="/tools/">Tool reviews</a></strong> of PRM platforms, co-selling tools, and marketplace management software</li>
        <li><strong><a href="/careers/">Career guides</a></strong> for breaking into and advancing in partnerships</li>
        <li><strong><a href="/glossary/">Glossary</a></strong> of partnerships and channel sales terminology</li>
    </ul>
    <p>Built by <strong>Rome Thorndike</strong>.</p>
</div>
'''

    page = get_page_wrapper(
        title=title,
        description=description,
        canonical_path="/about/",
        body_content=body,
        active_path="/about/",
        extra_head=get_breadcrumb_schema(crumbs),
        body_class="page-inner",
    )
    write_page("about/index.html", page)
    print(f"  Built: about/index.html")


# ---------------------------------------------------------------------------
# Core pages (newsletter, privacy, terms, 404)
# ---------------------------------------------------------------------------

def build_newsletter_page():
    title = "The Weekly Brief: Partner Channel Newsletter"
    description = (
        "Get weekly partnerships salary data, PRM tool intel, and channel job market analysis."
        " Free newsletter for partner and channel professionals. Every Monday."
    )
    crumbs = [("Home", "/"), ("Newsletter", None)]
    bc_html = breadcrumb_html(crumbs)

    body = f'''{bc_html}
<div class="newsletter-page">
    <section class="page-header">
        <h1>The Weekly Brief: Partner Channel News</h1>
    </section>
    <p class="lead">Every Monday: salary shifts, PRM tool intel, hiring trends, and job market data for partnerships and channel professionals.</p>
    <form class="hero-signup" onsubmit="return false;">
        <input type="email" placeholder="Your email" aria-label="Email address" required>
        <button type="submit" class="btn btn--primary">Get the Weekly Brief</button>
    </form>
    <ul class="newsletter-features">
        <li><strong>Salary movements:</strong> week-over-week changes in partner manager compensation across seniority levels and locations</li>
        <li><strong>Tool trends:</strong> which PRM and co-selling platforms are showing up in job postings and partner programs</li>
        <li><strong>Hiring signals:</strong> which companies are scaling their partner teams and what that tells us about the market</li>
        <li><strong>Career intel:</strong> job market data, interview insights, and skill demand shifts for channel professionals</li>
    </ul>
    <p style="color: var(--pc-text-secondary);">Free. No spam. Unsubscribe anytime.</p>
</div>
'''
    page = get_page_wrapper(
        title=title, description=description, canonical_path="/newsletter/",
        body_content=body, active_path="/newsletter/",
        extra_head=get_breadcrumb_schema(crumbs), body_class="page-inner",
    )
    write_page("newsletter/index.html", page)
    print(f"  Built: newsletter/index.html")


def build_privacy_page():
    title = "Privacy Policy for Partner Channels Website"
    description = (
        "Partner Channels privacy policy: how we collect, use, and protect your data."
        " We collect minimal information, never sell it, and respect your inbox."
    )
    description = pad_description(description)
    crumbs = [("Home", "/"), ("Privacy Policy", None)]
    bc_html = breadcrumb_html(crumbs)

    body = f'''{bc_html}
<section class="page-header">
    <h1>Privacy Policy for Partner Channels</h1>
</section>
<div class="legal-content">
    <p>Last updated: April 3, 2026</p>
    <h2>What We Collect</h2>
    <p>When you subscribe to our newsletter, we collect your email address. We do not track you across the web, sell your data, or build advertising profiles.</p>
    <h2>How We Use Your Email</h2>
    <p>Your email address is used to send you The Weekly Brief newsletter. We may also send occasional product updates. Every email includes an unsubscribe link that works immediately.</p>
    <h2>Email Service Provider</h2>
    <p>We use <a href="https://resend.com">Resend</a> to manage our email list and send newsletters. Your email address is stored in Resend's infrastructure.</p>
    <h2>Analytics</h2>
    <p>We may use privacy-respecting analytics to understand how visitors use the site. We do not use this data to identify individuals or build user profiles.</p>
    <h2>Cookies</h2>
    <p>This site uses minimal cookies for analytics purposes only. No advertising cookies. No tracking pixels from third parties.</p>
    <h2>Your Rights</h2>
    <p>You can unsubscribe from our newsletter at any time using the link in any email. To request deletion of your data, email <a href="mailto:rome@getprovyx.com">rome@getprovyx.com</a>.</p>
    <h2>Contact</h2>
    <p>Questions about this privacy policy? Email <a href="mailto:rome@getprovyx.com">rome@getprovyx.com</a>.</p>
</div>
'''
    page = get_page_wrapper(
        title=title, description=description, canonical_path="/privacy/",
        body_content=body, active_path="/privacy/",
        extra_head=get_breadcrumb_schema(crumbs), body_class="page-inner",
    )
    write_page("privacy/index.html", page)
    print(f"  Built: privacy/index.html")


def build_terms_page():
    title = "Terms of Service for Partner Channels Website"
    description = (
        "Partner Channels terms of service: usage rules, disclaimers, and limitations."
        " Salary data is for informational purposes only. Not financial advice."
    )
    description = pad_description(description)
    crumbs = [("Home", "/"), ("Terms of Service", None)]
    bc_html = breadcrumb_html(crumbs)

    body = f'''{bc_html}
<section class="page-header">
    <h1>Terms of Service for Partner Channels</h1>
</section>
<div class="legal-content">
    <p>Last updated: April 3, 2026</p>
    <h2>Use of Content</h2>
    <p>All content on partnerchannels.com is provided for informational purposes only. Salary data, tool reviews, and career guides reflect our best analysis but are not guarantees of accuracy.</p>
    <h2>No Professional Advice</h2>
    <p>Nothing on this site constitutes financial, legal, or career advice. Consult qualified professionals for decisions affecting your career or compensation.</p>
    <h2>Intellectual Property</h2>
    <p>All content, design, and code on this site are the property of Partner Channels. You may not reproduce, distribute, or create derivative works without written permission.</p>
    <h2>Affiliate Links</h2>
    <p>Some links on this site are affiliate links. We may earn a commission if you purchase through these links. This does not affect our editorial independence or review scores.</p>
    <h2>Limitation of Liability</h2>
    <p>Partner Channels is not liable for any damages arising from your use of this site or reliance on its content. Use at your own risk.</p>
    <h2>Changes</h2>
    <p>We may update these terms at any time. Continued use of the site constitutes acceptance of updated terms.</p>
    <h2>Contact</h2>
    <p>Questions? Email <a href="mailto:rome@getprovyx.com">rome@getprovyx.com</a>.</p>
</div>
'''
    page = get_page_wrapper(
        title=title, description=description, canonical_path="/terms/",
        body_content=body, active_path="/terms/",
        extra_head=get_breadcrumb_schema(crumbs), body_class="page-inner",
    )
    write_page("terms/index.html", page)
    print(f"  Built: terms/index.html")


def build_404_page():
    title = "Page Not Found"
    description = "The page you are looking for does not exist on Partner Channels."

    body = '''<div class="error-page">
    <div class="error-code">404</div>
    <h1>Page Not Found</h1>
    <p>The page you are looking for does not exist or has been moved.</p>
    <a href="/" class="btn btn--primary">Back to Homepage</a>
</div>
'''
    page = get_page_wrapper(
        title=title, description=description, canonical_path="/404.html",
        body_content=body, body_class="page-error",
    )
    write_page("404.html", page)
    print(f"  Built: 404.html")


# ---------------------------------------------------------------------------
# Sitemap + Robots
# ---------------------------------------------------------------------------

def build_sitemap():
    urls = ""
    for page_path in ALL_PAGES:
        clean = page_path.replace("index.html", "")
        if not clean.startswith("/"):
            clean = "/" + clean
        if not clean.endswith("/"):
            clean += "/"
        if clean == "//":
            clean = "/"
        urls += f"  <url>\n    <loc>{SITE_URL}{clean}</loc>\n    <lastmod>{BUILD_DATE}</lastmod>\n  </url>\n"

    sitemap = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n'
    with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap)
    print(f"  Built: sitemap.xml ({len(ALL_PAGES)} URLs)")


def build_robots():
    content = f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n"
    with open(os.path.join(OUTPUT_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Built: robots.txt")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print(f"=== Partner Channels Build ({BUILD_DATE}) ===\n")

    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)
    print("  Cleaned output/")

    shutil.copytree(ASSETS_DIR, os.path.join(OUTPUT_DIR, "assets"))
    print("  Copied assets/")

    print("\n  Building core pages...")
    build_homepage()
    build_about_page()
    build_newsletter_page()
    build_privacy_page()
    build_terms_page()
    build_404_page()

    build_all_salary_pages()
    build_all_tools_pages()
    build_all_glossary_pages()

    print("\n  Building meta files...")
    build_sitemap()
    build_robots()

    with open(os.path.join(OUTPUT_DIR, "CNAME"), "w", encoding="utf-8") as f:
        f.write("partnerchannels.com\n")
    print("  Built: CNAME")

    print(f"\n=== Build complete: {len(ALL_PAGES)} pages ===")
    print(f"  Output: {OUTPUT_DIR}")
    print(f"  Preview: cd output && python3 -m http.server 8090")


if __name__ == "__main__":
    main()
