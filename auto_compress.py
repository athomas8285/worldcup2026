"""Auto-compress images dropped into prize-photos folder.
Run once, stays alive, monitors prize-photos/** and compresses new images.
Ctrl+C to stop."""
import os, sys, time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PIL import Image

WATCH_DIR = os.path.dirname(os.path.abspath(__file__))
PHOTOS_DIR = os.path.join(WATCH_DIR, "prize-photos")
TARGET_WIDTH = 800
QUALITY = 75
MIN_SIZE = 80 * 1024  # Only compress files > 80KB

class ImageHandler(FileSystemEventHandler):
    def on_created(self, event):
        self._compress(event.src_path)
    
    def on_modified(self, event):
        self._compress(event.src_path)
    
    def _compress(self, path):
        if not path.lower().endswith(('.jpg', '.jpeg', '.png')):
            return
        if not os.path.exists(path):
            return
        # Wait a moment for file to be fully written
        time.sleep(0.5)
        try:
            size_before = os.path.getsize(path)
            if size_before <= MIN_SIZE:
                return
            img = Image.open(path)
            w, h = img.size
            if w > TARGET_WIDTH or h > TARGET_WIDTH:
                img.thumbnail((TARGET_WIDTH, TARGET_WIDTH), Image.LANCZOS)
            img.save(path, quality=QUALITY, optimize=True)
            size_after = os.path.getsize(path)
            pct = (1 - size_after / size_before) * 100
            print(f"[compress] {os.path.basename(path)}: {size_before//1024}KB -> {size_after//1024}KB (-{pct:.0f}%)")
        except Exception as e:
            print(f"[compress] {os.path.basename(path)}: ERROR {e}")

if __name__ == "__main__":
    print(f"Watching {PHOTOS_DIR}")
    print("Drop images into prize-photos/ — auto-compressed on arrival. Ctrl+C to stop.")
    handler = ImageHandler()
    observer = Observer()
    observer.schedule(handler, PHOTOS_DIR, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
