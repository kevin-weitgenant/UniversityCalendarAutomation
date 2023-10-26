from enum import Enum
import re
from typing import Dict, List, Any
from pydantic import BaseModel
from datetime import datetime

class classDetails(BaseModel):
    startTime: datetime
    endTime: datetime

    subject: str
    location: str

class Weekday(Enum):
    SEGUNDA_FEIRA = 0
    TERÇA_FEIRA = 1
    QUARTA_FEIRA = 2
    QUINTA_FEIRA = 3
    SEXTA_FEIRA = 4
    SABADO = 5
    DOMINGO = 6

def rename_keys(dictionary: Dict[str, str]) -> Dict[Weekday, str]:
    return {Weekday[key.replace("-", "_").upper()]: value for key, value in dictionary.items() if key.replace("-", "_").upper() in Weekday.__members__}

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


def remove_duplicates(input_dict: Dict[str, List[Dict[str, Any]]]) -> Dict[str, List[Dict]]:
    result = {}

    for key, values in input_dict.items():
        unique_values = []
        for value in values:
            if value not in unique_values:
                unique_values.append(value)
        result[key] = unique_values

    return result

def preliminary_text_to_dict(scheduleText: str) -> Dict[str, str]:  # just use the function to be more clear the output
    schedule = {}
    weekdays = ['SEGUNDA-FEIRA', 'TERÇA-FEIRA', 'QUARTA-FEIRA', 'QUINTA-FEIRA', 'SEXTA-FEIRA', 'SABADO', 'DOMINGO']
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
            parts = re.split('\t', entry)
            time = parts[0]
            subject = parts[1].split('-')[-1]
            location = parts[2].split('-')[0]
            lst.append({'time':time,
                        'subject': subject,
                        'location' :location})
        schedule[key]= lst


        
    return merge_events(remove_duplicates(schedule))


def parse_schedule_text(scheduleText: str) -> Dict[Weekday, List[classDetails]]:
    
    preliminary_dict = preliminary_text_to_dict(scheduleText)
    scheduleDict = rename_keys(preliminary_dict)
    
    for day, classes in scheduleDict.items():
      for index, classDetails in enumerate(classes):
        startTimeString = classDetails.get('time').split('-')[0].strip()
        endTimeString = classDetails.get('time').split('-')[-1].strip()

        startTime = datetime.strptime(startTimeString, '%H:%M')
        endTime = datetime.strptime(endTimeString, '%H:%M')
        scheduleDict[day][index]['startTime'] = startTime
        scheduleDict[day][index]['endTime'] = endTime
        del classDetails['time']
    
    return scheduleDict
    