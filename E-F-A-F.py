#علوش

from PIL import Image
from cryptography.fernet import Fernet
from random import randint
import base64
import math
import time
import os
import webbrowser

# TODO:
#    ADD AN ALTERNATIVE TEXT FOR A SPECIFIC KEY
#    ADD BORDERS
#    ADD IMAGETOIMAGE ENCRYPTION


def main():

    intro()
    getCommand()


def intro():

    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-# E.F.A.F Tool - Developed By: AbdulKarim Aldallo #=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
    time.sleep(0.5)
    print("Telegram: @xAbdulKareem")
    time.sleep(0.5)
    print("Use \"help\" or check the documentation if you do not know how to use the tool")


#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def getCommand():

    command = input("E.F.A.F: ")
    commandHandler(command.lower().split())


def commandHandler(cmd):
    if len(cmd) == 0:
        getCommand()
    time.sleep(0.5)
    if cmd[0] == "help":
        help()
    elif cmd[0] == "info" or cmd[0]  == "information":
        info()
    elif cmd[0] == "exit" or cmd[0]  == "stop":
        exit()
    elif cmd[0] == "encrypt":
        encryptCMDHandler(cmd)
    elif cmd[0] == "decrypt":
        decryptCMDHandler(cmd)
    elif cmd[0] == "documentation" or cmd[0] == "docs":
        openDocs()
    else:
        print("Unrecognized  command. Use \"help\" to get a list of all the available commands")
        getCommand()


#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


def help():
    print("=================================================")
    print("List of all available Commands: ")
    print("decrypt - Starts the decryption function")
    print("docs/documentation - Opens the documentation webpage")
    print("encrypt - Starts the encryption function")
    print("exit - Stops the program")
    print("help - Prints a list of all available commands")
    print("info/information - Prints the tool's information")
    print("stop - Stops the program")    
    print("=================================================")

    getCommand()


def info():

    print("====================================")
    print("Docs: https://github.com/Aldallo/E.F.A.F-Tool")
    print("Developer: AbdulKareem")
    print("Telegram: @xAbdulKareem")
    print("Version: 1.0.1 (Stable)")
    print("Release Date: 07/03/2019")
    print("Special thanks: HarvardX CS50, Omar A. Lebda")
    print("====================================")

    getCommand()


def openDocs():

    webbrowser.open("https://github.com/Aldallo/E.F.A.F-Tool")
    print("The documentation has been opened with your default browser")
    getCommand()

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


def getKey():

    while True:
        key = input("Key: ")
        if len(key) > 0:
            break
    return key

def EncryptionType(key):

    if len(key) == 32:
        return "Fernet"
    else:
        return "Vigenere"

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


def getInputImage():

    while True:
        t = input("Input Image Name: ")
        if os.path.isfile(f"./{t}"):
            break
        else:
            print("Image does not exist")
    return t


def getOutputImage():

    while True:
        t = input("Output Image Name: ").split(".")
        if os.path.isfile(f"./{t[0]}.png"):
            answer = input("There's already an image with that name. Do you want to overwrite it (Y/N)?" ).lower()
            if answer == "y" or answer == "yes":
                return f"{t[0]}.png"
            else:
                pass
        else:
            return f"{t[0]}.png"

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-    


def vigenereKeySlotAssign(key, array):

    for i in range(len(key)):

        if key[i].isdigit():

            array.append(ord(key[i]) - 48)

        elif ord(key[i]) == 32:

            array.append(ord(key[i]) + 36)
        
        elif key[i].isalpha():

            if key[i].isupper():
                array.append(ord(key[i]) - 65)
            if key[i].islower():
                array.append(ord(key[i]) - 97)
        else: 
            array.append(ord(key[i]) - 33)
    return array

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-    



def decryptCMDHandler(cmd):
    if len(cmd) == 1:
        decryptHelp()
    elif len(cmd) == 2:
        if cmd[1] == "types" or cmd[1] == "help":
            decryptHelp()
        if cmd[1] == "textfromimg":
            decryptTextFromImg()
        else:
            print("Invalid argument. Use \"decrypt help\" to get all the available decryption methods")
            getCommand()
    else:
        print("Too many arguments. Use \"decrypt help\"")
        getCommand()



def decryptHelp():
    print("=================================================")    
    print("Usage: \"decrypt [method]\"")
    print("List of available encryption methods:")
    print("textFromImg - Decrypts text from an image")
    print("=================================================")

    getCommand()


#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-    


def decryptTextFromImg():
    inIMGName = getInputImage()
    try: 
        img = Image.open(inIMGName)
    except:
        print("The selected file is not a valid image, please try another image")
        getCommand()    

    key = getKey()
    if EncryptionType(key) == "Fernet":
        text = fernetDecryption(img, key)
    elif EncryptionType(key) == "Vigenere":
        text = vigenereDecryption(img, key)
    print(f"Decrypted Text: {text}")



