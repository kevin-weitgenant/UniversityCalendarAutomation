import re
from typing import Dict, List
from parseCalendarText import parse_schedule_text
from generateIcal import writeCalendar,createCalendar


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


writeCalendar(createCalendar(parse_schedule_text(text)))