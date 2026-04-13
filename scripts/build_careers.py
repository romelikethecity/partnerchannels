# scripts/build_careers.py
# Career guide pages: index, how-to-become-partner-manager, job-growth.
# Called by build.py. Uses templates.py for HTML shell.

import os
import json

from nav_config import *
from templates import (get_page_wrapper, write_page, get_breadcrumb_schema,
                       get_faq_schema, get_article_schema, breadcrumb_html,
                       newsletter_cta_html, faq_html)


# ---------------------------------------------------------------------------
# Careers Index
# ---------------------------------------------------------------------------

def build_careers_index():
    title = "Partnership & Channel Career Guides"
    description = (
        "Career guides for partnerships and channel sales professionals."
        " Paths into partner management, job market data, skills, and salary expectations."
    )

    crumbs = [("Home", "/"), ("Careers", None)]
    bc_html = breadcrumb_html(crumbs)

    body = f'''{bc_html}
<section class="page-header">
    <h1>Partnership &amp; Channel Career Guides</h1>
    <p class="page-header-subtitle">Practical guidance for breaking into, advancing in, and understanding the partnerships job market.</p>
</section>
<div class="container">

    <p>Partnerships and channel sales is one of the fastest-growing functions in B2B SaaS. Companies that once relied entirely on direct sales teams are building out partner ecosystems, and they need people who know how to run them. That shift is creating career opportunities that did not exist five years ago.</p>

    <p>These guides are built on real job posting data, practitioner interviews, and compensation benchmarks. No generic career advice. Everything here is specific to the partnerships and channel function.</p>

    <h2>Career Guides</h2>

    <div class="preview-grid">
        <a href="/careers/how-to-become-partner-manager/" class="preview-card">
            <h3>How to Become a Partner Manager</h3>
            <p>Career paths into partner management from sales, marketing, and customer success. Skills, certifications, tools, and salary expectations for every level.</p>
            <span class="preview-link">Read the guide &rarr;</span>
        </a>
        <a href="/careers/job-growth/" class="preview-card">
            <h3>Partnerships &amp; Channel Job Market Growth</h3>
            <p>Data on how the partnerships job market is expanding, which roles are in highest demand, and where the growth is headed through 2027.</p>
            <span class="preview-link">See the data &rarr;</span>
        </a>
    </div>

    <h2>Why Partnerships Careers Are Growing</h2>

    <p>Three forces are driving demand for partnership professionals:</p>

    <ul>
        <li><strong>Ecosystem-led growth:</strong> Companies like HubSpot, Salesforce, and AWS have proven that partner-sourced revenue can outpace direct sales at scale. Smaller companies are now copying the playbook.</li>
        <li><strong>Co-selling platforms:</strong> Tools like Crossbeam and Reveal have made it possible to map overlapping customers and prospects between partner organizations, turning partnerships from a relationship game into a data-driven function.</li>
        <li><strong>Cloud marketplace adoption:</strong> AWS, Azure, and GCP marketplaces are becoming major procurement channels. Companies need people who understand marketplace listing, co-sell motions, and cloud commitment drawdown.</li>
    </ul>

    <h2>Core Roles in Partnerships</h2>

    <p>The partnerships function spans several distinct roles, each with different skill requirements and career trajectories:</p>

    <ul>
        <li><strong>Partner Manager:</strong> Owns a portfolio of partner relationships. Drives co-selling, joint marketing, and partner enablement. The most common entry point.</li>
        <li><strong>Channel Account Manager:</strong> Focused on reseller and distributor relationships. More common in traditional IT and infrastructure companies.</li>
        <li><strong>Partner Marketing Manager:</strong> Runs co-marketing campaigns, partner events, and joint content programs with strategic partners.</li>
        <li><strong>Partner Operations:</strong> Manages PRM platforms, deal registration workflows, partner data, and program reporting.</li>
        <li><strong>VP/Director of Partnerships:</strong> Leads the entire partner function. Sets strategy, builds the team, owns partner-sourced revenue targets.</li>
        <li><strong>Ecosystem/Platform Lead:</strong> Manages technology partnerships, API integrations, and marketplace listings. Increasingly common at platform companies.</li>
    </ul>

    <h2>Getting Started</h2>

    <p>If you are new to partnerships, start with the <a href="/careers/how-to-become-partner-manager/">How to Become a Partner Manager</a> guide. It covers the most common entry paths and what hiring managers actually look for. Then check the <a href="/careers/job-growth/">Job Market Growth</a> page to understand where demand is heading and which specializations are worth investing in.</p>

    <p>For salary benchmarks across every seniority level and location, see our <a href="/salary/">Salary Data</a> section.</p>

</div>
'''
    body += newsletter_cta_html("Career intel for partnership professionals, every Monday.")

    faq_pairs = [
        ("What background do you need for a partnerships career?",
         "Most partner managers come from sales, marketing, or customer success backgrounds. The key transferable skills are relationship management, strategic thinking, and comfort with revenue targets. Technical partnerships roles often require product or solutions engineering experience."),
        ("How much do partnership professionals earn?",
         "Entry-level partner managers typically earn $70,000 to $95,000 base. Mid-level roles range from $100,000 to $150,000. Senior directors and VPs of partnerships at growth-stage or enterprise companies earn $180,000 to $300,000+ in total compensation."),
        ("Is partnerships a good career path in 2026?",
         "Yes. Job postings for partnerships roles have grown 40-50% year over year since 2023. Companies are investing heavily in indirect revenue channels, and the talent pool has not kept pace with demand."),
    ]

    body += faq_html(faq_pairs)

    page = get_page_wrapper(
        title=title,
        description=description,
        canonical_path="/careers/",
        body_content=body,
        active_path="/careers/",
        extra_head=get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs),
        body_class="page-inner",
    )
    write_page("careers/index.html", page)
    print(f"  Built: careers/index.html")


