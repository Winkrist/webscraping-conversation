import speech_recognition as sr #speech to text
import pyaudio #speechtotext
from fuzzywuzzy import fuzz #product lookup to the scraped data
from fuzzywuzzy import process  #product lookup to the scraped data
from gtts import gTTS  #google text to speech
import pyttsx3 #text to speech
import yake #keyword

class audio:
    
    def __init__(self):
        
        print("audio class initialised")

    #voice recognition/speech to text
    def speechtotext(self):
            
            recognizer = sr.Recognizer()
            to_search = []
            with sr.Microphone() as source:
                    print('Your input:')
                    audio = recognizer.listen(source, timeout=10)

            try:
                text = recognizer.recognize_google(audio)
                print('You are searching for: {}'.format(text))
                to_search.append(text)
            except:
                print("Sorry I don't understand, can you repeat?")
            
            return to_search
        
    # initialize Text-to-speech engine 
    def texttospeech(self, tts_input):  
        engine = pyttsx3.init()
        engine.setProperty('rate', 125)  
        # convert this text to speech  
        text = tts_input  
        engine.say(text)  
        # play the speech  
        engine.runAndWait()
        
    def keyword_extract(self,phrase):

        kw_extractor = yake.KeywordExtractor()
        text = phrase
        language = 'en'
        max_ngram_size = 1
        deduplication_threshold = 0.5
        numOfKeywords = 10
        custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, top=numOfKeywords, features=None)
        keywords = custom_kw_extractor.extract_keywords(text)

        search_term = []

        print(keywords)

        for kw in keywords:
            search_term.append(kw[0]) 
        
        return search_term  