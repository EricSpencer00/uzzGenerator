from flask import Flask, request, render_template, send_file
import os
from werkzeug.utils import secure_filename
from uzz import process_text, save_custom_dictionary, load_custom_dictionary

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
CUSTOM_DICT_PATH = 'uzzGenerator/word_replacements.txt'
NOUN_LIST_PATH = 'uzzGenerator/nouns.txt'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    filename = secure_filename(file.filename)
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], f"processed_{filename}")

    file.save(input_path)

    process_text(input_path, output_path, custom_dict_path=CUSTOM_DICT_PATH, noun_list_path=NOUN_LIST_PATH)

    return send_file(output_path, as_attachment=True)

@app.route('/manage_dictionary', methods=['GET', 'POST'])
def manage_dictionary():
    custom_dict = load_custom_dictionary(CUSTOM_DICT_PATH)

    if request.method == 'POST':
        word = request.form.get('word')
        replacement = request.form.get('replacement')

        if word and replacement:
            custom_dict[word.lower()] = replacement
            save_custom_dictionary(custom_dict, CUSTOM_DICT_PATH)

    return render_template('manage_dictionary.html', dictionary=custom_dict)

@app.route('/manage_nouns', methods=['GET', 'POST'])
def manage_nouns():
    nouns = []
    if os.path.exists(NOUN_LIST_PATH):
        with open(NOUN_LIST_PATH, 'r') as file:
            nouns = [line.strip() for line in file]

    if request.method == 'POST':
        new_noun = request.form.get('noun')
        if new_noun:
            nouns.append(new_noun.strip())
            with open(NOUN_LIST_PATH, 'w') as file:
                file.write('\n'.join(nouns))

    return render_template('manage_nouns.html', nouns=nouns)

if __name__ == '__main__':
    app.run(debug=True)
