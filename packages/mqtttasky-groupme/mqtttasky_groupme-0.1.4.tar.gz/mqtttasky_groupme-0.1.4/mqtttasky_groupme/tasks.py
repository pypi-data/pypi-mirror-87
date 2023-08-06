from mqtttasky_groupme import gpio_status_light_util as status_light
from datetime import datetime as dt, timedelta
from mqtttasky_groupme.config import mqtt_config
from PIL import Image as PILImage, ImageTk
from cryptography.fernet import Fernet
from threading import Thread
from time import sleep
from tkinter import *

import paho.mqtt.client as mqtt
import pkg_resources
import os

mqtt_client = mqtt.Client()

key = ''
cipher = None

MESSAGE_ENCODING = 'utf-8'

# Taken from https://raspberrypi.stackexchange.com/questions/38294/error-when-attempting-to-create-python-gui-using-tkinter-no-display-name-and-n
# Necessary when the $DISPLAY var is null:
if os.environ.get('DISPLAY','') == '':
    print('No display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')


# This is called on by app.py because all of the config data must be entered before it is used..
def init_cipher():
    global key
    global cipher
    key = mqtt_config.CONFIG['cipher_key']
    cipher = Fernet(key)


# This is also called on by app.py because all of the config data must be entered before it is used..
def init_mqtt_client():
    # Use the username and password pair as provided in the
    # MQTT configuration:
    mqtt_client.username_pw_set(mqtt_config.CONFIG['username'],
                            mqtt_config.CONFIG['password'])

    mqtt_client.connect(host=mqtt_config.CONFIG['host'],
                    port=mqtt_config.CONFIG['port']) # Connect using host/port from config
    print('\n[ MQTT Client ] Connected to broker.\n')

    try:
        enc_task_buffer = cipher.encrypt(bytes('Hello from MQ T T Tasky!', MESSAGE_ENCODING))
        mqtt_client.publish('pub/tasks', enc_task_buffer)
    except:
        pass
    Thread(target=mqtt_client.loop_forever).start()

# The task object represents a task and is used as an arg
# to TaskWindow to display it graphically.
class Task:
    def __init__(self, title, start_date, task_time,
                    notif_time, description):
        self.title       = title
        self.start_date  = start_date
        self.task_time   = task_time
        self.description = description

        task_dt = dt.strptime((start_date + ' ' + task_time)
                                , '%m/%d/%y %H:%M')

        # The below code takes a time like '30 minutes before'
        # and creates a datetime object that would actually
        # represent that amount of time before the task's start
        # date and time.
        #
        # If format invalid or not recognized, set notification
        # time to equal task time (notification will be given
        # when the task is set to start).
        if ' minute' in notif_time:
            try:
                delta = notif_time.split(' minute')[0]
                notif_time_dt = task_dt - timedelta(minutes=int(delta))
                self.notif_time = notif_time_dt
            except:
                self.notif_time = task_dt
        elif ' hour' in notif_time:
            try:
                delta = notif_time.split( 'hour')[0]
                notif_time_dt = task_dt - timedelta(hours=int(delta))
                self.notif_time = notif_time_dt
            except:
                self.notif_time = task_dt
        elif ' day' in notif_time:
            try:
                delta = notif_time.split(' day')[0]
                notif_time_dt = task_dt - timedelta(days=int(delta))
                self.notif_time = notif_time_dt
            except:
                self.notif_time = task_dt
        elif ' week' in notif_time:
            try:
                delta = notif_time.split(' week')[0]
                notif_time_dt = task_dt - timedelta(weeks=int(delta))
                self.notif_time = notif_time_dt
            except:
                self.notif_time = task_dt
        else:
            self.notif_time = task_dt


    # This function is used to generate a string to be read by
    # text-to-speech engine simple_google_tts
    def tts(self):
        return (
            f"Task { self.title } starts on { self.start_date }"
            f" at { self.task_time }. Task's description is as follows:"
            f" { self.description }"
        )


    def __str__(self):
        if len(self.description) > 60:
            desc = '{}'.format(self.description[:60]) # Truncate to 60 chars.
        else:
            desc = self.description
        return (
            f"Title:        { self.title }"
            f"\nStart Date:  { self.start_date }"
            f"\nTask Time:   { self.task_time }"
            f"\nNotif. Time: { self.notif_time }"
            f"\nDescription: { desc }"
        )


