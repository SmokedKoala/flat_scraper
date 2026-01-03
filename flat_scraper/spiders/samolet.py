# import scrapy
# import re
# from flat_scraper.config import SAMOLET_START_URLS


# class SamoletSpider(scrapy.Spider):
#     name = "samolet"

#     custom_settings = {
#         "ROBOTSTXT_OBEY": False,
#         "FEEDS": {
#             "flats.csv": {"format": "csv", "encoding": "utf-8"},
#         },
#         "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#                       "AppleWebKit/537.36 (KHTML, like Gecko) "
#                       "Chrome/123.0 Safari/537.36",
#         "HTTPERROR_ALLOWED_CODES": [401, 403, 404],  # Allow these status codes to be processed
#         "DEFAULT_REQUEST_HEADERS": {
#             "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
#             "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
#             "Accept-Encoding": "gzip, deflate, br",
#             "Referer": "https://samolet.ru/",
#             "Sec-Fetch-Dest": "document",
#             "Sec-Fetch-Mode": "navigate",
#             "Sec-Fetch-Site": "same-origin",
#             "Upgrade-Insecure-Requests": "1",
#         },
#     }

#     def start_requests(self):
#         """Generate requests from URL dictionary with project names"""
#         for project_name, url in SAMOLET_START_URLS.items():
#             yield scrapy.Request(
#                 url=url,
#                 callback=self.parse,
#                 meta={'project_name': project_name},
#                 headers={
#                     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
#                     "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
#                     "Referer": "https://samolet.ru/",
#                 },
#                 dont_filter=True
#             )

#     def clean_price(self, price_str):
#         """Convert price string to numeric value"""
#         if not price_str:
#             return None
#         # Remove all non-digit characters except decimal point
#         price_clean = re.sub(r'[^\d]', '', str(price_str))
#         try:
#             return int(price_clean) if price_clean else None
#         except (ValueError, TypeError):
#             return None

#     def parse(self, response):
#         # Получаем проектное имя из метаданных запроса
#         project_name = response.meta.get('project_name', '')
        
#         # Проверяем статус ответа
#         if response.status == 401:
#             self.logger.warning(f"Получен 401 для {response.url}. Возможно, требуется авторизация или сайт блокирует запросы.")
#             return
        
#         # Получаем **первую карточку** как Selector
#         card = response.css("a[class*='_FlatCardV2']").get()
#         if not card:
#             # Альтернативный селектор - ищем любую ссылку с классом содержащим FlatCard
#             card = response.xpath("//a[contains(@class, 'FlatCard')]").get()
#         if not card:
#             self.logger.info(f"Карточки не найдены для {response.url}. Статус: {response.status}")
#             return

#         # Преобразуем HTML строки обратно в Selector
#         card_sel = scrapy.Selector(text=card)

#         # Ссылка - из href атрибута (полный URL)
#         url = card_sel.css("a::attr(href)").get()
#         if url:
#             # Убираем параметры запроса из URL для чистоты
#             url = url.split('?')[0] if '?' in url else url

#         # Название - комбинируем комнаты и площадь из _specs
#         rooms = card_sel.xpath(".//div[contains(@class, '_rooms_')]//text()").get()
#         if not rooms:
#             rooms = card_sel.xpath(".//div[contains(@class, 'rooms')]//text()").get()
        
#         square = card_sel.xpath(".//div[contains(@class, '_square_')]//text()").get()
#         if not square:
#             square = card_sel.xpath(".//div[contains(@class, 'square')]//text()").get()
        
#         # Комбинируем комнаты и площадь
#         title_parts = []
#         if rooms:
#             title_parts.append(rooms.strip())
#         if square:
#             title_parts.append(square.strip())
        
#         title = ", ".join(title_parts) if title_parts else None

#         # Цена - из div._price_1683e_110
#         price = card_sel.xpath(".//div[contains(@class, '_price_')]//text()").get()
#         if not price:
#             # Альтернативный вариант - ищем в _head
#             price = card_sel.xpath(".//div[contains(@class, '_head_')]//div[contains(@class, '_price_')]//text()").get()
        
#         if price:
#             price = price.strip()
        
#         # Convert price to numeric value
#         price_numeric = self.clean_price(price)

#         yield {
#             "project_name": project_name,
#             "url": url,
#             "title": title,
#             "price": price_numeric,
#         }

