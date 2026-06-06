import scrapy
import re
from urllib.parse import urljoin
from flat_scraper.config import LEVEL_START_URLS


class LevelSpider(scrapy.Spider):
    name = "level"

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
        for project_name, url in LEVEL_START_URLS.items():
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
        # Используем data-test-id для надежности
        card = response.css('div[data-test-id="filter-flat-card-desk"]').get()
        if not card:
            # Альтернативный селектор по классу
            card = response.css("div._item_avih5_55").get()
        if not card:
            self.logger.info("Карточки не найдены")
            return

        # Преобразуем HTML строки обратно в Selector
        card_sel = scrapy.Selector(text=card)

        # Ссылка - ищем ссылку на квартиру в элементе a с классом _card_avih5_158
        rel_url = card_sel.css("a._card_avih5_158::attr(href)").get()
        if not rel_url:
            # Альтернативный способ - ищем любую ссылку внутри карточки, которая начинается с /flat/
            rel_url = card_sel.xpath(".//a[starts-with(@href, '/') and contains(@href, '/flat/')]/@href").get()
        url = urljoin("https://level.ru", rel_url) if rel_url else None

        # Название — ищем по стабильному префиксу класса (хеш-суффикс меняется при пересборке)
        title_parts = card_sel.xpath(".//*[contains(@class, '_title_')]//text()").getall()
        if title_parts:
            title = "".join([part.strip() for part in title_parts if part.strip()]).strip()
        else:
            title = None

        # Цена - из span с data-test-id="filter-flat-price-desk"
        price = card_sel.css('span[data-test-id="filter-flat-price-desk"]::text').get()
        if not price:
            # Альтернативный способ - ищем в элементе с классом _price_1r319_27
            price = card_sel.css("p._price_1r319_27 span::text").get()
        if not price:
            # Еще один вариант - получить текст из span внутри _price_1r319_27
            price = card_sel.xpath(".//p[contains(@class, '_price_1r319_27')]//span[not(contains(@class, 'vtag'))]//text()").get()
        
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

