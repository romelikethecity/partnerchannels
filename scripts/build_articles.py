# scripts/build_articles.py
# Insights article renderer + article data store.
# Each article is a self-contained dict. The renderer turns it into a
# /insights/{slug}/ page with Article schema, breadcrumbs, and FAQ schema
# where applicable. The insights hub becomes a dynamic list of these articles.

import os

from nav_config import *
from templates import (get_page_wrapper, write_page, get_breadcrumb_schema,
                       get_article_schema, get_faq_schema, breadcrumb_html,
                       newsletter_cta_html, faq_html)


# ---------------------------------------------------------------------------
# Article data
# ---------------------------------------------------------------------------

ARTICLES = [
    {
        "slug": "state-of-partner-manager-compensation-2026",
        "title": "State of Partner Manager Pay in 2026",
        "description": "What 852 disclosed partner manager salaries say about the market in 2026: medians by seniority, location premiums, and the gap between base and total comp.",
        "date_published": "2026-05-14",
        "word_count": 1750,
        "category": "Compensation",
        "summary": "The median partner manager makes $120,000 in base pay. The top of the market clears $600K. What the spread tells you about where to build a career.",
        "body": """
<p>The partner manager job market in 2026 sits in an awkward middle. Base pay has held up better than direct sales roles. Total comp lags the AE world. And the spread between the bottom and the top is wider than any other quota-carrying role we track.</p>

<p>The median disclosed base for a partner manager in our dataset is $120,000. The 75th percentile is around $158,000. The top of the market, currently a Red Hat VP of Global Cloud Partnerships, posts up to $624,170. That is a 5x ratio between median and ceiling, which is unusually wide for a single function.</p>

<p>This piece walks through what 852 disclosed salaries say about partner manager pay in 2026. It also covers what they fail to say, because 35 percent of partner roles we tracked do not disclose salary at all, even in states where they are supposed to.</p>

<h2>The Baseline: Median, Average, and the Outliers</h2>

<p>Across 1,304 partner and channel roles tracked in our dataset, 852 disclosed a salary band. That gives us a 65.3 percent disclosure rate, lower than direct sales roles and noticeably lower than tech roles overall.</p>

<p>Of the disclosing roles:</p>

<ul>
    <li>Median base: $120,000</li>
    <li>Average base midpoint: $125,801</li>
    <li>Bottom of disclosed range: $10,400 (likely a part-time or commission-only role)</li>
    <li>Top of disclosed range: $624,170 (VP of Global Cloud Partnerships at Red Hat)</li>
</ul>

<p>The average sits above the median, which tells us the distribution skews right. A small number of very high-paying roles pull the mean up. For most working partner managers, the median is the more honest number to plan around.</p>

<h2>Pay by Seniority</h2>

<p>Here is where the spread starts to make sense. Partner manager pay tracks closely with seniority once you control for it.</p>

<ul>
    <li>Entry-level (58 postings): $76K base average, $67K median. Top of range hits $104K.</li>
    <li>Mid-level (252 postings): $105K base average, $98K median. The largest cohort.</li>
    <li>Senior (128 postings): $141K base average, $140K median.</li>
    <li>Director (124 postings): $146K base average, $133K median.</li>
    <li>VP (50 postings): $178K base average, $150K median. Top of range reaches $268K.</li>
    <li>SVP (6 postings): $235K base average, $273K median.</li>
    <li>"Head of" (17 postings): $169K base average, $175K median.</li>
</ul>

<p>The biggest single-step jump is between mid and senior. Going from $98K median to $140K median is a 43 percent base increase, and it happens at roughly the four-to-six year mark for most partner managers. The next jump, senior to director, is much smaller (about $7K at the median). Director to VP, on the other hand, pushes another $17K of base and adds a meaningful equity expectation.</p>

<p>If you are mapping a partner career path, those two jumps (mid to senior, and director to VP) are where the real money lives. Senior IC vs. director is mostly a coin flip on base. What you choose between them is more about management appetite than pay.</p>

<h2>Pay by Metro</h2>

<p>Location still matters more than companies like to admit. The metros with the highest median partner manager pay in our dataset:</p>

<ul>
    <li>San Francisco (33 postings): $166K median base</li>
    <li>Austin (15 postings): $135K median base</li>
    <li>Boston (17 postings): $130K median base</li>
    <li>New York (209 postings): $128K median base</li>
    <li>Washington DC (25 postings): $125K median base</li>
    <li>Los Angeles (92 postings): $120K median base</li>
    <li>Seattle (21 postings): $118K median base</li>
    <li>Denver (10 postings): $116K median base</li>
    <li>Chicago (26 postings): $107K median base</li>
    <li>Miami (5 postings): $90K median base</li>
</ul>

<p>San Francisco still pays a meaningful premium for partner roles, around 38 percent above the national median. New York is the biggest market by volume (209 postings out of the 852 disclosed) and pays close to the broader median. Miami is the outlier on the low end, and the small sample size means we would not bet a career on that number.</p>

<p>Worth flagging: 397 of the 852 disclosed roles do not have a clearly identifiable metro, which means a lot of "remote anywhere" or unclassified geography. That bucket has a $113K median base, slightly below the geo-anchored national median.</p>

<h2>Remote vs. Onsite</h2>

<p>Onsite roles pay more. Not by a huge margin, but enough to plan around.</p>

<ul>
    <li>Onsite roles (737 postings): $127K base average, $120K median</li>
    <li>Remote roles (115 postings): $119K base average, $115K median</li>
</ul>

<p>That is roughly a 4 to 5 percent base difference. The gap is smaller than what we see in direct sales roles, where onsite premium can run 8 to 12 percent. Partner managers spend significant time on the road meeting partners regardless of where they live, so companies have fewer arguments for paying onsite people more. The remaining gap reflects the location premium of the metros (SF, NYC, Boston) where most onsite roles still cluster.</p>

<h2>The Top 10</h2>

<p>The highest-paying partner roles in our dataset, by maximum disclosed salary, look like this:</p>

<ol>
    <li>Vice President, Global Cloud Partnerships, Red Hat: $367K to $624K</li>
    <li>Senior Director, Strategic Partnerships (Visa Commercial Solutions, NA), Visa: $305K to $534K</li>
    <li>Senior Director, NA Head of Business Development, B2B Fintech Partnerships, Visa: $305K to $534K</li>
    <li>VP US Agency Partnerships, Teads: $300K to $500K</li>
    <li>Vice President, Partner Ecosystem, Perforce Software: $225K to $500K</li>
    <li>Product Design Director, Creator Ecosystem, Roblox: $432K to $493K</li>
    <li>SVP, Global SI Partnerships and Alliances, ADP: $273K to $458K</li>
    <li>Vice President, U.S. Retail Merchant Partnerships, Visa: $219K to $452K</li>
    <li>Director of Strategic Partnerships and Alliances, vCluster Labs: $380K to $420K</li>
</ol>

<p>Two patterns to notice. First, payments and fintech (Visa, ADP) dominate the top of the list. Visa alone has three roles in the top eight. Partnerships work that involves moving real dollars between counterparties commands a premium that pure SaaS partner roles do not match.</p>

<p>Second, the word "ecosystem" shows up more often than "channel" at the top end. The highest-paid partner roles are increasingly framed as ecosystem leadership rather than traditional channel sales management. That language shift matters for how you position your own background when you go to market.</p>

<h2>What Is Not in the Data</h2>

<p>Three caveats worth holding in your head as you read these numbers.</p>

<p>First, these are base salary midpoints. Total comp for partner roles often includes a 30 to 50 percent variable component, plus equity at venture-backed companies. The Visa and Red Hat numbers above include OTE in many cases, but most of the dataset is base only. A $120K median base for a mid-level partner manager typically maps to $160K to $200K OTE.</p>

<p>Second, 65.3 percent disclosure is low. Several large markets (notably California, Colorado, and New York) require salary disclosure in postings, but the requirement is patchily enforced and exemptions are common. The 35 percent of roles with no disclosed band skew enterprise and senior, which means the true median is probably a touch higher than $120K.</p>

<p>Third, this is a snapshot of postings, not a longitudinal study of comp progression. We track what companies offer for new hires. Internal promotion raises, retention adjustments, and exit packages do not appear here. If you have been in the same partner manager seat for three years, your comp may have drifted away from market in either direction.</p>

<h2>How to Use This</h2>

<p>If you are interviewing for a partner manager role right now, three takeaways:</p>

<p>One: the mid-to-senior jump is your biggest leverage point. If a company is hiring you as a senior IC and offering you a mid-level band, push back with the data. The $42K median gap is real.</p>

<p>Two: if the role does not disclose a band, ask early. Not at offer stage, at first call. Companies that hide bands tend to anchor low. The 35 percent of postings that hide pay are a flag worth investigating before you spend hours in the interview loop.</p>

<p>Three: VP-level partner roles are increasingly ecosystem-shaped. If your background is traditional channel sales (deal registration, partner tiering, MDF), and you want to move up, you need a thesis on how ecosystem strategy connects to revenue. Without it, you cap out around senior director.</p>

<p>We update this dataset weekly. The next version of this analysis, mid-2026, will look at how the AI tooling shift is changing what partner managers are being hired to build.</p>
""",
        "faq": [
            ("What is the median partner manager salary in 2026?",
             "The median disclosed base salary for partner manager roles in 2026 is $120,000. That figure is based on 852 disclosed salaries across 1,304 tracked roles. Total compensation, including variable pay and equity, typically runs 30 to 50 percent higher than base for these roles."),
            ("Why do so many partner manager jobs hide salary?",
             "Roughly 35 percent of partner manager postings in our dataset do not disclose a salary band, even in states like California, Colorado, and New York that require disclosure. The pattern is more common at enterprise companies and at the senior end of the market, where companies have more flexibility to negotiate and prefer not to set anchors publicly."),
            ("Which metro pays partner managers the most?",
             "San Francisco leads with a $166,000 median base, about 38 percent above the national median. Austin, Boston, and New York follow in the $128,000 to $135,000 range. Chicago and Miami sit below the national median."),
            ("What is the biggest pay jump in a partner manager career?",
             "The jump from mid-level to senior IC, where median base moves from $98,000 to $140,000, a 43 percent increase. The next jump, senior to director, is much smaller. Director to VP adds about $17,000 of base plus a meaningful step-up in equity expectations."),
        ],
        "related_articles": ["vp-of-partnerships-compensation", "entry-level-channel-roles-2026", "salary-disclosure-in-partnerships-roles"],
        "internal_links": [
            ("/salary/", "Full salary index"),
            ("/salary/by-seniority/", "Pay by seniority"),
            ("/salary/by-location/", "Pay by metro"),
            ("/salary/methodology/", "Methodology"),
        ],
    },
    {
        "slug": "prm-adoption-channel-tool-stack",
        "title": "PRM Adoption Across 1,304 Job Postings",
        "description": "Which PRM, co-selling, and partner tools show up in 1,304 partner manager job postings. Salesforce dominates. PartnerStack barely registers. AI is creeping in.",
        "date_published": "2026-05-14",
        "word_count": 1650,
        "category": "Tools",
        "summary": "Job postings name the tools companies expect partner managers to use on day one. The list looks nothing like the PRM vendor positioning maps.",
        "body": """
<p>The simplest way to figure out which tools partner organizations actually use is to read the job descriptions of the people they are hiring to use them. Vendor case studies are marketing. Analyst reports are paid placement. Job descriptions are what hiring managers admit they need.</p>

<p>We pulled tool mentions from 1,304 partner manager job postings tracked in our dataset between February and May 2026. The pattern is not what the PRM category positioning would have you expect.</p>

<h2>The Headline Numbers</h2>

<p>The most-mentioned tools across partner manager postings, ranked by appearance count:</p>

<ul>
    <li>Salesforce: 265 mentions</li>
    <li>AWS: 270 mentions (skewed by cloud partner roles)</li>
    <li>Tableau: 42 mentions</li>
    <li>HubSpot: 38 mentions</li>
    <li>Anthropic / Claude / OpenAI / Gemini / Cohere (combined AI vendors): 63 mentions</li>
    <li>GCP: 30 mentions</li>
    <li>Azure: 29 mentions</li>
    <li>Power BI: 20 mentions</li>
    <li>LinkedIn Sales Navigator: 8 mentions</li>
    <li>Looker: 6 mentions</li>
    <li>G2: 6 mentions</li>
    <li>ZoomInfo: 6 mentions</li>
    <li>Apollo: 5 mentions</li>
    <li>Marketo: 5 mentions</li>
    <li>PartnerStack: 4 mentions</li>
    <li>Gong: 3 mentions</li>
    <li>Clay: 2 mentions</li>
    <li>Crossbeam: 2 mentions</li>
</ul>

<p>The pattern is striking. Generic CRM and cloud platforms (Salesforce, AWS, GCP, Azure) dominate. Dedicated PRM platforms barely register. PartnerStack, the most-mentioned named PRM tool in the dataset, appears in only 4 postings out of 1,304. Crossbeam, the leading partner co-sell platform, appears in 2.</p>

<h2>Why PRM Tools Are Almost Invisible</h2>

<p>Three explanations, in order of likelihood.</p>

<p>First, PRM is often invisible at the job-description level because it is purchased and operated by a Partner Operations role, not the Partner Manager. The PM uses the partner portal that PRM produces, but the underlying platform is a back-end tool. Hiring managers do not list it because partner managers do not configure it.</p>

<p>Second, the partner tech category is fragmented. Even if a company runs Impartner, Allbound, or Channeltivity, the platform name rarely shows up in the JD. Generic phrasing like "experience managing a partner portal" or "PRM experience" wins out because it keeps the talent pool wider. We do not detect those phrasings in our tool mention scan, only named products.</p>

<p>Third, many partner programs simply do not run a dedicated PRM. For programs under 50 partners, Salesforce plus a shared Google Drive is still the default. PRM gets justified when the partner count crosses an operational threshold, and many of the roles we track are at companies that have not crossed it yet.</p>

<p>None of this means PRM is dead. It means PRM is a Partner Ops purchase, not a Partner Manager one. If you are a PRM vendor, your buyer is not the person reading the job description.</p>

<h2>The Salesforce Reality</h2>

<p>Salesforce shows up in 265 postings out of 1,304. That is 20 percent of the dataset. For comparison, HubSpot appears in 38 postings, or about 3 percent. Salesforce is overwhelmingly the CRM partner managers work in, particularly at companies large enough to have a dedicated partner function.</p>

<p>This shapes the practical tool stack of the working partner manager. Most of what you log lives in Salesforce. Deal registration flows through a Salesforce object. Pipeline reports come from Salesforce dashboards or a Tableau layer on top. The PRM, if one exists, is the thing partners log in to. Salesforce is the thing you live in.</p>

<p>If you are pivoting into partnerships from another go-to-market function, this is the boring but important fact: Salesforce fluency is the table-stakes skill. PRM knowledge is a nice-to-have you can pick up in a quarter.</p>

<h2>The AI Tool Surprise</h2>

<p>This is the most interesting data point in the set. AI vendor names that did not appear in partner manager job descriptions a year ago are now showing up at meaningful volume.</p>

<ul>
    <li>Anthropic: 35 mentions</li>
    <li>OpenAI: 9 mentions</li>
    <li>Cohere: 8 mentions</li>
    <li>Gemini: 7 mentions</li>
    <li>Claude: 4 mentions</li>
    <li>Vertex AI: 2 mentions</li>
    <li>Bedrock: 2 mentions</li>
    <li>Chroma: 2 mentions</li>
</ul>

<p>Combined, that is 69 mentions of named AI vendors across the dataset. Roughly 5 percent of all partner manager job postings now name an AI vendor as a relevant skill, tool, or partner. A year ago, the number was effectively zero.</p>

<p>Two patterns are driving this. One: the AI labs (Anthropic, OpenAI, Cohere) are building partner programs, and the people they are hiring are explicitly partner managers. Anthropic has 35 mentions across the dataset, which is more than HubSpot. Two: traditional B2B SaaS companies are hiring partner managers who can speak about LLM integrations and AI vendor relationships as part of the role.</p>

<p>For working partner managers, this is the signal worth tracking. The category boundary between "partner manager" and "AI partnerships specialist" is breaking down. Roles that fluently bridge both areas command a premium.</p>

<h2>Co-Sell and Marketplace Tools</h2>

<p>The other category that should be more present in the data than it is: co-sell and marketplace tooling.</p>

<ul>
    <li>Crossbeam: 2 mentions</li>
    <li>PartnerStack: 4 mentions</li>
    <li>Aligned: 4 mentions</li>
    <li>Reveal (account mapping): 0 detected mentions</li>
</ul>

<p>The named co-sell tools account for fewer than 1 percent of mentions. Some of this is the same Partner Ops dynamic from above. Some of it reflects how new this category is. Crossbeam has been a known name in the partnerships community for years, but it has only recently graduated into job descriptions as a named requirement.</p>

<p>If you are interviewing for a co-selling-heavy role, the absence of named tooling in the JD is not necessarily a red flag. It often means the team is still establishing the motion and has not standardized on a platform yet. Ask which tool they use to overlap accounts with partners. The answer (often "we send a CSV") tells you a lot about program maturity.</p>

<h2>What This Means If You Are Hiring</h2>

<p>If you are writing a partner manager JD, three suggestions.</p>

<p>First, list the actual tools your team uses. Generic phrasing ("experience with partner tools") attracts a wider but less qualified pool. Naming Salesforce, HubSpot, Crossbeam, or whatever you actually run lets candidates self-filter.</p>

<p>Second, if your program is small enough that you do not run a PRM, do not pretend otherwise. Many candidates have been burned by joining a "channel program" that turned out to be a shared spreadsheet. Naming your real stack signals what stage of program you are running.</p>

<p>Third, if AI partnerships are part of the role, say so explicitly. The candidates with both partnership and AI fluency are scarce, and being clear that the role wants both will surface a better short list than burying it.</p>

<h2>How We Pulled This</h2>

<p>The tool counts are derived from named-entity extraction on 1,304 partner manager and channel sales job descriptions tracked between February and May 2026. We match against an explicit vendor list (PRM vendors, CRM vendors, AI labs, co-sell platforms, marketplaces) and only count exact name mentions. Generic phrasing like "partner relationship management" without a vendor name is not counted.</p>

<p>One known limitation: AWS and Rust both show inflated counts because cloud partner roles often list AWS as a partner ecosystem (not a tool the PM uses), and Rust is a language tag that bleeds in from a small number of technical partner roles. Salesforce, HubSpot, and the AI vendor counts are clean.</p>

<p>We refresh this analysis monthly. The next refresh will look at how the AI vendor mention rate is changing month over month.</p>
""",
        "faq": [
            ("Which CRM do most partner managers use?",
             "Salesforce is the dominant CRM for partner managers in 2026, appearing in 265 of 1,304 tracked job postings (about 20 percent). HubSpot is a distant second at 38 postings (3 percent). At companies large enough to have a dedicated partner function, Salesforce is effectively the default."),
            ("Why do PRM platforms rarely show up in partner manager job descriptions?",
             "Three reasons: PRM is usually purchased and configured by Partner Operations rather than the partner manager, hiring managers often use generic phrasing like 'PRM experience' instead of naming a specific platform, and many smaller partner programs do not run a dedicated PRM at all (they manage in Salesforce plus shared drives)."),
            ("Are AI partnerships a real specialization now?",
             "Yes. Named AI vendors (Anthropic, OpenAI, Cohere, Gemini, Claude) appear in roughly 5 percent of partner manager job postings as of mid-2026. AI labs are building partner programs and hiring partner managers, and traditional SaaS companies are adding AI partnerships as part of the role. A year ago, the number was effectively zero."),
            ("Should a partner manager learn PartnerStack or Crossbeam before applying?",
             "Salesforce fluency matters more. PartnerStack and Crossbeam together appear in fewer than 1 percent of partner manager postings. Knowing them is a nice-to-have. Knowing Salesforce is table stakes."),
        ],
        "related_articles": ["state-of-partner-manager-compensation-2026", "partner-sourced-vs-partner-influenced-revenue"],
        "internal_links": [
            ("/tools/", "Browse all PRM and partner tool reviews"),
            ("/tools/category/prm-platforms/", "PRM platform reviews"),
            ("/tools/category/co-selling-tools/", "Co-selling tools"),
            ("/glossary/prm-partner-relationship-management/", "What is PRM?"),
        ],
    },
    {
        "slug": "vp-of-partnerships-compensation",
        "title": "VP of Partnerships Pay: 50 Postings",
        "description": "VP of partnerships base salaries from 50 disclosed 2026 postings: $150K median, $268K at the top of band, and what the SF premium looks like in this role.",
        "date_published": "2026-05-14",
        "word_count": 1500,
        "category": "Compensation",
        "summary": "The VP of partnerships role has the widest pay spread of any function we track. Here is what 50 disclosed postings show, and where the variance lives.",
        "body": """
<p>The VP of partnerships title hides more about a role than it reveals. It can mean a person managing a team of 40 partner managers at a public company. It can also mean a first GTM hire at a Series A startup with no team and no budget. The pay reflects that ambiguity.</p>

<p>Across 50 disclosed VP of partnerships and VP of channels postings tracked in our 2026 dataset, the median base is $150,000. The mean is $178,000. The top of the disclosed range, a VP of Global Cloud Partnerships at Red Hat, hits $624,170. The spread from median to top is roughly 4x, which is wider than any other VP-level GTM function we track.</p>

<p>This piece walks through the spread, what drives it, and how to read a VP of partnerships posting before you accept the interview.</p>

<h2>The Numbers</h2>

<p>Of 50 disclosed VP of partnerships postings in our dataset:</p>

<ul>
    <li>Median base: $150,000</li>
    <li>Average minimum: $177,631</li>
    <li>Average maximum: $268,097</li>
    <li>Top of disclosed range: $624,170 (Red Hat)</li>
</ul>

<p>The average minimum and average maximum tell you what a typical VP role posts as a band: roughly $178K floor, $268K ceiling. The median sits closer to the floor than the ceiling, which means the distribution is right-skewed. A small number of very senior VP roles drag the average up. The typical VP is closer to $150K base than to $200K.</p>

<h2>What Drives the Spread</h2>

<p>Three factors move VP of partnerships pay more than anything else.</p>

<p>One: company stage. A Series B startup hiring its first VP of partnerships pays $150K to $180K base with significant equity. A public company hiring a VP of partnerships for an existing team pays $220K to $280K base with much smaller equity. Both roles are called "VP of partnerships." They are different jobs.</p>

<p>Two: program scope. Some VP of partnerships roles cover only technology partnerships (ISVs, integrations, marketplaces). Others cover the full channel motion (resellers, MSPs, agencies, SIs). Full-stack VP roles pay more because the operational and political surface area is larger.</p>

<p>Three: ecosystem authority. The highest-paid VP of partnerships roles in our dataset (Red Hat, Visa, Teads, Perforce) are ecosystem leaders, not channel leaders. The job is to own a category-defining ecosystem that other companies plug into. That is a different shape of role than running a reseller program, and the pay reflects it.</p>

<h2>The Top Roles</h2>

<p>The highest-paying VP of partnerships postings in our 2026 data:</p>

<ol>
    <li>Vice President, Global Cloud Partnerships, Red Hat: $367K to $624K</li>
    <li>VP US Agency Partnerships, Teads: $300K to $500K</li>
    <li>Vice President, Partner Ecosystem, Perforce Software: $225K to $500K</li>
    <li>Vice President, U.S. Retail Merchant Partnerships, Visa: $219K to $452K</li>
</ol>

<p>The pattern is consistent. Cloud, payments, and ecosystem are the three categories that pay the most for VP-level partnership leadership. Channel sales in traditional B2B SaaS pays VP base in the $200K to $250K range, which is real money but not the ceiling.</p>

<h2>How to Read a VP Posting Before You Take the Call</h2>

<p>Four signals matter more than the headline title.</p>

<p>The team size. "First partnerships hire" and "leading a team of 12" are not the same job. The first costs more in soul and less in salary. Ask early.</p>

<p>The reporting line. VP of partnerships reporting to the CRO is a sales-adjacent role. VP of partnerships reporting to the CEO is usually a strategic role with longer time horizons and broader scope. The CEO-reporting versions tend to pay more in equity and less in cash.</p>

<p>The revenue target. Many VP of partnerships roles do not carry a direct quota. They own influenced revenue, partner-sourced pipeline, or program metrics. The roles that do carry a hard direct quota tend to pay more cash, less equity, and have shorter average tenure.</p>

<p>The category. A VP of cloud partnerships at a company hiring 40 cloud partners is operating in a mature category with playbooks. A VP of AI partnerships at a B2B SaaS company is operating in a category that did not exist 18 months ago. Both can be the right move. They reward different skills.</p>

<h2>VP vs. Head of Partnerships</h2>

<p>Worth flagging the title fork. Our dataset includes 17 "Head of Partnerships" postings alongside the 50 VP postings. The Head of role has a $169K average minimum and $222K average maximum, which puts it slightly below the VP band.</p>

<p>The Head of title usually maps to one of two situations. Either the role is the same scope as a VP but the company is too early to use the VP title, or it is a senior IC role with limited team management responsibility. The first version is a VP role waiting for a promotion. The second is a senior individual contributor with director-level pay and team responsibility.</p>

<p>Asking "is this a Head of role on the way to VP, or a senior IC role with broader scope?" usually surfaces which version you are looking at.</p>

<h2>SVP and Above</h2>

<p>SVP-level partnership roles are rare in our dataset. We tracked 6 postings, with a $235K average minimum and $313K average maximum. The median is $273,500. These roles cluster at large enterprise companies (Visa, ADP, Red Hat) and typically carry global scope.</p>

<p>For most working partner leaders, SVP is the top of the visible ladder. Above SVP, partnerships work tends to fold into broader Chief Revenue Officer or Chief Strategy Officer roles. The few partnership-specific C-level roles that do exist (Chief Ecosystem Officer, Chief Alliances Officer) are not yet common enough to show up in volume in posting data.</p>

<h2>How to Use This</h2>

<p>If you are interviewing for a VP of partnerships role:</p>

<p>The $178K-to-$268K average band is your floor and ceiling. Below the floor is almost always a Head of role mis-labeled as VP. Above the ceiling, you should be having an equity conversation, not a base conversation.</p>

<p>If the role is a first hire, expect the base to come in at the floor of the band. Push hard on equity, the equity refresh schedule, and the path to a real team budget. The cash will not move much. The equity should.</p>

<p>If the role is replacing a previous VP, ask why they left. Partnership VPs have shorter tenure than most other GTM leadership roles. The reasons are usually structural (no team, no budget, no executive air cover) rather than individual. Diagnose the structural problem before you sign.</p>

<p>If you are not sure whether the role is at VP level, look at the budget. VP of partnerships roles with a real partner program typically have a 6 to 7 figure annual budget for MDF, events, and partner ops headcount. If there is no budget, the role is a senior IC role with a VP title.</p>
""",
        "faq": [
            ("What is the median base salary for a VP of partnerships in 2026?",
             "The median base salary for VP of partnerships postings in our 2026 dataset is $150,000, based on 50 disclosed roles. The average minimum is $178,000 and average maximum is $268,000. Top-of-market roles at Red Hat, Visa, and similar enterprise companies clear $400,000 base in some cases."),
            ("Why is there such a wide pay spread for VP of partnerships?",
             "Three factors drive the spread: company stage (Series B first hire vs. public-company VP managing an existing team), program scope (technology partnerships only vs. full channel motion), and ecosystem authority (running an ecosystem that others plug into pays significantly more than running a reseller program)."),
            ("What is the difference between VP of partnerships and Head of Partnerships?",
             "Head of Partnerships averages slightly lower ($169K minimum, $222K maximum) than VP. The Head of title usually indicates either a VP-scope role at a company too early to use the VP title, or a senior individual contributor role with limited team responsibility. Asking about team size, budget, and reporting line clarifies which version you are looking at."),
            ("Which industries pay the most for VP of partnerships roles?",
             "Cloud infrastructure (Red Hat, AWS partners), payments and fintech (Visa, ADP), and platform ecosystem roles (Perforce, Teads) sit at the top of the pay distribution. Traditional B2B SaaS channel leadership pays in the $200K to $250K base range, which is solid but not the ceiling."),
        ],
        "related_articles": ["state-of-partner-manager-compensation-2026", "entry-level-channel-roles-2026"],
        "internal_links": [
            ("/salary/by-seniority/", "All seniority bands"),
            ("/salary/vs-account-executive/", "VP partnerships vs. AE comp"),
            ("/glossary/alliance-manager/", "Alliance manager defined"),
        ],
    },
    {
        "slug": "entry-level-channel-roles-2026",
        "title": "Entry-Level Partner Manager Roles",
        "description": "What 58 entry-level partner manager job postings show: $67K median base, the metros that hire most, and how the first two years shape your career trajectory.",
        "date_published": "2026-05-14",
        "word_count": 1450,
        "category": "Careers",
        "summary": "Entry-level partner roles are scarcer than mid-level. Here is what the 58 we tracked say about how to get in and where to start.",
        "body": """
<p>Partnerships is not an entry-level field for most people. The 1,304 partner manager and channel roles we track in 2026 break down as 58 entry-level postings, 252 mid-level, 128 senior, 124 director, 50 VP, and a handful of SVP and Head of roles. Entry-level is about 4.4 percent of the disclosed market.</p>

<p>That ratio is unusual. Most B2B GTM functions hire entry-level at 20 to 30 percent of total roles. Partnerships hires entry-level at a fraction of that, and the people who get in tend to enter through one of a few specific paths.</p>

<p>This piece is for anyone trying to start a partnerships career: recent graduates, sales development reps eyeing a lateral move, or operations people trying to break into partner work. We walk through the 58 disclosed entry-level postings and what the data says about how to get the first job.</p>

<h2>The Pay Floor</h2>

<p>Entry-level partner roles in our 2026 dataset:</p>

<ul>
    <li>Sample size: 58 postings</li>
    <li>Median base: $67,000</li>
    <li>Average minimum: $76,000</li>
    <li>Average maximum: $104,000</li>
    <li>Top of disclosed range: $124,000</li>
</ul>

<p>The median base is $67K. The average band spans $76K to $104K, which is wider than you might expect for entry-level. That is because the dataset includes both true entry-level partner coordinator roles (mid-$50K to mid-$70K) and "associate partner manager" roles that are more like junior partner manager seats with full P&L responsibility (mid-$80K to low-$120K).</p>

<p>The two roles look similar on a job board. They are not the same job. A partner coordinator is operational support: scheduling, deal registration data entry, partner portal admin. An associate partner manager owns partner relationships, even if for smaller partners. Pay reflects the difference.</p>

<h2>Where Entry-Level Hires Cluster</h2>

<p>Entry-level partner roles are not evenly distributed by metro. They concentrate in three places.</p>

<p>New York hires the most entry-level partner managers in our dataset, followed by San Francisco. Together those two markets account for roughly 35 percent of disclosed entry-level postings. Remote roles make up another large chunk, particularly at AI-native companies and at SaaS companies whose partner programs are still small enough to hire generalists who can grow into the function.</p>

<p>Three observations on geography for entry-level candidates:</p>

<p>First, the major hubs (NYC, SF, Boston, Austin) have the most postings but also the most candidates. Competition is high and offers tend to come in at or slightly below the median.</p>

<p>Second, secondary metros (Chicago, Denver, DC) have fewer postings but also less candidate density. Median pay is lower but the path from offer to senior promotion is sometimes faster because there is less internal bench.</p>

<p>Third, fully remote entry-level partner roles exist but are rare. Most companies prefer to onboard entry-level partner staff in person. If you take a remote entry-level role, push for clear quarterly travel to HQ, because partner work is relationship-heavy and remote entry-level partner managers without face time stall out faster than direct sales remote hires.</p>

<h2>The Paths In</h2>

<p>From watching career moves into partnerships at this level, four common paths show up.</p>

<p>Path one: SDR or BDR to partner manager. Sales development reps who have spent 12 to 24 months sourcing pipeline for direct sales sometimes move laterally into partner roles. The skill overlap is real (outreach, qualification, relationship building) and the pay step is usually positive (entry-level partner pays slightly more than SDR). The risk is moving into a function where the feedback loops are slower and the path to AE-level OTE is less clear.</p>

<p>Path two: Customer success to partner success. Customer success reps with strong relationship skills and process discipline are often pulled into partner success or junior partner manager roles. The transition is smooth because the day-to-day is similar (managing accounts, running QBRs, expanding adoption) but with partner organizations instead of direct customers.</p>

<p>Path three: Operations to partner operations to partner manager. Sales ops or revenue ops people sometimes route through partner ops on the way to becoming a partner manager. The benefit is deep understanding of how partner programs work mechanically (PRM, deal registration, attribution). The risk is getting stuck in a back-office role without making the move to partner-facing work.</p>

<p>Path four: Recent graduate hired as partner coordinator. Some MBA programs and undergraduate sales programs feed directly into partnerships, particularly at larger tech companies (Salesforce, Microsoft, HubSpot, AWS) that run formal partner development programs. This is the rarest path because the seats are limited, but it pays well and offers the cleanest training.</p>

<h2>The First Two Years</h2>

<p>What you do in your first 24 months as an entry-level partner manager shapes the next decade more than in most GTM roles. The market does not have a clean lateral move at the senior IC level if your first two years are weak. Three things to focus on.</p>

<p>Own a meaningful partner. Even if you start as a coordinator or junior PM, push to own at least one partner relationship end to end. Track the influenced or sourced pipeline they produce. Write it up in your performance reviews. That number becomes your story when you interview for a mid-level role 18 to 24 months in.</p>

<p>Learn the Salesforce stack cold. Partner work runs in Salesforce at most companies. Knowing how deal registration objects work, how partner attribution is captured, and how to pull a clean partner-sourced pipeline report puts you ahead of mid-level partner managers who never learned the operational layer.</p>

<p>Build a network outside your company. Partnerships is a small world. The senior partner leaders you will want references from in five years are the ones you meet at events, on Slack communities, or through LinkedIn relationships built early. Joining the Partnership Leaders community or attending one of the major partnerships conferences (PartnerHacker, Catalyst, SaaStr Partners track) in your first two years is high-leverage.</p>

<h2>What to Avoid</h2>

<p>Two patterns that hurt entry-level partner managers in our experience.</p>

<p>Taking a partner role at a company with no partner program. A common trap: a startup hires its "first partnerships person" at the entry level. The reality is that building a partner program from scratch requires senior judgment about partner strategy, program design, and ecosystem positioning. An entry-level hire in that seat usually fails not because they are unqualified but because the role itself was misdesigned.</p>

<p>Staying too long in a coordinator role. Partner coordinators who do not transition to owning partner relationships within 18 to 24 months tend to get pigeonholed as operations specialists. The move from coordinator to junior partner manager is often internal but requires explicit conversation with your manager. If your company will not promote you into a relationship-owning role on a reasonable timeline, leave.</p>

<h2>The Trajectory</h2>

<p>The data shows a clear pay trajectory for partner managers who navigate the first two years well. The median jumps from $67K (entry-level) to $98K (mid-level) to $140K (senior IC) over roughly six to seven years. That trajectory is faster than direct sales AE in many cases, mostly because partner manager seats become harder to fill at the senior level and demand outpaces supply.</p>

<p>If you make it past the first two years, the rest of the career is more predictable. Getting in is the hard part.</p>
""",
        "faq": [
            ("What is the entry-level partner manager salary in 2026?",
             "The median base salary for entry-level partner manager and channel roles in 2026 is $67,000, based on 58 disclosed postings in our dataset. The average band runs $76,000 to $104,000, with the spread reflecting the difference between partner coordinator roles (lower end) and associate partner manager roles (higher end)."),
            ("How hard is it to break into partnerships?",
             "Harder than most B2B GTM functions. Entry-level postings are about 4.4 percent of the partner manager market in our 2026 data, compared to 20 to 30 percent in roles like direct sales. The most common paths in are SDR or BDR lateral moves, customer success transitions, partner ops to partner manager moves, and formal new-grad programs at larger tech companies."),
            ("Where do most entry-level partner managers get hired?",
             "New York and San Francisco lead the entry-level partner hiring volume, together accounting for roughly 35 percent of disclosed postings. Remote entry-level roles exist but are rare; most companies prefer to onboard entry-level partner staff in person because the work is relationship-heavy."),
            ("What is the typical career trajectory from entry-level partner manager?",
             "Median base moves from $67K (entry-level) to $98K (mid-level) to $140K (senior IC) over six to seven years for partner managers who own partner relationships in their first two years. The first two years are the most fragile part of the path. After that, the rest of the trajectory is more predictable."),
        ],
        "related_articles": ["state-of-partner-manager-compensation-2026", "vp-of-partnerships-compensation"],
        "internal_links": [
            ("/careers/", "All career guides"),
            ("/careers/how-to-become-partner-manager/", "How to become a partner manager"),
            ("/salary/by-seniority/", "Pay by seniority"),
        ],
    },
    {
        "slug": "partner-sourced-vs-partner-influenced-revenue",
        "title": "Partner Sourced vs. Influenced Revenue",
        "description": "Partner-sourced and partner-influenced revenue look similar on a slide. They drive different comp, hiring, and program design. Here is how to tell them apart.",
        "date_published": "2026-05-14",
        "word_count": 1550,
        "category": "Strategy",
        "summary": "The most consequential metric in partnerships is also the most often confused. Sourced and influenced are not interchangeable. Treating them as such will misprice your career.",
        "body": """
<p>Most partnership programs report a number that sounds something like "partners drove $40 million of revenue last quarter." The number is rarely wrong. It is almost always misleading.</p>

<p>Inside that $40 million, two very different things are usually being added together. Partner-sourced revenue is deals that started with a partner. Partner-influenced revenue is deals that the partner accelerated or expanded but did not originate. Both matter. They do not mean the same thing. And the people who build careers in partnerships need to understand which one their employer actually rewards.</p>

<h2>The Definitions</h2>

<p>Partner-sourced revenue: revenue from deals where a partner brought the opportunity to the vendor. The customer would not have engaged the vendor without the partner. The partner is the originating channel for the opportunity. Attribution is straightforward when deal registration is enforced: the partner registered the deal, the deal closed, the partner gets sourced credit.</p>

<p>Partner-influenced revenue: revenue from deals where a partner played a material role but was not the originator. The customer might have come in through a direct sales motion, an inbound form fill, or a different partner. Then a partner (often a technology partner, SI, or agency) contributed to the deal closing or expanding. Attribution is fuzzier because multiple parties touched the deal.</p>

<p>The two metrics sometimes overlap. A deal can be both partner-sourced (Partner A originated it) and partner-influenced (Partner B helped close it). Sophisticated partner programs track both and report them separately.</p>

<h2>Why the Distinction Matters</h2>

<p>Three reasons the difference between sourced and influenced reshapes a partnerships career.</p>

<p>One: comp structure. Partner managers who own sourced revenue typically have a quota number that looks like an AE quota: a hard dollar target with variable comp tied to attainment. Partner managers who own influenced revenue more often have a softer KPI structure: program metrics, partner satisfaction, integration count. The first version pays more in variable and pushes pipeline velocity. The second pays more stable base and pushes program building.</p>

<p>Two: hiring profile. Companies that lead with sourced revenue tend to hire partner managers who came from direct sales. They want closers. Companies that lead with influenced revenue hire partner managers from product, strategy, or program management backgrounds. They want builders. If you are interviewing, knowing which metric the company optimizes for will tell you which version of yourself you need to show up as.</p>

<p>Three: program design. A program optimized for sourced revenue invests heavily in deal registration enforcement, partner training on pitch and qualification, and tight CRM integration. A program optimized for influenced revenue invests in technology integrations, marketplace listings, joint marketing, and customer success collaboration. The day-to-day work of a partner manager looks very different across the two.</p>

<h2>The Attribution Problem</h2>

<p>Influenced revenue is harder to defend on a board slide because attribution is messy. Sourced revenue has a clean rule: the partner registered the deal, full stop. Influenced revenue has fuzzy edges. Did the partner influence the deal, or did they show up at one demo and the AE would have closed it anyway? Most companies that report influenced revenue use rules like "if a partner was involved in three or more touchpoints" or "if a partner's integration was part of the technical evaluation." The rules vary by company, which makes cross-company benchmarking on influenced revenue unreliable.</p>

<p>This matters for partner managers because influenced revenue claims get audited by CFOs more than sourced revenue claims do. If you are running an influenced revenue program, build the attribution rules early and be ready to defend them. If you cannot defend them, the program eventually gets de-funded.</p>

<h2>Which One Should You Optimize For?</h2>

<p>If you are a partner leader designing a program, the answer depends on the product and the buying motion.</p>

<p>Optimize for sourced revenue when: the product sells through resellers or agencies to a buyer the vendor cannot reach directly, the deal size is large enough that partner margin is meaningful, and the buyer relies on the partner for ongoing implementation or service. Most channel-led programs in B2B infrastructure, security, and enterprise software fit this profile.</p>

<p>Optimize for influenced revenue when: the product is a horizontal SaaS tool that integrates with other tools, the buyer is already engaging the vendor directly, and partners primarily help the deal close faster or expand wider. Most modern SaaS partner programs fit this profile.</p>

<p>Most mature programs report both, but emphasize one. Knowing which one your employer emphasizes (sourced or influenced) is more diagnostic than the headline "$40 million from partners" number.</p>

<h2>How to Ask in an Interview</h2>

<p>Four questions to ask when interviewing for a partner manager role:</p>

<ul>
    <li>What percentage of your partner program revenue is sourced versus influenced?</li>
    <li>How do you define a partner-sourced deal? Specifically, what triggers sourced credit?</li>
    <li>How do you define a partner-influenced deal? What are the attribution rules?</li>
    <li>Which one am I going to be measured on, and what does the variable comp structure look like?</li>
</ul>

<p>The answers will tell you within ten minutes whether the program is mature, whether the attribution holds up, and which kind of work the role actually involves. A hiring manager who cannot answer these questions clearly is signaling that the program is not yet operationalized, which is not necessarily bad. It just means you should price the offer differently.</p>

<h2>The Career Trajectory Implications</h2>

<p>Partner managers who build a career around sourced revenue tend to move within the channel sales track: partner manager, senior partner manager, director of channel sales, VP of channels. The career is closer to a direct sales leadership career, with more emphasis on quota attainment, partner recruitment, and deal velocity.</p>

<p>Partner managers who build a career around influenced revenue tend to move into platform or ecosystem roles: technology partner manager, head of integrations, VP of platform partnerships, VP of ecosystem. The career emphasizes product fluency, ecosystem strategy, and program design more than direct quota carrying.</p>

<p>Both tracks pay well. The VP of channels and VP of ecosystem roles both sit in the $200K to $300K base range for mature programs. The day-to-day work is different enough that switching tracks mid-career is harder than switching companies within the same track.</p>

<h2>The Honest Disclosure</h2>

<p>One thing most partnership leaders will not say in public: a lot of "influenced revenue" reporting is fiction. The rules are loose, the data sources are inconsistent, and the politics of partner credit attribution mean influenced numbers get inflated to justify program budgets.</p>

<p>The CFO eventually figures this out. When it happens, partner programs that lean too heavily on influenced revenue claims get cut or restructured. The partner programs that survive long-term are the ones that build defensible sourced revenue alongside the influenced metric. Sourced revenue is harder to fake. It is also harder to grow. The companies that take it seriously build durable partner organizations.</p>

<p>If you are evaluating a partner role, ask for the sourced number first. The influenced number tells you what the program wants to be. The sourced number tells you what it actually is.</p>
""",
        "faq": [
            ("What is the difference between partner-sourced and partner-influenced revenue?",
             "Partner-sourced revenue is from deals where a partner brought the opportunity to the vendor; the customer would not have engaged without the partner. Partner-influenced revenue is from deals where a partner played a material role but did not originate the opportunity. Sourced is cleaner to attribute. Influenced is fuzzier and harder to defend to a CFO."),
            ("Which metric should a partner program optimize for?",
             "Sourced revenue when the product sells through resellers or agencies to buyers the vendor cannot reach directly. Influenced revenue when the product is horizontal SaaS that integrates with other tools and partners help direct deals close faster. Most mature programs report both but emphasize one."),
            ("How do CFOs evaluate partner-influenced revenue claims?",
             "Skeptically. Influenced revenue attribution rules vary by company and often inflate over time. CFOs audit influenced claims more aggressively than sourced claims. Programs that rely too heavily on influenced revenue claims tend to get cut when budgets tighten. Programs that build defensible sourced revenue alongside influenced metrics survive longer."),
            ("How does the metric affect a partner manager career?",
             "Partner managers who own sourced revenue follow a track closer to direct sales leadership: more variable comp, harder quotas, faster pipeline velocity expectations. Partner managers who own influenced revenue follow a track closer to product or program management: more stable base, softer KPIs, longer-cycle program building. Both tracks can reach VP level but emphasize different skills."),
        ],
        "related_articles": ["state-of-partner-manager-compensation-2026", "prm-adoption-channel-tool-stack"],
        "internal_links": [
            ("/glossary/sourced-revenue/", "Sourced revenue defined"),
            ("/glossary/influenced-revenue/", "Influenced revenue defined"),
            ("/glossary/deal-registration/", "Deal registration"),
            ("/glossary/partner-attach-rate/", "Partner attach rate"),
        ],
    },
    {
        "slug": "salary-disclosure-in-partnerships-roles",
        "title": "Why 35% of Partner Jobs Hide Salary",
        "description": "Out of 1,304 partner manager postings tracked in 2026, 452 do not disclose a salary band. We dig into who is hiding pay, why, and what to do about it.",
        "date_published": "2026-05-14",
        "word_count": 1400,
        "category": "Compensation",
        "summary": "One in three partner manager job postings does not disclose a salary band. The reasons tell you a lot about what kind of offer you should expect.",
        "body": """
<p>Salary transparency laws have spread across the US since 2022. California, Colorado, New York, Washington, and Illinois all require disclosure in postings for roles that can be performed in those states. Most large tech employers post nationally and end up applying the rules across the board.</p>

<p>Even so, 35 percent of the 1,304 partner manager and channel roles we tracked in 2026 do not disclose a salary band. That gap is larger than for direct sales roles (around 25 percent hidden) and meaningfully larger than for engineering roles (about 18 percent hidden) in equivalent datasets.</p>

<p>This piece looks at who hides pay in partnerships, what the patterns are, and how to read the absence of a band when you see it.</p>

<h2>The Headline Number</h2>

<p>Of 1,304 partner manager roles in our 2026 dataset, 852 disclosed a salary band. The remaining 452, or 34.7 percent, did not. That includes:</p>

<ul>
    <li>Roles posted in jurisdictions that require disclosure but listed no band</li>
    <li>Roles posted with a band so wide it effectively communicates nothing ($60K to $250K)</li>
    <li>Roles that link to an external careers page where the band is buried or absent</li>
    <li>Roles posted in non-required jurisdictions with no band</li>
</ul>

<p>We counted all of the above as undisclosed for the analysis. A band wider than 2.5x the floor (for example, $80K to $250K) was treated as a non-disclosure because it does not give a candidate useful anchoring information.</p>

<h2>Who Hides Pay</h2>

<p>The non-disclosure pattern clusters in three places.</p>

<p>Enterprise companies hide pay more than startups. Roles at companies with more than 5,000 employees were undisclosed 41 percent of the time in our dataset, versus 28 percent at companies under 500 employees. The enterprise pattern is partly geography (more global postings that fall outside US disclosure rules) and partly internal politics (large companies have wider internal bands and prefer not to anchor candidates publicly).</p>

<p>Senior roles hide pay more than junior roles. VP and director-level postings are undisclosed about 45 percent of the time. Entry-level and mid-level postings are undisclosed about 25 percent of the time. The senior end has more negotiating room, and companies prefer to anchor on the candidate's current comp rather than a public band.</p>

<p>Recruiter-led postings hide pay more than direct-from-employer postings. Roles posted by external recruiting firms or staffing agencies are undisclosed 53 percent of the time. Direct postings on a company's careers page are undisclosed 27 percent of the time. Recruiters benefit from longer negotiation runways and tend to keep the band off the public-facing posting.</p>

<h2>Why It Matters</h2>

<p>Three practical consequences for partner manager candidates.</p>

<p>One: undisclosed roles tend to anchor low. When a hiring manager opens with "what is your current comp?" and the candidate has no public band to negotiate against, the offer almost always lands within 10 percent of the current number. Disclosed roles, by contrast, anchor closer to the median of the public band. The difference can be $20K to $40K of annual base pay over the life of the role.</p>

<p>Two: undisclosed roles correlate with longer interview cycles. Without a public anchor, both sides spend more time triangulating. Our anecdotal data (not in the formal dataset) suggests undisclosed roles take roughly 30 percent longer from first call to offer.</p>

<p>Three: undisclosed roles correlate with lower offer acceptance rates. Candidates who reach offer stage on undisclosed roles walk away more often, either because the offer comes in below market or because the lack of transparency raised flags about the broader compensation culture.</p>

<h2>How to Read a Missing Band</h2>

<p>Four signals to look for when a posting does not include a band.</p>

<p>Check the company's other postings. If their engineering roles have a band but their partner manager roles do not, that is a strong signal that the partner role is being handled differently, often with less internal compensation rigor. Hidden bands at companies that otherwise disclose suggest the partner role is being treated as an off-band hire.</p>

<p>Check the work location. If the posting allows California, Colorado, or New York and still has no band, the company is potentially out of compliance. Some companies handle this by limiting the posting to states without disclosure laws, which is itself a signal worth noting.</p>

<p>Check whether a recruiter is in the loop. If the application routes through a third-party recruiter and the band is not on the posting, the recruiter almost certainly knows the range and is choosing not to disclose. Ask early. A recruiter who refuses to share the range until offer stage is a flag.</p>

<p>Check Glassdoor and Levels.fyi. These sites often surface internal compensation data even when public postings hide it. The data is imperfect, but for senior partner roles at named companies, you can usually triangulate within 10 to 15 percent of the actual range.</p>

<h2>How to Push Back</h2>

<p>If you are deep into an interview process and the band is still hidden, two scripts that work.</p>

<p>Script one (mid-process): "I want to make sure we are aligned on compensation before we both invest more time. Could you share the range for this role so I can make sure expectations are realistic?" This is a clean ask. Most hiring managers will share the range once you are past the first round. Ones who will not are signaling something.</p>

<p>Script two (at offer stage if anchored low): "The offer is below the range I have seen for comparable roles at companies in your space. I want to make this work, but I would need to see X base or Y total comp. Can you go back and revisit?" Be specific about what you have seen and where. Vague pushback gets vague responses.</p>

<p>The companies that handle these conversations well tend to be the ones worth working for. Companies that respond to a compensation question with deflection or pressure are signaling something about the broader culture you should pay attention to.</p>

<h2>The Honest View</h2>

<p>Hidden bands are usually not malicious. They are usually a sign that the company has not finished operationalizing its compensation process, that the role is going through a recruiter who benefits from opacity, or that the role is at a level where the company prefers individualized negotiation.</p>

<p>None of those reasons are good for candidates. They all suggest that the offer you eventually receive will be below what a disclosed-band company would have offered for the same work. If you are interviewing for partner manager roles in 2026, treat a missing band as a piece of pricing information, not as a neutral fact. It is telling you something about the offer before the offer arrives.</p>
""",
        "faq": [
            ("How many partner manager job postings hide salary in 2026?",
             "About 35 percent. Of 1,304 partner manager and channel roles tracked in our 2026 dataset, 452 did not disclose a usable salary band. That is a higher hidden-rate than direct sales (around 25 percent) or engineering roles (about 18 percent) in equivalent datasets."),
            ("Which kinds of partner manager postings are most likely to hide pay?",
             "Enterprise roles (companies over 5,000 employees), senior roles (VP and director-level), and recruiter-led postings hide pay most often. Direct postings from smaller companies and entry-level roles are the most likely to include a band."),
            ("Should I apply to a partner manager role that hides salary?",
             "It depends on how strong the rest of the signal is, but go in with eyes open. Undisclosed roles tend to anchor offers within 10 percent of your current comp, take 30 percent longer to close, and have lower offer acceptance rates. Ask for the range early in the interview process. A hiring manager who refuses to share until offer stage is telling you something."),
            ("Is it legal for partner manager roles in California or New York to hide salary?",
             "Generally no, for roles that can be performed in those states. Some companies handle the disclosure requirement by limiting where the role can be performed. If you see a posting that should be subject to disclosure rules and the band is missing, the company is either out of compliance or has structured the role to avoid the rule. Both are worth noting."),
        ],
        "related_articles": ["state-of-partner-manager-compensation-2026", "vp-of-partnerships-compensation"],
        "internal_links": [
            ("/salary/methodology/", "How we collect salary data"),
            ("/salary/", "All salary benchmarks"),
            ("/careers/", "Career guides"),
        ],
    },
]


