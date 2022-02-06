from flask import Flask,redirect,url_for,render_template,request
from create_calendar import create_calendar,criar_dicionario
from forms import Horarios
from flask import send_file

app=Flask(__name__)
app.config[ 'SECRET_KEY'] = 'key'

@app.route('/',methods=['GET','POST'])
def home():
    form = Horarios()

    if form.validate_on_submit():
        
        #form.body.data = criar_dicionario(form.body.data)
        dicionario = criar_dicionario(form.body.data)
        print(dicionario)
        form.body.data = dicionario
        file_path = create_calendar(dicionario)
        
        return send_file(file_path, as_attachment=True)
    
    return render_template('home.html', form = form)



if __name__ == '__main__':
    app.run(port=5000,debug=False)