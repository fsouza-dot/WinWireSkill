#!/usr/bin/env python3
"""Generate WinWire HTML from JSON data.

Takes a data JSON file and produces a self-contained HTML page — either the CI&T
internal version or a partner-facing version (AWS, GCP, Azure). The HTML is fully
self-contained (fonts via Google Fonts link, logos as base64/inline SVG).

Usage:
    python build_html.py --data project.json --version internal --template-dir ../assets --output winwire-internal.html
    python build_html.py --data project.json --version partner --partner aws --template-dir ../assets --output winwire-aws.html
"""

import argparse
import base64
import json
import mimetypes
import re
import sys
from datetime import datetime
from pathlib import Path
from html import escape

# ── Partner logo assets (built into the skill, not user-provided) ─────────────

# Logos live next to this script, under ../assets/partner-logos/. They are loaded
# once at import time and base64-inlined into the HTML so the output stays fully
# self-contained. See SKILL.md "Partner logos" — the user never needs to supply
# these; they're shipped with the skill.

_PARTNER_LOGO_FILES = {
    "aws": "aws.svg",
    "gcp": "gcp.svg",
    "azure": "azure.svg",
}

_PARTNER_LOGO_CACHE = {}


def _load_partner_logo(partner_key):
    """Return an <img> tag with the partner logo as a base64-inlined data URL.

    If the SVG file is missing (e.g., the skill was packaged without assets),
    falls back to a minimal text SVG so the output still renders — but logs a
    warning so we notice the missing asset.
    """
    if partner_key in _PARTNER_LOGO_CACHE:
        return _PARTNER_LOGO_CACHE[partner_key]

    filename = _PARTNER_LOGO_FILES.get(partner_key)
    if not filename:
        _PARTNER_LOGO_CACHE[partner_key] = ""
        return ""

    # Logos live at <repo>/assets/partner-logos/<file>.svg relative to this script.
    logo_path = Path(__file__).resolve().parent.parent / "assets" / "partner-logos" / filename
    try:
        svg_bytes = logo_path.read_bytes()
        b64 = base64.b64encode(svg_bytes).decode("ascii")
        alt = {"aws": "AWS", "gcp": "Google Cloud", "azure": "Microsoft Azure"}.get(partner_key, partner_key.upper())
        tag = f'<img class="topbar-logo topbar-logo-partner" src="data:image/svg+xml;base64,{b64}" alt="{alt}">'
        _PARTNER_LOGO_CACHE[partner_key] = tag
        return tag
    except (OSError, FileNotFoundError) as e:
        print(f"Warning: partner logo asset missing: {logo_path} ({e})", file=sys.stderr)
        fallback = f'<span class="topbar-logo-partner-fallback">{partner_key.upper()}</span>'
        _PARTNER_LOGO_CACHE[partner_key] = fallback
        return fallback


# ── Partner theme definitions ──────────────────────────────────────────────────

PARTNER_THEMES = {
    "aws": {
        "name": "AWS",
        "color": "#FF9900",
        "color_dark": "#E68A00",
        "color_muted": "rgba(255, 153, 0, 0.10)",
        "color_surface": "#FFF5E6",
        "solution_label": "AWS-Powered Solution",
        "tech_title": "AWS Services Adopted",
        "approach_title": "Migration Approach",
        "metrics_title": "Business Outcomes",
        "page2_title_suffix": "AWS Services & Business Outcomes",
        "footer_prefix": "CI&T & AWS",
    },
    "gcp": {
        "name": "Google Cloud",
        "color": "#4285F4",
        "color_dark": "#3367D6",
        "color_muted": "rgba(66, 133, 244, 0.10)",
        "color_surface": "#EBF3FE",
        "solution_label": "Google Cloud Solution",
        "tech_title": "Google Cloud Services",
        "approach_title": "Migration Approach",
        "metrics_title": "Business Outcomes",
        "page2_title_suffix": "Google Cloud & Business Outcomes",
        "footer_prefix": "CI&T & Google Cloud",
    },
    "azure": {
        "name": "Azure",
        "color": "#0078D4",
        "color_dark": "#005A9E",
        "color_muted": "rgba(0, 120, 212, 0.10)",
        "color_surface": "#E6F2FB",
        "solution_label": "Azure-Powered Solution",
        "tech_title": "Azure Services Adopted",
        "approach_title": "Migration Approach",
        "metrics_title": "Business Outcomes",
        "page2_title_suffix": "Azure Services & Business Outcomes",
        "footer_prefix": "CI&T & Microsoft Azure",
    },
}

# ── CI&T logo as base64 SVG ───────────────────────────────────────────────────

