from playwright.async_api import Browser

class HimalayasWebsite():
    DATA_ANALYST_JOBS = 'https://himalayas.app/jobs/data-analyst'
    DATA_SCIENTIST_JOBS = 'https://himalayas.app/jobs/data-scientist'
    BUSINESS_ANALYST_JOBS = 'https://himalayas.app/jobs/business-analyst'
    DATA_ENGINEER_JOBS = 'https://himalayas.app/jobs/data-engineer'

    _BASE_URL = 'https://himalayas.app'

    def __init__(self, url):
        self._url = url
    
    def get_url(self):
        return self._url

    async def scrape(self, browser: Browser):
        job_titles = []
        page = await browser.new_page()
        url = self.get_url()
        print(f"Scraping URL: {url}")
        await page.goto(url, timeout=60000)

        # Wait for the job list to be present
        await page.wait_for_selector('.text-xl.font-medium.text-gray-900.md\\:w-112.md\\:truncate')

        joblist = page.locator('.w-full.flex-1')
            
        for job_index in range(await joblist.count()):
            try:

                job_title_selector = '.text-xl.font-medium.text-gray-900.md\\:w-112.md\\:truncate'
                job_title = await joblist.nth(job_index).locator(job_title_selector).inner_text()
                print(job_title)

                job_link_selector = '.text-xl.font-medium.text-gray-900.md\\:w-112.md\\:truncate'
                job_link = await joblist.nth(job_index).locator(job_link_selector).get_attribute('href')
                job_link = self._BASE_URL + job_link
                print(job_link)

                job_company_selector = '.inline-flex.items-center.font-medium.text-gray-900'
                job_company = await joblist.nth(job_index).locator(job_company_selector).inner_text()
                print(job_company)

                # Opening job description page
                subpage = await browser.new_page()
                subpage.set_default_navigation_timeout(30000)
                subpage.set_default_timeout(30000)
                await subpage.goto(job_link, timeout=0)

                job_description_selector = 'xpath=/html/body/main/section[2]/div/div[1]/div/div'
                job_description = subpage.locator(job_description_selector).nth(0)
                job_description = await job_description.inner_text()
                print(job_description)
                await subpage.close()
            
            except Exception as ex:
                print(ex)

        await page.close()

        return job_titles

