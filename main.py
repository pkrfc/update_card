import requests as requests

NM_ID = 116560924
WIDTH = 11 #Ширина
HEIGHT = 4 #Высота
LONG = 19 #Длинна

WB_TOKEN = 'primer_token'
HEADERS = {
    'Authorization': f'Bearer {WB_TOKEN}',
    'Content-Type': 'application/json',
}

GET_CARD = 'https://suppliers-api.wildberries.ru/content/v1/cards/cursor/list'

CET_CARD_FILTER = 'https://suppliers-api.wildberries.ru/content/v1/cards/filter'

UPDATE_CARD = 'https://suppliers-api.wildberries.ru/content/v1/cards/update'


def get_card():
    data = {
        "sort": {
            "filter": {
                "textSearch": str(NM_ID),
                "withPhoto": -1
            }
        }
    }
    card_info_response = requests.post(GET_CARD, headers=HEADERS, json=data)
    match card_info_response.status_code:
        case 200:
            card = card_info_response.json()
        case _:
            return 'Не нашёл карточку'
    try:
        vendor_code = card.get('data').get('cards')[0].get('vendorCode')
    except IndexError:
        return []
    except AttributeError:
        return []
    return vendor_code


def update_card(vendore_code):
    data = {
        "vendorCodes":
            [vendore_code]
    }
    card_filter_response = requests.post(CET_CARD_FILTER, headers=HEADERS, json=data)
    match card_filter_response.status_code:
        case 200:
            card_filter = card_filter_response.json()
        case _:
            return 'Не нашёл карточку'
    card_list = card_filter.get('data')
    for card in card_list:
        if card.get("nmID") == NM_ID:
            new_card = card
    characteristics = new_card['characteristics']
    new_characteristics = []
    for item in characteristics:
        if not item.get('Ширина упаковки') or item.get('Высота упаковки') or item.get('Длина упаковки'):
            new_characteristics.append(item)

    new_characteristics.append({'Ширина упаковки': WIDTH})
    new_characteristics.append({'Высота упаковки': HEIGHT})
    new_characteristics.append({'Длина упаковки': LONG})
    new_card['characteristics'] = new_characteristics
    new_card = [new_card, ]
    card_update = requests.post(UPDATE_CARD, headers=HEADERS, json=new_card)
    match card_update.status_code:
        case 200:
            return card_update.json()
        case _:
            return 'Не обновил'


if __name__ == '__main__':
    vendor_code = get_card()
    print(update_card(vendor_code))
