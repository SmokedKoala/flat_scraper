import scrapy
import re
from urllib.parse import urljoin
from flat_scraper.config import RG_START_URLS


class RgSpider(scrapy.Spider):
    name = "rg"

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
        for project_name, url in RG_START_URLS.items():
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
        card = response.css("a.flat-card.card").get()
        if not card:
            # Альтернативный селектор
            card = response.css("a[class*='flat-card']").get()
        if not card:
            self.logger.info("Карточки не найдены")
            return

        # Преобразуем HTML строки обратно в Selector
        card_sel = scrapy.Selector(text=card)

        # Ссылка - из href атрибута
        url = card_sel.css("a::attr(href)").get()
        if url:
            # Если относительный URL, делаем его абсолютным
            if url.startswith('/'):
                url = urljoin("https://rg-dev.ru", url)
            elif not url.startswith('http'):
                url = urljoin("https://rg-dev.ru", url)

        # Название - комбинируем комнаты и площадь из flat-card__head-info
        # Получаем все div с классом flat-card__head-info _room
        info_divs = card_sel.xpath(".//div[contains(@class, 'flat-card__head-info') and contains(@class, '_room')]")
        
        title_parts = []
        for div in info_divs[:2]:  # Берем только первые 2 (комнаты и площадь)
            # Получаем весь текст из div, включая sup
            text = div.xpath(".//text()").getall()
            if text:
                # Объединяем текст и очищаем
                combined = "".join([t.strip() for t in text if t.strip()]).strip()
                # Пропускаем "Номер" и пустые строки
                if combined and not combined.startswith("Номер"):
                    title_parts.append(combined)
        
        # Если не нашли через divs, пробуем альтернативный способ
        if not title_parts:
            # Получаем комнаты
            rooms = card_sel.xpath(".//div[contains(@class, 'flat-card__head-info')]//text()[contains(., 'комнат')]").get()
            if rooms:
                title_parts.append(rooms.strip())
            
            # Получаем площадь - ищем div с м² или sup
            square_divs = card_sel.xpath(".//div[contains(@class, 'flat-card__head-info')][.//sup or contains(., 'м')]")
            if square_divs:
                square_text = square_divs[0].xpath(".//text()").getall()
                square = "".join([t.strip() for t in square_text if t.strip()]).strip()
                if square and not square.startswith("Номер"):
                    title_parts.append(square)
        
        title = ", ".join(title_parts) if title_parts else None

        # Цена - из div.flat-card__val.c-red.fw-sb
        price = card_sel.css("div.flat-card__val.c-red.fw-sb::text").get()
        if not price:
            # Альтернативный селектор
            price = card_sel.xpath(".//div[contains(@class, 'flat-card__val') and contains(@class, 'c-red') and contains(@class, 'fw-sb')]//text()").get()
        if not price:
            # Еще один вариант - ищем цену в flat-card__info-row
            price = card_sel.xpath(".//div[contains(@class, 'flat-card__info-row')]//div[contains(@class, 'c-red')]//text()").get()
        
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

