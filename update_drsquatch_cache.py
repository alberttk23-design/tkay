import json

path = 'out/spy_cache/drsquatch.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

data['name'] = 'Dr. Squatch'
data['avatarUrl'] = '/static/avatars/drsquatch.png'
data['total_active_ads'] = 1144
data['total_all_time'] = '22K'
data['reach_toggle'] = 'Reach & Spend · EU/UK only 98 (9%)'
data['channels']['meta']['active'] = 1144
data['channels']['meta']['total'] = 22000

cards_meta = [
    {'days': 119, 'start': 'Jun 3', 'copies': 5, 'targeting': 'none', 'delta': '=', 'cta': 'Get Offer', 'domain': 'www.drsquatch.com', 'title': 'www.drsquatch.com'},
    {'days': 116, 'start': 'Jun 6', 'copies': 11, 'targeting': 'none', 'delta': '=', 'cta': 'Get Offer', 'domain': 'www.drsquatch.com', 'title': 'www.drsquatch.com'},
    {'days': 38, 'start': 'Aug 23', 'copies': 3, 'targeting': 'global', 'delta': '=', 'cta': 'Get Offer', 'domain': 'www.drsquatch.com', 'title': 'www.drsquatch.com'},
    {'days': 82, 'start': 'Jul 10', 'copies': 2, 'targeting': 'global', 'delta': '=', 'cta': 'Get Offer', 'domain': 'WWW.DRSQUATCH....', 'title': '🚨 ALMOST SOLD ...'},
    {'days': 37, 'start': 'Aug 24', 'copies': 4, 'targeting': 'none', 'delta': '↘', 'cta': 'Get Offer', 'domain': 'www.drsquatch.com', 'title': 'www.drsquatch.com'},
    {'days': 41, 'start': 'Aug 20', 'copies': 3, 'targeting': 'global', 'delta': '↘', 'cta': 'Get Offer', 'domain': 'WWW.DRSQUATCH....', 'title': '🧼 FREE SHOWER ...'},
    {'days': 110, 'start': 'Jun 12', 'copies': 9, 'targeting': 'none', 'delta': '↘', 'cta': 'Get Offer', 'domain': 'www.drsquatch.com', 'title': 'www.drsquatch.com'},
    {'days': 53, 'start': 'Aug 8', 'copies': 3, 'targeting': 'global', 'delta': '=', 'cta': 'Get Offer', 'domain': 'www.drsquatch.com', 'title': 'www.drsquatch.com'},
    {'days': 147, 'start': 'May 8', 'copies': 7, 'targeting': 'none', 'delta': '=', 'cta': 'Get Offer', 'domain': 'www.drsquatch.com', 'title': 'www.drsquatch.com'},
    {'days': 44, 'start': 'Aug 17', 'copies': 1, 'targeting': 'eu', 'reach_badge': '111K · $999 · $22.7/d', 'country': '🇷🇴', 'delta': '=', 'cta': 'Get Offer', 'domain': 'www.drsquatch.com', 'title': 'www.drsquatch.com'},
    {'days': 129, 'start': 'May 24', 'copies': 3, 'targeting': 'none', 'delta': '↗', 'cta': 'Get Offer', 'domain': 'www.drsquatch.com', 'title': 'www.drsquatch.com'},
    {'days': 27, 'start': 'Sep 3', 'copies': 3, 'targeting': 'global', 'delta': '↗', 'pct': '2%', 'cta': 'Get Offer', 'domain': 'www.drsquatch.com', 'title': 'www.drsquatch.com'}
]

ads = data.get('ads', [])
for i, m in enumerate(cards_meta):
    if i < len(ads):
        ads[i]['days_active'] = m['days']
        ads[i]['daysRunning'] = m['days']
        ads[i]['startDate'] = m['start']
        ads[i]['date_range'] = f"{m['days']}d · {m['start']} → now"
        ads[i]['copies_count'] = m['copies']
        ads[i]['duplicates'] = m['copies']
        ads[i]['rank_delta'] = m['delta']
        ads[i]['rank_pill'] = f"{i+1}/1,144 ({m.get('pct', '1%')})"
        ads[i]['ctaText'] = m['cta']
        ads[i]['ctaDomain'] = m['domain']
        ads[i]['cta_title'] = m['title']
        ads[i]['advertiserAvatarUrl'] = '/static/avatars/drsquatch.png'
        ads[i]['advertiser'] = 'Dr. Squatch'
        ads[i]['advertiserName'] = 'Dr. Squatch'
        if m['targeting'] == 'global':
            ads[i]['globalAds'] = True
            ads[i]['isGlobal'] = True
            ads[i]['reach_spend_badge'] = None
            ads[i]['euReach'] = 0
        elif m['targeting'] == 'eu':
            ads[i]['globalAds'] = False
            ads[i]['isGlobal'] = False
            ads[i]['reach_spend_badge'] = m['reach_badge']
            ads[i]['countryCode'] = m['country']
            ads[i]['euReach'] = 111000
            ads[i]['euSpend'] = 999
            ads[i]['dailySpend'] = 22.7
        else:
            ads[i]['globalAds'] = False
            ads[i]['isGlobal'] = False
            ads[i]['reach_spend_badge'] = None
            ads[i]['euReach'] = 0

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('Updated drsquatch.json successfully!')
