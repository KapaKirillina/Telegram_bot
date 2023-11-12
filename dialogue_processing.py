import nltk
from data_preprocessing import clear_phrase
from config import BOT_CONFIG
import random
from typing import Union

# Обработка диалогов из файла conversation.txt
with open('conversation.txt', encoding='utf-8') as f:
    content = f.read()

dialogues_str = content.split('\n\n')
dialogues = [dialogue_str.split('\n')[:2] for dialogue_str in dialogues_str]

dialogues_filtered = []
questions = set()

for dialogue in dialogues:
    if len(dialogue) != 2:
        continue

    question, answer = dialogue
    question = clear_phrase(question[2:])
    answer = answer[2:]

    if question != '' and question not in questions:
        questions.add(question)
        dialogues_filtered.append([question, answer])

dialogues_structured = {}

for question, answer in dialogues_filtered:
    words = set(question.split(' '))
    for word in words:
        if word not in dialogues_structured:
            dialogues_structured[word] = []
        dialogues_structured[word].append([question, answer])

dialogues_structured_cut = {}

for word, pairs in dialogues_structured.items():
    pairs.sort(key=lambda pair: len(pair[0]))
    dialogues_structured_cut[word] = pairs[:1000]

# Генерация ответа на основе входной фразы
def generate_answer(replica) -> Union[str, None]:
    replica = clear_phrase(replica)
    words = set(replica.split(' '))
    mini_dataset = []
    for word in words:
        if word in dialogues_structured_cut:
            mini_dataset += dialogues_structured_cut[word]

    answers = []  # [[distance_weighted, question, answer]]

    for question, answer in mini_dataset:
        if abs(len(replica) - len(question)) / len(question) < 0.2:
            distance = nltk.edit_distance(replica, question)
            distance_weighted = distance / len(question)
            if distance_weighted < 0.2:
                answers.append([distance_weighted, question, answer])

    if answers:
        return min(answers, key=lambda three: three[0])[2]

# Генерация ответа в случае неудачи
def get_failure_phrase() -> str:
    failure_phrases = BOT_CONFIG['failure_phrases']
    return random.choice(failure_phrases)
