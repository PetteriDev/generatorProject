from playwright.sync_api import sync_playwright

URL = "https://www.ramirent.fi/tuoteryhmat/generaattorit/"

def get_ramirent_titles():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            print(f"Opening {URL}")
            page.goto(URL, wait_until='networkidle')

            print("Waiting for product titles to appear...")
            page.wait_for_selector("a.em-block-product-card__link span.screen-reader-text", timeout=15000)

            span_elements = page.query_selector_all("a.em-block-product-card__link span.screen-reader-text")
            print(f"Found {len(span_elements)} titles, printing first 5:\n")

            titles = []
            for i, elem in enumerate(span_elements[:5]):
                try:
                    raw_text = elem.inner_text().strip()
                    cleaned_text = raw_text.replace('\xa0', ' ')
                    print(f"{i + 1}: {cleaned_text}")
                    titles.append(cleaned_text)
                except Exception as e:
                    print(f"Error reading title {i}: {e}")

            browser.close()
            print("Returning titles...\n")
            return titles

    except Exception as e:
        print(f"Ramirent scraping failed: {e}")
        return []

