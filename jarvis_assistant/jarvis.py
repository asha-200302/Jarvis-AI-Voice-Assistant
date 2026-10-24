import time
import threading
import keyboard
import numpy as np
import sounddevice as sd
import speech_recognition as sr
import os
import logging
for _name in ('comtypes', 'urllib3', 'comtypes.client._events'):
    logging.getLogger(_name).setLevel(logging.ERROR)
import pyautogui
import subprocess as sp
import webbrowser
import imdb
import datetime
import pyttsx3
import sys
from kivy.uix import widget,image,label,boxlayout,textinput
from kivy import clock
from const import SCREEN_HEIGHT,SCREEN_WIDTH,GEMINI_API_KEY
from utils import youtube,search_on_google,search_on_wikipedia,send_email,get_news,weather_forecast,find_my_ip
from jarvis_button import JarvisButton
import google.generativeai as genai


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 175)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

genai.configure(api_key=GEMINI_API_KEY)

USER_NAME = os.environ.get('USER_NAME', 'Asha')
BOT_NAME = os.environ.get('BOT_NAME', 'Jarvis')

SYSTEM_PROMPT = (
    f"You are {BOT_NAME}, a friendly, smart voice assistant talking with {USER_NAME}. "
    "You can answer questions on any topic, explain things, help with study, coding, "
    "writing and ideas, just like ChatGPT. Your replies are spoken aloud, so use plain "
    "conversational text only: no markdown, no bullet symbols, no asterisks, no emojis. "
    "Keep answers short (2 to 5 sentences) unless the user asks for a detailed explanation. "
    "Remember what was said earlier in this conversation."
)
model = genai.GenerativeModel(
    os.environ.get('GEMINI_MODEL', 'gemini-3.1-flash-lite'),
    system_instruction=SYSTEM_PROMPT,
)

# Phrases that trigger built-in computer commands. Everything else goes to the AI chat.
LOCAL_TRIGGERS = (
    "play music", "command prompt", "ip address", "youtube", "volume up", "volume down",
    "mute", "search on google", "close google", "search on wikipedia", "send an email",
    "give me news", "shut down the system", "restart the system", "go to sleep", "refresh",
    "scroll down", "drag visual studio", "open chrome", "maximize this window",
    "google search", "open new window", "open incognito", "minimise this window",
    "open history", "open downloads", "previous tab", "next tab", "close tab",
    "close window", "clear browsing history", "close chrome", "weather", "movie",
    "subscribe", "screenshot", "click my photo", "rectangular spiral", "close paint",
    "what time", "current time", "the time", "tell me the time",
)

DATE_PHRASES = (
    "today's date", "todays date", "today date", "what date", "date today", "current date",
    "what day", "day today", "which day", "date and day", "day and date", "today's day",
)

