from flask import Flask, render_template, request,flash
import requests

app = Flask(__name__, template_folder='templates')
app.secret_key="A233h#sdp@p"


@app.route('/')
def main():
    return render_template('index.html')



@app.route('/result', methods=['GET','POST'])
def gitrepo_volume():
    if request.method == 'POST':
        url = request.form['repo_url']
        base_api_url = 'https://api.github.com/repos'
        git_repo_url = str(url) + ".git"
        try:
            github_username, repository_name = git_repo_url[:-4].split('/')[-2:]
        except ValueError:
            flash("Invalid Input!")
            return render_template('index.html',size=None)
        
        result = requests.get(f'{base_api_url}/{github_username}/{repository_name}')

        if result.status_code==404:
            flash("Oh Sorry, that wasn't a valid Github Repository!")
            return render_template('index.html',size=None)


        repo_size_kb = result.json().get('size')
        repo_size_mb = repo_size_kb * 0.001
        repo_size_gb = repo_size_mb * 0.001
        repo_size_gb = f"{repo_size_gb:8f}"


        size_in_kb = (str(repo_size_kb)+"KB")
        size_in_mb = (str(repo_size_mb)+"MB")
        size_in_gb = (repo_size_gb+"GB")

        size = str(size_in_kb) + " | " + str(size_in_mb) + " | " + str(size_in_gb)

        return render_template('index.html', size=size)  
    

    else:
        return render_template('index.html')
        



if __name__ == '__main__':
    app.run(debug=True)
