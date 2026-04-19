# Document Extraction Agent Prompt

Use this prompt template when spawning the Haiku agent to extract WinWire content from attached documents.

## Agent Configuration

```
Agent({
  description: "Extract WinWire content from project docs",
  model: "haiku",
  prompt: <see template below>
})
```

## Prompt Template

```
You are extracting content from project documents to build a WinWire — a branded success story combining a deal announcement with a mini case study.

## Your task

Read ALL attached documents and extract the content listed below. Synthesize across documents to find the most compelling version of each item. Prioritize storytelling quality — choose details that make the project's impact vivid and concrete.

## Extraction modes

**Standard mode** (template provided) — User has already provided project identity in template:
- Challenge summary: {challenge_user_highlights}
- Solution summary: {solution_user_highlights}
- Client: {client_name}
- Industry: {industry}
- Partner: {partner}
- Project type: {project_type}

Use these as anchors — find supporting details, metrics, and quotes that reinforce this story.

**Full extraction mode** (`full_extraction: true`) — No template provided. Extract EVERYTHING
from docs, including project identity. Look for:
- **Client name** — SOW headers, footers, contract parties, "prepared for [client]"
- **Industry** — Context clues, regulatory mentions, business domain
- **Partner** — Which cloud? AWS/GCP/Azure service names reveal this
- **Project type** — "migration", "modernization", "platform", "data" in titles/summaries

## Extract these items

### CRITICAL (page 1 — must find or flag as missing)

1. **Revenue figures**
   - Services Revenue / TCV / ACV / deal size (for internal version)
   - Annual Cloud Revenue / ACR / cloud spend (for partner version)
   - Look in: SOW pricing, deal desk docs, partner registrations, executive summaries

2. **Challenge narrative**
   - What problem did the client face? Business impact? Urgency?
   - Find concrete details: system age, scale limits, compliance gaps, cost issues
   - Look in: executive summary, problem statement, current state analysis

3. **Solution narrative**
   - What did CI&T build? Architecture approach? Methodology?
   - Find specifics: patterns used, services deployed, delivery approach
   - Look in: technical approach, proposed solution, architecture sections

4. **Technologies**
   - List ALL specific cloud services, tools, frameworks mentioned
   - e.g., Amazon EKS, Lambda, DynamoDB, Terraform, ArgoCD
   - Look in: architecture docs, technical approach, diagrams (captions)

5. **Client quote**
   - Any direct quote, testimonial, or feedback from client stakeholders
   - Look in: emails, feedback docs, case study drafts, NPS comments

### HIGH (page 1 — strong impact)

6. **Title suggestion**
   - Draft a title with a key metric (e.g., "3x Transaction Throughput")
   - Base it on the most impressive outcome you find

7. **Subtitle suggestion**
   - 2-3 sentence overview of the engagement and results

8. **Tags**
   - Infer from: industry, partner, project type, technologies
   - e.g., ["Cloud Migration", "Microservices", "AWS", "FinTech"]

### MEDIUM (page 2 — flexible content blocks)

Page 2 uses a flexible block system. Extract whatever compelling content you find and return
it as blocks. Don't force content into rigid categories — if it doesn't exist, skip it.

**Block types available:**

| Type | When to Use | What to Extract |
|------|-------------|-----------------|
| `metrics` | Quantitative wins (numbers that impress) | Value + label pairs |
| `highlights` | Key achievements, challenges solved | Headline + detail pairs |
| `comparison` | Before/after improvements | Label + before + after |
| `list` | Technologies, deliverables, phases | Simple string list |
| `narrative` | Methodology, approach context | Prose paragraph |
| `quote` | Additional testimonials | Text + author + title |

**Selection logic:**
- Only include blocks with REAL content found in docs
- Prioritize content that helps sales teams sell (hard numbers, clear wins)
- 2-4 blocks is ideal; don't pad with weak content
- If nothing compelling for page 2, return empty blocks array (page 2 will be skipped)

**Column hints:**
- `"column": "left"` — appears in left column
- `"column": "right"` — appears in right column  
- `"column": "full"` — spans full width (good for tech lists)
- Omit column to let the system distribute evenly

## Output format

Return valid JSON only — no markdown, no explanation:

{
  "project_identity": {
    "client_name": "Extracted client name (full extraction mode only)",
    "industry": "Inferred industry",
    "partner": "aws|gcp|azure (based on services mentioned)",
    "project_type": "e.g., Cloud Migration, Data Platform"
  },
  "revenue": {
    "services_revenue": "$X.XM or null if not found",
    "acr": "$X.XM or null if not found"
  },
  "challenge": {
    "headline": "Short punchy headline",
    "body": "2-4 sentences with concrete details"
  },
  "solution": {
    "headline": "Short punchy headline",
    "body": "2-4 sentences with specifics",
    "technologies": ["Service1", "Service2", "..."]
  },
  "quote": {
    "text": "The quote text or null",
    "author": "Name or null",
    "title": "Role or null"
  },
  "title": "Suggested title with metric",
  "subtitle": "2-3 sentence overview",
  "tags": ["Tag1", "Tag2", "..."],
  "page2": {
    "include": true,
    "title": "Deep Dive: [Client] [Project Type]",
    "blocks": [
      {
        "type": "metrics",
        "title": "Business Impact",
        "column": "left",
        "items": [
          {"value": "3.8K TPS", "label": "Transaction Throughput"},
          {"value": "99.99%", "label": "Uptime"}
        ]
      },
      {
        "type": "highlights",
        "title": "Key Achievements",
        "column": "right",
        "items": [
          {"headline": "Zero-Downtime Migration", "detail": "2TB moved live"},
          {"headline": "PCI Compliant", "detail": "Certified in 3 weeks"}
        ]
      },
      {
        "type": "comparison",
        "title": "Before & After",
        "column": "left",
        "items": [
          {"label": "Deployment", "before": "Monthly", "after": "Daily"},
          {"label": "Latency", "before": "1200ms", "after": "180ms"}
        ]
      },
      {
        "type": "list",
        "title": "Technologies",
        "column": "full",
        "items": ["EKS", "Lambda", "DynamoDB", "EventBridge"]
      }
    ]
  },
  "missing": ["List any CRITICAL items you could not find"]
}
```

## Handling Results

After the agent returns:

1. **Merge with template data** — template values (user input) take priority over extracted values
2. **Check `missing` array** — if CRITICAL items missing, ask user directly
3. **Review narratives** — the agent drafts headlines/body; you refine for WinWire tone
4. **Fill gaps** — use extracted data to enhance user's challenge/solution highlights
