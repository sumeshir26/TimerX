# TimerX v0.2 by sumeshir26
# IMPORTS
ver = "0.9"

from time import sleep
from tkinter import *
from tkinter import ttk
import tkinter
from tkinter.constants import  LEFT
from playsound import playsound
from threading import  Thread
from platform import system
import os
from utils import *
import webbrowser
"""
# Disabled by default due to module unavailability on Linux
from BlurWindow.blurWindow import GlobalBlur, blur
"""
import darkdetect

from tkinter.messagebox import showinfo

# CONFIG

theme = f"{darkdetect.theme()}"

if not os.path.isfile("./config.json"):
    from utils import *
    createConfig()
    config = loadConfig()

else:
    config = loadConfig()

if config['theme'] == "System":
    if darkdetect.theme() == "dark":
        theme = "Dark"
    elif darkdetect.theme() == "light":
        theme = "Light"
elif config['theme'] == "Dark":
    theme = "Dark"
else:
    theme = "Light"

# TKINTER WINDOW
app = Tk()
app.title('TimerX')
app.geometry("300x210")
app.minsize(width=300, height=210)
app.maxsize(width=512, height=400)
app.update()
"""
# Disabled by default
HWND = ctypes.windll.user32.GetForegroundWindow()
GlobalBlur(HWND)
blur(HWND, hexColor='#12121240')
"""
# SYSTEM CODE
try:
    if  system() == "darwin":
        app.iconbitmap(r'assets/logo_new.icns')
        app.wm_attributes("-transparent", True)
        app.config(bg="systemTransparent")
    elif  system() == "Windows":
        app.iconbitmap(r'assets/logo_new.ico')
        from win10toast_click import ToastNotifier 
    elif  system() == "win":
        app.iconphoto(r'assets/logo_new.ico')
    else:
        logo_img = PhotoImage(file = 'assets/images/logo_new.png')
        app.iconphoto(False, logo_img)
except TclError:
    pass
    try:
        app.iconphoto(r'assets/logo.ico')
    except TclError:
        pass

# VARIABLES
app_on = True

timer_on = False
timer_paused = False

timer_seconds = 5
timer_minutes = 0
timer_hours = 0

# FUNCTIONS
def playBuzzer():
    playsound(r".\assets\sounds\sound1.wav")

def startstopButtonPressed():
    global timer_on, timer_paused
    if timer_on:
        timer_on = False
        timer_paused = True
        play_button.configure(text = "Play")
    elif timer_paused == False and timer_on == False:
        play_button.configure(text = "Pause")
        timer_thread = Thread(target=runTimer, daemon=True)
        timer_thread.start()
    else:
        timer_paused = False

def saveTimer(timer_sec_input, timer_min_input, timer_hr_input, manager_app_window):
    global timer_seconds, timer_minutes, timer_hours

    try:
        timer_seconds = int(timer_sec_input.get())
        timer_minutes = int(timer_min_input.get())
        timer_hours = int(timer_hr_input.get())
        time_selected_display.configure(text = f'{timer_hours} Hours, {timer_minutes} Minutes, {timer_seconds} Seconds')
        time_display.configure(text = f'{timer_hours} : {timer_minutes} : {timer_seconds}')
        manager_app_window.destroy()
    except ValueError:
        time_selected_display.configure(text = "Please enter a number!")

def showNotification():
    if  system() == "Windows":
        notification = ToastNotifier()
        notification.show_toast(
        "TimerX", 
        "Time's up!", 
        icon_path='./assets/logo.ico', 
        duration='None', 
        threaded=True,
        callback_on_click= app.focus_force(),
        title='TimerX'
        )

def runTimer():
    global timer_seconds, timer_minutes, timer_hours, timer_on, app, config

    seconds_left = timer_seconds
    minutes_left = timer_minutes
    hours_left = timer_hours
    timer_on = True

    while True:
        if  timer_on and timer_paused == False:
            time_display.configure(text = f'{hours_left} : {minutes_left} : {seconds_left}')
            if seconds_left == 0 and minutes_left != 0:
                minutes_left -= 1
                seconds_left = 59
            elif seconds_left == 0 and minutes_left == 0 and hours_left != 0:
                hours_left -= 1
                minutes_left = 59
                seconds_left = 59
            elif seconds_left == 0 and timer_minutes == 0 and hours_left == 0:
                break
            else:
                seconds_left -= 1
            sleep(1)

        else:
            time_display.configure(text = f'{hours_left} : {minutes_left} : {seconds_left}')

    timer_on = False
    time_display.configure(text = f'{hours_left} : {minutes_left} : {seconds_left}')
    play_button.config(text = "Play")

    if config['notify']:
        showNotification()
    if config['sound']:
        playBuzzer()

