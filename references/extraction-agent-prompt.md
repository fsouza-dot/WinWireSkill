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

## User-provided context

The user has already provided these highlights in their template:
- Challenge summary: {challenge_user_highlights}
- Solution summary: {solution_user_highlights}
- Client: {client_name}
- Industry: {industry}
- Partner: {partner}
- Project type: {project_type}

Use these as anchors — find supporting details, metrics, and quotes that reinforce this story.

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

### MEDIUM (page 2 — depth)

9. **Page 2 left section** — Pick the BEST content type based on what makes this project impressive:

   | Type | When to Use | What to Extract |
   |------|-------------|-----------------|
   | `milestones` | Project had impressive timeline/speed | Key dates + achievements |
   | `challenges` | Complex technical problems solved | Problem + solution pairs |
   | `innovation` | Novel approach, first-of-its-kind | What was new + why it matters |
   | `scale` | Impressive numbers (users, TPS, data) | Big metrics with before/after |
   | `integration` | Connected many systems | Systems/services connected |
   | `compliance` | Regulatory/security achievements | Certifications + timeline |
   | `speed` | Notably fast delivery | Week-by-week milestones |
   | `phases` | Generic fallback | Discovery, build, migrate, optimize |

   **Selection logic:** Score each type by how much compelling content you find. Pick the type with the richest, most impressive story. Sales teams want concrete achievements that help them sell — prioritize types with hard numbers and clear wins.

10. **Before/after metrics**
    - Any quantitative improvements: throughput, latency, cost, uptime, deployment frequency
    - Look in: results sections, KPIs, SLAs, performance reports

11. **Tech architecture details**
    - How specific services were used, design patterns, security approach
    - Group into: Compute, Data, Events, Security, Observability, CI/CD

## Output format

Return valid JSON only — no markdown, no explanation:

{
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
  "page2_left": {
    "type": "challenges|milestones|innovation|scale|integration|compliance|speed|phases",
    "title": "Section title (e.g., 'Challenges Conquered', 'Scale Achieved')",
    "items": [
      {"headline": "Short punchy headline", "detail": "Supporting detail or number"},
      ...
    ]
  },
  "metrics_table": [
    {"metric": "What measured", "before": "Old value", "after": "New value"},
    ...
  ],
  "tech_architecture": [
    {"category": "Category name", "description": "How it was used"},
    ...
  ],
  "missing": ["List any CRITICAL items you could not find"]
}
```

## Handling Results

After the agent returns:

1. **Merge with template data** — template values (user input) take priority over extracted values
2. **Check `missing` array** — if CRITICAL items missing, ask user directly
3. **Review narratives** — the agent drafts headlines/body; you refine for WinWire tone
4. **Fill gaps** — use extracted data to enhance user's challenge/solution highlights
