import nltk
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer
from config import BOT_CONFIG
import random
from typing import Union

# Функция для очистки фразы от ненужных символов
def clear_phrase(phrase) -> str:
    phrase = phrase.lower()
    alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя- '
    result = ''.join(symbol for symbol in phrase if symbol in alphabet)
    return result.strip()


X_text = []
Y = []

for intent, intent_data in BOT_CONFIG['intents'].items():
    for example in intent_data['examples']:
        X_text.append(example)
        Y.append(intent)

vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(3, 3))
X = vectorizer.fit_transform(X_text)
clf = LinearSVC()
clf.fit(X, Y)

# Функция для классификации намерения по фразе
def classify_intent(replica) -> Union[str, None]:
    replica = clear_phrase(replica)

    intent = clf.predict(vectorizer.transform([replica]))[0]

    for example in BOT_CONFIG['intents'][intent]['examples']:
        example = clear_phrase(example)
        distance = nltk.edit_distance(replica, example)
        if example and distance / len(example) <= 0.5:
            return intent

# # Функция для получения ответа по намерению
def get_answer_by_intent(intent) -> Union[str, None]:
    if intent in BOT_CONFIG['intents']:
        responses = BOT_CONFIG['intents'][intent]['responses']
        if responses:
            return random.choice(responses)
