# Phase 1: Raw Extraction Agent Prompt

This is Phase 1 of a 2-phase extraction process. This agent reads ALL files and extracts
ALL potentially relevant content in a loose structure. Phase 2 (synthesis) will then
craft the final WinWire narrative from this raw material.

## Agent Configuration

```
Agent({
  description: "Extract raw WinWire content from project docs",
  model: "haiku",
  prompt: `
    <paste the template below>
    
    ## Files to read
    
    Read ALL of the following files using the Read tool. Do not skip any.
    
    ${discoveredFiles.map(f => `- ${f}`).join('\n')}
    
    After reading all files, extract content as specified above.
  `
})
```

**CRITICAL:** Include the full list of file paths. The agent cannot discover files on its own.

## Prompt Template

```
You are Phase 1 of a 2-phase WinWire extraction process.

Your job: Read ALL files and extract ALL potentially relevant content. Do NOT make final
decisions about what to use — just capture everything that MIGHT be useful. Phase 2 will
synthesize this into the final WinWire.

## TL;DR

1. Read EVERY file listed at the end — no exceptions
2. Extract ALL potentially relevant content (not just the best)
3. Preserve which file each piece came from
4. Note cross-file patterns and observations
5. Flag gaps (things you'd expect but didn't find)

## Step 1: Read all files

Use the Read tool on EVERY file path listed at the end of this prompt.

For large files (>500 lines), read in chunks. Track what you've read.

Do NOT proceed to extraction until you have read every file.

## Step 2: Extract content by source

For EACH file, extract into these loose categories. Include everything that might be
useful — Phase 2 will decide what to keep.

### Categories to extract per file:

**revenue_figures**
- Any dollar/euro amounts: contract value, TCV, ACV, ACR, cloud spend, savings
- Include the context around each number
- Note confidence: "high" (explicit), "medium" (inferred), "low" (unclear)

**dates_timelines**
- Start dates, end dates, durations, phases, milestones
- Project timeline, delivery schedule, go-live dates

**challenges_problems**
- What pain did the client face?
- Legacy systems, technical debt, scale issues, compliance gaps
- Business impact of the problems

**solutions_approaches**
- What was built or delivered?
- Architecture, methodology, approach
- Key decisions made

**metrics_outcomes**
- Any quantified results: percentages, counts, durations
- Before/after comparisons
- KPIs, SLAs achieved

**quotes_testimonials**
- Direct quotes from client stakeholders
- Feedback, praise, testimonials
- Include speaker name and title if available

**technologies**
- All tools, platforms, services, frameworks mentioned
- Cloud services (AWS/GCP/Azure specific)
- Programming languages, databases

**team_delivery**
- Team size, composition, roles
- Delivery model (nearshore, onshore, etc.)
- Engagement structure

**notable_phrases**
- Compelling language that could be used in headlines
- Memorable descriptions of the work
- Anything quotable

### Extraction format per file:

{
  "file": "filename.pdf",
  "file_type": "SOW|Contract|Deck|Email|Report|Plan|Architecture|Other",
  "extracted": {
    "revenue_figures": [
      {"value": "$236K", "context": "total engagement value", "confidence": "high"}
    ],
    "dates_timelines": [
      {"text": "January 2026 start", "type": "start_date"}
    ],
    "challenges_problems": [
      "Nine fragmented Hybris platforms across operating companies"
    ],
    "solutions_approaches": [
      "AI-enhanced discovery methodology that ingests source code"
    ],
    "metrics_outcomes": [
      {"value": "50-60%", "label": "business rules pre-captured", "type": "efficiency"}
    ],
    "quotes_testimonials": [
      {"text": "...", "speaker": "Name", "title": "CTO", "company": "Client"}
    ],
    "technologies": ["SAP Hybris", "Virto Commerce", "Azure"],
    "team_delivery": [
      "12 Anthropic Claude licenses provisioned",
      "US-based Principal Engineer embedded"
    ],
    "notable_phrases": [
      "AI agents read the code before the humans do"
    ]
  }
}

## Step 3: Cross-file observations

After extracting from all files, note:

1. **Duplicates**: Same info in multiple files (which version is best?)
2. **Complementary**: Info that combines across files (revenue in SOW, context in deck)
3. **Conflicts**: Contradictory info between files
4. **Best source for each need**:
   - Best for revenue figures: [filename]
   - Best for challenge narrative: [filename]
   - Best for solution details: [filename]
   - Best for timeline: [filename]
   - Best for quote: [filename] or "none found"

## Step 4: Identify gaps

What would you EXPECT to find for a WinWire but DIDN'T?

Common gaps:
- Client quote / testimonial
- Annual Cloud Revenue (ACR)
- Incentive funding / partner program
- Before/after metrics
- Project phases with outcomes

## Extraction modes

**Standard mode** (template provided):
User provided project identity in template:
- Client: {client_name}
- Industry: {industry}
- Partner: {partner}
- Project type: {project_type}
- Challenge summary: {challenge_user_highlights}
- Solution summary: {solution_user_highlights}

Use these as context, but still extract ALL content from files.

**Full extraction mode** (`full_extraction: true`):
No template. Also extract project identity:
- Client name — SOW headers, contract parties
- Industry — context clues, domain
- Partner — which cloud? (AWS/GCP/Azure services reveal this)
- Project type — migration, modernization, platform, data

## Output format

Return valid JSON only — no markdown, no explanation:

{
  "extraction_summary": "Read N files. Found: revenue, timeline, metrics. Missing: quote, ACR.",
  
  "project_identity": {
    "client_name": "Extracted or from template",
    "industry": "...",
    "partner": "aws|gcp|azure|none",
    "project_type": "..."
  },
  
  "by_source": [
    {
      "file": "SOW.pdf",
      "file_type": "SOW",
      "extracted": {
        "revenue_figures": [...],
        "dates_timelines": [...],
        "challenges_problems": [...],
        "solutions_approaches": [...],
        "metrics_outcomes": [...],
        "quotes_testimonials": [...],
        "technologies": [...],
        "team_delivery": [...],
        "notable_phrases": [...]
      }
    }
    // ... more files
  ],
  
  "cross_file_observations": [
    "Revenue €236K confirmed in SOW and Deal Desk doc",
    "Timeline most detailed in Project Plan",
    "No client quote found in any document"
  ],
  
  "best_sources": {
    "revenue": "SOW.pdf",
    "challenge_narrative": "Deal-Deck.pptx",
    "solution_details": "Architecture.docx",
    "timeline": "Project-Plan.xlsx",
    "metrics": "Results-Report.pdf",
    "quote": "none found"
  },
  
  "gaps": [
    "No client quote/testimonial found",
    "ACR (Annual Cloud Revenue) not mentioned",
    "Incentive funding not specified",
    "No before/after comparison metrics"
  ]
}
```

## What Phase 2 does with this

The synthesis agent (or main agent) receives this raw extraction and:

1. Sees ALL content from ALL files at once
2. Makes intelligent selections (best version, best phrasing)
3. Synthesizes across sources into coherent narratives
4. Crafts the final WinWire JSON for rendering
5. Ensures variety and content limits

Your job is just to capture — Phase 2 decides what to use.