def setAlwaysOnTop(app):
    global config
    if  config['ontop'] == True:
        app.attributes('-topmost', True)
    else:
        app.attributes('-topmost', False)

setAlwaysOnTop(app)

#WINDOWS

def createManagerWindow(saveTimer, current_mins, current_secs, current_hrs):
    global manager_app_window, config
    manager_app_window = tkinter.Toplevel()
    manager_app_window.geometry('250x170')
    manager_app_window.title('Edit Timer')
    manager_app_window.attributes("-alpha", config['transperency'])

    manager_app_window.resizable(False, False)

    try:
        if system() == "darwin":
            manager_app_window.iconbitmap(r'assets/logo_new.icns')
            manager_app_window.wm_attributes("-transparent", True)
            manager_app_window.config(bg="systemTransparent")
        elif  system() == "Windows":
            manager_app_window.iconbitmap(r'assets/logo_new.ico')
        elif  system() == "win":
            manager_app_window.iconphoto(r'assets/logo_new.ico')
        else:
            logo_img = PhotoImage(file = 'assets/images/logo.png')
            manager_app_window.iconphoto(False, logo_img)
    except TclError:
        pass

    # WINDOW FRAME
    manager_window = ttk.Frame(manager_app_window)
    manager_window.pack(fill="both", expand=True)

    timer_hr_label = ttk.Label(manager_window, text = 'Hours: ')
    timer_hr_label.place(x=17, y=17)
    timer_hr_input = ttk.Entry(manager_window)
    timer_hr_input.place(x=65, y=10)
    timer_hr_input.insert(1, current_hrs)

    timer_min_label = ttk.Label(manager_window, text = 'Minutes: ')
    timer_min_label.place(x=13, y=57)
    timer_min_input = ttk.Entry(manager_window)
    timer_min_input.place(x=65, y=50)
    timer_min_input.insert(1, current_mins)

    timer_sec_label = ttk.Label(manager_window, text = 'Seconds: ')
    timer_sec_label.place(x=12, y=97)
    timer_sec_input = ttk.Entry(manager_window)
    timer_sec_input.place(x=65, y=90)
    timer_sec_input.insert(1, current_secs)

    ok_button = ttk.Button(manager_window, text = 'Ok!', command = lambda:saveTimer(timer_sec_input, timer_min_input, timer_hr_input, manager_app_window), style="Accent.TButton")
    ok_button.place(x=95, y=126)

def createAboutWindow():
    settings_window.destroy()

    about_window = tkinter.Toplevel()
    about_window.geometry("420x240")
    about_window.resizable(False, False)
    about_window.attributes('-topmost', True)

    try:
        if system() == "darwin":
            about_window.iconbitmap(r'assets/logo_new.icns')
            about_window.wm_attributes("-transparent", True)
            about_window.config(bg="systemTransparent")
        elif  system() == "Windows":
            about_window.iconbitmap(r'assets/logo_new.ico')
        elif  system() == "win":
            about_window.iconphoto(r'assets/logo_new.ico')
        else:
            logo_img = PhotoImage(file = 'assets/images/logo.png')
            about_window.iconphoto(False, logo_img)
    except TclError:
        pass

    logo = PhotoImage(file="./assets/logo_new_150x150.png")
    logo_label = ttk.Label(about_window, image=logo)
    logo_label.place(x=10, y=10)

    github_logo_dark = PhotoImage(file="./assets/images/dark/github.png")
    github_logo_light = PhotoImage(file="./assets/images/light/github.png")

    globe_dark = PhotoImage(file="./assets/images/dark/globe.png")
    globe_light = PhotoImage(file="./assets/images/light/globe.png")

    TimerX_Label = ttk.Label(about_window, text="TimerX", font=("Arial Rounded MT Bold", 50))
    TimerX_Label.place(x=170, y=20)

    version_Label = ttk.Label(about_window, text=f"Version: {ver}", font=("Segoe UI" ,"20"))
    version_Label.place(x=180, y=100)

    github_btn = ttk.Button(about_window, text=" Fork on Github", image=github_logo_dark, compound=LEFT, command=lambda:webbrowser.open("https://github.com/sumeshir26/TimerX"))
    github_btn.place(x=40, y=180)

    website_btn = ttk.Button(about_window, text=" Check out our Website!", image=globe_dark, compound=LEFT)
    website_btn.place(x=190, y=180)

    if theme == "Dark":
        github_btn.configure(image=github_logo_dark)
        website_btn.configure(image=globe_dark)
    elif theme == "Light":
        github_btn.configure(image=github_logo_light)
        website_btn.configure(image=globe_light)
    elif theme == "System":
        if darkdetect.theme() == "Dark":
            github_btn.configure(image=github_logo_dark)
            website_btn.configure(image=globe_dark)
        elif darkdetect.theme() == "Light":
            github_btn.configure(image=github_logo_light)
            website_btn.configure(image=globe_light)

    about_window.mainloop()

