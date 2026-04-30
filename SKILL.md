---
name: winwire-generator
description: >
  Generate polished CI&T WinWire documents — branded project success stories for internal teams
  and cloud partners (AWS, GCP, Azure). Produces self-contained HTML pages and print-fidelity PDFs.
  Use this skill whenever the user mentions: WinWire, win wire, win-wire, deal win, partner win,
  case study for a partner, project success story, or asks to create a branded project summary
  for AWS/GCP/Azure. Also trigger when the user has a filled-in WinWire spreadsheet/template
  and wants to generate the documents from it.
---

# WinWire Generator

You are an agent that produces polished, branded WinWire documents for CI&T. A WinWire is a
hybrid deal-win announcement and mini case study — shared internally to celebrate wins and
externally with cloud partners (AWS, GCP, Azure) to strengthen relationships.

## What you produce

For each project, you generate:

1. **CI&T Internal version** — focused on services revenue, deal cycle, incentive funding
2. **Partner-facing version(s)** — focused on cloud revenue (ACR), business outcomes, tech adoption
3. Each version ships as **self-contained HTML** (no external deps) + **PDF** (print-fidelity, content-fitted pages)

The design uses CI&T's brand system (Coral #FA5A50, Navy #000050, Playfair Display + DM Sans)
with partner color accents (not a full rebrand — the page always feels like a CI&T page).

## The one approval gate — read this before doing anything

This skill has **exactly one approval gate, and it is on the content**. Nothing else. Once the
user approves the consolidated content, every HTML and PDF (internal + all requested partner
versions) can be produced in one shot with no further stops.

### What the gate looks like

After you have (a) extracted content from the template and docs, (b) asked the user any
follow-up questions to fill gaps, and (c) received their answers — you MUST:

1. **Produce a single consolidated content preview.** This is the full, final text that will
   land in the WinWire — title, subtitle, tags, challenge headline + body, solution headline +
   body, technologies, quote, all three internal metrics, all three partner metrics, context
   bar items, and all page-2 content (phases, business-outcome cards, tech architecture
   cards). Present it as a clearly-formatted message so the user can scan and edit.

2. **Call `AskUserQuestion`** with options "Approve all — build the files", "Edit a section",
   "Cancel". Do NOT run any build script in the same turn as presenting the preview.

3. **Wait for the user's reply.** If they pick "Edit", loop back and update just that section,
   then re-present the full consolidated preview and re-ask. Only when they pick "Approve all"
   do you move to the build step.

### Critical failure mode to avoid

A common failure is: the skill asks gap-filling questions ("do you have a client quote?",
"what was the ACR?"), the user answers, and the skill immediately starts building files. That
skips the gate. **Answering a gap-filling question is not content approval.** After every
batch of Q&A, come back to the consolidated preview and the explicit approval question.

### After approval

Once the user approves, generate HTML + PDF for the internal version AND for every requested
partner version in the same turn — it's all automation at that point, no more stops. See
Step 4 for the exact build commands.

## Key design principle: minimize user effort

The simplified template only asks for what a human uniquely knows — deal numbers and a brief
challenge/solution summary. Everything else (polished narratives, tech details, page 2 phases,
architecture, quotes, tags) should be **extracted from attached project documents**. The user
should never have to type what's already written somewhere in their docs.

When you can't find something in the docs, **ask the user directly** — don't guess or fabricate.
Be specific about what's missing and why you need it.

## Non-negotiable rule: the revenue metric

Every WinWire MUST have a revenue metric among the three headline metric cards. This is the
number that makes the win tangible — without it, the document reads like a marketing blurb.

- **CI&T Internal version:** one of the three key metric cards MUST be **Services Revenue**
  (the contract value CI&T sold).
- **Partner-facing version:** one of the three key metric cards MUST be **Annual Cloud Revenue
  (ACR)** — the recurring cloud spend the partner will realize.

### How to enforce this at runtime

1. **First, check the template.** If the user filled in `Services Revenue` (internal) or
   `Annual Cloud Revenue (ACR)` (partner), you're done — use those values.
2. **If either is missing, mine the attached documents.** Look exhaustively for:
   - Total Contract Value (TCV), Annual Contract Value (ACV), deal size, booked revenue,
     services fees, professional services dollars → these may correspond to Services Revenue.
   - Annual Cloud Run-Rate, projected cloud consumption, ACR, cloud spend commit, workload
     migration dollars, monthly/yearly AWS/GCP/Azure bill estimates → these may correspond to ACR.
   Common locations: SOW pricing tables, deal desk approvals, partner registration forms, MAP
   applications, executive summaries, pipeline notes, email threads with commercial terms.
