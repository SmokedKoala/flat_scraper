import scrapy
import re
from urllib.parse import urljoin
from flat_scraper.config import TALAN_START_URLS


class TalanSpider(scrapy.Spider):
    name = "talan"

    custom_settings = {
        "ROBOTSTXT_OBEY": False,
        "FEEDS": {
            "flats.csv": {"format": "csv", "encoding": "utf-8"},
        },
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/123.0 Safari/537.36",
    }

    def start_requests(self):
        for project_name, url in TALAN_START_URLS.items():
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={'project_name': project_name}
            )

    def clean_price(self, price_str):
        if not price_str:
            return None
        price_clean = re.sub(r'[^\d]', '', str(price_str))
        try:
            return int(price_clean) if price_clean else None
        except (ValueError, TypeError):
            return None

    def parse(self, response):
        project_name = response.meta.get('project_name', '')

        # First card — flat hrefs are UUID-style (/msk/apartments/{uuid}), contain hyphens
        card = response.xpath("(//a[contains(@href, '/msk/apartments/') and contains(@href, '-')])[1]").get()
        if not card:
            self.logger.info("Карточки не найдены")
            return

        card_sel = scrapy.Selector(text=card)

        # URL
        rel_url = card_sel.css("a::attr(href)").get()
        if not rel_url:
            rel_url = card_sel.xpath(".//@href").get()
        url = urljoin("https://talan.ru", rel_url) if rel_url else None

        # Title — rooms + area, e.g. "2 комн. 40,6 м²"
        title_parts = card_sel.xpath(".//text()").getall()
        rooms = next((t.strip() for t in title_parts if 'комн' in t), None)
        area = next((t.strip() for t in title_parts if 'м2' in t or 'м²' in t), None)
        if rooms and area:
            title = f"{rooms} {area}".strip()
        elif rooms:
            title = rooms
        else:
            title = None

        # Price — prefer "Цена при 100% оплате" value; fallback to first number with ₽
        price_text = next(
            (t.strip() for t in title_parts if '₽' in t and 'месяц' not in t and 'м2' not in t and 'м²' not in t),
            None
        )
        price_numeric = self.clean_price(price_text)

        yield {
            "project_name": project_name,
            "url": url,
            "title": title,
            "price": price_numeric,
        }