CIT_LOGO_B64 = (
    "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz4NCjwhLS0gR2VuZXJhdG9yOiBBZG9i"
    "ZSBJbGx1c3RyYXRvciAyNi4wLjIsIFNWRyBFeHBvcnQgUGx1Zy1JbiAuIFNWRyBWZXJzaW9uOiA2LjAw"
    "IEJ1aWxkIDApICAtLT4NCjxzdmcgdmVyc2lvbj0iMS4xIiBpZD0iTGF5ZXJfMl8wMDAwMDA4NDUxOTUx"
    "MTIxMDU4NjU4MzQ0MDAwMDAwNTI1MzMyNTg5NDAxNzYxNTAzOF8iDQoJIHhtbG5zPSJodHRwOi8vd3d3"
    "LnczLm9yZy8yMDAwL3N2ZyIgeG1sbnM6eGxpbms9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGxpbmsi"
    "IHg9IjBweCIgeT0iMHB4IiB2aWV3Qm94PSIwIDAgNTEyIDE2NSINCgkgc3R5bGU9ImVuYWJsZS1iYWNr"
    "Z3JvdW5kOm5ldyAwIDAgNTEyIDE2NTsiIHhtbDpzcGFjZT0icHJlc2VydmUiPg0KPHN0eWxlIHR5cGU9"
    "InRleHQvY3NzIj4NCgkuc3Qwe2ZpbGw6I0ZBNUE1MDt9DQo8L3N0eWxlPg0KPGcgaWQ9IkxheWVyXzEt"
    "MiI+DQoJPHBhdGggY2xhc3M9InN0MCIgZD0iTTAsODIuOUMwLDMxLjQsMzYuNiwwLjQsODYuMywwLjRj"
    "NDAuMiwwLDcxLjgsMTkuOSw4MSw1OS4yaC0zOC41Yy00LjQtMjQuMS0xOC42LTQxLjQtNDEuOS00MS40"
    "DQoJCWMtMjguMywwLTQ1LjIsMjYuNi00NS4yLDU5LjdjMCwzNy43LDE4LjgsNjEuMyw1MS4xLDYxLjNj"
    "MjkuMSwwLDQ3LjktMTguOCw1My4yLTQ3LjloMjIuNGMtNi4zLDQ1LjItMzcuOSw3My43LTg0LjgsNzMu"
    "Nw0KCQlDMzMuMSwxNjUsMCwxMzEuNSwwLDgyLjl6Ii8+DQoJPHBhdGggY2xhc3M9InN0MCIgZD0iTTE3"
    "Ni43LDE2MC44YzcuNS01LjksOS4yLTE1LjMsOS4yLTMxLjhWMzUuOGMwLTE3LTEuNy0yNi05LjItMzEu"
    "OFYzLjFoNThWNGMtNy41LDUuOS05LjIsMTQuOS05LjIsMzEuOFYxMjkNCgkJYzAsMTYuNSwxLjcsMjYs"
    "OS4yLDMxLjh2MC44aC01OFYxNjAuOHoiLz4NCgk8cGF0aCBjbGFzcz0ic3QwIiBkPSJNMzcyLjQsMy4x"
    "SDUxMnYyOS4zYy0yMy05LTM1LTEzLjItNDktMTMuMmgtMVYxMjljMCwxNi41LDEuNywyNiw5LjIsMzEu"
    "OHYwLjhoLTU3Ljh2LTAuOA0KCQljNy41LTUuOSw5LjItMTUuMyw5LjItMzEuOFYxOS4zaC0wLjhjLTE0"
    "LjIsMC0yNi4yLDQuMi00OS40LDEzLjJMMzcyLjQsMy4xTDM3Mi40LDMuMXoiLz4NCgk8cGF0aCBjbGFz"
    "cz0ic3QwIiBkPSJNMjQzLjEsMTE5LjJjMC0yMi4zLDE0LjctMzcuOCwzNy42LTQ2LjZjLTEwLjEtMTEu"
    "NS0xNi0yMS44LTE2LTM0LjRjMC0yMy45LDE5LjktMzguMiw0Ni0zOC4yDQoJCWMyOC42LDAsNDYuNiwx"
    "OC4zLDQ4LjksNDYuMmgtMjkuNGMtMC4yLTE3LjYtNi4zLTMxLjktMTkuOS0zMS45Yy05LjksMC0xNiw2"
    "LjUtMTYsMTYuOHM2LjEsMTkuNSwyMy41LDM3LjJsMzUuMywzNS41DQoJCWMyLjEtOS4yLDMuNC0xOS4z"
    "LDMuNi0yOS40bDMxLjUtMC4ydjVjLTYuOSwxMy42LTEzLjksMjYuOS0yMS40LDM4LjZsNDAuNSw0MC43"
    "djMuMmgtMzkuOWwtMTkuMy0xOS43DQoJCWMtMTMuNiwxMy45LTMwLjIsMjIuNy01Mi4xLDIyLjdDMjY1"
    "LDE2NC42LDI0My4xLDE0Ni45LDI0My4xLDExOS4yTDI0My4xLDExOS4yeiBNMzExLDE0My40YzEyLDAs"
    "MjEtNC4yLDI3LjktMTEuMWwtNDkuMy01MC4yDQoJCWMtOS4yLDYuNS0xMy43LDE2LjQtMTMuNywyNy4z"
    "QzI3NS45LDEyOS4xLDI4OS41LDE0My40LDMxMSwxNDMuNEwzMTEsMTQzLjR6Ii8+DQo8L2c+DQo8L3N2"
    "Zz4NCg=="
)
def h(text):
    """HTML-escape text."""
    return escape(str(text)) if text else ""


def build_tags_html(tags, is_partner=False, partner_program_tag=None):
    """Build the hero tags HTML. First tag gets partner styling if partner version."""
    parts = []
    for i, tag in enumerate(tags):
        if is_partner and i == 0 and partner_program_tag:
            parts.append(f'      <span class="hero-tag hero-tag-partner">{h(partner_program_tag)}</span>')
        else:
            parts.append(f'      <span class="hero-tag">{h(tag)}</span>')
    return "\n".join(parts)


def build_tech_pills(technologies):
    """Build the technology pill list."""
    return "\n".join(
        f'        <span class="tech-pill">{h(t)}</span>' for t in technologies
    )


def build_metrics_html(items):
    """Build the 3-column metric cards."""
    parts = []
    for item in items:
        parts.append(f"""      <div class="metric">
        <div class="metric-value">{h(item["value"])}</div>
        <div class="metric-label">{h(item["label"])}</div>
      </div>""")
    return "\n".join(parts)


def build_context_bar(items):
    """Build the dark context bar at page bottom."""
    parts = []
    for item in items:
        parts.append(f"""      <div class="context-item">
        <strong>{h(item["value"])}</strong>
        {h(item["label"])}
      </div>""")
    return "\n".join(parts)


def build_phases_html(phases):
    """Build the numbered approach phases (fallback content type)."""
    parts = []
    for i, phase in enumerate(phases, 1):
        parts.append(f"""        <div class="phase">
          <div class="phase-num">{i}</div>
          <div class="phase-body">
            <h4>{h(phase["name"])}</h4>
            <p>{h(phase["description"])}</p>
          </div>
        </div>""")
    return "\n".join(parts)


