from flask import Flask, render_template, request, send_file
import PyPDF2
import os
from werkzeug.utils import secure_filename
import tempfile

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/merge', methods=['POST'])
def merge():
    pdf_files = request.files.getlist('pdfs')
    
    merger = PyPDF2.PdfMerger()
    temp_dir = tempfile.mkdtemp()

    for file in pdf_files:
        filename = secure_filename(file.filename)
        filepath = os.path.join(temp_dir, filename)
        file.save(filepath)
        merger.append(filepath)

    output_path = os.path.join(temp_dir, "merged_output.pdf")
    merger.write(output_path)
    merger.close()

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
