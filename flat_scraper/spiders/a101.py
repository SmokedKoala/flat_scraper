import scrapy
from urllib.parse import urljoin
from flat_scraper.config import A101_START_URLS


class A101Spider(scrapy.Spider):
    name = "a101"

    custom_settings = {
        "ROBOTSTXT_OBEY": False,
        "FEEDS": {
            "flats.csv": {"format": "csv", "encoding": "utf-8"},
        },
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/123.0 Safari/537.36",
    }

    start_urls = A101_START_URLS

    def parse(self, response):
        # Получаем **первую карточку** как Selector
        card = response.css("li.card-list-item").get()
        if not card:
            self.logger.info("Карточки не найдены")
            return

        # Преобразуем HTML строки обратно в Selector
        card_sel = scrapy.Selector(text=card)

        # Ссылка - ищем ссылку на квартиру (начинается с /kvartiry/)
        rel_url = card_sel.xpath(".//a[starts-with(@href, '/kvartiry/')]/@href").get()
        if not rel_url:
            # Альтернативный вариант - ссылка с aria-label
            rel_url = card_sel.xpath(".//a[@aria-label='Перейти на страницу квартиры']/@href").get()
        if not rel_url:
            # Если не нашли, пробуем найти любую ссылку, но не из breadcrumbs проекта
            rel_url = card_sel.xpath(".//a[not(ancestor::ul[@class*='breadcrumbs']) and starts-with(@href, '/kvartiry/')]/@href").get()
        url = urljoin("https://a101.ru", rel_url) if rel_url else None

        # Название
        title = card_sel.css("h2[class*='title']::text").get()
        if not title:
            title = card_sel.xpath(".//h2[contains(@class, 'title')]//text()").get()
        
        if title:
            title = title.strip()

        # Цена (не старая цена)
        price = card_sel.css("span[class*='price']:not([class*='oldPrice'])::text").get()
        if not price:
            price = card_sel.xpath(".//span[contains(@class, 'price') and not(contains(@class, 'oldPrice'))]//text()").get()
        
        if price:
            price = price.strip()

        yield {
            "url": url,
            "title": title,
            "price": price,
        }

