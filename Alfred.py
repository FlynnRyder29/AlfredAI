import pyttsx3, datetime, speech_recognition as sr
import wikipedia, webbrowser, os, random
import tkinter as tk
import threading
from PIL import Image, ImageTk  # Import from the Python Imaging Library (PIL)
import queue

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices)
engine.setProperty('voice', voices[0].id)
output_queue = queue.Queue()


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishme():
    hour = int(datetime.datetime.now().hour)
    if 6 <= hour < 12:
        output_queue.put("Good Morning Sir!! I hope your breakfast was Delicious!")
        speak("Good Morning Sir!! I hope your breakfast was Delicious!")
    elif 12 <= hour < 17:
        output_queue.put("Good Afternoon Sir!! I hope your Lunch was scrumptious!")
        speak("Good Afternoon Sir!! I hope your Lunch was scrumptious!")
    elif 17 <= hour < 19:
        output_queue.put("Good Evening Sir!! I hope your Hi-Tea was yum-yum! Please make sure to see the sunset,Sir")
        speak("Good Evening Sir!! I hope your Hi-Tea was yum-yum! Please make sure to see the sunset,Sir")
    else:
        output_queue.put("Good Night Sir!! I hope your Dinner was Moreish! Make sure to get plenty of rest!")
        speak("Good Night Sir!! I hope your Dinner was Moreish! Make sure to get plenty of rest!")
    output_queue.put("Alfred at your service Sir, How may I help you..")
    speak("Alfred at your service Sir, How may I help you..")


def takeCommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening......")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing......")
        query = r.recognize_google(audio, language='en-us')
        print(f"User Said: {query}\n")

    except Exception as e:
        print("Can you Repeat ,Sir!")
        output_queue.put("Can you Repeat ,Sir!")
        speak('Can you Repeat ,Sir!')
        return "None"
    return query


def backend():
    wishme()
    while True:
        query = takeCommand().lower()

        # logic for executing code
        if 'wikipedia' in query:
            speak('Searching in wikipedia......')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to wikipedia")
            print(results)
            speak(results)
            output_queue.put(results)

        elif 'open youtube' in query:
            output_queue.put('Opening youtube for you sir')
            webbrowser.open('youtube.com')

        elif 'open google' in query:
            output_queue.put("Opening google for you sir")
            webbrowser.open('google.com')

        elif 'open stackoverflow' in query:
            output_queue.put("Opening stackoverflow for you sir")
            webbrowser.open('stackoverflow.com')

        elif 'play music' in query:
            output_queue.put("Playing music for you sir")
            music_dir = "C:\\Users\\rocks\\Music"
            songs = os.listdir(music_dir)
            print(songs)
            kl = songs[random.randint(0, len(songs) - 1)]
            os.startfile(os.path.join(music_dir, kl))
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, The time is: {strTime}")
            output_queue.put(f"Sir, The time is: {strTime}")

        elif 'open brave' in query:
            output_queue.put("opening brave browser for you sir")
            codePath = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
            os.startfile(codePath)

        elif 'open chrome' in query:
            output_queue.put("opening chrome browser for you sir")
            codePath = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
            os.startfile(codePath)

        elif 'open teams' in query:
            output_queue.put("opening teams for you sir")
            codePath = r"C:\Users\rocks\AppData\Local\Microsoft\Teams\Update.exe"
            os.startfile(codePath)

        elif 'leave' in query:
            output_queue.put("Au revoir! Please take care sir!!!")
            speak("Au revoir! Please take care sir!!!")
            quit()

        elif 'open Pycharm' in query:
            output_queue.put("opening Pycharm for you sir")
            codePath = r"C:\Program Files\JetBrains\PyCharm Community Edition 2021.3.1\bin\pycharm64.exe"
            os.startfile(codePath)

        elif 'your creator' in query:
            output_queue.put("I was created by Sir Piyush Singh")
            speak(' I was created by Sir Piyush Singh.')

        elif 'depressed' in query:
            speak('Boldly go in the direction of your dreams.Stand tall and show the world what you are made of.\n'
                  ' When the world beats you down, find a reason to get back up again. Never give up on the success.'
                  'Try, try, try and try again. Feed your mind ideas of success, not failure.'
                  'Remember, the only way you can fail is if you give up. Every time you fail, you come one step '
                  'closer to success. '
                  'You are not scared; you are courageous. You are not weak; you are powerful. You are not '
                  'ordinary; you are remarkable. '
                  'Do not back down, do not give up.')
        elif 'thank you' in query:
            output_queue.put('You are most Welcome,sir!!! Its my job to see your every decent wish is fulfilled')
            speak('You are most Welcome,sir!!! Its my job to see your every decent wish is fulfilled')

        elif 'sad' in query:
            output_queue.put("Let me tell you a joke my friend!!")
            speak('Let me tell you a joke my friend!!')
            output_queue.put('Why can’t you send a duck to space? Because the bill would be astronomical!')
            speak(' What did one toilet say to the other?........You look a bit flushed.......hahahahahhahahahaha')

        elif 'joke' in query:
            output_queue.put('what  did the toaster say to the slice of bread?..... I want you inside me.')
            speak('What did the toaster say to the slice of bread?..... I want you inside me.')


def display_output(output_text_widget):
    while True:
        try:
            output = output_queue.get_nowait()
            output_text_widget.insert(tk.END, output + "\n")
            output_queue.task_done()
        except queue.Empty:
            pass


def main():
    # ... (other threads)

    # Create the Tkinter window
    root = tk.Tk()
    root.title("Alfred AI")

    # Load and display an image
    image_path = r"C:\Users\rocks\PycharmProjects\ErenAI\alfred.jpg"  # Replace with the path to your image
    image = Image.open(image_path)
    image = image.resize((860, 480), Image.ANTIALIAS)  # Resize the image as needed
    photo = ImageTk.PhotoImage(image)
    image_label = tk.Label(root, image=photo)
    image_label.image = photo
    image_label.pack()

    # Create a scrolled text widget to display output
    output_text = tk.Text(root, wrap=tk.WORD, height=100, width=100, font=("Helvetica", 12))
    output_text.pack(padx=10, pady=10)

    backend_thread = threading.Thread(target=backend)
    backend_thread.daemon = True
    backend_thread.start()

    display_thread = threading.Thread(target=display_output, args=(output_text,))
    display_thread.daemon = True
    display_thread.start()

    def leave():
        output_queue.put("Au revoir! Please take care sir!!!")
        speak("Au revoir! Please take care sir!!!")
        root.destroy()

    root.mainloop()


if __name__ == '__main__':
    # Start the main program
    main()
