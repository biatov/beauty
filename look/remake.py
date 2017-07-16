import json


def read(lang):
    try:
        with open('%s.json' % lang) as f:
            items = json.load(f)
    except FileNotFoundError:
        items = list()
    return items


def create(filename):
    en_list = list(read('en'))
    ch_list = list(read('ch'))

    ii = list()

    for each_en in en_list:
        try:
            i = list(map(lambda el: el['product_url'].split('/')[3], ch_list)).index(each_en['product_url'].split('/')[3])
            ii.append(i)
        except:
            pass

    new_ch_list = list()
    for i in en_list:
        new_ch_list.append(ch_list[i])

    with open(filename, 'w') as outfile:
        json.dump(new_ch_list, outfile)
