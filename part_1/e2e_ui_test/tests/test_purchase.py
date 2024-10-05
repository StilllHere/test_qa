from playwright.sync_api import sync_playwright


def test_purchase():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto('https://www.saucedemo.com')

        # Login
        page.fill('input[name="user-name"]', 'standard_user')
        page.wait_for_timeout(1000)
        page.fill('input[name="password"]', 'secret_sauce')
        page.wait_for_timeout(1000)
        page.click('input[type="submit"]')
        page.wait_for_timeout(1000)

        # Assert successful login by checking for product presence
        assert page.is_visible('div.inventory_item'), "Login failed or products not visible."
        page.wait_for_timeout(1000)

        # Add product to cart
        page.click('text=Sauce Labs Backpack')
        page.wait_for_timeout(1000)
        page.click('text=Add to cart')
        page.wait_for_timeout(1000)

        # Go to cart and verify product
        page.click('a.shopping_cart_link')
        page.wait_for_timeout(1000)
        assert page.is_visible('text=Sauce Labs Backpack'), "Product not in cart."
        page.wait_for_timeout(1000)

        # Checkout process
        page.click('text=Checkout')
        page.wait_for_timeout(1000)
        assert page.is_visible('input[name="firstName"]'), "Checkout page not loaded."

        page.fill('input[name="firstName"]', 'John')
        page.wait_for_timeout(1000)
        page.fill('input[name="lastName"]', 'Doe')
        page.wait_for_timeout(1000)
        page.fill('input[name="postalCode"]', '12345')
        page.wait_for_timeout(1000)
        page.click('text=Continue')

        # Verify summary page
        assert page.is_visible('text=Payment Information'), "Checkout information not visible."
        page.wait_for_timeout(1000)

        page.click('text=Finish')
        page.wait_for_timeout(1000)

        # Verify purchase complete
        assert page.is_visible('text=THANK YOU FOR YOUR ORDER'), "Purchase not completed successfully."
        page.wait_for_timeout(1000)

        # Close browser
        browser.close()


if __name__ == "__main__":
    test_purchase()