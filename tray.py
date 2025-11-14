# tray.py
import pystray
from PIL import Image
import threading
import sys

def create_tray(root, icon_path='icon.ico'):
    def show_window(icon, item):
        icon.stop()
        root.after(0, root.deiconify)

    def on_exit(icon, item):
        icon.stop()
        root.quit()

    def setup_tray():
        img = Image.open(icon_path)
        menu = pystray.Menu(
            pystray.MenuItem('显示', show_window),
            pystray.MenuItem('退出', on_exit)
        )
        tray = pystray.Icon('记账本', img, menu=menu)
        tray.run()

    root.withdraw()                                 # 启动即隐藏
    threading.Thread(target=setup_tray, daemon=True).start()