def getTextFromImage(file):
    text = ""
    pixels = file.load()
    y = 0
    i = 0
    z = 0
    while True:
        if z == file.width-1: 
            y += 1
            z = 0
        if pixels[(0,y)] == (10,5,0):
            z += 1
        if pixels[(0,y)] != (10,5,0):
            break
        if pixels[(z,y)] == (0,0,0):
            break
        R,G,B = file.getpixel((z, y))
        text += (chr(R+G+B))
        i+=1
    return text


#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-    


def fernetDecryption(img, key):
    key = base64.b64encode(key.encode())
    keyHandler = Fernet(key)
    text =  getTextFromImage(img)
    plain_text = keyHandler.decrypt(text.encode())
    return plain_text.decode()


def vigenereDecryption(img, key):
    text = getTextFromImage(img)
    keyS = []
    keySlot = vigenereKeySlotAssign(key, keyS)
    length = len(key)
    counter = 0
    decryptedText = ""
    for i in range(len(text)):
        if counter == length:
            counter = 0
        if text[i].isalpha():
            if text[i].islower():
                decryptedText += (chr((((ord(text[i]) - 97) - keySlot[counter]) % 26) + 97))
            else:
                decryptedText += (chr((((ord(text[i]) - 65) - keySlot[counter]) % 26) + 65))
              
        else:
            decryptedText += (text[i])
        counter += 1    
    return decryptedText    
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def encryptCMDHandler(cmd):
    if len(cmd) == 1:
        encryptHelp()
    elif len(cmd) == 2:
        if cmd[1] == "types" or cmd[1] == "help":
            encryptHelp()
        if cmd[1] == "texttoimg":
            encryptTextToImg()
        else:
            print("Invalid argument. Use \"encrypt help\" to get all the available encryption methods")
            getCommand()
    else:
        print("Too many arguments. Use \"encrypt help\"")
        getCommand()




def encryptHelp():
    print("=================================================")    
    print("Usage: \"encrypt [method]\"")
    print("List of available encryption methods:")
    print("textToImg - Encrypts text and hide it in a selected image")
    print("=================================================")

    getCommand()


def printEncryptionMethods():

    print("===================================")
    print("Fernet encryption (32 Charachter) - Most Secure")
    print("Vigenere encryption - Not Recommended. For Keys less or more than 32 Charachter")
    print("===================================")


#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-    


def encryptTextToImg():

    text = input("Text: ")
    inIMGName = getInputImage()
    try: 
        inputImg = Image.open(inIMGName).convert('RGB')
    except:
        print("The selected file is not a valid image, please try another image")
        getCommand()    

    outIMGName = getOutputImage()
    out = inputImg
    outpx = out.load()
    printEncryptionMethods()
    key = getKey()
    if EncryptionType(key) == "Fernet":
        encryptedText = fernetEncryption(text, key).decode()
    elif EncryptionType(key) == "Vigenere":
        encryptedText = vigenereEncryption(text, key)
    else:
        print("Other encryption types are not supported yet.")
        getCommand()
    drawLines(out, encryptedText)
    drawTextToImage(encryptedText, out)
    out.save(f"{outIMGName}")
    print("Your text has been encrypted successfully!")
    getCommand()


def fernetEncryption(text, key):

    key = base64.b64encode(key.encode())
    keyHandler = Fernet(key)
    encryptedText = keyHandler.encrypt(text.encode())
    return encryptedText


def vigenereEncryption(text, key):

    keyS = []
    keySlot = vigenereKeySlotAssign(key, keyS)
    length = len(key)
    counter = 0
    encryptedText = ""
    for i in range(len(text)):
        if counter == length:
            counter = 0  
        if text[i].isalpha():
            if text[i].islower():
                encryptedText += (chr((((ord(text[i]) - 97) + keySlot[counter]) % 26) + 97))
            else:
                encryptedText += (chr((((ord(text[i]) - 65) + keySlot[counter]) % 26) + 65))
              
        else:
            encryptedText += (text[i])        
        counter += 1
    return encryptedText


#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


def drawLines(file, text):
    pixels = file.load()

    repetition = math.ceil((len(text)+1) / file.width)
    for y in range(repetition):
        for x in range(file.width):
            if x == 0:
                pixels[(x,y)] = (10,5,0)
                x += 1
            pixels[(x,y)] = (0,0,0)
    
    for y in range(repetition, 1 , -1):
        for x in range(file.width):
            pixels[x, y] = (0,0,0)


def drawTextToImage(text, file):

    pixel = file.load()
    y = 0
    x = 0
    i = 0
    while True:
        if i == len(text):
            break
        if x == 0 :
            x += 1
        if x == file.width:
            x = 1
            y += 1
        char = ord(text[i])
        v1 = math.floor(char / 3)
        v2 = math.floor(char / 3)
        v3 = char-v1-v2
        pixel[(x, y)] = (v1,v2,v3)
        x += 1
        i += 1 




#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


if __name__ == "__main__":
    main()




