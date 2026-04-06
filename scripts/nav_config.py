# scripts/nav_config.py
# Site constants, navigation, and footer configuration.
# Pure data — zero logic, zero imports.

SITE_NAME = "Partner Channels"
SITE_URL = "https://partnerchannels.com"
SITE_TAGLINE = "Career intelligence for partnerships and channel professionals"
COPYRIGHT_YEAR = "2026"
CURRENT_YEAR = 2026
CSS_VERSION = "1"

CTA_HREF = "/newsletter/"
CTA_LABEL = "Get the Weekly Brief"

SIGNUP_WORKER_URL = "https://newsletter-subscribe.rome-workers.workers.dev/subscribe"

GA_MEASUREMENT_ID = "G-R29ZKXX0NX"
GOOGLE_SITE_VERIFICATION = ""
GOOGLE_SITE_VERIFICATION_META = ""

NAV_ITEMS = [
    {
        "href": "/salary/",
        "label": "Salary Data",
        "children": [
            {"href": "/salary/", "label": "Salary Index"},
            {"href": "/salary/by-seniority/", "label": "By Seniority"},
            {"href": "/salary/by-location/", "label": "By Location"},
            {"href": "/salary/remote-vs-onsite/", "label": "Remote vs Onsite"},
            {"href": "/salary/calculator/", "label": "Salary Calculator"},
            {"href": "/salary/methodology/", "label": "Methodology"},
        ],
    },
    {
        "href": "/tools/",
        "label": "Tools",
        "children": [
            {"href": "/tools/", "label": "Tools Index"},
            {"href": "/tools/category/prm/", "label": "PRM Platforms"},
            {"href": "/tools/category/co-selling/", "label": "Co-Selling Tools"},
            {"href": "/tools/category/marketplace/", "label": "Marketplace Management"},
            {"href": "/tools/category/crm/", "label": "CRM Platforms"},
            {"href": "/tools/category/analytics/", "label": "Analytics"},
        ],
    },
    {
        "href": "/careers/",
        "label": "Careers",
        "children": [
            {"href": "/careers/", "label": "Career Guides"},
            {"href": "/careers/how-to-become-partner-manager/", "label": "How to Become a Partner Manager"},
            {"href": "/careers/job-growth/", "label": "Job Market Growth"},
        ],
    },
    {"href": "/glossary/", "label": "Glossary"},
    {
        "href": "/insights/",
        "label": "Resources",
        "children": [
            {"href": "/insights/", "label": "Insights"},
            {"href": "/blog/", "label": "Blog"},
            {"href": "/jobs/", "label": "Job Board"},
        ],
    },
]

FOOTER_COLUMNS = {
    "Salary Data": [
        {"href": "/salary/", "label": "Salary Index"},
        {"href": "/salary/by-seniority/", "label": "By Seniority"},
        {"href": "/salary/by-location/", "label": "By Location"},
        {"href": "/salary/remote-vs-onsite/", "label": "Remote vs Onsite"},
        {"href": "/salary/calculator/", "label": "Salary Calculator"},
        {"href": "/salary/methodology/", "label": "Methodology"},
    ],
    "Tools": [
        {"href": "/tools/", "label": "All Tools"},
        {"href": "/tools/category/prm/", "label": "PRM Platforms"},
        {"href": "/tools/category/co-selling/", "label": "Co-Selling Tools"},
        {"href": "/tools/category/marketplace/", "label": "Marketplace"},
        {"href": "/tools/category/crm/", "label": "CRM Platforms"},
        {"href": "/tools/category/analytics/", "label": "Analytics"},
    ],
    "Resources": [
        {"href": "/careers/", "label": "Career Guides"},
        {"href": "/glossary/", "label": "Glossary"},
        {"href": "/jobs/", "label": "Job Board"},
        {"href": "/blog/", "label": "Blog"},
        {"href": "/insights/", "label": "Insights"},
        {"href": "/newsletter/", "label": "Newsletter"},
        {"href": "/about/", "label": "About"},
    ],
    "Site": [
        {"href": "/privacy/", "label": "Privacy Policy"},
        {"href": "/terms/", "label": "Terms of Service"},
    ],
    "Partner Ecosystem": [
        {"href": "https://therevopsreport.com", "label": "RevOps Report", "external": True},
        {"href": "https://gtmepulse.com", "label": "GTME Pulse", "external": True},
        {"href": "https://b2bsalestools.com", "label": "B2B Sales Tools", "external": True},
    ],
}