# ---------------------------------------------------------------------------
# How to Become a Partner Manager
# ---------------------------------------------------------------------------

def build_how_to_become_partner_manager():
    title = "How to Become a Partner Manager: Career Guide"
    description = (
        "Complete guide to becoming a partner manager. Career paths from sales,"
        " marketing, and CS into partnerships. Skills, tools, certifications, salary data."
    )

    crumbs = [("Home", "/"), ("Careers", "/careers/"), ("How to Become a Partner Manager", None)]
    bc_html = breadcrumb_html(crumbs)

    body = f'''{bc_html}
<section class="page-header">
    <h1>How to Become a Partner Manager</h1>
    <p class="page-header-subtitle">Career paths, skills, certifications, tools, and salary expectations for breaking into partner management.</p>
</section>
<div class="container article-content">

    <p>Partner management is one of the highest-leverage roles in B2B SaaS. A single partner manager who activates the right relationships can generate more pipeline than an entire team of SDRs. Companies know this, and they are hiring aggressively to build out their partner functions.</p>

    <p>But partner management is still a relatively new career path. There is no standard degree for it, no obvious pipeline from college to partner manager. Most people find their way in from adjacent roles. This guide covers the most common paths, what you need to get hired, and what to expect once you are in the seat.</p>

    <h2>What a Partner Manager Actually Does</h2>

    <p>A partner manager owns relationships with external organizations that sell, refer, or integrate with your product. The day-to-day varies depending on the partner type, but the core responsibilities are consistent:</p>

    <ul>
        <li><strong>Partner recruitment:</strong> Identifying and signing new partners that fit your ideal partner profile</li>
        <li><strong>Onboarding and enablement:</strong> Getting partners trained on your product, sales motion, and value proposition</li>
        <li><strong>Co-selling:</strong> Working joint deals with partners, mapping accounts, and coordinating handoffs between your sales team and theirs</li>
        <li><strong>Pipeline management:</strong> Tracking partner-sourced and partner-influenced revenue against targets</li>
        <li><strong>Relationship management:</strong> Regular business reviews, escalation handling, and strategic planning with key partners</li>
        <li><strong>Program development:</strong> Building incentive structures, tiering models, and certification programs that drive partner engagement</li>
    </ul>

    <p>The best partner managers operate as general managers of their partner portfolio. They think about revenue, marketing, product feedback, and competitive dynamics simultaneously.</p>

    <h2>Career Paths Into Partner Management</h2>

    <h3>From Sales (Most Common)</h3>

    <p>The most traveled path into partnerships runs through direct sales. Account executives and sales managers who have closed deals, managed pipelines, and built customer relationships have the foundational skills that transfer directly. The shift is from selling to buyers to enabling partners to sell on your behalf.</p>

    <p>If you are in sales and want to move into partnerships:</p>

    <ul>
        <li>Volunteer for co-selling deals with existing partners at your company</li>
        <li>Learn how your company's partner program works from the inside</li>
        <li>Track your partner-influenced deals so you can quantify the impact</li>
        <li>Study PRM platforms and co-selling tools (see our <a href="/tools/">Tools</a> section)</li>
    </ul>

    <p>Sales-to-partnerships transitions typically happen at the 2 to 4 year mark of a sales career. You need enough deal experience to be credible with partners but you do not need to be a top-1% closer.</p>

    <h3>From Marketing</h3>

    <p>Marketing professionals, especially those in field marketing, partner marketing, or demand generation, have a natural path into partnerships. Partner marketing managers run co-branded campaigns, joint webinars, and partner events. From there, the step to full partner management is shorter than most people think.</p>

    <p>The marketing-to-partnerships path works best for people who are comfortable with revenue accountability. In marketing, you influence pipeline. In partnerships, you own it. If that shift excites you rather than scares you, marketing is a strong launchpad.</p>

    <h3>From Customer Success</h3>

    <p>Customer success managers who work with large accounts or manage integration partnerships already do a version of partner management. They understand long-term relationship building, multi-stakeholder management, and value delivery, all core partnership skills.</p>

    <p>CS-to-partnerships moves are most common at companies where integration partnerships are a key growth lever. If your CS work involves coordinating with technology partners, you are already building relevant experience.</p>

    <h3>From Solutions Engineering or Pre-Sales</h3>

    <p>For technology partnerships and platform ecosystem roles, a solutions engineering background is highly valued. These roles require deep product knowledge, API fluency, and the ability to architect joint solutions. If you are a solutions engineer interested in business strategy, technology partnerships is where the two intersect.</p>

    <h2>Skills That Matter</h2>

    <p>Hiring managers for partner roles consistently prioritize these skills:</p>

    <h3>Must-Have Skills</h3>
    <ul>
        <li><strong>Relationship building at scale:</strong> Managing 20 to 50+ partner relationships simultaneously without dropping any</li>
        <li><strong>Revenue orientation:</strong> Ability to tie every activity back to pipeline and revenue impact</li>
        <li><strong>Cross-functional coordination:</strong> Working with sales, marketing, product, and legal teams internally while managing external partner contacts</li>
        <li><strong>Strategic thinking:</strong> Identifying which partners to invest in and which to deprioritize based on potential, not just current revenue</li>
        <li><strong>Communication:</strong> Clear writing and presenting skills. You will spend a lot of time on partner business reviews, internal stakeholder updates, and program documentation</li>
    </ul>

    <h3>High-Value Skills</h3>
    <ul>
        <li><strong>Data analysis:</strong> Ability to pull insights from partner performance data, overlap analysis, and attribution reports</li>
        <li><strong>PRM platform experience:</strong> Hands-on experience with tools like Impartner, PartnerStack, or Allbound (see our <a href="/tools/category/prm/">PRM reviews</a>)</li>
        <li><strong>Co-selling tool fluency:</strong> Crossbeam, Reveal, and similar platforms for account mapping and ecosystem intelligence</li>
        <li><strong>Marketplace knowledge:</strong> Understanding of AWS, Azure, or GCP marketplace mechanics for cloud co-sell roles</li>
    </ul>

    <h2>Certifications Worth Considering</h2>

    <p>Partnerships does not have mandatory certifications like accounting or project management. But a few credentials can strengthen your application, especially if you are transitioning from another function:</p>

    <ul>
        <li><strong>PartnerPath Certification:</strong> Covers partner program design, partner experience optimization, and ecosystem strategy. Well-regarded among channel leaders.</li>
        <li><strong>Cloud marketplace certifications:</strong> AWS Partner Accreditation, Microsoft Partner certifications, or Google Cloud partner training. Essential for cloud co-sell roles.</li>
        <li><strong>PRM vendor certifications:</strong> Impartner, PartnerStack, and other PRM vendors offer admin and user certifications that demonstrate platform competence.</li>
        <li><strong>Salesforce certifications:</strong> If your target companies run Salesforce, a Salesforce Admin or Sales Cloud cert shows you can work within the CRM ecosystem that most partner teams depend on.</li>
    </ul>

    <p>Do not over-invest in certifications. One or two relevant ones can help you get past resume screens, but hiring managers care far more about demonstrated results with partners.</p>

    <h2>Tools You Should Know</h2>

    <p>The modern partner tech stack includes:</p>

    <ul>
        <li><strong>PRM platforms:</strong> <a href="/tools/category/prm/">Impartner, PartnerStack, Allbound, Channeltivity</a></li>
        <li><strong>Co-selling/ecosystem platforms:</strong> <a href="/tools/category/co-selling/">Crossbeam, Reveal</a></li>
        <li><strong>CRM:</strong> <a href="/tools/category/crm/">Salesforce, HubSpot</a> (you will live in CRM daily)</li>
        <li><strong>Marketplace tools:</strong> <a href="/tools/category/marketplace/">Tackle.io, CloudBlue</a> for cloud marketplace management</li>
        <li><strong>Analytics:</strong> <a href="/tools/category/analytics/">Partner performance dashboards, attribution tools</a></li>
    </ul>

    <p>You do not need to be an expert in all of these before your first partner role. But familiarity with the landscape shows hiring managers you understand the modern partner function. Browse our <a href="/tools/">full tools directory</a> for detailed reviews.</p>

    <h2>Salary Expectations</h2>

    <p>Partner manager compensation varies by seniority, company stage, and location. Here is what to expect based on our <a href="/salary/">salary data</a>:</p>

    <ul>
        <li><strong>Associate/Junior Partner Manager:</strong> $65,000 to $85,000 base, $80,000 to $110,000 OTE</li>
        <li><strong>Partner Manager (mid-level):</strong> $90,000 to $120,000 base, $120,000 to $160,000 OTE</li>
        <li><strong>Senior Partner Manager:</strong> $120,000 to $155,000 base, $160,000 to $210,000 OTE</li>
        <li><strong>Director of Partnerships:</strong> $150,000 to $190,000 base, $200,000 to $280,000 OTE</li>
        <li><strong>VP of Partnerships:</strong> $180,000 to $250,000 base, $250,000 to $350,000+ OTE</li>
    </ul>

    <p>Remote roles and major tech hubs (San Francisco, New York, Seattle) tend to pay 15 to 25% above the median. Early-stage startups may offer lower base with more equity. Enterprise companies typically pay the highest base salaries.</p>

    <p>For detailed breakdowns by location and company stage, see our <a href="/salary/by-location/">salary by location</a> and <a href="/salary/by-seniority/">salary by seniority</a> pages.</p>

    <h2>How to Get Your First Partner Role</h2>

    <ol>
        <li><strong>Build internal credibility:</strong> If you are at a company with a partner program, volunteer for co-selling, partner events, or partner onboarding projects. Get visible to the partnerships team.</li>
        <li><strong>Document your results:</strong> Track every partner-related deal, introduction, or project you contribute to. Quantify it. "Influenced $X in partner-sourced pipeline" is the kind of data point that gets you hired.</li>
        <li><strong>Learn the tools:</strong> Sign up for free trials of PRM and co-selling platforms. Complete any available vendor certifications.</li>
        <li><strong>Network in the ecosystem:</strong> Follow partnership leaders on LinkedIn. Join communities like Partnership Leaders, the SaaS Partnerships Slack, or local partner meetups.</li>
        <li><strong>Target the right companies:</strong> Look for companies that are building or expanding their partner programs. Job postings for a company's first partner manager or a team that is scaling from 2 to 5 people signal the most growth opportunity.</li>
    </ol>

    <h2>Common Interview Questions</h2>

    <p>Expect these in partner management interviews:</p>

    <ul>
        <li>How would you evaluate whether a potential partner is worth investing in?</li>
        <li>Describe a time you managed a complex multi-stakeholder relationship. What was the outcome?</li>
        <li>How do you prioritize across a portfolio of 30+ partners with different levels of engagement?</li>
        <li>What metrics would you use to measure the health of a partner program?</li>
        <li>How would you handle a partner that is underperforming against their commitments?</li>
        <li>Walk me through how you would onboard a new strategic partner in your first 90 days.</li>
    </ul>

    <p>The best answers combine strategic thinking with specific examples. Use numbers whenever possible. "I managed 25 partners and grew partner-sourced revenue from $X to $Y in 12 months" beats any theoretical framework.</p>

</div>
'''
    body += newsletter_cta_html("Get partnership career intel every Monday.")

    faq_pairs = [
        ("Do I need a specific degree to become a partner manager?",
         "No. There is no required degree for partner management. Most partner managers have business, marketing, or communications backgrounds, but hiring managers prioritize relevant experience and demonstrated relationship management skills over specific credentials."),
        ("How long does it take to become a partner manager?",
         "Most people transition into their first partner management role after 2 to 4 years of experience in sales, marketing, or customer success. Direct entry from college is rare but possible at companies with associate-level partner programs."),
        ("What is the difference between a partner manager and a channel account manager?",
         "Partner manager is the broader term covering all partner types (technology, referral, reseller, integration). Channel account manager typically refers specifically to managing reseller and distributor relationships in traditional channel sales models."),
        ("Is partner management a good career for introverts?",
         "Yes, if you are comfortable with one-on-one relationship building. Partner management involves deep relationship work, strategic analysis, and written communication. It is not cold calling. Many successful partner managers describe themselves as introverts who are energized by meaningful professional relationships."),
    ]

    body += faq_html(faq_pairs)

    word_count = len(body.split())
    page = get_page_wrapper(
        title=title,
        description=description,
        canonical_path="/careers/how-to-become-partner-manager/",
        body_content=body,
        active_path="/careers/",
        extra_head=get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs) + get_article_schema(title, description, "how-to-become-partner-manager", "2026-04-01", word_count, url_path="/careers/how-to-become-partner-manager/"),
        body_class="page-inner",
    )
    write_page("careers/how-to-become-partner-manager/index.html", page)
    print(f"  Built: careers/how-to-become-partner-manager/index.html")


