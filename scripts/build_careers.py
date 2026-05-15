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
        <a href="/careers/negotiating-partner-manager-offer/" class="preview-card">
            <h3>Negotiating a Partner Manager Offer</h3>
            <p>Anchors, scripts, and equity questions for the offer conversation. Based on 852 disclosed partner manager salaries from 2026 hiring data.</p>
            <span class="preview-link">Read the playbook &rarr;</span>
        </a>
        <a href="/careers/partner-manager-vs-alliance-manager/" class="preview-card">
            <h3>Partner Manager vs. Alliance Manager</h3>
            <p>Two overlapping titles, different jobs. Pay, scope, and trajectory comparison using 2026 hiring data and disclosed compensation bands.</p>
            <span class="preview-link">Compare the roles &rarr;</span>
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
# Negotiating a Partner Manager Offer
# ---------------------------------------------------------------------------

def build_negotiating_partner_manager_offer():
    title = "Negotiate a Partner Manager Offer"
    description = (
        "How to negotiate a partner manager offer in 2026 using real disclosed"
        " salary data. Anchors, scripts, equity questions, and the moves that move base pay."
    )
    slug = "negotiating-partner-manager-offer"
    canonical = f"/careers/{slug}/"
    crumbs = [("Home", "/"), ("Careers", "/careers/"), ("Negotiating an Offer", None)]
    bc_html = breadcrumb_html(crumbs)

    body = f'''{bc_html}
<section class="page-header">
    <h1>How to Negotiate a Partner Manager Offer</h1>
    <p class="page-header-subtitle">A practical, data-grounded playbook using 852 disclosed partner manager salaries from 2026 hiring data.</p>
</section>
<article class="insight-article">
<div class="article-layout">
<div class="article-content">

<p>Most partner managers leave $15,000 to $40,000 of base salary on the table at offer stage. Not because they negotiate poorly, but because they walk in without an anchor. This guide gives you the anchor.</p>

<p>The data here comes from 852 disclosed partner manager salaries across 1,304 tracked roles in 2026. We will walk through the four numbers you need at the negotiating table, the three questions that move offers most, and the moves that work for the specific seniority you are interviewing for.</p>

<h2>The Four Numbers You Need</h2>

<p>Walk into every partner manager negotiation knowing these four anchors for your seniority level.</p>

<ul>
    <li>Median base for your seniority (the most common number)</li>
    <li>Average maximum for your seniority (the top of typical bands)</li>
    <li>Top-of-market for the role (the ceiling)</li>
    <li>OTE multiplier (what total comp tends to be vs. base)</li>
</ul>

<p>Here are the 2026 numbers by seniority, sourced from our salary dataset:</p>

<ul>
    <li>Entry-level: $67K median, $104K average max, ~1.2x OTE multiplier</li>
    <li>Mid-level: $98K median, $158K average max, ~1.4x OTE multiplier</li>
    <li>Senior: $140K median, $206K average max, ~1.5x OTE multiplier</li>
    <li>Director: $133K median, $197K average max, ~1.5x OTE multiplier</li>
    <li>VP: $150K median, $268K average max, ~1.6x OTE multiplier</li>
</ul>

<p>OTE multipliers are estimates based on disclosed equity and variable comp signals. Treat them as directional, not precise. Your actual variable component will depend on the company and the role structure.</p>

<h2>The First 60 Seconds of Comp Discussion</h2>

<p>Three rules for the opening comp conversation.</p>

<p>Rule one: never give a number first. If the recruiter asks for your target, deflect to range. "I am targeting roles in the $140K to $170K base range depending on equity and variable comp" is fine. "I want $150K" gives the company a ceiling to anchor below.</p>

<p>Rule two: separate base, variable, and equity in your head before the call. Most candidates conflate these and get talked into a low base by a promise of "huge equity upside." Equity at most companies is illusory unless the company is profitable, has a clear exit path, or has a liquid secondary market. Anchor on base first.</p>

<p>Rule three: do not negotiate against yourself. If the recruiter mentions a range, the actual offer will usually come in at the floor of that range. Your job is to push it toward the ceiling, not anchor at the midpoint.</p>

<h2>The Three Questions That Move Offers</h2>

<p>Once you have an offer in hand, three questions consistently produce upward movement.</p>

<p>Question one: "What is the band for this role, and where in the band is this offer?" If the offer is below the midpoint of the company's band, there is room to move. Most recruiters will admit if the offer is at the floor of the band, which is a clear signal to push back.</p>

<p>Question two: "What does the path to the next level look like?" This is not directly about money, but it surfaces whether the next promotion is a year out or three years out. For partner manager roles, that timeline shapes the value of accepting a lower base in exchange for faster advancement.</p>

<p>Question three: "Can we revisit base?" Asked once, calmly, with a specific counter number. Vague pushback ("can you do better?") gets vague responses. Specific pushback ("I am hoping to see base at $145K based on what comparable roles in this market are paying") gets specific responses.</p>

<h2>Equity Questions Worth Asking</h2>

<p>Equity is the easiest place to lose money in a partner manager negotiation, because most candidates do not know what to ask.</p>

<ul>
    <li>Total share count outstanding (so you can calculate your percentage ownership)</li>
    <li>Strike price and current 409A valuation</li>
    <li>Vesting schedule, including cliff and acceleration on change of control</li>
    <li>Whether there is an equity refresh program and when you become eligible</li>
    <li>What the most recent secondary or tender offer priced shares at</li>
</ul>

<p>If the company will not share these details, the equity should be treated as having near-zero value for negotiation purposes. Real equity packages come with transparent math. Opaque equity packages usually exist because the math does not flatter the company.</p>

<h2>Moves by Seniority</h2>

<p>Different seniority levels have different levers worth pulling.</p>

<p>Entry-level: push for sign-on bonus rather than base. Companies are more flexible on one-time payments than on raising base, because base affects internal banding. A $10K sign-on bonus on an entry-level offer is meaningful and often achievable.</p>

<p>Mid-level: push for both base and equity. This is the band where the most negotiation movement happens. Companies expect mid-level candidates to negotiate. Coming in at the listed offer signals you do not understand market.</p>

<p>Senior: push for variable comp structure, including how partner-sourced or influenced revenue is measured. The base is somewhat capped by internal bands, but the variable structure is often negotiable and can change your effective comp by $20K to $40K annually.</p>

<p>Director and above: push for scope, team budget, and reporting line in addition to comp. Director and VP roles are about leverage as much as money. A director role reporting to the CRO with a five-person team and a $500K MDF budget is worth more than the same title without those.</p>

<h2>What Not to Do</h2>

<p>Three negotiating moves that hurt partner manager candidates.</p>

<p>Bluffing competing offers you do not have. Recruiters track this. If you claim a competing offer, expect to be asked for details. Inventing a number you cannot back up damages trust for the rest of the relationship.</p>

<p>Negotiating after accepting. Once you have said yes, your leverage is gone. Take the time to negotiate before accepting, even if it means delaying the start date by a week.</p>

<p>Asking for "more" without a number. Pushing back without specifying what you want creates ambiguity. The company will respond by adding a small amount and assuming the negotiation is done. Always pair pushback with a specific counter number.</p>

<h2>When to Walk</h2>

<p>Two scenarios where walking is the right move.</p>

<p>If the company refuses to share the band after multiple asks. This indicates either an opaque compensation process or an intentionally low offer. Either way, the relationship starts on a bad foot and rarely recovers.</p>

<p>If the offer comes in below the median for your seniority and the company refuses to move. The 50th percentile is a low bar. Accepting below it sets a comp trajectory you will spend years correcting at your next company.</p>

<p>Walking is a real option more often than candidates think. Partner manager hiring in 2026 is competitive on the employer side. Companies that lose a final-round candidate over compensation usually re-engage within 30 to 60 days with a stronger offer.</p>

<h2>The Larger Frame</h2>

<p>The negotiation conversation itself is information. How a company handles the back-and-forth tells you a lot about how it will handle the next four years of comp adjustments, promotion conversations, and equity refreshes. Companies that negotiate well at offer stage tend to negotiate well throughout the relationship. Companies that pressure you into a low offer at the start tend to pressure you on every comp conversation afterward.</p>

<p>If the negotiation feels adversarial in a way that surprises you, pay attention to that signal. The role is also a culture sample. The way they negotiate is how they operate.</p>

</div>
<aside class="article-sidebar">
    <h3>Related data on this site</h3>
    <ul class="article-sidebar-links">
        <li><a href="/salary/">Full salary index</a></li>
        <li><a href="/salary/by-seniority/">Pay by seniority</a></li>
        <li><a href="/salary/calculator/">Salary calculator</a></li>
        <li><a href="/insights/salary-disclosure-in-partnerships-roles/">Why partner jobs hide pay</a></li>
    </ul>
</aside>
</div>
</article>
'''
    word_count = 1450
    faq_pairs = [
        ("How much can you negotiate up on a partner manager offer?",
         "On average, partner manager candidates who negotiate end up $15,000 to $40,000 of annual base salary higher than the initial offer. The exact movement depends on seniority, how far below the median the initial offer lands, and how cleanly the candidate anchors with market data."),
        ("Should I share my current salary when asked?",
         "No. In most US states, employers are legally barred from asking, and even where they are not, sharing your current number anchors the offer to your current comp rather than to the market rate for the role. Redirect with a target range based on market data for the role you are interviewing for."),
        ("What is the typical OTE multiplier for partner manager roles?",
         "Total compensation typically runs 1.2x to 1.6x base for partner manager roles, depending on seniority. Entry-level partner managers see closer to 1.2x. Senior, director, and VP roles trend toward 1.5x to 1.6x. Variable comp is usually tied to partner-sourced revenue, partner-influenced revenue, or program metrics."),
        ("Is it worth negotiating if the offer is already strong?",
         "Usually yes, but the moves shift. If base is already at or above the median for your seniority, push for equity, signing bonus, or non-cash elements (vacation, remote flexibility, equipment budget). Companies that respond well to a polite ask on a strong offer tend to be the same companies that handle internal comp adjustments well over time."),
    ]
    body += faq_html(faq_pairs)
    body += newsletter_cta_html("Career intelligence for partner and channel professionals, every Monday.")

    article_schema = get_article_schema(title, description, slug, "2026-05-14", word_count, url_path=canonical)
    extra_head = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs) + article_schema

    page = get_page_wrapper(
        title=title,
        description=description,
        canonical_path=canonical,
        body_content=body,
        active_path="/careers/",
        extra_head=extra_head,
        body_class="page-inner",
    )
    write_page(f"careers/{slug}/index.html", page)
    print(f"  Built: careers/{slug}/index.html")


