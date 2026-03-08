import os
import time
import tkinter as tk
from pathlib import Path

from OpenGL.GL import GL_PACK_ALIGNMENT, GL_RGBA, GL_UNSIGNED_BYTE, glPixelStorei, glReadPixels
from PIL import Image
from pyopengltk import OpenGLFrame

from core.Input import Input


class Base(OpenGLFrame):

    def __init__(self, master):
        self.screenSize = (900, 600)
        self.deltaTime = 0
        self.input = Input()
        self.running = True

        self._initialized = False
        self._lastTime = None
        self._currentFps = 0
        self._pendingScreenshot = None
        self._iconImage = None
        self._smokeFrameLimit = int(os.environ.get("THREEPY_SMOKE_FRAMES", "0") or "0")
        self._smokeTimeoutMs = int(os.environ.get("THREEPY_SMOKE_TIMEOUT_MS", "0") or "0")
        self._frameCount = 0
        self._initializationError = None

        super().__init__(master, width=self.screenSize[0], height=self.screenSize[1])
        self.animate = 1
        self.pack(fill="both", expand=True)
        self.focus_set()

        self.input.attach(self)
        self.winfo_toplevel().protocol("WM_DELETE_WINDOW", self._requestQuit)

        self.setWindowTitle("   ")
        self.setWindowSize(640, 640)
        self._setWindowIcon()

        if self._smokeTimeoutMs > 0:
            self.after(self._smokeTimeoutMs, self._requestQuit)

    def setWindowTitle(self, text):
        self.winfo_toplevel().title(text)

    def setWindowSize(self, width, height):
        self.screenSize = (width, height)
        self.configure(width=width, height=height)
        self.winfo_toplevel().geometry(f"{width}x{height}")

    def centerWindow(self):
        window = self.winfo_toplevel()
        window.update_idletasks()

        width, height = self.screenSize
        screenWidth = window.winfo_screenwidth()
        screenHeight = window.winfo_screenheight()

        x = max((screenWidth - width) // 2, 0)
        y = max((screenHeight - height) // 2, 0)
        window.geometry(f"{width}x{height}+{x}+{y}")

    def initialize(self):
        pass

    def update(self):
        pass

    def initgl(self):
        self._initializeContext()

    def redraw(self):
        self._renderFrame()

    def saveScreenshot(self, fileName=None):
        if fileName is None:
            timeString = str(int(1000 * time.time()))
            fileName = "image-" + timeString + ".png"
        self._pendingScreenshot = fileName
        return fileName

    def _setWindowIcon(self):
        iconPath = Path(__file__).resolve().parent.parent / "images" / "icon.png"
        if not iconPath.exists():
            return
        try:
            self._iconImage = tk.PhotoImage(file=str(iconPath))
            self.winfo_toplevel().iconphoto(True, self._iconImage)
        except tk.TclError:
            self._iconImage = None

    def _initializeContext(self):
        if self._initialized:
            return
        try:
            self.initialize()
            self._lastTime = time.perf_counter()
            self._initialized = True
        except Exception as error:
            self._initializationError = error
            self.running = False
            self.after_idle(self.winfo_toplevel().destroy)
            raise

    def _renderFrame(self):
        if self._initializationError is not None:
            self.running = False
            self.after_idle(self.winfo_toplevel().destroy)
            return

        if not self.running:
            self.after_idle(self.winfo_toplevel().destroy)
            return

        self.input.update()

        if self.input.quit():
            self.running = False
            self.after_idle(self.winfo_toplevel().destroy)
            return

        currentTime = time.perf_counter()
        if self._lastTime is None:
            self._lastTime = currentTime
        self.deltaTime = currentTime - self._lastTime
        self._lastTime = currentTime
        if self.deltaTime > 0:
            self._currentFps = 1.0 / self.deltaTime

        ctrlPressed = self.input.isKeyPressed("Control_L") or self.input.isKeyPressed("Control_R")

        if ctrlPressed and self.input.isKeyDown("f"):
            print("FPS: " + str(int(self._currentFps)))

        if ctrlPressed and self.input.isKeyDown("s"):
            fileName = self.saveScreenshot()
            print("Image saved to: " + fileName)

        self.update()
        self._frameCount += 1

        if self._smokeFrameLimit > 0 and self._frameCount >= self._smokeFrameLimit:
            self.running = False

        if self._pendingScreenshot is not None:
            self._captureScreenshot(self._pendingScreenshot)
            self._pendingScreenshot = None

    def _captureScreenshot(self, fileName):
        width = max(1, self.winfo_width())
        height = max(1, self.winfo_height())
        glPixelStorei(GL_PACK_ALIGNMENT, 1)
        pixelData = glReadPixels(0, 0, width, height, GL_RGBA, GL_UNSIGNED_BYTE)
        image = Image.frombytes("RGBA", (width, height), pixelData)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        image.save(fileName)

    def _requestQuit(self):
        self.input.setQuit(True)
        self.running = False


class BaseApp(tk.Tk):

    def __init__(self, baseClass=Base):
        super().__init__()
        self.base = baseClass(self)
