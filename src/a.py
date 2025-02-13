import json
import os
import shutil
import subprocess
import threading
import time
import tkinter
import utils


def buttonStartEvent():
    finalarg = cubingFolder + "\\jre\\bin\\java.exe " + jvmargs.get() + " -Djava.library.path=cubing\\natives -classpath cubing\\CubingClient.jar;cubing\\libraries\\oshi-project\\oshi-core\\1.1\\oshi-core-1.1.jar;cubing\\libraries\\net\\java\\dev\\jna\\jna\\3.4.0\\jna-3.4.0.jar;cubing\\libraries\\net\\java\\dev\\jna\\platform\\3.4.0\\platform-3.4.0.jar;cubing\\libraries\\com\\ibm\\icu\\icu4j-core-mojang\\51.2\\icu4j-core-mojang-51.2.jar;cubing\\libraries\\net\\sf\\jopt-simple\\jopt-simple\\4.6\\jopt-simple-4.6.jar;cubing\\libraries\\com\\paulscode\\codecjorbis\\20101023\\codecjorbis-20101023.jar;cubing\\libraries\\com\\paulscode\\codecwav\\20101023\\codecwav-20101023.jar;cubing\\libraries\\com\\paulscode\\libraryjavasound\\20101123\\libraryjavasound-20101123.jar;cubing\\libraries\\com\\paulscode\\librarylwjglopenal\\20100824\\librarylwjglopenal-20100824.jar;cubing\\libraries\\com\\paulscode\\soundsystem\\20120107\\soundsystem-20120107.jar;cubing\\libraries\\io\\netty\\netty-all\\4.0.23.Final\\netty-all-4.0.23.Final.jar;cubing\\libraries\\com\\google\\guava\\guava\\17.0\\guava-17.0.jar;cubing\\libraries\\org\\apache\\commons\\commons-lang3\\3.3.2\\commons-lang3-3.3.2.jar;cubing\\libraries\\commons-io\\commons-io\\2.4\\commons-io-2.4.jar;C:\\Users\\andyt\\Desktop\\CubingClient\\jars\\versions\\1.8.9\\1.8.9.jar;cubing\\libraries\\net\\java\\jinput\\jinput\\2.0.5\\jinput-2.0.5.jar;cubing\\libraries\\net\\java\\jutils\\jutils\\1.0.0\\jutils-1.0.0.jar;cubing\\libraries\\com\\google\\code\\gson\\gson\\2.2.4\\gson-2.2.4.jar;cubing\\libraries\\com\\mojang\\authlib\\1.5.21\\authlib-1.5.21.jar;cubing\\libraries\\org\\apache\\commons\\commons-compress\\1.8.1\\commons-compress-1.8.1.jar;cubing\\libraries\\org\\apache\\httpcomponents\\httpclient\\4.3.3\\httpclient-4.3.3.jar;cubing\\libraries\\commons-logging\\commons-logging\\1.1.3\\commons-logging-1.1.3.jar;cubing\\libraries\\org\\apache\\httpcomponents\\httpcore\\4.3.2\\httpcore-4.3.2.jar;cubing\\libraries\\org\\apache\\logging\\log4j\\log4j-api\\2.0-beta9\\log4j-api-2.0-beta9.jar;cubing\\libraries\\org\\apache\\logging\\log4j\\log4j-core\\2.0-beta9\\log4j-core-2.0-beta9.jar;cubing\\libraries\\org\\lwjgl\\lwjgl\\lwjgl\\2.9.4-nightly-20150209\\lwjgl-2.9.4-nightly-20150209.jar;cubing\\libraries\\org\\lwjgl\\lwjgl\\lwjgl_util\\2.9.4-nightly-20150209\\lwjgl_util-2.9.4-nightly-20150209.jar;cubing\\libraries\\tv\\twitch\\twitch\\6.5\\twitch-6.5.jar;cubing\\libraries\\commons-codec\\commons-codec\\1.9\\commons-codec-1.9.jar;cubing\\libraries\\com\\mojang\\realms\\1.7.59\\realms-1.7.59.jar Start"
    proc = subprocess.Popen(finalarg.split(" "), cwd=minecraftFolder)
    root.withdraw()
    while True:
        if proc.poll() is not None:
            exit(0)


def buttonReinstallEvent():
    showInstall(True)
    e.place_forget()
    startButton.place_forget()
    jvmLabel.place_forget()
    reinstallButton.place_forget()
    fileThread(True)