def createSettingsWindow():
    global theme, config, settings_window

    settings_window = tkinter.Toplevel()
    settings_window.geometry('500x320')
    settings_window.title('Settings')
    settings_window.resizable(False, False)
    settings_window.attributes("-alpha", config['transperency'])

    try:
        if system() == "darwin":
            settings_window.iconbitmap(r'assets/logo_new.icns')
            settings_window.wm_attributes("-transparent", True)
            settings_window.config(bg="systemTransparent")
        elif  system() == "Windows":
            settings_window.iconbitmap(r'assets/logo_new.ico')
        elif  system() == "win":
            settings_window.iconphoto(r'assets/logo_new.ico')
        else:
            logo_img = PhotoImage(file = 'assets/images/logo_new.png')
            settings_window.iconphoto(False, logo_img)
    except TclError:
        pass

    theme_dark = PhotoImage(file="./assets/images/dark/dark_theme.png")
    theme_light = PhotoImage(file="./assets/images/light/dark_theme.png")

    transparency_dark = PhotoImage(file="./assets/images/dark/transparency.png")
    transparency_light = PhotoImage(file="./assets/images/light/transparency.png")

    speaker_dark = PhotoImage(file="./assets/images/dark/speaker.png")
    speaker_light = PhotoImage(file="./assets/images/light/speaker.png")

    bell_dark = PhotoImage(file="./assets/images/dark/bell.png")
    bell_light = PhotoImage(file="./assets/images/light/bell.png")

    pin_dark = PhotoImage(file="./assets/images/dark/pin.png")
    pin_light = PhotoImage(file="./assets/images/light/pin.png")

    info_dark = PhotoImage(file="./assets/images/dark/info.png")
    info_light = PhotoImage(file="./assets/images/light/info.png")


    theme_label = ttk.Label(settings_window, text="  Change theme of the app", image=theme_dark, compound=LEFT)
    theme_label.place(x=23, y=23)

    transparency_label = ttk.Label(settings_window, text="  Adjust Transparency of the app", image=transparency_dark, compound=LEFT)
    transparency_label.place(x=23, y=73)

    speaker_label = ttk.Label(settings_window, text="  Play sound when timer ends", image=speaker_dark, compound=LEFT)
    speaker_label.place(x=23, y=123)

    bell_label = ttk.Label(settings_window, text="  Show notification when timer ends", image=bell_dark, compound=LEFT)
    bell_label.place(x=23, y=173)

    pin_label = ttk.Label(settings_window, text="  Keep app always on top", image=pin_dark, compound=LEFT)
    pin_label.place(x=23, y=223)

    about_btn = ttk.Button(master=settings_window, image=info_dark, command=lambda:createAboutWindow(), style="Toolbutton")
    about_btn.place(x=5, y=273)

    if theme == "Dark":
        theme_label.configure(image=theme_dark)
        transparency_label.configure(image=transparency_dark)
        speaker_label.configure(image=speaker_dark)
        bell_label.configure(image=bell_dark)
        pin_label.configure(image=pin_dark)
        about_btn.configure(image=info_dark)
    else:
        theme_label.configure(image=theme_light)
        transparency_label.configure(image=transparency_light)
        speaker_label.configure(image=speaker_light)
        bell_label.configure(image=bell_light)
        pin_label.configure(image=pin_light)
        about_btn.configure(image=info_light)
    if theme == "System":
        if darkdetect.theme() == "Dark":
            theme_label.configure(image=theme_dark)
            transparency_label.configure(image=transparency_dark)
            speaker_label.configure(image=speaker_dark)
            bell_label.configure(image=bell_dark)
            pin_label.configure(image=pin_dark)
            about_btn.configure(image=info_dark)
        elif darkdetect.theme() == "Light":
            theme_label.configure(image=theme_light)
            transparency_label.configure(image=transparency_light)
            speaker_label.configure(image=speaker_light)
            bell_label.configure(image=bell_light)
            pin_label.configure(image=pin_light)
            about_btn.configure(image=info_light)

    box_slider_value= StringVar(settings_window)

    if config['theme'] == 'System':
        box_slider_value.set("System")    
    elif theme == "Dark":
        box_slider_value.set("Dark")
    elif theme == "Light":
        box_slider_value.set("Light")

    theme_combobox = ttk.Spinbox(settings_window, state="readonly", values=("Dark", "Light", "System"), wrap=True, textvariable=box_slider_value)
    theme_combobox.place(x=275, y=20)

    slider_value = tkinter.DoubleVar()

    didsliderload = False

    def slider_value():
        return  ".{:.0f}".format(slider.get())

    def slider_changed(event):
        if didsliderload:
            settings_window.attributes("-alpha", slider_value())
            app.attributes("-alpha", slider_value())

    slider = ttk.Scale(settings_window, from_=25, to=99, orient="horizontal", command=slider_changed, variable=slider_value)
    slider.set(str(config['transperency']).lstrip("."))
    slider.place(x=325, y=75)

    didsliderload = True

    sound_button = ttk.Checkbutton(settings_window, style="Switch.TCheckbutton")
    if config['sound'] == True:
        sound_button.state(['!alternate', 'selected'])
    elif config['sound'] == False:
        sound_button.state(['!alternate'])
    sound_button.place(x=360, y=125)

    notify_button = ttk.Checkbutton(settings_window, style="Switch.TCheckbutton")
    if config['notify'] == True:
        notify_button.state(['!alternate', 'selected'])
    elif config['notify'] == False:
        notify_button.state(['!alternate'])
    notify_button.place(x=360, y=175)

    ###

    ontop_button = ttk.Checkbutton(settings_window, style="Switch.TCheckbutton")
    if config['ontop'] == True:
        ontop_button.state(['!alternate', 'selected'])
    elif config['ontop'] == False:
        ontop_button.state(['!alternate'])
    ontop_button.place(x=360, y=215)

    def ApplyChanges():
        global theme

        config['theme'] = theme_combobox.get()
        theme = config['theme']
        config['transperency'] = slider_value()
        config['sound'] = sound_button.instate(['selected'])
        config['notify'] = notify_button.instate(["selected"])
        config['ontop'] = ontop_button.instate(["selected"])
        setAlwaysOnTop(app)
        
        setConfig(config)

        if theme == "Dark":
            app.tk.call("set_theme", "dark")
            settings_btn.configure(image=settings_image_dark)
        elif theme == "Light":
            app.tk.call("set_theme", "light")
            settings_btn.configure(image=settings_image_light)
        elif theme == "System":
            if darkdetect.theme() == "Dark":
                settings_btn.configure(image=settings_image_dark)
                app.tk.call("set_theme", "dark")
            elif darkdetect.theme() == "Light":
                settings_btn.configure(image=settings_image_light)
                app.tk.call("set_theme", "light")
       
        settings_window.destroy()

    okbtn = ttk.Button(settings_window, text="Apply Changes", command=lambda:ApplyChanges(), style="Accent.TButton")
    okbtn.place(x=250, y=270)

    cancelbtn = ttk.Button(settings_window, text="Cancel", command=lambda:settings_window.destroy()) 
    cancelbtn.place(x=125, y=270)

    settings_window.mainloop() 

