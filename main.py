import requests
from bs4 import BeautifulSoup
import json


url = "https://github.com/trending"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
repos = soup.find_all('article', class_='Box-row')

popular_repos = []


for repo in repos[:5]:
    repo_name_tag = repo.find('h2', class_='h3 lh-condensed')
    if repo_name_tag:
        repo_name = repo_name_tag.text.strip().replace('\n', ' ').strip()
    else:
        continue

    stars_tag = None
    links = repo.find_all('a')
    for link in links:
        if link.get('href') and '/stargazers' in link.get('href'):
            stars_tag = link
            break

    stars = stars_tag.text.strip() if stars_tag else '0'
    popular_repos.append({
        'repository': repo_name,
        'stars': stars
    })


index = 1
for repo in popular_repos:
    print(f"{index}. Repository: {repo['repository']}; Stars: {repo['stars']}")
    index += 1


with open('data.json', 'w') as json_file:
    json.dump(popular_repos, json_file, indent=4)


html_cod = '''
<head>
    <title>Popular repositories GitHub</title>
    <style>
        body {
            font-family: Arial;
            background-color: #9D81BA;
        }

        h1 {
            text-align: center;
            color: #000000;
        }

        table {
            width: 100%;
            background-color: #ece6ff;
        }

        th, td {
            padding: 8px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }

        th {
            background-color: #e0d6ff;
        }

        a {
            color: #CD00CD;
            text-decoration: none;
        }

    </style>
</head>
<body>
    <h1>Popular repositories GitHub</h1>
    <table>
        <tr>
            <th>#</th>
            <th>Repository</th>
            <th>Stars</th>
        </tr>
'''

for index, repo in enumerate(popular_repos, 1):
    html_cod += f'''
    <tr>
        <td>{index}</td>
        <td>{repo["repository"]}</td>
        <td>{repo["stars"]}</td>
    </tr>
    '''

html_cod += '''
    <h5>Source of information: <a href="https://github.com/trending">GitHub Trending</a></h5>
</body>
</html>
'''


with open('index.html', 'w') as html_file:
    html_file.write(html_cod)