# DESIGN

## Goal

- Remove `pygame`
- Move runtime to `pyopengltk + tkinter + PyOpenGL`
- Keep the existing `Base` inheritance model for examples

## Runtime Structure

- `Base` directly inherits `OpenGLFrame`
- Each example implements `initialize()` and `update()` by inheriting `Base`
- Each runnable file defines its own local `GLApp(tk.Tk)`
- `GLApp` creates the example instance as `self.base = TestXxx(self)`
- Entry points use `main() -> None` and `if __name__ == "__main__": main()`

## Rendering Loop

- OpenGL context creation is handled by `pyopengltk.OpenGLFrame`
- `Base.initgl()` performs one-time scene initialization
- `Base.redraw()` performs per-frame updates and rendering
- Frame scheduling currently uses `pyopengltk` timer mode with `self.animate = 1`
- This is timer-driven, not `after_idle(...)`

## Windowing

- `tkinter` owns the top-level window and main loop
- `Base` provides:
  - `setWindowTitle()`
  - `setWindowSize()`
  - `centerWindow()`
- Shutdown uses `WM_DELETE_WINDOW` plus the internal `running` flag

## Input

- `Input` uses `tkinter` event bindings instead of `pygame.event`
- Supported input:
  - keyboard
  - mouse button and mouse move
  - resize
- Existing query style is kept:
  - `isKeyDown()`
  - `isKeyPressed()`
  - `isMouseDown()`
  - `resize()`
  - `getWindowSize()`

## Images And Text

- Texture loading moved from `pygame.image` to `Pillow`
- `OpenGLUtils.initializeTexture()`, `initializeSurface()`, and `updateSurface()` accept `PIL.Image` or `numpy` buffers
- `TextImage` now uses `Pillow.ImageDraw` and `ImageFont`
- Korean text works when the selected font file contains Korean glyphs

## Example Conventions

- `Test*.py` files follow one common runnable pattern
- Each file defines:
  - one `Base` subclass
  - one local `GLApp(tk.Tk)`
  - one `main()` function
- `TestCube.py` was added
- `TestTextImage.py` includes D2Coding Korean text and FPS HUD examples

## Compatibility Fixes

- `numpy 2.x` compatibility:
  - removed `Matrix.itemset()`
  - replaced with direct indexed assignment
- Collision example fixes:
  - corrected `intersectSphere()` call name
  - added zero-distance guard for overlapping sphere centers

## Validation

- Full Python compile check completed
- `Test*.py` direct execution smoke tests completed
- Test-only environment variables:
  - `THREEPY_SMOKE_FRAMES`
  - `THREEPY_SMOKE_TIMEOUT_MS`
