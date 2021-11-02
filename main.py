import random
import csv

import aiohttp
import asyncio

from config import config

data_moscow = []
data_spb = []


async def download(cl: aiohttp.ClientSession, region: str, start: bool, offset: int = 0):
    await asyncio.sleep(random.uniform(10, 15))
    print(
        f"Downloading json from {config['url'].format(region, offset if start else config['meta']['length'] - offset)}....")
    try:
        res = await cl.get(url=config['url'].format(
            region, offset if start else config['meta']['length'] - offset), headers=config['headers']
        )
        print(f"Downloaded! Status: {res.status}")
        json_res = await res.json()
        for i in json_res['items']:
            item = {
                'id': i.get('id'),
                'title': ("".join(list(map(lambda x: x + " ", i.get('title').split(' ')[:-1]))))[:-1],
                'url': i.get('link').get('web_url'),
                'region': 'Moscow' if region == 'RU-MOW' else 'Saint Petersburg',
            }
            if i.get('promo'):
                item['promo_price'] = str(i.get('price').get('price')) + str(i.get('price').get('currency'))
                item['price'] = str(i.get('old_price').get('price')) + str(i.get('old_price').get('currency'))
            else:
                item['price'] = str(i.get('price').get('price')) + str(i.get('price').get('currency'))
                item['promo_price'] = ''

            if region == 'RU-MOW':
                data_moscow.append(item)
            else:
                data_spb.append(item)

        if (start and offset + config['meta']['limit'] > config['meta']['length'] / 2) or \
                (not start and config['meta']['length'] - offset < config['meta']['length'] / 2):
            return

        await download(cl=cl,
                       offset=((offset + config['meta']['limit'])
                               if offset < config['meta']['length'] / 2
                               else config['meta']['length'] - offset - config['meta']['limit']),
                       region=region, start=start)

    except Exception as e:
        print('Connecting error: ', e)
        return


async def download_meta(cl: aiohttp.ClientSession):
    print(f"Downloading meta from: {config['meta_url']}")

    try:
        res = await cl.get(url=config['meta_url'], headers=config['headers'])
        print(f"Downloaded! Status: {res.status}")
        json_res = await (res.json())
        meta = {'limit': json_res['meta']['limit'],
                'length': json_res['meta']['length'],
                'title': json_res['meta']['title']}

        config['meta'] = meta
        print(config['meta'])
    except Exception as e:
        print('Connecting error: ', e)
        return


async def download_data():
    async with aiohttp.ClientSession() as client:
        await download_meta(cl=client)
        await asyncio.gather(
            download(cl=client, region=config['regions'][0], start=True),
            download(cl=client, region=config['regions'][0], start=False),
            download(cl=client, region=config['regions'][1], start=True),
            download(cl=client, region=config['regions'][1], start=False)
        )


def handle_data():
    output_data = list({v['id']: v for v in data_moscow}.values())
    output_data += list({v['id']: v for v in data_spb}.values())
    with open(f'detmir_{config["meta"]["title"]}_items.csv', 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['id', 'title', 'price', 'promo_price', 'url', 'region']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in output_data:
            writer.writerow(row)

    print("Data has been written to \'detmir_items.csv\'")


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(download_data())

handle_data()
