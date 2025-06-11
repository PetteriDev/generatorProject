from playwright.sync_api import sync_playwright

BASE_URL = "https://www.ramirent.fi"
URL = BASE_URL + "/tuoteryhmat/generaattorit/"

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
            for i, card in enumerate(card_elements):
                try:
                    link_elem = card.query_selector("a.em-block-product-card__link")
                    rel_link = link_elem.get_attribute("href") if link_elem else ""
                    product_link = BASE_URL + rel_link if rel_link else ""
                    img_elem = card.query_selector("div.em-block-product-card__image img")
                    photo_url = img_elem.get_attribute("src") if img_elem else ""
                    title_elem = card.query_selector("span.screen-reader-text")
                    title = title_elem.inner_text().strip() if title_elem else ""

                    # Go to product page for price and model
                    brand_or_model = price_amount = price_currency = price_tax_text = ""
                    if product_link:
                        detail_page = browser.new_page()
                        detail_page.goto(product_link, wait_until='networkidle')
                        model_elem = detail_page.query_selector("p.em-block-product-card__model")
                        brand_or_model = model_elem.inner_text().strip() if model_elem else ""
                        price_elem = detail_page.query_selector('span.em-block-product-card__price.product__price-daily__value[data-price-has-vat="false"]')
                        price_amount = price_elem.inner_text().replace('\xa0', ' ').replace('€', '').strip() if price_elem else ""
                        price_currency = "€"
                        price_tax_text = "ei sis. ALV"
                        detail_page.close()

                    print(f"{i + 1}: {title} | {brand_or_model} | {product_link} | {photo_url} | {price_amount} {price_currency} {price_tax_text}")
                    titles.append((
                        title, brand_or_model, product_link, photo_url,
                        price_amount, price_currency, price_tax_text
                    ))
                except Exception as e:
                    print(f"Error reading card {i}: {e}")

            browser.close()
            print("Returning titles...\n")
            return titles

    except Exception as e:
        print(f"Ramirent scraping failed: {e}")
        return []

