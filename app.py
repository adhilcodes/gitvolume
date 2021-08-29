from flask import Flask, render_template, request
import requests
app = Flask(__name__, template_folder='templates')


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/result', methods=['POST'])
def gitrepo_volume():

    if request.method == 'POST':

        url = request.form['repo_url']
        base_api_url = 'https://api.github.com/repos'
        git_repo_url = str(url) + ".git"

        github_username, repository_name = git_repo_url[:-4].split('/')[-2:]
        result = requests.get(f'{base_api_url}/{github_username}/{repository_name}')

        repo_size_kb = result.json().get('size')
        repo_size_mb = repo_size_kb * 0.001
        repo_size_gb = repo_size_mb * 0.001

        size_in_kb = (str(repo_size_kb)+"KB")
        size_in_mb = (str(repo_size_mb)+"MB")
        size_in_gb = (str(repo_size_gb)+"GB")

        size = str(size_in_kb) + " | " + str(size_in_mb) + " | " + str(size_in_gb)

        return render_template('index.html', size=size)    


if __name__ == '__main__':
    app.run(debug=True)
