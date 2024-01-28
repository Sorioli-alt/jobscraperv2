from .websites.himalayaswebsite import HimalayasWebsite as himalayas
from playwright.async_api import async_playwright
import asyncio

async def main():
    playwright = await async_playwright().start()
    sites = [himalayas(himalayas.DATA_ANALYST_JOBS),
             himalayas(himalayas.BUSINESS_ANALYST_JOBS),
             himalayas(himalayas.DATA_SCIENTIST_JOBS),
             himalayas(himalayas.DATA_ENGINEER_JOBS)]
    
    for site in sites:
        browser = None
        try:
            browser = await playwright.chromium.launch(headless=True)
            await site.scrape(browser)
            await browser.close()
        
        except Exception as e:
            print(e)
            if browser is not None:
                await browser.close()
    await playwright.stop()

def execute():
    asyncio.run(main())

if __name__ == '__main__':
    execute()
