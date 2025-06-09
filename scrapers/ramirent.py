from playwright.sync_api import sync_playwright

URL = "https://www.ramirent.fi/tuoteryhmat/generaattorit/"

def get_ramirent_titles():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            print(f"Opening {URL}")
            page.goto(URL, wait_until='networkidle')

            print("Waiting for product cards to appear...")
            page.wait_for_selector("article.em-block-product-card", timeout=20000)

            card_elements = page.query_selector_all("article.em-block-product-card")
            print(f"Found {len(card_elements)} cards, printing first 5:\n")

            titles = []
            for i, card in enumerate(card_elements[:5]):
                try:
                    title_elem = card.query_selector("span.screen-reader-text")
                    img_elem = card.query_selector("div.em-block-product-card__image img")
                    title = title_elem.inner_text().strip() if title_elem else ""
                    photo_url = img_elem.get_attribute("src") if img_elem else ""
                    print(f"{i + 1}: {title} | {photo_url}")
                    titles.append((title, photo_url))
                except Exception as e:
                    print(f"Error reading card {i}: {e}")

            browser.close()
            print("Returning titles...\n")
            return titles

    except Exception as e:
        print(f"Ramirent scraping failed: {e}")
        return []

