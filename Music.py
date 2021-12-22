from logging import NOTSET
import multiprocessing
from typing import MutableMapping

from pydub import AudioSegment
from pydub.playback import play
import fnmatch
import os
import time 

from threading import Thread
import multiprocessing as mp
import psutil

class Music:

    def __init__(self):
        self.Tracks = []
        self.Folders = []
        self.songsList = {}
        self.__time = 0
        self.MusicControl = None
        self.SongID = None
        self.loopID = None
        self.songName = None
        self.songSegment = None

        self.songLoop = False
        self.playlistLoopFlag = False
        self.loopflag = False

        self.__get_songs()
        self.__setList()
        

    def __get_songs(self, Path = '/', Format = '*.mp3'):
        
        try :
            cacheFile = open("Cache.txt", 'x')
        except : 
            return
        
        for root, dirs, files in os.walk(Path):
            for filename in fnmatch.filter(files, Format):
                self.Folders.append(os.path.join(root))
                self.Tracks.append(os.path.join(filename))
                Source = os.path.join(root , filename)
               
                cacheFile.write(filename + ":*:")
                cacheFile.write(Source)
                cacheFile.write('\n')     
        cacheFile.close()

    
    def __setList(self):
        self.__get_songs()
        cacheFile = open("Cache.txt", 'r')
        
        for line in cacheFile:
            name, path = line.split(":*:")
            self.songsList[name] = path[:-1]
        
    def __timer(self):
        while self.SongID != psutil.STATUS_ZOMBIE:
            mins, secs = divmod(self.__time, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            print(timer, end="\r")
            time.sleep(1)
            self.__time += 1



    def selectSong(self):
        val = 1
        print("Select the song among the songs from the List below ")
        print()
        for song in self.songsList.keys():
            print(val , ": ", song)
            val += 1
        Num = int(input("\nEnter the Song Number to play : "))
        print()
        songsName = list(self.songsList)
        
        self.songName = self.songsList[songsName[Num-1]]
        self.play()
        
    
    def play(self):
        
        self.songSegment = sound = AudioSegment.from_file(self.songName, format="mp3")
        
        p1 = mp.Process(target=play, args=(sound,))
        p1.start()
        self.SongID = p1.pid    
        
        if False == self.songLoop:
            self.menu()
 

    def __pausePlay(self):
        process = psutil.Process(self.SongID)
        if self.MusicControl == 1 and process.status() == psutil.STATUS_SLEEPING:
            """
            Halt the execution of play
            """
            process.suspend()

        elif self.MusicControl == 1 and process.status() == psutil.STATUS_STOPPED:
            """
            Resume the execution of play
            """
            process.resume()


    def menu(self):
        while self.SongID != psutil.STATUS_ZOMBIE:
            #self.__timer()
            print("Enter command : ")
            self.MusicControl = int(
                input("  (1 : pause/play)\n  (2 : loopSong)\n  "
                      "(3 : loopPlaylist)\n  (4 : loopAB)\n  "
                      "(5 : seek)\n  (6 : stop)\n"))

            if 1 == self.MusicControl:
                self.__pausePlay()

            elif 2 == self.MusicControl:
                if self.loopflag == True:
                    self.loopflag = False
                    self.stop()
                else:
                    self.loopflag = True
                    self.loopSong()

            elif 3 == self.MusicControl:
                pass

            elif 4 == self.MusicControl:
                if self.loopflag == True:
                    self.loopflag = False
                    self.stop()
                else:
                    self.loopflag = True
                    self.loopAB()

            elif 5 == self.MusicControl:
                self.seek()

            elif 6 == self.MusicControl:
                self.stop()


    def seek(self):
        psutil.Process(self.SongID).kill()
        seekValue = int(input("\nEnter the starting position in seconds : "))

        sound = self.songSegment[seekValue*1000:]
        
        p1 = mp.Process(target=play, args=(sound,))
        p1.start()
        self.SongID = p1.pid


    def stop(self):
        psutil.Process(self.SongID).kill()

        self.SongID = None
        self.songName = None
        self.playlistLoopFlag = False
        self.loopflag = False
        self.songLoop = False
        self.selectSong()


    def loopSong(self, startSecond = 0, endSecond = 0):
        if 0 == endSecond:
            endSecond = self.songSegment.duration_seconds
            
        sound = self.songSegment[startSecond*1000: endSecond*1000]
        psutil.Process(self.SongID).kill()

        def __innerLoop(x):
            while self.loopflag:
                play(sound)
                
        l1 = mp.Process(target=__innerLoop, args=(5,))
        l1.start()
        self.SongID = l1.pid

    
    def loopAB(self):
        startSecond = int(input("\nEnter starting position in seconds : "))
        endSecond = int(input("\nEnter ending position in seconds : "))

        self.loopSong(startSecond, endSecond)


if __name__ == "__main__":
    music = Music()
    music.selectSong()
