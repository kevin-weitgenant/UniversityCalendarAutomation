from flask import Flask,redirect,url_for,render_template,request
from create_calendar import create_calendar,criar_dicionario
from forms import Horarios
from flask import send_file
from Create_embeddedGoogleCalendar import generate_calendar,init_service
import os

app=Flask(__name__)

#app.config[ 'SECRET_KEY'] = "algumacoisa"
app.config[ 'SECRET_KEY'] = os.environ["key"]



@app.route('/',methods=['GET','POST'])
def home():
    form = Horarios()

    if request.method == 'POST':
        if request.form['submit'] == 'Calendário GoogleCalendar':
            
            dicionario = criar_dicionario(form.body.data)
            form.body.data = dicionario
            email = form.email.data
            
            if email == '':
                print("faltou o e-mail")
            
            if calendar_id is False:
                print("API chegou ao limite")  

            else:
                calendar_id = calendar_id.split('@')[0]
                return redirect(url_for('getCalendar', calendar_id = calendar_id))
        
        elif request.form['submit2'] == 'Arquivo .ical':
            dicionario = criar_dicionario(form.body.data)
            form.body.data = dicionario
            file_path = create_calendar(dicionario)           
            return send_file(file_path, as_attachment=True)

    elif request.method == 'GET':
        return render_template('home.html', form = form)

    
@app.route('/calendario',methods=['GET','POST'] )
def getCalendar():
    calendar_id = request.args['calendar_id']
    return render_template("calendario.html", calendar_id = calendar_id)    

if __name__ == '__main__':
    app.run(port=5000,debug=True)