import re 
from collections import defaultdict
from dateutil.rrule import rrule, WEEKLY, MO
from datetime import date, datetime, timedelta
from icalendar import Calendar, Event,Alarm
import pytz
import uuid
import os

def create_calendar(dicionario):
  conversao = {'SEGUNDA-FEIRA': 0, 'TERÇA-FEIRA':1, 'QUARTA-FEIRA':2,'QUINTA-FEIRA':3,'SEXTA-FEIRA':4,'SÁBADO':5,'DOMINGO':6, 'SABADO' : 5}
  dicionario = rename_keys(dicionario,conversao)
  cal = Calendar()
  cal.add('prodid', '-//Google Inc//Google Calendar 70.9054//EN')
  cal.add('version', '2.0')

  #---------------------- 
  # atribuition of info recorded in the dictionary into the event
  for k,v in dicionario.items():
    for key, value in v.items():
      next_day = rrule(freq=WEEKLY, dtstart=date.today(), byweekday=k, count=1)[0]
      time = datetime.strptime(ajustar(value)[0][0], '%H:%M')
      end_time = datetime.strptime(ajustar(value)[0][1], '%H:%M')
      
      comeco = datetime(next_day.year,next_day.month,next_day.day, time.hour, time.minute)
      fim = datetime(next_day.year,next_day.month,next_day.day, end_time.hour, end_time.minute)

      criar_evento(cal,key,comeco, fim)
  #--------------------------
  
  basedir = os.path.abspath(os.path.dirname(__file__))
  filepath = os.path.join(basedir,f'calendars/{uuid.uuid4().hex}.ics')
  with open(f'{filepath}', 'wb') as fw:
    fw.write(cal.to_ical())
  return filepath

def criar_evento(cal,nome,inicio, fim): #comeco:datetime
                                        # fim: datetime

  event = Event()
  event.add('summary', nome)

  tzone = pytz.timezone('America/Sao_Paulo')

  event.add('dtstart', tzone.localize(inicio, is_dst=None))
  event.add('dtend', tzone.localize(fim, is_dst=None))
  event.add('rrule', {'freq': ['WEEKLY']})

  alarm = Alarm()
  alarm.add('action', 'DISPLAY')
  alarm.add('trigger', timedelta(minutes=-10))

  event.add_component(alarm)

  cal.add_component(event)


def criar_dicionario(string):
  linhas = string.split(sep = '\n')
  dicionario = defaultdict(lambda : [])
  #EXTRAIR OS DIAS 
  for x in range(len(linhas) -1):
    
    extraido = re.findall(r'^[^\d]*$',linhas[x])  #CHECA SE NÃO TEM NENHUM NÚMERO, CASO NAO TENHA, É UM DIA DA SEMANA
    if len(extraido)>0:
      dia = extraido[0].rstrip()
      linha_valida = True
      x = x+1
      
      disciplina_dict = defaultdict(lambda : [])
      while( linha_valida  and x< len(linhas)):
        if(len(re.findall(r'^[^\d]*$',linhas[x])) ==0 ):
          #EXTRAIR O NOME DA DISCIPLINA
          aux = linhas[x].split(sep = '-')[-1]
          aux = re.findall(r'(.*)\sNão informado',aux)         
          disciplina = aux[0].strip()
          #EXTRAIR AS HORAS
          horas = re.findall(r'\d{2}:\d{2}',linhas[x])  
          x = x+1
          disciplina_dict[disciplina].append(horas)
        else: 
          linha_valida = False
      
      dicionario[dia] = dict(disciplina_dict)
      disciplina_dict = defaultdict(lambda : [])
  
  
  return dict(dicionario)

def rename_keys(d, keys):
    return dict([(keys.get(k), v) for k, v in d.items()])

def ajustar(lista):
  lista2 = list()
  aux = list()

  if len(lista) == 1:
    return [(lista[0][0],lista[0][1])]

  for x in range(len(lista) -1):
    passou = False
    fim = lista[x][1]
    for y in range (x+1,len(lista)):
      if fim == lista[y][0]:
        passou = True
        fim = lista[y][1]
        
    if passou and fim not in aux:
      lista2.append( (lista[x][0],fim))
      aux.append(fim)
    else:
      if fim not in aux:
        lista2.append((lista[x][0], fim))

  return lista2     