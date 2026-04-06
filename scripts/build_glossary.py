# scripts/build_glossary.py
# Glossary section page generators. 45 term pages + index.
# Called by build.py. Uses templates.py for HTML shell.

import os
import re
import json

from nav_config import *
from templates import (get_page_wrapper, write_page, get_breadcrumb_schema,
                       get_faq_schema, breadcrumb_html, newsletter_cta_html,
                       faq_html)


# ---------------------------------------------------------------------------
# Term data: slug, display name, short definition, long body, FAQ pairs,
# related term slugs
# ---------------------------------------------------------------------------

GLOSSARY_TERMS = [
    {
        "slug": "prm-partner-relationship-management",
        "term": "PRM (Partner Relationship Management)",
        "short": "Software that helps companies recruit, onboard, enable, and manage channel partners at scale.",
        "body": """<p>Partner Relationship Management (PRM) is a category of software built to manage the full lifecycle of a company's partner relationships. It covers partner recruitment, onboarding, training, deal registration, lead distribution, MDF allocation, and performance tracking in a single system.</p>

<p>PRM emerged because CRM platforms were never designed for indirect sales. A CRM tracks your direct sales team's pipeline. A PRM tracks the external organizations that sell on your behalf. The data models are fundamentally different. Partners need portal access, co-branded collateral, certification paths, and commission structures that CRM cannot handle natively.</p>

<p>Most PRM platforms include a partner portal where partners log in to register deals, access marketing materials, complete training modules, and view their performance dashboards. The vendor side gets visibility into partner activity, pipeline contribution, and program health metrics.</p>

<p>Companies typically adopt PRM when they pass 20 to 50 active partners. Below that threshold, spreadsheets and email work. Above it, the manual overhead becomes unsustainable. Deal registration conflicts increase, training compliance drops, and partner engagement data becomes impossible to track.</p>

<p>Leading PRM vendors include Impartner, PartnerStack, Allbound, Channeltivity, and Magentrix. Enterprise buyers often look at Salesforce Experience Cloud or custom-built portals. Pricing ranges from $500 per month for SMB programs to six figures annually for enterprise deployments with hundreds of partners.</p>""",
        "faq": [
            ("What is the difference between PRM and CRM?", "CRM manages your direct sales team's pipeline and customer relationships. PRM manages external partner organizations, including their portal access, deal registration, training, and commissions. Most mature partner programs use both, integrated via API."),
            ("When should a company invest in PRM?", "When you have more than 20 active partners and manual processes start breaking. Signs include missed deal registrations, partner complaints about collateral access, and inability to report on partner-sourced revenue accurately."),
            ("How much does PRM software cost?", "Entry-level PRM starts around $500 per month. Mid-market solutions run $1,000 to $5,000 per month. Enterprise PRM with custom integrations and hundreds of partners can exceed $100,000 annually."),
        ],
        "related": ["partner-portal", "deal-registration", "partner-enablement", "partner-tiering"],
    },
    {
        "slug": "channel-sales",
        "term": "Channel Sales",
        "short": "A go-to-market strategy where companies sell through third-party partners instead of (or alongside) a direct sales force.",
        "body": """<p>Channel sales is a distribution model where a company sells its products or services through third-party partners rather than exclusively through its own sales team. These partners can be resellers, distributors, managed service providers, system integrators, or referral partners.</p>

<p>The core advantage of channel sales is leverage. A company with 10 direct reps can reach a limited number of accounts. That same company with 200 channel partners can cover thousands of accounts simultaneously, using the partners' existing customer relationships and local market knowledge.</p>

<p>Channel sales models vary in structure. In a one-tier model, the vendor sells directly to partners who sell to end customers. In a two-tier model, the vendor sells through distributors who then supply resellers. The choice depends on deal complexity, geographic coverage needs, and the vendor's ability to manage partner relationships at scale.</p>

<p>The economics differ from direct sales. Instead of paying salaries and commissions to an internal team, the vendor shares margin with partners through discounts, rebates, or referral fees. The trade-off is lower per-deal margin in exchange for broader reach and lower fixed costs.</p>

<p>Channel sales works best for products that benefit from local implementation, ongoing service, or industry-specific customization. Enterprise software, IT infrastructure, cybersecurity, and telecommunications have historically relied on channel sales. SaaS companies increasingly adopt hybrid models that blend direct and channel motions.</p>""",
        "faq": [
            ("What is the difference between channel sales and direct sales?", "Direct sales uses an internal team to sell to customers. Channel sales uses external partners. Most companies use a hybrid of both, with direct handling enterprise accounts and channel covering mid-market and SMB."),
            ("What percentage of revenue should come from channel sales?", "It varies by industry and company stage. Mature tech companies often see 50 to 80 percent of revenue through channel. Early-stage companies typically start with direct and add channel once the product and sales motion are proven."),
            ("What are the biggest challenges in channel sales?", "Channel conflict with direct sales, maintaining partner engagement, ensuring consistent messaging, and accurately attributing revenue to partner influence are the most common challenges."),
        ],
        "related": ["direct-sales", "indirect-sales", "channel-strategy", "channel-conflict", "channel-manager"],
    },
    {
        "slug": "direct-sales",
        "term": "Direct Sales",
        "short": "Selling products or services through an in-house sales team without third-party intermediaries.",
        "body": """<p>Direct sales is a go-to-market model where a company's own employees sell products or services to end customers without intermediaries. The company controls the entire sales process from prospecting through closing and post-sale support.</p>

<p>The direct model offers full control over pricing, messaging, customer experience, and deal velocity. Sales leadership can train, coach, and monitor reps in real time. Pipeline data flows directly into the company's CRM without the latency and data quality issues common in channel models.</p>

<p>Direct sales is the default starting point for most companies. Before you can enable partners to sell your product, you need to prove the sales motion works internally. This means establishing repeatable messaging, pricing that converts, and a sales cycle that delivers predictable revenue.</p>

<p>The limitation of direct sales is scale. Hiring, training, and retaining sales reps is expensive. Each rep has a finite number of accounts they can work. Geographic expansion requires either remote reps or physical offices. For companies selling into fragmented markets with thousands of potential buyers, direct alone cannot achieve full coverage.</p>

<p>Most B2B companies eventually adopt a hybrid approach, using direct sales for strategic and enterprise accounts while routing mid-market and SMB opportunities through channel partners. The key is defining clear rules of engagement so the two motions complement rather than compete with each other.</p>""",
        "faq": [
            ("When is direct sales better than channel sales?", "Direct is better for complex enterprise deals requiring deep product expertise, during early-stage product-market fit when the sales motion is still being refined, and for strategic accounts where relationship control matters most."),
            ("What is the average cost of a direct sales rep?", "Fully loaded cost (base salary, commission, benefits, tools, management overhead) for a B2B SaaS AE in the US ranges from $150,000 to $300,000 per year depending on seniority and market."),
        ],
        "related": ["channel-sales", "indirect-sales", "channel-conflict", "channel-strategy"],
    },
    {
        "slug": "indirect-sales",
        "term": "Indirect Sales",
        "short": "Any revenue generated through third-party partners, distributors, or affiliates rather than the company's own sales team.",
        "body": """<p>Indirect sales encompasses all revenue that flows through third parties rather than a company's internal sales organization. This includes reseller transactions, distributor sales, referral commissions, marketplace purchases, and any deal where an external partner plays a material role in the sale.</p>

<p>The term is broader than channel sales. While channel sales specifically refers to a structured partner program, indirect sales captures any transaction where the vendor is not the entity closing the deal with the end customer. An affiliate link on a blog that drives a purchase is indirect sales. A systems integrator bundling your software into a larger implementation is indirect sales.</p>

<p>Companies track indirect sales as a percentage of total revenue to understand their go-to-market mix. A healthy ratio depends on the business model. Infrastructure companies like Cisco or HPE may see 80 percent or more through indirect. A PLG SaaS startup might start at zero and gradually build to 20 or 30 percent as partner programs mature.</p>

<p>The challenge with indirect sales is attribution. When a customer interacts with both a partner and a direct rep before purchasing, who gets credit? This question drives significant debate and has spawned metrics like influenced revenue and sourced revenue to differentiate levels of partner contribution.</p>

<p>Measuring indirect sales accurately requires integration between PRM, CRM, and financial systems. Without clean data flows, companies undercount partner contribution, which in turn undermines investment in the partner program.</p>""",
        "faq": [
            ("How do you measure indirect sales?", "Track sourced revenue (partner originated the deal) and influenced revenue (partner accelerated or expanded an existing deal) separately. Integrate PRM and CRM data to avoid double-counting or undercounting."),
            ("What industries rely most on indirect sales?", "IT infrastructure, cybersecurity, telecommunications, and enterprise software have the highest indirect sales ratios, often exceeding 60 percent of total revenue."),
        ],
        "related": ["channel-sales", "direct-sales", "sourced-revenue", "influenced-revenue", "revenue-share"],
    },
    {
        "slug": "partner-ecosystem",
        "term": "Partner Ecosystem",
        "short": "The network of companies, integrations, and relationships that surround a product or platform and extend its value to customers.",
        "body": """<p>A partner ecosystem is the interconnected network of companies that work together around a shared platform, product, or market opportunity. It includes technology partners who integrate, service partners who implement, resellers who distribute, and referral partners who recommend.</p>

<p>The ecosystem concept goes beyond transactional channel partnerships. In a true ecosystem, partners create value for each other, not just for the platform vendor. A Salesforce partner, for example, benefits from the entire AppExchange ecosystem because more integrations make Salesforce stickier, which means more customers, which means more implementation work.</p>

<p>Building an ecosystem requires investment in APIs, documentation, partner programs, and community. The platform vendor creates the foundation. Partners build on top of it. Over time, the ecosystem becomes a competitive moat because switching away from the platform means losing access to the entire partner network.</p>

<p>Ecosystem health is measured by metrics like the number of active partners, integration depth, partner-sourced revenue, and customer retention rates for accounts with partner-built integrations. Healthy ecosystems show network effects: each new partner makes the platform more valuable for every other partner.</p>

<p>The partner ecosystem model has accelerated in SaaS because cloud APIs make integration easier and marketplace distribution reduces friction. Companies like AWS, Microsoft, Salesforce, and HubSpot have built ecosystems with thousands of partners that generate billions in indirect revenue annually.</p>""",
        "faq": [
            ("What makes a partner ecosystem successful?", "Strong APIs and documentation, a clear partner program with fair economics, marketplace distribution, community engagement, and executive commitment to ecosystem as a strategic priority rather than a cost center."),
            ("How long does it take to build a partner ecosystem?", "A basic partner program can launch in 3 to 6 months. Building a self-sustaining ecosystem with network effects typically takes 2 to 5 years of consistent investment."),
        ],
        "related": ["ecosystem-led-growth", "partner-led-growth", "nearbound", "technology-partner", "marketplace"],
    },
    {
        "slug": "technology-partner",
        "term": "Technology Partner",
        "short": "A company that integrates its product with another company's platform to deliver combined value to shared customers.",
        "body": """<p>A technology partner is a company that builds an integration between its product and another company's platform. The integration creates combined value that neither product delivers alone. For example, a data enrichment tool that integrates with a CRM gives CRM users access to enriched contact data without leaving their workflow.</p>

<p>Technology partnerships differ from reseller or referral relationships. The partnership is product-level, not sales-level. The integration itself is the value. Sales collaboration may follow, but it starts with the products working together.</p>

<p>Most technology partnerships are formalized through a vendor's technology partner program. The vendor provides API access, sandbox environments, co-marketing support, and marketplace listing opportunities. In return, the technology partner builds and maintains the integration, markets it to their own customer base, and often pays a listing fee or revenue share for marketplace transactions.</p>

<p>For the platform vendor, technology partnerships extend the product's capabilities without building everything in-house. For the technology partner, the integration provides distribution through the platform's customer base and marketplace. Customers benefit from pre-built integrations that reduce implementation time.</p>

<p>The strongest technology partnerships involve shared customers. When both companies serve the same buyer, the integration solves a real workflow problem. Partnerships built on theory rather than customer demand rarely produce meaningful results.</p>""",
        "faq": [
            ("How do technology partnerships generate revenue?", "Revenue comes through marketplace transactions (direct), co-sell referrals (influence), and reduced churn for shared customers (retention). Some technology partners also receive MDF or co-marketing funds from the platform vendor."),
            ("What makes a good technology partner fit?", "Overlapping customer base, complementary (not competitive) products, strong API capabilities on both sides, and mutual willingness to invest in go-to-market collaboration beyond just building the integration."),
        ],
        "related": ["partner-ecosystem", "isv-partner", "marketplace", "co-selling", "co-marketing"],
    },
    {
        "slug": "isv-partner",
        "term": "ISV Partner",
        "short": "An Independent Software Vendor that builds and sells software on or alongside another company's platform.",
        "body": """<p>An ISV (Independent Software Vendor) partner is a software company that has built its product to work on, alongside, or within another company's platform. The term is most commonly used in cloud and enterprise software ecosystems, where ISVs build applications that extend a platform's capabilities.</p>

<p>ISV partnerships are a subset of technology partnerships, but the term carries specific connotations. ISV usually implies the partner is a software company (not a services firm), that they sell their own product (not just integrate), and that there is a formalized program governing the relationship.</p>

<p>Cloud providers like AWS, Microsoft Azure, and Google Cloud run large ISV partner programs. These programs give ISVs technical resources to build cloud-native applications, co-sell support to reach enterprise buyers, and marketplace listing to simplify procurement. In return, ISVs drive consumption of cloud infrastructure and expand the platform's solution breadth.</p>

<p>For ISVs, the value proposition is distribution. Listing on AWS Marketplace, for instance, allows enterprise buyers to purchase the ISV's product using their existing cloud commit. This reduces procurement friction and can shorten sales cycles significantly.</p>

<p>ISV partner programs typically include tiers based on technical certification, customer success stories, and revenue contribution. Higher tiers unlock more co-sell resources, dedicated partner development managers, and premium marketplace placement.</p>""",
        "faq": [
            ("What does ISV stand for?", "ISV stands for Independent Software Vendor. It refers to a company that develops and sells software, as opposed to a hardware company, services firm, or platform provider."),
            ("How do ISV partner programs work?", "ISVs apply to a platform's partner program, build a certified integration, list on the marketplace, and then collaborate with the platform's sales team on co-sell opportunities. The platform typically takes a revenue share on marketplace transactions."),
        ],
        "related": ["technology-partner", "marketplace", "cloud-marketplace", "listing-fee", "revenue-share"],
    },
    {
        "slug": "agency-partner",
        "term": "Agency Partner",
        "short": "A marketing, design, or consulting agency that implements or resells a company's product as part of client engagements.",
        "body": """<p>An agency partner is a marketing, design, development, or consulting firm that recommends, implements, or resells a company's product as part of its client work. The agency's primary business is services, and the product is a tool they use to deliver results for their clients.</p>

<p>Agency partnerships are common in the marketing technology and CRM space. HubSpot's Solutions Partner Program, for example, has thousands of agencies that implement HubSpot for their clients. These agencies generate revenue from services (strategy, setup, content creation) and the platform vendor benefits from customer acquisition and retention.</p>

<p>The economics of agency partnerships work differently than reseller relationships. Agencies rarely take a margin on the software itself. Instead, they earn implementation fees, ongoing retainer revenue for managed services, and sometimes referral commissions from the vendor. The vendor gets a customer who is properly onboarded and more likely to succeed.</p>

<p>Agency partners bring domain expertise that product vendors cannot replicate at scale. A marketing agency understands campaign strategy, content creation, and performance optimization. The product vendor understands the platform. Together, they deliver better outcomes than either could alone.</p>

<p>Challenges in agency partnerships include quality control (the vendor's brand is affected by the agency's work), certification requirements (ensuring agencies are technically competent), and conflict when agencies work with competing platforms for different clients.</p>""",
        "faq": [
            ("How do agency partner programs differ from reseller programs?", "Agency programs focus on services and implementation. The agency earns from client retainers and project fees. Reseller programs focus on product distribution with the partner earning margin on the sale itself."),
            ("What does a good agency partner program include?", "Technical certification, co-marketing support, lead sharing, implementation playbooks, a partner directory for customer referrals, and tiered benefits based on certification level and customer count."),
        ],
        "related": ["reseller", "si-systems-integrator", "partner-enablement", "partner-tiering", "co-marketing"],
    },
    {
        "slug": "reseller",
        "term": "Reseller",
        "short": "A company that purchases products from a vendor and sells them to end customers, typically adding some value through bundling, support, or local presence.",
        "body": """<p>A reseller is a company that buys a vendor's product (often at a discount) and sells it to end customers at a markup. The reseller takes ownership of the customer relationship for the transaction, handles billing, and often provides first-line support or implementation services.</p>

<p>Reseller models have deep roots in IT distribution. Before cloud delivery, most enterprise software and hardware reached customers through networks of resellers who maintained local inventory, provided technical support, and managed ongoing customer relationships.</p>

<p>In the SaaS era, the reseller model has evolved. Instead of buying and stocking physical products, SaaS resellers manage licenses on behalf of customers, handle billing and procurement, and bundle the software with implementation and managed services. The economics shift from product margin to service margin.</p>

<p>Vendors use resellers to reach markets they cannot cover with direct sales. A US-based SaaS company might use resellers in Japan, Brazil, or Germany where local language, business customs, and regulatory requirements make direct sales impractical.</p>

<p>Reseller agreements define pricing (typically 20 to 40 percent discount off list), territory rights, minimum commitments, support responsibilities, and brand usage guidelines. The best reseller relationships are mutually dependent: the vendor needs the reseller's customer access, and the reseller needs the vendor's product to build their services practice around.</p>""",
        "faq": [
            ("What is the typical reseller margin?", "Reseller discounts range from 20 to 40 percent off list price, depending on volume, partner tier, and the complexity of services the reseller provides. Higher-touch products with implementation requirements tend to offer larger margins."),
            ("What is the difference between a reseller and a distributor?", "A reseller sells to end customers. A distributor sells to resellers. Distributors add a logistics and credit layer between the vendor and the reseller network. In two-tier distribution, the flow is vendor to distributor to reseller to customer."),
        ],
        "related": ["var-value-added-reseller", "distributor", "two-tier-distribution", "channel-sales", "white-label"],
    },
    {
        "slug": "var-value-added-reseller",
        "term": "VAR (Value Added Reseller)",
        "short": "A reseller that adds services, customization, or complementary products before selling to the end customer.",
        "body": """<p>A Value Added Reseller (VAR) is a company that takes a vendor's product, enhances it with additional services, integrations, or customizations, and sells the combined solution to end customers. The "value add" distinguishes VARs from pure resellers who simply pass through the product with minimal modification.</p>

<p>The value that VARs add takes many forms: custom configuration, integration with existing systems, training and onboarding, ongoing managed services, or bundling complementary products into a complete solution. A VAR selling a CRM platform might add data migration, workflow customization, and ongoing admin support.</p>

<p>VARs are particularly important in industries where products require significant customization to deliver value. Healthcare IT, manufacturing, government, and financial services all depend on VARs who understand the industry-specific requirements and can tailor generic platforms to meet compliance, workflow, and integration needs.</p>

<p>The VAR model creates deeper customer relationships than pure resale. Because the VAR provides ongoing services, they become embedded in the customer's operations. This creates recurring revenue for the VAR and sticky customer relationships for the vendor.</p>

<p>For vendors, VARs extend reach into vertical markets and customer segments that require specialized knowledge. The trade-off is less control over the customer experience and dependence on the VAR's technical capabilities and service quality.</p>""",
        "faq": [
            ("What is the difference between a VAR and a regular reseller?", "A regular reseller primarily handles distribution. A VAR adds meaningful services like customization, integration, training, or managed support. VARs typically earn higher margins because they deliver more value to the end customer."),
            ("Are VARs still relevant in the SaaS era?", "Yes. While the resale component has shifted to license management, the services component is more important than ever. SaaS products still require implementation, integration, and ongoing optimization that VARs provide."),
        ],
        "related": ["reseller", "si-systems-integrator", "msp-managed-service-provider", "channel-sales"],
    },
    {
        "slug": "msp-managed-service-provider",
        "term": "MSP (Managed Service Provider)",
        "short": "A company that remotely manages a customer's IT infrastructure, security, or business applications on an ongoing basis.",
        "body": """<p>A Managed Service Provider (MSP) is a company that takes over the day-to-day management of a customer's technology environment. This includes IT infrastructure monitoring, security management, cloud administration, backup and disaster recovery, and help desk support, all delivered remotely on a subscription basis.</p>

<p>MSPs operate on a recurring revenue model. Instead of project-based billing, they charge monthly or annual fees for ongoing management. This aligns their incentives with the customer: fewer problems mean lower costs for the MSP and better uptime for the customer.</p>

<p>For technology vendors, MSPs are a powerful channel because they control their customers' technology stack. When an MSP recommends a vendor's product, that recommendation carries weight because the MSP will be the one implementing and managing it. MSPs prioritize tools that are easy to deploy at scale and generate reliable margins.</p>

<p>The MSP market has consolidated significantly. Small break-fix IT shops have given way to larger managed services firms that offer security operations (MSSP), cloud management, and compliance services alongside traditional IT support.</p>

<p>Vendor-MSP partnerships require different program structures than traditional reseller programs. MSPs need multi-tenant management tools, aggregate billing, and per-device or per-user pricing models. Vendors that make it easy for MSPs to deploy and manage their product across hundreds of client environments win MSP loyalty.</p>""",
        "faq": [
            ("What is the difference between an MSP and a VAR?", "A VAR sells and implements solutions on a project basis. An MSP provides ongoing management and monitoring of technology environments for a recurring fee. Many companies operate as both, selling solutions (VAR) and then managing them long-term (MSP)."),
            ("How do MSPs make money from vendor partnerships?", "MSPs earn monthly management fees from end customers, margin on licenses they resell, and sometimes referral or rebate payments from vendors. The recurring management fee is typically the largest revenue component."),
        ],
        "related": ["var-value-added-reseller", "reseller", "channel-sales", "two-tier-distribution"],
    },
    {
        "slug": "si-systems-integrator",
        "term": "SI (Systems Integrator)",
        "short": "A consulting or services firm that brings together multiple technology products into a unified solution for enterprise customers.",
        "body": """<p>A Systems Integrator (SI) is a services firm that combines multiple technology products, platforms, and custom development into a cohesive solution for enterprise customers. SIs handle the complex work of making different systems talk to each other, migrating data, configuring workflows, and ensuring the combined solution meets business requirements.</p>

<p>SIs range from global firms like Accenture, Deloitte, and Wipro to regional consultancies with deep expertise in specific verticals. Global SIs (GSIs) work on multi-million dollar transformation projects. Smaller SIs focus on mid-market implementations that require significant customization but not the scale of a GSI engagement.</p>

<p>For technology vendors, SI partnerships are high-leverage relationships. A single SI engagement can drive hundreds of thousands of dollars in software licenses as part of a larger implementation. SIs also influence technology selection early in the buying process, often before the vendor's sales team is involved.</p>

<p>SI partnerships require investment from both sides. The vendor provides training, certification, sandbox environments, and often dedicated alliance managers. The SI commits to building a practice around the vendor's technology, hiring and training consultants, and developing implementation methodologies.</p>

<p>The economics are service-driven. SIs earn from implementation fees, not product margin. A typical enterprise implementation might involve $200,000 in software licenses and $1 million or more in SI services. This ratio means SIs prioritize vendors whose products generate the most services revenue.</p>""",
        "faq": [
            ("What is the difference between an SI and a VAR?", "VARs add value through bundling and configuration. SIs handle complex, multi-system integration projects that require custom development, data migration, and enterprise-scale implementation. SIs typically work on larger, more technically complex engagements."),
            ("How do you build relationships with systems integrators?", "Start with a single practice lead who sees opportunity in your technology. Provide training and certification. Fund a proof-of-concept engagement. SI partnerships are built one successful project at a time."),
        ],
        "related": ["var-value-added-reseller", "technology-partner", "partner-enablement", "alliance-manager"],
    },
    {
        "slug": "oem-partner",
        "term": "OEM Partner",
        "short": "A company that embeds another vendor's technology into its own product and sells it under its own brand.",
        "body": """<p>An OEM (Original Equipment Manufacturer) partner is a company that licenses another vendor's technology and integrates it directly into their own product. The end customer sees a single product from the OEM, often without knowing that a component comes from an external vendor.</p>

<p>OEM partnerships are common in both hardware and software. A laptop manufacturer embeds an operating system. A cybersecurity platform embeds a threat intelligence feed. A business application embeds a reporting engine. In each case, the OEM partner packages the technology as part of a larger offering.</p>

<p>The economics of OEM deals differ from resale. OEM pricing is typically 60 to 80 percent below list price because the vendor is getting high-volume distribution without sales or support costs. The OEM handles all customer interaction. The vendor provides the technology and API support.</p>

<p>OEM agreements are complex legal documents covering licensing terms, branding restrictions, support escalation procedures, and revenue commitments. Most include minimum annual commitments to ensure the vendor gets a baseline return on the integration effort.</p>

<p>For vendors, OEM partnerships provide scale distribution and revenue predictability. For OEM partners, embedded technology accelerates product development. Building a reporting engine from scratch might take two years. Licensing one takes two months. The trade-off is dependency on an external vendor for a core component.</p>""",
        "faq": [
            ("What is the difference between OEM and white label?", "OEM embeds technology as a component inside a larger product. White label takes a complete product and rebrands it. With OEM, the customer interacts with the OEM partner's product. With white label, the customer interacts with a fully rebranded version of the vendor's product."),
            ("How is OEM pricing structured?", "OEM pricing typically runs 60 to 80 percent below list price. Deals include minimum annual commitments and volume-based tiers. Revenue is predictable but per-unit margin is low, so OEM works for vendors seeking scale distribution."),
        ],
        "related": ["white-label", "private-label", "technology-partner", "revenue-share"],
    },
    {
        "slug": "referral-partner",
        "term": "Referral Partner",
        "short": "A company or individual that sends qualified leads to a vendor in exchange for a commission or fee on closed deals.",
        "body": """<p>A referral partner is any individual or organization that introduces potential buyers to a vendor in exchange for compensation when those introductions result in closed business. Referral partnerships are the simplest form of partner relationship: the partner identifies an opportunity, makes an introduction, and earns a fee if the deal closes.</p>

<p>Referral partners do not sell the product, handle implementation, or provide ongoing support. Their role is limited to the introduction. After the handoff, the vendor's direct sales team takes over the relationship and drives the deal to close.</p>

<p>Compensation models vary. Fixed referral fees (for example, $500 per closed deal) work for transactional products. Percentage-based commissions (typically 10 to 20 percent of the first year's contract value) align better with higher-value enterprise sales. Some programs offer recurring commissions for the life of the customer.</p>

<p>Referral partnerships appeal to individuals and organizations that have strong networks but no desire to build a sales or implementation practice. Management consultants, industry analysts, complementary software vendors, and professional services firms often participate as referral partners.</p>

<p>The operational overhead is low. Referral programs require a tracking system (often built into PRM), clear rules about what qualifies as a valid referral, and a defined window (typically 30 to 90 days) during which the referral must convert to earn the commission. Well-designed programs also include partner portals where referral partners can submit leads and track deal progress.</p>""",
        "faq": [
            ("How much do referral partners earn?", "Referral commissions typically range from 10 to 20 percent of the first year's deal value. Some programs offer flat fees ($250 to $2,000 per closed deal) or recurring commissions for the customer's lifetime."),
            ("What is the difference between a referral partner and a reseller?", "A referral partner makes an introduction and steps away. A reseller owns the customer relationship, handles billing, and often provides support. Referral requires minimal operational commitment but earns lower compensation."),
        ],
        "related": ["deal-registration", "channel-sales", "partner-portal", "sourced-revenue"],
    },
    {
        "slug": "co-selling",
        "term": "Co-Selling",
        "short": "A collaborative sales motion where a vendor and partner jointly engage a prospect, sharing account intelligence and selling effort.",
        "body": """<p>Co-selling is a go-to-market motion where a vendor's sales team and a partner's sales team jointly pursue a shared opportunity. Both sides bring account intelligence, relationships, and expertise to the deal. The goal is to combine forces to win accounts that neither could close alone.</p>

<p>Co-selling differs from referral partnerships in a critical way: both parties are actively involved in the sales process. A referral partner hands off a lead. A co-selling partner joins calls, shares account insights, provides technical validation, and helps navigate the buying committee.</p>

<p>The co-selling motion was popularized by ecosystem platforms like Crossbeam and Reveal, which enable partners to identify overlapping accounts and prospects without exposing their full customer lists. Once overlap is identified, partner managers coordinate joint outreach.</p>

<p>Effective co-selling requires clear rules of engagement. Who leads the account? How is revenue attributed? What information can be shared? Without these agreements, co-sell attempts devolve into confusion about ownership and credit.</p>

<p>Cloud providers have formalized co-selling at scale. AWS, Microsoft, and Google all run co-sell programs where ISV partners submit opportunities that the cloud provider's sales team helps close. These programs work because the cloud provider has enterprise relationships and procurement influence that the ISV lacks independently.</p>""",
        "faq": [
            ("What is the difference between co-selling and co-marketing?", "Co-selling is joint sales engagement on specific deals. Co-marketing is joint promotion and demand generation. Co-marketing fills the top of the funnel. Co-selling converts specific opportunities in the middle and bottom of the funnel."),
            ("How do you measure co-selling success?", "Track co-sell influenced pipeline, co-sell win rates versus solo win rates, average deal size on co-sold deals, and time-to-close. Successful co-selling programs show higher win rates and larger deals than direct-only motions."),
        ],
        "related": ["co-marketing", "account-mapping", "partner-overlap", "nearbound", "deal-registration"],
    },
    {
        "slug": "co-marketing",
        "term": "Co-Marketing",
        "short": "Joint marketing activities between a vendor and partner to generate shared demand and brand awareness.",
        "body": """<p>Co-marketing is the practice of two companies collaborating on marketing activities to reach a larger audience than either could access alone. Common co-marketing activities include joint webinars, co-authored content, shared event sponsorships, co-branded landing pages, and joint case studies.</p>

<p>Co-marketing works because it gives each company access to the other's audience. A PRM vendor co-hosting a webinar with a CRM platform reaches CRM users who might need partner management. The CRM platform reaches PRM users who might upgrade their CRM. Both audiences are relevant to both companies.</p>

<p>Effective co-marketing requires audience alignment and equitable effort. The best campaigns feature complementary brands with overlapping buyer personas but non-competing products. When both companies promote equally, the combined reach can be three to five times what either achieves alone.</p>

<p>Many vendor partner programs fund co-marketing through Market Development Funds (MDF). Partners submit marketing plans, receive funding, execute the campaign, and report results. This structure ensures marketing spend aligns with the vendor's messaging while leveraging the partner's local market knowledge.</p>

<p>The biggest failure mode in co-marketing is unequal commitment. One company promotes heavily while the other does the minimum. Successful co-marketing requires a shared campaign plan, mutual promotion commitments, and shared metrics for measuring success.</p>""",
        "faq": [
            ("What are the most effective co-marketing activities?", "Joint webinars consistently produce the highest ROI for B2B co-marketing. Co-authored research reports, shared customer case studies, and joint event presence also perform well. The key is picking formats that naturally feature both brands."),
            ("How is co-marketing funded?", "Many vendor partner programs provide Market Development Funds (MDF) to support co-marketing. Partners can also split costs directly. Typical budgets range from $2,000 for a joint webinar to $50,000 or more for event sponsorships."),
        ],
        "related": ["co-selling", "mdf-market-development-funds", "through-channel-marketing", "partner-enablement"],
    },
    {
        "slug": "deal-registration",
        "term": "Deal Registration",
        "short": "A process where channel partners register sales opportunities with a vendor to protect their margin and establish deal ownership.",
        "body": """<p>Deal registration is a formal process where a channel partner notifies a vendor about a specific sales opportunity they are pursuing. Once approved, the partner receives protection on that deal, typically in the form of guaranteed discount pricing, priority over other partners, and protection from the vendor's direct sales team.</p>

<p>Deal registration exists to solve the free-rider problem in channel sales. Without it, a partner might invest weeks developing an opportunity only to have another partner (or the vendor's direct team) swoop in at the last minute with a lower price. Deal registration guarantees that the partner who found and developed the opportunity earns the margin.</p>

<p>A typical deal registration process works like this: the partner submits the customer name, opportunity details, estimated deal size, and expected close date through the vendor's PRM or partner portal. The vendor reviews the submission, checks for conflicts (like an existing direct opportunity), and either approves or rejects within a defined timeframe, usually 24 to 48 hours.</p>

<p>Approved registrations include an expiration window, commonly 90 days. If the deal does not close within that window, the registration expires and can be re-registered or opened to other partners.</p>

<p>Deal registration compliance is one of the most important factors in partner satisfaction. When vendors override or ignore registrations, trust erodes quickly. The best programs have clear rules, fast approval, and transparent conflict resolution processes that partners can rely on.</p>""",
        "faq": [
            ("Why is deal registration important for channel partners?", "It protects the partner's investment in developing an opportunity. Without registration, another partner or the vendor's direct team could undercut the price or claim the deal. Registration guarantees the partner earns margin on deals they source."),
            ("What happens when two partners register the same deal?", "Most programs use a first-to-register rule. The first partner to submit a valid registration gets deal protection. If both submit simultaneously, the vendor evaluates which partner has the stronger customer relationship."),
        ],
        "related": ["partner-portal", "channel-conflict", "prm-partner-relationship-management", "channel-sales"],
    },
    {
        "slug": "partner-portal",
        "term": "Partner Portal",
        "short": "A web-based platform where partners access training, marketing materials, deal registration, and performance dashboards.",
        "body": """<p>A partner portal is a dedicated web application where a vendor's channel partners go to access everything they need to sell, implement, and support the vendor's products. It serves as the central hub for the partner relationship, replacing the scattered emails, shared drives, and ad-hoc processes that small partner programs rely on.</p>

<p>Core partner portal features include deal registration, lead management, marketing content libraries, training and certification modules, co-branded collateral generators, performance dashboards, and commission tracking. Advanced portals add business planning tools, MDF request workflows, and community forums.</p>

<p>The quality of the partner portal directly affects partner engagement. Partners work with multiple vendors and will gravitate toward programs that make it easy to find information, register deals, and track performance. A slow, confusing, or outdated portal is one of the fastest ways to lose partner mindshare.</p>

<p>Partner portals are typically built on PRM platforms (Impartner, PartnerStack, Allbound) or as custom builds on Salesforce Experience Cloud, WordPress, or purpose-built applications. The build-versus-buy decision depends on partner program complexity and the vendor's technical resources.</p>

<p>Portal usage data provides valuable insights into partner health. Active partners log in regularly, download marketing materials, register deals, and complete training. Declining portal activity is an early warning sign of partner disengagement that partner success teams should monitor and address.</p>""",
        "faq": [
            ("What should a partner portal include at minimum?", "Deal registration, a marketing content library, training or certification modules, and a performance dashboard. These four features cover the core needs of any channel partner."),
            ("How do you improve partner portal adoption?", "Simplify the login process (SSO if possible), make the most-used features accessible within two clicks, send regular notifications about new content, and tie portal activity to partner tier advancement."),
        ],
        "related": ["prm-partner-relationship-management", "deal-registration", "partner-enablement", "partner-tiering"],
    },
    {
        "slug": "mdf-market-development-funds",
        "term": "MDF (Market Development Funds)",
        "short": "Vendor-provided funds that channel partners use for local marketing, demand generation, and brand awareness activities.",
        "body": """<p>Market Development Funds (MDF) are marketing budgets that vendors allocate to channel partners for joint demand generation activities. Partners use MDF to run local events, digital advertising campaigns, content marketing, and other activities that generate pipeline for the vendor's products in the partner's market.</p>

<p>MDF differs from co-op funds. Co-op funds are earned retroactively based on sales performance (for example, 2 percent of quarterly revenue). MDF is allocated proactively based on submitted marketing plans and is not directly tied to past sales. In practice, many companies use the terms interchangeably.</p>

<p>The MDF process typically works like this: a partner submits a marketing plan to the vendor describing the activity, target audience, budget, and expected results. The vendor reviews and approves the plan. The partner executes the activity, often using pre-approved vendor messaging and co-branded templates. After execution, the partner submits proof of performance (receipts, screenshots, lead lists) to receive reimbursement.</p>

<p>MDF management is one of the most operationally complex aspects of channel programs. Tracking allocations across hundreds of partners, processing claims, enforcing brand guidelines, and measuring ROI on marketing activities requires dedicated systems and staff.</p>

<p>The most common complaint from partners about MDF is the approval and reimbursement process being too slow or bureaucratic. Programs that make it easy for partners to propose, execute, and get reimbursed see significantly higher MDF utilization and marketing activity than those with complex multi-step approval chains.</p>""",
        "faq": [
            ("How much MDF do vendors typically allocate?", "MDF budgets vary widely. Small programs might offer $500 to $2,000 per partner per quarter. Large enterprise programs allocate millions annually across their partner base, with top-tier partners receiving $50,000 or more per quarter."),
            ("What can MDF funds be used for?", "Common uses include local events, digital advertising, content creation, trade show participation, direct mail campaigns, and webinars. Activities must typically generate leads or brand awareness for the vendor's products."),
        ],
        "related": ["co-marketing", "through-channel-marketing", "partner-tiering", "partner-enablement"],
    },
    {
        "slug": "partner-enablement",
        "term": "Partner Enablement",
        "short": "Training, tools, content, and support that help channel partners effectively sell, implement, and support a vendor's product.",
        "body": """<p>Partner enablement is the systematic effort to equip channel partners with everything they need to successfully sell and deliver a vendor's product. It covers sales training, technical certification, marketing content, demo environments, competitive battlecards, implementation guides, and ongoing support.</p>

<p>Enablement exists because partners are not employees. They did not go through your onboarding program, do not attend your all-hands meetings, and sell multiple vendors' products simultaneously. Your product competes for their attention with every other vendor in their portfolio. Effective enablement makes your product the easiest to sell and the most profitable to deliver.</p>

<p>The best enablement programs follow a structured path. New partners complete foundational training (product overview, value proposition, competitive positioning). They then advance through technical certification that validates implementation competency. Ongoing enablement covers product updates, new use cases, and market trends.</p>

<p>Content is the backbone of enablement. Partners need case studies to build credibility, ROI calculators to justify purchases, demo scripts to run effective presentations, and objection handling guides to navigate competitive situations. This content must be easy to find, always current, and available in co-brandable formats.</p>

<p>Measuring enablement effectiveness requires tracking certification completion rates, time to first deal for new partners, deal sizes for trained versus untrained partners, and partner satisfaction scores. The correlation between enablement engagement and revenue production is typically strong and provides justification for continued investment.</p>""",
        "faq": [
            ("What is the difference between partner enablement and partner onboarding?", "Onboarding is the initial phase of enablement focused on getting new partners productive. Enablement is the ongoing process of training, certifying, and supporting partners throughout the relationship. Onboarding is a subset of enablement."),
            ("How do you measure partner enablement ROI?", "Compare revenue per partner for enabled versus non-enabled partners, track time to first deal after certification, measure deal sizes, and survey partner satisfaction with enablement resources. Most programs see 2x to 4x revenue difference between fully enabled and non-enabled partners."),
        ],
        "related": ["partner-onboarding", "partner-portal", "partner-tiering", "prm-partner-relationship-management"],
    },
    {
        "slug": "channel-conflict",
        "term": "Channel Conflict",
        "short": "Friction that occurs when a vendor's direct sales team competes with channel partners for the same customer or deal.",
        "body": """<p>Channel conflict occurs when a vendor's sales channels compete with each other rather than collaborating. The most common form is direct-versus-channel conflict, where the vendor's internal sales team pursues the same customer that a channel partner is already working. But conflict also arises between partners competing for the same opportunity.</p>

<p>Channel conflict is the single biggest trust destroyer in partner programs. When a partner invests time developing an opportunity and then sees the vendor's direct team undercutting their price or claiming the deal, the partner stops investing effort. Repeated conflict drives partners to prioritize competing vendors who protect their deals.</p>

<p>Preventing conflict requires clear rules of engagement. These rules must define which accounts belong to direct sales, which belong to channel, and how to handle accounts where both are engaged. Deal registration is the primary mechanism for establishing ownership, but it only works when the vendor enforces it consistently.</p>

<p>Territory-based rules (direct handles accounts above a certain size; channel handles everything below) are the simplest approach but often create gray areas. Account-based rules (named accounts for direct; all others open to channel) provide more clarity but require ongoing list maintenance.</p>

<p>Some conflict is inevitable. The goal is not to eliminate it entirely but to have a fair, transparent resolution process. Partners accept that conflicts happen. They do not accept being blindsided by a direct sales rep who ignores their registration and offers a lower price.</p>""",
        "faq": [
            ("How do you prevent channel conflict?", "Implement deal registration with fast approval and consistent enforcement. Define clear rules of engagement between direct and channel sales. Create a conflict resolution process with a named escalation contact. Compensate direct reps for partner-sourced deals."),
            ("Why do direct sales reps cause channel conflict?", "Direct reps are compensated on their own quota. Without incentives to support channel deals, they may pursue the same accounts. Solving this requires comp plan changes that credit direct reps for partner-influenced revenue."),
        ],
        "related": ["deal-registration", "channel-sales", "direct-sales", "channel-strategy", "channel-manager"],
    },
    {
        "slug": "partner-tiering",
        "term": "Partner Tiering",
        "short": "A structured system that segments partners into levels (e.g., Silver, Gold, Platinum) based on performance, certification, and commitment.",
        "body": """<p>Partner tiering is a program structure that classifies partners into levels based on their investment in and performance with a vendor's products. Common tier names include Registered, Silver, Gold, and Platinum, though many programs use custom naming. Each tier comes with different benefits, requirements, and expectations.</p>

<p>Tiering serves two purposes. For partners, it creates a clear path for growth and investment. Higher tiers unlock better pricing, more MDF, priority deal registration, dedicated support, and co-marketing opportunities. For vendors, tiering segments the partner base so resources go to the partners most likely to produce results.</p>

<p>Tier requirements typically include a combination of revenue targets (close X dollars in annual sales), certification (maintain Y certified professionals), customer satisfaction (achieve Z CSAT scores), and business planning (submit an annual joint business plan). The best programs balance achievable requirements with meaningful differentiation between tiers.</p>

<p>A common mistake is creating too many tiers. When the difference between Silver and Gold is marginal, partners have no motivation to invest in advancement. Effective programs have three to four tiers with significant benefit jumps between them.</p>

<p>Annual tier reviews create accountability but should include grace periods for partners experiencing temporary setbacks. Demoting a strong partner because they missed a quarterly target by 5 percent damages the relationship more than it enforces standards.</p>""",
        "faq": [
            ("How many partner tiers should a program have?", "Three to four tiers work best for most programs. Fewer than three do not provide enough differentiation. More than five dilute the value of each tier and confuse partners about what they are working toward."),
            ("What benefits should top-tier partners receive?", "Best pricing and margins, dedicated partner manager, priority deal registration, increased MDF allocation, executive sponsorship, co-marketing support, early access to product roadmap, and logo placement in vendor marketing."),
        ],
        "related": ["partner-scorecard", "partner-enablement", "partner-portal", "mdf-market-development-funds"],
    },
    {
        "slug": "partner-scorecard",
        "term": "Partner Scorecard",
        "short": "A measurement framework that evaluates partner performance across revenue, enablement, customer success, and engagement metrics.",
        "body": """<p>A partner scorecard is a structured assessment tool that measures how well individual partners are performing against a defined set of criteria. It provides a data-driven alternative to subjective partner evaluations and creates transparency about what the vendor values in the partnership.</p>

<p>Typical scorecard metrics span four categories. Revenue metrics include sourced revenue, influenced revenue, deal count, and average deal size. Enablement metrics track certified staff count, training completion rates, and specialization achievements. Customer success metrics measure customer satisfaction, renewal rates, and support escalation frequency. Engagement metrics look at portal activity, marketing campaign participation, and business plan compliance.</p>

<p>Scorecards are commonly used to determine partner tier placement, allocate MDF budgets, and identify partners that need intervention. A partner with strong revenue but declining certification might need enablement investment. A partner with high certification but low revenue might need pipeline support.</p>

<p>The cadence matters. Quarterly scorecards provide enough frequency to catch trends without creating administrative burden. Monthly reviews are appropriate for top-tier partners with active business plans. Annual reviews are insufficient for managing a dynamic partner base.</p>

<p>Effective scorecards are transparent. Partners should be able to see their own scores, understand the calculation methodology, and know what they need to do to improve. Hidden scoring systems breed distrust and undermine the scorecard's ability to drive partner behavior.</p>""",
        "faq": [
            ("What metrics should a partner scorecard include?", "Revenue (sourced and influenced), certification and training completion, customer satisfaction scores, portal engagement, deal registration activity, and marketing campaign participation. Weight metrics based on what matters most to your program."),
            ("How often should partner scorecards be reviewed?", "Quarterly for most partners. Monthly for top-tier partners with joint business plans. Share results with partner managers and partner leadership to ensure alignment on improvement areas."),
        ],
        "related": ["partner-tiering", "sourced-revenue", "influenced-revenue", "partner-attach-rate"],
    },
    {
        "slug": "through-channel-marketing",
        "term": "Through-Channel Marketing",
        "short": "Marketing programs and automation that enable channel partners to execute vendor-approved campaigns in their local markets.",
        "body": """<p>Through-channel marketing (TCM) is the practice of enabling channel partners to run marketing campaigns on behalf of a vendor, using vendor-provided content, templates, and automation tools. The vendor creates the marketing playbook; partners execute it in their local markets with their own audience and brand.</p>

<p>TCM platforms (also called through-channel marketing automation or TCMA) provide the technology layer. Partners log into a portal, select a campaign template, customize it with their logo and contact information, and launch it. The platform handles email delivery, landing pages, lead capture, and reporting. The vendor maintains brand control while partners execute locally.</p>

<p>The fundamental challenge TCM solves is the marketing capability gap. Most channel partners are not sophisticated marketers. They lack the staff, tools, and expertise to create effective campaigns. By providing ready-to-run campaigns, vendors make it possible for partners to generate demand without building a marketing function.</p>

<p>TCM is different from co-marketing. Co-marketing involves two companies actively collaborating on a shared campaign. TCM is more scalable but less customized: the vendor builds a campaign once and distributes it to hundreds of partners who execute with minimal modification.</p>

<p>Adoption is the primary challenge. Even with easy-to-use platforms, many partners do not execute TCM campaigns consistently. Successful programs combine good technology with partner marketing support, regular campaign suggestions, and MDF to offset partner execution costs.</p>""",
        "faq": [
            ("What is through-channel marketing automation?", "TCMA platforms let partners select, customize, and launch vendor-created marketing campaigns from a portal. The platform handles email delivery, landing pages, and lead capture while maintaining vendor brand guidelines."),
            ("How do you increase partner adoption of TCM programs?", "Simplify the platform, provide pre-built campaigns that require minimal customization, offer MDF to offset costs, share success stories from partners who have generated leads, and have partner marketing managers provide hands-on support."),
        ],
        "related": ["co-marketing", "mdf-market-development-funds", "partner-enablement", "partner-portal"],
    },
    {
        "slug": "partner-led-growth",
        "term": "Partner-Led Growth",
        "short": "A go-to-market strategy where partner relationships are the primary engine for customer acquisition, expansion, and retention.",
        "body": """<p>Partner-led growth (PLG in the partnerships context, not to be confused with product-led growth) is a go-to-market strategy that positions partner relationships as the primary driver of revenue. Instead of treating partners as a supplementary channel, partner-led companies build their entire growth motion around ecosystem collaboration.</p>

<p>In a partner-led model, the majority of new customers come through partner referrals, co-sell motions, or marketplace transactions. Product roadmaps prioritize integrations that partners request. Marketing budgets fund co-marketing and through-channel campaigns. Sales enablement trains reps to sell with partners, not just to partners.</p>

<p>Partner-led growth gained traction as customer acquisition costs through direct and digital channels continued to rise. When a trusted partner recommends your product, the buyer arrives with built-in trust, shorter evaluation cycles, and higher close rates. This makes partner-sourced deals economically attractive even after paying partner commissions.</p>

<p>The shift to partner-led growth requires organizational changes. Sales compensation must reward partner collaboration, not just direct quota. Product teams must treat partner integrations as first-class features. Marketing must allocate meaningful budget to partner co-marketing rather than treating it as an afterthought.</p>

<p>Companies like HubSpot, Shopify, and Salesforce have demonstrated partner-led growth at scale. Their partner ecosystems contribute 40 to 70 percent of new customer acquisition and significantly reduce churn through deeper product integration and services support.</p>""",
        "faq": [
            ("How does partner-led growth differ from traditional channel sales?", "Traditional channel treats partners as a distribution layer. Partner-led growth makes the ecosystem the primary growth engine, influencing product, marketing, sales, and customer success strategy. It is a company-wide operating model, not just a sales motion."),
            ("What metrics indicate a company is successfully partner-led?", "Over 40 percent of revenue sourced or influenced by partners, partner-attached customers showing lower churn, partner integrations increasing product adoption, and ecosystem contribution growing faster than direct."),
        ],
        "related": ["ecosystem-led-growth", "nearbound", "partner-ecosystem", "sourced-revenue", "partner-attach-rate"],
    },
    {
        "slug": "nearbound",
        "term": "Nearbound",
        "short": "A go-to-market strategy that uses partner ecosystem data and relationships to identify, reach, and convert prospects more effectively.",
        "body": """<p>Nearbound is a go-to-market approach that leverages the trust and data in a company's partner ecosystem to reach buyers more effectively than cold outbound or inbound alone. The core idea: your partners already have relationships with your ideal customers. By mapping those overlaps and coordinating outreach, you can warm up prospects before ever making contact.</p>

<p>The term was coined and popularized by Jared Fuller and the team at Reveal (formerly Crossbeam). It sits alongside inbound (customers find you) and outbound (you find customers) as a third category: nearbound (your partners help you find and win customers).</p>

<p>Nearbound starts with account mapping. By securely comparing customer and prospect lists with partners, companies identify accounts where a partner already has a relationship. Instead of cold outreach to that account, the sales rep can ask the partner for a warm introduction or intelligence about the buying committee.</p>

<p>The data shows that nearbound works. Deals where a partner provides an introduction or account intel close at two to three times the rate of cold outbound. The reason is trust transfer: when a partner the buyer already trusts recommends a product, the barrier to engagement drops significantly.</p>

<p>Operationalizing nearbound requires technology (ecosystem platforms for account mapping), process (workflows for requesting and providing partner intel), and culture (sales teams that view partners as assets rather than competitors for commission). Companies adopting nearbound typically start with their top 10 partners and a single use case before scaling.</p>""",
        "faq": [
            ("What is the difference between nearbound and outbound?", "Outbound is cold: you reach prospects with no prior relationship. Nearbound is warm: you leverage partner relationships and data to reach the same prospects with trust and context. Nearbound typically produces 2x to 3x better conversion rates."),
            ("What tools support a nearbound strategy?", "Ecosystem platforms like Reveal and Crossbeam enable account mapping. CRM and PRM integrations surface partner intelligence in the sales workflow. Slack or Teams channels facilitate real-time partner communication on live deals."),
        ],
        "related": ["ecosystem-led-growth", "partner-led-growth", "account-mapping", "partner-overlap", "co-selling"],
    },
    {
        "slug": "ecosystem-led-growth",
        "term": "Ecosystem-Led Growth",
        "short": "A growth strategy that leverages the surrounding ecosystem of partners, integrations, and marketplaces to acquire and retain customers.",
        "body": """<p>Ecosystem-led growth (ELG) is a go-to-market strategy where a company's partner ecosystem becomes the primary engine for customer acquisition, expansion, and retention. It encompasses partner-led growth and nearbound as specific motions within a broader ecosystem framework.</p>

<p>ELG operates on a simple insight: modern B2B buyers do not make purchasing decisions in isolation. They consult their existing vendors, implementation partners, and industry peers. Companies that position themselves within this web of influence win more deals than those relying solely on direct marketing and sales.</p>

<p>The three pillars of ecosystem-led growth are integration (building connections with the platforms your buyers already use), collaboration (co-selling and co-marketing with partners who share your buyer), and distribution (listing on marketplaces where procurement already happens).</p>

<p>ELG requires a shift in how companies measure success. Traditional metrics like MQLs and direct pipeline tell only part of the story. ELG metrics include partner-influenced pipeline, ecosystem-sourced revenue, integration adoption rates, marketplace transaction volume, and co-sell win rates.</p>

<p>The rise of ELG has been driven by several market forces: the proliferation of SaaS tools (average company uses 100+ applications), increasing buyer sophistication (buyers research independently before engaging sales), and cloud marketplace growth (enterprise procurement through AWS, Azure, and GCP). Companies that build strong ecosystems create compounding advantages as each partner makes the platform more valuable for customers and future partners.</p>""",
        "faq": [
            ("How does ecosystem-led growth differ from partner-led growth?", "Partner-led growth focuses specifically on partner-sourced revenue. Ecosystem-led growth is broader, encompassing integration strategy, marketplace distribution, and the full network of relationships that influence buyer decisions. PLG is a subset of ELG."),
            ("What companies are known for ecosystem-led growth?", "Salesforce, HubSpot, Shopify, AWS, and Slack are frequently cited examples. Each has built an ecosystem where partners, integrations, and marketplace transactions drive a significant portion of growth."),
        ],
        "related": ["partner-led-growth", "nearbound", "partner-ecosystem", "marketplace", "co-selling"],
    },
    {
        "slug": "partner-attach-rate",
        "term": "Partner Attach Rate",
        "short": "The percentage of deals where a partner is involved, either sourcing the opportunity or influencing the outcome.",
        "body": """<p>Partner attach rate is the percentage of closed deals that involve a channel partner in some capacity. It measures how frequently partners are participating in the sales motion, whether by sourcing opportunities, providing implementation services, or influencing the buying decision.</p>

<p>The calculation is straightforward: divide the number of deals with partner involvement by the total number of deals closed in a period. A company that closes 100 deals and 35 involve a partner has a 35 percent partner attach rate.</p>

<p>Partner attach rate is a leading indicator of ecosystem maturity. Early-stage partner programs see attach rates below 10 percent. Mature programs with strong co-selling motions achieve 40 to 60 percent. Companies with deeply embedded ecosystems (like Salesforce) can exceed 70 percent.</p>

<p>High attach rates correlate with several positive business outcomes. Partner-attached deals typically close faster, have larger contract values, and show higher retention rates than unattached deals. This makes sense: when a partner is involved, the customer gets implementation support, and the product is more deeply integrated into their workflow.</p>

<p>Improving attach rate requires making it easy for sales reps to involve partners. This means building partner referral into the sales process, training reps on when and how to engage partners, and compensating reps fully on partner-attached deals. If reps lose commission when a partner is involved, they will avoid partner engagement.</p>""",
        "faq": [
            ("What is a good partner attach rate?", "It depends on the maturity of the partner program. Below 10 percent is early stage. 20 to 40 percent indicates a developing program. Above 40 percent suggests a mature ecosystem. Industry leaders achieve 60 percent or higher."),
            ("How do you increase partner attach rate?", "Remove compensation penalties for partner-attached deals, make partner referral a default step in the sales process, train sales reps on which partners to engage for which use cases, and track attach rate as a team-level KPI."),
        ],
        "related": ["influenced-revenue", "sourced-revenue", "partner-scorecard", "co-selling"],
    },
    {
        "slug": "influenced-revenue",
        "term": "Influenced Revenue",
        "short": "Revenue from deals where a partner had a meaningful impact on the outcome but did not originate the opportunity.",
        "body": """<p>Influenced revenue is the total contract value of deals where a channel partner played a significant role in advancing the sale, even though the partner did not originate the opportunity. The deal might have been sourced by the vendor's direct team or inbound marketing, but a partner's involvement accelerated the close, expanded the scope, or tipped the decision.</p>

<p>Influence takes many forms. A technology partner might provide a joint demo showing integration value. A consulting partner might validate the vendor's approach during a buying committee review. A co-sell partner might share account intel that helps the sales rep navigate a complex org chart.</p>

<p>Influenced revenue is harder to measure than sourced revenue because the attribution is inherently subjective. Did the partner's involvement actually change the outcome, or would the deal have closed anyway? Companies handle this differently. Some use self-reported attribution (the sales rep tags the deal as partner-influenced). Others require specific evidence like logged partner activities or joint meeting records.</p>

<p>Despite measurement challenges, influenced revenue is often larger than sourced revenue. Partners influence more deals than they source because the barrier is lower. Sourcing requires finding a net-new opportunity. Influencing requires adding value to an existing one.</p>

<p>Tracking influenced revenue matters because it captures the full value of the partner program. If you only measure sourced revenue, you undercount partner contribution by 50 to 70 percent in most programs. This undercounting leads to underinvestment in partnerships and misallocation of resources.</p>""",
        "faq": [
            ("What is the difference between influenced and sourced revenue?", "Sourced revenue: the partner found the customer and initiated the deal. Influenced revenue: the partner accelerated or expanded a deal that already existed. Both represent partner value, but sourced is easier to measure and attribute."),
            ("How do you accurately track influenced revenue?", "Require sales reps to tag partner involvement in CRM at deal creation, log partner activities like joint meetings and demos, and review attribution during deal reviews. Some companies survey closed-won customers about partner involvement for additional validation."),
        ],
        "related": ["sourced-revenue", "partner-attach-rate", "partner-scorecard", "co-selling"],
    },
    {
        "slug": "sourced-revenue",
        "term": "Sourced Revenue",
        "short": "Revenue from deals that a channel partner originated, meaning the partner identified the customer and created the opportunity.",
        "body": """<p>Sourced revenue is the total contract value of deals that a channel partner originated. The partner found the customer, identified the need, and created the sales opportunity. Without the partner, the deal would not exist. This is the clearest form of partner contribution to revenue.</p>

<p>Sourced revenue is tracked through deal registration. When a partner registers a deal and it closes, the full contract value counts as partner-sourced. The attribution is clean: the partner submitted the registration before any other engagement occurred on the account.</p>

<p>For most partner programs, sourced revenue represents 15 to 30 percent of total revenue. The remaining partner contribution comes through influenced revenue. The ratio varies by partner type: referral partners primarily source, while technology partners primarily influence.</p>

<p>Sourced revenue is the metric that most directly justifies partner program investment. It represents incremental business that the vendor's direct team would not have captured. When leadership asks whether the partner program is worth the investment, sourced revenue provides the clearest answer.</p>

<p>Growing sourced revenue requires investing in partner recruitment (more partners means more deal flow), partner enablement (trained partners source better-qualified opportunities), and partner incentives (commissions and deal protection that motivate partners to bring deals to you rather than to competitors). Tracking sourced revenue by partner, tier, and type helps identify which segments of the partner base are driving the most incremental business.</p>""",
        "faq": [
            ("How do you calculate sourced revenue?", "Sum the total contract value of all closed-won deals where the partner registered the opportunity first and no prior direct engagement existed on the account. Most PRM and CRM systems can automate this calculation."),
            ("What percentage of revenue should be partner-sourced?", "Benchmarks vary by industry and company maturity. SaaS companies with established partner programs typically see 15 to 30 percent sourced. Enterprise software companies with deep channel roots may see 40 to 60 percent."),
        ],
        "related": ["influenced-revenue", "deal-registration", "partner-attach-rate", "referral-partner"],
    },
    {
        "slug": "partner-overlap",
        "term": "Partner Overlap",
        "short": "Shared customers or prospects between two companies, identified through secure account mapping to reveal co-selling opportunities.",
        "body": """<p>Partner overlap is the set of customers and prospects that two companies have in common. Identifying overlap is the starting point for co-selling: when your partner already has a relationship with one of your target accounts, you have a warm path to that buyer.</p>

<p>Overlap is identified through account mapping, where two companies securely compare their customer and prospect lists. Modern ecosystem platforms like Reveal and Crossbeam use encrypted matching so neither company exposes their full list to the other. The platform reveals only the accounts that both companies have in common.</p>

<p>There are four types of overlap that matter. Customer-to-customer: both companies have active customers in common (opportunity for integration). Customer-to-prospect: one company's customer is the other's prospect (opportunity for warm introduction). Prospect-to-prospect: both companies are targeting the same account (opportunity to coordinate outreach). Prospect-to-customer is the most valuable for the company doing the prospecting.</p>

<p>High overlap with a partner suggests strong fit for a co-selling relationship. If two companies share 30 percent or more of their target accounts, the potential for mutual introductions is significant. Low overlap might still support a technology partnership or integration relationship, even if co-selling opportunities are limited.</p>

<p>Operationalizing overlap data requires more than just running the analysis. Sales teams need workflows to request introductions, partner managers need processes to facilitate them, and both companies need agreements about data sharing, attribution, and reciprocity.</p>""",
        "faq": [
            ("How do you identify partner overlap?", "Use ecosystem platforms like Reveal or Crossbeam to run encrypted account matching. You can also manually compare customer lists in a spreadsheet, though this approach does not scale and raises data security concerns."),
            ("What percentage of overlap indicates a strong partnership fit?", "There is no fixed threshold, but 20 to 30 percent overlap in target accounts is generally considered strong. Even 5 to 10 percent can be valuable if the overlapping accounts are high-value enterprise targets."),
        ],
        "related": ["account-mapping", "co-selling", "nearbound", "partner-ecosystem"],
    },
    {
        "slug": "account-mapping",
        "term": "Account Mapping",
        "short": "The process of securely comparing customer and prospect lists between partners to identify shared accounts and co-selling opportunities.",
        "body": """<p>Account mapping is the process of comparing CRM data between two partner companies to identify which customers and prospects they have in common. It is the foundational activity for co-selling, nearbound, and ecosystem-led growth strategies.</p>

<p>Traditional account mapping involved exporting spreadsheets and comparing them manually. This was slow, error-prone, and raised legitimate data security concerns. Modern ecosystem platforms have replaced this approach with automated, encrypted matching that identifies overlap without exposing either company's full account list.</p>

<p>The output of account mapping is an overlap matrix. For each shared account, both companies see their own relationship status (customer, prospect, churned) alongside the partner's status. This immediately reveals actionable opportunities: your partner's customer who is your prospect is a warm introduction waiting to happen.</p>

<p>Account mapping works best when done regularly, not as a one-time exercise. Customer and prospect lists change constantly. Running mapping monthly or connecting it to live CRM data ensures the overlap data stays current and sales teams act on fresh intelligence.</p>

<p>The value of account mapping scales with the number of partners. If you map accounts with one partner, you get one set of insights. Map with 20 partners and you build a comprehensive picture of ecosystem coverage across your target market. Some companies find that their combined partner ecosystem covers 80 to 90 percent of their ideal customer profile.</p>""",
        "faq": [
            ("What tools are used for account mapping?", "Reveal (formerly Crossbeam) and Crossbeam are the leading purpose-built platforms. Some PRM systems include basic account mapping. CRM-native solutions like Salesforce Connect can also facilitate data sharing between partner organizations."),
            ("How do you protect data during account mapping?", "Modern platforms use encrypted matching. Each company hashes their account data before comparison. The platform identifies matches without either company seeing the other's full list. Only mutually agreed overlap data is revealed."),
        ],
        "related": ["partner-overlap", "co-selling", "nearbound", "ecosystem-led-growth"],
    },
    {
        "slug": "marketplace",
        "term": "Marketplace",
        "short": "A digital storefront where software vendors list their products for buyers to discover, evaluate, and purchase.",
        "body": """<p>A marketplace in the B2B context is a digital platform where software vendors list their products and buyers discover, evaluate, and purchase solutions. Marketplaces range from app stores within specific platforms (Salesforce AppExchange, HubSpot Marketplace) to cloud provider marketplaces (AWS Marketplace, Azure Marketplace) to independent aggregators.</p>

<p>Marketplaces solve a procurement problem. Enterprise buyers need to evaluate, approve, and purchase software. Marketplace listings provide standardized information (pricing, reviews, certifications) and streamlined purchasing (procurement through existing cloud commits or platform accounts).</p>

<p>For vendors, marketplace listing provides distribution. Products become discoverable to the platform's entire customer base. For cloud marketplaces specifically, the ability to transact through existing cloud commits is a powerful sales accelerator: buyers can purchase your software using budget they have already allocated for cloud spend.</p>

<p>Marketplace economics involve listing fees, revenue sharing, or both. Cloud marketplaces typically charge 3 to 20 percent of transaction value. Platform marketplaces may charge listing fees, take revenue share, or operate as free directories that drive traffic to the vendor's own purchase flow.</p>

<p>Marketplace strategy has become a distinct competency in B2B software. Companies hire marketplace managers, invest in listing optimization, and build dedicated marketplace transaction workflows. The most sophisticated players treat marketplace as a primary revenue channel, not just a secondary listing.</p>""",
        "faq": [
            ("What is the benefit of listing on a cloud marketplace?", "Buyers can purchase using existing cloud commit budgets, which removes budget friction. Marketplace deals also benefit from the cloud provider's co-sell support and can close faster because procurement is pre-approved."),
            ("How much do marketplaces charge vendors?", "Cloud marketplaces typically take 3 to 20 percent of transaction value. SaaS platform marketplaces range from free listings with referral fees to 15 to 30 percent revenue share. Many offer reduced rates for higher-volume sellers."),
        ],
        "related": ["cloud-marketplace", "listing-fee", "revenue-share", "isv-partner", "technology-partner"],
    },
    {
        "slug": "cloud-marketplace",
        "term": "Cloud Marketplace",
        "short": "A procurement platform operated by AWS, Azure, or GCP where enterprise buyers purchase third-party software using their cloud commit.",
        "body": """<p>A cloud marketplace is a digital procurement platform operated by a major cloud provider (AWS, Microsoft Azure, or Google Cloud) where enterprise buyers can discover, purchase, and deploy third-party software. The defining feature is the ability to purchase software using existing cloud commit budgets, which removes procurement friction and accelerates deal cycles.</p>

<p>Cloud marketplaces have grown rapidly because they solve a real problem for enterprise procurement. Large organizations commit millions to cloud providers through Enterprise Discount Programs (EDPs) and Microsoft Azure Consumption Commitments (MACCs). Purchasing software through the marketplace counts toward these commitments, effectively making the software "free" from a budget perspective since the money was already allocated.</p>

<p>For ISVs and SaaS vendors, cloud marketplace listing provides access to enterprise buyers who prefer marketplace procurement. Deals that stall in traditional procurement (legal review, vendor onboarding, purchase orders) can close in days through the marketplace because the cloud provider is already an approved vendor.</p>

<p>The economics include a revenue share to the cloud provider (typically 3 to 5 percent for private offers) and potential co-sell support from the cloud provider's sales team. AWS ISV Accelerate, Microsoft co-sell, and Google Cloud partner programs all offer incentives for marketplace transactions.</p>

<p>Marketplace management platforms like Tackle.io, Clyde, and Labra have emerged to help vendors manage listings, create private offers, handle metering and billing, and optimize their marketplace strategy across all three providers simultaneously.</p>""",
        "faq": [
            ("How do cloud marketplace transactions work?", "The vendor creates a listing or private offer. The buyer accepts through their cloud console. Payment flows through the cloud provider's billing system. The vendor receives the transaction amount minus the marketplace fee, typically within 30 to 60 days."),
            ("What is a private offer on cloud marketplace?", "A private offer is a custom pricing agreement between a vendor and a specific buyer, facilitated through the marketplace. It allows negotiated pricing, custom terms, and multi-year commitments while still counting toward the buyer's cloud commit."),
        ],
        "related": ["marketplace", "listing-fee", "revenue-share", "isv-partner"],
    },
    {
        "slug": "listing-fee",
        "term": "Listing Fee",
        "short": "A fee charged by a marketplace or directory for placing a product listing on their platform.",
        "body": """<p>A listing fee is a charge that a marketplace, directory, or platform levies on vendors for placing their product in the catalog. The fee structure varies widely: some marketplaces charge a flat annual fee for presence, others charge per-listing fees, and many have moved to transaction-based models where the fee is a percentage of revenue generated through the platform.</p>

<p>In cloud marketplaces, listing fees have largely been replaced by revenue share models. AWS, Azure, and Google Cloud do not charge upfront fees to list. Instead, they take a percentage (typically 3 to 20 percent) of each transaction. This aligns incentives: the marketplace earns only when the vendor earns.</p>

<p>Platform-specific marketplaces (like Salesforce AppExchange or Shopify App Store) may charge a combination of listing fees and revenue share. Salesforce charges security reviews and listing fees that vary by listing type. Shopify takes a revenue share on app subscriptions sold through its marketplace.</p>

<p>For B2B software vendors, listing fees are a cost of distribution. The decision to list depends on whether the marketplace provides access to buyers who would not otherwise discover the product. A $5,000 annual listing fee that generates even one enterprise deal provides strong ROI.</p>

<p>Some vendors negotiate reduced or waived listing fees as part of technology partner agreements, especially when their integration adds significant value to the marketplace platform's ecosystem.</p>""",
        "faq": [
            ("Do cloud marketplaces charge listing fees?", "Major cloud marketplaces (AWS, Azure, GCP) generally do not charge upfront listing fees. They use a revenue-share model, taking a percentage of each transaction. Platform-specific marketplaces may charge listing fees in addition to or instead of revenue share."),
            ("Are marketplace listing fees worth the cost?", "For most B2B software vendors, yes. Even modest listing fees provide access to a captive audience of buyers already using the platform. One enterprise deal typically covers years of listing fees."),
        ],
        "related": ["marketplace", "cloud-marketplace", "revenue-share"],
    },
    {
        "slug": "revenue-share",
        "term": "Revenue Share",
        "short": "A compensation model where a vendor splits a percentage of deal revenue with a partner who contributed to the sale.",
        "body": """<p>Revenue share is a compensation arrangement where a vendor pays a channel partner a percentage of revenue generated from customers that the partner sourced, influenced, or transacted. It is the most common economic model in technology partnerships and marketplace relationships.</p>

<p>Revenue share percentages vary by partner type and contribution. Referral partners typically receive 10 to 20 percent of the first year's contract value. Resellers earn 20 to 40 percent margins (equivalent to buying at discount). Marketplace platforms take 3 to 20 percent of transaction value. Affiliate programs offer 15 to 30 percent recurring commissions.</p>

<p>The structure of revenue share deals differs in important ways. One-time payments reward partners for sourcing the initial deal but provide no ongoing incentive to ensure customer success. Recurring revenue share (paid for the life of the customer) aligns partner incentives with retention and expansion. Most modern SaaS partner programs have shifted toward recurring models.</p>

<p>Revenue share calculations need clear definitions. Does "revenue" mean the total contract value, the first-year value, or the monthly recurring revenue? Is it based on list price or the actual transacted price? Are renewals included? Are upsells included if the partner was not involved? These details must be spelled out in the partner agreement to avoid disputes.</p>

<p>For vendors, revenue share is an expense that scales with success. Unlike fixed costs like headcount, revenue share only increases when revenue increases. This makes it an efficient way to fund channel growth, especially for companies where direct customer acquisition costs are rising.</p>""",
        "faq": [
            ("What is a typical revenue share percentage for channel partners?", "Referral partners: 10 to 20 percent. Resellers: 20 to 40 percent discount (equivalent margin). Marketplace platforms: 3 to 20 percent. Affiliate programs: 15 to 30 percent. The rate depends on partner contribution and the vendor's margin structure."),
            ("Should revenue share be one-time or recurring?", "Recurring revenue share aligns partner incentives with customer retention and long-term value. One-time payments motivate initial sourcing but not ongoing engagement. Most SaaS programs now use recurring models."),
        ],
        "related": ["referral-partner", "reseller", "marketplace", "listing-fee"],
    },
    {
        "slug": "channel-manager",
        "term": "Channel Manager",
        "short": "A professional responsible for recruiting, enabling, and managing a vendor's relationships with channel partners.",
        "body": """<p>A channel manager is the person responsible for building and managing a vendor's relationships with channel partners. They recruit new partners, onboard them into the program, drive partner enablement, manage deal registration, resolve channel conflicts, and ultimately ensure that partners generate revenue.</p>

<p>The channel manager role requires a blend of sales and relationship management skills. Unlike direct sales reps who sell to end customers, channel managers sell through partners. They must motivate and support independent organizations over which they have no direct authority. Success depends on building trust, demonstrating value, and making it easy for partners to do business.</p>

<p>Day-to-day responsibilities include conducting partner business reviews, managing pipeline with top partners, coordinating co-selling and co-marketing activities, tracking partner performance against scorecard metrics, and advocating for partner needs within the vendor organization.</p>

<p>Channel managers are measured on partner-sourced and partner-influenced revenue, partner recruitment targets, partner engagement metrics, and overall channel revenue growth. The best channel managers build genuine relationships with their partner counterparts and understand each partner's business model well enough to articulate mutual value.</p>

<p>Career progression for channel managers typically moves from individual contributor to senior channel manager to director of channel partnerships to VP of partnerships or channel chief. The role has grown in strategic importance as companies invest more heavily in ecosystem-led growth.</p>""",
        "faq": [
            ("What skills does a channel manager need?", "Relationship building, strategic thinking, sales enablement, project management, and the ability to influence without authority. Technical knowledge of the vendor's product and the partner's business model are equally important."),
            ("What is the average salary for a channel manager?", "In the US, channel manager base salaries range from $80,000 to $140,000 depending on experience, company size, and location. OTE (on-target earnings) with variable compensation ranges from $110,000 to $200,000."),
        ],
        "related": ["alliance-manager", "partner-success", "channel-strategy", "channel-sales"],
    },
    {
        "slug": "alliance-manager",
        "term": "Alliance Manager",
        "short": "A professional who manages strategic technology and business partnerships between two companies at the executive and organizational level.",
        "body": """<p>An alliance manager is responsible for managing strategic partnerships between two companies at an organizational level. While channel managers focus on enabling many partners to generate transactional revenue, alliance managers focus on deep, strategic relationships with a small number of high-value partners.</p>

<p>Alliance management is most common in relationships between large technology companies. An alliance manager at Salesforce might manage the relationship with AWS. An alliance manager at Accenture might oversee the firm's partnership with Microsoft. These relationships span multiple business units, involve executive alignment, and generate tens or hundreds of millions in shared revenue.</p>

<p>The role involves developing joint business plans, coordinating executive relationships, aligning product roadmaps, managing co-investment programs, measuring partnership health, and resolving cross-organizational conflicts. Alliance managers operate at the intersection of sales, product, marketing, and corporate strategy.</p>

<p>Alliance managers need executive communication skills, strategic planning ability, financial acumen, and deep understanding of both organizations' business models. They must navigate complex internal politics at two companies simultaneously and build alignment between stakeholders who may have competing priorities.</p>

<p>Career paths in alliance management typically require prior experience in sales, business development, or channel management. Senior alliance roles (VP of Alliances, Chief Partnership Officer) are increasingly common in the C-suite as companies recognize that strategic partnerships drive competitive advantage.</p>""",
        "faq": [
            ("What is the difference between an alliance manager and a channel manager?", "A channel manager manages many partners with a focus on transactional revenue. An alliance manager manages a few strategic partnerships with a focus on long-term business alignment, joint product development, and executive relationships. Alliance deals are typically larger and more complex."),
            ("What is the typical salary for an alliance manager?", "Alliance manager salaries in the US range from $120,000 to $200,000 base, with OTE reaching $180,000 to $350,000 at senior levels. VP-level alliance roles at large technology companies can exceed $400,000 total compensation."),
        ],
        "related": ["channel-manager", "partner-success", "co-selling", "partner-ecosystem"],
    },
    {
        "slug": "partner-success",
        "term": "Partner Success",
        "short": "A function dedicated to ensuring channel partners achieve their business goals and maximize value from the vendor relationship.",
        "body": """<p>Partner success is a function within a vendor's partnerships organization that focuses on ensuring channel partners achieve their goals, remain engaged, and grow their business with the vendor's products. It applies the principles of customer success management to the partner relationship.</p>

<p>The partner success function emerged because traditional channel management focused primarily on recruitment and deal support, often neglecting partners after they joined the program. Partners would sign up, complete onboarding, and then receive little proactive support. This led to high partner churn and low engagement rates.</p>

<p>Partner success managers (PSMs) take a proactive approach. They monitor partner health metrics (portal activity, certification status, deal pipeline, customer satisfaction), identify partners at risk of disengagement, and intervene with targeted support before the relationship deteriorates.</p>

<p>Common partner success activities include quarterly business reviews, enablement gap assessments, marketing campaign support, customer success escalation assistance, and growth planning. PSMs also serve as the partner's advocate within the vendor organization, ensuring that partner feedback reaches product, marketing, and executive teams.</p>

<p>The ROI of partner success is measured through partner retention rates, partner revenue growth, net partner score (equivalent of NPS for partners), and time-to-value for new partners. Companies with dedicated partner success functions typically see 20 to 40 percent higher partner retention and faster partner ramp times compared to those without.</p>""",
        "faq": [
            ("What is the difference between partner success and channel management?", "Channel management focuses on recruitment, deal support, and program operations. Partner success focuses on proactive relationship health, partner goal achievement, and retention. Think of it as account management versus customer success applied to the partner base."),
            ("How do you measure partner success?", "Key metrics include partner retention rate, partner NPS, average revenue per partner over time, time from onboarding to first deal, partner satisfaction survey scores, and partner engagement indices based on portal and program activity."),
        ],
        "related": ["channel-manager", "partner-onboarding", "partner-scorecard", "partner-enablement"],
    },
    {
        "slug": "partner-onboarding",
        "term": "Partner Onboarding",
        "short": "The structured process of bringing new channel partners into a vendor's program, from agreement signing through first deal.",
        "body": """<p>Partner onboarding is the structured process of taking a newly signed channel partner from agreement to first productive engagement. It covers program orientation, technical training, sales enablement, portal access setup, and all the activities needed to make the partner ready and willing to sell.</p>

<p>Effective onboarding follows a defined timeline with milestones. A typical 30-60-90 day plan includes: Week 1: portal access, program overview, and assigned partner manager. Month 1: product training and sales certification. Month 2: first customer engagement or deal registration. Month 3: first closed deal or joint marketing activity.</p>

<p>The speed and quality of onboarding directly correlates with long-term partner success. Partners who achieve their first deal within 90 days are significantly more likely to remain active and grow their investment. Partners who drift past six months without a win often disengage permanently.</p>

<p>Onboarding should be tailored to partner type. A technology partner needs API documentation and integration support. A reseller needs pricing, competitive positioning, and deal registration training. An agency partner needs implementation playbooks and certification paths. One-size-fits-all onboarding fails because different partner types have different needs and motivations.</p>

<p>Automation improves onboarding scale. PRM platforms can trigger email sequences, assign training modules, track completion, and alert partner managers when milestones are missed. But automation cannot replace human connection. The most effective programs combine automated workflows with personal engagement from dedicated partner managers during the critical first 90 days.</p>""",
        "faq": [
            ("How long should partner onboarding take?", "The goal is a productive partner within 90 days. Most programs structure a 30-60-90 day plan with increasing commitment at each stage. Complex SI or technology partnerships may require longer onboarding due to technical integration requirements."),
            ("What is the biggest mistake in partner onboarding?", "Treating onboarding as a one-time event rather than a guided process. Sending a welcome email with a portal link and expecting the partner to figure it out results in low engagement. Structured, milestone-based onboarding with accountability produces dramatically better results."),
        ],
        "related": ["partner-enablement", "partner-success", "partner-portal", "prm-partner-relationship-management"],
    },
    {
        "slug": "channel-strategy",
        "term": "Channel Strategy",
        "short": "The deliberate plan for how a company will use indirect sales channels to reach customers, including partner types, economics, and go-to-market rules.",
        "body": """<p>Channel strategy is the comprehensive plan for how a company will use indirect sales channels to reach customers and grow revenue. It defines which partner types to recruit, what economics to offer, how to segment direct and indirect accounts, and how the channel program supports overall business objectives.</p>

<p>A sound channel strategy starts with market analysis. Where are your customers buying? What expertise do they need during evaluation and implementation? Which geographies or verticals are underserved by your direct team? The answers determine whether you need resellers, SIs, MSPs, referral partners, or a combination.</p>

<p>Economics are the core of channel strategy. The margin structure must work for both sides. If partner margin is too thin, partners will prioritize competing vendors. If too generous, it erodes the vendor's profitability. The right balance depends on partner contribution (do they just refer, or do they sell, implement, and support?) and competitive dynamics (what do competing vendors offer their partners?).</p>

<p>Rules of engagement between direct and channel sales must be defined before launching, not after conflicts arise. Which accounts are channel-exclusive? Which are direct-exclusive? How are hybrid accounts handled? Clear rules prevent the channel conflict that destroys partner trust.</p>

<p>Channel strategy is not static. Market conditions, competitive dynamics, and internal capabilities change. The best programs review strategy annually, adjusting partner types, tier structures, economics, and market focus based on data from the prior year's performance.</p>""",
        "faq": [
            ("When should a company develop a channel strategy?", "After proving product-market fit and establishing a repeatable direct sales motion. Launching channel before you know how to sell the product yourself transfers your learning curve to partners, which rarely works."),
            ("What are the components of a channel strategy?", "Partner type selection, economic model (margins, commissions, MDF), direct-channel rules of engagement, territory or segment definitions, partner recruitment criteria, enablement plan, and success metrics with quarterly review cadence."),
        ],
        "related": ["channel-sales", "channel-conflict", "channel-manager", "partner-tiering", "two-tier-distribution"],
    },
    {
        "slug": "two-tier-distribution",
        "term": "Two-Tier Distribution",
        "short": "A channel model where the vendor sells to distributors, who then supply and support a network of resellers who sell to end customers.",
        "body": """<p>Two-tier distribution is a channel model where a vendor sells products to distributors, who then resell to a network of resellers, VARs, or MSPs that serve end customers. The flow is: vendor to distributor to reseller to customer. Each tier adds value and takes margin.</p>

<p>This model exists because managing thousands of small resellers directly is operationally expensive. Distributors aggregate demand, handle logistics, extend credit, and provide technical support to the reseller network. The vendor gets broad market coverage without the overhead of managing each reseller relationship individually.</p>

<p>Distributors add several forms of value. Credit and billing: they extend payment terms to resellers so the vendor does not carry accounts receivable risk across thousands of small partners. Logistics: they warehouse and ship physical products (still relevant for hardware and hybrid deployments). Technical enablement: they train and certify resellers on the vendor's products. Market reach: they have established relationships with resellers the vendor could not efficiently recruit on its own.</p>

<p>In the SaaS era, the two-tier model has evolved. Physical logistics are less relevant, but the credit, enablement, and market reach functions remain valuable. Cloud distributors like Pax8, Sherweb, and AppSmart have built modern versions of two-tier distribution optimized for subscription software.</p>

<p>Two-tier economics reduce the vendor's margin per unit but increase total units sold. The vendor might earn 50 cents on the dollar instead of 70, but sell five times the volume. The math works when the product has low marginal cost (software) and the reseller network provides coverage the vendor could not achieve alone.</p>""",
        "faq": [
            ("What is the difference between one-tier and two-tier distribution?", "In one-tier, the vendor sells directly to resellers. In two-tier, a distributor sits between the vendor and the reseller network. Two-tier adds cost but provides broader reach and operational services that make it practical to work with thousands of small partners."),
            ("Is two-tier distribution still relevant for SaaS?", "Yes, though it has evolved. Cloud distributors provide license management, billing aggregation, technical enablement, and market access for SaaS vendors. The logistics function is less relevant, but the financial and enablement functions remain valuable."),
        ],
        "related": ["distributor", "reseller", "channel-strategy", "channel-sales"],
    },
    {
        "slug": "distributor",
        "term": "Distributor",
        "short": "A company that buys from vendors in volume and resells to a network of resellers, adding logistics, credit, and enablement services.",
        "body": """<p>A distributor is an intermediary in the channel that buys products from vendors at volume pricing and resells them to a network of resellers, VARs, and MSPs. Distributors do not sell to end customers. Their customer is the reseller.</p>

<p>The distributor business model is built on scale and operational efficiency. By aggregating demand from hundreds or thousands of resellers, distributors achieve volume pricing from vendors and pass part of that discount to their reseller customers. They earn margin on the spread, plus fees for value-added services.</p>

<p>Traditional IT distributors like Ingram Micro, TD SYNNEX, and Arrow Electronics built massive logistics operations: warehouses, shipping networks, and inventory management for hardware products. They also provide credit (resellers buy on terms instead of paying upfront), technical training, and marketing support.</p>

<p>Cloud and SaaS have created a new class of distributors. Companies like Pax8, Sherweb, and AppSmart focus on subscription software. Instead of warehousing and shipping, they provide license provisioning, billing aggregation, and multi-vendor management portals for MSPs and resellers.</p>

<p>For vendors, distributors provide market coverage that would be impossible to build directly. A single distributor relationship can connect you to thousands of resellers across geographies. The trade-off is another layer of margin and less direct control over how your product is positioned and sold to end customers.</p>""",
        "faq": [
            ("What is the difference between a distributor and a reseller?", "A distributor sells to resellers. A reseller sells to end customers. The distributor is a logistics, credit, and enablement layer between the vendor and the reseller network. Resellers are the last mile to the customer."),
            ("How do distributors make money?", "Distributors earn margin on the spread between vendor pricing and reseller pricing, typically 5 to 15 percent. They also earn fees for value-added services like training, marketing, and technical support. Volume rebates from vendors supplement margins."),
        ],
        "related": ["two-tier-distribution", "reseller", "var-value-added-reseller", "channel-sales"],
    },
    {
        "slug": "white-label",
        "term": "White Label",
        "short": "A product or service built by one company and rebranded by another company to sell as their own.",
        "body": """<p>White labeling is a business arrangement where one company produces a product or service and another company rebrands it and sells it under their own name. The end customer interacts with the reselling company's brand and may never know that the underlying product was built by a different organization.</p>

<p>White labeling is common across industries. In software, a company might white-label a reporting platform, embedding it within their own application under their own brand. In services, an agency might white-label SEO work from a specialist firm and deliver it to clients as their own service.</p>

<p>The economics benefit both sides. The producer gets scale distribution without building a sales and marketing operation for each market. The reseller gets a product to sell without the R&D investment of building it. Both companies earn margin: the producer on volume production, the reseller on brand and distribution.</p>

<p>White labeling requires specific technical and legal infrastructure. The product must be fully rebrandable: logos, colors, domain, and customer-facing communications all need to carry the reseller's brand. Legal agreements must cover liability, intellectual property, exclusivity terms, and quality standards.</p>

<p>The main risk for white-label buyers is dependency. If the producer raises prices, changes the product, or goes out of business, the reseller has a serious problem because they do not own the underlying technology. Smart white-label agreements include source code escrow, performance SLAs, and transition assistance clauses.</p>""",
        "faq": [
            ("What is the difference between white label and private label?", "The terms are often used interchangeably, but white label typically refers to a generic product rebranded by multiple resellers, while private label implies an exclusive arrangement where the product is customized and sold by a single reseller."),
            ("What should a white label agreement include?", "Branding guidelines, pricing and minimum commitments, SLAs for uptime and support, intellectual property ownership, exclusivity terms (if any), termination procedures, and transition assistance provisions."),
        ],
        "related": ["private-label", "oem-partner", "reseller", "revenue-share"],
    },
    {
        "slug": "private-label",
        "term": "Private Label",
        "short": "A product manufactured or developed by one company but sold exclusively under another company's brand, often with customization.",
        "body": """<p>Private labeling is a business arrangement where a product is manufactured or developed by one company but sold exclusively under another company's brand. Unlike white labeling, which typically involves a generic product rebranded by multiple companies, private labeling usually implies an exclusive or semi-exclusive arrangement with product customization for the selling company.</p>

<p>In software, private labeling means the selling company gets a customized version of the product with their branding, custom features, and often exclusive access to certain capabilities. The level of customization distinguishes private label from white label, though the boundary between the two is not always clear.</p>

<p>Retailers have long used private labeling to offer store-brand products. In the SaaS world, the model is gaining traction as companies look to offer adjacent capabilities without building them in-house. A CRM company might private-label a marketing automation tool, customizing it to integrate deeply with their platform and selling it as a native feature.</p>

<p>Private label agreements are more complex than white label because they involve customization, exclusivity, and often joint product roadmap planning. The producer invests more upfront in creating the customized version, so they typically require longer contracts and higher minimum commitments.</p>

<p>For the selling company, private label provides control over the customer experience without the cost and time of building from scratch. For the producing company, a private label deal provides guaranteed revenue and a strategic partnership with a larger brand that can drive significant volume.</p>""",
        "faq": [
            ("When does private labeling make sense?", "When you need a product capability that is outside your core competency, time-to-market matters, and you want brand control over the customer experience. Private label is faster and cheaper than building but more controlled than white label."),
            ("What is the difference between private label and OEM?", "Private label sells a complete, branded product. OEM embeds a technology component inside a larger product. With private label, the product is standalone under the seller's brand. With OEM, the technology is invisible to the end customer, buried inside another product."),
        ],
        "related": ["white-label", "oem-partner", "reseller"],
    },
]


