import win32gui
import win32con
import win32api
import dearpygui.dearpygui as dpg
import ctypes
from ctypes import c_int
from pytube import YouTube
from plyer import notification
import re

def download_video(url, resolution):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4', resolution=resolution).first()
        if stream:
            stream.download()
            return True, None
        else:
            return False, "Video with the specified resolution not found."
    except Exception as e:
        return False, str(e)

def is_valid_youtube_url(url):
    pattern = r"^(https?://)?(www\.)?youtube\.com/watch\?v=[\w-]+(&\S*)?$"
    return re.match(pattern, url) is not None

def download_by_resolution(resolution):
    url = dpg.get_value("input_text")
    
    if not url:
        notification.notify(
            title='Download Error',
            message="Missing 'url' parameter.",
            app_name='TubeGui'
        )
        return

    if not is_valid_youtube_url(url):
        notification.notify(
            title='Download Error',
            message="Invalid YouTube URL.",
            app_name='TubeGui'
        )
        return
    
    success, error_message = download_video(url, resolution)
    if success:
        notification.notify(
            title='Download Complete',
            message="Video downloaded successfully.",
            app_name='TubeGui'
        )
    else:
        notification.notify(
            title='Download Error',
            message=error_message,
            app_name='TubeGui'
        )

dwm = ctypes.windll.dwmapi

dpg.create_context()

class MARGINS(ctypes.Structure):
    _fields_ = [("cxLeftWidth", c_int),
                ("cxRightWidth", c_int),
                ("cyTopHeight", c_int),
                ("cyBottomHeight", c_int)
               ]

# Get screen width and height
screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

# Set viewport size
viewport_width = 1000  # Increased width
viewport_height = 800  # Increased height

# Calculate position to center the viewport
viewport_x = (screen_width - viewport_width) // 2
viewport_y = (screen_height - viewport_height) // 2

dpg.create_viewport(title='overlay', width=viewport_width, height=viewport_height, x_pos=viewport_x, y_pos=viewport_y, always_on_top=True, decorated=False, clear_color=[0.0, 0.0, 0.0, 0.0])

dpg.set_viewport_always_top(True)
dpg.setup_dearpygui()

# Set window size
window_width = 415
window_height = 125

# Calculate position to center the window within the viewport
window_x = (viewport_width - window_width) // 2
window_y = (viewport_height - window_height) // 2

with dpg.window(label="Main Window", tag='main_win', no_resize=True, width=window_width, height=window_height, pos=(window_x, window_y), on_close=dpg.stop_dearpygui):
    dpg.add_input_text(label="", hint="'https://www.youtube.com/watch?v=xxxxxxxxxxx'", width=325, tag="input_text")
    dpg.add_same_line()
    dpg.add_button(label="Download", callback=lambda: download_by_resolution("720p"))

dpg.show_viewport()

# Make the window transparent
hwnd = win32gui.FindWindow(None, "overlay")
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(0, 0, 0), 0, win32con.LWA_COLORKEY)

dpg.start_dearpygui()
dpg.show_viewport()