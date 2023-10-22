import re
from typing import Dict, List


def parse_schedule_text(scheduleText: str) -> Dict[str, List[Dict[str, str]]]:
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
    return schedule