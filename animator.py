class Animator:
    def __init__(self):
        self._fps = 0
        self._timeBetweenFrames = 0
        self._timeSinceLastFrame = 0
    
    def Set(self, fps):
        self._fps = fps
        self._timeBetweenFrames = 1.0 / fps
        self._timeSinceLastFrame = self._timeBetweenFrames
    
    def Update(self, elapsed) -> bool :
        self._timeSinceLastFrame -= elapsed
        if self._timeSinceLastFrame <= 0 :
            self._timeSinceLastFrame = self._timeBetweenFrames
            return True
        
        return False