# ---------------------------------------------------------------------------
# Partner Manager vs Alliance Manager
# ---------------------------------------------------------------------------

def build_partner_manager_vs_alliance_manager():
    title = "Partner Manager vs. Alliance Manager"
    description = (
        "Partner manager and alliance manager titles overlap but signal different roles."
        " Pay, scope, and trajectory comparison using 2026 hiring and salary band data."
    )
    slug = "partner-manager-vs-alliance-manager"
    canonical = f"/careers/{slug}/"
    crumbs = [("Home", "/"), ("Careers", "/careers/"), ("Partner vs. Alliance Manager", None)]
    bc_html = breadcrumb_html(crumbs)

    body = f'''{bc_html}
<section class="page-header">
    <h1>Partner Manager vs. Alliance Manager</h1>
    <p class="page-header-subtitle">Both titles show up in partner organizations. The pay is similar. The work is not. Here is how to tell them apart before you take the job.</p>
</section>
<article class="insight-article">
<div class="article-layout">
<div class="article-content">

<p>Partner manager and alliance manager are two titles that often appear at the same company, sometimes on the same team, occasionally for the same job. Most candidates use them interchangeably. Most hiring managers do not.</p>

<p>The difference matters because the day-to-day work, the kind of partners you manage, and the path from one role to the next look meaningfully different. This guide walks through how the two roles diverge in 2026, what the pay data says, and how to figure out which version you are actually interviewing for.</p>

<h2>The Core Distinction</h2>

<p>Partner manager is the broader category. It typically describes someone managing a portfolio of partner relationships: technology partners, resellers, agencies, or referral partners. The scope can be wide or narrow depending on the company. Most companies use "partner manager" as a default title for anyone in a partner-facing seat.</p>

<p>Alliance manager is the more specific category. It typically describes someone managing a small number of high-value strategic partner relationships, often with named global system integrators (SIs), major cloud providers (AWS, Azure, GCP), or large ISVs. Alliance manager work is fewer relationships, deeper engagement, and longer time horizons.</p>

<p>The practical test: a partner manager probably owns 15 to 50 partner relationships and works on monthly metrics. An alliance manager probably owns 3 to 8 strategic relationships and works on quarterly or annual joint business plans.</p>

<h2>What the Pay Data Says</h2>

<p>Across our 2026 dataset, the two titles cluster around similar but slightly different bands.</p>

<ul>
    <li>Partner Manager (all seniorities): $98K to $158K average band, $120K median base</li>
    <li>Alliance Manager (all seniorities): $115K to $175K average band, $135K median base</li>
</ul>

<p>Alliance manager roles pay about 12 percent more at the median than partner manager roles. Two reasons. First, alliance manager titles cluster at larger companies (Visa, ADP, Red Hat, AWS) which pay more broadly. Second, the scope of an alliance manager job tends to involve larger deals and bigger budgets, which justifies a higher band.</p>

<p>At the VP level, the gap narrows. VP of Partnerships and VP of Alliances both sit in the $180K to $270K base range with significant equity components. The titles converge at the leadership level because the scope (running a partner organization) becomes more important than the title nomenclature.</p>

<h2>Day-to-Day Differences</h2>

<p>A typical week for a partner manager involves: 10 to 20 partner calls, deal registration triage, joint marketing campaign coordination, partner enablement (training, certification, onboarding), and pipeline reporting. The pace is operational. The success metrics are deal-shaped (sourced revenue, influenced revenue, partner attach rate).</p>

<p>A typical week for an alliance manager involves: 3 to 5 deep strategic calls, joint business plan development, executive briefings with partner leadership, co-marketing strategy at the program level, and quarterly business reviews with named alliance partners. The pace is more strategic and longer-cycle. Success metrics are program-shaped (joint pipeline, named opportunities co-developed, marketplace co-sell volume).</p>

<p>Neither role is harder. They are different. A great partner manager is operationally precise and high-energy. A great alliance manager is strategically patient and politically fluent. Most people are better suited to one than the other.</p>

<h2>Career Trajectories</h2>

<p>Partner manager career path typically runs: partner manager, senior partner manager, director of partnerships, VP of partnerships. The progression is gradual and tied to managing more partners and more revenue.</p>

<p>Alliance manager career path typically runs: alliance manager, senior alliance manager, head of alliances, VP of strategic alliances. The progression is tied to owning bigger strategic relationships and shaping the company's positioning with major ecosystem partners.</p>

<p>Switching between the two tracks happens, but usually only at the senior IC or director level. An alliance manager at a startup may move into a broader partner manager role at a larger company. A partner manager at a mid-sized company may grow into an alliance manager role focused on a single global SI relationship.</p>

<h2>Which Role Is Right For You</h2>

<p>Three diagnostic questions.</p>

<p>Do you prefer breadth or depth in your professional relationships? Partner managers thrive on a wide portfolio of medium-depth relationships. Alliance managers thrive on a small number of deep, multi-year relationships with major partners.</p>

<p>How comfortable are you with longer feedback loops? Partner manager work has shorter cycles: a deal registered this quarter shows up as sourced revenue next quarter. Alliance manager work has longer cycles: a joint go-to-market plan negotiated this year may not produce significant pipeline for 12 to 18 months.</p>

<p>How political is your tolerance? Alliance manager work involves significant cross-organizational politics, particularly at the leadership level. You will spend meaningful time aligning your executives with your partner's executives. Partner managers can sometimes operate below the political radar. Alliance managers cannot.</p>

<h2>How to Tell Which Role You Are Interviewing For</h2>

<p>Four questions that surface the truth, regardless of what the job title says.</p>

<ul>
    <li>How many partner relationships will I own?</li>
    <li>What are the names of the partners I will manage?</li>
    <li>Do I have a hard quota, or do I own program metrics?</li>
    <li>Who at the partner organization is my counterpart, and what level are they?</li>
</ul>

<p>If you will own 15+ partners with names you have never heard of, that is a partner manager role. If you will own 3 to 5 named partners, including at least one Fortune 500 partner with a Senior Director or VP-level counterpart, that is an alliance manager role. The title is a label. The questions tell you what the job is.</p>

<h2>When Companies Use the Titles Loosely</h2>

<p>Some companies use both titles for similar roles, which creates confusion. Two patterns to watch for.</p>

<p>Title inflation. A startup might call a partner manager role an "alliance manager" to sound more strategic. The pay band and scope tell you whether the title is real. If the role is called "alliance manager" but the scope is 30 partners and the pay is $110K, that is a partner manager role with an aspirational title.</p>

<p>Title hierarchy. Some companies use "partner manager" for individual contributors and "alliance manager" for senior individual contributors with a couple of high-value partners. Both report to the same head of partnerships. This is internally coherent but invisible to external candidates. Ask about the internal hierarchy explicitly.</p>

<p>Bottom line: do not optimize for the title. Optimize for the scope, the partners, and the pay band. Two years into the role, no one will ask whether your business card said partner manager or alliance manager. They will ask what you built.</p>

</div>
<aside class="article-sidebar">
    <h3>Related data on this site</h3>
    <ul class="article-sidebar-links">
        <li><a href="/glossary/alliance-manager/">Alliance manager defined</a></li>
        <li><a href="/glossary/channel-manager/">Channel manager defined</a></li>
        <li><a href="/salary/by-seniority/">Pay by seniority</a></li>
        <li><a href="/insights/vp-of-partnerships-compensation/">VP partnerships pay</a></li>
    </ul>
</aside>
</div>
</article>
'''
    word_count = 1380
    faq_pairs = [
        ("What is the difference between a partner manager and an alliance manager?",
         "Partner manager typically describes someone managing a portfolio of 15 to 50 partner relationships with monthly operating metrics. Alliance manager typically describes someone managing 3 to 8 high-value strategic partnerships (often named global SIs or major cloud providers) with quarterly and annual planning cycles. The titles can overlap, but the day-to-day work and the kind of partners you own usually differ."),
        ("Do alliance managers make more than partner managers?",
         "Slightly, at the median. Alliance manager roles in our 2026 dataset average about 12 percent higher than partner manager roles ($135K median base vs. $120K median base). The gap narrows at the VP level, where both titles converge around $180K to $270K base. Most of the gap is driven by alliance manager titles clustering at larger enterprise companies."),
        ("Can you switch from partner manager to alliance manager?",
         "Yes, most commonly at the senior individual contributor or director level. Partner managers who want to move into alliances usually need to either grow into a larger named strategic relationship at their current company or move to a new company in a more focused alliance role. The reverse path (alliance manager to partner manager) is also common when alliance managers want broader portfolio experience."),
        ("Which role has a better career path?",
         "Neither is universally better. Partner manager paths offer more lateral mobility and a wider range of company types. Alliance manager paths offer deeper expertise with named partners and a more strategic orientation. The right path depends on whether you prefer breadth or depth, shorter or longer feedback loops, and lower or higher political surface area in your day-to-day work."),
    ]
    body += faq_html(faq_pairs)
    body += newsletter_cta_html("Career analysis for partnership and alliance professionals, every Monday.")

    article_schema = get_article_schema(title, description, slug, "2026-05-14", word_count, url_path=canonical)
    extra_head = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs) + article_schema

    page = get_page_wrapper(
        title=title,
        description=description,
        canonical_path=canonical,
        body_content=body,
        active_path="/careers/",
        extra_head=extra_head,
        body_class="page-inner",
    )
    write_page(f"careers/{slug}/index.html", page)
    print(f"  Built: careers/{slug}/index.html")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def build_all_careers_pages():
    print("\n  Building career pages...")
    build_careers_index()
    build_how_to_become_partner_manager()
    build_job_growth()
    build_negotiating_partner_manager_offer()
    build_partner_manager_vs_alliance_manager()
