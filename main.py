import time
from pydub import AudioSegment
from pydub.playback import play
from pydub.silence import split_on_silence
import numpy as np
from pydub.utils import mediainfo
from os import walk
from os import listdir
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import subprocess


if __name__ == '__main__':

    # --------------------------------------
    # Constants that have to be changed frequently
    # Give all songs a genre tag
    genreName = "AlternativeFM02"
    # --------------------------------------

    # Directories with the files
    dirSource = "/home/freddy/Downloads/ripperOld"
    dirNew = "/home/freddy/Downloads/ripperNew"
    dirTrash = "/home/freddy/Downloads/ripperTrash"

    # Sort the files
    files = [f for f in listdir(dirSource)]
    files.sort()

    # Constants for the music splitting
    # Upper limit in time - length in seconds to listen from the next song
    timeOffSetSecond = 10000
    # Lower limit in time - length in seconds to listen from the end of the previous song
    timeOffSet = -15000 - timeOffSetSecond
    # When user sets moment in time to split, cut away a little more
    # Amount to cut away from previous song
    timeCut = 1000
    # Amount to cut away from the next song
    timeCutSecond = 200

    # Constants for song tagging out of file name
    # Remove the first chars from the file name
    nameRemoveBeginning = 30

    # Flag if user stops process
    stop = 0
    # Say if first song shall be saved, do only if beginning of first song is correct!
    firstSave = 0

    # Check if enough songs available (first and last song have to be discarded)
    if len(files) < 3:
        raise Exception("Minimum of 3 files required. First and last are discarded!")
    # Get first song from list and use as previous song
    song1 = AudioSegment.from_mp3(dirSource + "/" + files[0])
    # Loop though songs
    for index in range(len(files)):

        # Get next song
        song2 = AudioSegment.from_mp3(dirSource + "/" + files[index + 1])
        # Create new song with beginning of next song added to previous one
        song1 = song1 + song2[:timeOffSetSecond]
        # Cut that part away from next song
        song2 = song2[timeOffSetSecond + 1:]

        # Loop until user is ok with cut result
        repeat = 1
        timeOffSetNew = timeOffSet
        while repeat:

            # Play song and wait for user interrupt to save new cutting time
            timeTic = time.time()
            try:
                play(song1[timeOffSetNew:])
            except KeyboardInterrupt:
                pass
            timeToc = time.time()
            # Calculate new times for end
            dif = (timeToc - timeTic) * 1000
            timeEnd = timeOffSetNew + dif - timeCut
            if timeEnd >= 0:
                timeEnd = -25
            # create new song
            songNew = (song1[:timeEnd] + AudioSegment.silent(1000, song1.frame_rate)).fade_out(2000)
            # calculate new time for start second
            timeStartSecond = timeOffSetNew + dif - timeCutSecond
            if timeStartSecond >= 0:
                timeStartSecond = -1

            # check if repeat sequence
            try:
                cmd1 = input("\n'ö':repeat; 'p':cut middle; 'o':play new end;\n 'l':change start; 'k':end; other:continue")
                if cmd1 == 'ö':
                    repeat = 1
                elif cmd1 == 'p':
                    # Loop variables
                    middleRep = 1
                    # Loop for middle Cut
                    while middleRep:
                        repeat = 0
                        # play cut sequence
                        timeTic = time.time()
                        play(song1[timeEnd:])
                        timeToc = time.time()
                        dif = (timeToc - timeTic) * 1000
                        # calculate new time for start second
                        timeStartSecond = timeEnd + dif - timeCutSecond
                        if timeStartSecond >= 0:
                            timeStartSecond = -1
                        # check if repeat
                        cmd2 = input("\n'ö':repeat; 'p':repeat all; other:continue")
                        if cmd2 == 'ö':
                            middleRep = 1
                        elif cmd2 == 'p':
                            middleRep = 0
                            repeat = 1
                        else:
                            middleRep = 0
                elif cmd1 == 'o':
                    # play firsts song end
                    play(songNew[-4000:])
                    # play second song beginning
                    if timeStartSecond + 4000 < 0:
                        play(song1[timeStartSecond:timeStartSecond+4000])
                    else:
                        play(song1[timeStartSecond:])
                    # check user input
                    cmd2 = input("\n'ö':repeat; other:continue")
                    if cmd2 == 'ö':
                        repeat = 1
                    else:
                        repeat = 0
                elif cmd1 == 'l':
                    timeOffSetNew = input("\nEnter new offset: (-15000)")
                    timeOffSetNew = int(timeOffSetNew) - timeOffSetSecond
                    repeat = 1
                elif cmd1 == 'k':
                    stop = 1
                    repeat = 0
                else:
                    repeat = 0
            except:
                repeat = 1

        # All finished and tag new song
        # Get name of file and create tags out of file name
        newName = files[index]
        # Cut away beginning of file name
        newName = newName[nameRemoveBeginning:]
        # Remove the ending and numbers due to duplicates
        newTags = newName.replace('.mp3', '')
        newTags = newTags.replace(' (1)', '')
        newTags = newTags.replace(' (2)', '')
        # Split the song into artist and title
        # Artist
        newTags = newTags.split(" - ")
        newArtist = newTags[0]
        # Use title case
        newArtist = newArtist.title()
        # Title if available
        if len(newTags) > 1:
            newTitle = newTags[1]
            newTitle = newTitle.title()
            # Create a new name from new artist and title
            newName = newArtist + " - " + newTitle + ".mp3"
        else:
            newTitle = 'NoTitle'

        # Check if it is the first song, otherwise save
        if firstSave:
            # Save the song and assign the tags
            songNew.export(dirNew + "/" + newName, format = "mp3", tags = {'title': newTitle, 'artist': newArtist})
            # Not all tags have been set, so reload and assign other tags
            m = MP3(dirNew + "/" + newName, EasyID3)
            m["title"] = newTitle
            m["artist"] = newArtist
            m["genre"] = genreName
            # Save again with new tags
            m.save()
            print("\n--------------------\n%s\n--------------------\n" %newName)
        else:
            firstSave = 1

        # Check if end of file list has been reached or stopped
        # Last song can not be used anymore, since ending will be wrong without a following song
        if index + 1 >= len(files) or stop:
            break

        # Next section only relevant if not stopped and ending not reached
        # Move used song to trash folder
        cmd = ["mv", dirSource + "/" + files[index], dirTrash + "/" + files[index]]
        process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Use next song as new previous song and fix its beginning according to results
        song1 = song1[timeStartSecond:] + song2

    # ------
    # OLD
    # -------
    # amp = [0] * 5
    # m = [0] * 5

    # song = AudioSegment.from_mp3("05 - Kann mich irgendjemand hören.mp3")
    # id = 0
    # min = 4
    # sec = 21.15
    # time = 1000 * (min * 60 + sec)
    # timeEnd = time + 1 * 1000
    # songA = song[time:timeEnd]
    # amp[id] = songA.dBFS
    # seq = songA.get_array_of_samples()
    # m[id] = np.mean(seq)
    # # play(songA)
    #
    # song = AudioSegment.from_mp3("AlternativeFM - rockt.  - THE LUKA STATE - GIRL.mp3")
    # id = 1
    # min = 2
    # sec = 34.8
    # time = 1000 * (min * 60 + sec)
    # timeEnd = time + 1 * 1000
    # songA = song[time:timeEnd]
    # amp[id] = songA.dBFS
    # seq = songA.get_array_of_samples()
    # m[id] = np.mean(seq)
    # # play(songA)
    #
    # song = AudioSegment.from_mp3("AlternativeFM - rockt.  - BEATSTEAKS - 40 DEGREES.mp3")
    # id = 2
    # min = 2
    # sec = 20.2
    # time = 1000 * (min * 60 + sec)
    # timeEnd = time + 1 * 1000
    # songA = song[time:timeEnd]
    # amp[id] = songA.dBFS
    # seq = songA.get_array_of_samples()
    # m[id] = np.mean(seq)
    # # play(songA)
    #
    # song = AudioSegment.from_mp3("AlternativeFM - rockt.  - 30 SECONDS TO MARS - THIS IS WAR.mp3")
    # id = 3
    # min = 4
    # sec = 44.7
    # time = 1000 * (min * 60 + sec)
    # timeEnd = time + 1 * 1000
    # songA = song[time:timeEnd]
    # amp[id] = songA.dBFS
    # seq = songA.get_array_of_samples()
    # m[id] = np.mean(seq)
    # # play(songA)
    #
    # song = AudioSegment.from_mp3("AlternativeFM - rockt.  - TOOL - SOBER.mp3")
    # id = 4
    # min = 4
    # sec = 53.5
    # time = 1000 * (min * 60 + sec)
    # timeEnd = time + 1 * 1000
    # songA = song[time:timeEnd]
    # amp[id] = songA.dBFS
    # seq = songA.get_array_of_samples()
    # m[id] = np.mean(seq)
    # # play(songA)
    #
    # print("AMP:\n")
    # for a in amp:
    #     print(a,"\n")
    #
    # print("MEAN:\n")
    # for n in m:
    #     print(n, "\n")
