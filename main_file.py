import os
import random
import pandas as pd
import re


def select_folder():
    folders_data = pd.read_csv('song_folders.csv')
    folder_names = list(folders_data['Folder_Name'])
    folder_paths = list(folders_data['Folder_path'])

    # print(folder_names[2])
    # print(folder_paths)

    ind = 0
    for index, row in folders_data.iterrows():
        ind = index + 1
        print(str(ind) + '. ' + row['Folder_Name'])
    print(str(ind + 1) + '. ' + 'Select Randomly')
    print('last value ind: ' + str(ind))
    choice = int(input('Enter your choice no: '))
    if 0 < choice <= ind:
        # print('Apna Choice wala')   # debug
        # print('\nPlaying from: {}'.format(folder_names[choice - 1]))
        selected_folder_name = folder_names[choice - 1]
        print('\nPlaying from Folder'
              '\n{}'
              '\n: {}'
              '\n{}'.format('-' * (len(selected_folder_name) + 4), selected_folder_name,
                            '-' * (len(selected_folder_name) + 4)))

        return folder_paths[choice - 1]
    else:
        # print('Apna Random wala')   # debug
        rand_choice = random.randint(1, ind - 1)
        # print('\nPlaying from: {}'.format(folder_names[rand_choice - 1]))
        selected_folder_name = folder_names[rand_choice - 1]
        print('\nPlaying from Folder'
              '\n{}'
              '\n: {}'
              '\n{}'.format('-' * (len(selected_folder_name) + 4), selected_folder_name,
                            '-' * (len(selected_folder_name) + 4)))

        return folder_paths[rand_choice - 1]


# play random songs from the directory
def play_music(folder_path, song_list):
    flg = 1
    while flg == 1:
        try:
            now_playing_song = random.choice(song_list)
            song_name_length = len(now_playing_song)
        except IndexError:
            print('No more songs to play..')
            break

        print('\nCurrently playing '
              '\n{}'
              '\n: {}'
              '\n{}'
              .format('-' * song_name_length,
                      now_playing_song[:-4],
                      '-' * song_name_length))

        song_file_location = "{}\{}".format(folder_path, now_playing_song)
        os.system('"' + song_file_location + '"')

        song_list.remove(now_playing_song)
        print(len(song_list))

        flg = int(input('\nPlay next or stop: (1/0)'))


if __name__ == '__main__':
    folder_path = select_folder()  # selects a folder to play songs from
    song_list = os.listdir(folder_path)  # get the list of all songs in a directory
    print('\n' + str(len(song_list)) + ' Songs ')
    play_music(folder_path, song_list)