def _slugify(text):
    """Convert text to URL-safe slug."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')


def _get_related_terms(term_data, all_terms_by_slug):
    """Return list of (name, slug) for related terms that exist."""
    related = []
    for slug in term_data.get("related", []):
        if slug in all_terms_by_slug:
            related.append((all_terms_by_slug[slug]["term"], slug))
    return related


# ---------------------------------------------------------------------------
# Glossary index page
# ---------------------------------------------------------------------------

def build_glossary_index(all_terms):
    """Build /glossary/ index page listing all terms."""
    title = "Partnerships & Channel Sales Glossary: 45 Key Terms"
    description = (
        "Clear definitions for 45 partnerships and channel sales terms."
        " PRM, co-selling, deal registration, nearbound, ecosystem-led growth, and more."
    )

    crumbs = [("Home", "/"), ("Glossary", None)]
    bc_html = breadcrumb_html(crumbs)

    # Group terms alphabetically
    alpha_groups = {}
    for t in sorted(all_terms, key=lambda x: x["term"].lower().lstrip('"')):
        first = t["term"][0].upper()
        # Handle parenthetical terms like "PRM (Partner...)"
        if first == '"':
            first = t["term"][1].upper()
        alpha_groups.setdefault(first, []).append(t)

    letter_nav = ""
    cards = ""
    for letter in sorted(alpha_groups.keys()):
        letter_nav += f'<a href="#letter-{letter}" class="glossary-letter-link">{letter}</a> '
        cards += f'<h2 id="letter-{letter}" class="glossary-letter-heading">{letter}</h2>\n'
        cards += '<div class="glossary-grid">\n'
        for t in alpha_groups[letter]:
            cards += f'''<a href="/glossary/{t["slug"]}/" class="glossary-card">
    <h3 class="glossary-card-term">{t["term"]}</h3>
    <p class="glossary-card-def">{t["short"]}</p>
</a>
'''
        cards += '</div>\n'

    body = f'''{bc_html}
<section class="page-header">
    <h1>Partnerships &amp; Channel Sales Glossary</h1>
    <p class="page-header-sub">Clear definitions for the terms that matter in partnerships, channel sales, and ecosystem strategy. No jargon soup. Each entry explains the concept, why it matters, and how it connects to the broader partner ecosystem.</p>
</section>
<div class="container">
    <div class="glossary-letter-nav">{letter_nav}</div>
    {cards}
</div>
'''
    body += newsletter_cta_html("Glossary updates and new terms delivered weekly.")

    schema = get_breadcrumb_schema(crumbs)

    page = get_page_wrapper(
        title=title,
        description=description,
        canonical_path="/glossary/",
        body_content=body,
        active_path="/glossary/",
        extra_head=schema,
        body_class="page-inner",
    )
    write_page("glossary/index.html", page)
    print(f"  Built: glossary/index.html")


# ---------------------------------------------------------------------------
# Individual term pages
# ---------------------------------------------------------------------------

def build_glossary_term_page(term_data, all_terms_by_slug):
    """Build a single glossary term page at /glossary/{slug}/."""
    t = term_data
    slug = t["slug"]
    term_name = t["term"]

    title = f"What Is {term_name}? Definition & Guide"
    description = t["short"]
    if len(description) > 158:
        description = description[:155].rstrip() + "..."

    crumbs = [("Home", "/"), ("Glossary", "/glossary/"), (term_name, None)]
    bc_html = breadcrumb_html(crumbs)

    # Related terms section
    related = _get_related_terms(t, all_terms_by_slug)
    related_html = ""
    if related:
        related_links = ""
        for rname, rslug in related:
            related_links += f'<a href="/glossary/{rslug}/" class="related-term-link">{rname}</a>\n'
        related_html = f'''<section class="related-terms">
    <h2>Related Terms</h2>
    <div class="related-terms-grid">
        {related_links}
    </div>
</section>'''

    # FAQ section (visible + schema)
    faq_pairs = t.get("faq", [])
    faq_section = ""
    faq_schema_str = ""
    if faq_pairs:
        faq_section = faq_html(faq_pairs)
        faq_schema_str = get_faq_schema(faq_pairs)

    bc_schema = get_breadcrumb_schema(crumbs)
    combined_schema = bc_schema + faq_schema_str

    body = f'''{bc_html}
<section class="page-header">
    <h1>What Is {term_name}?</h1>
    <p class="page-header-sub">{t["short"]}</p>
</section>
<div class="container glossary-content">
    <article class="glossary-article">
        {t["body"]}
    </article>
    {faq_section}
    {related_html}
</div>
'''
    body += newsletter_cta_html(f"Get more partnerships insights like this {term_name} guide.")

    page = get_page_wrapper(
        title=title,
        description=description,
        canonical_path=f"/glossary/{slug}/",
        body_content=body,
        active_path="/glossary/",
        extra_head=combined_schema,
        body_class="page-inner",
    )
    write_page(f"glossary/{slug}/index.html", page)


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def build_all_glossary_pages():
    """Build all glossary pages: index + individual terms."""
    print("\n  Building glossary pages...")

    all_terms_by_slug = {t["slug"]: t for t in GLOSSARY_TERMS}

    build_glossary_index(GLOSSARY_TERMS)

    for t in GLOSSARY_TERMS:
        build_glossary_term_page(t, all_terms_by_slug)

    print(f"  Built: {len(GLOSSARY_TERMS)} glossary term pages")
