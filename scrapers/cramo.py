from playwright.sync_api import sync_playwright

BASE_URL = "https://www.cramo.fi"
URL = BASE_URL + "/fi/category/rakennuskoneet_sahkoistys-ja-valaistus_generaattorit-diesel"

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
        for i, card in enumerate(card_elements):
            try:
                title_elem = card.query_selector("div.product-card-title")
                brand_elem = card.query_selector("div.product-card-brand")
                img_elem = card.query_selector("div.product-card-image img")
                link_elem = card.query_selector("a.product-card-content")
                title = title_elem.inner_text().strip() if title_elem else ""
                brand = brand_elem.inner_text().strip() if brand_elem else ""
                photo_url = img_elem.get_attribute("src") if img_elem else ""
                rel_link = link_elem.get_attribute("href") if link_elem else ""
                product_link = BASE_URL + rel_link if rel_link else ""

                # Go to product page for price
                price_amount = price_currency = price_tax_text = ""
                if product_link:
                    detail_page = browser.new_page()
                    detail_page.goto(product_link, wait_until='networkidle')
                    price_elem = detail_page.query_selector("span.price-amount")
                    price_amount = price_elem.inner_text().strip() if price_elem else ""
                    currency_elem = detail_page.query_selector("span.price-currency")
                    price_currency = currency_elem.inner_text().strip() if currency_elem else ""
                    tax_elem = detail_page.query_selector("span.price-vat")
                    price_tax_text = tax_elem.inner_text().strip() if tax_elem else ""
                    detail_page.close()

                print(f"{i + 1}: {title} | {brand} | {product_link} | {photo_url} | {price_amount} {price_currency} {price_tax_text}")
                titles.append((
                    title, brand, product_link, photo_url,
                    price_amount, price_currency, price_tax_text
                ))
            except Exception as e:
                print(f"Error reading card {i}: {e}")

        browser.close()
        return titles
