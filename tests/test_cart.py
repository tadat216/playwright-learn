import re
import pytest
import asyncio
from playwright.async_api import Page, expect, async_playwright

async def login(page: Page, username: str, password: str):
    await page.get_by_placeholder("Username").fill(username)
    await page.get_by_placeholder("Password").fill(password)
    await page.locator("#login-button").click()
    await expect(page).to_have_url(re.compile("/inventory.html"))

@pytest.mark.asyncio
@pytest.mark.parametrize("username,password", [
    ("standard_user", "secret_sauce"),
    ("problem_user", "secret_sauce"),
    ("error_user", "secret_sauce"),
])
async def test_cart_display_updated(page: Page, username: str, password: str):
    await login(page, username, password)
    items = page.locator(".inventory_item")
    count = await items.count()
    for index in range(count):
        await items.nth(index).locator(".btn_inventory").click()
        await expect(page.locator(".shopping_cart_badge")).to_have_text(str(index + 1))
    