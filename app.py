from flask import Flask,redirect,url_for,render_template,request, flash
from create_calendar import create_calendar,criar_dicionario
from forms import Horarios
from flask import send_file
from Create_embeddedGoogleCalendar import generate_calendar
import os

app=Flask(__name__)

#app.config[ 'SECRET_KEY'] = "algumacoisa"
app.config[ 'SECRET_KEY'] = os.environ["key"]

@app.route('/',methods=['GET','POST'])
def home():
    form = Horarios()

    if request.method == 'POST':
        if request.form['submit'] == 'Calendário GoogleCalendar':
            
            if form.body.data != '':
                dicionario = criar_dicionario(form.body.data)
                email = form.email.data
                
                if email == '':
                    flash("Caso contrário, não é possível para que os eventos sejam atribuídos a sua conta.", 'alert')
                    return render_template('home.html', form = form)
                
                calendar_id = generate_calendar(dicionario,email)

                if calendar_id is False:
                    flash("Provavelmente limite da API, a Google limita o número de calendários criados por dia, tente mais tarde ou use a opção de baixar o arquivo .ical", 'error')
                    return render_template('home.html', form = form) 

                else:
                    calendar_id = calendar_id.split('@')[0]
                    return redirect(url_for('getCalendar', calendar_id = calendar_id))

            else:
                flash("Copie no cobalto em ALUNO/CONSULTA/HORÁRIOS", 'missing')
                return render_template('home.html', form = form) 
        
        elif request.form['submit'] == 'Arquivo .ical':
            

            if form.body.data != '':
                dicionario = criar_dicionario(form.body.data)
                file_path = create_calendar(dicionario)           
                return send_file(file_path, as_attachment=True)
            
            else:
                flash("Copie no cobalto em ALUNO/CONSULTA/HORÁRIOS", 'missing')
                return render_template('home.html', form = form)    

    elif request.method == 'GET':
        return render_template('home.html', form = form)

    
@app.route('/calendario',methods=['GET','POST'] )
def getCalendar():
    calendar_id = request.args['calendar_id']
    return render_template("calendario.html", calendar_id = calendar_id)    

if __name__ == '__main__':
    app.run(port=5000,debug=True)