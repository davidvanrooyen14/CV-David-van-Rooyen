from playwright.sync_api import sync_playwright
from pathlib import Path

html_path = Path(__file__).parent / "index.html"
output_path = Path(__file__).parent / "David_van_Rooyen_CV.pdf"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.set_viewport_size({"width": 794, "height": 2000})
    page.goto(html_path.as_uri(), wait_until="networkidle")

    # Use screen media so the print engine doesn't paginate at A4 boundaries
    page.emulate_media(media="screen")

    # Strip screen-only cosmetic styles (shadow, body background, margins)
    page.add_style_tag(content="""
        body { background: none !important; margin: 0 !important; padding: 0 !important; }
        .cv-container { margin: 0 !important; box-shadow: none !important; }
    """)

    height = page.evaluate(
        "document.querySelector('.cv-container').getBoundingClientRect().height"
    )

    page.pdf(
        path=str(output_path),
        width="210mm",
        height=f"{height}px",
        print_background=True,
        prefer_css_page_size=False,
        margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
    )
    browser.close()

print(f"PDF saved to {output_path} ({height:.0f}px tall, single page)")
