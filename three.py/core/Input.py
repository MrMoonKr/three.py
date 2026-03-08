class Input(object):

    def __init__(self):
        self.keyDownList     = []
        self.keyPressedList  = set()
        self.keyUpList       = []
        self.mouseButtonDown    = False
        self.mouseButtonPressed = False
        self.mouseButtonUp      = False
        self.quitStatus         = False
        # did the window resize since the last update?
        self.windowResize       = False
        self.windowWidth        = None
        self.windowHeight       = None
        self.mousePosition      = (0, 0)

        self._pendingKeyDown    = []
        self._pendingKeyUp      = []
        self._pendingResize     = None
        self._pendingMouseDown  = False
        self._pendingMouseUp    = False

    def attach(self, widget):
        widget.bind("<Map>", self._focusWidget, add="+")
        widget.bind("<Enter>", self._focusWidget, add="+")
        widget.bind("<KeyPress>", self._onKeyDown, add="+")
        widget.bind("<KeyRelease>", self._onKeyUp, add="+")
        widget.bind("<ButtonPress>", self._onMouseDown, add="+")
        widget.bind("<ButtonRelease>", self._onMouseUp, add="+")
        widget.bind("<Motion>", self._onMouseMove, add="+")
        widget.bind("<Configure>", self._onResize, add="+")

    def update(self):
        self.keyDownList = []
        self.keyUpList   = []
        self.mouseButtonDown = False
        self.mouseButtonUp   = False
        self.windowResize    = False
        self.keyDownList = self._pendingKeyDown
        self.keyUpList = self._pendingKeyUp
        self.mouseButtonDown = self._pendingMouseDown
        self.mouseButtonUp = self._pendingMouseUp

        self._pendingKeyDown = []
        self._pendingKeyUp = []
        self._pendingMouseDown = False
        self._pendingMouseUp = False

        if self._pendingResize is not None:
            self.windowResize = True
            self.windowWidth, self.windowHeight = self._pendingResize
            self._pendingResize = None

    def isKeyDown(self, keyCode):
        return keyCode in self.keyDownList
    
    def isKeyPressed(self, keyCode):
        return keyCode in self.keyPressedList

    def isKeyUp(self, keyCode):
        return keyCode in self.keyUpList

    def isMouseDown(self):
        return self.mouseButtonDown

    def isMousePressed(self):
        return self.mouseButtonPressed

    def isMouseUp(self):
        return self.mouseButtonUp

    def getMousePosition(self):
        return self.mousePosition

    def quit(self):
        return self.quitStatus
    
    def resize(self):
        return self.windowResize
        
    def getWindowSize(self):
        return { "width": self.windowWidth, "height": self.windowHeight }

    def setQuit(self, status):
        self.quitStatus = status

    def _focusWidget(self, event):
        event.widget.focus_set()

    def _onKeyDown(self, event):
        key = event.keysym
        if key not in self.keyPressedList:
            self.keyPressedList.add(key)
            self._pendingKeyDown.append(key)

    def _onKeyUp(self, event):
        key = event.keysym
        self.keyPressedList.discard(key)
        self._pendingKeyUp.append(key)

    def _onMouseDown(self, event):
        self.mousePosition = (event.x, event.y)
        self.mouseButtonPressed = True
        self._pendingMouseDown = True

    def _onMouseUp(self, event):
        self.mousePosition = (event.x, event.y)
        self.mouseButtonPressed = False
        self._pendingMouseUp = True

    def _onMouseMove(self, event):
        self.mousePosition = (event.x, event.y)

    def _onResize(self, event):
        self._pendingResize = (event.width, event.height)
