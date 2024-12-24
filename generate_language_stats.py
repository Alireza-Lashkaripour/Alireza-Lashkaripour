import requests
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd

USERNAME = 'Alireza-Lashkaripour'
TOKEN = 'YOUR_GITHUB_PERSONAL_ACCESS_TOKEN'

response = requests.get(
    f'https://api.github.com/users/{USERNAME}/repos?per_page=100',
    headers={'Authorization': f'token {TOKEN}'}
)

repos = response.json()
languages = {}

for repo in repos:
    lang_url = repo['languages_url']
    lang_data = requests.get(lang_url, headers={'Authorization': f'token {TOKEN}'}).json()
    for lang, bytes_used in lang_data.items():
        if lang in languages:
            languages[lang] += bytes_used
        else:
            languages[lang] = bytes_used

total_bytes = sum(languages.values())
language_stats = {lang: (bytes_used / total_bytes) * 100 for lang, bytes_used in languages.items()}

df = pd.DataFrame(list(language_stats.items()), columns=['Language', 'Percentage'])
df = df.sort_values(by='Percentage', ascending=False)

fig, ax = plt.subplots()
bars = plt.bar(df['Language'], [0] * len(df['Language']))

def update(frame):
    for bar, height in zip(bars, df['Percentage']):
        bar.set_height(height * (frame + 1) / 10)
    return bars

ani = FuncAnimation(fig, update, frames=10, repeat=False)
ani.save('language_stats.gif', writer='pillow')
