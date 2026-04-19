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

3. **Spawn an extraction agent** with the discovered file paths explicitly listed:

   ```
   Agent({
     description: "Extract WinWire content from project docs",
     model: "haiku",
     prompt: `
       <paste full prompt from references/extraction-agent-prompt.md>
       
       ## Files to read
       
       Read ALL of the following files using the Read tool. Do not skip any.
       After reading all files, extract the content as specified above.
       
       - /path/to/file1.pdf
       - /path/to/file2.docx
       - /path/to/file3.pptx
       ... (list ALL discovered files)
     `
   })
   ```

   **CRITICAL:** You MUST include the full list of discovered file paths at the end of the prompt.
   The extraction agent cannot discover files on its own — it can only read paths you give it.
   If you don't include the file list, the agent will have nothing to read.

   The agent reads all files, synthesizes across them, and returns structured JSON with raw
   content pools. See `references/extraction-agent-prompt.md` for the full prompt template.

4. **Merge results.** Template values (user input) always take priority over extracted values.
   Check the agent's `missing` array — if CRITICAL items are missing, ask the user directly.

### Step 2b: Docs-only flow (no template)

If the user provided documents but no template, use "full extraction mode":

1. **Discover all documents** in the workspace folder recursively (same file types as Step 2).
   Tell the user what you found: "Found 8 documents. Reading them to extract WinWire content..."

