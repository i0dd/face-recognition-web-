from flask import Flask, render_template, request, send_from_directory, render_template_string
import os
import cv2
import face_recognition

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Load known image and encode it
known_image = face_recognition.load_image_file("R (1).jpg")
known_encoding = face_recognition.face_encodings(known_image)[0]

@app.route('/')
def index():
    return render_template_string('''
    <!doctype html>
    <title>File Upload</title>
    <h1>Upload a file</h1>
    <form method="post" action="/upload" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" value="Upload">
    </form>
    <div id="result"></div>
    <script>
        document.querySelector('form').addEventListener('submit', async (event) => {
            event.preventDefault();
            const formData = new FormData(event.target);
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });
            const result = await response.text();
            document.getElementById('result').innerHTML = result;
        });
    </script>
    ''')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        print(file.filename)
        
        
        folderpath = "C:/Users/trpsk/Desktop/erm/uploads"
    
        unkown1image = os.path.join(folderpath, file.filename)
        unknown_image = face_recognition.load_image_file(unkown1image)
        unknown_encodings = face_recognition.face_encodings(unknown_image)

        if not unknown_encodings:
            return 'No faces found in the uploaded image.'

        unknown_encoding = unknown_encodings[0]
        results = face_recognition.compare_faces([known_encoding], unknown_encoding)
        if results[0]:
            return render_template('acessaproved.html')
        else:
            return render_template('accesdenied.html')

if __name__ == '__main__':
    app.run(debug=True)
