from flask import Flask, render_template, request, redirect, url_for
import os
from collections import Counter
import re

# creates app instance
app = Flask(__name__, template_folder='templates', static_folder='static')

# to stop caching static file
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# function to analyze text and return statistics 
def analyze_text(text):
    # words count - split by whitespace and remove empty string
    words = [word for word in text.split() if word]
    word_count = len(words)

    # character count
    char_count = len(text)
    char_count_no_space = len(text.replace(" ", ""))

    # most frequent words
    word_freq = Counter(words)
    most_common_words = word_freq.most_common(10)

    # sentences count 
    sentences = [s for s in re.split(r'[.!?]+', text) if s.strip()]
    sentence_count = len(sentences)

    return {
        'word_count': word_count,
        'char_count': char_count,
        'char_count_no_space': char_count_no_space,
        'most_common_words': most_common_words,
        'sentence_count': sentence_count,
        'original_text': text
        }

# this decorator creates the home route
# @app.route() - defines URL endpoints
@app.route('/')
def home():
    # injecting data to the html files using jinja2 template engine
    techs = ['HTML', 'CSS', 'Python', 'Flask']
    name = 'Text Analyzer'
    return render_template('home.html', techs = techs, name = name, title = 'Home')

@app.route('/about')
def about():
    name = 'Text Analyzer'
    return render_template('about.html', name = name, title = 'About us')

@app.route('/result')
def result():
    return render_template('result.html')

@app.route('/post', methods =['GET', 'POST'])
def post():
    name = 'Text Analyzer'
    if request.method == 'GET':
        return render_template('post.html', name = name, title = 'Post')

    if request.method == 'POST':
        # this retrieves the value of the form input field named 'content'
        content = request.form['content']
        
        # checks if the submitted content is empty or just whitespace
        # strip() removes leading/trailing whitespace - So this line avoids analyzing blank input
        if not content.strip():
            # if the input is blank, it redirects the user back to the 'post' route (likely the form page).
            return redirect(url_for('post'))
        
        # analyze the text
        analysis = analyze_text(content)
        return render_template('result.html', analysis = analysis, title = 'results')       

if __name__ == '__main__':
    # for deployment we use the environ
    # to make it work for both production and development
    # os.environ.get() - configures deployment port
    port = int(os.environ.get("PORT", 5000))
    # debug=True - auto-reload + error pages
    # host='0.0.0.0' - allows network access
    app.run(debug=True, host='0.0.0.0', port = port)


