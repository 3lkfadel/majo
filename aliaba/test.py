import asyncio
import re
from playwright.async_api import async_playwright
import csv
from selectorlib import Extractor

async def parse(page, search_text, extractor):
    html_content = await page.content()
    return extractor.extract(html_content, base_url=page.url)

async def process_page(page, url, search_text, extractor, max_pages, writer, current_page_no=1):
    try:
        await page.goto(url)
        data = await parse(page, search_text, extractor)
        if 'Products' not in data:
            print("No 'Products' key found in data.")
            return
        
        product = data['Products']
        if product is None:
            print("No product data found.")
            return
        
       
        writer.writerow([product.get('name', 'N/A'), product.get('price', 'N/A'), product.get('seller_name', 'N/A'), product.get('Link', 'N/A'), product.get('image_url', 'N/A')])
        print(f"Product written to CSV: {product}")

#truc de page la 
        if data['Products'] and current_page_no < max_pages:
            next_page_no = current_page_no + 1
            next_page_url = re.sub(r'(page=\d+)|$', lambda match: f'page={next_page_no}' if match.group(1) else f'&page={next_page_no}', url)
            await process_page(page, next_page_url, search_text, extractor, max_pages, writer, next_page_no)

    except Exception as e:
        print(f"Error processing page: {e}")

async def start_requests(page, extractor, max_pages):
    with open("keywords.csv") as search_keywords, open("alibaba_products.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        # Write CSV header
        writer.writerow(["Name", "Price", "Seller Name", "Link","Image URL"])

        reader = csv.DictReader(search_keywords)
        for keyword in reader:
            search_text = keyword["keyword"]
            url = f"https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&CatId=&SearchText={search_text}&viewtype=G&page=1"
            await process_page(page, url, search_text, extractor, max_pages, writer)

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

#route du yaml fait avec selector
        extractor = Extractor.from_yaml_file("aliaba/goku.yml")
        max_pages = 20

        await start_requests(page, extractor, max_pages)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())




