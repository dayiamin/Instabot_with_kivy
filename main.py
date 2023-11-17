import kivy
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.button import MDRectangleFlatButton, MDIconButton,MDRectangleFlatIconButton
import sys
import pickle
from kivy.uix.screenmanager import ScreenManager, Screen
import random
from instalogin2 import login,get_all_posts_categoris,get_user_media,direct_msg
from model.categorizer import categ
from kivy.clock import Clock

from datetime import date
import numpy as np


kivy.require("1.10.1")




class HomePage(MDFloatLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.toolbar = MDTopAppBar(title='dr link')
        self.toolbar.pos_hint = {'top': 1}
        self.add_widget(self.toolbar)

        self.logo = Image(
            source='logo.png',
            size_hint=(0.3, 0.3),
            pos_hint={'center_x': 0.5, 'center_y': 0.73})
        self.add_widget(self.logo)

        self.label1 = MDLabel(
            text='Choose Options for login \nOption 1 for login with password \nOption 2 if you had logged in before',
            font_style='H5',
            size_hint=(.85, .85),
            pos_hint={'center_x': .5, 'center_y': 0.5},
            halign='center',
            color=(34, 34, 34, 255))
        self.add_widget(self.label1)


        self.button1 = MDRectangleFlatIconButton(icon='instagram',
                                                text='Option   1',
                                                pos_hint={'center_x': 0.5, 'center_y': 0.3},
                                                size_hint_x=0.8,
                                                theme_icon_color = "Custom",
                                                icon_color = "cyan",
                                                 font_size='20sp'
        )

        self.button1.bind(on_press=self.transition_to_password_page)

        self.add_widget(self.button1)

        self.button2 = MDRectangleFlatIconButton(icon='instagram',text='Option  2',
                                                pos_hint={'center_x': 0.5, 'center_y': 0.2},size_hint_x=0.8,
                                                theme_icon_color= "Custom",
                                                icon_color="red",
                                                 font_size='20sp'
                                             )

        self.button2.bind(on_press=self.transition_to_login_page)


        self.add_widget(self.button2)

    def transition_to_password_page(self,instance):

        chat_app.screen_manager.current = 'Password'

    def transition_to_login_page(self,instance):

        chat_app.screen_manager.current = 'Login'


class LoginPage(MDFloatLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.toolbar = MDTopAppBar(title='dr link')
        self.toolbar.pos_hint = {'top': 1}
        self.add_widget(self.toolbar)

        self.username = MDTextField(
            hint_text="Enter username",
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
            size_hint_x=0.7,
            )
        self.add_widget(self.username)
        self.button = MDRectangleFlatButton(text='Enter',
                                       pos_hint={'center_x': 0.5, 'center_y': 0.25},size_hint_x=0.7
                                       )
        self.button.bind(on_press=self.user_login_username)

        self.add_widget(self.button)

        self.button2 = MDIconButton(icon='home',
                                             pos_hint={'center_x': 0.95, 'center_y': 0.82},icon_size='55sp'
                                             )

        self.button2.bind(on_press=self.reset)

        self.add_widget(self.button2)


    def user_login_username(self,instance):
        username = self.username.text

        if username.strip() !='':
            try:
                login(username)
                status=True
                info = 'login successfully '
            except:
                status = False
                info = 'login failed'
        else:
            status = False
            info = 'please fill in the forms'
        chat_app.info_page.update_info(info)
        chat_app.screen_manager.current = 'Info'
        if status:
            Clock.schedule_once(self.connect, 5)
        else:
            Clock.schedule_once(self.reset, 7)

    def connect(self, _):
        chat_app.screen_manager.current = 'BaseUser'
    def reset(self, _):
        chat_app.screen_manager.current = 'Home'


class PasswordPage(MDFloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.toolbar = MDTopAppBar(title='dr link')
        self.toolbar.pos_hint = {'top': 1}
        self.add_widget(self.toolbar)

        self.username2 = MDTextField(
            hint_text="Enter username",
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
            size_hint_x=0.7
            )
        self.add_widget(self.username2)

        self.password = MDTextField(
            hint_text= "Password",
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint_x=0.7,
            password = True)
        self.add_widget(self.password)
        self.button3 = MDRectangleFlatButton(text='Enter',
                                       pos_hint={'center_x': 0.5, 'center_y': 0.25}
                                       )

        self.button3.bind(on_press=self.user_login_password)

        self.add_widget(self.button3)

        self.button2 = MDIconButton(icon='home',
                                    pos_hint={'center_x': 0.95, 'center_y': 0.82},
                                    icon_size='55sp'

                                             )

        self.button2.bind(on_press=self.reset)

        self.add_widget(self.button2)

    def user_login_password(self,instance):
        username = self.username2.text
        password = self.password.text
        print(username,password)
        print(type(username),type(password))
        if username.strip() !='' and password.strip() != '':
            try:
                login(username,password)

                status=True
                info = 'login successfully '
            except:
                status=False
                info = 'login failed please check your instagram account it might got banned'
        else:
            status=False
            info = 'please fill in the forms'

        chat_app.info_page.update_info(info)
        chat_app.screen_manager.current = 'Info'
        self.username2.text=''
        self.password.text=''
        if status:
            Clock.schedule_interval(self.connect, 5)
        else:
            Clock.schedule_interval(self.reset, 7)


    def connect(self, _):

        chat_app.screen_manager.current = 'BaseUser'


    def reset(self, _):

        chat_app.screen_manager.current = 'Home'



class BaseUserPage(MDFloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.toolbar = MDTopAppBar(title='dr link')
        self.toolbar.pos_hint = {'top': 1}
        self.add_widget(self.toolbar)

        self.username3 = MDTextField(
            hint_text="Enter base page username",
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint_x=0.7,
            )
        self.add_widget(self.username3)

        self.button4 = MDRectangleFlatButton(text='Enter',
                                             pos_hint={'center_x': 0.5, 'center_y': 0.25}
                                             )

        self.button4.bind(on_press=self.base_user)
        self.add_widget(self.button4)

        self.button5 = MDRectangleFlatButton(text='Already entered?',
                                             pos_hint={'center_x': 0.5, 'center_y': 0.15}
                                             )

        self.button5.bind(on_press=self.connect)
        self.add_widget(self.button5)

        self.button = MDIconButton(icon='home',
                                             pos_hint={'center_x': 0.95, 'center_y': 0.82},icon_size='55sp'
                                             )

        self.button.bind(on_press=self.back)

        self.add_widget(self.button)

    def base_user(self, instance):
        username = self.username3.text

        global baseuser
        baseuser = username
        print(baseuser)
        if username.strip() != '':
            try:
                info = get_all_posts_categoris(username)

                status = True
            except:
                status = False
                info = 'Error in getting information of Base page '
        else:
            status = False
            info = 'Please fill in the form '

        print(info)
        if status:
            chat_app.info_page.update_info(info)
            chat_app.screen_manager.current = 'Info'
            Clock.schedule_once(self.connect, 50)
        else:
            chat_app.info_page.update_info(info)
            chat_app.screen_manager.current = 'Info'
            Clock.schedule_once(self.reset, 7)


    def connect(self, _):

        chat_app.screen_manager.current = 'TargetUser'

    def reset(self, _):

        chat_app.screen_manager.current = 'BaseUser'

    def back(self,_):

        chat_app.screen_manager.current = 'Home'



class TargetUserPage(MDFloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.toolbar = MDTopAppBar(title='dr link')
        self.toolbar.pos_hint = {'top': 1}
        self.add_widget(self.toolbar)

        self.username4 = MDTextField(
            hint_text="Enter Target page username",
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint_x=0.7)
        self.add_widget(self.username4)

        self.button5 = MDRectangleFlatButton(text='Enter',
                                             pos_hint={'center_x': 0.5, 'center_y': 0.25},size_hint_x=0.6
                                             )

        self.button5.bind(on_press=self.target_user)

        self.add_widget(self.button5)

        self.button = MDIconButton(icon='home',
                                             pos_hint={'center_x': 0.95, 'center_y': 0.82},
                              icon_size='55sp',

                                             )

        self.button.bind(on_press=self.hom)

        self.button3 = MDIconButton(icon='backburger',
                                             pos_hint={'center_x': 0.05, 'center_y': 0.82},icon_size='55sp'
                                             )


        self.button3.bind(on_press=self.back)
        self.add_widget(self.button)
        self.add_widget(self.button3)

    def target_user(self, instance):
        username = self.username4.text

        global targetuser
        targetuser = username
        print(targetuser)
        if username.strip() != '':
            try:
                global userlist
                userlist, caption, post_date, pk = get_user_media(username)
                print(userlist)
                pk_list = []
                pk_list.append(pk)
                if post_date.date() == date.today():
                    global category
                    category = categ(caption, pk_list)
                    print(category)
                    pred = list(category.values())[0]
                    fardi_num = pred[0] * 100
                    zoji_num = pred[1] * 100
                    koodak_num = pred[2] * 100
                    ezdevaj_num = pred[3] * 100
                    translate = {0:'Fardi',1:'Zoji va jensi',2:'Koodak va nojavan',3:'Pish az ezdevaj'}
                    if list(category.values())[0][0] == 4:
                        self.status3 = 0

                    else:
                        result = f'{username} last post caption was \n{caption}\nand model prediction is\n'+ f'Ehtemal fardi>>> ' '%.2f' % fardi_num + '% ,'+ f'\nEhtemal zoji ya jensi>>> '+ '%.2f' % zoji_num + '% ,' +f'\nEhtemal kodak va nojavan '+ '%.2f' % koodak_num + '% ,' + f'\nEhtemal pish az ezdevaj ' + '%.2f' % ezdevaj_num + '%'+ f'\nso max prediction is >> {translate[np.argmax(pred)]}'


                        self.status3 = 1
                else:
                    self.status3 = 2
            except:
                self.status3 = 3
        else:
            self.status3 = 4

        match self.status3:
            case 0:
                info = 'Error Target page last post is not categorized '
            case 1:
                info = result
            case 2:
                info = 'Error Target page last post was not for today '
            case 3:
                info = 'Error in getting target user data '
            case 4:
                info = 'please fill in the form '


        print(info)
        if self.status3 != 1:
            chat_app.info_page.update_info(info)
            chat_app.screen_manager.current = 'Info'
            Clock.schedule_once(self.reset, 55)
        else:
            chat_app.info_page.update_info(info)
            chat_app.screen_manager.current = 'Info'
            Clock.schedule_once(self.connect, 8)

    def connect(self, _):

        chat_app.screen_manager.current = 'Direct'
    def reset(self, _):

        chat_app.screen_manager.current = 'TargetUser'
    def hom(self,_):

        chat_app.screen_manager.current = 'Home'
    def back(self,_):

        chat_app.screen_manager.current = 'BaseUser'

# todo \/ and fix the earlier pages for more error support
class Direct(MDFloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #

        self.toolbar = MDTopAppBar(title='dr link')
        self.toolbar.pos_hint = {'top': 1}
        self.add_widget(self.toolbar)


        self.label1 = MDLabel(
                text = f'do you want direct  users we found from target"s last post?',
                font_style = 'H5',
                size_hint = (.85, .85),
                pos_hint = {'center_x': .5, 'center_y': 0.55},
                halign = 'center',
                color = (34, 34, 34, 255))

        self.add_widget(self.label1)

        self.button = MDRectangleFlatButton(text='yes',
                                             pos_hint={'center_x': 0.25, 'center_y': 0.35},size_hint_x=0.7
                                             )
        self.button.bind(on_press=self.yes)

        self.add_widget(self.button)
        self.button2 = MDRectangleFlatButton(text='no',
                                       pos_hint={'center_x': 0.6, 'center_y': 0.35}, size_hint_x=0.7
                                       )

        self.button2.bind(on_press=self.noo)

        self.add_widget(self.button2)

    def yes(self,_):
        try:
            with open(f"files/userlist-{targetuser}", "rb") as fpp:  # Pickling
                users = pickle.load(fpp)
            with open(f"files/allpostcateg-{baseuser}", "rb") as fpppp:  # Pickling
                base_user_categ = pickle.load(fpppp)
            self.final = []
            pred = list(category.values())[0]
            print(users)
            print(base_user_categ.values(),base_user_categ)
            for i, j in zip(base_user_categ.values(), base_user_categ):
                if i == np.argmax(pred):
                    self.final.append(j)
            print(self.final)
            direct_msg(random.choice(self.final), users)
            status = True
            info = f'{users} are chosen \nDirect Sent !!!!'

        except:
            status = False
            info = 'Error in sending Direct !!!'

        chat_app.info_page.update_info(info)
        chat_app.screen_manager.current = 'Info'
        if not status :
                Clock.schedule_once(self.reset, 40)
        else:
                Clock.schedule_once(self.hom, 40)

    def noo(self,_):
        chat_app.screen_manager.current = 'TargetUser'

    def reset(self,_):
        chat_app.screen_manager.current = 'Direct'

    def hom(self,_):
        chat_app.screen_manager.current = 'Home'


class InfoPage(MDFloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.message = MDLabel(halign="center", valign="middle", font_size=30)

        self.message.bind(width=self.update_text_width)

        self.add_widget(self.message)

    def update_info(self, message):
        self.message.text = message

    def update_text_width(self, *_):
        self.message.text_size = (self.message.width * 0.9, None)


class MyApp(MDApp):
    def build(self):

        self.screen_manager = ScreenManager()
        self.home_page = HomePage()
        screen = Screen(name='Home')
        screen.add_widget(self.home_page)
        self.screen_manager.add_widget(screen)

        self.info_page = InfoPage()
        screen = Screen(name='Info')
        screen.add_widget(self.info_page)
        self.screen_manager.add_widget(screen)

        chat_app.create_login_page()
        chat_app.create_password_page()
        chat_app.create_base_user_page()
        chat_app.create_target_user_page()
        chat_app.create_direct_user()


        return self.screen_manager

    def create_password_page(self):

        self.password_page = PasswordPage()
        screen = Screen(name='Password')
        screen.add_widget(self.password_page)
        self.screen_manager.add_widget(screen)

    def create_base_user_page(self):
        self.base_user_page = BaseUserPage()
        screen = Screen(name='BaseUser')
        screen.add_widget(self.base_user_page)
        self.screen_manager.add_widget(screen)



    def create_login_page(self):

        self.login_page = LoginPage()
        screen = Screen(name='Login')
        screen.add_widget(self.login_page)
        self.screen_manager.add_widget(screen)

    def create_target_user_page(self):

        self.target_user_page = TargetUserPage()
        screen = Screen(name='TargetUser')
        screen.add_widget(self.target_user_page)
        self.screen_manager.add_widget(screen)

    def create_direct_user(self):

        self.direct_user = Direct()
        screen = Screen(name='Direct')
        screen.add_widget(self.direct_user)
        self.screen_manager.add_widget(screen)

def show_error(message):
    chat_app.info_page.update_info(message)
    chat_app.screen_manager.current = 'Info'
    Clock.schedule_once(sys.exit, 10)
#

if __name__ == "__main__":
    my_app = MyApp()

    my_app.run()