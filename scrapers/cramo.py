from playwright.sync_api import sync_playwright

URL = "https://www.cramo.fi/fi/category/rakennuskoneet_sahkoistys-ja-valaistus_generaattorit-diesel"

def get_cramo_titles():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print(f"Opening {URL}")
        page.goto(URL, wait_until='networkidle')

        print("Waiting for product titles to appear...")
        page.wait_for_selector("div.product-card-title", timeout=15000)

        title_elements = page.query_selector_all("div.product-card-title")
        print(f"Found {len(title_elements)} titles, printing first 5:\n")

        titles = []
        for i, elem in enumerate(title_elements[:5]):
            title = elem.inner_text().strip()
            print(f"{i + 1}: {title}")
            titles.append(title)

        browser.close()
        return titles  # 🔁 PALAUTUS
