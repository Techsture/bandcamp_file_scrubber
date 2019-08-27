#!/usr/bin/env python3

import argparse
import json
from mp3_tagger import MP3File, VERSION_1, VERSION_2, VERSION_BOTH


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('path', help='System path to file.')
  args = parser.parse_args()
  path = args.path
  # Create MP3File instance.
  mp3 = MP3File(path)
  tags = mp3.get_tags()
  print(json.dumps(tags, indent=2, default=str))
  exit()


if __name__ == '__main__':
  main()
