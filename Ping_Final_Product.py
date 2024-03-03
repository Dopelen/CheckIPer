import os
import sys

from kivy.config import Config
from kivy.resources import resource_add_path, resource_find

Config.set('graphics', 'resizable', False)
import platform
import subprocess
import re
import threading
from random import randint

from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import BoxShadow, Color, Ellipse
from kivy.animation import Animation
from kivy.factory import Factory
from kivy.clock import Clock
from kivy.clock import ClockEvent

from kivy.uix.textinput import TextInput
from kivy.uix.stacklayout import StackLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.uix.popup import Popup
from kivy.uix.image import *
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scatter import Scatter
from kivy.uix.filechooser import FileChooserIconView

Window.size = (600, 600)
Window.clearcolor = (70 / 255, 70 / 255, 120 / 255, 1)
Window.scroll_title = "Monitoring"


class MySpinnerOption(SpinnerOption):
    """Contain main color for spinner"""
    background_color = [84 / 255, 84 / 255, 144 / 255, 1]


class Start_Bt_with_Shadow(Button):
    """Shadow setting for custom button"""

    def __init__(self, **kwargs):
        super(Start_Bt_with_Shadow, self).__init__(**kwargs)
        self.bind(pos=self.update_shadow, size=self.update_shadow, state=self.update_shadow)
        with self.canvas.before:
            self.shadow_color = Color(152 / 255, 152 / 255, 175 / 255, 0.85)
            self.shadow = BoxShadow(
                pos=self.pos,
                size=self.size,
                offset=(0, 0),
                spread_radius=(0, 0),
                border_radius=(0, 0, 0, 0),
                blur_radius=0)

    def update_shadow(self, *args):
        """Update shadow of button in case of status change"""
        self.shadow.pos = self.pos
        self.shadow.size = self.size
        if self.state == "normal":
            self.shadow.blur_radius = 20
        else:
            self.shadow.blur_radius = 40


class RedCircle(Widget):
    """"Custom Widget with Color and Animation settings"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            self.circle_color = Color(18 / 255, 18 / 255, 80 / 255, 0)
            self.circle = Ellipse(pos=self.center, size=(250, 250))

    def setup_for_animate(self, mails):
        """Gets widget, adds animation to it appearing over time"""
        setup_anim = Animation(opacity=0.8, duration=1)
        setup_anim.start(mails)
        Clock.schedule_once(lambda dt: self.animate(mails), 2)

    def animate(self, mails):
        """Gets a widget and adds movement animation to it at specified coordinates"""
        anim = Animation(center_x=295, center_y=295, t='out_quart', duration=2.5)
        anim.start(mails)

    def on_size(self, *args):
        """Update the position of animated elements"""
        self.circle.pos = (self.center_x - 120, self.center_y - 145)

    def shine(self, background_color=(28 / 255, 28 / 255, 90 / 255, 0.9), duration=0.5):
        """Gets a widget and adds color changing animation to it"""
        ani_shine = Animation(r=background_color[0], g=background_color[1], b=background_color[2],
                              a=background_color[3], duration=duration)
        ani_shine.start(self.circle_color)

    def shine_border(self, background_color=(0.8, 0.8, 1, 0.8), duration=0.3):
        """Gets a widget and adds color changing and size changing animation to it"""
        self.circle.size = (280, 280)
        self.circle.pos = (self.center_x - 135, self.center_y - 160)
        ani_shine_b = Animation(r=background_color[0], g=background_color[1], b=background_color[2],
                                a=background_color[3], duration=duration)
        ani_shine_b.start(self.circle_color)
        ani_shine_b.bind(on_complete=self.on_animation_complete)

    def on_animation_complete(self, *args):
        """Causes a delay after the animation is executed, triggering the screen changing function"""
        Clock.schedule_once(self.switch_screen, 1)

    def switch_screen(self, *args):
        """Changing current screen"""
        application.root.current = 'interface_window'


class WelcomeScreen(Screen, RedCircle):
    """Gets images from the startup file directory and uses them to construct the loading screen.
