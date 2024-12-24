import os
import requests
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image

USERNAME = 'Alireza-Lashkaripour'
TOKEN = os.getenv('GH_TOKEN')

if not TOKEN:
    raise ValueError("GitHub token is missing. Please set 'GH_TOKEN' as an environment variable.")

repos = []
page = 1

while True:
    response = requests.get(
        f'https://api.github.com/users/{USERNAME}/repos?per_page=100&page={page}',
        headers={'Authorization': f'token {TOKEN}'}
    )
    if response.status_code != 200:
        raise ValueError(f"Failed to fetch repositories: {response.status_code}")
    
    data = response.json()
    if not data:
        break
    
    repos.extend(data)
    page += 1

languages = {}

for repo in repos:
    lang_url = repo['languages_url']
    lang_response = requests.get(lang_url, headers={'Authorization': f'token {TOKEN}'})
    
    if lang_response.status_code != 200:
        continue
    
    lang_data = lang_response.json()
    for lang, bytes_used in lang_data.items():
        languages[lang] = languages.get(lang, 0) + bytes_used

excluded_languages = {'C', 'Assembly', 'Java'}
languages = {lang: bytes_used for lang, bytes_used in languages.items() if lang not in excluded_languages}

total_bytes = sum(languages.values())
if total_bytes == 0:
    raise ValueError("No language data found across repositories after filtering.")

language_stats = {lang: (bytes_used / total_bytes) * 100 for lang, bytes_used in languages.items()}
df = pd.DataFrame(list(language_stats.items()), columns=['Language', 'Percentage'])
df = df.sort_values(by='Percentage', ascending=False)

fig, ax = plt.subplots(figsize=(10, 10))
colors = plt.cm.tab20.colors[:len(df['Language'])]

wedges, texts, autotexts = ax.pie(
    df['Percentage'], 
    labels=df['Language'], 
    autopct=lambda p: f'{p:.1f}%' if p > 0 else '',
    startangle=140,
    textprops={'fontsize': 12},
    colors=colors
)

for text, autotext in zip(texts, autotexts):
    text.set(size=12)
    autotext.set(size=10, weight="bold")

ax.axis('equal')
plt.title('GitHub Language Usage Across All Repositories (Filtered)', fontsize=16, weight='bold')
plt.tight_layout()
plt.savefig('language_stats.png', format='png')
plt.close(fig)

img = Image.open('language_stats.png')
img.save('language_stats.gif', format='GIF')

print("Language usage GIF generated: 'language_stats.gif'")
