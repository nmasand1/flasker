

from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import os
from werkzeug.utils import secure_filename
from comparator import CSVComparator  # Importing the CSVComparator class

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['OUTPUT_FOLDER'] = 'output_files/'
app.config['ALLOWED_EXTENSIONS'] = {'csv'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    description = (
        "This tool allows you to upload two CSV files for comparison. "
        "Supported files are in .csv format, with options to specify the start row for data and columns to compare. "
        "You can also choose the comparison order to control which file is prioritized in the comparison."
    )

    if request.method == 'POST':
        # Get files and form data
        csv1_file = request.files.get('csv1_file')
        csv2_file = request.files.get('csv2_file')
        columns = request.form.get('columns')
        data_start_row_csv1 = int(request.form.get('data_start_row_csv1') or 0)
        data_start_row_csv2 = int(request.form.get('data_start_row_csv2') or 0)
        comparison_order = int(request.form.get('order') or 1)

        if not csv1_file or not csv2_file or not allowed_file(csv1_file.filename) or not allowed_file(csv2_file.filename):
            return render_template('upload.html', error_message="Please upload valid CSV files.")

        # Save CSV files
        csv1_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(csv1_file.filename))
        csv2_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(csv2_file.filename))
        csv1_file.save(csv1_path)
        csv2_file.save(csv2_path)

        # Run CSV comparison
        comparator = CSVComparator(csv1_path, csv2_path, columns, data_start_row_csv1, data_start_row_csv2, comparison_order)
        comparator.run_comparison()

        generated_files = ['matching_rows.csv', 'non_matching_rows.csv', 'comparison_stats.csv']
        return render_template('results.html', files=generated_files)

    return render_template('upload.html', description=description)

@app.route('/downloads/<path:filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
