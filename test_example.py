import re
from playwright.sync_api import Page, expect
import pytest

def test_has_title(page: Page):
    page.goto("/")
    expect(page).to_have_title(re.compile("Swag Labs"))

def test_login_standard_user(page: Page):
    page.goto("/")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.locator("#login-button").click()
    expect(page).to_have_url(re.compile("/inventory.html"))
    expect(page.get_by_text("Products")).to_be_visible()