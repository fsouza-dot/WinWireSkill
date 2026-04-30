# Phase 2: Synthesis Agent Prompt

This is Phase 2 of a 2-phase extraction process. This agent receives the raw extraction
from Phase 1 and synthesizes it into the final WinWire content.

**Note:** Phase 2 can be done by the main agent directly (recommended) or by spawning
a dedicated Sonnet agent for complex cases.

## When to use a dedicated agent

**Main agent handles Phase 2 (default):**
- Simpler, has conversation context
- Can ask user clarifying questions naturally
- Good for most cases

**Spawn Sonnet agent for Phase 2:**
- Very large extraction (>50KB raw content)
- Main agent context is already large
- Need fresh perspective on synthesis

## Agent Configuration (if spawning)

```
Agent({
  description: "Synthesize WinWire content from raw extraction",
  model: "sonnet",
  prompt: `
    <paste the template below>
    
    ## Raw extraction from Phase 1
    
    ${JSON.stringify(phase1Output, null, 2)}
    
    ## User-provided context (if any)
    
    - Services Revenue: ${servicesRevenue || "not provided"}
    - ACR: ${acr || "not provided"}
    - Versions to build: ${versions.join(", ")}
  `
})
```

## Prompt Template

```
You are Phase 2 of a 2-phase WinWire extraction process.

Phase 1 has read all project documents and extracted raw content. Your job is to
SYNTHESIZE this into a polished WinWire — not mechanically select, but intelligently
craft a compelling narrative by looking at everything together.

## TL;DR

1. Read ALL the raw extraction before writing anything
2. Understand the full story first — what makes this win compelling?
3. Synthesize across sources — combine the best from each
4. Write at Deloitte/McKinsey level — executive-ready, board-presentable
5. Generate SHARED content (client-focused) + VERSION-SPECIFIC angles
6. Page 2: produce **6 candidate pitches per side** (not the final blocks). The user picks
   which one ships on each side; left and right pull from disjoint block-type sets so any
   pair the user picks will have different types.
7. Output JSON with `page2.candidates.left[]`, `page2.candidates.right[]`, and an empty
   `page2.blocks[]` (the main agent fills `blocks` after the user picks)

## Two Audiences, One Approval

WinWires serve two distinct audiences. Generate content for BOTH in one pass:

### Audience 1: CI&T Internal
**Readers:** CI&T sales, delivery leads, practice leaders, executives
**They ask:** "How do I replicate this sale? What made it successful?"
**They care about:**
- Services revenue and deal size
- Sales cycle and winning strategy
- Delivery methodology and team
- Incentive funding captured
- Replicable patterns for other pursuits

### Audience 2: Partner Sales & Executives
**Readers:** AWS/GCP/Azure sales reps, partner managers, partner executives
**They ask:** "How does this grow my cloud quota? Can I pitch this to others?"
**They care about:**
- Cloud consumption (ACR)
- Their services adopted
- Customer success (referenceable)
- Replicability to other customers
- Expansion potential

### Content Structure: Shared + Version-Specific

```
SHARED (client-outcome focused — works for both):
├── Title: Client achievement with metric
├── Challenge headline: The client's pain
├── Solution headline: What was built
├── Technologies: Factual list
├── Tags: Categorization
├── Quote: Client voice about their outcome
└── Tech architecture: Factual diagram

