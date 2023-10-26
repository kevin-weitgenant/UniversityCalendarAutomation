import { useState } from 'react'
import EmbeddedGoogleCalendar from './EmbeddedGoogleCalendar'
import { getEmbeddedCalendarID, handleDownload } from './services/services'


function App() {
  
  const [email, setEmail] = useState('kcweitgenant@inf.ufpel.edu.br');
  const [calendarId, setCalendarId] = useState('');

  const exampleSchedule = `SEGUNDA-FEIRA
08:00 - 08:50	22000174 - T1 - ENGENHARIA DE SOFTWARE II	[ANG] 235 - Sala de Aula
08:50 - 09:40	22000174 - T1 - ENGENHARIA DE SOFTWARE II	[ANG] 235 - Sala de Aula
15:10 - 16:00	22000268 - T2 - CÁLCULO NUMÉRICO COMPUTACIONAL	[ANG] 220 - Sala de Aula
16:00 - 16:50	22000268 - T2 - CÁLCULO NUMÉRICO COMPUTACIONAL	[ANG] 220 - Sala de Aula
17:10 - 18:00	22000346 - T1 - TÓPICOS ESPECIAIS EM COMPUTAÇÃO V	[ANG] 330 - Laboratório Computação 2
18:00 - 18:50	22000346 - T1 - TÓPICOS ESPECIAIS EM COMPUTAÇÃO V	[ANG] 330 - Laboratório Computação 2
TERÇA-FEIRA
08:00 - 08:50	22000186 - T1 - COMPUTAÇÃO E SOCIEDADE	[ANG] 342 - Sala de aula
08:50 - 09:40	22000186 - T1 - COMPUTAÇÃO E SOCIEDADE	[ANG] 342 - Sala de aula
15:10 - 16:00	22000187 - T1 - COMPUTAÇÃO GRÁFICA	[ANG] 330 - Laboratório Computação 2
16:00 - 16:50	22000187 - T1 - COMPUTAÇÃO GRÁFICA	[ANG] 330 - Laboratório Computação 2
QUARTA-FEIRA
10:00 - 10:50	22000268 - T2 - CÁLCULO NUMÉRICO COMPUTACIONAL	[ANG] 336 - Laboratório Computação 5
10:50 - 11:40	22000268 - T2 - CÁLCULO NUMÉRICO COMPUTACIONAL	[ANG] 336 - Laboratório Computação 5
QUINTA-FEIRA
08:00 - 08:50	22000186 - T1 - COMPUTAÇÃO E SOCIEDADE	[ANG] 342 - Sala de aula
08:00 - 08:50	22000186 - T1 - COMPUTAÇÃO E SOCIEDADE	[ANG] 342 - Sala de aula
08:50 - 09:40	22000186 - T1 - COMPUTAÇÃO E SOCIEDADE	[ANG] 342 - Sala de aula
08:50 - 09:40	22000186 - T1 - COMPUTAÇÃO E SOCIEDADE	[ANG] 342 - Sala de aula
13:30 - 14:20	22000187 - T1 - COMPUTAÇÃO GRÁFICA	[ANG] 330 - Laboratório Computação 2
14:20 - 15:10	22000187 - T1 - COMPUTAÇÃO GRÁFICA	[ANG] 330 - Laboratório Computação 2
15:10 - 16:00	22000351 - T1 - TÓPICOS ESPECIAIS EM COMPUTAÇÃO X	[ANG] 220 - Sala de Aula
16:00 - 16:50	22000351 - T1 - TÓPICOS ESPECIAIS EM COMPUTAÇÃO X	[ANG] 220 - Sala de Aula
17:10 - 18:00	22000351 - T1 - TÓPICOS ESPECIAIS EM COMPUTAÇÃO X	[ANG] 330 - Laboratório Computação 2
18:00 - 18:50	22000351 - T1 - TÓPICOS ESPECIAIS EM COMPUTAÇÃO X	[ANG] 330 - Laboratório Computação 2
SEXTA-FEIRA
08:00 - 08:50	22000272 - T1 - INTROD PROCESSAMENTO PARALELO E DISTRIBUÍDO 	[ANG] 314 - Sala de aula
08:50 - 09:40	22000272 - T1 - INTROD PROCESSAMENTO PARALELO E DISTRIBUÍDO 	[ANG] 314 - Sala de aula
10:00 - 10:50	22000272 - T1 - INTROD PROCESSAMENTO PARALELO E DISTRIBUÍDO 	[ANG] 314 - Sala de aula
10:50 - 11:40	22000272 - T1 - INTROD PROCESSAMENTO PARALELO E DISTRIBUÍDO 	[ANG] 314 - Sala de aula
15:10 - 16:00	22000174 - T1 - ENGENHARIA DE SOFTWARE II	[ANG] 314 - Sala de aula
16:00 - 16:50	22000174 - T1 - ENGENHARIA DE SOFTWARE II	[ANG] 314 - Sala de aula
17:10 - 18:00	22000305 - M1 - TRABALHO DE CONCLUSÃO DE CURSO I	[ANG] 235 - Sala de Aula
18:00 - 18:50	22000305 - M1 - TRABALHO DE CONCLUSÃO DE CURSO I	[ANG] 235 - Sala de Aula`

const scheduleEU = `
SEGUNDA-FEIRA
10:00 - 10:50	22000303 - M1 - PROJETO DE COMPILADORES	[ANG] 343 - Sala de aula
10:50 - 11:40	22000303 - M1 - PROJETO DE COMPILADORES	[ANG] 343 - Sala de aula
QUINTA-FEIRA
10:00 - 10:50	22000303 - M1 - PROJETO DE COMPILADORES	[ANG] 235 - Sala de Aula
10:50 - 11:40	22000303 - M1 - PROJETO DE COMPILADORES	[ANG] 235 - Sala de Aula
SEXTA-FEIRA
17:10 - 18:00	22000306 - M1 - TRABALHO DE CONCLUSÃO DE CURSO II	[ANG] 342 - Sala de aula
18:00 - 18:50	22000306 - M1 - TRABALHO DE CONCLUSÃO DE CURSO II	[ANG] 342 - Sala de aula`

const [textSchedule, setTextSchedule] = useState(exampleSchedule);

  const handleGenerateCalendar = async () => {
    try {
      const calendarId = await getEmbeddedCalendarID(email, textSchedule);
      setCalendarId(calendarId);
    } catch (error) {
      console.error('Error generating embedded Google Calendar:', error);
    }
  };

  return (
    <div>
      <p>------------------------faça sua mágica</p>

      <input
        type="text"
        placeholder="Coloque o texto neste campo"
        value={textSchedule}
        onChange={(e) => setTextSchedule(e.target.value)}
      />

      <input
        type="text"
        placeholder="Coloque o seu e-mail neste campo"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />

      <button onClick={() => handleDownload(textSchedule)}>Download .ical</button>
      <button onClick={handleGenerateCalendar}>Gerar Embedded Google Calendar</button>
      
      <EmbeddedGoogleCalendar calendarId={calendarId} />
    </div>
  );
}

export default App
