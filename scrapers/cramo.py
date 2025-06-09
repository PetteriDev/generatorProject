from playwright.sync_api import sync_playwright

URL = "https://www.cramo.fi/fi/category/rakennuskoneet_sahkoistys-ja-valaistus_generaattorit-diesel"

def get_cramo_titles():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print(f"Opening {URL}")
        page.goto(URL, wait_until='networkidle')

        # Accept cookies if present
        try:
            page.click('button#onetrust-accept-btn-handler', timeout=5000)
            print("Accepted cookies.")
        except Exception:
            pass

        print("Waiting for product cards to appear...")
        page.wait_for_selector("article.product-card", timeout=20000)

        card_elements = page.query_selector_all("article.product-card")
        print(f"Found {len(card_elements)} cards, printing first 5:\n")

        titles = []
        for i, card in enumerate(card_elements[:5]):
            title_elem = card.query_selector("div.product-card-title")
            img_elem = card.query_selector("div.product-card-image img")
            title = title_elem.inner_text().strip() if title_elem else ""
            photo_url = img_elem.get_attribute("src") if img_elem else ""
            print(f"{i + 1}: {title} | {photo_url}")
            titles.append((title, photo_url))

        browser.close()
        return titles