3. **If still missing, ask the user directly.** Use the AskUserQuestion tool. Be specific —
   e.g., "I couldn't find the Services Revenue (total CI&T contract value) in your docs. What
   was the deal size?"
4. **If the user says they don't have the number, warn them clearly** before proceeding:

   > ⚠ **Heads up:** without Services Revenue (internal) / Annual Cloud Revenue (partner),
   > this WinWire will be significantly weaker. These are the single most important numbers
   > for the audience — executives and partner stakeholders open the doc looking for them.
   > Publishing without them risks the WinWire being dismissed as unsubstantiated. Do you
   > still want to proceed, or would you like to pause and recover the number first?

   Only proceed after the user explicitly acknowledges the trade-off. If they proceed, render
   the metric card with a dash ("—") and label it anyway — an empty slot is more honest than
   rearranging the layout to hide the gap.

**Do not substitute a different metric into this slot.** Cost reduction, throughput, or
services-adopted numbers are valuable — but they belong in the *other two* metric slots, not
the revenue slot. The revenue slot is reserved.

## Partner logos (built into the skill)

The AWS, Google Cloud, and Microsoft Azure logos are shipped with the skill — they live in
`assets/partner-logos/` (`aws.svg`, `gcp.svg`, `azure.svg`) and are base64-inlined by
`build_html.py` at build time. **The user never supplies these.** Selecting the partner
(`aws` / `gcp` / `azure` in the template) is enough to render the correct logo in the topbar
on both the internal and partner versions, sitting between the CI&T mark and the optional
client logo.

If you ever see a missing-asset warning on stderr (`Warning: partner logo asset missing:
…`), it means the skill was packaged without its `assets/partner-logos/` folder — repackage
the .skill with the assets directory included.

## Client logo resolution flow

Every WinWire should have the client's logo in the topbar (alongside CI&T and the partner).
The CI&T logo and partner logo are both built into the skill. **You are responsible for the
client logo** — the user will not chase this themselves. Follow this ladder and do not skip
steps:

### Step 1 — Check the template

Read the `Client Logo URL` and `Client Logo File` fields from the template. If either is
populated:

- **URL present:** try to download it. Use Python's urllib (or `curl` via Bash) to fetch the
  bytes. Example:

  ```bash
  python3 - <<'PY'
  import urllib.request, sys, pathlib
  url = "<URL_FROM_TEMPLATE>"
  out = pathlib.Path("<WORKSPACE>/client-logo.<ext>")
  try:
      urllib.request.urlretrieve(url, str(out))
      print("OK", out)
  except Exception as e:
      print("FAIL", e); sys.exit(1)
  PY
  ```

  If the download fails (HTTP error, timeout, bad content type, 0 bytes): tell the user
  the URL didn't work and ask for a new URL or another way to get the logo (e.g., "can
  you attach the file directly?"). Do not silently skip.

  If the download succeeds, save it in the workspace folder. Pass its local path to
  `build_html.py` via `logos.client_logo_url` in the JSON — the script auto-base64-encodes
  local files so the HTML stays self-contained.

- **Client Logo File present:** use that filename. Look for it in the workspace folder; if
  found, use its local path. If the file name is given but not found, tell the user and ask
  them to confirm the filename or drop the file into the folder.

### Step 2 — Search the workspace folder for image files

If neither template field is populated, list image files in the same folder as the template:
`.png`, `.jpg`, `.jpeg`, `.svg`, `.webp`, `.gif`. Exclude the CI&T preview / partner preview
thumbnails that ship with this skill (`cit-preview-*`, `aws-preview-*`, `gcp-preview-*`,
`azure-preview-*`).

- **Zero candidates:** proceed to Step 3.
- **Exactly one candidate:** present it to the user and ask "Is this the client logo?"
  with a Yes / No option set.
- **Multiple candidates:** list them and ask the user which one is the client logo (or
  "none of these").

### Step 3 — Explicit confirmation before shipping logo-less

If Steps 1 and 2 have exhausted every path, call `AskUserQuestion`:

