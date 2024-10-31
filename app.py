# from flask import Flask, request, render_template, redirect, url_for
# import os
# from werkzeug.utils import secure_filename
# import yaml
# from comparator import CSVComparator  # Importing the CSVComparator class

# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = 'uploads/'
# app.config['ALLOWED_EXTENSIONS'] = {'csv', 'yml'}

# # Ensure the upload folder exists
# os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# @app.route('/', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         # Check if the post request has the files part
#         if 'yml_file' not in request.files or 'csv_files' not in request.files:
#             return 'No file part'
        
#         yml_file = request.files['yml_file']
#         csv_files = request.files.getlist('csv_files')

#         # Validate the YAML configuration file
#         if yml_file and allowed_file(yml_file.filename):
#             yml_filename = secure_filename(yml_file.filename)
#             yml_file_path = os.path.join(app.config['UPLOAD_FOLDER'], yml_filename)
#             yml_file.save(yml_file_path)

#             # Update the YAML configuration with the uploaded CSV file paths
#             with open(yml_file_path, 'r') as file:
#                 config = yaml.safe_load(file)

#             # Dynamically save paths of uploaded CSV files
#             config['files'] = []  # Clear previous file paths
#             for csv_file in csv_files:
#                 if csv_file and allowed_file(csv_file.filename):
#                     csv_filename = secure_filename(csv_file.filename)
#                     csv_file_path = os.path.join(app.config['UPLOAD_FOLDER'], csv_filename)
#                     csv_file.save(csv_file_path)
#                     # Add the uploaded file path to the configuration
#                     config['files'].append({csv_filename: csv_file_path})

#             # Save the updated YAML configuration
#             with open(yml_file_path, 'w') as file:
#                 yaml.dump(config, file)

#             # Now run the comparison
#             comparator = CSVComparator(yml_file_path)
#             comparator.run_comparison()

#             return redirect(url_for('upload_file'))

#     return render_template('upload.html')

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import os
from werkzeug.utils import secure_filename
import yaml
from comparator import CSVComparator  # Importing the CSVComparator class

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['OUTPUT_FOLDER'] = 'output_files/'  # Define the output folder for results
app.config['ALLOWED_EXTENSIONS'] = {'csv', 'yml'}

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)  # Ensure output folder exists

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the files part
        if 'yml_file' not in request.files or 'csv_files' not in request.files:
            return 'No file part'
        
        yml_file = request.files['yml_file']
        csv_files = request.files.getlist('csv_files')

        # Validate the YAML configuration file
        if yml_file and allowed_file(yml_file.filename):
            yml_filename = secure_filename(yml_file.filename)
            yml_file_path = os.path.join(app.config['UPLOAD_FOLDER'], yml_filename)
            yml_file.save(yml_file_path)

            # Update the YAML configuration with the uploaded CSV file paths
            with open(yml_file_path, 'r') as file:
                config = yaml.safe_load(file)

            # Dynamically save paths of uploaded CSV files
            config['files'] = []  # Clear previous file paths
            for csv_file in csv_files:
                if csv_file and allowed_file(csv_file.filename):
                    csv_filename = secure_filename(csv_file.filename)
                    csv_file_path = os.path.join(app.config['UPLOAD_FOLDER'], csv_filename)
                    csv_file.save(csv_file_path)
                    # Add the uploaded file path to the configuration
                    config['files'].append({csv_filename: csv_file_path})

            # Save the updated YAML configuration
            with open(yml_file_path, 'w') as file:
                yaml.dump(config, file)

            # Now run the comparison
            comparator = CSVComparator(yml_file_path)
            comparator.run_comparison()

            # Get generated files for the results page
            generated_files = ['matching_rows.csv', 'non_matching_rows.csv', 'comparison_stats.csv']
            return render_template('results.html', files=generated_files)

    return render_template('upload.html')

@app.route('/downloads/<path:filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
