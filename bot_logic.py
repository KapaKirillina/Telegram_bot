from data_preprocessing import classify_intent, get_answer_by_intent
from dialogue_processing import generate_answer, get_failure_phrase

stats = {'intent': 0, 'generate': 0, 'failure': 0}


def bot(replica) -> str:
    intent = classify_intent(replica)

    # выбор заготовленной реплики
    if intent:
        answer = get_answer_by_intent(intent)
        if answer:
            stats['intent'] += 1
            return answer

    # вызов генеративной модели
    answer = generate_answer(replica)
    if answer:
        stats['generate'] += 1
        return answer

    # берем заглушку
    stats['failure'] += 1
    return get_failure_phrase()
