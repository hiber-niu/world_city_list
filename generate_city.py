#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: generate_city.py
Author: hiber
Email: niuhaibo@xiaomi.com
Github: https://github.com/hiber-niu
Description:
"""

import json
import copy
import xmltodict


EN_NAMES = {}

def build_names():
    """build (type_code, name) key-value pairs.
    :returns: TODO

    """
    with open("data/city_en.xml") as xmlf:
        xml = ''.join(xmlf.readlines())
    results = eval(json.dumps(xmltodict.parse(xml)))

    global EN_NAMES
    for country in results['Location']['CountryRegion']:
        EN_NAMES['国家_'+country['@Code']] = country['@Name']
        states = country.get('State', None)
        if states:
            if isinstance(states, dict):
                states = [states]

            for state in states:
                if '@Code' in state:
                    EN_NAMES['省/州_'+country['@Code']+'_'+state['@Code']] = state['@Name']
                cities = state.get('City', None)
                if cities:
                    if isinstance(cities, dict):
                        cities = [cities]
                    for city in cities:
                        if '@Code' in state:
                            prefix = '城市_'+country['@Code']+'_'+state['@Code']+'_'+city['@Code']
                        else:
                            prefix = '城市_'+country['@Code']+'_'+city['@Code']
                        EN_NAMES[prefix] = city['@Name']


def add_en_name():
    """获取输入城市的英文名，并写入json文件。
    """
    with open('data/place.json', 'r', encoding='utf-8') as jfile:
        places = json.load(jfile)

    added_places = copy.deepcopy(places)
    for index, place in enumerate(places):
        key = place['category']+'_'+place['code']
        added_places[index]['en_name'] = EN_NAMES.get(key, "")
        print("{} with english name {} added!".format(key, added_places[index]['en_name']))

    with open("result/new_places.json", 'w', encoding='utf-8') as outfile:
        json.dump(added_places, outfile)
        print('Write places to new_places.json done!')


if __name__ == "__main__":
    build_names()
    add_en_name()
