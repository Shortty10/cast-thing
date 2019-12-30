# cast-thing
Find common actors in a list of movies.

![Sample Output](/images/example.jpg)

## Requirements
 - Python 3.6 or higher

## Installation
```sh
$ git clone https://github.com/Shortty10/cast-thing.git
$ cd cast-thing
$ pip install -r requirements.txt
```

### Open titles.txt
- Find the IMDB ID for each movie you want to include. This can be found in the URL of the IMDB link.
- For example, American Sniper's IMDB URL is https://www.imdb.com/title/tt2179136/, meaning the ID is  tt2179136.
- Add each ID into titles.txt.
- To exclude an ID from the next run, add an asterisk before the ID (as shown below)
- To add a comment after an ID, (to note the name of the movie, etc.) add a slash after the ID and type your comment.

![Sample titles.txt file](/images/titles.jpg)

- Finally, run main.py