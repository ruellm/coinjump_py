import time
import math

class Timer:
    def __init__(self):
        self._startTime = 0
        self._fbCallBack = None
        self._timeTrigger = 0; # in milliseconds
        self._elapsed = 0;  # in seconds
        self._isRunning = False

        # for time tick callback
        self._tickTrigger = 0  # in milleseconds
        self._tickCache = 0
        self._fbTickCallBack = None

        # for pause implementation
        self.cachedTime = 0
    
    def Start(self):
        self._startTime = time.time()
        self._isRunning = True

    def Stop(self):
        self._isRunning = False
    
    def Pause(self):
        self._isRunning = False
        self.cachedTime = self._elapsed
    
    def Resume(self):
        if self._isRunning == True :
            return
        
        self.Start()
    
    def Update(self):
        if self._isRunning is not True:
            return
        
        currTime = time.time()
        self._elapsed = (currTime - self._startTime)
        self._elapsed += self.cachedTime

    def format_str(self) -> str:
        str_result = ""
        floored = math.floor(self._elapsed)

        minute = math.floor(floored / 60)
        sec = floored % 60

        if sec < 10 :
            sec = "0" + str(sec)

        if minute < 10:
            minute = "0" + str(minute)

        strResult = minute + " : " + sec
        return str_result
    