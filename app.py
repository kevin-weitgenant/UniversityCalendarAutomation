from flask import Flask,redirect,url_for,render_template,request
from create_calendar import create_calendar,criar_dicionario
from forms import Horarios, Calendario
from flask import send_file
from Create_embeddedGoogleCalendar import generate_calendar,init_service
import os

app=Flask(__name__)

#app.config[ 'SECRET_KEY'] = "algumacoisa"
app.config[ 'SECRET_KEY'] = os.environ["key"]



@app.route('/',methods=['GET','POST'])
def home():
    form = Horarios()

    if form.validate_on_submit():
        
        dicionario = criar_dicionario(form.body.data)
        form.body.data = dicionario
        file_path = create_calendar(dicionario)
        email = form.email.data
        
        if email == '':
            return send_file(file_path, as_attachment=True)     
        calendar_id = generate_calendar(dicionario,email)
        
        if calendar_id is False:
            print("API chegou ao limite")
            return send_file(file_path, as_attachment=True)    

        else:
            calendar_id = calendar_id.split('@')[0]
            return redirect(url_for('getCalendar', calendar_id = calendar_id, file_path = file_path))
    return render_template('home.html', form = form)

    
@app.route('/calendario',methods=['GET','POST'] )
def getCalendar():
    calendar_id = request.args['calendar_id']
    file_path = request.args['file_path']
    form = Calendario()

    if form.validate_on_submit():
        return send_file(file_path, as_attachment=True)
    return render_template("calendario.html", calendar_id = calendar_id, file_path = file_path, form = form )    


if __name__ == '__main__':
    app.run(port=5000,debug=True)