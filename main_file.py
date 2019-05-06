import os
import random

# get the list of all songs in a directory
song_list = os.listdir('F:\Videos\Hindi_SONGZ')
print(str(len(song_list)) + ' Songs in your collection.')
flg = 1

# play random songs from the directory
while True:
    try:
        now_playing_song = random.choice(song_list)
        song_name_length = len(now_playing_song)
    except IndexError:
        print('played all songs, no more songs to play..')
        break

    print('\nCurrently playing '
          '\n{}'
          '\n: {}'
          '\n{}'
          .format('-'*song_name_length,
                  now_playing_song[:-4],
                  '-'*song_name_length))

    song_file_location = "F:\Videos\Hindi_SONGZ\{}".format(now_playing_song)
    os.system('"' + song_file_location + '"')

    song_list.remove(now_playing_song)
    print(len(song_list))

    # flg = int(input('\nPlay next or stop: (1/0)'))
