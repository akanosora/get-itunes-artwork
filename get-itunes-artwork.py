#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
import urllib, urllib2
import json

SAVE_TO = "%s/Desktop/" % os.path.expanduser("~") # Directory must exist
TITLES = [] # Optionally populate this with a list of titles for batch processing

MOVIE = {
    'title_prompt': "Search for a movie (or type '--help' or '-h' to see more options): ",
    'entity': 'movie',
    'name_node': 'trackName'
}
TV = {
    'title_prompt': "Search for a TV show (or type '--help' or '-h' to see more options): ",
    'entity': 'tvShow',
    'name_node': 'collectionName'
}
ALBUM = {
    'title_prompt': "Search for an album (or type '--help' or '-h' to see more options): ",
    'entity': 'album',
    'name_node': 'collectionName'
}

media = MOVIE.copy()
media.update({'country': 'US'})

def get_art(title=None, keep_going=False, unique_filenames=True):
    global not_found, media
    if not title:
        title = raw_input(media['title_prompt'])
        if title == '':
            get_art(None, True, False)
        elif title in ('--movie', '-m'):
            media.update(MOVIE)
            get_art(None, True, False)
        elif title in ('--tv-show', '-t'):
            media.update(TV)
            get_art(None, True, False)
        elif title in ('--album', '-a'):
            media.update(ALBUM)
            get_art(None, True, False)
        elif title in ('--country', '-c'):
            media.update({'country': raw_input('Type two-letter country code for the store you want to search: ')})
            get_art(None, True, False)
        elif title in ('--help', '-h'):
            print "\n" + \
                    "Type '--movie' or '-m' to switch to searching for movies\n" + \
                    "Type '--tv-show' or '-t' to switch to searching for TV shows\n" + \
                    "Type '--album' or '-a' to switch to searching for albums\n" + \
                    "Type '--country' or '-c' to change country (The default is US)\n" + \
                    "Type '--quit' or '-q' to exit the program\n"
            get_art(None, True, False)
        elif title in ('--quit', '-q'):
            exit();
    
    print "\nSearching for \"%s\"..." % title
    
    search_term = urllib.quote_plus(title)

    try:
        response = urllib2.urlopen("https://itunes.apple.com/search?entity=%s&country=%s&term=%s" % (media['entity'], media['country'].upper(), search_term))
        results = json.load(response)
        resultCount = results['resultCount']
        if resultCount > 0:
            if resultCount == 1:
                which = 0
            else:
                for index, result in enumerate(results['results']):
                    print "%s. %s" % (index+1, result[media['name_node']].encode("utf-8"))
                which = raw_input("\nEnter a number to download its artwork (or hit Enter to search again): ")
                try:
                    which = int(which) - 1
                except:
                    which = None
                    not_found.append(title)
            if which != None:
                url = results['results'][which]['artworkUrl100'].replace("100x100bb.jpg", "1200x1200bb.png")
                sys.stdout.write("Downloading artwork...")
                if unique_filenames:
                    urllib.urlretrieve(url, "%s/%s.png" % (SAVE_TO, title.replace("/", "-").replace(":", "_")))
                else:
                    urllib.urlretrieve(url, "%s/Poster.png" % SAVE_TO)
                sys.stdout.write(" done.\n\n")
            
        else:
            print "No results found for \"%s\"" % title
            not_found.append(title)
    except urllib2.HTTPError:
        not_found.append(title)
        pass
    
    if keep_going:
        get_art(None, True, unique_filenames)

if __name__ == "__main__":
    not_found = []
    if TITLES:
        for title in TITLES:
            get_art(title)
    else:
        get_art(None, True, False)
    print "\n\nArtwork was not found for the following titles:"
    for title in not_found:
        print title