# APP THEME
app.attributes("-alpha", config['transperency'])

app.tk.call("source", "sun-valley.tcl")
app.tk.call("set_theme", f"{theme.lower()}")
if theme == "System":
    if darkdetect.theme() == "Dark":
        app.tk.call("set_theme", "dark")
    elif darkdetect.theme() == "Light":
        app.tk.call("set_theme", "light")

#KEYBINDS
app.bind('key-space', startstopButtonPressed)

#GRID CONFIGURE
Grid.rowconfigure(app, 0, weight=1)
Grid.columnconfigure(app, 1, weight=1)
Grid.rowconfigure(app, 2, weight=1)

# IMAGES
settings_image_light = PhotoImage(file=f"./assets/images/light/settings.png")
settings_image_dark = PhotoImage(file=f"./assets/images/dark/settings.png")

# WINDOW ELEMENTS
time_selected_display = ttk.Label(master = app, text = f'{timer_hours} Hours, {timer_minutes} Minutes, {timer_seconds} Seconds')
time_selected_display.grid(column=1, row=0, sticky="N", pady=10)

time_display = ttk.Label(master = app, text = f'{timer_hours} : {timer_minutes} : {timer_seconds}', font = ("Segoe UI Variable", 30))
time_display.grid(column=1, row=0, sticky="", rowspan=2, pady=20)

