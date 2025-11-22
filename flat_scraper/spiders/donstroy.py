# import scrapy
# from urllib.parse import urljoin
# from flat_scraper.config import DONSTROY_START_URLS


# class DonstroySpider(scrapy.Spider):
#     name = "donstroy"

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
#         for project_name, url in DONSTROY_START_URLS.items():
#             yield scrapy.Request(
#                 url=url,
#                 callback=self.parse,
#                 meta={'project_name': project_name}
#             )

#     def parse(self, response):
#         # Получаем проектное имя из метаданных запроса
#         project_name = response.meta.get('project_name', '')
        
#         # Получаем **первую карточку** как Selector
#         card = response.css("div.d-flat-card").get()
#         if not card:
#             self.logger.info("Карточки не найдены")
#             return

#         # Преобразуем HTML строки обратно в Selector
#         card_sel = scrapy.Selector(text=card)

#         # Ссылка - ищем ссылку на квартиру в элементе d-flat-card__link
#         rel_url = card_sel.css("a.d-flat-card__link::attr(href)").get()
#         if not rel_url:
#             rel_url = card_sel.xpath(".//a[contains(@class, 'd-flat-card__link')]/@href").get()
#         url = urljoin("https://donstroy.moscow", rel_url) if rel_url else None

#         # Название - из d-flat-card__title (включая текст внутри span)
#         title_parts = card_sel.xpath(".//div[contains(@class, 'd-flat-card__title')]//text()").getall()
#         if title_parts:
#             title = "".join(title_parts).strip()
#         else:
#             title = None

#         # Цена - из d-flat-card__price (текущая цена, не старая)
#         # Старая цена в d-flat-card__priceOld, текущая цена - это прямой текстовый узел после старой цены
#         # Получаем прямые текстовые узлы из d-flat-card__price (не внутри дочерних элементов)
#         price_nodes = card_sel.xpath(".//div[contains(@class, 'd-flat-card__price')]/text()[normalize-space()]").getall()
#         if price_nodes:
#             # Берем последний непустой элемент (текущая цена после старой цены)
#             price = [p.strip() for p in price_nodes if p.strip()][-1] if price_nodes else None
#         else:
#             # Если не нашли прямые текстовые узлы, получаем весь текст и исключаем старую цену
#             all_price_text = card_sel.xpath(".//div[contains(@class, 'd-flat-card__price')]//text()[normalize-space()]").getall()
#             old_price_text = card_sel.xpath(".//div[contains(@class, 'd-flat-card__priceOld')]//text()[normalize-space()]").getall()
#             if all_price_text:
#                 # Фильтруем, убирая текст старой цены
#                 old_price_set = {op.strip() for op in old_price_text if op.strip()}
#                 price = [p.strip() for p in all_price_text if p.strip() and p.strip() not in old_price_set]
#                 price = price[-1] if price else None
#             else:
#                 price = None
        
#         if price and isinstance(price, str):
#             price = price.strip()

#         yield {
#             "project_name": project_name,
#             "url": url,
#             "title": title,
#             "price": price,
#         }