Also uses class RedCircle(Widget) to create widgets with resizing and color properties

    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        ground_fl = FloatLayout()
        Shine_cir = RedCircle()
        Shine_cir_border = RedCircle()
        for mail in range(20):
            mail_picture_bt = Button(on_press=self.setup_for_animate, size_hint=(None, None), size=(47, 32),
                                     background_normal="mmsmall.png", pos=(randint(30, 540), +randint(30, 540)),
                                     opacity=0)
            mail_picture_bt.trigger_action(duration=0)
            ground_fl.add_widget(mail_picture_bt)
        ground_fl.add_widget(Shine_cir_border)
        ground_fl.add_widget(Shine_cir)
        big_title = Label(text="Check'IP'er", font_size=80, color=(1, 1, 1, 0.9), opacity=0,
                          outline_color=(38 / 255, 38 / 255, 100 / 255, 1), outline_width=4,
                          font_name="MonaspaceKryptonVarVF[wght,wdth,slnt].ttf", pos_hint={"x": 0.01, "y": 0.3})
        ground_fl.add_widget(big_title)
        title_anim = Animation(opacity=1, duration=2)
        title_anim.start(big_title)
        self.add_widget(ground_fl)
        Clock.schedule_once(lambda dt: Shine_cir.shine(), 3.5)
        Clock.schedule_once(lambda dt: Shine_cir_border.shine_border(), 4.2)
        serv_Img = Image(source="data-analysis.png", size_hint=(0.3, 0.3), pos=(230, 200))
        ground_fl.add_widget(serv_Img)


class TitleButton(Button):
    """Contain buttons settingns for castomizing title"""
    background_color = (70 / 255, 70 / 255, 120 / 255, 1)
    disabled = True
    disabled_color = ""


class TimeInput(TextInput):
    """Contains additional conditions for input restrictions"""

    def insert_text(self, substring, from_undo=False):
        """ Gets a string and blocks input for certain characters in the following cases:
If the character is not a digit.
If the character is 0 and the text input field is previously empty.
If the number of characters currently entered is more than 2.
If the number obtained as a result of entering is greater than 60

"""

        if re.compile(r'^\d$').match(substring) == None or (self.text == "" and substring == "0"):
            return
        elif len(self.text) + len(substring) <= 2:
            if int(str(self.text) + str(substring)) < 60:
                return super().insert_text(substring, from_undo=from_undo)


class MyApp(App):
    """Creating ScreenManager with 2 screans and animation of changing screen"""

    def build(self):
        Screens_of_app = ScreenManager(
            transition=WipeTransition(duration=1, clearcolor=(70 / 255, 70 / 255, 120 / 255, 1)))
        Screens_of_app.add_widget(WelcomeScreen(name='welcone_animation'))
        Screens_of_app.add_widget(InterfaceScreen(name='interface_window'))
        return Screens_of_app


