##############################################################################
# Author: Orion Crocker
# Filename: main.py
# Date: 01/13/20
# 
# Spotify Collage Creator
#   Automatically downloads all album art from Spotify playlist and assembles a
#     collage
################################################################################

import argparse
from . import images, collage

def main():

  parse = argparse.ArgumentParser(description='Spotify image gatherer and creator of collages')
  #parse.add_argument('-p', '--playlist', dest='playlist', type=str, help='Get all album art from a specific playlist')
  #parse.add_argument('-a', '--artist', dest='artist', type=str, help='Get album art from an artist, by default it grabs first 10')
  parse.add_argument('url', type=str, help='Spotify artist or playlist to be parsed')
  parse.add_argument('-d', '--directory', type=str, help='Specify the a target directory to output results')
  parse.add_argument('-c', '--collage', action='count', default=0, help='Create a collage out of images gathered from "playlist" or "artist" argument.')
  parse.add_argument('-v', '--verbose', action='count', default=0, help='See the program working instead of just believing that it is working')
  parse.add_argument('-z', '--zip', action='count', default=0, help='Output the directory into a zip file')

  args = parse.parse_args()
  if args.url is None:
    print('A Spotify URL is required.')
    exit(1)
  
  stored_images=images.get_images(args.url, directory=args.directory, verbose=args.verbose, zip_this=args.zip)

  if args.collage:
    collage.make_collage(directory=stored_images, verbose=args.verbose)


if __name__ == '__main__':
  main()