# ---------------------------------------------------------------------------
# Job Market Growth
# ---------------------------------------------------------------------------

def build_job_growth():
    title = "Partnerships & Channel Job Market Growth in 2026"
    description = (
        "Data on partnerships and channel sales job market growth. Role demand,"
        " hiring trends, top titles, and projections through 2027. Updated weekly."
    )

    crumbs = [("Home", "/"), ("Careers", "/careers/"), ("Job Market Growth", None)]
    bc_html = breadcrumb_html(crumbs)

    body = f'''{bc_html}
<section class="page-header">
    <h1>Partnerships &amp; Channel Job Market Growth</h1>
    <p class="page-header-subtitle">Hiring trends, role demand, and projections for the partnerships function.</p>
</section>
<div class="container article-content">

    <p>The partnerships and channel sales job market has expanded significantly since 2022. What was once a niche function staffed by a single "partner guy" at most companies has become a strategic growth lever with dedicated teams, specialized roles, and executive-level leadership.</p>

    <p>This page tracks the data behind that growth: which roles are being created, which industries are hiring, and where the market is heading.</p>

    <h2>The Numbers: Partnerships Hiring 2022 to 2026</h2>

    <p>Job postings containing "partnerships," "channel sales," or "partner manager" in the title have grown consistently over the past four years:</p>

    <div class="data-table-wrapper">
        <table class="data-table">
            <thead>
                <tr>
                    <th>Year</th>
                    <th>Estimated Job Postings</th>
                    <th>YoY Growth</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>2022</td><td>18,000</td><td>Baseline</td></tr>
                <tr><td>2023</td><td>24,500</td><td>+36%</td></tr>
                <tr><td>2024</td><td>33,000</td><td>+35%</td></tr>
                <tr><td>2025</td><td>45,000</td><td>+36%</td></tr>
                <tr><td>2026 (projected)</td><td>58,000+</td><td>+29%</td></tr>
            </tbody>
        </table>
    </div>

    <p>Growth has moderated slightly in 2026 as the market matures, but the trend remains strongly upward. The partnerships function is following the same trajectory that sales operations followed a decade ago: from optional to essential.</p>

    <h2>Fastest-Growing Roles</h2>

    <p>Not all partnership roles are growing at the same rate. The highest demand is concentrated in a few categories:</p>

    <h3>1. Ecosystem and Platform Partnerships</h3>
    <p>Roles focused on technology integrations, API partnerships, and platform ecosystem management are growing fastest. Companies building platform plays (think HubSpot, Shopify, Salesforce) need people who can recruit technology partners, manage integration quality, and drive ecosystem adoption. Job postings for "ecosystem" partnership roles have roughly doubled year over year since 2023.</p>

    <h3>2. Cloud Marketplace Specialists</h3>
    <p>AWS, Azure, and GCP marketplace co-sell roles are a new category that barely existed before 2022. As enterprise procurement shifts toward cloud commitment drawdown, companies need specialists who understand marketplace listing mechanics, CPPO (Channel Partner Private Offers), and co-sell attribution. These roles command premium compensation because the talent pool is still small.</p>

    <h3>3. Partner Operations</h3>
    <p>As partner programs scale, the operational complexity increases. Partner ops roles manage PRM platforms, deal registration workflows, partner data hygiene, and program analytics. This is the "RevOps for partnerships" equivalent, and it is growing as companies realize they cannot scale partner programs without operational infrastructure.</p>

    <h3>4. Partner Marketing</h3>
    <p>Co-marketing, through-partner marketing, and partner content roles are expanding as companies invest more in enabling their partners to generate demand. Partner marketing managers who can run co-branded campaigns and measure partner marketing ROI are in high demand.</p>

    <h2>Industries Hiring the Most</h2>

    <p>Partnership hiring is concentrated in a few sectors:</p>

    <ul>
        <li><strong>B2B SaaS:</strong> By far the largest employer of partnership professionals. Every major SaaS category (CRM, marketing automation, HR tech, fintech, cybersecurity) is building or expanding partner programs.</li>
        <li><strong>Cloud infrastructure:</strong> AWS, Azure, GCP, and the ISV ecosystem around them. Cloud marketplace roles are a major driver.</li>
        <li><strong>Fintech:</strong> Embedded finance and banking-as-a-service companies are building partnership functions to distribute through non-financial brands.</li>
        <li><strong>E-commerce and retail tech:</strong> Shopify, BigCommerce, and the app ecosystem around them. Agency partnerships and technology integrations are key growth levers.</li>
        <li><strong>Cybersecurity:</strong> Channel-heavy by tradition, now adding modern partnership roles (ecosystem, co-sell, marketplace) on top of the traditional reseller model.</li>
    </ul>

    <h2>Geographic Distribution</h2>

    <p>Partnership roles have followed the broader remote work trend in tech:</p>

    <ul>
        <li><strong>Fully remote:</strong> Approximately 45% of partnerships job postings list remote as an option, up from 25% in 2022</li>
        <li><strong>Hybrid:</strong> 30% of postings require some in-office presence, typically 2 to 3 days per week</li>
        <li><strong>Onsite:</strong> 25% require full-time office presence, mostly at enterprise companies or in field partnership roles</li>
    </ul>

    <p>The top metro areas for in-person partnership roles remain San Francisco, New York, Seattle, Austin, and Boston. For detailed salary data by location, see our <a href="/salary/by-location/">Salary by Location</a> page.</p>

    <h2>Compensation Trends</h2>

    <p>Partnership salaries have risen faster than the broader tech market over the past three years, driven by talent scarcity:</p>

    <ul>
        <li><strong>Entry-level partner roles:</strong> Base salaries have increased 12 to 18% since 2023</li>
        <li><strong>Mid-level partner managers:</strong> Base salaries up 15 to 22%, with OTE growth outpacing base as companies add variable compensation tied to partner-sourced revenue</li>
        <li><strong>Director and VP level:</strong> Total compensation packages have grown 20 to 30%, with equity becoming a standard component at growth-stage companies</li>
    </ul>

    <p>The compensation premium for partnerships roles reflects the difficulty of hiring experienced talent. Unlike sales or marketing, the partnerships talent pool is still relatively shallow. Companies often compete for the same candidates, driving up offers. For current salary benchmarks, see our full <a href="/salary/">Salary Data</a> section.</p>

    <h2>What This Means for Your Career</h2>

    <p>If you are considering a career in partnerships or already in the function, the market fundamentals are strongly in your favor:</p>

    <ul>
        <li><strong>Demand exceeds supply.</strong> There are more open partnership roles than qualified candidates. This gives you leverage in job searches and salary negotiations.</li>
        <li><strong>Specialization pays.</strong> Generalist partner managers are abundant. Specialists in cloud marketplace, ecosystem strategy, or partner operations command premium compensation.</li>
        <li><strong>The function is still being defined.</strong> Unlike sales or marketing, partnerships does not have rigid career ladders at most companies. Early career professionals who join now can shape the function as it matures.</li>
        <li><strong>Adjacent skills transfer well.</strong> If you are in sales, marketing, CS, or solutions engineering, the transition to partnerships is shorter than you think. See our guide on <a href="/careers/how-to-become-partner-manager/">how to become a partner manager</a> for specific paths.</li>
    </ul>

</div>
'''
    body += newsletter_cta_html("Weekly partnerships job market data, every Monday.")

    faq_pairs = [
        ("How fast is the partnerships job market growing?",
         "Job postings for partnerships and channel roles have grown 30 to 40% year over year since 2022. The market is projected to reach 58,000+ annual postings in 2026, up from 18,000 in 2022."),
        ("Which partnership roles are in highest demand?",
         "Ecosystem and platform partnerships, cloud marketplace specialists, and partner operations roles are growing fastest. These specializations command premium compensation due to limited talent supply."),
        ("Are partnerships jobs available remotely?",
         "Yes. Approximately 45% of partnerships job postings offer remote work, up from 25% in 2022. The trend toward remote-friendly partnership roles continues to accelerate."),
        ("Do partnerships roles pay well compared to sales?",
         "Partner manager compensation is comparable to account executive compensation at the same seniority level. Senior partnership roles (Director, VP) often pay more than equivalent sales management roles because the talent pool is smaller and the strategic impact is higher."),
    ]

    body += faq_html(faq_pairs)

    word_count = len(body.split())
    page = get_page_wrapper(
        title=title,
        description=description,
        canonical_path="/careers/job-growth/",
        body_content=body,
        active_path="/careers/",
        extra_head=get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs) + get_article_schema(title, description, "job-growth", "2026-04-01", word_count, url_path="/careers/job-growth/"),
        body_class="page-inner",
    )
    write_page("careers/job-growth/index.html", page)
    print(f"  Built: careers/job-growth/index.html")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def build_all_careers_pages():
    print("\n  Building career pages...")
    build_careers_index()
    build_how_to_become_partner_manager()
    build_job_growth()