- Question: "I couldn't find a client logo. Do you want to proceed without one?"
- Options:
  - **Proceed without a client logo**
  - **Pause — I'll provide a logo** (user will paste a URL or attach a file)
  - **Cancel**

Only proceed with no client logo after the user explicitly picks "Proceed without". Do not
silently ship without a client logo — that was the failure mode we fixed.

### Passing the logo into build_html.py

In the JSON data, set `logos.client_logo_url` to one of:

- An `https://…` URL (kept as-is; the HTML will reference it externally).
- A `data:image/...;base64,…` URL (used as-is; self-contained).
- An absolute local path (read + base64-encoded by the script; self-contained — preferred).
- A filename relative to the JSON's directory (same behavior as absolute).

The script logs a warning to stderr if the path can't be resolved — watch for those.

## Cross-platform notes

This skill runs on Windows, macOS, and Linux. Path examples use forward slashes (`/`) for
readability, but the Python scripts use `pathlib.Path` internally and handle both separators.
When invoking scripts, use paths appropriate for your OS (e.g., `C:\Users\...` on Windows).

**Python command:** Always use `python3` (not `python`). This works on macOS, Linux, and
modern Windows Python installations.

## Workflow

Follow this sequence. The user stays in control of content decisions at every step.

### Step 1: Check for inputs

Look for a WinWire template (.xlsx) in the workspace folder. Also check for attached project
documents (SOWs, decks, PDFs, notes).

**Path A — Template found:** Proceed to Step 2 (template + docs flow).

**Path B — No template, but docs provided:** Proceed to Step 2b (docs-only flow). This is
faster for the user but requires Q&A for deal metrics.

**Path C — Neither template nor docs:** Generate a template for the user:

```bash
python3 <SKILL_DIR>/scripts/create_template.py --output <WORKSPACE>/winwire-template.xlsx
```

Present the template and explain: "Fill in the deal numbers and attach any project documents.
Or just drop your project docs here and I'll extract what I can and ask you for the rest."

**Wait for the user to return with either template or docs before proceeding.**

### Step 2: Read the template + extract from attached docs

Once the user provides the filled template and any supporting documents:

1. **Read the template** using openpyxl:
   ```bash
   python3 <SKILL_DIR>/scripts/ingest.py --template <path-to-xlsx> --output <WORKSPACE>/project-data.json
   ```

2. **Discover all documents** in the workspace folder recursively. Use Glob to find supported files:

   | Category | Extensions |
   |----------|------------|
   | Documents | `.pdf`, `.docx`, `.doc`, `.txt`, `.md`, `.rtf`, `.odt`, `.pages` |
   | Presentations | `.pptx`, `.ppt`, `.odp`, `.key` |
   | Spreadsheets | `.xlsx`, `.xls`, `.csv`, `.ods`, `.tsv`, `.numbers` |
   | Images | `.png`, `.jpg`, `.jpeg`, `.svg`, `.gif`, `.webp`, `.tiff` |
   | Web/Data | `.html`, `.htm`, `.xml`, `.json` |
   | Email | `.eml`, `.msg` |

   **Exclude:** `winwire-template.xlsx`, `winwire-*.html`, `winwire-*.pdf`, `project-data.json`,
   and folders like `.git`, `node_modules`, `__pycache__`, `.venv`.

   Tell the user what you found: "Found 12 documents across 4 folders. Reading them now..."

3. **Spawn Phase 1: Raw Extraction Agent** (Haiku) with the discovered file paths:

   ```
   Agent({
     description: "Extract raw WinWire content from project docs",
     model: "haiku",
     prompt: `
       <paste full prompt from references/extraction-agent-prompt.md>
       
       ## Files to read
       
       Read ALL of the following files using the Read tool. Do not skip any.
       
       - /path/to/file1.pdf
       - /path/to/file2.docx
       - /path/to/file3.pptx
       ... (list ALL discovered files)
     `
   })
   ```

   **CRITICAL:** You MUST include the full list of discovered file paths at the end of the prompt.
   The extraction agent cannot discover files on its own — it can only read paths you give it.

   Phase 1 returns a raw dump of ALL potentially relevant content organized by source file:
   - `by_source[]`: Each file's extracted content (revenue figures, challenges, solutions, etc.)
   - `cross_file_observations`: Notes on duplicates, complements, and conflicts
   - `best_sources`: Which file is best for each content type
   - `gaps`: What's missing that we need to ask the user

   See `references/extraction-agent-prompt.md` for the full prompt template and output schema.