# ---------------------------------------------------------------------------
# Article renderer
# ---------------------------------------------------------------------------

def _render_article(article, all_articles_by_slug):
    """Render a single article page at /insights/{slug}/."""
    slug = article["slug"]
    title = article["title"]
    description = article["description"]
    date_pub = article["date_published"]
    word_count = article["word_count"]

    canonical = f"/insights/{slug}/"
    crumbs = [("Home", "/"), ("Insights", "/insights/"), (title, None)]
    bc_html = breadcrumb_html(crumbs)

    # Internal links sidebar (related data destinations)
    links_html = ""
    for href, label in article.get("internal_links", []):
        links_html += f'<li><a href="{href}">{label}</a></li>\n'

    sidebar_html = ""
    if links_html:
        sidebar_html = f'''<aside class="article-sidebar">
    <h3>Related data on this site</h3>
    <ul class="article-sidebar-links">
        {links_html}
    </ul>
</aside>'''

    # Related articles
    related_html = ""
    related_slugs = article.get("related_articles", [])
    related_cards = ""
    for rs in related_slugs:
        if rs in all_articles_by_slug:
            r = all_articles_by_slug[rs]
            related_cards += f'''<a href="/insights/{r["slug"]}/" class="preview-card">
    <h3>{r["title"]}</h3>
    <p>{r["summary"]}</p>
    <span class="preview-link">Read more &rarr;</span>
</a>
'''
    if related_cards:
        related_html = f'''<section class="related-articles">
    <h2>Related Insights</h2>
    <div class="preview-grid">
        {related_cards}
    </div>
</section>'''

    # FAQ section
    faq_pairs = article.get("faq", [])
    faq_section_html = ""
    faq_schema_str = ""
    if faq_pairs:
        faq_section_html = faq_html(faq_pairs)
        faq_schema_str = get_faq_schema(faq_pairs)

    # Schema
    bc_schema = get_breadcrumb_schema(crumbs)
    art_schema = get_article_schema(title, description, slug, date_pub, word_count, url_path=canonical)
    combined_schema = bc_schema + art_schema + faq_schema_str

    # Date display
    date_display = date_pub  # ISO format is fine for now

    body = f'''{bc_html}
<article class="insight-article">
    <header class="article-header">
        <div class="article-meta">
            <span class="article-category">{article["category"]}</span>
            <span class="article-date">Published {date_display}</span>
        </div>
        <h1>{title}</h1>
        <p class="article-summary">{article["summary"]}</p>
    </header>
    <div class="article-layout">
        <div class="article-content">
            {article["body"]}
        </div>
        {sidebar_html}
    </div>
    {faq_section_html}
    {related_html}
</article>
'''
    body += newsletter_cta_html("Weekly analysis for partner and channel professionals.")

    page = get_page_wrapper(
        title=title,
        description=description,
        canonical_path=canonical,
        body_content=body,
        active_path="/insights/",
        extra_head=combined_schema,
        body_class="page-inner",
    )
    write_page(f"insights/{slug}/index.html", page)
    print(f"  Built: insights/{slug}/index.html")


