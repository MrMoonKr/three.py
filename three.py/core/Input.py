import tkinter as tk

class Input(object):
    MOUSE_BUTTON_LEFT = 1
    MOUSE_BUTTON_MIDDLE = 2
    MOUSE_BUTTON_RIGHT = 3

    def __init__(self):
        self.keyDownList        = []
        self.keyPressedList     = set()
        self.keyUpList          = []
        self.mouseButtonDown    = False
        self.mouseButtonPressed = False
        self.mouseButtonUp      = False
        self.mouseButtonDownList = []
        self.mouseButtonPressedList = set()
        self.mouseButtonUpList  = []
        self.mouseWheel         = 0
        self.quitStatus         = False
        # did the window resize since the last update?
        self.windowResize       = False
        self.windowWidth        = None
        self.windowHeight       = None
        self.mousePosition      = (0, 0)

        self._pendingKeyDown    = []
        self._pendingKeyUp      = []
        self._pendingResize     = None
        self._pendingMouseDown  = []
        self._pendingMouseUp    = []
        self._pendingMouseWheel = 0

    def attach(self, widget: tk.Misc) -> None:
        widget.bind("<Map>", self._focusWidget, add="+")
        widget.bind("<Enter>", self._focusWidget, add="+")
        widget.bind("<KeyPress>", self._onKeyDown, add="+")
        widget.bind("<KeyRelease>", self._onKeyUp, add="+")
        widget.bind("<ButtonPress>", self._onMouseDown, add="+")
        widget.bind("<ButtonRelease>", self._onMouseUp, add="+")
        widget.bind("<MouseWheel>", self._onMouseWheel, add="+")
        widget.bind("<Motion>", self._onMouseMove, add="+")
        widget.bind("<Configure>", self._onResize, add="+")

    def update(self):
        self.keyDownList = []
        self.keyUpList   = []
        self.mouseButtonDown = False
        self.mouseButtonUp   = False
        self.mouseButtonDownList = []
        self.mouseButtonUpList = []
        self.mouseWheel = 0
        self.windowResize    = False
        self.keyDownList = self._pendingKeyDown
        self.keyUpList = self._pendingKeyUp
        self.mouseButtonDownList = self._pendingMouseDown
        self.mouseButtonUpList = self._pendingMouseUp
        self.mouseWheel = self._pendingMouseWheel
        self.mouseButtonDown = len(self.mouseButtonDownList) > 0
        self.mouseButtonUp = len(self.mouseButtonUpList) > 0

        self._pendingKeyDown = []
        self._pendingKeyUp = []
        self._pendingMouseDown = []
        self._pendingMouseUp = []
        self._pendingMouseWheel = 0

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

    def isMouseDown(self, buttonCode=None):
        if buttonCode is None:
            return self.mouseButtonDown
        return buttonCode in self.mouseButtonDownList

    def isMousePressed(self, buttonCode=None):
        if buttonCode is None:
            return self.mouseButtonPressed
        return buttonCode in self.mouseButtonPressedList

    def isMouseUp(self, buttonCode=None):
        if buttonCode is None:
            return self.mouseButtonUp
        return buttonCode in self.mouseButtonUpList

    def getMousePosition(self):
        return self.mousePosition

    def getMouseDownList(self):
        return self.mouseButtonDownList

    def getMousePressedList(self):
        return self.mouseButtonPressedList

    def getMouseUpList(self):
        return self.mouseButtonUpList

    def getMouseWheel(self):
        return self.mouseWheel

    def isMouseWheelUp(self):
        return self.mouseWheel > 0

    def isMouseWheelDown(self):
        return self.mouseWheel < 0

    def quit(self):
        return self.quitStatus
    
    def resize(self):
        return self.windowResize
        
    def getWindowSize(self):
        return { "width": self.windowWidth, "height": self.windowHeight }

    def setQuit(self, status):
        self.quitStatus = status

    def _focusWidget(self, event: tk.Event) -> None:
        event.widget.focus_set()

    def _onKeyDown(self, event: tk.Event) -> None:
        key = event.keysym
        if key not in self.keyPressedList:
            self.keyPressedList.add(key)
            self._pendingKeyDown.append(key)

    def _onKeyUp(self, event: tk.Event) -> None:
        key = event.keysym
        self.keyPressedList.discard(key)
        self._pendingKeyUp.append(key)

    def _onMouseDown(self, event: tk.Event) -> None:
        button = event.num
        if button == 4 or button == 5:
            self._queueMouseWheelFromButton(event)
            return
        self.mousePosition = (event.x, event.y)
        if button not in self.mouseButtonPressedList:
            self.mouseButtonPressedList.add(button)
            self._pendingMouseDown.append(button)
        self.mouseButtonPressed = len(self.mouseButtonPressedList) > 0

    def _onMouseUp(self, event: tk.Event) -> None:
        button = event.num
        if button == 4 or button == 5:
            return
        self.mousePosition = (event.x, event.y)
        self.mouseButtonPressedList.discard(button)
        self._pendingMouseUp.append(button)
        self.mouseButtonPressed = len(self.mouseButtonPressedList) > 0

    def _onMouseWheel(self, event: tk.Event) -> None:
        self.mousePosition = (event.x, event.y)
        delta = event.delta
        if delta == 0:
            return
        if abs(delta) >= 120:
            delta = int(delta / 120)
        else:
            delta = 1 if delta > 0 else -1
        self._pendingMouseWheel += delta

    def _onMouseMove(self, event: tk.Event) -> None:
        self.mousePosition = (event.x, event.y)

    def _onResize(self, event: tk.Event) -> None:
        self._pendingResize = (event.width, event.height)

    def _queueMouseWheelFromButton(self, event: tk.Event) -> None:
        self.mousePosition = (event.x, event.y)
        if event.num == 4:
            self._pendingMouseWheel += 1
        elif event.num == 5:
            self._pendingMouseWheel -= 1
