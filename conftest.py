import pytest
import asyncio
import os
from playwright.async_api import async_playwright, Page

@pytest.fixture(scope="function")
async def page(request):
    playwright = await async_playwright().start()

    browser = await playwright.chromium.launch(
        headless=False,
        #slow_mo=700,
    )
    context = await browser.new_context()
    os.makedirs("traces", exist_ok=True)

    test_name = request.node.name
    await context.tracing.start(screenshots=True, snapshots=True)
    
    page = await context.new_page()
    
    await page.goto("https://www.saucedemo.com/")
    
    yield page

    # Lưu trace với tên file dựa trên tên test
    trace_path = f"traces/{test_name}.zip"
    await context.tracing.stop(path=trace_path)
    print(f"Trace saved to: {trace_path}")
    
    await page.close()
    await context.close()
    await browser.close()
    await playwright.stop()

@pytest.fixture(scope="session")
def event_loop_policy():
    return asyncio.get_event_loop_policy()

@pytest.mark.asyncio(loop_scope="session")
@pytest.fixture(scope="session")
def event_loop(event_loop_policy):
    loop = event_loop_policy.new_event_loop()
    yield loop
    loop.close()