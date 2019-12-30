"""
MIT License

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

import json
from scraper import scrape
from comparison import compare

# The cache and titles files.
CACHE_DIR = 'cache/cache.json'
TITLES_DIR = 'titles.txt'


def main():
    # Read data from titles.txt
    with open(TITLES_DIR, 'r') as file:
        data = file.read()
        # Each newline is a new movie
        movies = data.split('\n')
        # Split before the slash
        movies = [x.split(' /')[0] for x in movies]

    # Remove lines prefixed with * and blank lines
    movies = [mov for mov in movies if not '*' in mov and mov.strip() != '']

    try:
        # Load the cache
        with open(CACHE_DIR, 'r') as file:
            cache = json.load(file)
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        # Create cache if it doesn't exist
        with open(CACHE_DIR, 'w'):
            pass
        cache = {'movies': []}

    for movie in movies:
        # Skip cached movies
        cached_movies = []

        for keys in [x.keys() for x in cache['movies']]:
            for key in keys:
                cached_movies.append(key)

        if movie in cached_movies:
            for mov in cache['movies']:
                try:
                    name = mov[movie]['name']
                    break
                except KeyError:
                    continue
                name = movie
            print(f'Cast found for {name}')
            continue

        # Find cast for uncached movies
        cast = scrape(movie)
        if cast:
            cache['movies'].append(cast)

            # Push changes to cache
            with open(CACHE_DIR, 'w') as file:
                json.dump(cache, file)

    # Find common actors in movies
    compare(movies, cache)


if __name__ == '__main__':
    main()
    input('')
