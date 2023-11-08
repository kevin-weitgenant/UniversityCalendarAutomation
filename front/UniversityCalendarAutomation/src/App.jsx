import { useState,useEffect } from 'react'
import { getEmbeddedCalendarID, handleDownload,getCount } from './services/services'
import styles from './App.module.css';
import ufpel_logo from './assets/ufpel.png'
import github_logo from './assets/github.png'
import gifImage from './assets/tutorial_gif_novo.gif';
import validator from 'validator';
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css'; // Import the CSS
import { useNavigate } from 'react-router';

function App() {
  
  const [email, setEmail] = useState('');
  const [calendarCount, setCalendarCount] = useState(null);

  const exampleSchedule =`SEGUNDA-FEIRA
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



const [textSchedule, setTextSchedule] = useState('');
const navigate = useNavigate();
// const [isModalOpen, setIsModalOpen] = useState(false);

// const openModal = () => {
//   setIsModalOpen(true);
// };

// // Função para fechar o modal
// const closeModal = () => {
//   setIsModalOpen(false);
// };

useEffect(() => {
  const fetchCount = async () => {
    const countFromServer = await getCount();
    setCalendarCount(countFromServer);
  };

  fetchCount();
}, []);



const handleIcalDownload = () => {                                                                                                                                       
  if (textSchedule.trim() === '') {                                                                                                                                      
    toast.error('Faltou informar o texto do calendário!', {                                                                                                              
      position: 'top-right', // Position the message                                                                                                                     
      autoClose: 3000, // Close the message after 3 seconds                                                                                                              
    });                                                                                                                                                                  
  } else {                                                                                                                                                               
    handleDownload(textSchedule);                                                                                                                                                    
  }                                                                                                                                                                      
};   

const handleGenerateCalendar = async () => {
  

  if (textSchedule.trim() === '') {
    toast.error('Faltou informar o texto do calendário!', {
      position: 'top-right',
      autoClose: 3000,
    });
    return;
  }

  if (!validator.isEmail(email)) {
    toast.error('Faltou informar o e-mail!', {
      position: 'top-right',
      autoClose: 3000,
    });
    return;
  }

  try {
    toast.promise(
      getEmbeddedCalendarID(email, textSchedule),
      {
        pending: 'Gerando o seu calendário...',
        success: 'Calendário gerado com sucesso',
        error: 'Erro gerando o seu calendario.',
      },
      {
        position: 'top-right',
        autoClose: 3000,
      }
    ).then(calendarId => {
      // Use navigate to change the route and pass calendarId as state
      navigate('/calendar', { state: { calendarId } });
    });
  } catch (error) {
    console.error('Error generating embedded Google Calendar:', error);
  }
};

  return (
    <div className= { styles.outerContainer }>
      <div className = { styles.container }>
        <header className = { styles.header }>
          <img src = { ufpel_logo } alt="Logotipo UFPEL"  className = { styles.logo }/>
          <span className = { styles.headerSpan }>Calendário UFPEL</span>
          {/*<button onClick={openModal} className = { styles.howWorks }>Como funciona?</button>*/}
        </header>

        <div className = { styles.gifContainer }>
          <img src={gifImage} alt="Your GIF" />          
        </div>

        {/* <Modal
          isOpen={isModalOpen}
          onRequestClose={closeModal}
          contentLabel="Modal com GIF"
          style={{
            content: {
              width: 'fit-content',
              height: 'auto',
              margin: 'auto',
              display: 'flex',
              padding: '0',
              cursor: 'pointer',
            },
          }}
        >
          <img onClick={closeModal} src = { tutorial_gif } alt="GIF de explicação" />
        </Modal> */}
        
        <div>
          <div className = { styles.textInputsContainer }>
          <div className={styles.labelAndInput}>
            <label htmlFor="calendarInput">Texto do Calendário</label>
            <div className = { styles.outerCalendarInput }>
              <textarea
                name="calendarInput"
                placeholder= {exampleSchedule}
                value={textSchedule}
                onChange={(e) => setTextSchedule(e.target.value)}
                className={ styles.calendarInput }
              />              
            </div>

          </div>
          </div>

          <div className = { styles.buttonContainer }>
            <button className = { styles.downloadButton } onClick={handleIcalDownload}>Download .ical</button>   
            <div className = { styles.labelAndInput }>
              <label htmlFor="emailInput">Seu E-mail</label>
              <input
                name = "emailInput"
                type="text"
                placeholder="seunome@gmail.com ou seunome@inf.ufpel.edu.br"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className = { styles.emailInput }
              />
            </div>
            <button className = { styles.embeddedButton }  onClick={handleGenerateCalendar}>Enviar Google Calendar para o E-mail</button>      
          </div>
        </div>

        <p className = { styles.counting }>Contagem de Calendários Gerados: {calendarCount !== null ? calendarCount : 'Loading...'}</p>
        
        {/* <div className = { styles.calendar }>
          <EmbeddedGoogleCalendar calendarId={calendarId}/>
        </div> */}

        <footer>
          <span>Desenvolvido por Kevin Weitgenant e Gabriel Ramires</span>
          <a href="https://github.com/kevin-weitgenant/UniversityCalendarAutomation" target='__blank'>
            <img className = { styles.logoGit } src = { github_logo } alt="Logo da Github" />
          </a>
        </footer>
      </div>
    </div>
  );
}

export default App