class InterfaceScreen(Screen):
    """Receives a text file from "Select file" function and, based on it,
constructs a graphical display of the results of the "ping" command for the IP addresses
specified in the file and their description.

Also allows the above check to be carried out at a certain interval (with a maximum limit of 59 hours and 59 minutes),
after entering the interval duration in the "Change timer" window.

During code execution, the operating system used is checked to adjust the parameters of the ping command
(using platform.system()), so that the program can run on different operating systems.

For the program to work correctly, you must follow the file structure:
IP"separator"Description"separator"Place"separator"Type
In this implementation, the separator is a tab: \t
Thus, "Description" corresponds to the field in the text file that comes after IP in the file "IP.txt" separated by \t
"Place" corresponds to the field in the text file that comes after "Description" in the file "IP.txt" separated by \t and so on

It allows you to group the displayed data using the "Group output" button.
Grouping is carried out on the data obtained in the previous iteration and does not trigger a new check.

"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.IP_info = {}
        self.additional_check = []
        self.param = '-n' if platform.system().lower() == 'windows' else '-c'
        self.timer_minutes, self.timer_hours = 0, 0
        self.started = False
        self.current_time = "00:00:00"
        self.timer_empty = True
        self.path = ''
        self.error_catcher = False
        # For the timer to work correctly, it is necessary to clear currently ongoing events before starting new ones,
        # To avoid errors due to trying to cancel a running event, before it has been created, this variable is introduced,
        # which is a Clock object that can be canceled until the user uses the timer
        self.time_update = Clock.schedule_once(self.clock_std, 100)
        background_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        upper_box = BoxLayout(orientation="horizontal", size_hint=(1, .1))
        color_theme_bt = ToggleButton(text="Light", font_size=(10), halign="left", valign="top", size_hint=(.1, 1),
                                      width=60, height=40, padding=[0, 0, 0, 0],
                                      background_color=(70 / 255, 70 / 255, 120 / 255, 0.75))
        inside_upper = StackLayout(size_hint=(1, .9), orientation='rl-bt', spacing=10, padding=[0, 0, 7, 7])
        self.time_lbl = Label(text=self.current_time, font_size=(25), halign="right", valign="center",
                              size_hint=(.25, .1), font_name="MonaspaceKryptonVarVF[wght,wdth,slnt].ttf")
        time_text = Label(text="Time until next check", font_size=(25), halign="right", valign="center",
                          size_hint=(None, .1), width=(325), font_name="MonaspaceKryptonVarVF[wght,wdth,slnt].ttf")
        inside_upper.add_widget(self.time_lbl)
        inside_upper.add_widget(time_text)
        upper_box.add_widget(color_theme_bt)
        upper_box.add_widget(inside_upper)
        background_layout.add_widget(upper_box)

        self.bl_for_scroll_view = BoxLayout(size_hint_y=None, orientation="vertical")
        self.bl_for_scroll_view.bind(minimum_height=self.bl_for_scroll_view.setter("height"))
        self.scroll_title = BoxLayout(orientation="horizontal", size_hint_y=None, height=50)
        self.scroll_title.add_widget(TitleButton(text="IP"))
        self.scroll_title.add_widget(TitleButton(text="Description"))
        self.scroll_title.add_widget(TitleButton(text="Place"))
        self.scroll_title.add_widget(TitleButton(text="Type"))
        self.scroll_title.add_widget(TitleButton(text="Status"))
        self.bl_for_scroll_view.add_widget(self.scroll_title)
        for elem in self.IP_info:
            btn = Button(text=str(elem), size_hint_y=None, height=40,
                         background_color=(70 / 255, 70 / 255, 120 / 255, 0.6))
            self.bl_for_scroll_view.add_widget(btn)
        scroll_view = ScrollView(size_hint=(1, .8))
        scroll_view.add_widget(self.bl_for_scroll_view)
        background_layout.add_widget(scroll_view)

        lower_sl = StackLayout(size_hint=(1, .1), orientation='lr-tb', spacing=10)
        start_but = Start_Bt_with_Shadow(text="Start", size_hint=(.1, 1),
                                         background_color=(70 / 255, 70 / 255, 120 / 255, 0.8))
        start_but.bind(on_press=self.previous_selection)
        lower_sl.add_widget(start_but)
        group_spiner = Spinner(text="Group output", values=("Description", "Place", "Type", "Status"),
                               size_hint=(.3, 1), background_color=(70 / 255, 70 / 255, 120 / 255, 0.8),
                               option_cls=Factory.get("MySpinnerOption"))
        group_spiner.bind(text=self.change_grouping)
        lower_sl.add_widget(group_spiner)
        change_time_bt = Button(text="Change timer", size_hint=(.3, 1),
                                background_color=(70 / 255, 70 / 255, 120 / 255, 0.8))
        lower_sl.add_widget(change_time_bt)
        lower_sl.add_widget(Button(text="Select file", size_hint=(.3, 1), on_press=self.select_file,
                                   background_color=(70 / 255, 70 / 255, 120 / 255, 0.8)))
        time_window = BoxLayout(orientation="vertical", spacing=10)
        time_input_window = BoxLayout(orientation="horizontal")
        self.text_hours = TimeInput(text="", hint_text="Hours", input_filter="int", multiline=False)
        self.text_minutes = TimeInput(text="", hint_text="Minutes", input_filter="int", multiline=False)
        time_input_window.add_widget(self.text_hours)
        time_input_window.add_widget(self.text_minutes)
        timer_view = Popup(title='Set the time until the next check\nMaximum value = 59',
                           content=time_window,
                           size_hint=(None, None), size=(300, 150), title_align="center", overlay_color=(0, 0, 0, .45),
                           separator_color=(70 / 255, 70 / 255, 120 / 255, 1), background_color=(1, 1, 1.7, 1))
        change_time_bt.bind(on_press=timer_view.open)
        time_window.add_widget(time_input_window)
        accept_timer_start_bt = (
            Button(text="Okey", size=(50, 30), background_color=(70 / 255, 70 / 255, 120 / 255, 0.8)))
        time_window.add_widget(accept_timer_start_bt)
        accept_timer_start_bt.bind(on_press=timer_view.dismiss)
        timer_view.bind(on_dismiss=self.timer_status)
        background_layout.add_widget(lower_sl)
        self.add_widget(background_layout)
        self.error_popup = Popup(title='Error',
                                 content=Label(
                                     text="Processing this file caused an error, please check if the file is in the required format:\nIP\\tDescription\\tPlace\\tType\nIn this implementation, the separator is a tab: \\t",
                                     size_hint_y=None,
                                     text_size=(400, None),
                                     halign='left',
                                     valign='top', padding=(30, 10)),
                                 size_hint=(None, None), size=(400, 200), title_align="center",
                                 overlay_color=(0, 0, 0, .85),
                                 separator_color=(70 / 255, 70 / 255, 120 / 255, 1),
                                 background_color=(1, 1, 1.7, 1))

    def previous_selection(self, instance):
        """This function starts the check if a check file has been selected previously, or prompts you to select a file
        Also shows an error if an error occurred while reading the file

        """

        if not os.path.isfile("CheckIPer_previous_selection.txt"):
            self.select_file(self)
        else:
            if not self.error_catcher:
                self.ping_initialization_loading_screen()
            else:
                self.error_popup.open()

    def ping_initialization_loading_screen(self, *args):
        """Constructs a loading screen using an image and a ttf font file obtained from the launch directory
