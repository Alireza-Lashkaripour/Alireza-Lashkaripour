import os
import json
import requests
import pandas as pd

USERNAME = 'Alireza-Lashkaripour'
TOKEN = os.getenv('GH_TOKEN')

LANGUAGE_COLORS = {
    'Python': '#3572A5',
    'JavaScript': '#F7DF1E',
    'HTML': '#E34C26',
    'CSS': '#563D7C',
    'C++': '#f34b7d',
    'Shell': '#89e051',
    'Dockerfile': '#384d54',
    'Fortran': '#4d41b1',
    'Julia': '#a270ba',
    'TeX': '#3D6117',
    'LaTeX': '#008080',
}

EXCLUDED_LANGUAGES = {
    'C', 'Assembly', 'Rust', 'TypeScript', 'Vue', 'Roff',
    'Smarty', 'Hack', 'Makefile', 'CMake', 'M4', 'Perl',
    'Pascal', 'QMake', 'Tcl', 'Vim Script'
}

def fetch_github_language_stats():
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
        lang_response = requests.get(
            lang_url, 
            headers={'Authorization': f'token {TOKEN}'}
        )
        
        if lang_response.status_code != 200:
            continue
        
        lang_data = lang_response.json()
        for lang, bytes_used in lang_data.items():
            if lang not in EXCLUDED_LANGUAGES:
                languages[lang] = languages.get(lang, 0) + bytes_used

    total_bytes = sum(languages.values())
    if total_bytes == 0:
        raise ValueError("No language data found across repositories.")

    language_data = [
        {
            "language": lang,
            "percentage": (bytes_used / total_bytes) * 100
        }
        for lang, bytes_used in languages.items()
    ]

    language_data.sort(key=lambda x: x["percentage"], reverse=True)
    return language_data[:10]

def generate_top10_line():
    try:
        language_data = fetch_github_language_stats()
        top10_line = ", ".join(
            f"{lang['language']} ({lang['percentage']:.1f}%)"
            for lang in language_data
        )
        
        print(f"Top 10 Languages: {top10_line}")
        
        with open('top10_languages.txt', 'w', encoding='utf-8') as f:
            f.write(top10_line)
        
        print("✅ Top 10 languages saved to 'top10_languages.txt'")
        
    except Exception as e:
        print(f"❌ Error generating top 10 languages: {str(e)}")
        raise

if __name__ == "__main__":
    generate_top10_line()
