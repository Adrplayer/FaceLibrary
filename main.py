# main.py# import the necessary packages
from flask import Flask, render_template, Response, redirect, request
from flask.helpers import url_for
from camera import VideoCamera
import data
import numpy as np
app = Flask(__name__)
lib = data.datab()

ALOWED_EXTENSIONS={'png','jpg','jpeg','gif'}
def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.',1)[1].lower() in ALOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/camera')
def cam():
    return render_template('camera.html')

@app.route('/library')
def library():
    i,n,l,a = lib.getlist()
    return render_template('library.html',_id=i,names = n, lasts = l, access=a,leng=len(n))

@app.route('/delete/<string:_id>',methods=['POST','GET'])
def delete_user(_id):
    lib.delete(_id)
    return(redirect(url_for('library')))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register',methods=['GET','POST'])
def register():
    newid = lib.getnewid()
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        name =request.form['name']
        last =request.form['last']
        access = int(request.form['access'])
        _id = int(request.form['id'])
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            lib.register(file,_id,name,last,access)
            return render_template('register.html',_id=newid + 1)
    return render_template('register.html',_id=newid)
           


def gen(camera):
    while True:
        #get camera frame
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    Lnames,encodings=lib.getencodings()
    return Response(gen(VideoCamera(Lnames,encodings)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    # defining server ip address and port
    app.run(host='0.0.0.0',port='5000', debug=True)