4. **Phase 2: Synthesis** (main agent handles this directly):

   With the raw extraction in hand, YOU now synthesize it into the final WinWire content.
   This gives you the advantage of seeing ALL content from ALL files at once, allowing you to:
   
   - Pick the best-phrased version of duplicated content
   - Combine complementary info across files into coherent narratives
   - Make intelligent selections (not just mechanical picking)
   - Craft compelling headlines from notable phrases across documents
   
   Follow the synthesis approach in `references/synthesis-agent-prompt.md`:
   
   a. **Understand the full story first:**
      - What's the core narrative? (pain → unique delivery → headline result)
      - What's the single most impressive metric?
      - What content is duplicated across files? (pick best version)
      - What's missing that you need to ask the user?
   
   b. **Craft the narratives** in WinWire tone (confident, concrete, short sentences):
      - Title (≤15 words, include key metric)
      - Subtitle (2-3 sentences)
      - Challenge headline (≤8 words) + body (2-4 sentences)
      - Solution headline (≤8 words) + body (2-4 sentences)
      - Technologies (deduplicated, ordered by importance)
      - Tags (4-6 tags)
   
   c. **Build page 2 content** from the raw pools, respecting content limits.
   
   **When to spawn a Sonnet agent instead:**
   - Very large extraction (>50KB raw content)
   - Main agent context is already large
   - Need fresh perspective on synthesis
   
   See `references/synthesis-agent-prompt.md` for the full synthesis prompt template.

5. **Merge with template.** Template values (user input) always take priority over synthesized values.
   Check the Phase 1 `gaps` array — if CRITICAL items are missing, ask the user directly.

### Step 2b: Docs-only flow (no template)

If the user provided documents but no template, use "full extraction mode":

1. **Discover all documents** in the workspace folder recursively (same file types as Step 2).
   Tell the user what you found: "Found 8 documents. Reading them to extract WinWire content..."

2. **Spawn Phase 1: Raw Extraction Agent** with `full_extraction: true` AND the file list:

   ```
   Agent({
     description: "Extract raw WinWire content from project docs",
     model: "haiku",
     prompt: `
       <extraction prompt with full_extraction: true>
       
       ## Files to read
       
       Read ALL of the following files. Do not skip any.
       
       - /path/to/file1.pdf
       - /path/to/file2.docx
       ... (list ALL discovered files)
     `
   })
   ```

   **CRITICAL:** Include the full file list. The agent cannot discover files on its own.
   
   With `full_extraction: true`, the agent also extracts project identity (client name,
   industry, partner, project type) that would normally come from the template.

3. **Phase 2: Synthesis** — Same as Step 2 item 4. You (the main agent) synthesize the raw
   extraction into polished WinWire content. See `references/synthesis-agent-prompt.md`.

4. **Confirm inferred identity.** Present what you synthesized:
   > "I found this in your docs:
   > - **Client:** [name]
   > - **Industry:** [industry]
   > - **Partner:** [aws/gcp/azure]
   > - **Project type:** [type]
   >
   > Is this correct?"

   Use `AskUserQuestion` with options: "Yes, correct" / "Fix something" / "Cancel"

5. **Ask for deal metrics.** These are rarely in project docs — ask directly:
   > "I need a few numbers that aren't typically in project docs:
   > 1. **Services Revenue** — total CI&T contract value (e.g., $3.2M)
   > 2. **Annual Cloud Revenue (ACR)** — recurring cloud spend (e.g., $1.2M)
   > 3. **Incentive Funding** — partner program funding received (e.g., $280K MAP 2.0)
   > 4. **Deal Cycle** — days from opportunity to close (e.g., 94 days)
   >
   > Please provide these, or type 'skip' for any you don't have."

6. **Create the data structure.** Combine synthesized content with user-provided metrics,
   then proceed to Step 2c (analyze raw pools for page 2 layout).

### Step 2c: Generate page 2 candidates and let the user pick

Page 2 always renders **ONE block per side**. The skill does NOT decide which block ships —
the user does. Your job in this step is to craft **6 candidate "executive success pitches"
per side** and present them so the user can pick one for the left column and one for the
right column.

This is a deliberate design choice: each candidate is a fully-formed pitch tuned to a
different angle of the story, and the user is the best judge of which angle resonates with
their audience. Never auto-select on the user's behalf.

