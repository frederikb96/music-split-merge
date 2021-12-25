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

# --------------------------------------
# Say if first song is already saved
firstSave = 0 # 0 if stopped and proceed
genreName = "AlternativeFM02"
# --------------------------------------

# get all file names
dir = "/home/freddy/Downloads/ripperOld"
dirNew = "/home/freddy/Downloads/ripperNew"
files = [f for f in listdir(dir)]
files.sort()

# Constants
timeOffSetSecond = 10000
timeOffSet = -15000 - timeOffSetSecond
timeCut = 1000
timeCutSecond = 200
stop = 0
# Loop though songs
song2 = AudioSegment.from_mp3(dir + "/" + files[0])
for index in range(len(files)):
    # import song
    song1 = song2
    if index + 1 < len(files):
        song2 = AudioSegment.from_mp3(dir + "/" + files[index + 1])
        song1 = song1 + song2[:timeOffSetSecond]
        song2 = song2[timeOffSetSecond + 1:]

    # Loop variables
    repeat = 1
    timeOffSetNew = timeOffSet
    # play song and safe time
    while repeat:
        try:
            timeTic = time.time()
            play(song1[timeOffSetNew:])
            timeToc = time.time()
            time.sleep(0.5)
        except KeyboardInterrupt:
            pass
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

    # all finished and save new song
    newName = files[index]
    newName = newName[30:]
    newTags = newName.replace('.mp3', '')
    newTags = newTags.replace(' (1)', '')
    newTags = newTags.replace(' (2)', '')
    newTags = newTags.split(" - ")
    newArtist = newTags[0]
    newArtist = newArtist.title()
    if len(newTags) > 1:
        newTitle = newTags[1]
        newTitle = newTitle.title()
        newName = newArtist + " - " + newTitle + ".mp3"
    else:
        newTitle = 'NoTitle'

    # if stopped mark this last song to be used next time as start
    if stop:
        newName = "000_CONT_HERE_RENAME_" + newName
    # Save song
    if firstSave:
        songNew.export(dirNew + "/" + newName, format = "mp3", tags = {'title': newTitle, 'artist': newArtist})
        m = MP3(dirNew + "/" + newName, EasyID3)
        m["title"] = newTitle
        m["artist"] = newArtist
        m["genre"] = genreName
        m.save()
        print("\n--------------------\n%s\n--------------------\n" %newName)
    else:
        firstSave = 1

    # break if stopped
    if stop:
        break

    # create next song and append data
    if index + 1 < len(files):
        song2 = song1[timeStartSecond:] + song2

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
