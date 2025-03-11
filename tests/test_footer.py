import re
from playwright.sync_api import Page, expect
import pytest

@pytest.mark.skip()
def test_login(page: Page, username: str, password: str):
    page.goto("/")
    page.get_by_placeholder("Username").fill(username)
    page.get_by_placeholder("Password").fill(password)
    page.locator("#login-button").click()
    expect(page).to_have_url(re.compile("/inventory.html"))

@pytest.mark.parametrize("username,password", [
    ("standard_user", "secret_sauce"),
    ("problem_user", "secret_sauce"),
    ("performance_glitch_user", "secret_sauce")
])
def test_footer_is_displayed(page: Page, username: str, password: str):
    test_login(page, username, password)
    footer = page.locator(".footer")
    expect(footer).to_be_visible()

@pytest.mark.parametrize("username,password", [
    ("standard_user", "secret_sauce"),
    ("problem_user", "secret_sauce"),
    ("performance_glitch_user", "secret_sauce")
])
def test_footer_text_is_correct(page: Page, username: str, password: str):
    test_login(page, username, password)
    expect(page.locator(".footer_copy")).to_have_text("© 2025 Sauce Labs. All Rights Reserved. Terms of Service | Privacy Policy")

@pytest.mark.parametrize("username,password", [
    ("standard_user", "secret_sauce"),
    ("problem_user", "secret_sauce"),
    ("performance_glitch_user", "secret_sauce")
])
def test_twitter_link(page: Page, username: str, password: str):
    test_login(page, username, password)
    with page.expect_popup() as popup_info:
        page.locator(".social_twitter a").click()
    twitter_page = popup_info.value
    expect(twitter_page).to_have_url(re.compile("x.com"))

@pytest.mark.parametrize("username,password", [
    ("standard_user", "secret_sauce"),
    ("problem_user", "secret_sauce"),
    ("performance_glitch_user", "secret_sauce")
])
def test_facebook_link(page: Page, username: str, password: str):
    test_login(page, username, password)
    with page.expect_popup() as popup_info:
        page.locator(".social_facebook a").click()
    facebook_page = popup_info.value
    expect(facebook_page).to_have_url(re.compile("facebook.com"))

@pytest.mark.parametrize("username,password", [
    ("standard_user", "secret_sauce"),
    ("problem_user", "secret_sauce"),
    ("performance_glitch_user", "secret_sauce")
])
def test_linkedin_link(page: Page, username: str, password: str):
    test_login(page, username, password)
    with page.expect_popup() as popup_info:
        page.locator(".social_linkedin a").click()
    linkedin_page = popup_info.value
    expect(linkedin_page).to_have_url(re.compile("linkedin.com"))
