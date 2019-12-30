from scraper import scraper
from comparison import compare
import json

CACHE_DIR = 'cache/cache.json'
TITLES_DIR = 'titles.txt'


def main():
    # Read data from titles.txt
    with open(TITLES_DIR, 'r') as file:
        data = file.read()
        movies = data.split('\n')

    # Remove lines prefixed with * and blank lines
    movies = [mov for mov in movies if not '*' in mov and mov.strip() != '']

    try:
        # Load the cache
        with open(CACHE_DIR, 'r') as file:
            cache = json.load(file)
    except (json.decoder.JSONDecodeError, FileNotFoundError) as error:
        if isinstance(error, json.decoder.JSONDecodeError):
            print("Cache corrupted. Rebuilding...")
        if isinstance(error, FileNotFoundError):
            print("Creating cache...")
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
            print(f'{name} found in cache.')
            continue

        # Find cast for uncached movies
        cast = scraper(movie)
        cache['movies'].append(cast)

        # Push changes to cache
        with open(CACHE_DIR, 'w') as f:
            json.dump(cache, f)

    # Find common actors in movies
    compare(movies)


if __name__ == '__main__':
    main()
    input('Enter any key to exit: ')
