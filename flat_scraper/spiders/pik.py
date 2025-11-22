import scrapy
from urllib.parse import urljoin
from flat_scraper.config import PIK_START_URLS

class PikHtmlSpider(scrapy.Spider):
    name = "pik_html"

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

        # Название
        title = card_sel.css('span.sc-kMizLa.lcxtwE::text').get()
        if not title:
            title = card_sel.xpath(".//div[contains(@class,'eSyyrj')]/text()").get()

        # Цена
        price = card_sel.css('span.sc-kprGbJ.gjMelT::text').get()
        if not price:
            price = card_sel.xpath(".//div[contains(@class,'eMgPOy')]/text()").get()

        yield {
            "project_name": project_name,
            "url": url,
            "title": title,
            "price": price,
        }