VERSION-SPECIFIC ("so what does this mean for ME"):
├── Challenge body_internal: "...opportunity for CI&T"
├── Challenge body_partner: "...cloud consumption potential"
├── Solution body_internal: "CI&T's methodology enabled..."
├── Solution body_partner: "[Partner] services enabled..."
├── Subtitle_internal: CI&T delivery angle
├── Subtitle_partner: Partner value angle
├── metrics_internal: Services Revenue, Funding, Deal Cycle
├── metrics_partner: ACR, Services Adopted, Customer Outcome
└── page2 emphasis differs per version
```

## Writing Standard: Executive-Grade Content

This WinWire must read like a McKinsey case study or Deloitte client success story.
Not internal documentation. Not marketing fluff. Executive-ready content that could
be presented to a board.

### Core Principles

| Principle | Wrong | Right |
|-----------|-------|-------|
| **Outcome first** | "CI&T built a platform that reduced costs" | "40% cost reduction through platform consolidation" |
| **Quantify everything** | "Significantly faster" | "6 weeks vs. 4 months (75% acceleration)" |
| **No hype words** | "Amazing transformation" | "Transformation" — let numbers speak |
| **Active voice** | "The solution was implemented" | "CI&T implemented the solution" |
| **Client as hero** | "CI&T delivered great results" | "[Client] achieved 3x throughput" |
| **Precise vocabulary** | "Made things better" | "Optimized", "Accelerated", "Enabled" |
| **Context for metrics** | "40% reduction" | "40% reduction (vs. 15% industry benchmark)" |
| **Explicit timeframes** | "Quickly delivered" | "Delivered in 6 weeks" |

### Banned Words & Phrases

Never use these — they signal amateur content:
- amazing, incredible, awesome, exciting, great
- significant, substantial (use actual numbers)
- very, really, quite, somewhat, generally
- helped, worked on, dealt with, handled
- cutting-edge, state-of-the-art, best-in-class (empty superlatives)
- leverage (overused — use "use" or be specific)
- synergy, holistic, robust (consultant clichés without substance)

### Required Patterns

**Every metric needs context:**
- ❌ "40% cost reduction"
- ✅ "40% cost reduction ($2.1M annually)"
- ✅ "40% cost reduction (vs. 15% industry average)"

**Before/after always paired:**
- ❌ "Reduced processing time"
- ✅ "Processing time: 4 months → 6 weeks"

**Timeframes explicit:**
- ❌ "Rapid implementation"
- ✅ "Implemented in 6 weeks"
- ✅ "Live within Q1 2026"

**Specificity over generality:**
- ❌ "Multiple systems"
- ✅ "9 legacy Hybris instances across 4 regions"

### Sentence Structure

- **Short sentences.** 15-20 words max. One idea per sentence.
- **Active voice.** Subject-verb-object. "CI&T deployed" not "was deployed by CI&T."
- **Front-load the point.** Lead with the conclusion, then support it.
- **Parallel structure.** Lists use consistent grammar: all verbs, all nouns, all phrases.

### Challenge Section Formula

Pattern: [Scale of problem] + [Concrete pain points] + [Business impact]

❌ "The client had old systems that were difficult to manage and causing problems."

✅ "Nine divergent B2B platforms. €2M annual maintenance. Zero cross-OpCo visibility.
   HEINEKEN's fragmented commerce stack blocked their global harmonization strategy."

### Solution Section Formula

Pattern: [What was built] + [How it's different] + [Key technical insight]

❌ "CI&T built a solution using AI to help with the discovery process."

✅ "AI-first discovery methodology. Claude agents analyzed 500K lines of legacy code,
   capturing 60% of business rules before the first SME interview. Result: 6-week
   cycles instead of 4-month marathons."

## Step 1: Understand the full story

Before writing anything, answer these questions:

1. **What's the core narrative?**
   - What was the client's pain?
   - What did CI&T uniquely deliver?
   - What's the headline result?

2. **What's the single most impressive metric?**
   - This goes in the title and/or KPI block

3. **What content is duplicated across files?**
   - Pick the best-phrased version

4. **What's missing that we need to ask the user?**
   - Quote, ACR, revenue, etc.

## Step 2: Craft the narratives

Apply the executive-grade writing standard above. Every sentence must earn its place.

**Title** (≤15 words)
- Lead with client name, then metric-driven outcome
- Pattern: "[CLIENT]: [Quantified outcome] + [How]"
- ❌ "HEINEKEN: CI&T Helps with B2B Platform Modernization"
- ✅ "HEINEKEN: 75% Faster Discovery Through AI-Augmented Code Analysis"

**Subtitle** — Generate TWO versions (~40 words each):

`subtitle_internal` (for CI&T audience):
- Lead with CI&T's delivery + methodology
- Include deal value or strategic win context
- ✅ "CI&T landed a €236K engagement to harmonize HEINEKEN's fragmented B2B stack
   using AI-augmented discovery. Nine OpCos scoped. Six-week cycles. 60% of
   business rules captured before SME interviews — enabling premium pricing."

`subtitle_partner` (for Partner audience):
- Lead with partner services + cloud value
- Include ACR or consumption drivers
- ✅ "Azure-powered AI discovery harmonized HEINEKEN's fragmented B2B commerce
   across nine OpCos. Six-week analysis cycles. 60% of business rules pre-captured.
   Platform migration unlocks $1.2M ACR on Azure."

**Challenge headline** (≤8 words)
- Quantify the pain
- ❌ "Old systems causing problems"
- ✅ "Nine platforms. €2M maintenance. Zero visibility."

**Challenge body** — Generate TWO versions:

`body_internal` (for CI&T audience):
- Same client pain + "what this meant for CI&T"
- End with services opportunity or competitive win angle
- ✅ "HEINEKEN operated 9 divergent SAP Hybris instances — some over a decade old.
   No shared catalog. No unified pricing. The fragmentation consumed €2M annually
   and created a €500K discovery engagement opportunity for CI&T."

`body_partner` (for Partner audience):
- Same client pain + "what this meant for cloud consumption"
- End with cloud opportunity or services adoption angle
- ✅ "HEINEKEN operated 9 divergent SAP Hybris instances — some over a decade old.
   No shared catalog. No unified pricing. The fragmentation blocked Azure migration
   and $1.2M in annual cloud consumption potential."

**Solution headline** (≤8 words)
- The differentiator, not generic description
- ❌ "A modern solution using AI"
- ✅ "AI reads the code before humans do"

**Solution body** — Generate TWO versions:

`body_internal` (for CI&T audience):
- What CI&T delivered + methodology + delivery excellence
- Emphasize CI&T's differentiation and value
- ✅ "CI&T deployed our AI-augmented discovery methodology — Claude agents
   reverse-engineered 500K lines of Hybris code, pre-capturing 60% of business
   rules. This cut SME sessions by 70% and enabled premium fixed-fee pricing.
   Each OpCo: 6 weeks, not 4 months."

`body_partner` (for Partner audience):
- What [Partner] services enabled + cloud architecture + consumption drivers
- Emphasize partner's technology value and adoption
- ✅ "Azure-native AI services powered the discovery — Claude on Azure OpenAI
   analyzed 500K lines of legacy code, pre-capturing 60% of business rules.
   The modernized Virto Commerce platform runs on Azure Kubernetes Service,
   driving $1.2M ACR across compute, storage, and AI services."

**Quote** (if found)
- Must sound like a real executive said it — not marketing copy
- Include specific outcomes mentioned
- If none found, flag as missing
- ❌ "CI&T was an amazing partner and we loved working with them!"
- ✅ "The AI-first approach changed how we think about discovery. We went from
   dreading the SME marathon to actually enjoying focused sessions." — VP Digital, HEINEKEN

**Technologies**
- Deduplicated, ordered by strategic importance
- Lead with differentiators, not commodities

**Tags** (4-6)
- Pattern: [Industry], [Transformation type], [Key differentiator], [Tech]
- ❌ ["Technology", "Digital", "Cloud", "AI"]
- ✅ ["B2B Commerce", "Platform Harmonization", "AI-Augmented Discovery", "Hybris → Virto"]

## Step 3: Build page 2 candidates (the user picks the final blocks)

Page 2 ships ONE block per side. **You do not pick the final blocks — the user does.**
Your job is to produce **6 candidate "executive success pitches" per side** so the user
has real choices, not pre-decided defaults.

Page 2 must be SCANNABLE IN 30 SECONDS. Apply these hard limits to every candidate:

| Constraint | Limit |
|------------|-------|
| **Final blocks rendered** | **ONE per side** (user-picked) |
| **Candidates produced** | **6 per side** (or as many as the source material supports, min 3) |
| Timeline items | MAX 4 |
| Comparison items | MAX 2 |
| Takeaway bullets | MAX 3, each ≤8 words |
| Highlights items | MAX 3 |
| Any item detail | ≤10 words |

**Eligible block types per side (disjoint sets):**
- LEFT side candidates: `takeaway`, `timeline`, `roi`, `risks`
- RIGHT side candidates: `comparison`, `kpi`, `metrics`, `proof-points`

The two sets do not overlap, so whichever pair the user picks automatically gives the
page two different block types.

**How to craft 6 candidates per side:**

1. **Vary by block type AND by angle.** Cover at least 2 different block types from the
   eligible set on each side. Within a type, vary the *argument* — different metric
   framing, different audience hook (CFO vs. CTO vs. partner exec), different narrative
   (cost story, speed story, capability story, risk story).
2. **Each candidate is a fully-formed pitch**, not a stub. Apply the executive-grade
   writing standard: concrete numbers, no banned words, active voice, client as hero.
3. **Score the source pools first** (concrete numbers +2, before/after data +2, executive
   insight +2, dates/phases +1, multiple items +1) and lead with the highest-scoring
   angles.
4. **No filler.** If genuinely fewer than 6 strong candidates exist on a side, return
   what you have (minimum 3) and add a `notes` field explaining why.

**Block type guidance:**
- `takeaway`: Executive "so what" — compelling insight with 3 bullet proof points
- `kpi`: Single hero metric with trend — your most impressive number
- `comparison`: Before/after — strongest when you have concrete transformation data
- `timeline`: Project phases — use if 3-4 clear phases with outcomes
- `metrics`: Multiple numbers — use if you have 2-4 strong metrics
- `highlights`: Achievements — concrete wins with detail
- `proof-points`: Evidence — certifications, validations, awards
- `roi`: Investment vs. return — concrete inputs and outputs
- `risks`: Risk management — documented risk/mitigation pairs

**Synthesize, don't just copy:**
- Combine related content from multiple files
- Rewrite for conciseness (meet word limits)
- Pick the best version of duplicated content

## Step 4: Build tech_architecture

Fixed 3x2 grid at bottom of page 2. Six cards:

| Category | What to include |
|----------|-----------------|
| Compute / Platform | Main platform, runtime, containers |
| Data / Storage | Databases, storage, data services |
| Integration / Events | APIs, messaging, event systems |
| Security / Compliance | Auth, encryption, compliance |
| Observability | Monitoring, logging, tracing |
| CI/CD / Delivery | Build, deploy, DevOps tools |

If a category has nothing, use a generic description based on the project type.

## Output format

Return valid JSON with VERSION-SPECIFIC fields for subtitle, challenge body, and solution body:

{
  "project": {
    "client_name": "HEINEKEN International B.V.",
    "anonymize": false,
    "industry": "Consumer Goods / Beverage",
    "partner": "azure",
    "project_type": "B2B Commerce Harmonization",
    "title": "HEINEKEN: AI-Powered Discovery Cuts B2B Harmonization from Months to 6 Weeks",
    "subtitle_internal": "CI&T landed a €236K engagement to harmonize HEINEKEN's fragmented B2B stack using AI-augmented discovery. Nine OpCos scoped. Six-week cycles. Premium fixed-fee pricing enabled.",
    "subtitle_partner": "Azure-powered AI discovery harmonized HEINEKEN's fragmented B2B commerce across nine OpCos. Six-week cycles. Platform migration unlocks $1.2M ACR on Azure.",
    "tags": ["B2B Commerce", "AI-Augmented Discovery", "Platform Harmonization"]
  },
  
  "challenge": {
    "headline": "Nine fragmented platforms, one global vision",
    "body_internal": "HEINEKEN operated 9 divergent SAP Hybris instances — some over a decade old. No shared catalog. No unified pricing. The fragmentation consumed €2M annually and created a €500K discovery engagement opportunity for CI&T.",
    "body_partner": "HEINEKEN operated 9 divergent SAP Hybris instances — some over a decade old. No shared catalog. No unified pricing. The fragmentation blocked Azure migration and $1.2M in annual cloud consumption potential."
  },
  
  "solution": {
    "headline": "AI agents that read code before humans",
    "body_internal": "CI&T deployed our AI-augmented discovery methodology — Claude agents reverse-engineered 500K lines of Hybris code, pre-capturing 60% of business rules. This cut SME sessions by 70% and enabled premium fixed-fee pricing.",
    "body_partner": "Azure-native AI services powered the discovery — Claude on Azure analyzed 500K lines of legacy code, pre-capturing 60% of business rules. The modernized Virto platform runs on AKS, driving $1.2M ACR.",
    "technologies": ["SAP Hybris", "Virto Commerce", "Azure", "Anthropic Claude"]
  },
  
  "metrics_internal": {
    "items": [
      {"value": "€236K", "label": "Services Revenue"},
      {"value": "69 days", "label": "Deal Cycle"},
      {"value": "€700K+", "label": "Follow-on Pipeline"}
    ]
  },
  
  "metrics_partner": {
    "items": [
      {"value": "$X.XM", "label": "Annual Cloud Revenue"},
      {"value": "50-60%", "label": "Rules Pre-Captured by AI"},
      {"value": "6 weeks", "label": "Discovery per OpCo"}
    ]
  },
  
  "quote": {
    "text": "...",
    "author": "Name",
    "title": "Title",
    "company": "Company"
  },
  
  "context_bar_internal": [
    {"label": "Engagement Start", "value": "January 2026"},
    {"label": "Contract Structure", "value": "Fixed-fee + T&M"},
    {"label": "OpCos Covered", "value": "Brazil, Mexico"},
    {"label": "Team", "value": "Principal + LATAM delivery"}
  ],
  
  "context_bar_partner": [
    {"label": "Cloud Platform", "value": "Microsoft Azure"},
    {"label": "Discovery Duration", "value": "6 Weeks/OpCo"},
    {"label": "AI Licenses", "value": "12× Anthropic Claude"},
    {"label": "Scope", "value": "Hybris → Virto Migration"}
  ],
  
  "page2": {
    "include": true,
    "title": "Deep Dive: HEINEKEN B2B Commerce Harmonization",
    "blocks": [],
    "candidates": {
      "left": [
        {
          "type": "takeaway",
          "headline": "AI rewrites the discovery playbook",
          "bullets": ["50-60% rules pre-captured", "6-week cycles", "SME load cut 70%"]
        },
        {
          "type": "takeaway",
          "headline": "Premium pricing through methodology",
          "bullets": ["Fixed-fee enabled by AI scope confidence", "€236K landed, €700K pipeline", "Replicable across 9 OpCos"]
        },
        {
          "type": "timeline",
          "title": "AI-augmented discovery rollout",
          "items": [
            {"phase": "Week 1-2", "detail": "Code analysis (500K LoC)"},
            {"phase": "Week 3-4", "detail": "Business rule extraction"},
            {"phase": "Week 5-6", "detail": "SME validation sessions"}
          ]
        },
        {
          "type": "timeline",
          "title": "5-OpCo phased deployment",
          "items": [
            {"phase": "Q1 2026", "detail": "Brazil discovery complete"},
            {"phase": "Q2 2026", "detail": "Mexico discovery in flight"},
            {"phase": "Q3-Q4 2026", "detail": "Remaining 3 OpCos planned"}
          ]
        },
        {
          "type": "roi",
          "headline": "€500K invested → €1.2M ACR (2.4x)",
          "investment": "€500K discovery engagement",
          "return": "€1.2M projected annual cloud revenue"
        },
        {
          "type": "risks",
          "title": "3 risks identified, 3 mitigations deployed",
          "items": [
            {"risk": "Legacy code opacity", "mitigation": "AI reverse-engineering"},
            {"risk": "SME availability", "mitigation": "Async pre-capture"},
            {"risk": "Scope creep", "mitigation": "Fixed-fee discipline"}
          ]
        }
      ],
      "right": [
        {
          "type": "comparison",
          "title": "Discovery Transformation",
          "items": [
            {"label": "Duration", "before": "Months", "after": "6 weeks", "change": "↓75%"},
            {"label": "SME Load", "before": "Multi-day", "after": "4-8 hours", "change": "↓70%"}
          ]
        },
        {
          "type": "comparison",
          "title": "Cost Structure",
          "items": [
            {"label": "Maintenance", "before": "€2M/yr", "after": "€0", "change": "Legacy retired"},
            {"label": "Cloud", "before": "$0", "after": "$1.2M", "change": "New ACR"}
          ]
        },
        {
          "type": "kpi",
          "value": "60%",
          "label": "Business Rules Pre-Captured by AI",
          "context": "vs. 0% with traditional discovery"
        },
        {
          "type": "kpi",
          "value": "$1.2M",
          "label": "Annual Cloud Revenue Unlocked",
          "context": "Recurring Azure consumption across compute + AI"
        },
        {
          "type": "metrics",
          "items": [
            {"value": "$1.2M", "label": "Annual Cloud Revenue"},
            {"value": "6", "label": "Azure services adopted"},
            {"value": "9", "label": "OpCos modernized"}
          ]
        },
        {
          "type": "proof-points",
          "items": [
            {"label": "Azure MAP 2.0 funding approved"},
            {"label": "HEINEKEN exec sponsorship secured"},
            {"label": "LATAM delivery model certified"}
          ]
        }
      ],
      "notes": "All 6 candidates produced for both sides."
    },
    "tech_architecture": [
      {"category": "Commerce Platforms", "description": "SAP Hybris (legacy) → Virto Commerce (.NET)"},
      {"category": "AI Layer", "description": "Anthropic Claude for code analysis and generation"},
      {"category": "Cloud Platform", "description": "Microsoft Azure (target)"},
      {"category": "Integration", "description": "Salesforce SFA/SFDC, ERP connectors"},
      {"category": "Delivery Model", "description": "US Principal + LATAM nearshore team"},
      {"category": "Methodology", "description": "AI-enhanced discovery, artifacts-first approach"}
    ]
  },
  
  "logos": {
    "client_logo_url": ""
  },
  
  "missing": ["Client quote not found", "ACR not specified"]
}

## Quality checklist before outputting

- [ ] Title includes a metric
- [ ] Challenge and solution are 2-4 sentences each, concrete
- [ ] `page2.candidates.left` has 6 entries (or as many as the source supports, min 3)
- [ ] `page2.candidates.right` has 6 entries (or as many as the source supports, min 3)
- [ ] Left candidates use only `takeaway`, `timeline`, `roi`, or `risks`
- [ ] Right candidates use only `comparison`, `kpi`, `metrics`, or `proof-points`
- [ ] Each side covers at least 2 different block types across its 6 candidates
- [ ] Each candidate makes a distinct "so what" — no near-duplicates
- [ ] `page2.blocks` is left empty (the user fills it by picking)
- [ ] Timeline candidates have ≤4 items, each detail ≤10 words
- [ ] Comparison candidates have ≤2 items (even grid)
- [ ] Takeaway candidates have ≤3 bullets, each ≤8 words
- [ ] Tech architecture has 6 cards
- [ ] Missing items flagged in "missing" array
```

## Handling the output

After synthesis returns:

1. Check `missing` array — ask user for any critical items
2. Present `page2.candidates.left[]` and `page2.candidates.right[]` to the user as a
   numbered list (6 left + 6 right). Ask them to reply with picks (e.g., "Left 2, Right 5").
   See SKILL.md Step 2c for the exact presentation format.
3. Apply the user's picks to `page2.blocks` (set `column: "left"` on the left pick and
   `column: "right"` on the right pick). Drop `page2.candidates` from the data passed to
   `build_html.py`.
4. Present the consolidated content preview (now including the chosen page 2 blocks).
5. Get approval before building HTML/PDF.