#### Block type sets (disjoint by side)

| Side | Eligible block types |
|------|----------------------|
| LEFT | `takeaway`, `timeline`, `roi`, `risks` |
| RIGHT | `comparison`, `kpi`, `metrics`, `proof-points` |

The two sets are disjoint, so whichever pair the user picks automatically satisfies
"different block types per side" — no extra enforcement needed.

#### How to craft the 6 candidates per side

Synthesize across the raw `by_source[]` pools to produce candidates that read like
**executive success pitches** — not generic block fills. Each candidate should make a
*different argument* about why this win matters, so the user has six meaningful choices,
not six near-duplicates.

For each side:

1. **Score the available pools** (concrete numbers +2, before/after data +2, executive
   insight +2, dates/phases +1, multiple items with 3+ entries +1).

2. **Generate 6 distinct candidates.** Vary by **block type** AND by **angle**:
   - Cover at least 2 different block types from the eligible set (e.g., 3 `takeaway`
     variations + 2 `timeline` variations + 1 `roi` on the left).
   - Each candidate should pitch a *different* "so what" — different metric framing,
     different audience hook (CFO vs. CTO vs. partner exec), different narrative angle
     (cost story, speed story, capability story, risk story).
   - Apply the executive-grade writing standard from
     `references/synthesis-agent-prompt.md`: concrete numbers, no banned words, active
     voice, client as hero.

3. **Respect content limits per block** (timeline ≤4 items, comparison ≤2 items, takeaway
   ≤3 bullets each ≤8 words, highlights ≤3 items, any item detail ≤10 words).

4. **If fewer than 6 strong candidates exist for a side**, present what you have (minimum
   3) and tell the user explicitly: "I could only craft N strong candidates for the [left|right]
   side because [reason — e.g., docs lacked before/after metrics]." Do **not** pad with
   weak filler just to hit 6.

#### Presenting the candidates

Show all 12 candidates (6 left + 6 right) in a single message, each numbered and clearly
labeled with its block type. Format:

```
📊 PAGE 2 CANDIDATES — pick one from each side

═══ LEFT COLUMN ═══

L1. [takeaway] "AI cuts discovery from months to weeks"
    • 60% rules pre-captured before SME interviews
    • 6-week cycles vs 4-month marathons
    • SME load reduced 70%

L2. [timeline] AI-augmented discovery rollout
    Week 1-2: Code analysis (500K LoC)
    Week 3-4: Business rule extraction
    Week 5-6: SME validation sessions

L3. [takeaway] "Premium pricing through methodology differentiation"
    • Fixed-fee enabled by AI-driven scope confidence
    • €236K landed; €700K pipeline opened
    • Replicable across 9 OpCos

L4. [roi] €500K invested → €1.2M projected ACR (2.4x)

L5. [risks] 3 risks identified, 3 mitigations deployed
    • Legacy code opacity → AI reverse-engineering
    • SME availability → async pre-capture
    • Scope creep → fixed-fee discipline

L6. [timeline] 5-OpCo phased deployment
    ...

═══ RIGHT COLUMN ═══

R1. [comparison] Discovery Transformation
    Duration: Months → 6 weeks (↓75%)
    SME Load: Multi-day → 4-8 hours (↓70%)

R2. [kpi] 60% — Business Rules Pre-Captured by AI
    (vs. 0% with traditional discovery)

R3. [metrics] Three impact numbers
    • $1.2M Annual Cloud Revenue
    • 6 Azure services adopted
    • 9 OpCos modernized

R4. [proof-points] Three external validations
    • Azure MAP 2.0 funding approved
    • HEINEKEN exec sponsorship secured
    • LATAM delivery model certified

R5. [comparison] Cost Structure
    Maintenance: €2M/yr → €0 (legacy retired)
    Cloud: $0 → $1.2M (new ACR)

R6. [kpi] $1.2M — Annual Cloud Revenue Unlocked
    (recurring Azure consumption across compute + AI)
```

Then ask the user for their picks in plain text:

> Reply with your picks — e.g., **"Left 2, Right 5"**. If none of the candidates on a
> side feel right, tell me which angle you'd prefer and I'll regenerate that side.

