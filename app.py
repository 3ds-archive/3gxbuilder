import os
from flask import Flask, url_for, render_template, request
from github import Github

app = Flask(__name__)

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/build', methods=['POST'])
def result():
    
    g = Github(os.environ['GITHUB_API'])
    repo = g.get_repo('3ds-archive/3gxbuilder')
    link = request.form['link']
    repo.create_repository_dispatch(link)
    
    return render_template('https://github.com/3ds-archive/3gxbuilder/actions')

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)