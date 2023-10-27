from data_preprocessing import classify_intent, get_answer_by_intent
from dialogue_processing import generate_answer, get_failure_phrase

stats = {'intent': 0, 'generate': 0, 'failure': 0}


def bot(replica):
    intent = classify_intent(replica)

    if intent:
        answer = get_answer_by_intent(intent)
        if answer:
            stats['intent'] += 1
            return answer

    answer = generate_answer(replica)
    if answer:
        stats['generate'] += 1
        return answer

    stats['failure'] += 1
    return get_failure_phrase()
