"""MIT License

Copyright (c) 2019 Shortty10

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import requests
from bs4 import BeautifulSoup


def find_cast(cast):
    """
    Parse IMDB's cast database
    """
    cast_list = []

    for member in cast:
        member_data = member.find_all('a')
        try:
            member_id = member_data[0]['href'].split('/name/')[1].split('/')[0]
        except IndexError:
            continue
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


def scrape(movie):
    """
    Find cast members for an uncached movie
    """
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
        print(f'{movie} was not found. Skipping...')
        return
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
