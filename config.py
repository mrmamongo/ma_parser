config = {
    "headers": {
        'content-type': 'application/json; charset=utf-8',
        'accept-language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
    },
    'regions': ['RU-MOW', 'RU-SPE'],
    'meta_url': 'https://api.detmir.ru/v2/products?filter=categories[].alias:lego;promo:false;withregion:RU-MOW&expand=meta.facet.ages.adults,meta.facet.gender.adults&meta=*',
    'url': "https://api.detmir.ru/v2/products?filter=categories[].alias:lego;promo:false;withregion:{0}&expand=meta.facet.ages.adults,meta.facet.gender.adults&meta=*&limit=30&offset={1}&sort=popularity:desc"
}
