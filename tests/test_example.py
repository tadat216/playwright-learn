import re
from playwright.sync_api import Page, expect
import pytest

@pytest.mark.skip()
def test_has_title(page: Page):
    page.goto("/")
    expect(page).to_have_title(re.compile("Swag Labs"))

@pytest.mark.skip()
def test_login_standard_user(page: Page):
    page.goto("/")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.locator("#login-button").click()
    expect(page).to_have_url(re.compile("/inventory.html"))
    expect(page.get_by_text("Products")).to_be_visible()

@pytest.mark.skip()
def test_logout(page: Page):
    test_login_standard_user(page)
    page.locator('#react-burger-menu-btn').click()
    page.locator('#logout_sidebar_link').click()
    expect(page).to_have_url(re.compile("/"))

@pytest.mark.skip()
def test_add_to_cart(page: Page):
    #step 1: login
    test_login_standard_user(page)
    product = page.locator('.inventory_item').nth(0) #First product
    #step 2: check have to card button
    expect(product.locator('.btn_inventory')).to_have_text("Add to cart")
    #step 3: add first item to cart
    product.locator('.btn_inventory').click()
    #check if cart has 1 item
    expect(page.locator('#shopping_cart_container')).to_have_text("1") 
    
@pytest.mark.skip()
def test_remove_from_cart(page: Page):
    #step 1: add to cart
    test_add_to_cart(page)
    #step 2: check if product card has remove button  
    product = page.locator('.inventory_item').nth(0) #First product
    expect(product.locator('.btn_inventory')).to_have_text("Remove")
    #step 3: click on remove button
    product.locator('.btn_inventory').click()
    #step 4: check if cart is empty
    expect(page.locator('#shopping_cart_container')).to_have_text("")

@pytest.mark.skip()
def test_checkout(page: Page):
    #step 1: add product to cart
    test_add_to_cart(page)
    #step 2: click on cart icon
    page.locator('#shopping_cart_container').click()
    expect(page).to_have_url(re.compile("/cart.html"))
    #step 3: click on checkout button
    page.locator('#checkout').click()
    #step 4: fill in the form
    page.locator('#first-name').fill("Dat")
    page.locator('#last-name').fill("Ta")
    page.locator('#postal-code').fill("12345")
    page.locator('#continue').click()
    #step 5: click on finish button
    page.locator('#finish').click()
    #step 6: check if order is completed
    expect(page).to_have_url(re.compile("/checkout-complete.html"))
    #step 7: go to product page
    page.locator('#back-to-products').click()
    expect(page).to_have_url(re.compile("/inventory.html"))