import scrapy
import re
from urllib.parse import urljoin
from flat_scraper.config import PIK_START_URLS

class PikHtmlSpider(scrapy.Spider):
    name = "pik"

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
        for project_name, url in PIK_START_URLS.items():
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
        card = response.css("div[id^='listing_flat_']").get()
        if not card:
            self.logger.info("Карточки не найдены")
            return

        # Преобразуем HTML строки обратно в Selector
        card_sel = scrapy.Selector(text=card)

        # Ссылка
        rel_url = card_sel.css("a::attr(href)").get()
        url = urljoin("https://www.pik.ru", rel_url) if rel_url else None

        # Название - из span.sc-bEeDdh.ejIZJO (2 комнаты, 46.3 м²)
        title = card_sel.css('span.sc-bEeDdh.ejIZJO::text').get()
        if not title:
            # Альтернативный селектор по частичному совпадению класса
            title = card_sel.xpath(".//span[contains(@class, 'sc-bEeDdh')]//text()").get()
        if not title:
            # Еще один вариант - ищем span с описанием квартиры
            title = card_sel.xpath(".//span[contains(text(), 'комнат')]//text()").get()
        if title:
            title = title.strip()

        # Цена - из span.sc-kACOFk.eCqpmK (22 391 310 ₽)
        # Пробуем разные варианты селекторов
        price = card_sel.css('span.sc-kACOFk.eCqpmK::text').get()
        if not price:
            # Альтернативный CSS селектор
            price = card_sel.css('span.sc-kACOFk::text').get()
        if not price:
            # XPath - получаем прямой текст из span (не вложенный)
            price = card_sel.xpath(".//span[contains(@class, 'sc-kACOFk') and contains(@class, 'eCqpmK')]/text()").get()
        if not price:
            # XPath - получаем текст из span внутри sc-gJfQTX (первый span с ценой)
            price = card_sel.xpath(".//div[contains(@class, 'sc-fukmEy')]//span[contains(@class, 'sc-gJfQTX')]//span[contains(@class, 'sc-kACOFk')]/text()").get()
        if not price:
            # XPath - ищем span с классом sc-kACOFk (любой вариант)
            price = card_sel.xpath(".//span[contains(@class, 'sc-kACOFk')]/text()").get()
        if not price:
            # XPath - ищем первый span с ценой (содержит ₽), исключая sc-gMIrBl
            price = card_sel.xpath(".//span[contains(text(), '₽') and not(contains(@class, 'sc-gMIrBl'))]/text()").get()
        if not price:
            # Последний вариант - ищем в структуре sc-LAAhi первый span с ценой
            price = card_sel.xpath(".//div[contains(@class, 'sc-LAAhi')]//span[contains(@class, 'sc-gJfQTX')]//span/text()").get()
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