def startEvent():
    showInstall(False)
    getFiles(False)


def showInstall(reinstall):
    installLabel.config(text=("Reinstalling..." if reinstall else "Installing..."))
    installLabel.place(x=rWidth / 2, y=rHeight / 2, anchor="center")


def fileThread(value):
    threading.Thread(target=getFiles, args=(value,)).start()


def getFiles(reset):
    print(os.path.isdir(cubingFolder))
    if os.path.exists(cubingFolder):
        if not os.path.isdir(cubingFolder):
            os.remove(cubingFolder)
            os.mkdir(cubingFolder)
    else:
        os.mkdir(cubingFolder)
    paths = ["libs.zip", "natives.zip", "libraries.zip", "assets.zip", "jre.zip", "launcher.json"]
    if reset:
        for x in range(len(paths)):
            isFolder = paths[x].split(".")[1] == "zip"
            shutil.rmtree(cubingFolder + "\\" + (paths[x].split(".")[0] if isFolder else paths[x]))
            fileLoc = cubingFolder + "\\" + paths[x]
            if os.path.exists(fileLoc):
                os.remove(fileLoc)
    for x in range(len(paths)):
        isFolder = paths[x].split(".")[1] == "zip"
        if reset or (not os.path.exists(cubingFolder + "\\" + (paths[x].split(".")[0] if isFolder else paths[x]))):
            fileLoc = cubingFolder + "\\" + paths[x]
            utils.dl("https://speedcubing.top/files/cubingclient/" + paths[x], fileLoc)
            if isFolder:
                utils.ext(fileLoc, minecraftFolder + "\\cubing")
                os.remove(fileLoc)
    global f, texts, updateState
    f = json.load(open(cubingFolder + "\\launcher.json"))
    texts.clear()
    redotexts.clear()

    installLabel.place_forget()

    eWidth = 700
    e.place(x=(rWidth - eWidth) / 2, y=300, width=eWidth, height=50)
    updateState = True
    e.insert(0, f["jvmargs"])
    updateState = False

    startWidth = 120
    startButton.place(x=(rWidth - startWidth) / 2, y=400, width=startWidth, height=60)
    jvmLabel.place(x=(rWidth - eWidth) / 2, y=270)

    reinstallButton.place(x=850, y=450, width=100, height=60)


def updateArgs():
    global updateState, lastModified
    if not updateState:
        current = int(time.time() * 1000.0)
        if current - lastModified > 1000:
            texts.insert(0, f["jvmargs"])
        lastModified = current
    f["jvmargs"] = jvmargs.get()
    with open(cubingFolder + "\\launcher.json", "w") as outfile:
        outfile.write(json.dumps(f, indent=4))


def undo(event):
    if len(texts) > 0:
        global updateState
        redotexts.insert(0, jvmargs.get())
        updateState = True
        e.delete(0, tkinter.END)
        e.insert(0, texts[0])
        updateState = False
        texts.pop(0)


def redo(event):
    if len(redotexts) > 0:
        global updateState
        texts.insert(0, redotexts[0])
        updateState = True
        e.delete(0, tkinter.END)
        e.insert(0, redotexts[0])
        updateState = False
        redotexts.pop(0)


lastModified = 0
updateState = False
texts = []
redotexts = []

minecraftFolder = os.getenv('APPDATA') + "\\.minecraft"
cubingFolder = minecraftFolder + "\\cubing"

f = None
root = tkinter.Tk()
root.title('Cubing Client Launcher')
root.geometry('960x540')
rWidth = 960
rHeight = 540

jvmargs = tkinter.StringVar()
jvmargs.trace("w", lambda name, index, mode, jvm=jvmargs: updateArgs())
e = tkinter.Entry(root, textvariable=jvmargs, font=("Consolas", 14, 'bold'))
e.bind("<Control-z>", undo)
e.bind("<Control-Z>", redo)
startButton = tkinter.Button(root, text='Start', font=("Consolas", 16, 'bold'), command=buttonStartEvent)
jvmLabel = tkinter.Label(root, text="JVM ARGUMENTS:", font=("Consolas", 16, 'bold'))
reinstallButton = tkinter. Button(root, text='Reinstall', font=("Consolas", 12, 'bold'), command=buttonReinstallEvent)
installLabel = tkinter.Label(root, text="", font=("Consolas", 16, 'bold'))

threading.Thread(target=startEvent).start()

root.mainloop()