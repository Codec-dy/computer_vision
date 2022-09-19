from flask import Flask, redirect, url_for, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'supersecretkey'

IMG_FOLDER = os.path.join('static', 'Laptop')
app.config['UPLOAD_FOLDER'] = IMG_FOLDER

class  Upload(FlaskForm):
    file = FileField("File")
    submit = SubmitField("Upload File")


@app.route('/', methods=['GET','POST'])
def home():
    form = Upload()
    print('here1')
    IMG_LIST=[]
    info=''
    if form.validate_on_submit():
        app.config['UPLOAD_FOLDER'] = 'statics'
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
        print('statics/'+file.filename)
        import testModel2 as testModel
        model = testModel.figureOut('statics/'+file.filename)
        print(model)
        if len(model) != 0: 
            IMG_LIST = []

            for img in model[1]:
                IMG_LIST.append('TrainingImages/'+img[2]+'/'+img[1])
            print(IMG_LIST)
            info=model[0]
    return render_template("index.html", form=form, imagelist=IMG_LIST, info=info)

if __name__ == '__main__':
    app.run()