from flask import Flask, request, render_template

app = Flask(__name__)

# Preloaded custom dictionary for the session
custom_dictionary = {
    "bros": "bruzz",
    "girls": "huzz",
    "unemployed": "unempluzz",
    "son": "suzz",
    "fine shyts": "huzz",
    "fine shyt": "huzz",
    "mom": "muzz",
    "dad": "duzz",
    "teacher": "tuzz",
    "fruit snacks": "fruizz",
    "chopped huzz": "chuzz",
    "daughter": "daughtuzz",
    "freshmen": "fuzz",
    "jug": "juzz",
    "crashout": "cruzz",
    "friend": "fruzz",
    "family": "famuzz",
    "squad": "squzz",
    "party": "paruzz",
    "sibling": "sibuzz",
    "team": "teuzz",
    "love": "luzz",
    "hustle": "hustluzz",
    "grinded": "gruzzed",
    "leader": "leuzz",
    "legend": "leguzz",
    "champion": "chuzz",
    "winner": "winnuzz",
    "player": "playuzz",
    "fighter": "fighuzz",
    "dreamer": "dreuzz",
}

# Function to transform text
def transform_text(input_text, dictionary):
    words = input_text.split()
    transformed_words = [
        dictionary.get(word.lower(), word) for word in words
    ]
    return " ".join(transformed_words)

@app.route("/", methods=["GET", "POST"])
def index():
    transformed_text = ""
    if request.method == "POST":
        input_text = request.form.get("input_text", "")
        transformed_text = transform_text(input_text, custom_dictionary)
    return render_template("index.html", transformed_text=transformed_text, dictionary=custom_dictionary)

@app.route("/update_dictionary", methods=["POST"])
def update_dictionary():
    word = request.form.get("word", "").strip().lower()
    replacement = request.form.get("replacement", "").strip()
    if word and replacement:
        custom_dictionary[word] = replacement
    return render_template("index.html", dictionary=custom_dictionary)

if __name__ == "__main__":
    app.run(debug=True)
