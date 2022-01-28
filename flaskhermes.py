from flask import Flask, render_template
import hermes
from datetime import datetime
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

@app.route("/")
def run_prog():
    # obtain seed for random func
    seed = int(datetime.now().strftime("%y%m%d%H%M"))

    # get word
    word_arr, meaning = hermes.generate_word(("processed_pres", "processed_roots", "processed_sufs"), seed)
    
    return render_template('index.html', word_arr=word_arr, meaning=meaning, time=datetime.now().strftime("%H:%M"))

if __name__ == "__main__":
    app.run(debug=True)