**Why free text instead of `AskUserQuestion`:** `AskUserQuestion` caps at 4 options per
question, but we need 6. Splitting into multiple 4-option questions or forcing the user
through "Other" makes the interaction worse. A numbered list + free-text reply is cleaner.

#### Apply the picks

Once the user picks one from each side:

1. Add the two chosen blocks to the data structure as `page2.blocks`, with `column:
   "left"` and `column: "right"` set correctly.
2. Discard the unpicked candidates.
3. Proceed to Step 3 (content gate).

If the user replies with only one pick (e.g., "Left 2") and no right pick, ask for the
missing side before continuing. If the user wants entirely different candidates on a side
("none of these — give me something more about partner enablement"), regenerate just that
side and re-present its 6 candidates while keeping the other side's list intact.

### Step 3: Refine the summary and present for approval

The user's challenge and solution highlights from the template are a starting point — not
final copy. Your job is to **refine them into polished WinWire-ready narratives**, combining
the user's bullet points with whatever you found in the attached docs.

For each summary section (challenge and solution), do the following:

1. **Start with what the user wrote** in the template. This is their intent — the core message
   they want to convey.
2. **Enrich with doc content.** Add concrete details, specific numbers, technology names, or
   business context found in attached documents. The user's highlights tell you *what* to say;
   the docs tell you *how to say it well*.
3. **Write a refined version** in WinWire tone: confident, concrete, short sentences. Challenge
   should be 2-4 sentences about the pain. Solution should be 2-4 sentences about what CI&T built.
4. **Draft a headline** for each (e.g., "A monolith blocking growth" / "Event-driven microservices on AWS").
5. **Draft a title and subtitle** for the hero section if the user didn't provide one. The title
   should include a key metric. The subtitle is a 2-3 sentence overview.

Then present everything to the user, showing your refinements clearly:

- **What you wrote** → the refined challenge headline + body
- **What you started from** → "Based on your highlights: [their original text]"
- **What you added from docs** → "Enhanced with details from [document name]"

Do the same for the solution, title, subtitle, quote, tech list, and all other sections.

**For anything you couldn't find, ask the user directly.** Be specific:
- "I couldn't find a client quote in your docs. Do you have one, or should I leave the quote section out?"
- "The docs mention DynamoDB and EKS but I'm not sure about the full tech stack. Can you confirm which services were used?"
- "I didn't find before/after metrics for page 2. Do you have numbers for things like throughput, latency, deployment frequency?"

**Do not fabricate content.** If you don't have it and the user can't provide it, skip the
section (for optional content) or ask the user to provide it (for required content).

Also confirm **which versions** the user wants built: internal only, or internal + one or more
partners (aws / gcp / azure). You need this answer before you reach the approval step so the
preview reflects what's actually going to ship.

#### 🛑 The content gate — consolidated preview + approval (STOP HERE)

Once every gap is filled (all Q&A is answered, all missing metrics recovered, user picked
which versions to produce), **STOP and show the full consolidated content** in a single
message. This is the preview the user will approve.

**Format the preview to show SHARED content and VERSION-SPECIFIC angles clearly:**

```
📋 CONTENT PREVIEW

═══ SHARED (client-outcome focused) ═══

Title: "HEINEKEN: 75% Faster Discovery Through AI-Augmented Analysis"

Challenge headline: "Nine platforms. €2M maintenance. Zero visibility."

Solution headline: "AI agents that read code before humans"

Technologies: [Azure, Claude, Virto Commerce, SAP Hybris]

Tags: [B2B Commerce, Platform Harmonization, AI-Augmented Discovery]

Quote: "The AI-first approach changed how we think about discovery..."
       — VP Digital, HEINEKEN

═══ CI&T INTERNAL VERSION ═══

Subtitle: "CI&T landed a €236K engagement to harmonize HEINEKEN's 
fragmented B2B stack using AI-augmented discovery..."

Challenge angle: "...created a €500K discovery engagement opportunity for CI&T."

Solution angle: "CI&T deployed our AI-augmented methodology...enabled 
premium fixed-fee pricing."

Metrics: €236K Services Revenue | 69 days Deal Cycle | €700K Pipeline

═══ PARTNER VERSION (Azure) ═══

Subtitle: "Azure-powered AI discovery harmonized HEINEKEN's fragmented 
B2B commerce...Platform migration unlocks $1.2M ACR."

Challenge angle: "...blocked Azure migration and $1.2M in annual cloud 
consumption potential."

Solution angle: "Azure-native AI services powered the discovery...driving 
$1.2M ACR across compute, storage, and AI services."

Metrics: $1.2M ACR | 6 Azure Services | 60% Faster Discovery

═══ PAGE 2 ═══
[Left block] + [Right block] + Tech Architecture
```

