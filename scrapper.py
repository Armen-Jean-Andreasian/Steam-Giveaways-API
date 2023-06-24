import requests
from bs4 import BeautifulSoup


def steam():
    url = 'https://store.steampowered.com/search/?sort_by=Price_ASC&ignore_preferences=1&specials=1&hidef2p=1' \
          '&maxprice=free&supportedlang=english'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    games = []


    for row in soup.select('#search_resultsRows > a'):
        content = {}

        game_title = row.select_one('.title').get_text(strip=True)
        game_url = row['href']

        server_image_url = row.select_one('.search_capsule img')['src']
        # https://cdn.akamai.steamstatic.com/steam/apps/1180660/capsule_sm_120.jpg?t=1685640127

        server_app_image_repo = server_image_url[:54]
        game_image_url = server_app_image_repo + "header.jpg"
        # result : https://cdn.akamai.steamstatic.com/steam/apps/1238430/header.jpg

        content['game_title'] = game_title
        content['game_url'] = game_url
        content["game_image_url"] = game_image_url

        games.append(content)
    return games


if __name__ == '__main__':
    print(steam())