def build_page2_left_section(page2_left, fallback_phases=None):
    """Build the dynamic page 2 left section based on content type."""
    if not page2_left or not page2_left.get("items"):
        if fallback_phases:
            return build_phases_html(fallback_phases), "Project Approach"
        return "", "Project Approach"

    content_type = page2_left.get("type", "phases")
    title = page2_left.get("title", "Project Approach")
    items = page2_left.get("items", [])

    if content_type == "phases" or not items:
        if fallback_phases:
            return build_phases_html(fallback_phases), title
        return "", title

    # All other types use a card-based layout
    parts = []
    for item in items:
        headline = h(item.get("headline", ""))
        detail = h(item.get("detail", ""))

        if content_type == "scale":
            # Big number emphasis
            parts.append(f"""        <div class="highlight-card highlight-scale">
          <div class="highlight-value">{headline}</div>
          <div class="highlight-label">{detail}</div>
        </div>""")
        elif content_type == "speed":
            # Timeline style
            parts.append(f"""        <div class="highlight-card highlight-timeline">
          <div class="timeline-marker"></div>
          <div class="highlight-body">
            <strong>{headline}</strong>
            <span>{detail}</span>
          </div>
        </div>""")
        elif content_type == "compliance":
            # Checkmark style
            parts.append(f"""        <div class="highlight-card highlight-check">
          <div class="check-icon">✓</div>
          <div class="highlight-body">
            <strong>{headline}</strong>
            <span>{detail}</span>
          </div>
        </div>""")
        else:
            # Default card style for challenges, milestones, innovation, integration
            parts.append(f"""        <div class="highlight-card">
          <div class="highlight-body">
            <strong>{headline}</strong>
            <p>{detail}</p>
          </div>
        </div>""")

    return "\n".join(parts), title


def build_metrics_table(rows):
    """Deprecated — kept for backwards compatibility. Delegates to build_outcome_cards."""
    return build_outcome_cards(rows)


def build_outcome_cards(rows):
    """Build the business-outcome / before-after cards (replaces the old table)."""
    parts = []
    for row in rows:
        before = h(row.get("before", ""))
        after = h(row.get("after", ""))
        metric = h(row.get("metric", ""))
        before_html = (
            f'<div class="outcome-delta"><span class="outcome-before-label">Before</span>'
            f'<span class="outcome-before-value">{before}</span></div>'
            if before else ""
        )
        parts.append(f"""          <div class="outcome-card">
            <div class="outcome-label">{metric}</div>
            <div class="outcome-value">{after}</div>
            {before_html}
          </div>""")
    return "\n".join(parts)


def build_tech_cards(cards):
    """Build the 3x2 technology architecture cards."""
    parts = []
    for card in cards:
        parts.append(f"""          <div class="tech-card">
            <h4>{h(card["category"])}</h4>
            <p>{h(card["description"])}</p>
          </div>""")
    return "\n".join(parts)


def resolve_logo_src(value, data_dir=None):
    """Resolve a logo value into an HTML `src` attribute value.

    Accepts:
      - http(s) URL → returned as-is (externally loaded; may not be self-contained)
      - data: URL  → returned as-is
      - local file path (absolute or relative to data_dir / cwd) → read and base64-encoded

    Returns empty string if the value is empty or the local file cannot be read.
    """
    if not value:
        return ""
    v = str(value).strip()
    if not v:
        return ""
    # Already a data URL or http(s) URL — use as-is.
    if v.startswith("data:") or v.startswith("http://") or v.startswith("https://"):
        return v
    # Treat as local file path. Try absolute, then relative to data_dir, then cwd.
    candidates = [Path(v)]
    if data_dir:
        candidates.append(Path(data_dir) / v)
    candidates.append(Path.cwd() / v)
    for p in candidates:
        if p.exists() and p.is_file():
            mime, _ = mimetypes.guess_type(str(p))
            if not mime:
                # Fall back to octet-stream, but prefer common image guesses
                ext = p.suffix.lower()
                mime = {
                    ".png": "image/png",
                    ".jpg": "image/jpeg",
                    ".jpeg": "image/jpeg",
                    ".svg": "image/svg+xml",
                    ".webp": "image/webp",
                    ".gif": "image/gif",
                }.get(ext, "application/octet-stream")
            try:
                encoded = base64.b64encode(p.read_bytes()).decode("ascii")
                return f"data:{mime};base64,{encoded}"
            except OSError as e:
                print(
                    f"⚠ WARNING: could not read client logo file {p}: {e}",
                    file=sys.stderr,
                )
                return ""
    print(
        f"⚠ WARNING: client logo value {v!r} is not a URL or an existing file — skipping.",
        file=sys.stderr,
    )
    return ""


def get_client_display_name(data):
    """Return the display name — anonymized if requested."""
    project = data["project"]
    if project.get("anonymize") and project.get("anonymized_name"):
        return project["anonymized_name"]
    return project["client_name"]


