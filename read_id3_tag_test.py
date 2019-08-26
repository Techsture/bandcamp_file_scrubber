#!/usr/bin/env python3

from mp3_tagger import MP3File, VERSION_1, VERSION_2, VERSION_BOTH

def main():
  # Create MP3File instance.
  mp3 = MP3File("/Users/michael/Desktop/New Music/Music For Sleep - The Edge.mp3")
  tags = mp3.get_tags()
  print(tags)
  exit()

if __name__ == '__main__':
  main()
