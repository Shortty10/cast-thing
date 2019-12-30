import requests
from bs4 import BeautifulSoup


class MovieNotFound(Exception):
    pass


def find_cast(cast):
    cast_list = []

    for member in cast:
        member_data = member.find_all('a')
        member_id = member_data[0]['href'].split('/name/')[1].split('/')[0]
        member_name = member_data[1].text.strip()
        member_role = member.find('td', class_='character').text.strip()
        if '(' in member_role and '\n' in member_role:
            member_role = member_role.split(' /')[0]
        member_role = ' '.join(member_role.split())

        member_dict = {
            'id': member_id,
            'name': member_name,
            'role': member_role
        }

        cast_list.append(member_dict)

    return cast_list


def scraper(movie):
    # The IMDB url
    url = f'https://www.imdb.com/title/{movie}/fullcredits'
    # Send a GET request
    request = requests.get(url).text
    # Generate a Soup object
    soup = BeautifulSoup(request, 'lxml')

    # Find name and year of movie
    meta = soup.find('h3', itemprop='name')
    try:
        movie_name = meta.find('a').text
    except AttributeError:
        raise MovieNotFound(f'{movie} was not found.')
    year = meta.find('span').text.strip()
    title = f'{movie_name} {year}'

    # Remove empty lines in cast list
    cast = soup.find('table', class_='cast_list').find_all('tr')
    for member in cast:
        try:
            member['class']
        except KeyError:
            cast.remove(member)

    # Find the cast
    cast_list = find_cast(cast)

    # Update the cache
    cast = {
        movie: {
            "name": title,
            "cast": cast_list
        }
    }

    print(f'Cast found for {title}')

    return cast
