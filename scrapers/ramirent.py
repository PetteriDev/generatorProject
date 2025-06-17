from playwright.sync_api import sync_playwright

# Base URL and generator product listing
BASE_URL = "https://www.ramirent.fi"
URL = BASE_URL + "/tuoteryhmat/generaattorit/"

def get_ramirent_titles():
    with sync_playwright() as p:
        # Launch the browser in headless mode
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print(f"Opening {URL}")
        page.goto(URL, wait_until='networkidle')

        # Wait until product cards are visible on the page
        print("Waiting for product cards to appear...")
        page.wait_for_selector("article.em-block-product-card", timeout=20000)

        # Get all product card elements
        card_elements = page.query_selector_all("article.em-block-product-card")

        titles = []
        for i, card in enumerate(card_elements):
            try:
                # Extract product link
                link_elem = card.query_selector("a.em-block-product-card__link")
                rel_link = link_elem.get_attribute("href") if link_elem else ""
                product_link = BASE_URL + rel_link if rel_link else ""

                # Extract image URL
                img_elem = card.query_selector("div.em-block-product-card__image img")
                photo_url = img_elem.get_attribute("src") if img_elem else ""

                # Extract product title and model/brand
                title_elem = card.query_selector("span.screen-reader-text")
                model_elem = card.query_selector("p.em-block-product-card__model")
                title = title_elem.inner_text().strip() if title_elem else ""
                brand_or_model = model_elem.inner_text().strip() if model_elem else ""

                # Extract VAT-free price
                price_elem = card.query_selector(
                    'span.em-block-product-card__price.product__price-daily__value[data-price-has-vat="false"]'
                )
                price_amount = price_elem.inner_text().replace('\xa0', ' ').replace('€', '').strip() if price_elem else ""
                price_currency = "€"
                price_tax_text = "ei sis. ALV"

                # Append collected data
                titles.append((
                    title, brand_or_model, product_link, photo_url,
                    price_amount, price_currency, price_tax_text
                ))
            except Exception as e:
                print(f"Error reading card {i}: {e}")

        # Close browser after scraping
        browser.close()
        return titles