and then creates a separate control thread to execute the ping command.

        """

        loading_fl = FloatLayout()
        loading_label = Label(text="Checking...", pos_hint={'center_x': 0.5, 'center_y': 0.5},
                              font_name="MonaspaceKryptonVarVF[wght,wdth,slnt].ttf", font_size=30)
        label_flicker = Animation(opacity=0) + Animation(opacity=1)
        label_flicker.repeat = True
        loading_fl.add_widget(loading_label)
        label_flicker.start(loading_label)
        rotat = Scatter(do_rotation=True, do_translation=False, do_scale=False, auto_bring_to_front=False,
                        pos=(250, 250), size_hint=(1, 1))
        rot_img = Image(source="3.png", size=(60, 60), center=rotat.center,
                        color=(100 / 255, 100 / 255, 170 / 255, 0.8))
        rotat.add_widget(rot_img)
        loading_fl.add_widget(rotat)
        self.loading_popup = Popup(title='', content=loading_fl, title_align="center", overlay_color=(0, 0, 0, .45),
                                   size_hint=(None, None), size=(450, 450), auto_dismiss=False,
                                   separator_color=(70 / 255, 70 / 255, 120 / 255, 1),
                                   background_color=(1, 1, 1.7, 1))
        self.loading_popup.open()
        main_anim = Animation(rotation=360000, duration=3000, center=rotat.center)
        main_anim.start(rotat)
        thread_for_ping = threading.Thread(target=self.read_ip)
        thread_for_ping.start()

    def change_grouping(self, instance, text):
        """Receives the required grouping selected by the Group output button.
Using a dictionary, converts the selected value into the field index from the IP.txt file
Starts the screen refresh process according to the selected grouping by passing the sort_base argument

        """
        sorting_variants = {"Description": 0, "Place": 1, "Type": 2, "Status": 3}
        self.update_view(sort_base=sorting_variants[text])

    def update_view(self, sort_base=-1):
        """In the case where the view was clipped earlier, it clears it.
