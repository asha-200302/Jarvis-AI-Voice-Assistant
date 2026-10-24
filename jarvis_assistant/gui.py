from __future__ import with_statement
import pyttsx3
import speech_recognition as sr
import datetime
import keyboard
import os
import subprocess as sp
import wikipedia
import imdb
import wolframalpha
import pyautogui
import webbrowser
import time
import sys
from datetime import datetime
from const import SCREEN_HEIGHT,SCREEN_WIDTH,GEMINI_API_KEY
import google.generativeai as genai
from jarvis_button import JarvisButton




from datetime import datetime
from decouple import config
from random import choice
from const import random_text
from utils import find_my_ip, search_on_google, search_on_wikipedia, youtube, send_email, get_news, weather_forecast

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

USER = config('USER_NAME', default='Asha')
HOSTNAME = config('BOT_NAME', default='Jarvis')


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def greet_me():
    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        speak(f"Good morning {USER}")
    elif (hour >= 12) and (hour <= 16):
        speak(f"Good afternoon {USER}")
    elif (hour >= 16) and (hour < 19):
        speak(f"Good evening {USER}")
    speak(f"I am {HOSTNAME}. How may i assist you? {USER}")


listening = False


def start_listening():
    global listening
    listening = True
    print("started listening ")


def stop_listening():
    global listening
    listening = False
    print("stopped listening")


keyboard.add_hotkey('ctrl+alt+k', start_listening)
keyboard.add_hotkey('ctrl+alt+p', stop_listening)


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing....")
        queri = r.recognize_google(audio, language='en-in')
        print(queri)

    except Exception:
        speak("Sorry I couldn't understand. Can you please repeat that?")
        return 'None'
    return queri


if __name__ == "__main__":
    greet_me()
    while True:
        query = take_command().lower()
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
            print('My Name Is Six')
            speak('My Name Is Six')
            print('I can Do Everything that my creator programmed me to do')
            speak('I can Do Everything that my creator programmed me to do')

        elif "who created you" in query:
            print('I Do not Know His Name, I created with Python Language, in Visual Studio Code.')
            speak('I Do not Know His Name, I created with Python Language, in Visual Studio Code.')

                
        elif "play music" in query:
                    speak("Playing your favourite songs, sir")
                    a = (1,2,3)
                    b = random_text(a)
                    if b==1:
                        webbrowser.open("https://www.youtube.com/watch?v=E3jOYQGu1uw&t=1246s&ab_channel=scientificoder")
                        
       
        elif "open command prompt" in query:
            os.system("start cmd")

        elif "close command prompt" in query:
                 os.system("taskkill /f /im cmd.exe")


        elif "open camera" in query:
            speak("Opening camera sir")
            sp.run('start microsoft.windows.camera:', shell=True)

        elif "open notepad" in query:
            npath = "C:\WINDOWS\system32\\notepad.exe"
            os.startfile(npath)

        elif "close notepad" in query:
            os.system("taskkill /f /im notepad.exe")

        elif 'ip address' in query:
            ip_address = find_my_ip()
            speak(f'Your IP Address is {ip_address}.\n For your convenience, I am printing it on the screen sir.')
            print(f'Your IP Address is {ip_address}')

        elif "open youtube" in query:
            speak("What do you want to play on youtube sir?")
            video = take_command().lower()
            youtube(video)
            
        elif "volume up" in query:
            pyautogui.press("volumeup")


        elif "volume down" in query:
            pyautogui.press("volumedown")



        elif "mute" in query:
            pyautogui.press("volumemute")


        elif "open google" in query:
            speak(f"What do you want to search on google {USER}")
            query = take_command().lower()
            search_on_google(query)
            
        elif 'close google' in query:
            os.system("taskkill /f /im msedge.exe")


        elif "wikipedia" in query:
            speak("what do you want to search on wikipedia sir?")
            search = take_command().lower()
            results = search_on_wikipedia(search)
            speak(f"According to wikipedia,{results}")
            speak("I am printing in on terminal")
            print(results)

        elif "send an email" in query:
            speak("On what email address do you want to send sir?. Please enter in the terminal")
            receiver_add = input("Email address:")
            speak("What should be the subject sir?")
            subject = take_command().capitalize()
            speak("What is the message ?")
            message = take_command().capitalize()
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
            
        elif 'the time' in query:
                 strTime = datetime.now().strftime("%H:%M:%S")
                 speak(f"Sir, the time is {strTime}")


        elif "shut down my system" in query:
            os.system("shutdown /s /t 5")


        elif "restart my system" in query:
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
            text = take_command()
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

        elif "calculate" in query:
            app_id = "J2E654-AVLVY7ERUA"
            client = wolframalpha.Client(app_id)
            ind = query.lower().split().index("calculate")
            text = query.split()[ind + 1:]
            result = client.query(" ".join(text))
            try:
                ans = next(result.results).text
                speak("The answer is " + ans)
                print("The answer is " + ans)
            except StopIteration:
                speak("I couldn't find that . Please try again")

        elif 'what is' in query or 'who is' in query or 'which is' in query:
            app_id = "J2E654-AVLVY7ERUA"
            client = wolframalpha.Client(app_id)

            try:

                ind = query.lower().index('what is') if 'what is' in query.lower() else \
                    query.lower().index('who is') if 'who is' in query.lower() else \
                        query.lower().index('which is') if 'which is' in query.lower() else None

                if ind is not None:
                    text = query.split()[ind + 2:]
                    res = client.query(" ".join(text))
                    ans = next(res.results).text
                    speak("The answer is " + ans)
                    print("The answer is " + ans)
                else:
                    speak("I couldn't find that. Please try again.")
            except StopIteration:
                speak("I couldn't find that. Please try again.")

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
                     import pyautogui #pip install pyautogui
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
            
                    
                    
        
                    
                

                    
        
                