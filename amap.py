import requests
import json

KEY = 'bb0db1700b2084cf0e94c0525afb5b05'
CITY = '南京'
BASE_URL = 'http://restapi.amap.com/v3/'


def loc(address):
    url = BASE_URL + 'geocode/geo'
    params = {'city': CITY, 'address': address, 'key': KEY}
    j = json.loads(requests.get(url, params).content)
    if j['status'] == '1' and j['geocodes']:
        r = j['geocodes'][0]
        result = dict()
        result['loc'] = r['location']
        result['lng'], result['lat'] = r['location'].split(',')
        return result
    else:
        return j['info']


def draw(path, **kargs):
    url = BASE_URL + 'staticmap'
    params = {'scale': 2}
    for each in kargs:
        params[each] = kargs[each]
    if 'markers' in kargs:
        params['markers'] = 'small,,:'
        for each in kargs['markers']:
            print(f'>>> 正在查找【{each}】的位置...')
            try:
                params['markers'] += f"{loc(each)['loc']};"
            except:
                print(f'>>> 未能在地图上标出【{each}】')
        params['markers'] = params['markers'][:-1]
    if 'labels' in kargs:
        params['labels'] = ''
        for each in kargs['labels']:
            print(f'>>> 正在查找【{each}】的位置...')
            try:
                params['labels'] += f"{each},0,0,14,0xFFFFFF,0xFF0000:{loc(each)['loc']}|"
            except:
                print(f'>>> 未能在地图上标出【{each}】')
        params['labels'] = params['labels'][:-1]
    params['key'] = KEY
    image = requests.get(url, params).content
    with open(path, 'wb') as f:
        f.write(image)
    print(f">>> 已保存，文件地址：{path}")