# Singleton class -- learned from https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html
class TaskScheduler:
    class __TaskScheduler:
        def __init__(self):
            self.task_list = []
            self.iterable_task_list = []
            t = Thread(target=self.manage_notifications)
            t.start()


        def schedule(self, task):
            self.task_list.append(task)
            print(task.notif_time)


        def remove(self, task):
            self.task_list.remove(task)

        
        def remove_all(self):
            try: # May fail if it is being iterated over.
                self.task_list.clear()
                return True
            except:
                sleep(.2)
                try:
                    self.task_list.clear()
                    return True
                except:
                    return False


        def pub_notification(self, task_str):
            Thread(target=status_light.blink_notification).start() # Blink lights in sequence.
            try:
                # Convert the message from utf-8 string to byte array and encrypt:
                enc_task_buffer = cipher.encrypt(bytes(task_str, MESSAGE_ENCODING))
                # Publish
                mqtt_client.publish('pub/tasks', enc_task_buffer)
            except:
                pass

        # Call on simple_google_tts to read the task aloud:
        def read_task(self, task_str):
            os.system('simple_google_tts -p en ' + '\"' + task_str + '\"')


        # This function will iterate over each task in list and compare
        # its notification time to the current time. When they match,
        # it broadcasts a notification to pub/tasks, reads the message
        # aloud using simple_google_tts, displays it graphically and
        # deletes the Task object.
        def manage_notifications(self):
            while True:
                for t in self.task_list:
                    self.iterable_task_list.append(t)

                now = dt.now().replace(second=0, microsecond=0)
                for t in self.iterable_task_list:
                    if t.notif_time == now:
                        pub_thread = Thread(target=self.pub_notification, args=(t.tts(),))
                        tts_thread = Thread(target=self.read_task, args=(t.tts(),))
                        gui_thread = Thread(target=TaskWindow, args=(t,))

                        pub_thread.start() # Encrypt and publish to pub/tasks
                        tts_thread.start() # Read aloud over using simple_google_tts
                        gui_thread.start() # Display the Task on screen for several seconds
                        
                        self.task_list.remove(t)

                self.iterable_task_list.clear()
                sleep(30)

    instance = None


    def __new__(cls):
        if not TaskScheduler.instance:
            TaskScheduler.instance = TaskScheduler.__TaskScheduler()
        return TaskScheduler.instance


    def __getattr__(self, name):
        return getattr(self.instance, name)


    def __setattr__(self, name):
        return setattr(self.instance, name)
        
# Basic GUI window, loads the data into labels, adds the labels
# to the window, displays for 4 seconds, and self-disposes.
class TaskWindow:
    def __init__(self, task):
        self.title       = task.title
        self.start_date  = task.start_date
        self.task_time   = task.task_time
        self.description = task.description

        self.WINDOW = Tk()
        self.WINDOW.title('Task alert: ' + self.title)
        self.WINDOW.minsize(400, 300)

        self.init_components()
        self.init_labels()
        self.add_to_window()

        self.WINDOW.after(4000, lambda: self.WINDOW.destroy())
        mainloop()


    def init_components(self):
        path = pkg_resources.resource_filename(__name__, 'images/clock-32x32.png')
        self.clock_image = ImageTk.PhotoImage(
            PILImage.open(path)
        )


    def init_labels(self):
        self.title_label   = Label(self.WINDOW,
                                    text=self.title,
                                    fg='#4286F6',
                                    font=('Arial', 26),
                                    wraplength=350)

        self.image_label   = Label(self.WINDOW,
                                    image=self.clock_image)

        self.header_label1 = Label(self.WINDOW,
                                    text='Today',
                                    fg='black',
                                    font=('Arial', 16))

        self.header_label2 = Label( self.WINDOW,
                                    text=(self.start_date),
                                    fg='black',
                                    font=('Arial', 16))

        self.time_label    = Label(self.WINDOW,
                                    text=self.task_time,
                                    fg='black',
                                    font=('Arial', 14))

        self.descr_label   = Label(self.WINDOW,
                                    text=self.description,
                                    fg='black',
                                    bg = '#E6E6E6',
                                    font=('Arial', 18),
                                    highlightbackground='#4286F6',
                                    highlightthickness=1,
                                    wraplength=350)

    def add_to_window(self):
        self.title_label.place(x=32, y=16)
        self.image_label.place(x=32, y=108)
        self.header_label1.place(x=76, y=92)
        self.header_label2.place(x=156, y=92)
        self.time_label.place(x=76, y=120)
        self.descr_label.place(x=32, y=180)
