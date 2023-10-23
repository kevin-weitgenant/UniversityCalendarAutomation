import re
from typing import Dict, List

text = """
ÑÃO FINROMADO
SEGUNDA-FEIRA
10:00 - 10:50    22000303 - M1 - PROJETO DE COMPILADORES    [ANG] 343 - Sala de aula
10:50 - 11:40    22000303 - M1 - PROJETO DE COMPILADORES    [ANG] 343 - Sala de aula
QUINTA-FEIRA
10:00 - 10:50    22000303 - M1 - PROJETO DE COMPILADORES    [ANG] 235 - Sala de Aula
10:50 - 11:40    22000303 - M1 - PROJETO DE COMPILADORES    [ANG] 235 - Sala de Aula
SEXTA-FEIRA
17:10 - 18:00    22000306 - M1 - TRABALHO DE CONCLUSÃO DE CURSO II    [ANG] 342 - Sala de aula
18:00 - 18:50    22000306 - M1 - TRABALHO DE CONCLUSÃO DE CURSO II    [ANG] 342 - Sala de aula"""


def merge_events(dictionaryVariable: dict) -> dict:
    merged_dictionary = {}

    for day, events in dictionaryVariable.items():
        merged_events = []
        i = 0
        while i < len(events):
            current_event = events[i]
            # If there's a next event and it has the same subject as the current event
            if i + 1 < len(events) and current_event['subject'] == events[i + 1]['subject']:
                next_event = events[i + 1]
                # If the end time of the current event is the start time of the next event
                if current_event['time'].split(' - ')[1] == next_event['time'].split(' - ')[0]:
                    # Merge the events
                    merged_event = {
                        'time': current_event['time'].split(' - ')[0] + ' - ' + next_event['time'].split(' - ')[1],
                        'subject': current_event['subject'],
                        'location': current_event['location'] if current_event['location'] == next_event['location'] else current_event['location'] + ', ' + next_event['location']
                    }
                    current_event = merged_event  # Set the current event to the merged event
                    i += 1  # Skip the next event

            merged_events.append(current_event)
            i += 1

        merged_dictionary[day] = merged_events

    return merged_dictionary




def parse_schedule_text(scheduleText: str = text) -> Dict[str, List[Dict[str, str]]]:
    schedule = {}
    weekdays = ['SEGUNDA-FEIRA', 'TERCA-FEIRA', 'QUARTA-FEIRA', 'QUINTA-FEIRA', 'SEXTA-FEIRA', 'SABADO', 'DOMINGO']
    lines = scheduleText.splitlines()
    current_day = None

    # create dictionary with keys as weekdays and values as a list with every index as one class time entry
    #{'SEGUNDA-FEIRA': ['10:00 - 10:50    22000303 - M1 - PROJETO DE COMPILADORES    [ANG] 343 - Sala de aula', '10:50 - 11:40    22000303 - M1 - PROJETO DE COMPILADORES    [ANG] 343 - Sala de aula'], 'QUINTA-FEIRA': ['10:00 - 10:50    22000303 - M1 - PROJETO DE COMPILADORES    [ANG] 235 - Sala de Aula', '10:50 - 11:40    22000303 - M1 - PROJETO DE COMPILADORES    [ANG] 235 - Sala de Aula'], 'SEXTA-FEIRA': ['17:10 - 18:00    22000306 - M1 - TRABALHO DE CONCLUSÃO DE CURSO II    [ANG] 342 - Sala de aula', '18:00 - 18:50    22000306 - M1 - TRABALHO DE CONCLUSÃO DE CURSO II    [ANG] 342 - Sala de aula']}
    for line in lines:
        if line in weekdays:
            current_day = line
            schedule[current_day] = []
        elif current_day is not None:
            schedule[current_day] += line.strip().split('\n')


    # the dictionary schedule will be updated in a way that the keys will continue to be the days of the week but
    # values will be a list of dictionaries, every dictionary being a class time entry
    # and this dictionary will have keys: time,subject,location
    for key,value in schedule.items():
        lst = []
        for entry in value:
            parts = re.split(r'\s{2,}', entry)
            time = parts[0]
            subject = parts[1].split('-')[-1]
            location = parts[2].split('-')[0]
            lst.append({'time':time,
                        'subject': subject,
                        'location' :location})
        schedule[key]= lst




# schedule = parse_schedule(text)