import scrapy
import re
from urllib.parse import urljoin
from flat_scraper.config import GRANELLE_START_URLS


class GranelleSpider(scrapy.Spider):
    name = "granelle"

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
        """Generate requests from URL dictionary with project names"""
        for project_name, url in GRANELLE_START_URLS.items():
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={'project_name': project_name}
            )

    def clean_price(self, price_str):
        """Convert price string to numeric value"""
        if not price_str:
            return None
        # Remove all non-digit characters except decimal point
        price_clean = re.sub(r'[^\d]', '', str(price_str))
        try:
            return int(price_clean) if price_clean else None
        except (ValueError, TypeError):
            return None

    def parse(self, response):
        # Получаем проектное имя из метаданных запроса
        project_name = response.meta.get('project_name', '')
        
        # Получаем **первую карточку** как Selector
        card = response.css("article[class*='FlatsGridCard']").get()
        if not card:
            # Альтернативный селектор
            card = response.css("article.card").get()
        if not card:
            self.logger.info("Карточки не найдены")
            return

        # Преобразуем HTML строки обратно в Selector
        card_sel = scrapy.Selector(text=card)

        # Ссылка - из a#FlatsGridCardContent или a с href начинающимся с /flats/
        rel_url = card_sel.css("a#FlatsGridCardContent::attr(href)").get()
        if not rel_url:
            rel_url = card_sel.xpath(".//a[starts-with(@href, '/flats/')]/@href").get()
        url = urljoin("https://granelle.ru", rel_url) if rel_url else None

        # Название - из h2.title_X67gZ (включая весь текст с sup)
        title_parts = card_sel.xpath(".//h2[contains(@class, 'title')]//text()").getall()
        if title_parts:
            title = "".join([part.strip() for part in title_parts if part.strip()]).strip()
        else:
            title = card_sel.css("h2[class*='title']::text").get()
            if title:
                title = title.strip()

        # Цена - из span.priceLabel_puyxx (не старая цена)
        price = card_sel.css("span.priceLabel_puyxx::text").get()
        if not price:
            price = card_sel.xpath(".//span[contains(@class, 'priceLabel')]//text()").get()
        if not price:
            # Альтернативный вариант - ищем в div.price_4-Z0j
            price = card_sel.xpath(".//div[contains(@class, 'price')]//span[not(ancestor::div[contains(@class, 'oldPrice')])]//text()").get()
        
        if price:
            price = price.strip()
        
        # Convert price to numeric value
        price_numeric = self.clean_price(price)

        yield {
            "project_name": project_name,
            "url": url,
            "title": title,
            "price": price_numeric,
        }

