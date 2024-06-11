# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 00:15:08 2024

@author: LENOVO
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import speech_recognition as sr
from googletrans import Translator

class SpeechApp(App):
    def build(self):
        self.recognizer = sr.Recognizer()
        self.translator = Translator()

        self.layout = BoxLayout(orientation='vertical', padding=10)

        self.arabic_to_english_button = Button(text="Convert Arabic to English")
        self.arabic_to_english_button.bind(on_press=self.convert_arabic_to_english)
        self.layout.add_widget(self.arabic_to_english_button)

        self.english_to_arabic_button = Button(text="Convert English to Arabic")
        self.english_to_arabic_button.bind(on_press=self.convert_english_to_arabic)
        self.layout.add_widget(self.english_to_arabic_button)

        self.output_label = Label(text="Output:")
        self.layout.add_widget(self.output_label)

        self.output_entry = TextInput(multiline=False, readonly=True)
        self.layout.add_widget(self.output_entry)

        return self.layout

    def speech_to_text(self, language):
        with sr.Microphone() as source:
            print(f"Say something in {language}...")
            audio = self.recognizer.listen(source)

            try:
                text = self.recognizer.recognize_google(audio, language=language)
                print(f"Recognized Text: {text}")
                return text
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")

        return None

    def translate_text(self, text, src_lang, dest_lang):
        translated = self.translator.translate(text, src=src_lang, dest=dest_lang)
        print(f"Translated Text: {translated.text}")
        return translated.text

    def convert_arabic_to_english(self, instance):
        arabic_text = self.speech_to_text(language='ar-SA')
        if arabic_text:
            english_text = self.translate_text(arabic_text, src_lang='ar', dest_lang='en')
            self.output_entry.text = english_text
        else:
            self.output_entry.text = "Could not recognize any speech."

    def convert_english_to_arabic(self, instance):
        english_text = self.speech_to_text(language='en-US')
        if english_text:
            arabic_text = self.translate_text(english_text, src_lang='en', dest_lang='ar')
            self.output_entry.text = arabic_text
        else:
            self.output_entry.text = "Could not recognize any speech."

if __name__ == '__main__':
    SpeechApp().run()
