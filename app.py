# creating routes
# the home route
from flask import Flask, render_template, request, redirect, url_for
import os

# creates app instance
app = Flask(__name__)

# to stop caching static file
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
# this decorator creates the home route
# @app.route() - defines URL endpoints
@app.route('/')
def home():
    # injecting data to the html files using jinja2 template engine
    techs = ['HTML', 'CSS', 'Python', 'Flask']
    name = '30 days of python programming'
    return render_template('home.html', techs = techs, name = name, title = 'Home')

@app.route('/about')
def about():
    name = '30 days of python programming'
    return render_template('about.html', name = name, title = 'About us')

@app.route('/result')
def result():
    return render_template('result.html')

@app.route('/post', methods =['GET', 'POST'])
def post():
    name = 'Text Analyzer'
    if request.method == 'GET':
        return render_template('post.html', name = name, title = 'post')
    if request.method == 'POST':
        content = request.form['content']
        print(content)
        return redirect(url_for('result'))

if __name__ == '__main__':
    # for deployment we use the environ
    # to make it work for both production and development
    # os.environ.get() - configures deployment port
    port = int(os.environ.get("PORT", 5000))
    # debug=True - auto-reload + error pages
    # host='0.0.0.0' - allows network access
    app.run(debug=True, host='0.0.0.0', port = port)

