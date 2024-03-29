# @author swapmali

import subprocess
import os
import random
import pandas as pd
import re
import sys
from moviepy.video.io.VideoFileClip import VideoFileClip
import time


def select_folder():
    folders_data = pd.read_csv('song_folders.csv')
    folder_names = list(folders_data['Folder_Name'])
    folder_paths = list(folders_data['Folder_path'])

    # print music folders to choose where to play from or random folder select choice or ask for enter folder path
    ind = 0
    for index, row in folders_data.iterrows():
        ind = index + 1
        print(str(ind) + '. ' + row['Folder_Name'])
    ind += 1
    print(str(ind) + '. ' + 'Select Randomly')
    ind += 1
    print(str(ind) + '. ' + 'Enter manually New Folder path')

    try:
        choice = int(input('\nEnter your choice no: '))
        if 0 < choice <= (ind - 2):
            selected_folder_name = folder_names[choice - 1]
            print('\nPlaying from Folder '
                  '\n{}'
                  '\n** {} **'
                  '\n{}'.format('*' * (len(selected_folder_name) + 6), selected_folder_name,
                                '*' * (len(selected_folder_name) + 6)))

            return folder_paths[choice - 1]

        elif choice == (ind - 1):
            rand_choice = random.randint(1, ind - 1)
            selected_folder_name = folder_names[rand_choice - 1]
            print('\nPlaying from Folder '
                  '\n{}'
                  '\n** {} **'
                  '\n{}'.format('*' * (len(selected_folder_name) + 6), selected_folder_name,
                                '*' * (len(selected_folder_name) + 6)))

            return folder_paths[rand_choice - 1]

        else:
            return input('\nEnter folder path:')

    except ValueError:
        print('\nPlease try again with valid choice..')
        sys.exit()


def play_music(folder_path, song_list):  # play random songs from the directory
    while True:
        try:
            now_playing_song = random.choice(song_list)     # shuffle play
            song_name_length = len(now_playing_song)
        except IndexError:
            print('No more songs to play..')    # if no songs are there is folder or all songs are already played
            break

        print('\nNow playing '
              '\n{}'
              '\n: {}'
              '\n{}'
              .format('-' * song_name_length,
                      now_playing_song[:-4],
                      '-' * song_name_length))

        # song_file_location stores complete path of a song
        song_file_location = "{}\{}".format(folder_path, now_playing_song)

        # video duration is used as timeout
        video_duration = get_file_duration(song_file_location)
        # print('waiting for ' + str(video_duration) + 'sec')

        # Main part which plays music, subprocess with timeout implementation
        p = subprocess.Popen([r"C:\Program Files\VideoLAN\VLC\vlc.exe", song_file_location])
        song_list.remove(now_playing_song)
        print('\nPlaylist : ' + str(len(song_list)) + ' songs      ', end='')
        print(str(get_playlist_time(folder_path, song_list)))
        try:
            p.wait(video_duration - 4)      # if media player is closed by the user starts playing next music
        except subprocess.TimeoutExpired:
            p.kill()                        # wait till audio/video playing is completed and start next playing next music


def get_file_duration(song_file_location):      # returns video duration in seconds of video file currently playing
    clip = VideoFileClip(song_file_location)
    video_duration = clip.duration
    clip.reader.close()
    clip.audio.reader.close_proc()
    return video_duration


def make_song_list(folder_path):
    # regular expression to match all types of file formats supported by VLC media player
    pattern = '.{0,}\.(avi|mkv|mp4|wmv|mov|flv|ogm|vob|dat|ogg|asf|m1v|m2v|mp3|aac|flac|wma|rma)'

    all_files_list = os.listdir(folder_path)    # stores list of all files in the folder
    valid_music_files = []                      # stores list of only music files which are playable in the folder
    invalid_music_files = []                    # stores list of files which are not playable

    for i in range(len(all_files_list)):
        if re.match(pattern, all_files_list[i]):
            valid_music_files.append(all_files_list[i])
        else:
            invalid_music_files.append(all_files_list[i])

    no_all_files = len(all_files_list)          # total files in the folder
    no_music_files = len(valid_music_files)     # no of songs in the folder

    if no_all_files == no_music_files:
        print('\n' + str(no_music_files) + ' Songs ')
    else:
        print('\n' + '=' * (13 + count_digit(no_all_files)) +
              '\nTotal files: ' + str(no_all_files) +
              '\nMusic files: ' + str(no_music_files) +
              '\n' + '=' * (13 + count_digit(no_all_files)))

    return valid_music_files


def get_playlist_time(folder_path, song_list):
    total_time = 0
    # print('\nCalculating Total Playlist time..Please wait')
    for i in range(len(song_list)):
        song_file_location = "{}\{}".format(folder_path, song_list[i])
        clip = VideoFileClip(song_file_location)
        total_time += clip.duration
        clip.reader.close()
        clip.audio.reader.close_proc()
    formatted_time = time.strftime('%Hhr %Mmin %Ssec', time.gmtime(total_time))
    return formatted_time


def count_digit(n):
    cnt = 0
    while n > 0:
        n = n // 10
        cnt += 1
    return cnt


if __name__ == '__main__':
    folder_path = select_folder()               # selects a folder to play songs from
    song_list = make_song_list(folder_path)     # list of all songs in a folder
    play_music(folder_path, song_list)          # plays music in shuffle from the folder selected