The user approves BOTH versions in one gate. They can edit either angle separately.

#### 🛑 Page 2 sanity check

Before showing the approval question, verify:

1. `page2.blocks` has **exactly two entries** — one with `column: "left"`, one with
   `column: "right"`.
2. The left block's type is in `{takeaway, timeline, roi, risks}` and the right block's
   type is in `{comparison, kpi, metrics, proof-points}`.

If either condition fails, you skipped Step 2c — go back and run the candidate-and-pick
flow before continuing. Do not improvise the page 2 layout.

(Block-type variety between sides is guaranteed by the disjoint sets, so there is no
separate "different types" check needed once Step 2c is followed.)

#### Content approval question

Then, in the SAME message (but AFTER the preview), **call `AskUserQuestion`**:

- Question: "Approve this content and build the WinWire files?"
- Options:
  - **Approve — build all files** (Recommended)
  - **Edit a section first**
  - **Cancel**

**Hard rules at this gate:**

- Do NOT run any build script in the same turn as presenting the preview. The `AskUserQuestion`
  call ends the turn; the build happens in the next turn after the user answers.
- Answering a gap-filling question is **not** content approval. Every time the user answers a
  batch of questions, you must come back with the full consolidated preview and re-ask the
  approval question. Do not shortcut straight to building.
- If the user picks "Edit", update just that section, then present the full preview again and
  re-ask the approval question. Don't build anything in between.
- If the user's message is ambiguous ("looks good" / "ok" / "sure") without picking one of the
  three options, re-ask the approval question explicitly — don't assume.
- **Page 2 picks must be in `page2.blocks` before approval.** If you forgot Step 2c (the
  6-candidate pick), do that first — do not present the approval question with auto-picked
  blocks.

### Step 4: Build everything (only after the content gate passes)

Once the user picks "Approve — build all files", generate HTML + PDF for the internal version
and every requested partner version, all in this single step. No further approval stops.

> **Never re-implement the rendering.** `scripts/build_html.py` is the only supported way to
> produce a WinWire HTML. Do **not** read the template HTML files under `assets/` and populate
> them by hand, and do **not** generate HTML from scratch — the script handles theming,
> base64-inlined logos, reserved metric slots, and page-2 fitting that hand-rolled output
> will silently get wrong. If a `Read` of `scripts/build_html.py` looks truncated or
> malformed, that is a tool-layer display artifact, not a broken file — invoke the script
> anyway and if it actually errors at runtime, surface the stderr to the user and stop.

1. Internal HTML:

   ```bash
   python3 <SKILL_DIR>/scripts/build_html.py \
     --data <path-to-data.json> \
     --version internal \
     --template-dir <SKILL_DIR>/assets \
     --output <WORKSPACE>/winwire-cit-internal.html
   ```

2. Internal PDF:

   ```bash
   python3 <SKILL_DIR>/scripts/build_pdf.py \
     --html <WORKSPACE>/winwire-cit-internal.html \
     --output <WORKSPACE>/winwire-cit-internal.pdf
   ```

3. For each requested partner (aws, gcp, azure), build both HTML and PDF:

   ```bash
   python3 <SKILL_DIR>/scripts/build_html.py \
     --data <path-to-data.json> \
     --version partner \
     --partner aws \
     --template-dir <SKILL_DIR>/assets \
     --output <WORKSPACE>/winwire-aws-partner.html

   python3 <SKILL_DIR>/scripts/build_pdf.py \
     --html <WORKSPACE>/winwire-aws-partner.html \
     --output <WORKSPACE>/winwire-aws-partner.pdf
   ```

Batching these build commands in parallel is fine — they're automation, no decisions involved.

### Step 5: Deliver all files

Present every HTML and PDF produced in Step 4 to the user with `present_files`.

If after reviewing the rendered outputs the user asks for content changes, loop all the way
back to the content gate — update the content, re-present the consolidated preview, re-ask for
approval, then rebuild.

## Content extraction strategy (2-phase architecture)

Content extraction uses a 2-phase architecture for better cross-file synthesis:

