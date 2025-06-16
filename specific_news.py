import speech_recognition as sr
import pyttsx3
import requests

# News API Key
API_KEY = "e16ab92fe92f40a79194df2432b122e9"

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """Convert text to speech"""
    engine.say(text)
    engine.runAndWait()

def get_news(topic="general"):
    """Fetch news based on a specific topic"""
    URL = f"https://newsapi.org/v2/everything?q={topic}&apiKey={API_KEY}"
    
    try:
        response = requests.get(URL)
        data = response.json()
        articles = data.get("articles", [])

        if not articles:
            return f"Sorry, no news found for {topic}."

        news_list = [f"{i+1}. {news['title']}" for i, news in enumerate(articles[:5])]
        return "\n".join(news_list)

    except Exception as e:
        return f"Error fetching news: {str(e)}"

def recognize_voice():
    """Listen to user's voice command"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening... Say a topic like 'technology news' or 'sports news'.")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        command = recognizer.recognize_google(audio).lower()
        return command
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        return "API unavailable"

# Main program loop
if __name__ == "__main__":
    speak("What type of news would you like to hear?")
    print("Listening for a topic...")

    command = recognize_voice()
    
    if command:
        topic = command.replace("news", "").strip()  # Extract the topic
        speak(f"Fetching {topic} news...")
        news = get_news(topic)
        speak(news)
        print(news)
    else:
        speak("I didn't understand. Please try again.")
