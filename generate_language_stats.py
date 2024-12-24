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

total_bytes = sum(languages.values())
if total_bytes == 0:
    raise ValueError("No language data found across repositories.")

language_stats = {lang: (bytes_used / total_bytes) * 100 for lang, bytes_used in languages.items()}
df = pd.DataFrame(list(language_stats.items()), columns=['Language', 'Percentage'])
df = df.sort_values(by='Percentage', ascending=False)

fig, ax = plt.subplots(figsize=(10, 10))
colors = plt.cm.tab20.colors[:len(df['Language'])]

wedges, texts, autotexts = ax.pie(
    df['Percentage'], 
Run python generate_language_stats.py
Traceback (most recent call last):
  File "/home/runner/work/Alireza-Lashkaripour/Alireza-Lashkaripour/generate_language_stats.py", line 70, in <module>
    plt.savefig('language_stats.gif', format='gif')
  File "/opt/hostedtoolcache/Python/3.12.8/x64/lib/python3.12/site-packages/matplotlib/pyplot.py", line 1243, in savefig
    res = fig.savefig(*args, **kwargs)  # type: ignore[func-returns-value]
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.12.8/x64/lib/python3.12/site-packages/matplotlib/figure.py", line 3490, in savefig
    self.canvas.print_figure(fname, **kwargs)
  File "/opt/hostedtoolcache/Python/3.12.8/x64/lib/python3.12/site-packages/matplotlib/backend_bases.py", line 2125, in print_figure
    self._switch_canvas_and_return_print_method(format, backend)
  File "/opt/hostedtoolcache/Python/3.12.8/x64/lib/python3.12/contextlib.py", line 137, in __enter__
    return next(self.gen)
           ^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.12.8/x64/lib/python3.12/site-packages/matplotlib/backend_bases.py", line 2026, in _switch_canvas_and_return_print_method
    raise ValueError(
ValueError: Format 'gif' is not supported (supported formats: eps, jpeg, jpg, pdf, pgf, png, ps, raw, rgba, svg, svgz, tif, tiff, webp)
Error: Process completed with exit code 1.
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
plt.title('GitHub Language Usage Across All Repositories', fontsize=16, weight='bold')
plt.tight_layout()
plt.savefig('language_stats.png', format='png')
plt.close(fig)

img = Image.open('language_stats.png')
img.save('language_stats.gif', format='GIF')

print("Language usage GIF generated: 'language_stats.gif'")