play_button = ttk.Button(master = app, text = "Play", width = 25, command = startstopButtonPressed, style="Accent.TButton")
play_button.grid(column=1, row=0, sticky="S", rowspan=2)

manager_button = ttk.Button(master = app, text = 'Edit Timer', command = lambda: createManagerWindow(saveTimer, timer_minutes, timer_seconds, timer_hours), width = 25)
manager_button.grid(column=1, row=2, sticky="N", pady=10)

settings_btn = ttk.Button(master=app, image=settings_image_dark, command=lambda:createSettingsWindow(), style="Toolbutton")

#RESIZING
def sizechanged(e):
    settings_btn.place(x=5, y=app.winfo_height() - 45)
    if app.winfo_height() >= 220:
        if app.winfo_height() > 250:
            if app.winfo_height() > 270:
                if app.winfo_height() > 290:
                    if app.winfo_height() > 330:
                        if app.winfo_height() > 350:
                            if app.winfo_height() > 370:
                                if app.winfo_height() > 390:
                                    if app.winfo_width() > 420:
                                        time_display.configure(font=("Segoe UI Variable", 100))
                            else:
                                if app.winfo_width() > 420:
                                    time_display.configure(font=("Segoe UI Variable", 90))
                        else:
                            if app.winfo_width() > 400:
                                time_display.configure(font=("Segoe UI Variable", 80))
                    else:
                        if app.winfo_width() > 360:
                            time_display.configure(font=("Segoe UI Variable", 70))
                else:
                    if app.winfo_width() > 360:
                        time_display.configure(font=("Segoe UI Variable", 60))
            else:
                if app.winfo_width() >= 300:
                    time_display.configure(font=("Segoe UI Variable", 50))
        else:
            if app.winfo_width() >= 300:
                time_display.configure(font=("Segoe UI Variable", 40))
    else:
        time_display.configure(font=("Segoe UI Variable", 30))

    if app.winfo_width() >= 301:
        if app.winfo_width() >= 320:
            if app.winfo_width() >= 340:
                if app.winfo_width() >= 360:
                    if app.winfo_width() >= 380:
                        if app.winfo_width() >= 400:
                            if app.winfo_width() >= 420:
                                if app.winfo_width() >= 440:
                                    if app.winfo_width() >= 460:
                                        play_button.configure(width=54)
                                        manager_button.configure(width=54)
                                else:
                                    play_button.configure(width=50)
                                    manager_button.configure(width=50)
                            else:
                                play_button.configure(width=46)
                                manager_button.configure(width=46)
                        else:
                            play_button.configure(width=42)
                            manager_button.configure(width=42)
                    else:
                        play_button.configure(width=38)
                        manager_button.configure(width=38)
                else:
                    play_button.configure(width=34)
                    manager_button.configure(width=34)
            else:
                play_button.configure(width=31)
                manager_button.configure(width=31)
        else:
            play_button.configure(width=28)
            manager_button.configure(width=28)
    else:
        play_button.configure(width=25)
        manager_button.configure(width=25)
        

# THEMED IMAGES
if config['theme'] == "Dark":
    settings_btn.configure(image=settings_image_dark)
elif config['theme'] == "Light":
    settings_btn.configure(image=settings_image_light)
if theme == "System":
    if darkdetect.theme() == "Dark":
        settings_btn.configure(image=settings_image_dark)
    elif darkdetect.theme() == "Light":
        settings_btn.configure(image=settings_image_light)  

#DETECT RESIZING
app.bind("<Configure>", sizechanged)

# TKINTER MAINLOOP
app.mainloop()
