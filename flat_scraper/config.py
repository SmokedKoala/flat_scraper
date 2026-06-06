# URL Configuration for Scrapy Spiders
# Add or modify URLs here to control which pages the spider will scrape

# URLs for PikHtmlSpider — используем api.pik.ru (block_id = числовой ID комплекса)
PIK_START_URLS = {
    "Саларьево парк":           "https://api.pik.ru/v2/flat?block_id=118&rooms=2,3&floor_from=4&floor_to=17&status=free&sortBy=price&orderBy=asc",
    "Саларьево парк 55+":       "https://api.pik.ru/v2/flat?block_id=118&rooms=2,3&floor_from=4&floor_to=17&area_from=55&status=free&sortBy=price&orderBy=asc",
    "Кронштадтский 9":          "https://api.pik.ru/v2/flat?block_id=518&rooms=2,3&floor_from=4&floor_to=32&status=free&sortBy=price&orderBy=asc",
    "Кронштадтский 9 55+":      "https://api.pik.ru/v2/flat?block_id=518&rooms=2,3&floor_from=4&floor_to=32&area_from=55&status=free&sortBy=price&orderBy=asc",
    "Нарвин":                   "https://api.pik.ru/v2/flat?block_id=1165&rooms=2,3&floor_from=4&status=free&sortBy=price&orderBy=asc",
    "Нарвин 55+":               "https://api.pik.ru/v2/flat?block_id=1165&rooms=2,3&floor_from=4&area_from=55&status=free&sortBy=price&orderBy=asc",
    "Большая Академическая 85": "https://api.pik.ru/v2/flat?block_id=1372&rooms=2,3&floor_from=4&floor_to=24&status=free&sortBy=price&orderBy=asc",
    "Большая Академическая 85 55+": "https://api.pik.ru/v2/flat?block_id=1372&rooms=2,3&floor_from=4&floor_to=24&area_from=55&status=free&sortBy=price&orderBy=asc",
    "Holland Park":             "https://api.pik.ru/v2/flat?block_id=320&rooms=2,3&floor_from=4&floor_to=24&status=free&sortBy=price&orderBy=asc",
    "Holland Park 55+":         "https://api.pik.ru/v2/flat?block_id=320&rooms=2,3&floor_from=4&floor_to=24&area_from=55&status=free&sortBy=price&orderBy=asc",
}

# URLs for A101Spider
A101_START_URLS = {
    "Дом на Зорге":"https://a101.ru/kvartiry/?order=actual_price&floor_max=16&floor_min=4&room=2,3,-2&project=dom-na-zorge",
    "Дом на Зорге 55+":"https://a101.ru/kvartiry/?order=actual_price&area_max=87.3&area_min=55&floor_max=16&floor_min=4&room=2,3,-2&project=dom-na-zorge"
}

# Криво работает
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

# Нельзя распарсить, карточки подгружаются JS
LSR_START_URLS = {
    "Дмитровское небо": "https://www.lsr.ru/msk/kvartiry-v-novostroikah/?type%5B8%5D=8&type%5B9%5D=9&price%5Bmin%5D=&price%5Bmax%5D=&price_range%5Bmin%5D=18.1&price_range%5Bmax%5D=32.2&last_delivery=30&obj%5B%5D=207&area%5Bmin%5D=&area%5Bmax%5D=&area_range%5Bmin%5D=54&area_range%5Bmax%5D=81&floor%5Bmin%5D=&floor%5Bmax%5D=&floor_range%5Bmin%5D=2&floor_range%5Bmax%5D=32&floor%5Bnfirst%5D=1&__s=",
    "Дмитровское небо 55+": "https://www.lsr.ru/msk/kvartiry-v-novostroikah/?type%5B8%5D=8&type%5B9%5D=9&obj%5B%5D=207&area%5Bmin%5D=55.00&floor%5Bnfirst%5D=1"
}

GRANELLE_START_URLS = {
    "Тринити": "https://granelle.ru/flats/?project=tri&order=price&is_released=0&rooms=3-euro,4-euro&floor_number_min=4&floor_number_max=32&view=grid",
    "Тринити 55+": "https://granelle.ru/flats/?project=tri&order=price&is_released=0&rooms=3-euro,4-euro&area_max=104&area_min=55&floor_number_min=4&floor_number_max=32&view=grid"
}

# 401 ошибка
SAMOLET_START_URLS = {
    "Sky Sputnik": "https://samolet.ru/flats/?nameType=s&free=1&type=100000000&ordering=-order_manual,filter_price_package,pk&rooms=2,3&floor_min=4&floor_max=26&place=true&place_project=7",
    "Sky Sputnik 55+": "https://samolet.ru/flats/?nameType=s&free=1&type=100000000&ordering=-order_manual,filter_price_package,pk&rooms=2,3&floor_min=4&floor_max=26&place=1&place_project=7&area_min=55&area_max=89.8"
}

RG_START_URLS = {
    "Михайловский": "https://rg-dev.ru/flats/?ordering=actual_price&status=1&complex=b0dbb09f-3c7b-eb11-8118-00155df44d2f&rooms=2,3,4&floor_min=4&floor_max=20",
    "Михайловский 55+": "https://rg-dev.ru/flats/?ordering=actual_price&status=1&complex=b0dbb09f-3c7b-eb11-8118-00155df44d2f&rooms=2,3,4&square_min=55&square_max=94&floor_min=4&floor_max=20",
    "Петровский парк 2": "https://rg-dev.ru/flats/?ordering=actual_price&status=1&complex=fb403bc2-e5e0-ec11-8120-00155d1f3d3d&rooms=2,3",
    "Петровский парк 2 55+": "https://rg-dev.ru/flats/?ordering=actual_price&status=1&complex=fb403bc2-e5e0-ec11-8120-00155d1f3d3d&rooms=2,3&square_min=55"
}

TALAN_START_URLS = {
    "Инджой": "https://talan.ru/msk/apartments/flats?complex=2322413&floor_range=%7B%22min%22%3A%224%22%2C%22max%22%3A%22%22%7D&not_last=true&rooms=2%2B&rooms=3&rooms=3%2B&rooms=4&rooms=2",
    "Инджой 55+": "https://talan.ru/msk/apartments/flats?complex=2322413&area_range=%7B%22min%22%3A%2255%22%2C%22max%22%3A%22%22%7D&floor_range=%7B%22min%22%3A%224%22%2C%22max%22%3A%22%22%7D&not_last=true&rooms=2%2B&rooms=3&rooms=3%2B&rooms=4&rooms=2",
}

# You can add more URL configurations for other spiders here
# EXAMPLE_SPIDER_URLS = [
#     "https://example.com/page1",
#     "https://example.com/page2",
# ]

