# Partner Themes Reference

## Design Philosophy

The WinWire always looks like a CI&T page. Partners get **color accents** in specific
locations — not a full visual rebrand. The CI&T brand system (Coral, Navy, Playfair Display
+ DM Sans) remains the foundation. Partner branding is layered on top through CSS custom
properties and a handful of HTML/label swaps.

## Partner Color Definitions

### AWS
```css
--partner: #FF9900;
--partner-dark: #E68A00;
--partner-muted: rgba(255, 153, 0, 0.10);
--partner-surface: #FFF5E6;
```

### GCP (Google Cloud)
```css
--partner: #4285F4;
--partner-dark: #3367D6;
--partner-muted: rgba(66, 133, 244, 0.10);
--partner-surface: #EBF3FE;
```

### Azure (Microsoft)
```css
--partner: #0078D4;
--partner-dark: #005A9E;
--partner-muted: rgba(0, 120, 212, 0.10);
--partner-surface: #E6F2FB;
```

## Where Partner Colors Appear

Partner colors are applied in these specific locations — everything else stays CI&T branded:

### Page 1
| Element | CI&T Internal | Partner Version |
|---------|--------------|-----------------|
| Topbar label color | `var(--accent)` (Coral) | `var(--partner)` |
| Topbar logos | CI&T only | CI&T + divider + partner logo |
| Hero top stripe | none | 5px `var(--partner)` bar via `::before` |
| Solution label text | "The Solution" | "{Partner}-Powered Solution" |
| Solution label color | `var(--accent)` | `var(--partner)` (uses `.block-label-partner`) |
| Tech pills bg | `var(--surface)` | `var(--partner-muted)` |
| Tech pills text | `var(--navy-mid)` | `var(--partner-dark)` |
| Metric values color | `var(--accent)` | `var(--partner)` |
| Quote mark color | `var(--accent)` | `var(--partner)` |
| First hero tag | normal style | `.hero-tag-partner` with `bg: var(--partner)` |

### Page 2
| Element | CI&T Internal | Partner Version |
|---------|--------------|-----------------|
| Page break top border | `var(--accent)` | `var(--partner)` |
| Page 2 header bg | `var(--surface-alt)` | `var(--partner-surface)` |
| Page 2 header label color | `var(--accent)` | `var(--partner)` |
| Phase number circles | `var(--accent)` | `var(--partner)` |
| Ext-table header bg | `var(--surface)` | `var(--partner-surface)` |
| Ext-table header text | `var(--navy-mid)` | `var(--partner-dark)` |
| Tech detail section bg | `var(--surface-alt)` | `var(--partner-surface)` |
| Tech card h4 color | default | `var(--partner-dark)` |

## Content Label Differences

| Element | CI&T Internal | AWS Partner | GCP Partner | Azure Partner |
|---------|--------------|-------------|-------------|---------------|
| Topbar label | "Win Wire — Internal" | "Win Wire — Partner" | "Win Wire — Partner" | "Win Wire — Partner" |
| Solution label | "The Solution" | "AWS-Powered Solution" | "Google Cloud Solution" | "Azure-Powered Solution" |
| Hero eyebrow | "{Industry} · {Partner}" | "{Industry} · {ProjectType} · {Partner}" | same | same |
| Page 2 title | "Deep Dive: {ProjectTitle}" | "Deep Dive: AWS Services & Business Outcomes" | "Deep Dive: Google Cloud & Business Outcomes" | "Deep Dive: Azure Services & Business Outcomes" |
| Approach title | "Project Approach" | "Migration Approach" | "Migration Approach" | "Migration Approach" |
| Metrics title | "Full Metrics" | "Business Outcomes" | "Business Outcomes" | "Business Outcomes" |
| Tech title | "Technology Architecture" | "AWS Services Adopted" | "Google Cloud Services" | "Azure Services Adopted" |
| Footer prefix | "CI&T · Confidential" | "CI&T & AWS" | "CI&T & Google Cloud" | "CI&T & Microsoft Azure" |

## Logo Handling

### CI&T Logo
Always present. Embedded as base64 SVG in the HTML (no external dependency). The same
logo is used in both internal and partner versions.

### Partner Logos
In the partner version, the topbar shows both CI&T and partner logos separated by a
vertical divider:

```html
<div class="topbar-logos">
  <img class="topbar-logo" src="[base64 CI&T SVG]" alt="CI&T">
  <div class="topbar-divider"></div>
  [partner logo element]
</div>
```

Partner logo implementations:
- **AWS**: Inline SVG text element — `<svg><text fill="#FF9900">AWS</text></svg>`
- **GCP**: Inline SVG text element — `<svg><text fill="#4285F4">Google Cloud</text></svg>`
- **Azure**: Inline SVG text element — `<svg><text fill="#0078D4">Azure</text></svg>`

If the user provides actual partner logo files (SVG/PNG), prefer those. The text-based SVGs
are fallbacks that maintain consistent styling without requiring external assets.

### Client Logo
Optional. If provided, it can appear in the hero section or footer, but this is not a
default element. Handle it as an extra if supplied in the data JSON (`logos.client_logo_url`).

## Metrics Differences

The three headline metric cards change between versions:

### CI&T Internal
1. **Services Revenue** — total contract value (e.g., "$3.2M")
2. **Incentive Funding** — partner program dollars (e.g., "$280K")
3. **Deal Cycle** — days from opportunity to close (e.g., "94 days")

### Partner-Facing
1. **Annual Cloud Revenue** — recurring cloud spend (e.g., "$1.2M")
2. **Business Outcome** — measurable client improvement (e.g., "40%")
3. **Services Adopted** — count and type of partner services (e.g., "6 AWS Services")

## Context Bar Differences

The dark bar at the bottom of page 1 also varies:

### CI&T Internal (4 items)
- Incentive Program, Funding Received, Deal Cycle, Delivery Team

### Partner-Facing (4 items)
- Incentive Program, Funding Received, Deal Cycle, Delivery Timeline

The key difference: internal shows **team size** (e.g., "18 People"), partner shows
**delivery duration** (e.g., "9 Months").

## First Hero Tag

In the partner version, the first tag in the hero section gets special styling to highlight
the partner program:

```html
<span class="hero-tag hero-tag-partner">AWS MAP 2.0</span>
```

This uses `background: var(--partner)` instead of the default semi-transparent white,
making the partner program badge stand out.
