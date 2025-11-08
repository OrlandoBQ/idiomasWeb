# study/utils.py
from datetime import date, timedelta

def sm2(score, scheduling_data):
    """
    Implementa el algoritmo SM-2 (Anki style)
    """
    if score < 3:
        scheduling_data.repetitions = 0
        scheduling_data.interval = 1
    else:
        if scheduling_data.repetitions == 0:
            scheduling_data.interval = 1
        elif scheduling_data.repetitions == 1:
            scheduling_data.interval = 6
        else:
            scheduling_data.interval *= scheduling_data.ease_factor

        scheduling_data.repetitions += 1

    scheduling_data.ease_factor = max(1.3, scheduling_data.ease_factor + (0.1 - (5 - score) * (0.08 + (5 - score) * 0.02)))
    scheduling_data.due_date = date.today() + timedelta(days=round(scheduling_data.interval))
    scheduling_data.save()
    return scheduling_data
