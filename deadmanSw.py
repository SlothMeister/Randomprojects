import datetime
import time
import pyAesCrypt
import twint


# This is the payload - it will encrypt whatever file we specified. Commeted out the part that deletes the original file
def FirePayload(filePath, encryptPass):
    print("Activated Payload!!!")
    bufferSize = 64 * 1024  # Encryption/decryption buffer size - 64K
    pyAesCrypt.encryptFile(filePath, (filePath+'.aes'), encryptPass, bufferSize)  # encrypt


# Checks for the keyphrase on twitter, checks if the time is up.
def CheckKey(c, delayTime, filePath, encryptPass, targetTime):
    try:
        twint.run.Search(c)
    except ValueError:
        print("Something bad happen")
        GetTargets()
    tweets = twint.output.tweets_list
    if not tweets:
        if (time.time() >= targetTime):
            FirePayload(filePath, encryptPass)
        else:
            print("No results, trying again after delay")
            time.sleep(delayTime)
            CheckKey(c, delayTime, filePath, encryptPass, targetTime)
    else:
        print("Deadswitch de-activated, entered safe mode")
        exit()


# Gets the information to run the loop, such as the keyword, file to encrypt.
def GetTargets():
    c = twint.Config()
    startTime = input("Date to start searching (Format: %Y-%M-%D)\n>")
    try:
        datetime.datetime.strptime(startTime, "%Y-%M-%D")
    except ValueError:
        print("That's Not a date, try again (Format: %Y-%M-%D)")
        GetTargets()  # Make sure the format is correct for the data.
    c.Since = startTime
    c.Search = input("Keyphrase to disarm switch?\n>")
    c.Username = input("Twitter account to watch?\n>")
    delayTime = int(input("Time in seconds to wait between checking the account?\n>"))
    filePath = input("File to encrypt if switch fires?\n>")
    encryptPass = input("Password to encrypt file?\n>")
    targetTime = (time.time() + (int(input("How many mintues to run before firing?\n>")) * 60))
    c.Hide_output = True
    c.Store_object = True
    CheckKey(c, delayTime, filePath, encryptPass, targetTime)


GetTargets()
