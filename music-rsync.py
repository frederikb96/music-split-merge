# ---------------------------------------
# ADB:
# adb root
#
# Delete files and copy new ones:
# from phone to pc (you rather deleted and created files on phone)
# adb-sync -dfR sdcard/Music/Media/ /mnt/Backup/owncloud/Music/ --dry-run
# from pc to phone (you rather deleted and created files on pc)
# adb-sync -df /mnt/Backup/owncloud/Music/ sdcard/Music/Media/ --dry-run
#
# Than update only modified files with this script, both directions are ok:
# ---------------------------------------
import subprocess
import datetime

# ------------------------------------
# USER VALUES CHANGE HERE
# ----------------
dirSd = "sdcard/Music/Media/"
dirL = "/mnt/Backup/owncloud/Music/"
dateString = "2021-08-17 16:30:58"
sd2L = 1    # Direction sd to linux
# -----------------------------------

dateFormat = "%Y-%m-%d %H:%M:%S"
dateOld = datetime.datetime.strptime(dateString, dateFormat)
dateNew = datetime.datetime.now()
dateDif = dateNew - dateOld
print("DateDif: ", dateDif)
dateDif = dateDif.total_seconds()
if dateDif < 0:
    print("date negative")
    quit()
dateDif = (dateDif / -60).__int__() # convert to minutes from seconds

if sd2L:
    cmd = ["adb", "shell", "find", dirSd, "-type", "f", "-mmin", str(dateDif)]
else:
    cmd = ["find", dirL, "-type", "f", "-mmin", str(dateDif)]
process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
files = process.stdout
files = files.splitlines()
print("FILES " + str(files.__len__())+ " :")
print(process.stdout)

print("\nSTART:")
for f in files:
    if sd2L:
        fSd = f
        fName = fSd.replace(dirSd, '')
        fL = dirL + fName
        cmd = ["adb", "pull", fSd, fL]
    else:
        fL = f
        fName = fL.replace(dirL, '')
        fSd = dirSd + fName
        cmd = ["adb", "push", fL, fSd]
    # print(cmd)
    process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    outputMessage = (process.stdout.splitlines())[-1]
    print(process.stderr + outputMessage + "\n")
print("Finished! COPY NEW DATE!!!!")
print(dateNew.strftime(dateFormat))