#!/usr/bin/env python3

# This script requires the 'mp3-tagger' package.
# `pip install mp3-tagger`

import argparse
import json
from mp3_tagger import MP3File, VERSION_1, VERSION_2, VERSION_BOTH
import os
import re
import string


def correct_comment_tag(file):
  file.set_version(VERSION_2)
  # If there is no comment, add "N/A"
  if file.comment is None:
    file.comment = '\x00N/A'
    file.set_version(VERSION_BOTH)
    file.save()
    return
  else:
    comment = file.comment
    # Replace the 'eng' that MixedInKey puts at the beginning of the comment:
    comment = comment.replace('eng', '')
    # Replace "/" with a space:
    comment = comment.replace('/', ' ')
  file.comment = '\x00' + comment
  file.set_version(VERSION_BOTH)
  file.save()
  return


def get_file_list(directory):
  file_list = []
  for file in os.listdir(directory):
    if file.endswith(".mp3"):
      file_list.append(file)  
  return file_list


def get_info_from_filename(file):
  filename = re.split('\ -\ |\.', file)
  artist = filename[0]
  song = filename[1]
  return artist, song


def delete_unnecessary_tags(file, correct_key_comment):
  file.set_version(VERSION_1)
  del file.song
  del file.artist
  del file.album
  del file.year
  del file.comment
  del file.track
  del file.genre
  file.set_version(VERSION_2)
  # Delete the comment if the script wasn't run with the --correct_key_comment switch:
  if not correct_key_comment:
    file.comment = ''
  file.band = ''
  file.track = ''
  file.set_version(VERSION_BOTH)
  file.save()
  return


def rename_file(file, directory):
  # Break the filename into its different parts.
  current_filename = re.split('\ -\ |\.', file)
  artist = current_filename[0]
  album = current_filename[1]
  song = current_filename[2]
  extension = current_filename[3]
  # Make sure all the words in the song name are capitalized:
  #   Doing this manually instead of using string.capwords() is necessary because
  #   otherwise words after an open parentheses will be lower-cased.
  song_word_list = song.split()
  new_song_word_list = []
  for word in song_word_list:
    if word.startswith('('):
      new_song_word_list.append('(' + word[1:].capitalize())
    else:
      new_song_word_list.append(word.capitalize())
  new_song_name = ' '.join(new_song_word_list)
  # Remove the track number from the song name:
  new_song_name = new_song_name[3:]
  # Reconstruct the filename:
  new_filename = artist + ' - ' + new_song_name + '.' + extension
  # Write the new filename:
  print("Renaming file `{}` to `{}`.".format(file, new_filename))
  os.rename(directory + file, directory + new_filename)
  return


def set_necessary_tags(file, artist, song):
  file.set_version(VERSION_2)
  file.artist = artist
  file.song = song
  file.save()
  return


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('directory', help='System path to directory containing files.')
  parser.add_argument('--rename_files', help='Use this if you want to rename files.  \
    Useful only if the files haven\'t already been manually renamed.', action='store_true')
  parser.add_argument('--correct_key_comment', help='Use this if you want to remove the `/` between \
    keys added by MixedInKey, and add `N/A` if no key was added (i.e. file was too long).', action='store_true')
  args = parser.parse_args()
  correct_key_comment = args.correct_key_comment
  directory = args.directory
  rename_files = args.rename_files
  # First, rename the files themselves to get rid of Album and Track number) if that option was passed:
  if rename_files:
    file_list = get_file_list(directory)
    for file in file_list:
      rename_file(file, directory)
  # Next, re-read the files with their new names and update the ID3 tags:
  file_list = get_file_list(directory)
  for file in file_list:
    print("Scrubbing ID3 tags for `{}`.".format(file))  
    artist, song = get_info_from_filename(file)
    file = MP3File(directory + file)
    delete_unnecessary_tags(file, correct_key_comment)
    set_necessary_tags(file, artist, song)
    # Correct the key written to the comment tag if MixedInKey has already been run.
    if correct_key_comment:
      correct_comment_tag(file)
  exit()


if __name__ == '__main__':
  main()
