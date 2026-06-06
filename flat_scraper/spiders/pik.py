import scrapy
import json
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
                      "Chrome/124.0.0.0 Safari/537.36",
    }

    def start_requests(self):
        for project_name, url in PIK_START_URLS.items():
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={'project_name': project_name}
            )

    def parse(self, response):
        project_name = response.meta.get('project_name', '')

        data = json.loads(response.text)
        flats = data.get('flats', [])

        if not flats:
            self.logger.info(f"Квартиры не найдены: {project_name}")
            return

        flat = flats[0]
        rooms = flat.get('rooms')
        area = flat.get('area')
        title = f"{rooms} комн. {area} м²" if rooms and area else None

        yield {
            "project_name": project_name,
            "url": flat.get('url'),
            "title": title,
            "price": flat.get('price'),
        }