def build_css(version, partner_key=None):
    """Generate the full CSS block. Internal version uses CI&T coral; partner adds partner vars."""
    theme = PARTNER_THEMES.get(partner_key, {}) if partner_key else {}
    is_partner = version == "partner" and theme

    # Partner CSS custom properties
    partner_vars = ""
    if is_partner:
        partner_vars = f"""
    /* Partner accent */
    --partner: {theme["color"]};
    --partner-dark: {theme["color_dark"]};
    --partner-muted: {theme["color_muted"]};
    --partner-surface: {theme["color_surface"]};"""

    # In the partner version, several elements swap from --accent to --partner
    metric_color = "var(--partner)" if is_partner else "var(--accent)"
    quote_mark_color = "var(--partner)" if is_partner else "var(--accent)"
    tech_pill_bg = "var(--partner-muted)" if is_partner else "var(--surface)"
    tech_pill_color = "var(--partner-dark)" if is_partner else "var(--navy-mid)"
    page_break_border = f"4px solid var(--partner)" if is_partner else "4px solid var(--accent)"
    page2_header_bg = "var(--partner-surface)" if is_partner else "var(--surface-alt)"
    page2_header_label = "var(--partner)" if is_partner else "var(--accent)"
    phase_num_bg = "var(--partner)" if is_partner else "var(--accent)"
    ext_table_th_bg = "var(--partner-surface)" if is_partner else "var(--surface)"
    ext_table_th_color = "var(--partner-dark)" if is_partner else "var(--navy-mid)"
    tech_detail_bg = "var(--partner-surface)" if is_partner else "var(--surface-alt)"
    tech_card_h4_color = f"color: var(--partner-dark);" if is_partner else ""

    # Hero stripe for partner
    hero_before = ""
    if is_partner:
        hero_before = """
  .hero::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 5px;
    background: var(--partner);
  }"""

    # Partner-specific tag styling
    hero_tag_partner = ""
    if is_partner:
        hero_tag_partner = """
  .hero-tag-partner {
    background: var(--partner);
    color: #fff;
  }"""

    # Partner label class
    block_label_partner = ""
    if is_partner:
        block_label_partner = """
  .block-label-partner {
    color: var(--partner);
  }"""

    # Topbar logos container — always present (CI&T + partner), with an optional
    # client logo slot appended when the user has supplied one.
    topbar_logos_css = """
  .topbar-logos {
    display: flex;
    align-items: center;
    gap: 16px;
  }
  .topbar-divider {
    width: 1px;
    height: 24px;
    background: var(--surface-border);
  }
  .topbar-logo-partner {
    height: 28px;
    max-width: 140px;
    object-fit: contain;
    display: block;
  }
  .topbar-logo-partner-fallback {
    font-family: var(--font-body);
    font-weight: 700;
    font-size: 14px;
    color: var(--partner, #555);
    letter-spacing: 0.5px;
  }
  .topbar-logo-client {
    height: 26px;
    max-width: 120px;
    object-fit: contain;
  }"""

    topbar_label_color = "var(--partner)" if is_partner else "var(--accent)"

    return f"""<style>
  /* ── Reset & Tokens ── */
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  :root {{
    --bg: #ffffff;
    --surface: #B4DCFA;
    --surface-alt: #f5f5f7;
    --surface-border: #dce8f5;
    --text-primary: #000050;
    --text-secondary: #393973;
    --accent: #FA5A50;
    --accent-dark: #D94A41;
    --accent-muted: rgba(250, 90, 80, 0.10);
    --deep-red: #690037;
    --navy-mid: #242459;
    --blue-mid: #8CB3D9;
    --font-display: 'Playfair Display', Georgia, serif;
    --font-body: 'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    --page-w: 1000px;
    --radius: 8px;{partner_vars}
  }}
  body {{
    font-family: var(--font-body);
    color: var(--text-primary);
    background: var(--bg);
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
  }}
  .page {{ max-width: var(--page-w); margin: 0 auto; }}

  /* ════════ PAGE 1 ════════ */

  .topbar {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20px 40px;
    border-bottom: 1px solid var(--surface-border);
  }}
  .topbar-logo {{ height: 28px; }}
  .topbar-label {{
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: {topbar_label_color};
  }}{topbar_logos_css}

  .hero {{
    background: var(--accent);
    color: #fff;
    padding: 48px 40px 40px;
    position: relative;
    overflow: hidden;
  }}{hero_before}
  .hero::after {{
    content: '&';
    position: absolute;
    right: -20px;
    bottom: -40px;
    font-family: var(--font-display);
    font-size: 280px;
    font-weight: 700;
    opacity: 0.08;
    line-height: 1;
    pointer-events: none;
  }}
  .hero-eyebrow {{
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    opacity: 0.85;
    margin-bottom: 12px;
  }}
  .hero h1 {{
    font-family: var(--font-display);
    font-size: 36px;
    font-weight: 700;
    line-height: 1.2;
    margin-bottom: 12px;
    max-width: 700px;
  }}
  .hero-sub {{
    font-size: 16px;
    opacity: 0.9;
    max-width: 600px;
    line-height: 1.5;
  }}
  .hero-tags {{
    display: flex;
    gap: 8px;
    margin-top: 20px;
    flex-wrap: wrap;
  }}
  .hero-tag {{
    display: inline-block;
    background: rgba(255,255,255,0.18);
    color: #fff;
    font-size: 11px;
    font-weight: 600;
    padding: 5px 12px;
    border-radius: 14px;
    letter-spacing: 0.3px;
  }}{hero_tag_partner}

  .content {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0;
  }}

  .block {{ padding: 32px 40px; }}
  .block-challenge {{
    border-right: 1px solid var(--surface-border);
    border-bottom: 1px solid var(--surface-border);
  }}
  .block-solution {{ border-bottom: 1px solid var(--surface-border); }}
  .block-label {{
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 10px;
  }}{block_label_partner}
  .block h2 {{
    font-family: var(--font-display);
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 10px;
    line-height: 1.3;
  }}
  .block p {{
    font-size: 14px;
    color: var(--text-secondary);
    line-height: 1.6;
  }}
  .tech-list {{
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 14px;
  }}
  .tech-pill {{
    font-size: 11px;
    font-weight: 600;
    background: {tech_pill_bg};
    color: {tech_pill_color};
    padding: 4px 10px;
    border-radius: 12px;
  }}

  .metrics {{
    grid-column: 1 / -1;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    border-bottom: 1px solid var(--surface-border);
  }}
  .metric {{
    padding: 28px 32px;
    text-align: center;
    border-right: 1px solid var(--surface-border);
  }}
  .metric:last-child {{ border-right: none; }}
  .metric-value {{
    font-family: var(--font-display);
    font-size: 38px;
    font-weight: 700;
    color: {metric_color};
    line-height: 1.1;
  }}
  .metric-label {{
    font-size: 13px;
    color: var(--text-secondary);
    margin-top: 4px;
    font-weight: 500;
  }}

  .quote-section {{
    grid-column: 1 / -1;
    padding: 32px 40px;
    background: var(--surface-alt);
    border-bottom: 1px solid var(--surface-border);
    position: relative;
  }}
  .quote-mark {{
    font-family: var(--font-display);
    font-size: 64px;
    color: {quote_mark_color};
    line-height: 1;
    position: absolute;
    top: 16px;
    left: 32px;
    opacity: 0.3;
  }}
  .quote-text {{
    font-family: var(--font-display);
    font-size: 18px;
    font-weight: 400;
    font-style: italic;
    color: var(--text-primary);
    line-height: 1.5;
    max-width: 780px;
    margin-left: 24px;
  }}
  .quote-attr {{
    font-size: 13px;
    color: var(--text-secondary);
    margin-top: 12px;
    margin-left: 24px;
    font-style: normal;
  }}
  .quote-attr strong {{ color: var(--text-primary); }}

  .context-bar {{
    grid-column: 1 / -1;
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    background: var(--text-primary);
    color: rgba(255,255,255,0.85);
  }}
  .context-item {{
    padding: 18px 20px;
    text-align: center;
    border-right: 1px solid rgba(255,255,255,0.1);
    font-size: 12px;
  }}
  .context-item:last-child {{ border-right: none; }}
  .context-item strong {{
    display: block;
    font-size: 15px;
    color: #fff;
    margin-bottom: 2px;
  }}

  /* ════════ PAGE 2 ════════ */
  .page-break {{
    border-top: {page_break_border};
    margin-top: 48px;
    padding-top: 0;
  }}
  .page2-header {{
    background: {page2_header_bg};
    padding: 24px 40px;
    border-bottom: 1px solid var(--surface-border);
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}
  .page2-header h2 {{
    font-family: var(--font-display);
    font-size: 22px;
    font-weight: 700;
  }}
  .page2-header span {{
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: {page2_header_label};
  }}

  .page2-content {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0;
  }}

  .approach {{
    padding: 32px 40px;
    border-right: 1px solid var(--surface-border);
    border-bottom: 1px solid var(--surface-border);
  }}
  .approach h3 {{ font-size: 16px; font-weight: 600; margin-bottom: 16px; }}
  .phase {{ display: flex; gap: 12px; margin-bottom: 16px; align-items: flex-start; }}
  .phase-num {{
    flex-shrink: 0;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: {phase_num_bg};
    color: #fff;
    font-size: 13px;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
  }}
  .phase-body h4 {{ font-size: 14px; font-weight: 600; margin-bottom: 2px; }}
  .phase-body p {{ font-size: 13px; color: var(--text-secondary); line-height: 1.45; }}

  /* Dynamic page2 left section cards */
  .highlight-card {{
    background: var(--bg);
    border: 1px solid var(--surface-border);
    border-left: 3px solid {metric_color};
    border-radius: var(--radius);
    padding: 14px 16px;
    margin-bottom: 10px;
  }}
  .highlight-card:last-child {{ margin-bottom: 0; }}
  .highlight-body strong {{
    display: block;
    font-size: 14px;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 4px;
  }}
  .highlight-body p,
  .highlight-body span {{
    font-size: 12px;
    color: var(--text-secondary);
    line-height: 1.4;
  }}
  .highlight-scale {{
    text-align: center;
    padding: 18px 16px;
  }}
  .highlight-scale .highlight-value {{
    font-family: var(--font-display);
    font-size: 32px;
    font-weight: 700;
    color: {metric_color};
    line-height: 1.1;
  }}
  .highlight-scale .highlight-label {{
    font-size: 12px;
    color: var(--text-secondary);
    margin-top: 4px;
  }}
  .highlight-timeline {{
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding-left: 12px;
  }}
  .timeline-marker {{
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: {metric_color};
    flex-shrink: 0;
    margin-top: 5px;
  }}
  .highlight-check {{
    display: flex;
    align-items: flex-start;
    gap: 12px;
  }}
  .check-icon {{
    width: 22px;
    height: 22px;
    border-radius: 50%;
    background: {metric_color};
    color: #fff;
    font-size: 12px;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }}

  .ext-metrics {{
    padding: 32px 40px;
    border-bottom: 1px solid var(--surface-border);
  }}
  .ext-metrics h3 {{ font-size: 16px; font-weight: 600; margin-bottom: 16px; }}

  .outcome-cards {{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }}
  .outcome-card {{
    position: relative;
    background: var(--bg);
    border: 1px solid var(--surface-border);
    border-left: 3px solid {metric_color};
    border-radius: var(--radius);
    padding: 16px 20px 18px;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }}
  .outcome-label {{
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.7px;
    color: var(--text-secondary);
    line-height: 1.3;
  }}
  .outcome-value {{
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 32px;
    font-weight: 700;
    color: {metric_color};
    line-height: 1.05;
    margin-top: 2px;
  }}
  .outcome-delta {{
    display: flex;
    align-items: baseline;
    gap: 6px;
    font-size: 11px;
    color: var(--text-secondary);
    margin-top: 4px;
    padding-top: 6px;
    border-top: 1px dashed var(--surface-border);
  }}
  .outcome-before-label {{
    font-size: 9px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    color: var(--text-muted, #8790a8);
  }}
  .outcome-before-value {{
    font-weight: 600;
    color: var(--text-primary);
  }}

  /* Legacy .ext-table rules kept for older data that may still render as table */
  .ext-table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
  .ext-table th {{
    text-align: left;
    font-weight: 600;
    padding: 8px 12px;
    background: {ext_table_th_bg};
    color: {ext_table_th_color};
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}
  .ext-table td {{
    padding: 8px 12px;
    border-bottom: 1px solid var(--surface-border);
    color: var(--text-secondary);
  }}
  .ext-table td:last-child {{ font-weight: 600; color: var(--text-primary); }}

  .tech-detail {{
    grid-column: 1 / -1;
    padding: 32px 40px;
    background: {tech_detail_bg};
  }}
  .tech-detail h3 {{ font-size: 16px; font-weight: 600; margin-bottom: 16px; }}
  .tech-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
  }}
  .tech-card {{
    background: var(--bg);
    border: 1px solid var(--surface-border);
    border-radius: var(--radius);
    padding: 16px;
  }}
  .tech-card h4 {{ font-size: 13px; font-weight: 600; margin-bottom: 4px; {tech_card_h4_color} }}
  .tech-card p {{ font-size: 12px; color: var(--text-secondary); line-height: 1.45; }}

  .footer {{
    padding: 20px 40px;
    text-align: center;
    font-size: 11px;
    color: var(--text-secondary);
    border-top: 1px solid var(--surface-border);
  }}

  /* ════════ PRINT ════════ */
  @media print {{
    body {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
    @page {{ size: A4 portrait; margin: 0; }}

    .page {{ max-width: none; width: 210mm; overflow: hidden; }}

    .page1 {{
      width: 210mm;
      page-break-after: always;
      break-after: page;
      display: flex;
      flex-direction: column;
    }}

    .topbar {{ padding: 10px 16px; flex-shrink: 0; }}
    .topbar-logo {{ height: 22px; }}
    .topbar-label {{ font-size: 10px; }}
    .topbar-logo-partner {{ height: 22px; max-width: 120px; }}
    .topbar-logo-client {{ height: 20px; max-width: 100px; }}
    .topbar-divider {{ height: 18px; }}
    .topbar-logos {{ gap: 10px; }}

    .hero {{ padding: 28px 20px 24px; flex-shrink: 0; }}
    .hero::after {{ font-size: 200px; right: -20px; bottom: -30px; }}
    .hero-eyebrow {{ font-size: 11px; margin-bottom: 8px; }}
    .hero h1 {{ font-size: 30px; margin-bottom: 8px; }}
    .hero-sub {{ font-size: 13px; line-height: 1.45; }}
    .hero-tags {{ margin-top: 12px; gap: 5px; }}
    .hero-tag {{ font-size: 10px; padding: 4px 10px; }}

    .content {{
      display: grid !important;
      grid-template-columns: 1fr 1fr;
      grid-template-rows: auto auto auto auto;
    }}
    .block-challenge {{ grid-column: 1; grid-row: 1; border-right: 1px solid var(--surface-border); }}
    .block-solution {{ grid-column: 2; grid-row: 1; }}
    .metrics {{ grid-column: 1 / -1; grid-row: 2; }}
    .quote-section {{ grid-column: 1 / -1; grid-row: 3; }}
    .context-bar {{ grid-column: 1 / -1; grid-row: 4; }}

    .block {{ padding: 16px 18px; }}
    .block-label {{ font-size: 10px; margin-bottom: 6px; }}
    .block h2 {{ font-size: 17px; margin-bottom: 8px; }}
    .block p {{ font-size: 12px; line-height: 1.55; }}
    .tech-list {{ margin-top: 10px; gap: 4px; }}
    .tech-pill {{ font-size: 10px; padding: 3px 8px; }}

    .metric {{ padding: 16px 14px; }}
    .metric-value {{ font-size: 34px; }}
    .metric-label {{ font-size: 11px; }}

    .quote-section {{ padding: 16px 20px; }}
    .quote-mark {{ font-size: 48px; top: 8px; left: 14px; }}
    .quote-text {{ font-size: 14px; line-height: 1.45; margin-left: 18px; }}
    .quote-attr {{ font-size: 11px; margin-top: 8px; margin-left: 18px; }}

    .context-item {{ padding: 12px 10px; font-size: 10px; }}
    .context-item strong {{ font-size: 13px; }}

    .page-break {{
      break-before: page;
      page-break-before: always;
      margin-top: 0;
      border-top: none;
      padding-top: 0;
      width: 210mm;
      display: flex;
      flex-direction: column;
    }}

    .page2-header {{ padding: 14px 18px; flex-shrink: 0; }}
    .page2-header h2 {{ font-size: 17px; }}
    .page2-header span {{ font-size: 9px; }}

    .page2-content {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      grid-template-rows: auto auto auto;
    }}

    .approach {{ padding: 16px 18px; }}
    .approach h3 {{ font-size: 13px; margin-bottom: 10px; }}
    .phase {{ margin-bottom: 10px; gap: 8px; }}
    .phase-num {{ width: 22px; height: 22px; font-size: 11px; }}
    .phase-body h4 {{ font-size: 11px; }}
    .phase-body p {{ font-size: 10px; line-height: 1.4; }}

    .highlight-card {{ padding: 10px 12px; margin-bottom: 6px; }}
    .highlight-body strong {{ font-size: 11px; margin-bottom: 2px; }}
    .highlight-body p, .highlight-body span {{ font-size: 9px; }}
    .highlight-scale {{ padding: 12px 10px; }}
    .highlight-scale .highlight-value {{ font-size: 22px; }}
    .highlight-scale .highlight-label {{ font-size: 10px; }}
    .timeline-marker {{ width: 8px; height: 8px; margin-top: 4px; }}
    .check-icon {{ width: 16px; height: 16px; font-size: 9px; }}

    .ext-metrics {{ padding: 16px 18px; }}
    .ext-metrics h3 {{ font-size: 13px; margin-bottom: 10px; }}
    .outcome-cards {{ gap: 8px; }}
    .outcome-card {{ padding: 11px 14px 13px; gap: 4px; }}
    .outcome-label {{ font-size: 9px; letter-spacing: 0.5px; }}
    .outcome-value {{ font-size: 22px; }}
    .outcome-delta {{ font-size: 10px; padding-top: 4px; margin-top: 2px; }}
    .outcome-before-label {{ font-size: 8px; }}
    .ext-table th {{ font-size: 9px; padding: 5px 6px; }}
    .ext-table td {{ font-size: 10px; padding: 5px 6px; }}

    .tech-detail {{ padding: 16px 18px; }}
    .tech-detail h3 {{ font-size: 13px; margin-bottom: 10px; }}
    .tech-grid {{ gap: 8px; }}
    .tech-card {{ padding: 10px; }}
    .tech-card h4 {{ font-size: 11px; margin-bottom: 3px; }}
    .tech-card p {{ font-size: 9px; line-height: 1.35; }}

    .footer {{ padding: 8px 18px; font-size: 9px; flex-shrink: 0; }}
  }}

  /* ════════ RESPONSIVE ════════ */
  @media (max-width: 700px) {{
    .content {{ grid-template-columns: 1fr; }}
    .block-challenge {{ border-right: none; }}
    .metrics {{ grid-template-columns: 1fr; }}
    .metric {{ border-right: none; border-bottom: 1px solid var(--surface-border); }}
    .context-bar {{ grid-template-columns: 1fr 1fr; }}
    .page2-content {{ grid-template-columns: 1fr; }}
    .approach {{ border-right: none; }}
    .tech-grid {{ grid-template-columns: 1fr; }}
    .outcome-cards {{ grid-template-columns: 1fr; }}
    .hero h1 {{ font-size: 28px; }}
    .topbar, .hero, .block, .quote-section, .page2-header,
    .approach, .ext-metrics, .tech-detail {{ padding-left: 24px; padding-right: 24px; }}
  }}
</style>"""


