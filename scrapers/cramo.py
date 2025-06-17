from playwright.sync_api import sync_playwright

# Base URL and target product category
BASE_URL = "https://www.cramo.fi"
URL = BASE_URL + "/fi/category/rakennuskoneet_sahkoistys-ja-valaistus_generaattorit-diesel"

def get_cramo_titles():
    with sync_playwright() as p:
        # Launch the browser in headless mode
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print(f"Opening {URL}")
        page.goto(URL, wait_until='networkidle')

        # Wait until product cards are loaded on the page
        print("Waiting for product cards to appear...")
        page.wait_for_selector("article.product-card", timeout=20000)

        # Scroll to the bottom to load all products (handles lazy loading)
        previous_height = 0
        while True:
            current_height = page.evaluate("document.body.scrollHeight")
            if current_height == previous_height:
                break
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(1000)  # Wait for new products to load
            previous_height = current_height

        # Collect all product card elements
        card_elements = page.query_selector_all("article.product-card")

        titles = []
        for i, card in enumerate(card_elements):
            try:
                # Scroll the card into view to trigger price loading
                card.scroll_into_view_if_needed()
                page.wait_for_timeout(300)  # Wait a bit for price to load

                title_elem = card.query_selector("div.product-card-title")
                brand_elem = card.query_selector("div.product-card-brand")
                img_elem = card.query_selector("div.product-card-image img")
                link_elem = card.query_selector("a.product-card-content")
                price_elem = card.query_selector("span.price-amount")
                currency_elem = card.query_selector("span.price-currency")
                tax_elem = card.query_selector("span.price-vat")

                title = title_elem.inner_text().strip() if title_elem else ""
                brand = brand_elem.inner_text().strip() if brand_elem else ""
                photo_url = img_elem.get_attribute("src") if img_elem else ""
                rel_link = link_elem.get_attribute("href") if link_elem else ""
                product_link = BASE_URL + rel_link if rel_link else ""

                price_amount = price_elem.inner_text().strip() if price_elem else ""
                price_currency = currency_elem.inner_text().strip() if currency_elem else ""
                price_tax_text = tax_elem.inner_text().strip() if tax_elem else ""

                titles.append((
                    title, brand, product_link, photo_url,
                    price_amount, price_currency, price_tax_text
                ))
            except Exception as e:
                print(f"Error reading card {i}: {e}")

        # Close the browser after scraping
        browser.close()
        return titles