Also accepts a sorting argument, based on which it draws a new view.
Calls the function to create pop-up windows on_press for fields that do not fit in the display

        """

        current_IPs = self.IP_info
        if sort_base != -1:
            current_IPs = dict(sorted(self.IP_info.items(), key=lambda item: item[1][sort_base]))
        if self.started:
            self.bl_for_scroll_view.clear_widgets()
            self.bl_for_scroll_view.add_widget(self.scroll_title)

        for ip, result_of_ping in current_IPs.items():
            line_of_output = BoxLayout(orientation="horizontal", size_hint_y=None, height=40, )
            shade_for_result = (70 / 255, 70 / 255, 120 / 255, 0.6)
            ip_text = Button(text=str(ip), text_size=(90, 40), font_size=(15), halign="left", valign="center",
                             max_lines=1, shorten=True, shorten_from="right", background_color=shade_for_result)
            if len(ip) > 10:
                ip_text.bind(on_press=self.full_name_popup_constract)
            line_of_output.add_widget(ip_text)
            for peace_of_answer in result_of_ping:
                hal = "left"
                if peace_of_answer == "UP":
                    hal = "center"
                    shade_for_result = (70 / 255, 120 / 255, 100 / 255, 0.6)
                elif peace_of_answer == "ERROR" or peace_of_answer == "NO RESPONSE":
                    hal = "center"
                    shade_for_result = (120 / 255, 70 / 255, 100 / 255, 0.6)
                but_for_ans = Button(text=str(peace_of_answer), text_size=(90, 40), font_size=(15), halign=hal,
                                     valign="center", max_lines=1, shorten=True, shorten_from="right",
                                     background_color=shade_for_result)
                if len(peace_of_answer) > 6:
                    but_for_ans.bind(on_press=self.full_name_popup_constract)
                line_of_output.add_widget(but_for_ans)
            self.bl_for_scroll_view.add_widget(line_of_output)

    def full_name_popup_constract(self, instance):
        """Receives a button and based on its content creates a popup window displaying the received text limited to 30 characters"""

        full_name_ip_popup = Popup(title='', content=Label(text=instance.text), size_hint=(None, None),
                                   size=(400, 100),
                                   auto_dismiss=True, overlay_color=(0, 0, 0, .45),
                                   separator_color=(70 / 255, 70 / 255, 120 / 255, 1),
                                   background_color=(1, 1, 1.7, 1))
        if len(instance.text) > 30:
            full_name_ip_popup.content.text = f"{instance.text[:30]}..."
        full_name_ip_popup.open()

    def update_time(self, instance):
        """Refers to the sum of the total time, in seconds, that is specified in the timer.
Based on it, it constructs a label displaying the time remaining until the next check
Cancels the time event when the time has elapsed and starts a new iteration of the check

        """

        if self.secs_for_timer != 0:
            self.secs_for_timer -= 1
            seconds_for_display = str(divmod(self.secs_for_timer, 60)[1]).zfill(2)
            if seconds_for_display == "00" and self.secs_for_timer != 0:
                if self.timer_minutes == 0 and self.timer_hours != 0:
                    self.timer_hours -= 1
                    self.timer_minutes = 59
                else:
                    self.timer_minutes -= 1
            minutes_for_display = str(self.timer_minutes).zfill(2)
            hours_for_display = str(self.timer_hours).zfill(2)
            self.time_lbl.text = f"{hours_for_display}:{minutes_for_display}:{seconds_for_display}"
        else:
            ClockEvent.cancel(self.time_update)
            self.ping_initialization_loading_screen()

    def reset_time(self):
        """ A function that:
Cancels a currently running Clock event
Changes the "started" flag
Accesses the timer and converts the time specified there into one that is correctly displayed on the screen
and processed by the update_time function
Prevents the check from being restarted if the timer is empty

        """

        ClockEvent.cancel(self.time_update)
        self.started = True
        if self.timer_empty:
            self.time_lbl.text = "00:00:00"
            return
        self.time_lbl.text = f"{self.text_hours.text.zfill(2)}:{self.text_minutes.text.zfill(2)}:00"
        self.text_minutes.text = self.text_minutes.text.zfill(1)
        self.text_hours.text = self.text_hours.text.zfill(1)
        self.timer_minutes, self.timer_hours = int(self.text_minutes.text), int(self.text_hours.text)
        self.secs_for_timer = self.timer_minutes * 60 + self.timer_hours * 3600
        if self.timer_minutes > 0:
            self.timer_minutes -= 1
        elif self.timer_minutes == 0:
            self.timer_hours -= 1
            self.timer_minutes = 59
        self.time_update = Clock.schedule_interval(self.update_time, 1)

    def timer_status(self, instance):
        """When called, it checks the time input fields in the timer window.