def build_topbar(version, partner_key, data):
    """Build the topbar HTML.

    Layout on both versions: CI&T logo · partner logo · (optional) client logo.
    The partner logo is always rendered when a partner is specified — it's built
    into the skill (see _load_partner_logo) and not user-provided.
    """
    theme = PARTNER_THEMES.get(partner_key, {}) if partner_key else {}
    is_partner = version == "partner" and theme

    cit_logo = f'<img class="topbar-logo" src="data:image/svg+xml;base64,{CIT_LOGO_B64}" alt="CI&T">'

    # Partner logo — rendered on both internal and partner versions. Loaded from
    # assets/partner-logos/ and base64-inlined; see _load_partner_logo.
    partner_logo_html = _load_partner_logo(partner_key) if partner_key else ""

    # Optional client logo — resolved from URL / data URL / local file. See SKILL.md
    # "Client logo resolution flow" — by the time we get here, the skill has already
    # asked the user and either supplied a source or confirmed proceeding without.
    client_name = get_client_display_name(data)
    client_logo_src = resolve_logo_src(
        data.get("logos", {}).get("client_logo_url") or data.get("logos", {}).get("client_logo_file"),
        data_dir=data.get("_data_dir"),
    )
    client_logo_html = (
        f'<img class="topbar-logo topbar-logo-client" src="{h(client_logo_src)}" alt="{h(client_name)}">'
        if client_logo_src else ""
    )

    label = "Win Wire — Partner" if is_partner else "Win Wire — Internal"

    # Assemble the logo row: CI&T · partner · client (each pair separated by a divider).
    logo_parts = [cit_logo]
    if partner_logo_html:
        logo_parts.extend(['<div class="topbar-divider"></div>', partner_logo_html])
    if client_logo_html:
        logo_parts.extend(['<div class="topbar-divider"></div>', client_logo_html])
    logo_row = "\n      ".join(logo_parts)

    return f"""  <div class="topbar">
    <div class="topbar-logos">
      {logo_row}
    </div>
    <span class="topbar-label">{label}</span>
  </div>"""


