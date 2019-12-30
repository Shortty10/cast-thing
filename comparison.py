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


def compare(movies, cache):
    """
    Uses a list of movie IDs and the cache to find common actors.
    """

    # Create a list of actors
    casts = []
    for movie in cache['movies']:
        for mov in movies:
            try:
                cast = movie[mov]['cast']
                movie_name = movie[mov]['name']
                for member in cast:
                    member['movie'] = movie_name
                    casts.append(member)
            except KeyError:
                pass

    # The IDs of all actors
    ids = [member['id'] for member in casts]
    # A list of duplicates in the 'ids' list
    duplicates = [x for x in ids if ids.count(x) != 1]

    # Return if duplicates is empty
    if not duplicates:
        print('\n\n\nNo matches found.')
        return

    # Remove duplicates from the 'duplicates' list
    res = []
    for i in duplicates:
        if i not in res:
            res.append(i)

    # Find information for remaining duplicate actors, and print it
    print('\n')
    for i in res:
        print('\n')
        printed_name = False
        for member in casts:
            if member['id'] == i:
                name = member['name']
                movie = member['movie']
                role = member['role']
                if not printed_name:
                    print(f'{name}:')
                printed_name = True
                print(f'\t{movie}:')
                print(f'\t\t{role}\n')
