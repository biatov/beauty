import json


def read(lang):
    try:
        with open(lang) as f:
            items = json.load(f)
    except FileNotFoundError:
        items = list()
    return items


def create(filename, english, chinese):
    en_list = list(read(english))
    ch_list = list(read(chinese))

    ii = list()

    for each_en in en_list:
        try:
            i = list(map(lambda el: el['product_url'].split('/')[3], ch_list)).index(each_en['product_url'].split('/')[3])
            ii.append(i)
        except:
            pass

    new_ch_list = list()
    for i in ii:
        new_ch_list.append(ch_list[i])

    with open(filename, 'w') as outfile:
        json.dump(new_ch_list, outfile)

create('look/remake_json/men_ch_items_remake.json',
       'look/json_en/men_items.json',
       'look/json_ch/men_ch_items.json')
