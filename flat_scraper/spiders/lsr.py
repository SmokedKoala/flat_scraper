# import scrapy
# from urllib.parse import urljoin
# from flat_scraper.config import LSR_START_URLS

# class LsrHtmlSpider(scrapy.Spider):
#     name = "lsr"

#     custom_settings = {
#         "ROBOTSTXT_OBEY": False,
#         "FEEDS": {
#             "flats.csv": {"format": "csv", "encoding": "utf-8"},
#         },
#         "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#                       "AppleWebKit/537.36 (KHTML, like Gecko) "
#                       "Chrome/123.0 Safari/537.36",
#     }

#     def start_requests(self):
#         """Generate requests from URL dictionary with project names"""
#         for project_name, url in LSR_START_URLS.items():
#             yield scrapy.Request(
#                 url=url,
#                 callback=self.parse,
#                 meta={'project_name': project_name}
#             )

#     def parse(self, response):
#         # Получаем проектное имя из метаданных запроса
#         project_name = response.meta.get('project_name', '')
        
#         # Получаем **первую карточку** как Selector
#         card = response.css("div.listingCard.listingCard--isFlat").get()
#         if not card:
#             self.logger.info("Карточки не найдены")
#             return

#         # Преобразуем HTML строки обратно в Selector
#         card_sel = scrapy.Selector(text=card)

#         # Ссылка
#         rel_url = card_sel.css("a.listingCard__linkWrapper::attr(href)").get()
#         url = urljoin("https://www.lsr.ru/", rel_url) if rel_url else None

#         # Название (первый span.h4 в listingCard__main)
#         title = card_sel.css("div.listingCard__main > span.h4:first-child::text").get()
#         if title:
#             title = title.strip()

#         # Цена (пробуем оба варианта: isHiddenInGrid и isColorAlizarinCrimson)
#         price = card_sel.css("span.h4.isHiddenInGrid::text").get()
#         if not price:
#             price = card_sel.css("span.h4.isColorAlizarinCrimson.isVisibleInGrid::text").get()
#         if price:
#             price = price.strip()

#         yield {
#             "project_name": project_name,
#             "url": url,
#             "title": title,
#             "price": price,
#         }