def build_hero(version, partner_key, data):
    """Build the hero section."""
    project = data["project"]
    theme = PARTNER_THEMES.get(partner_key, {}) if partner_key else {}
    is_partner = version == "partner" and theme

    client_name = get_client_display_name(data)
    title = h(project["title"])
    subtitle = h(project["subtitle"])
    industry = h(project["industry"])
    partner_name = theme.get("name", project.get("partner", "").upper()) if is_partner else project.get("partner", "").upper()

    if is_partner:
        eyebrow = f'{industry} &middot; {h(project.get("project_type", ""))} &middot; {partner_name}'
    else:
        eyebrow = f'{industry} &middot; {partner_name}'

    tags = project.get("tags", [])
    # For partner version, use incentive program tag as the first highlighted tag
    partner_program_tag = None
    if is_partner:
        ctx = data.get("context_bar_partner", data.get("context_bar_internal", []))
        for item in ctx:
            if "incentive" in item.get("label", "").lower() or "program" in item.get("label", "").lower():
                partner_program_tag = item.get("value", "")
                break
    tags_html = build_tags_html(tags, is_partner=is_partner, partner_program_tag=partner_program_tag)

    return f"""  <div class="hero">
    <div class="hero-eyebrow">{eyebrow}</div>
    <h1>{client_name}: {title}</h1>
    <p class="hero-sub">{subtitle}</p>
    <div class="hero-tags">
{tags_html}
    </div>
  </div>"""


