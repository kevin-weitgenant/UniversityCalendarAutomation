import axios from 'axios';

const apiUrl = 'http://localhost:5000';

export const getIcal = async () => {
  try {
    const response = await axios.get(`${apiUrl}/getIcal`);
    return response.data;
  } catch (error) {
    console.error('Error fetching iCal:', error);
    throw error;
  }
};


const exampleSchedule = `SEGUNDA-FEIRA
08:00 - 08:50	22000174 - T1 - ENGENHARIA DE SOFTWARE II	[ANG] 235 - Sala de Aula
08:50 - 09:40	22000174 - T1 - ENGENHARIA DE SOFTWARE II	[ANG] 235 - Sala de Aula
15:10 - 16:00	22000268 - T2 - CÁLCULO NUMÉRICO COMPUTACIONAL	[ANG] 220 - Sala de Aula
16:00 - 16:50	22000268 - T2 - CÁLCULO NUMÉRICO COMPUTACIONAL	[ANG] 220 - Sala de Aula
17:10 - 18:00	22000346 - T1 - TÓPICOS ESPECIAIS EM COMPUTAÇÃO V	[ANG] 330 - Laboratório Computação 2
18:00 - 18:50	22000346 - T1 - TÓPICOS ESPECIAIS EM COMPUTAÇÃO V	[ANG] 330 - Laboratório Computação 2
TERÇA-FEIRA
08:00 - 08:50	22000186 - T1 - COMPUTAÇÃO E SOCIEDADE	[ANG] 342 - Sala de aula
08:00 - 08:50	22000186 - T1 - COMPUTAÇÃO E SOCIEDADE	[ANG] 342 - Sala de aula
08:50 - 09:40	22000186 - T1 - COMPUTAÇÃO E SOCIEDADE	[ANG] 342 - Sala de aula
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


export const getEmbeddedCalendarID = async (email = 'kcweitgenant@inf.ufpel.edu.br', scheduleText = exampleSchedule) => {
    try {
      const response = await axios.get(`${apiUrl}/getEmbeddedCalendarID`, { params: { email,scheduleText} });
      
      return response.data.calendarID;
    } catch (error) {
      console.error('Error fetching Embedded Calendar ID:', error);
      throw error;
    }
  };
  