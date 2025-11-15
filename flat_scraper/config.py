# URL Configuration for Scrapy Spiders
# Add or modify URLs here to control which pages the spider will scrape

# URLs for PikHtmlSpider
PIK_START_URLS = [
    "https://www.pik.ru/search/sp?rooms=2,3&floorFrom=4&floorTo=17&status=free&sortBy=price&orderBy=asc",
    "https://www.pik.ru/search/sp?rooms=2,3&areaFrom=55&floorFrom=4&floorTo=17&status=free&sortBy=price&orderBy=asc",
    "https://www.pik.ru/search/kron9?rooms=2,3&floorFrom=4&floorTo=32&status=free&sortBy=price&orderBy=asc",
    "https://www.pik.ru/search/kron9?rooms=2,3&areaFrom=55&floorFrom=4&floorTo=32&status=free&sortBy=price&orderBy=asc"
]

# URLs for A101Spider
A101_START_URLS = [
    "https://a101.ru/kvartiry/?order=actual_price&floor_max=16&floor_min=4&room=2,3,-2&project=dom-na-zorge",
    "https://a101.ru/kvartiry/?order=actual_price&area_max=87.3&area_min=55&floor_max=16&floor_min=4&room=2,3,-2&project=dom-na-zorge"
]

# You can add more URL configurations for other spiders here
# EXAMPLE_SPIDER_URLS = [
#     "https://example.com/page1",
#     "https://example.com/page2",
# ]

