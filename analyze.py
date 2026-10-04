import json
with open('D:/ZySpace/zy_code/seo/codexlimit/audit_result.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
for lang, p in data['pages'].items():
    print('='*50)
    print(f'LANG: {lang}')
    print(f'Title ({p[ title_len]}) : {p[title]}')
    print(f'Desc  ({p[description_len]}) : {p[description]}')
    print(f'Canonical : {p[canonical]}')
    print(f'H1 Count  : {p[h1_count]}, {p[h1_texts]}')
    print(f'Hreflang  : {p[hreflangs]}')
    print(f'Ext JS    : {p[external_scripts]}')
    print(f'Ext CSS   : {p[external_styles]}')
    print(f'JSON-LDs  : {len(p[json_lds])}')
    for idx, j in enumerate(p[json_lds]):
        if j['valid'] and isinstance(j['data'], dict):
            print(f'  LD[{idx}]: {j[data].get(@type)} - {j[data].get(name, ")[:30]}')
print('='*50)
print('ROBOTS.TXT:')
print(data['robots'].get('raw', ''))
print('='*50)
print('SITEMAP.XML:')
print(data['sitemap'].get('raw', ''))
