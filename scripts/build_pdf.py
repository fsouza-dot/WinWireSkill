#!/usr/bin/env python3
"""Convert WinWire HTML files to PDF with content-fitted page sizes.

Uses @page CSS injection + preferCSSPageSize for pixel-perfect sizing.
Each logical page (page1 and page2) gets rendered into its own PDF with
a page size exactly matching the content height, then the two are merged.

Usage:
    python build_pdf.py --html winwire-internal.html --output winwire-internal.pdf
    python build_pdf.py --html winwire-aws.html --output winwire-aws.pdf --page1-only
"""

import argparse
import asyncio
import shutil
import sys
import tempfile
from pathlib import Path

from playwright.async_api import async_playwright

PAGE_WIDTH_MM = 210


async def generate_page(browser, html_path, pdf_path, hide_selector, measure_selector):
    """Hide one section, inject @page with exact content height, generate PDF.

    The approach:
    1. Open the HTML file in a wide viewport
    2. Hide the "other" page section (so only the target page is visible)
    3. Remove any break-before/after CSS that might add phantom page breaks
    4. Switch to print media emulation
    5. Measure the visible section's bounding rect height
    6. Inject an @page CSS rule with that exact height
    7. Generate PDF with preferCSSPageSize so the browser uses our dimensions
    """
    page_width_px = int(PAGE_WIDTH_MM * 96 / 25.4)
    page = await browser.new_page()
    await page.set_viewport_size({"width": page_width_px, "height": 4000})
    await page.goto(f"file://{html_path}", wait_until="networkidle")
    await page.wait_for_timeout(1000)

    # Hide the other page
    await page.evaluate(f"document.querySelector('{hide_selector}').style.display = 'none'")

    # Remove page-break CSS so it doesn't push content down
    await page.evaluate(f"""(() => {{
        const el = document.querySelector('{measure_selector}');
        if (el) {{
            el.style.breakBefore = 'auto';
            el.style.pageBreakBefore = 'auto';
            el.style.breakAfter = 'auto';
            el.style.pageBreakAfter = 'auto';
            el.style.marginTop = '0';
        }}
    }})()""")

    # Emulate print media
    await page.emulate_media(media="print")
    await page.wait_for_timeout(500)

    # Measure the visible section height in CSS px
    height_px = await page.evaluate(f"""() => {{
        const el = document.querySelector('{measure_selector}');
        return el ? el.getBoundingClientRect().height : 0;
    }}""")

    if height_px <= 0:
        print(f"  Warning: {measure_selector} has zero height — skipping", file=sys.stderr)
        await page.close()
        return False

    # Inject @page rule using px units — the browser handles the conversion
    await page.evaluate(f"""(() => {{
        const style = document.createElement('style');
        style.textContent = '@page {{ size: {PAGE_WIDTH_MM}mm {height_px}px; margin: 0; }}';
        document.head.appendChild(style);
    }})()""")

    height_mm = height_px * 25.4 / 96
    print(f"    {measure_selector}: {height_px:.0f}px → ~{height_mm:.1f}mm")

    await page.pdf(
        path=str(pdf_path),
        prefer_css_page_size=True,
        print_background=True,
        margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
    )
    await page.close()
    return True


async def html_to_pdf(html_path: Path, pdf_path: Path, page1_only: bool = False):
    """Convert a WinWire HTML file to a content-fitted PDF."""
    tmp_dir = Path(tempfile.mkdtemp(prefix="winwire_pdf_"))

    try:
        tmp_p1 = tmp_dir / "page1.pdf"
        tmp_p2 = tmp_dir / "page2.pdf"

        async with async_playwright() as p:
            browser = await p.chromium.launch()

            # Generate page 1
            print("  Generating page 1...")
            ok_p1 = await generate_page(
                browser, html_path, tmp_p1,
                hide_selector=".page-break",
                measure_selector=".page1"
            )

            # Generate page 2 (unless page1_only)
            ok_p2 = False
            if not page1_only:
                print("  Generating page 2...")
                ok_p2 = await generate_page(
                    browser, html_path, tmp_p2,
                    hide_selector=".page1",
                    measure_selector=".page-break"
                )

            await browser.close()

        if not ok_p1:
            print("Error: page 1 generation failed", file=sys.stderr)
            return False

        # Merge if both pages exist
        if ok_p2:
            from pypdf import PdfWriter
            writer = PdfWriter()
            writer.append(str(tmp_p1))
            writer.append(str(tmp_p2))
            pdf_path.parent.mkdir(parents=True, exist_ok=True)
            writer.write(str(pdf_path))
            writer.close()
        else:
            pdf_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(tmp_p1), str(pdf_path))

        size_kb = pdf_path.stat().st_size / 1024
        print(f"  ✓ {pdf_path.name} ({size_kb:.0f} KB)")
        return True

    finally:
        # Clean up temp files
        shutil.rmtree(tmp_dir, ignore_errors=True)


def main():
    parser = argparse.ArgumentParser(description="Convert WinWire HTML to content-fitted PDF")
    parser.add_argument("--html", required=True, help="Input HTML file path")
    parser.add_argument("--output", required=True, help="Output PDF file path")
    parser.add_argument("--page1-only", action="store_true",
                        help="Only generate page 1 (skip page 2)")
    args = parser.parse_args()

    html_path = Path(args.html).resolve()
    pdf_path = Path(args.output).resolve()

    if not html_path.exists():
        print(f"Error: HTML file not found: {html_path}", file=sys.stderr)
        sys.exit(1)

    print(f"Converting {html_path.name}...")
    success = asyncio.run(html_to_pdf(html_path, pdf_path, page1_only=args.page1_only))
    if not success:
        sys.exit(1)
    print("Done!")


if __name__ == "__main__":
    main()
