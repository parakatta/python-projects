from flask import Flask,render_template,request, redirect,send_file,flash,url_for,get_flashed_messages,session
import json,PyPDF2,os
from werkzeug.utils import secure_filename

app=Flask(__name__)
app.secret_key="super secret key"

app.config['FILE_UPLOADS']=r"E:\web\PROJECTS\8 js py php\flask pro\converts"
app.config['ALLOWED_FILE_TYPES']=['TXT']

def allowed_file(filename):
    if not '.' in filename:
        flash('Invalid file type',category='error')
    ext=filename.rsplit('.',1)[1]
    if ext.upper() in app.config['ALLOWED_FILE_TYPES']:
        return True
    else:
        return False

@app.route('/')
def index():
    return render_template('index.html');


   
@app.route("/json", methods=['GET','POST'])
def json1():
    txt={}
    text=request.form.get('text')
    items=text.split()
    txt={items[i]:items[i+1] for i in range(0,len(items),2)}
    data=json.dumps(txt)
    return render_template('index.html',data=data);

@app.route("/pdf", methods=['GET','POST'])
def pdf():
    if request.method=="POST":
        if request.files:
            file1=request.files["file"]
        
            filename = secure_filename(file1.filename)
            file1.save(os.path.join(app.config['FILE_UPLOADS'],secure_filename(file1.filename)))
                
            file1.save(secure_filename(file1.filename))
            flash('saved',category='success')

            if not allowed_file(file1.filename):
                flash('Invalid file type',category='error')

    return redirect('/downloadfile/'+ filename)
    return render_template('index.html')

@app.route("/downloadfile/<filename>", methods = ['GET'])
def download_file(filename):
    text=request.form.get('text')
    file=open('text.pdf','w')
    pdfreader=PyPDF2.PdfFileReader(text)
    page=pdfreader.getPage(0)
    pdfwriter=PyPDF2.PdfFileWriter();
    pdfwriter.addPage(page)
    file.close();
    return render_template('json.html',value=filename)

@app.route('/return-files/<filename>')
def return_files_tut(filename):
    file_path = app.config['FILE_UPLOADS'] + filename
    return send_file(file_path, as_attachment=True, attachment_filename='')


'''@app.route("/json", methods=['GET','POST'])
def json():
    return jsonify({'Courses':courses})

@app.route("/courses/<int :course_id>",methods=['GET'])
def get_course(course_id):
    return jsonify({'course':courses[course_id]})


@app.route("/course",methods=['POST'])
def create():
    course=;
    courses.append(course)
    return jsonify({'Created':course})'''

if __name__=="__main__":
    app.run(debug=True)