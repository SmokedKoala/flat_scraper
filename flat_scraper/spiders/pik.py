import scrapy
from urllib.parse import urljoin

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

    start_urls = [
        "https://www.pik.ru/search/sp?rooms=2,3&floorFrom=4&floorTo=17&status=free&sortBy=price&orderBy=asc",
        "https://www.pik.ru/search/sp?rooms=2,3&areaFrom=55&floorFrom=4&floorTo=17&status=free&sortBy=price&orderBy=asc",
        "https://www.pik.ru/search/kron9?rooms=2,3&floorFrom=4&floorTo=32&status=free&sortBy=price&orderBy=asc",
        "https://www.pik.ru/search/kron9?rooms=2,3&areaFrom=55&floorFrom=4&floorTo=32&status=free&sortBy=price&orderBy=asc"
    ]

    def parse(self, response):
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
            "url": url,
            "title": title,
            "price": price,
        }