In accordance with this, the timer_empty flag is changed to indicate the need to restart the verification program
after the time has expired

        """

        if re.compile(r'^(00|0|)$').match(self.text_hours.text) is not None and re.compile(r'^(00|0|)$').match(
                self.text_minutes.text) is not None:
            self.timer_empty = True
        else:
            self.timer_empty = False

    def select_file(self, instance):
        """Calls the file manager when you click on the file selection button, or if the file was not selected earlier, when you click on the start button"""
        file_chooser = FileChooserIconView()
        file_chooser.filters = ["*.txt"]
        file_chooser.bind(on_submit=self.file_selected)
        file_chooser_window = BoxLayout(orientation="vertical", spacing=10)
        file_chooser_window.add_widget(file_chooser)
        self.file_chooser_view = Popup(title='Select the file with data',
                                       content=file_chooser_window,
                                       size_hint=(None, None), size=(500, 500), title_align="center",
                                       overlay_color=(0, 0, 0, .7),
                                       separator_color=(70 / 255, 70 / 255, 120 / 255, 1),
                                       background_color=(1, 1, 1.7, 1))
        self.file_chooser_view.open()

    def file_selected(self, file_chooser, selected, mouse_pos):
        """Sends the path to the file selected through the manager, then closes the file manager, records the file path for future calls"""
        if selected:
            self.path = selected[0]
            with open("CheckIPer_previous_selection.txt", "w") as new_memo:
                new_memo.write(self.path)
                self.error_catcher = False
            self.file_chooser_view.dismiss()

    def ping(self, host, package_amount="1", first=True):
        """The function receives a string containing 4 fields separated by a "separator" (\t default).
Converts it into a list, where the first field corresponds to the IP and the subsequent ones to the
description for the grouping (more read in InterfaceScreen(Screen).__doc__).
In accordance with the IP, it carries out a check and adds its results to the list.
The check is performed using subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
"command" is the verification parameters (1 package).
As a result of the check, only the return code is read and, in accordance with it,
the status is added to the IP information list.

if first ... else... are necessary for the further implementation of the mechanism for re-checking
non-responding addresses. So far there is no visual component to implement this functionality

        """

        if first:
            try:
                host = host.split("\t")
                self.IP_info[host[0]] = [host[1], host[2], host[3], "IN PROCESS"]
            except Exception as format_exc:
                self.error_catcher = True
                return
        command = ['ping', self.param, package_amount, host[0]]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0 and b'TTL=' in result.stdout:
            ping_result = "UP"
        elif result.returncode == 2:
            ping_result = "NO RESPONSE"
            self.additional_check.append(host[0])
        else:
            ping_result = "ERROR"
            if first:
                self.additional_check.append(host[0])
        if first:
            self.IP_info[host[0]][3] = f"{ping_result}"
        else:
            print(result.stdout.decode("866"))

    def read_ip(self):
        """A function that opens the selected from select function .txt file,
initiates checking each line, and also schedules the launch of view and reset_time
        """

        with open("CheckIPer_previous_selection.txt", "r") as memo:
            self.path = memo.readline()
        with open(f"{self.path}", "r") as verifiable_ip:
            check = verifiable_ip.read().splitlines()
            for line in check:
                if not self.error_catcher:
                    self.ping(line)
        self.loading_popup.dismiss()
        Clock.schedule_once(lambda dt: self.update_view())
        Clock.schedule_once(lambda dt: self.reset_time())

    def clock_std(self, instance):
        pass


if __name__ == "__main__":
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    application = MyApp()
    application.run()
