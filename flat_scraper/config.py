# URL Configuration for Scrapy Spiders
# Add or modify URLs here to control which pages the spider will scrape

# URLs for PikHtmlSpider
PIK_START_URLS = {
    "Саларьево парк": "https://www.pik.ru/search/sp?rooms=2,3&floorFrom=4&floorTo=17&status=free&sortBy=price&orderBy=asc",
    "Саларьево парк 55+": "https://www.pik.ru/search/sp?rooms=2,3&areaFrom=55&floorFrom=4&floorTo=17&status=free&sortBy=price&orderBy=asc",
    "Кронштадтский 9": "https://www.pik.ru/search/kron9?rooms=2,3&floorFrom=4&floorTo=32&status=free&sortBy=price&orderBy=asc",
    "Кронштадтский 9 55+": "https://www.pik.ru/search/kron9?rooms=2,3&areaFrom=55&floorFrom=4&floorTo=32&status=free&sortBy=price&orderBy=asc",
    "Нарвин": "https://www.pik.ru/search/narvin?type=1&rooms=2,3&floorFrom=4&status=free&sortBy=price&orderBy=asc",
    "Нарвин 55+": "https://www.pik.ru/search/narvin?type=1&rooms=2,3&areaFrom=55&floorFrom=4&status=free&sortBy=price&orderBy=asc",
    "Большая Академическая 85": "https://www.pik.ru/search/ba85?rooms=2,3&floorFrom=4&floorTo=24&status=free&sortBy=price&orderBy=asc",
    "Большая Академическая 85 55+": "https://www.pik.ru/search/ba85?rooms=2,3&areaFrom=55&floorFrom=4&floorTo=24&status=free&sortBy=price&orderBy=asc",
    "Holland Park": "https://www.pik.ru/search/hp?rooms=2,3&floorFrom=4&floorTo=24&status=free&sortBy=price&orderBy=asc",
    "Holland Park 55+": "https://www.pik.ru/search/hp?rooms=2,3&areaFrom=55&floorFrom=4&floorTo=24&status=free&sortBy=price&orderBy=asc",
}

# URLs for A101Spider
A101_START_URLS = {
    "Дом на Зорге":"https://a101.ru/kvartiry/?order=actual_price&floor_max=16&floor_min=4&room=2,3,-2&project=dom-na-zorge",
    "Дом на Зорге 55+":"https://a101.ru/kvartiry/?order=actual_price&area_max=87.3&area_min=55&floor_max=16&floor_min=4&room=2,3,-2&project=dom-na-zorge"
}

# URLs for DonstroySpider
DONSTROY_START_URLS = {
    "Символ":"https://donstroy.moscow/full-search/?price%5B%5D=15.8&price%5B%5D=725.2&area%5B%5D=25&area%5B%5D=472&floor_number%5B%5D=4&floor_number%5B%5D=50&rooms%5B%5D=2&rooms%5B%5D=3&rooms%5B%5D=4&rooms%5B%5D=5&projects%5B%5D=10&floor_first_last=false&discount=false&furnish=false&apartments=false&secondary=false&sort=price-asc&view_type=flats&page=1&view=card",
    "Символ 55+":"https://donstroy.moscow/full-search/?price%5B%5D=15.8&price%5B%5D=725.2&area%5B%5D=55&area%5B%5D=392&floor_number%5B%5D=4&floor_number%5B%5D=50&rooms%5B%5D=2&rooms%5B%5D=3&rooms%5B%5D=4&rooms%5B%5D=5&projects%5B%5D=10&floor_first_last=false&discount=false&furnish=false&apartments=false&secondary=false&sort=price-asc&view_type=flats&page=1&view=card"
}

LEVEL_START_URLS = {
    "Селигерская": "https://level.ru/filter/?rooms=2,3,4&floor_min=4&floor_max=30&project=selig&ordering=price,pk,mode&cardType=vertical",
    "Селигерская 55+": "https://level.ru/filter?rooms=2,3,4&area_min=55&area_max=67&floor_min=4&floor_max=30&project=selig&ordering=price,pk,mode&cardType=vertical",
    "Войковская": "https://level.ru/filter?rooms=2,3&floor_min=4&floor_max=24&project=vojkov&ordering=price,pk,mode&cardType=vertical",
    "Войковская 55+": "https://level.ru/filter?rooms=2,3&area_min=55&floor_min=4&floor_max=24&project=vojkov&ordering=price,pk,mode&cardType=vertical"
}

# You can add more URL configurations for other spiders here
# EXAMPLE_SPIDER_URLS = [
#     "https://example.com/page1",
#     "https://example.com/page2",
# ]

