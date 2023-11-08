import styles from './App.module.css';
import styles2 from './CalendarRoute.module.css'
import ufpel_logo from './assets/ufpel.png'
import github_logo from './assets/github.png'
import EmbeddedGoogleCalendar from './EmbeddedGoogleCalendar';
import { useLocation } from 'react-router-dom';

const CalendarRoute = () => {
    const location = useLocation();
    const calendarId = location.state?.calendarId;
    
    return (
        <div className= { styles.outerContainer }>
          <div className = { styles.container }>
            <header className = { styles.header }>
              <img src = { ufpel_logo } alt="Logotipo UFPEL"  className = { styles.logo }/>
              <span className = { styles.headerSpan }>Calendário UFPEL</span>
            </header>
    
            <div className = { styles2.calendarContainer }>
              <EmbeddedGoogleCalendar className = { styles2.calendar } calendarId={calendarId}/>
            </div>

            <div className = { styles2.imgContainer }>
                <img src={"/email.png" } alt="Imagem Demonstração" />   
            </div>
    
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
    
  
  
  
  export default CalendarRoute;
  