def build_page1_content(version, partner_key, data):
    """Build the challenge/solution/metrics/quote/context-bar content grid."""
    theme = PARTNER_THEMES.get(partner_key, {}) if partner_key else {}
    is_partner = version == "partner" and theme

    challenge = data["challenge"]
    solution = data["solution"]

    # Solution label
    if is_partner:
        solution_label_class = 'block-label block-label-partner'
        solution_label_text = theme["solution_label"]
    else:
        solution_label_class = 'block-label'
        solution_label_text = "The Solution"

    tech_pills = build_tech_pills(solution.get("technologies", []))

    # Metrics. Reserved slot #1 is the revenue metric: Services Revenue for internal,
    # Annual Cloud Revenue for partner. If it's empty at this point the skill layer has
    # already warned the user and received permission to publish without it — render a
    # dash so the absence is visible rather than silently dropping or reordering cards.
    if is_partner and "metrics_partner" in data:
        metrics_items = [dict(m) for m in data["metrics_partner"]["items"]]
        revenue_label = "Annual Cloud Revenue"
    else:
        metrics_items = [dict(m) for m in data["metrics_internal"]["items"]]
        revenue_label = "Services Revenue"

    if metrics_items and not metrics_items[0].get("value"):
        metrics_items[0]["value"] = "—"
        if not metrics_items[0].get("label"):
            metrics_items[0]["label"] = revenue_label
        print(
            f"⚠ WARNING: reserved revenue slot ({revenue_label}) is empty. "
            "Rendering as '—'. Make sure you have confirmed with the user that they "
            "accept a weaker WinWire without this number. See SKILL.md "
            "'Non-negotiable rule: the revenue metric'.",
            file=sys.stderr,
        )

    metrics_html = build_metrics_html(metrics_items)

    # Quote — only render if there's actual quote text
    quote = data.get("quote", {})
    quote_text = quote.get("text", "").strip() if quote.get("text") else ""
    if quote_text:
        quote_company = h(quote.get("company", ""))
        company_suffix = f", {quote_company}" if quote_company else ""
        quote_html = f"""
    <div class="quote-section">
      <span class="quote-mark">&ldquo;</span>
      <p class="quote-text">{h(quote_text)}</p>
      <p class="quote-attr"><strong>{h(quote.get("author", ""))}</strong>, {h(quote.get("title", ""))}{company_suffix}</p>
    </div>
"""
    else:
        quote_html = ""

    # Context bar
    if is_partner and "context_bar_partner" in data:
        ctx_items = data["context_bar_partner"]
    elif "context_bar_internal" in data:
        ctx_items = data["context_bar_internal"]
    else:
        ctx_items = []
    context_html = build_context_bar(ctx_items)

    return f"""  <div class="content">

    <div class="block block-challenge">
      <div class="block-label">The Challenge</div>
      <h2>{h(challenge["headline"])}</h2>
      <p>{h(challenge["body"])}</p>
    </div>

    <div class="block block-solution">
      <div class="{solution_label_class}">{solution_label_text}</div>
      <h2>{h(solution["headline"])}</h2>
      <p>{h(solution["body"])}</p>
      <div class="tech-list">
{tech_pills}
      </div>
    </div>

    <div class="metrics">
{metrics_html}
    </div>
{quote_html}
    <div class="context-bar">
{context_html}
    </div>

  </div>"""