### Phase 1: Raw Extraction (Haiku agent)

A lightweight Haiku agent reads ALL files and extracts ALL potentially relevant content in
loose categories. It does NOT make final decisions — just captures everything that MIGHT be
useful. See `references/extraction-agent-prompt.md` for the full prompt template.

**Output structure:**
- `by_source[]`: Each file's extracted content (revenue, challenges, solutions, metrics, quotes, technologies, etc.)
- `cross_file_observations`: Notes on duplicates, complementary info, and conflicts
- `best_sources`: Which file is best for each content type
- `gaps`: What's missing (quote, ACR, incentive funding, etc.)

### Phase 2: Synthesis (main agent or Sonnet)

You (the main agent) receive the raw extraction and synthesize it into polished WinWire content.
This gives you the advantage of seeing ALL content from ALL files at once, allowing intelligent
narrative construction rather than mechanical selection.

**Key synthesis tasks:**
- Understand the full story before writing anything
- Pick the best-phrased version of duplicated content
- Combine complementary info into coherent narratives
- Craft compelling headlines from notable phrases
- Build page 2 blocks respecting content limits

See `references/synthesis-agent-prompt.md` for the full synthesis approach.

**When to spawn Sonnet instead:**
- Very large extraction (>50KB raw content)
- Main agent context is already large
- Need fresh perspective on synthesis

## Content and design references

Before generating any HTML, read these reference files for detailed guidance:

- `references/content-guide.md` — Content structure, JSON data format, metrics by version,
  writing tone guidelines, page 1 vs page 2 content rules
- `references/partner-themes.md` — Partner color schemes, logo handling, label differences
  per partner, how branding accents work

## Important design principles

- **Page 1 is the star.** Everything essential goes on page 1: hero, challenge/solution,
  key metrics, quote, context bar. Page 2 is an optional deep-dive.
- **Content-fitted PDFs.** Pages are sized to their content — no fixed A4 with whitespace.
  The build_pdf.py script handles this automatically.
- **Self-contained HTML.** No external dependencies except Google Fonts (with system fallbacks).
  Logos are embedded as base64 SVGs or downloaded and inlined.
- **CI&T brand first, partner accents second.** The layout and typography are always CI&T.
  Partners get color accents (topbar tag pill, metric values, tech card headers) and a
  co-branded logo bar — not a full visual overhaul.

## Writing Standard: Executive-Grade Content

WinWires must read like McKinsey case studies or Deloitte client success stories — 
executive-ready, board-presentable. Not internal documentation. Not marketing fluff.

See `references/synthesis-agent-prompt.md` for the complete writing guide. Key principles:

### Do This

- **Outcome first.** "40% cost reduction through platform consolidation"
- **Quantify everything.** "6 weeks vs. 4 months (75% acceleration)"
- **Client as hero.** "[Client] achieved 3x throughput"
- **Context for metrics.** "40% reduction ($2.1M annually)"
- **Explicit timeframes.** "Delivered in 6 weeks"
- **Short sentences.** 15-20 words max. One idea per sentence.
- **Active voice.** "CI&T deployed" not "was deployed by CI&T"

### Never Do This

- **Banned words:** amazing, incredible, significant, very, really, helped, worked on,
  cutting-edge, state-of-the-art, leverage, synergy, holistic, robust
- **Vague claims:** "Significantly improved" → use actual numbers
- **Passive voice:** "The solution was implemented" → "CI&T implemented"
- **Generic descriptions:** "Multiple systems" → "9 legacy Hybris instances across 4 regions"

### Formula: Challenge Section

[Scale] + [Pain points] + [Business impact]

❌ "The client had old systems that were difficult to manage."
✅ "Nine divergent platforms. €2M annual maintenance. Zero cross-OpCo visibility."

### Formula: Solution Section

[What was built] + [What's different] + [Key insight]

❌ "CI&T built a solution using AI to help with discovery."
✅ "AI-first discovery captured 60% of business rules before the first SME interview."

## Script dependencies

The scripts require these Python packages. Install them if not already available:

```bash
pip3 install openpyxl playwright pypdf
playwright install chromium
```

On Linux with system Python, you may need `--break-system-packages` or use a virtual environment.

## Anonymized versions

If the user sets "Anonymize?" to YES in the template, pass `--anonymize` to build_html.py.
This replaces the client name with the anonymized descriptor throughout.
