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
5. Ensure page 2: ONE block per side, different types
6. Output final JSON ready for build_html.py

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

**Subtitle** (2-3 sentences, ~40 words)
- Sentence 1: What CI&T delivered + primary outcome
- Sentence 2: Scope and scale
- Sentence 3: Strategic significance (optional)
- ❌ "CI&T worked with HEINEKEN to help them modernize their B2B platform using AI."
- ✅ "CI&T deployed AI-first discovery to harmonize HEINEKEN's fragmented B2B commerce
   stack. Nine OpCos. Six weeks per analysis cycle. 60% of business rules captured
   before SME interviews began."

**Challenge headline** (≤8 words)
- Quantify the pain
- ❌ "Old systems causing problems"
- ✅ "Nine platforms. €2M maintenance. Zero visibility."

**Challenge body** (2-4 sentences)
- Sentence 1: Scale and specifics (numbers, ages, counts)
- Sentence 2: Concrete pain points
- Sentence 3: Business impact / strategic blocker
- ❌ "The client had multiple legacy systems that were hard to manage."
- ✅ "HEINEKEN operated 9 divergent SAP Hybris instances across operating companies —
   some over a decade old. No shared catalog. No unified pricing logic. The
   fragmentation blocked their global B2B harmonization roadmap and consumed €2M
   annually in redundant maintenance."

**Solution headline** (≤8 words)
- The differentiator, not generic description
- ❌ "A modern solution using AI"
- ✅ "AI reads the code before humans do"

**Solution body** (2-4 sentences)
- Sentence 1: What was built/deployed (specific)
- Sentence 2: What makes it different (the insight)
- Sentence 3: Key technical decision or methodology
- ❌ "CI&T built a solution using AI to analyze code and help with discovery."
- ✅ "CI&T deployed Claude-powered agents to reverse-engineer legacy Hybris codebases,
   extracting business rules directly from source. The AI pre-captured 60% of
   functional requirements — transforming SME sessions from exhaustive interviews
   into focused gap-filling. Each OpCo analysis: 6 weeks, not 4 months."

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

## Step 3: Build page 2 content

Page 2 must be SCANNABLE IN 30 SECONDS. Apply these hard limits:

| Constraint | Limit |
|------------|-------|
| **Total blocks** | **ONE per side** (2 total) |
| Timeline items | MAX 4 |
| Comparison items | MAX 2 |
| Takeaway bullets | MAX 3, each ≤8 words |
| Highlights items | MAX 3 |
| Any item detail | ≤10 words |

**Selection priority — focus on BUSINESS IMPACT:**
1. Pick the 2 most impactful block types from what you found
2. Prioritize blocks with concrete numbers showing business value
3. `comparison` (before/after) and `kpi` (hero metric) are strongest for impact
4. `takeaway` is good for executive summary if you have compelling insight

**ONE block per side — non-negotiable:**
- LEFT side: pick ONE from `takeaway`, `timeline`, `roi`, or `risks`
- RIGHT side: pick ONE from `comparison`, `kpi`, `metrics`, or `proof-points`
- NO EXCEPTIONS. One block left, one block right. That's it.

**Block selection logic:**
- `takeaway`: Executive "so what" — compelling insight with 3 bullet proof points
- `kpi`: Single hero metric with trend — your most impressive number
- `comparison`: Before/after — strongest when you have concrete transformation data
- `timeline`: Project phases — use if 3-4 clear phases with outcomes
- `metrics`: Multiple numbers — use if you have 2-4 strong metrics
- `highlights`: Achievements — concrete wins with detail
- `proof-points`: Evidence — certifications, validations, awards
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

Return valid JSON matching the build_html.py schema:

{
  "project": {
    "client_name": "HEINEKEN International B.V.",
    "anonymize": false,
    "industry": "Consumer Goods / Beverage",
    "partner": "azure",
    "project_type": "B2B Commerce Harmonization",
    "title": "HEINEKEN: AI-Powered Discovery Cuts B2B Harmonization from Months to 6 Weeks",
    "subtitle": "CI&T landed a €236K engagement to re-engineer fragmented B2B SAP Hybris platforms...",
    "tags": ["B2B Commerce", "AI-Augmented Discovery", "Platform Harmonization"]
  },
  
  "challenge": {
    "headline": "Nine fragmented platforms, one global vision",
    "body": "HEINEKEN operates divergent B2B e-commerce stacks across operating companies..."
  },
  
  "solution": {
    "headline": "AI agents that read code before humans",
    "body": "CI&T deployed an AI-enhanced discovery methodology...",
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
    "blocks": [
      {
        "type": "takeaway",
        "column": "left",
        "headline": "AI rewrites the discovery playbook",
        "bullets": ["50-60% rules pre-captured", "6-week cycles", "SME load cut 70%"]
      },
      {
        "type": "comparison",
        "column": "right",
        "title": "Discovery Transformation",
        "items": [
          {"label": "Duration", "before": "Months", "after": "6 weeks", "change": "↓75%"},
          {"label": "SME Load", "before": "Multi-day", "after": "4-8 hours", "change": "↓70%"}
        ]
      }
    ],
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
- [ ] Page 2 has ONE block per side (left and right)
- [ ] Blocks chosen for maximum business impact
- [ ] Left and right columns use DIFFERENT block types
- [ ] Timeline has ≤4 items, each detail ≤10 words
- [ ] Comparison has ≤2 items (even grid)
- [ ] Takeaway has ≤3 bullets, each ≤8 words
- [ ] Tech architecture has 6 cards
- [ ] Missing items flagged in "missing" array
```

## Handling the output

After synthesis returns:

1. Check `missing` array — ask user for any critical items
2. Present consolidated content preview to user
3. Get approval before building HTML/PDF