def build_page2(version, partner_key, data):
    """Build page 2 if data includes it."""
    page2 = data.get("page2", {})
    if not page2.get("include"):
        return ""

    theme = PARTNER_THEMES.get(partner_key, {}) if partner_key else {}
    is_partner = version == "partner" and theme

    # Titles
    if is_partner:
        deep_dive_title = f"Deep Dive: {theme['page2_title_suffix']}"
        metrics_title = theme["metrics_title"]
        tech_title = theme["tech_title"]
    else:
        deep_dive_title = f"Deep Dive: {h(page2.get('deep_dive_title', ''))}"
        metrics_title = "Full Metrics"
        tech_title = "Technology Architecture"

    # Dynamic left section — uses page2_left if available, falls back to phases
    left_section_html, left_section_title = build_page2_left_section(
        page2.get("page2_left"),
        fallback_phases=page2.get("phases", [])
    )

    # Business outcome cards (replaces the old before/after table)
    outcome_cards = build_outcome_cards(page2.get("metrics_table", []))

    # Tech cards
    tech_cards = build_tech_cards(page2.get("tech_architecture", []))

    # Footer
    client_name = get_client_display_name(data)
    project_type = data["project"].get("project_type", "")
    now = datetime.now()
    date_str = now.strftime("%B %Y")

    if is_partner:
        footer_text = f'{theme["footer_prefix"]} &middot; Win Wire — {client_name} {project_type} &middot; {date_str}'
    else:
        footer_text = f'CI&T &middot; Confidential &middot; Win Wire — {client_name} {project_type} &middot; {date_str}'

    return f"""
  <div class="page-break">
    <div class="page2-header">
      <h2>{deep_dive_title}</h2>
      <span>Page 2 — Details</span>
    </div>

    <div class="page2-content">

      <div class="approach">
        <h3>{h(left_section_title)}</h3>
{left_section_html}
      </div>

      <div class="ext-metrics">
        <h3>{h(metrics_title)}</h3>
        <div class="outcome-cards">
{outcome_cards}
        </div>
      </div>

      <div class="tech-detail">
        <h3>{h(tech_title)}</h3>
        <div class="tech-grid">
{tech_cards}
        </div>
      </div>

    </div>

    <div class="footer">
      {footer_text}
    </div>

  </div>"""


def build_html(data, version="internal", partner_key=None):
    """Assemble the full HTML document."""
    project = data["project"]
    client_name = get_client_display_name(data)
    theme = PARTNER_THEMES.get(partner_key, {}) if partner_key else {}
    is_partner = version == "partner" and theme

    # Title tag
    if is_partner:
        title_tag = f"WinWire — {client_name} {project.get('project_type', '')} | CI&T & {theme['name']}"
    else:
        title_tag = f"WinWire — {client_name} {project.get('project_type', '')} | CI&T"

    css = build_css(version, partner_key)
    topbar = build_topbar(version, partner_key, data)
    hero = build_hero(version, partner_key, data)
    content = build_page1_content(version, partner_key, data)
    page2 = build_page2(version, partner_key, data)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{h(title_tag)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=Playfair+Display:wght@400;600;700&display=swap" rel="stylesheet">
{css}
</head>
<body>

<div class="page">

  <div class="page1">

{topbar}

{hero}

{content}

  </div>
{page2}

</div>

</body>
</html>"""


def main():
    parser = argparse.ArgumentParser(description="Generate WinWire HTML from JSON data")
    parser.add_argument("--data", required=True, help="Path to the JSON data file")
    parser.add_argument("--version", choices=["internal", "partner"], default="internal",
                        help="Version to generate: internal or partner")
    parser.add_argument("--partner", choices=["aws", "gcp", "azure"], default=None,
                        help="Partner key (required for partner version)")
    parser.add_argument("--template-dir", default=None,
                        help="Path to template assets directory (currently unused, reserved)")
    parser.add_argument("--output", required=True, help="Output HTML file path")
    parser.add_argument("--anonymize", action="store_true",
                        help="Override anonymize flag in data to true")
    args = parser.parse_args()

    if args.version == "partner" and not args.partner:
        print("Error: --partner is required when --version is partner", file=sys.stderr)
        sys.exit(1)

    data_path = Path(args.data)
    if not data_path.exists():
        print(f"Error: data file not found: {data_path}", file=sys.stderr)
        sys.exit(1)

    with open(data_path) as f:
        data = json.load(f)

    # Record the data file's directory so that relative logo paths can be resolved
    # against the location of the JSON (typically the workspace folder).
    data["_data_dir"] = str(data_path.parent.resolve())

    if args.anonymize:
        data["project"]["anonymize"] = True

    # Partner logo is shown on both internal and partner versions. For the internal
    # version, the --partner flag is optional — if omitted, fall back to what's in
    # the data (project.partner). This way a single JSON drives both versions and
    # the partner logo appears in the topbar regardless.
    partner_key = args.partner
    if not partner_key:
        data_partner = (data.get("project", {}).get("partner") or "").strip().lower()
        if data_partner in _PARTNER_LOGO_FILES:
            partner_key = data_partner

    html = build_html(data, version=args.version, partner_key=partner_key)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    print(f"Generated: {output_path}")


if __name__ == "__main__":
    main()