2. **Spawn the extraction agent** with `full_extraction: true` AND the file list:

   ```
   Agent({
     description: "Extract WinWire content from project docs",
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

3. **Confirm inferred identity.** Present what the agent found:
   > "I found this in your docs:
   > - **Client:** [name]
   > - **Industry:** [industry]
   > - **Partner:** [aws/gcp/azure]
   > - **Project type:** [type]
   >
   > Is this correct?"

   Use `AskUserQuestion` with options: "Yes, correct" / "Fix something" / "Cancel"

4. **Ask for deal metrics.** These are rarely in project docs — ask directly:
   > "I need a few numbers that aren't typically in project docs:
   > 1. **Services Revenue** — total CI&T contract value (e.g., $3.2M)
   > 2. **Annual Cloud Revenue (ACR)** — recurring cloud spend (e.g., $1.2M)
   > 3. **Incentive Funding** — partner program funding received (e.g., $280K MAP 2.0)
   > 4. **Deal Cycle** — days from opportunity to close (e.g., 94 days)
   >
   > Please provide these, or type 'skip' for any you don't have."

5. **Create the data structure.** Combine agent-extracted content with user-provided metrics,
   then proceed to Step 2c (analyze raw pools for page 2 layout).

### Step 2c: Analyze raw content pools and select page 2 layout

The extraction agent returns raw content pools in `page2.raw`, not final blocks. Your job is
to analyze these pools and select the best layout with visual variety.

1. **Score each pool** for content quality:

   | Quality signal | Score boost | Good for |
   |----------------|-------------|----------|
   | Has concrete numbers | +2 | `kpi`, `metrics`, `comparison` |
   | Has before/after data | +2 | `comparison` |
   | Has dates/phases | +1 | `timeline` |
   | Has executive insight | +2 | `takeaway` |
   | Multiple items (3+) | +1 | more options |
   | Empty or single weak item | skip | — |

2. **Select block types** from strongest pools:

   | Pool | Best as | Fallback | Skip if |
   |------|---------|----------|---------|
   | `executive_insights` | `takeaway` | — | empty |
   | `hero_metrics` | `kpi` | `metrics` | no trend/context |
   | `metric_sets` | `metrics` | `highlights` | <2 items |
   | `achievements` | `highlights` | `proof-points` | empty |
   | `transformations` | `comparison` | `metrics` | no before/after |
   | `project_phases` | `timeline` | `highlights` | <3 phases |
   | `financial_analysis` | `roi` | skip | incomplete |
   | `validations` | `proof-points` | `highlights` | <2 items |
   | `risks_managed` | `risks` | skip | <2 pairs |

3. **Enforce content limits** — page 2 must be scannable in 30 seconds:

   | Constraint | Limit |
   |------------|-------|
   | Blocks per column | MAX 2 |
   | Timeline items | MAX 4 |
   | Comparison items | MAX 2 (even grid) |
   | Takeaway bullets | MAX 3, each ≤8 words |
   | Highlights items | MAX 3 |
   | Any item detail | ≤10 words |

   If raw pools have more items than limits allow, **select the best ones, not all**.
   A dense wall of text looks amateur. White space is professional.

4. **Assign columns ensuring variety**:

   - **Left column priority:** `takeaway`, `timeline`, `roi`, `risks`
   - **Right column priority:** `kpi`, `comparison`, `metrics`, `proof-points`
   - **HARD RULE:** Never same primary block type on both sides

5. **Present layout recommendation with alternatives** via `AskUserQuestion`:

   ```
   📊 Recommended page 2 layout:
   
   LEFT COLUMN:
   ├─ takeaway: "AI cuts discovery from months to weeks"
   │   • 60% context pre-captured
   │   • 4 parallel tracks
   │   • 9 OpCos unified
   └─ timeline: 4 project phases
       Discovery → Feature Gap → Migration Pilot → Augmentation
   
   RIGHT COLUMN:
   ├─ kpi: "60%" SME Context Pre-Captured (↓40% interview load)
   └─ comparison: 2 transformations
       Discovery: Months → 6-8 weeks (↓75%)
       SME Load: 12 sessions → 4-5 (↓60%)
   
   📦 Available alternatives (content found but not used):
   • highlights: 2 achievements with impact badges
   • proof-points: 3 validations
   • risks: 2 risk/mitigation pairs
   
   Options:
   - **Use recommended layout** ✓
   - **Swap a block** (tell me which)
   - **Add more blocks** (pick from alternatives)
   - **Skip page 2** (one-pager only)
   ```

6. **Apply user's choice** and proceed to Step 3 with the finalized blocks.

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
message. This is the preview the user will approve. It must include every piece of text and
every number that will appear in the WinWire:

- **Project identity** — client name (or anonymized name), industry, partner(s), project type, tags
- **Hero** — title, subtitle
- **Challenge** — headline, body
- **Solution** — headline, body, technology list
- **Metrics (internal)** — all three values and labels (Services Revenue must be present)
- **Metrics (partner)** — all three values and labels (Annual Cloud Revenue must be present), if building a partner version
- **Quote** — text, author, title, company
- **Context bar** — every label/value pair, for every version being produced
- **Page 2 (if included)** — left section content, business-outcome cards, tech architecture cards

Format it clearly — headings and prose, not raw JSON. The user needs to be able to scan and
point to what they want changed.

#### 🛑 Page 2 block variety — BLOCKING CHECK

Before showing the approval question, check if left and right columns use the same primary
block type. **If they do, you MUST resolve this with the user first — do not proceed to approval.**

Same block type on both sides = amateur document. This is a quality gate.

When block variety is violated:

1. **Flag the problem explicitly:**
   > "⚠️ Page 2 needs adjustment: both columns use 'highlights' blocks, which creates visual
   > monotony and looks unprofessional."

2. **Offer concrete alternatives:**
   > "I recommend restructuring for visual variety:
   > - **Left column:** `takeaway` (executive insight) + `timeline` (project phases)
   > - **Right column:** `kpi` (hero metric) + `comparison` (before/after transformation)
   >
   > This gives you: callout box, timeline dots, big number, transformation arrows — four
   > distinct visual patterns instead of two identical lists."

3. **Ask the user to choose** via `AskUserQuestion`:
   - Question: "How should I fix the page 2 layout?"
   - Options:
     - **Apply suggested restructure** (Recommended)
     - **Keep current layout anyway** (not recommended)
     - **Let me specify the block types**

4. **Only after the user responds**, proceed to the content approval question.

**Do NOT bundle this into a single "notes" section and continue.** Block variety must be
resolved as a separate interaction before content approval.

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
- **Block variety violations must be resolved BEFORE content approval.** Do not present the
  approval question if page 2 columns use the same primary block type — fix it first.

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

## Content extraction strategy

The extraction agent (Haiku) handles document analysis. See `references/extraction-agent-prompt.md`
for the full prompt template, priority tiers, and output schema.

**Priority tiers:**
- **CRITICAL**: Revenue figures, Challenge/Solution narratives, Technologies, Client quote
- **HIGH**: Title, Subtitle, Tags
- **MEDIUM**: Project phases, Before/after metrics, Tech architecture

The agent synthesizes across all attached documents to find the most compelling content for
storytelling. It returns structured JSON that you merge with template data.

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

## Writing tone for narratives you draft

When writing challenge/solution blocks, titles, or subtitles from user highlights and docs:

- **Confident but not boastful.** State results with numbers, let them speak.
- **Concrete over abstract.** "Tripled transaction throughput" not "significantly improved performance."
- **Short sentences in challenge/solution blocks.** These are scanned, not read deeply.
- **Quote should feel authentic.** If the user provides one, use it as-is. Never fabricate quotes.
- **Title should include a key metric.** "3x Transaction Throughput" or "40% Cost Reduction."

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
