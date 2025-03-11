import re
import pytest
import asyncio
from playwright.async_api import Page, expect, async_playwright

@pytest.mark.skip()
async def login(page: Page, username: str, password: str):
    await page.get_by_placeholder("Username").fill(username)
    await page.get_by_placeholder("Password").fill(password)
    await page.locator("#login-button").click()
    await expect(page).to_have_url(re.compile("/inventory.html"), timeout=2.0)

@pytest.mark.asyncio
@pytest.mark.parametrize("username,password", [
    ("standard_user", "secret_sauce"),
    ("problem_user", "secret_sauce"),
])
async def test_footer_is_displayed(page: Page, username: str, password: str):
    await login(page, username, password)
    footer = page.locator(".footer")
    await expect(footer).to_be_visible()

@pytest.mark.asyncio
@pytest.mark.parametrize("username,password", [
    ("standard_user", "secret_sauce"),
    ("problem_user", "secret_sauce"),
])
async def test_footer_text_is_correct(page: Page, username: str, password: str):
    await login(page, username, password)
    await expect(page.locator(".footer_copy")).to_have_text(
        "© 2025 Sauce Labs. All Rights Reserved. Terms of Service | Privacy Policy"
    )

@pytest.mark.asyncio
@pytest.mark.parametrize("username,password", [
    ("standard_user", "secret_sauce"),
    ("problem_user", "secret_sauce"),
])
async def test_social_links(page: Page, username: str, password: str):
    await login(page, username, password)

    async with page.expect_popup() as popup_info:
        await page.locator(".social_twitter a").click()
    twitter_page = await popup_info.value
    await expect(twitter_page).to_have_url(re.compile("x.com"))

    async with page.expect_popup() as popup_info:
        await page.locator(".social_facebook a").click()
    facebook_page = await popup_info.value
    await expect(facebook_page).to_have_url(re.compile("facebook.com"))

    async with page.expect_popup() as popup_info:
        await page.locator(".social_linkedin a").click()
    linkedin_page = await popup_info.value
    await expect(linkedin_page).to_have_url(re.compile("linkedin.com"))