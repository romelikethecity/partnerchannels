# scripts/conferences_pages.py
# Conference index page generator for Partner Channels.

import os
import json

from nav_config import SITE_NAME, SITE_URL, CURRENT_YEAR
from templates import (get_page_wrapper, write_page, get_breadcrumb_schema,
                       breadcrumb_html, newsletter_cta_html)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PROJECT_DIR, "data")


def load_conferences():
    with open(os.path.join(DATA_DIR, "conferences.json"), "r") as f:
        return json.load(f)


def build_conferences_index():
    """Build /conferences/ index page."""
    conferences = load_conferences()
    role = "Partnerships & Channel"
    title = f"Best {role} Conferences in {CURRENT_YEAR}"
    description = (
        f"Top {len(conferences)} conferences for partnership and channel professionals in {CURRENT_YEAR}. "
        f"Events covering ecosystem strategy, PRM, co-selling, cloud marketplaces, and partner programs."
    )

    crumbs = [("Home", "/"), ("Conferences", None)]
    bc_schema = get_breadcrumb_schema([("Home", "/"), (f"{role} Conferences", f"{SITE_URL}/conferences/")])
    bc_html = breadcrumb_html(crumbs)

    cards_html = ""
    for conf in conferences:
        tags_html = "".join(
            f'<span class="conference-tag">{tag}</span>' for tag in conf["relevance_tags"][:4]
        )
        attendees = f"{conf['typical_attendees']:,}" if conf['typical_attendees'] else "TBA"
        cards_html += f'''<div class="conference-card">
    <div class="conference-card-header">
        <h3><a href="{conf['website_url']}" target="_blank" rel="noopener">{conf['name']}</a></h3>
        <span class="conference-organizer">by {conf['organizer']}</span>
    </div>
    <p class="conference-description">{conf['description']}</p>
    <div class="conference-meta">
        <span class="conference-location">{conf['location']}</span>
        <span class="conference-attendees">{attendees} typical attendees</span>
    </div>
    <div class="conference-tags">{tags_html}</div>
    <a href="{conf['website_url']}" target="_blank" rel="noopener" class="conference-link">Visit website</a>
</div>
'''

    body = f'''{bc_html}
<section class="page-header">
    <h1>{title}</h1>
    <p class="page-subtitle">The events where partnership professionals build relationships, learn ecosystem strategy, and shape the channel.</p>
</section>

<section class="content-section">
    <div class="content-body">
        <p>The partnerships and channel landscape is evolving faster than almost any other go-to-market function. Ecosystem-led growth has moved from buzzword to board-level strategy. Cloud marketplaces have changed how software gets bought and sold. Co-selling motions that barely existed five years ago now drive significant pipeline for SaaS companies of every size.</p>

        <p>Conferences are where you see these shifts play out in real time. They bring together the people building the playbooks, the vendors creating the tools, and the leaders deciding how partnerships fit into the broader revenue strategy. For a function that is still defining its own best practices, these in-person connections are essential.</p>

        <p>We curated this list of {len(conferences)} conferences based on their relevance to partnerships and channel professionals in {CURRENT_YEAR}. The list spans ecosystem-focused events, traditional channel conferences, and broader SaaS gatherings with strong partnership tracks.</p>

        <h2>Navigating the Partnership Conference Landscape</h2>
        <p>Partnership conferences fall into two broad categories. First, there are ecosystem and SaaS partnership events like Catalyst, Supernode, and PartnerStack Summit that focus on technology partnerships, co-selling, and ecosystem strategy. Second, there are traditional channel events like Channel Partners Conference and ChannelCon that serve the IT channel, MSPs, and distribution. Most partnership professionals will find value in both categories, depending on their business model.</p>

        <p>Cloud marketplace events are an emerging third category worth watching. As procurement increasingly shifts to AWS, Azure, and GCP marketplaces, understanding marketplace strategy has become a core partnership skill.</p>

        <h2>Top {role} Conferences in {CURRENT_YEAR}</h2>
    </div>
</section>

<section class="conferences-grid">
    {cards_html}
</section>

<section class="content-section">
    <div class="content-body">
        <h2>Making Conference Attendance Count</h2>
        <p>Partnership is a relationship-driven function, and conferences are relationship accelerators. Before you attend, identify the partners, vendors, and peers you want to connect with. Use the event app or attendee list to schedule meetings in advance. The professionals who get the most from these events treat them as strategic business development opportunities, not just learning experiences.</p>

        <p>If you can only attend one conference this year, choose the one where your most important current or potential partners will be. The hallway conversation with a partner who can change your business trajectory is worth more than any keynote.</p>
    </div>
</section>

{newsletter_cta_html("Get conference recaps and partnership insights delivered weekly.")}
'''

    page = get_page_wrapper(
        title=title,
        description=description,
        canonical_path="/conferences/",
        body_content=body,
        active_path="/conferences/",
        extra_head=bc_schema,
    )
    write_page("/conferences/index.html", page)
    print(f"  Built: /conferences/ ({len(conferences)} conferences)")
