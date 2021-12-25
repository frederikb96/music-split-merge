# ---------------------------------------
# ---------------------------------------
import mutagen
from mutagen.id3 import ID3
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import subprocess

# ------------------------------------
# USER VALUES CHANGE HERE
dirL = "/mnt/Backup/owncloud/Music/"
# -----------------------------------

cmd = ["find", dirL, "-type", "f", "-name", "*.mp3"]
process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
files = process.stdout
files = files.splitlines()
print(len(files))



# # start tracknumber in album and non albums
# print("\nStart:")
# l = {}
# for f in files:
#     m = MP3(f, EasyID3)
#     title = str(m["title"])
#     try:
#         album = str(m["album"])
#         try:
#             if album in l:
#                 l[album] += 1
#             else:
#                 l[album] = 1
#         except:
#             print(title)
#     except:
#         pass
#
# print("\nStartWriting:")
# for f in files:
#     mn = MP3(f, EasyID3)
#     titlen = str(mn["title"])
#     try:
#         albumn = str(mn["album"])
#         try:
#             if l[albumn] <= 1:
#                 try:
#                     trackn = mn["tracknumber"]
#                 except:
#                     mn["tracknumber"] = ['01']
#             else:
#                 pass
#         except:
#             print(titlen)
#             a = 1
#     except:
#         try:
#             mn.pop("albumartist")
#             print(titlen)
#             a = 1
#         except:
#             pass
#         try:
#             mn.pop("tracknumber")
#             print(titlen)
#             a = 1
#         except:
#             pass
#     # mn.save()
# print("done")












# # start rename albums with only one song to unknown and album interpret also away
# print("\nStart:")
# l = {}
# for f in files:
#     m = MP3(f, EasyID3)
#     title = str(m["title"])
#     try:
#         album = str(m["album"])
#         try:
#             if album in l:
#                 l[album] += 1
#             else:
#                 l[album] = 1
#         except:
#             print(title)
#     except:
#         pass
# # for key, value in l.items():
# #     print(key, " : ", value)
#
# print("\nStartWriting:")
# for f in files:
#     mn = MP3(f, EasyID3)
#     titlen = str(mn["title"])
#     try:
#         albumn = str(mn["album"])
#         try:
#             if l[albumn] <= 1:
#                 trackn = 1
#                 try:
#                     trackn = mn["tracknumber"]
#                     if trackn == ['01/01'] or trackn == ['01']:
#                         trackn = 1
#                     else:
#                         trackn = 2
#                 except:
#                     pass
#                 if trackn == 1:
#
#                     if (titlen.lower().find(albumn.lower()) != -1) or (albumn.lower().find(titlen.lower()) != -1):
#                         pass
#                     else:
#                         print(titlen, " : ", albumn, "\n")
#                         mn.pop("album")
#                         try:
#                             mn.pop("albumartist")
#                         except:
#                             pass
#                         # mn.save()
#
#                     # mn.pop("album")
#                     # try:
#                     #     mn.pop("albumartist")
#                     #     print("poped", titlen)
#                     # except:
#                     #     mn.save()
#                     #     pass
#                     # # mn.save()
#
#             else:
#                 pass
#         except:
#             print(titlen)
#     except:
#         pass















# # start search album with unknown
# print("\nStart:")
# a=0
# for f in files:
#     m = MP3(f, EasyID3)
#     title = str(m["title"])
#     if title.find("hatta") != -1:
#         print(title)
#         pass
#     try:
#         album = str(m["album"])
#         # if album.find("Unknown") != -1:
#             # print(title)
#             # m.pop("album")
#             # m.save()
#     except:
#         pass
#         a += 1
#         print(title)
# print(a)






# # start search unknown artists
# print("\nStart:")
# a=0
# for f in files:
#     m = MP3(f, EasyID3)
#     title = str(m["title"])
#     try:
#         artist = str(m["artist"])
#         # if artist.find("Unknown") != -1:
#         #     print(title)
#         #     m.pop("artist")
#         #     m.save()
#
#     except:
#         pass
#         a += 1
#         print(title)
# print(a)











# # Convert m4a to mp3
# a = 0
# for f in files:
#     try:
#         out = f.replace(".m4a", ".mp3")
#         cm = ["ffmpeg", "-v", "5", "-y", "-i", f, "-acodec", "libmp3lame", "-ac", "2", "-ab", "192k", out]
#         p =  subprocess.run(cm, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#         a += 1
#         print(out)
#         if p.stderr != "":
#             print("\n\n\n\nERRIR"+out)
#     except:
#         print("\n\n\n\nERRIR"+out)
# print(a)


# # start search title split but no art
# print("\nStart:")
# for f in files:
#     m = MP3(f, EasyID3)
#     title = str(m["title"][0])
#     titleSplit = title.split(" - ")
#     if len(titleSplit) <= 1:
#         continue
#     try:
#         artist = str(m["artist"][0])
#         if title.find(artist) != -1:
#             continue
#         print("Art: " + artist)
#     except:
#         pass
#     print("Title: " + title + "\n")





# # start title to new title and art
# for f in files:
#     m = MP3(f, EasyID3)
#     title = str(m["title"][0])
#     try:
#         artist = str(m["artist"][0])
#         preTitle = title.split(" - ")
#         if preTitle.__len__() <= 1:
#             continue
#         postTitle = preTitle[1]
#         preTitle = preTitle[0]
#         if preTitle.find(artist) != -1:
#             m["artist"] = [preTitle]
#             m["title"] = [postTitle]
#             print("Title: " + title + "\n" + "Art: " + artist)
#             m.save()
#             print("NewTitle: " + postTitle + "\n" + "NewArt: " + preTitle + "\n")
#     except:
#         pass
