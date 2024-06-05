import json
import nltk # type: ignore
from nltk.stem import WordNetLemmatizer # type: ignore
import pickle
import random

import numpy as np # type: ignore
import tensorflow as tf # type: ignore

nltk.download('punkt')  
nltk.download('wordnet')  

lemmatizer = WordNetLemmatizer()


words = pickle.load(open("words.pkl", "rb"))
classes = pickle.load(open("classes.pkl", "rb"))

def clean_up_sentence(sentence):
    word_list = nltk.word_tokenize(sentence)
    word_list = [lemmatizer.lemmatize(word.lower()) for word in word_list if word not in ["?", "!"]]
    return word_list


def bag_of_words(sentence):
    word_list = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for word in word_list:
        if word in words:
            bag[words.index(word)] = 1
    return bag


def predict_class(sentence):
    bag = bag_of_words(sentence)
    model = tf.keras.models.load_model("chatbot_simplilearnmodel.h5")
    results = model.predict(np.array([bag]))[0]
    class_index = np.argmax(results)
    class_label = classes[class_index]
    return class_label, results[class_index]


def get_response(sentence):
    class_label, p = predict_class(sentence)
    with open("intents.json", "r") as f:
        intents = json.load(f)

    for intent in intents["intents"]:
        if class_label == intent["tag"]:
            return random.choice(intent["responses"])


def chat():
    print("I am Jarvis, the chatbot.  How can I help you?")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break

        response = get_response(user_input)
        print(f"Jarvis: {response}")

chat()
