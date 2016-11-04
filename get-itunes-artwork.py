#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
import urllib, urllib2
import json

MOVIES = {
    'title_prompt': "Search for a movie title (or type '#help' to see more options): ",
    'entity': 'movie',
    'name_node': 'trackName'
}
TV = {
    'title_prompt': "Search for a TV show (or type '#help' to see more options): ",
    'entity':  'tvShow',
    'name_node': 'collectionName'
}

media = MOVIES.copy()
media.update({'country': 'US'})

SAVE_TO = "%s/Desktop/" % os.path.expanduser("~") # Directory must exist
TITLES = [] # Optionally populate this with a list of titles for batch processing

def get_art(title=None, keep_going=False):
    global not_found, media
    if not title:
        title = raw_input(media['title_prompt'])
        if title == '':
            get_art(None, True)
        if title == '#movie':
            media.update(MOVIES)
            get_art(None, True)
        elif title == '#tvshow':
            media.update(TV)
            get_art(None, True)
        elif title == '#country':
            media.update({'country': raw_input('Type two-letter country code for the store you want to search: ')})
            get_art(None, True)
        elif title == '#help':
            print "Type '#movie' to switch to searching for movie titles\nType '#tvshow' to switch to searching for TV shows\nType '#country' to change country (The default is US)\nType '#quit' to exit the program"
            get_art(None, True)
        elif title == '#quit':
            exit();
    
    print "\nSearching for \"%s\"..." % title
    
    search_term = urllib.quote_plus(title)

    try:
        results = json.load(response)
        resultCount = results['resultCount']
        if resultCount > 0:
            if resultCount == 1:
                which = 0
            else:
                for index, result in enumerate(results['results']):
                    print "%s. %s" % (index+1, result[media['name_node']])
                which = raw_input("\nEnter a number to download its artwork (or hit Enter to search again): ")
                try:
                    which = int(which) - 1
                except:
                    which = None
                    not_found.append(title)
            if which != None:
                url = results['results'][which]['artworkUrl100'].replace("100x100bb.jpg", "1200x1200bb.png")
                sys.stdout.write("Downloading artwork...") 
                urllib.urlretrieve(url, "%s/Poster.png" % SAVE_TO)
                sys.stdout.write(" done.\n\n")
            
        else:
            print "No results found for \"%s\"" % title
            not_found.append(title)
    except urllib2.HTTPError:
        not_found.append(title)
        pass
    
    if keep_going:
        get_art(None, True)

if __name__ == "__main__":
    not_found = []
    if TITLES:
        for title in TITLES:
            get_art(title)
    else:
        get_art(None, True)
    print "\n\nArtwork was not found for the following titles:"
    for title in not_found:
        print title
