
import re
import requests
import json

url = 'https://moscow.flamp.ru/firm/shokoladnica_set_kofeen-4504127908427082'  # url для второй страницы
r = requests.get(url)

headers = {

    'user-agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"

}

r = requests.get(url, headers=headers)

with open('flamp.html', 'w') as output_file:
    output_file.write(r.text)

clean_text = r.text.replace('\r', ' ').replace('\n', ' ').replace('\t', ' ')
reviews = re.findall(r"<li class=\"ugc-list__item js-ugc-list-item\">(?P<date>.+?)</cat-entities-ugc-item>\s*</li>",
                     clean_text)
#print(r.status_code)
shokoladnica_data = {}
shokoladnica_data['review_data'] = []

for review in reviews:
    date_published = re.findall(r"<meta itemprop=\"datePublished\" content=\"(?P<date>.+?)\"/>", review)
    rating_value = re.findall(r"<meta itemprop=\"ratingValue\" content=\"(?P<rating>.+?)\"/>", review)
    user_id = re.findall(r"link\sitemprop=\"url\"\shref=\"//flamp.ru/(?P<id>.+?)\"", review)
    user_review = re.findall(r"itemprop=\"reviewBody\"\s+>\s+<p class=\"t-rich-text__p\">\s+(?P<reviewBody>.+?)\s+</p>",
                             review)

    shokoladnica_data['review_data'].append({
        'user_id': ''.join(user_id),
        'date_published': ''.join(date_published),
        'rating_value': ''.join(rating_value),
        'user_review': ''.join(user_review)
    })

with open('shokoladnica_data.txt', 'w') as outfile:
    json.dump(shokoladnica_data, outfile)

with open('shokoladnica_data.txt') as json_file:
    shokoladnica_data = json.load(json_file)
    for review_data in shokoladnica_data['review_data']:
        print('user_id: ' + review_data['user_id'])
        print('date_published: ' + review_data['date_published'])
        print('rating_value: ' + review_data['rating_value'])
        print('user_review: ' + review_data['user_review'])
        print()