class Jarvis(widget.Widget):
    def __init__(self, **kwargs):
        super(Jarvis, self).__init__(**kwargs)
        self.volume = 0
        self.volume_history = [0,0,0,0,0,0,0]
        self.volume_history_size = 140
      
        self.min_size = .2 * SCREEN_WIDTH
        self.max_size = .7 * SCREEN_WIDTH
        
        self.add_widget(image.Image(source='images/border.eps.png',size=(1920,1080)))
        self.circle = JarvisButton(size=(284.0,284.0),background_normal='images\circle.png')
        self.circle.bind(on_press=self.start_recording)
        self.start_recording()
        self.add_widget(image.Image(source='images/jarvis.gif', size=(self.min_size, self.min_size), pos=(SCREEN_WIDTH / 2 - self.min_size / 2, SCREEN_HEIGHT / 2 - self.min_size / 2)))
        
        time_layout = boxlayout.BoxLayout(orientation='vertical',pos=(150,900))
        self.time_label = label.Label(text='', font_size=24, markup=True,font_name='images/dusri.ttf')
        time_layout.add_widget(self.time_label)
        self.add_widget(time_layout)
        
        clock.Clock.schedule_interval(self.update_time, 1)
        
        self.title = label.Label(text='[b][color=3333ff]NATIONAL DEGREE COLLEGE BAGEPALLI CS DEPARTMENT[/color][/b]',font_size = 42,markup=True,font_name='images/mw.ttf',pos=(920,900))
        self.add_widget(self.title)
        
        self.subtitles_input = textinput.TextInput(
            text=f'Hey {USER_NAME}, I am {BOT_NAME}, your personal assistant',
            font_size=24,
            readonly=False,
            background_color=(0, 0, 0, 0),
            foreground_color=(1, 1, 1, 1),
            size_hint_y=None,
            height=80,
            pos=(720, 100),
            width=1200,
            font_name='images/teesri.otf',
        )
        self.add_widget(self.subtitles_input)
        
        self.vrh=label.Label(text='',font_size=30,markup=True,font_name='images/dusri.ttf',pos=(1500,500))
        self.add_widget(self.vrh)
        
        self.vlh=label.Label(text='',font_size=30,markup=True,font_name='images/dusri.ttf',pos=(400,500))
        self.add_widget(self.vlh)
        self.add_widget(self.circle)
        
    def take_command(self):
            """Listen for one follow-up answer (uses the already-open microphone)."""
            try:
                audio = self._r.listen(self._source, phrase_time_limit=15)
                text = self._r.recognize_google(audio, language='en-in')
                print(f"You: {text}")
                return text.lower()
            except Exception:
                speak("Sorry I couldn't understand. Can you please repeat that?")
                return 'none'

    def start_recording(self, *args):
            # Start the always-on listening loop (only once).
            t = getattr(self, "listen_thread", None)
            if t is not None and t.is_alive():
                return
            self.listen_thread = threading.Thread(target=self.listen_loop, daemon=True)
            self.listen_thread.start()

    def flush_mic(self):
            # Throw away audio captured while Jarvis was speaking, so it doesn't hear itself.
            try:
                stream = self._source.stream.pyaudio_stream
                n = stream.get_read_available()
                if n:
                    stream.read(n, exception_on_overflow=False)
            except Exception:
                pass

    def listen_loop(self):
            self._r = sr.Recognizer()
            self._r.pause_threshold = 0.8
            self._r.dynamic_energy_threshold = True
            with sr.Microphone() as source:
                self._source = source
                print("Calibrating microphone, please stay quiet for a second...")
                self._r.adjust_for_ambient_noise(source, duration=1)
                print(f"\n{BOT_NAME} is ready. Just keep asking questions. Say 'go to sleep' to stop.\n")
                while True:
                    try:
                        audio = self._r.listen(source, phrase_time_limit=20)
                    except Exception as e:
                        print(e)
                        continue
                    try:
                        query = self._r.recognize_google(audio, language="en-in")
                    except sr.UnknownValueError:
                        continue
                    except sr.RequestError as e:
                        print(e)
                        continue
                    print(f'\nYou: {query}')
                    clock.Clock.schedule_once(lambda dt, q=query: setattr(self.subtitles_input, 'text', q))
                    self.handle_jarvis_commands(query.lower())
                    self.flush_mic()

    def update_time(self,dt):
            current_time = time.strftime('TIME\n\t%H:%M:%S')
            self.time_label.text = f'[b][color=3333ff]{current_time}[/color][/b]'
              
    def update_circle(self, dt):
            try:
                self.size_value = int(np.mean(self.volume_history))
                
            except Exception as e:
                self.size_value = self.min_size
                print('Warning:',e)
                
            if self.size_value <= self.min_size:
                self.size_value = self.min_size
            elif self.size_value >= self.max_size:
                self.size_value = self.max_size                                     
            self.circle.size = (self.size_value,self.size_value)
            self.circle.pos = (SCREEN_WIDTH / 2 - self.circle.width / 2, SCREEN_HEIGHT / 2 - self.circle.height / 2)
            
            
    def update_volume(self,indata,frames,time,status):
            volume_norm = np.linalg.norm(indata) * 200
            self.volume = volume_norm
            self.volume_history.append(volume_norm)
            self.vrh.text = f'[b][color=3333ff]{np.mean(self.volume_history)}[/color][/b]'
            self.vlh.text = f'[b][color=3333ff]{np.mean(self.volume_history)}[/color][/b]'
            self.vlh.text = f'''[b][color=3344ff]
                {round(self.volume_history[0],7)}\n
                {round(self.volume_history[1],7)}\n
                {round(self.volume_history[2],7)}\n
                {round(self.volume_history[3],7)}\n
                {round(self.volume_history[4],7)}\n
                {round(self.volume_history[5],7)}\n
                {round(self.volume_history[6],7)}\n
                [/color][/b]'''
                
            self.vrh.text = f'''[b][color=3344ff]
                {round(self.volume_history[0],7)}\n
                {round(self.volume_history[1],7)}\n
                {round(self.volume_history[2],7)}\n
                {round(self.volume_history[3],7)}\n
                {round(self.volume_history[4],7)}\n
                {round(self.volume_history[5],7)}\n
                {round(self.volume_history[6],7)}\n
                [/color][/b]'''  
                
            if len(self.volume_history) > self.volume_history_size:
                self.volume_history.pop(0)  
                
    def start_listening(self):
            self.stream = sd.InputStream(callback=self.update_volume) 
            self.stream.start()
    
    def is_local_command(self, query):
        if query.startswith(("open ", "close ")):
            return True
        if any(p in query for p in DATE_PHRASES):
            return True
        return any(t in query for t in LOCAL_TRIGGERS)

    def chat_reply(self, query):
        if any(p in query for p in ("new chat", "forget everything", "reset chat")):
            self.chat = None
            speak("Okay, starting a fresh conversation.")
            return
        answer = self.get_gemini_response(query)
        answer = answer.replace("*", "").replace("#", "")
        print(f"\n{BOT_NAME}: {answer}\n")
        shown = answer if len(answer) < 350 else answer[:347] + "..."
        clock.Clock.schedule_once(lambda dt: setattr(self.subtitles_input, 'text', shown))
        speak(answer)

    def get_gemini_response(self,query):
        try:
            print("Thinking...")
            if getattr(self, "chat", None) is None:
                self.chat = model.start_chat(history=[])
            now = datetime.datetime.now().strftime("%A, %d %B %Y, %I:%M %p")
            response = self.chat.send_message(f"(Current date and time: {now}) {query}", request_options={"timeout": 30})
            return response.text
        except Exception as e:
            print(f"Error getting Gemini response ({type(e).__name__}): {e}")
            if not getattr(self, "_models_listed", False):
                self._models_listed = True
                try:
                    names = [m.name for m in genai.list_models()
                             if "generateContent" in m.supported_generation_methods]
                    print("Models your key can use:", ", ".join(names))
                    print("Put one of these names in .env as GEMINI_MODEL=<name without 'models/'>")
                except Exception as e2:
                    print(f"Could not list models: {e2}")
            return "I'm sorry, I couldn't process that request."
            
    def handle_jarvis_commands(self,query):  
            query = query.replace(BOT_NAME.lower(), "").replace("jarvis", "").strip(" ,.")
            if not query:
                return
            if not self.is_local_command(query):
                self.chat_reply(query)
                return
            try:
                if "how are you" in query:
                    speak("I am absolutely fine sir. What about you")

                elif "hello" in query:
                    speak("Hello sir, how are you ?")
                    
                elif "i am fine" in query:
                    speak("that's great, sir")
                    
                elif "how are you" in query:
                    speak("Perfect, sir")
                    
                elif "thank you" in query:
                    speak("you are welcome, sir")
                    
                elif "who are you" in query:
                   print(f'My name is {BOT_NAME}')
                   speak(f'My name is {BOT_NAME}')
                   print(f'I am your personal assistant, {USER_NAME}')
                   speak(f'I am your personal assistant, {USER_NAME}')

                elif "who created you" in query:
                      print('I Do not Know His Name, I created with Python Language, in Visual Studio Code.')
                      speak('I Do not Know His Name, I created with Python Language, in Visual Studio Code.')

                
                elif "play music" in query:
                    speak("Playing your favourite songs")
                    webbrowser.open("https://www.youtube.com/results?search_query=latest+songs")

                elif "open command prompt" in query:
                     os.system("start cmd")

                elif "close command prompt" in query:
                   os.system("taskkill /f /im cmd.exe")


                elif "camera" in query and "open" in query:
                    speak("Opening camera sir")
                    sp.run('start microsoft.windows.camera:', shell=True)

                elif "notepad" in query and "open" in query:
                    speak("Opening Notepad for you sir")
                    os.startfile("notepad.exe")

                elif "discord" in query and "open" in query:
                    speak("Opening Discord for you sir")
                    sp.run(os.path.expandvars(r'"%LOCALAPPDATA%\Discord\Update.exe" --processStart Discord.exe'), shell=True)

                elif 'ip address' in query:
                    ip_address = find_my_ip()
                    speak(
                        f'Your IP Address is {ip_address}.\n For your convenience, I am printing it on the screen sir.')
                    print(f'Your IP Address is {ip_address}')

                elif "youtube" in query:
                    speak("What do you want to play on youtube sir?")
                    video = self.take_command().lower()
                    youtube(video)
                    
                elif "volume up" in query:
                 pyautogui.press("volumeup")


                elif "volume down" in query:
                    pyautogui.press("volumedown")



                elif "mute" in query:
                   pyautogui.press("volumemute")


                elif "search on google" in query:
                    speak(f"What do you want to search on google")
                    query = self.take_command().lower()
                    search_on_google(query)
                    
                elif 'close google' in query:
                  os.system("taskkill /f /im msedge.exe")

                elif "search on wikipedia" in query:
                    speak("what do you want to search on wikipedia sir?")
                    search = self.take_command().lower()
                    results = search_on_wikipedia(search)
                    speak(f"According to wikipedia,{results}")
                

                elif "send an email" in query:
                    speak("On what email address do you want to send sir?. Please enter in the terminal")
                    receiver_add = input("Email address:")
                    speak("What should be the subject sir?")
                    subject = self.take_command().capitalize()
                    speak("What is the message ?")
                    message = self.take_command().capitalize()
                    if send_email(receiver_add, subject, message):
                        speak("I have sent the email sir")
                        print("I have sent the email sir")
                    else:
                        speak("something went wrong Please check the error log")

                    
                elif "give me news" in query:
                    speak(f"I am reading out the latest headline of today,sir")
                    speak(get_news())
                    speak("I am printing it on screen sir")
                    print(*get_news(), sep='\n')

                elif any(p in query for p in DATE_PHRASES):
                    today = datetime.datetime.now().strftime("%A, %d %B %Y")
                    print(today)
                    speak(f"{USER_NAME}, today is {today}")

                elif 'time' in query.split():
                 strTime = datetime.datetime.now().strftime("%I:%M %p")
                 print(strTime)
                 speak(f"{USER_NAME}, the time is {strTime}")


                elif "shut down the system" in query:
                     os.system("shutdown /s /t 5")


                elif "restart the system" in query:
                    os.system("shutdown /r /t 5")
                    
                elif "go to sleep" in query:
                  speak(' alright then, I am switching off')
                  sys.exit()
                  
                elif "refresh" in query:
                 pyautogui.moveTo(1551,551, 2)
                 pyautogui.click(x=1551, y=551, clicks=1, interval=0, button='right')
                 pyautogui.moveTo(1620,667, 1)
                 pyautogui.click(x=1620, y=667, clicks=1, interval=0, button='left')


                elif "scroll down" in query:
                   pyautogui.scroll(1000)


                elif "drag visual studio to the right" in query:
                      pyautogui.moveTo(46, 31, 2)
                      pyautogui.dragRel(1857, 31, 2)
                      
                elif'open chrome' in query: 
                  os.startfile('https://www.google.com/')
              
                elif 'maximize this window' in query:        
                    pyautogui.hotkey('alt', 'space')    
                    time.sleep(1)    
                    pyautogui.press('x') 
 
 
                elif 'google search' in query:     
                      query = query.replace("google search", "") 
                      pyautogui.hotkey('alt', 'd')         
                      pyautogui.write(f"{query}", 0.1)    
                      pyautogui.press('enter') 
 
 
                elif 'youtube search' in query:         
                      query = query.replace("youtube search", "")  
                      pyautogui.hotkey('alt', 'd')          
                      time.sleep(1)      
                      pyautogui.press('tab')  
                      pyautogui.press('tab')     
                      pyautogui.press('tab')    
                      pyautogui.press('tab')      
                      time.sleep(1)          
                      pyautogui.write(f"{query}", 0.1)       
                      pyautogui.press('enter') 
 
 
                elif 'open new window' in query:            
                     pyautogui.hotkey('ctrl', 'n')
                           
                elif 'open incognito window' in query:       
                      pyautogui.hotkey('ctrl', 'shift', 'n') 
 
 
                elif 'minimise this window' in query:      
                  pyautogui.hotkey('alt', 'space')       
                  time.sleep(1)         
                  pyautogui.press('n') 
 
 
                elif 'open history' in query:      
                     pyautogui.hotkey('ctrl', 'h') 
 
 
                elif 'open downloads' in query:      
                         pyautogui.hotkey('ctrl', 'j') 
 
 
                elif 'previous tab' in query: 
                   pyautogui.hotkey('ctrl', 'shift', 'tab') 
 
 
                elif 'next tab' in query: 
                    pyautogui.hotkey('ctrl', 'tab') 
 
 
                elif 'close tab' in query: 
                     pyautogui.hotkey('ctrl', 'w') 
 
 
                elif 'close window' in query: 
                    pyautogui.hotkey('ctrl', 'shift', 'w')  
                
                elif 'clear browsing history' in query: 
                   pyautogui.hotkey('ctrl', 'shift', 'delete') 
 
 
                elif 'close chrome' in query: 
                     os.system("taskkill /f /im chrome.exe")  

                    
                elif 'weather' in query:
                    ip_address = find_my_ip()
                    speak("tell me the name of your city")
                    city = input("Enter name of your city")
                    speak(f"Getting weather report for your city {city}")
                    weather, temp, feels_like = weather_forecast(city)
                    speak(f"The current temperature is {temp}, but it feels like {feels_like}")
                    speak(f"Also, the weather report talks about {weather}")
                    speak("For your convenience, I am printing it on the screen sir.")
                    print(f"Description: {weather}\nTemperature: {temp}\nFeels like: {feels_like}")

                elif "movie" in query:
                    movies_db = imdb.IMDb()
                    speak("Please tell me the movie name:")
                    text = self.take_command()
                    movies = movies_db.search_movie(text)
                    speak("searching for" + text)
                    speak("I found these")
                    for movie in movies:
                        title = movie["title"]
                        year = movie["year"]
                        speak(f"{title}-{year}")
                        info = movie.getID()
                        movie_info = movies_db.get_movie(info)
                        rating = movie_info["rating"]
                        cast = movie_info["cast"]
                        actor = cast[0:5]
                        plot = movie_info.get('plot outline', 'plot summary not available')
                        speak(f"{title} was released in {year} has imdb ratings of {rating}.It has a cast of {actor}. "
                            f"The plot summary of movie is {plot}")

                        print(f"{title} was released in {year} has imdb ratings of {rating}.\n It has a cast of {actor}. \n"
                            f"The plot summary of movie is {plot}")


                elif 'subscribe' in query:
                    speak(
                        "Everyone who are watching this video, Please subscribe for more amazing content from error by "
                        "night. I will show you how to do this")
                    speak("Firstly Go to youtube")
                    webbrowser.open("https://www.youtube.com/")
                    speak("click on the search bar")
                    pyautogui.moveTo(806, 125, 1)
                    pyautogui.click(x=806, y=125, clicks=1, interval=0, button='left')
                    speak("Error by night")
                    pyautogui.typewrite("Error by night", 0.1)
                    time.sleep(1)
                    speak("press enter")
                    pyautogui.press('enter')
                    pyautogui.moveTo(971, 314, 1)
                    speak("Here you will see our channel")
                    pyautogui.moveTo(1688, 314, 1)
                    speak("click here to subscribe our channel")
                    pyautogui.click(x=1688, y=314, clicks=1, interval=0, button='left')
                    speak("And also Don't forget to press the bell icon")
                    pyautogui.moveTo(1750, 314, 1)
                    pyautogui.click(x=1750, y=314, clicks=1, interval=0, button='left')
                    speak("turn on all notifications")
                    pyautogui.click(x=1750, y=320, clicks=1, interval=0, button='left')
                    
                elif "open" in query:   #EASY METHOD
                    query = query.replace("open","")
                    query = query.replace("jarvis","")
                    pyautogui.press("super")
                    pyautogui.typewrite(query)
                    pyautogui.sleep(2)
                    pyautogui.press("enter")
                    
                elif "open" in query:
                    from Dictapp import openappweb
                    openappweb(query)
                
                elif "close" in query:
                    from Dictapp import closeappweb
                    closeappweb(query)
                    
                    
                elif "screenshot" in query:
                     im = pyautogui.screenshot()
                     im.save("ss.jpg")

                elif "click my photo" in query:
                    pyautogui.press("super")
                    pyautogui.typewrite("camera")
                    pyautogui.press("enter")
                    pyautogui.sleep(2)
                    speak("SMILE")
                    pyautogui.press("enter")
                    
                elif "rectangular spiral" in query:
                     pyautogui.hotkey('win')
                     time.sleep(1)
                     pyautogui.write('paint')
                     time.sleep(1)
                     pyautogui.press('enter')
                     pyautogui.moveTo(100, 193, 1)
                     pyautogui.rightClick
                     pyautogui.click()
                     distance = 300
                     while distance > 0:
                          pyautogui.dragRel(distance, 0, 0.1, button="left")
                          distance = distance - 10
                          pyautogui.dragRel(0, distance, 0.1, button="left")
                          pyautogui.dragRel(-distance, 0, 0.1, button="left")
                          distance = distance - 10
                          pyautogui.dragRel(0, -distance, 0.1, button="left")

                elif "close paint" in query:
                     os.system("taskkill /f /im mspaint.exe")
            
                else:
                    gemini_response = self.get_gemini_response(query)
                    gemini_response = gemini_response.replace("*","")
                    if gemini_response and gemini_response != "I'm sorry, I couldn't process that request.":
                        speak(gemini_response)
                        print(gemini_response)
                
            except Exception as e:
                print(e)