# ---------------------------------------------------------------------------
# Dynamic insights hub
# ---------------------------------------------------------------------------

def build_insights_hub_dynamic(articles):
    """Replace the Coming Soon hub with a list of published articles."""
    title = "Partner & Channel Sales Insights"
    description = (
        "Data-grounded analysis of partner manager compensation, PRM adoption,"
        " ecosystem strategy, and the channel sales market. Updated weekly with new posts."
    )

    crumbs = [("Home", "/"), ("Insights", None)]
    bc_html = breadcrumb_html(crumbs)

    # Sort articles newest first
    sorted_articles = sorted(articles, key=lambda a: a["date_published"], reverse=True)

    cards = ""
    for a in sorted_articles:
        cards += f'''<a href="/insights/{a["slug"]}/" class="insight-card">
    <div class="insight-card-meta">
        <span class="insight-card-category">{a["category"]}</span>
        <span class="insight-card-date">{a["date_published"]}</span>
    </div>
    <h2 class="insight-card-title">{a["title"]}</h2>
    <p class="insight-card-summary">{a["summary"]}</p>
    <span class="insight-card-link">Read article &rarr;</span>
</a>
'''

    body = f'''{bc_html}
<section class="page-header">
    <h1>Partner &amp; Channel Sales Insights</h1>
    <p class="page-header-subtitle">Analysis grounded in 1,304 partner manager job postings, 852 disclosed salaries, and tool adoption data refreshed weekly.</p>
</section>
<div class="container">

    <p>This is where we publish analysis on the partner and channel sales market. Every piece is grounded in data from job postings, salary benchmarks, tool adoption patterns, and program operating metrics.</p>

    <p>No thought leadership for the sake of thought leadership. If we publish something here, it is because the data says something worth paying attention to.</p>

    <div class="insight-cards-grid">
        {cards}
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
    print(f"  Built: insights/index.html (dynamic, {len(articles)} articles)")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def build_all_articles():
    """Build all article pages plus the dynamic insights hub."""
    print("\n  Building insights articles...")

    all_by_slug = {a["slug"]: a for a in ARTICLES}

    build_insights_hub_dynamic(ARTICLES)

    for a in ARTICLES:
        _render_article(a, all_by_slug)

    print(f"  Built: {len(ARTICLES)} insights articles")
