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
    'PHP': '#4F5D95',
    'SCSS': '#CC6699',
    'Ruby': '#701516',
    'Java': '#b07219',
    'C++': '#f34b7d',
    'C#': '#178600',
    'Go': '#00ADD8',
    'Swift': '#ffac45',
    'Kotlin': '#F18E33',
    'Rust': '#dea584',
    'Shell': '#89e051',
    'Dockerfile': '#384d54',
    'Fortran': '#4d41b1',
    'Julia': '#a270ba',
    'TeX': '#3D6117',
    'Jupyter Notebook': '#DA5B0B',
    'R': '#198CE7',
    'MATLAB': '#e16737',
    'Assembly': '#6E4C13',
    'LaTeX': '#008080',
    'Markdown': '#083FA1'
}

EXCLUDED_LANGUAGES = {
    'C',
    'Assembly',
    'Rust',
    'TypeScript',
    'Vue',
    'Roff',
    'Smarty',
    'Hack',
    'Makefile',
    'CMake',
    'M4',
    'Perl',
    'Pascal',
    'QMake',
    'Tcl',
    'Vim Script'
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
            if lang not in EXCLUDED_LANGUAGES:  # Only count non-excluded languages
                languages[lang] = languages.get(lang, 0) + bytes_used

    # Calculate percentages
    total_bytes = sum(languages.values())
    if total_bytes == 0:
        raise ValueError("No language data found across repositories.")

    language_data = [
        {
            "language": lang,
            "percentage": (bytes_used / total_bytes) * 100,
            "color": LANGUAGE_COLORS.get(lang, "#666666")
        }
        for lang, bytes_used in languages.items()
        if (bytes_used / total_bytes) * 100 > 0.1  
    ]

    language_data.sort(key=lambda x: x["percentage"], reverse=True)

    return language_data

def generate_stats_file():
    try:
        language_data = fetch_github_language_stats()
        
        output_data = {
            "timestamp": pd.Timestamp.now().isoformat(),
            "username": USERNAME,
            "stats": language_data
        }

        with open('language_stats.json', 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2)
        
        print("✅ Language statistics JSON generated successfully!")
        print(f"📊 Found {len(language_data)} languages with usage > 0.1%")
        print("\nTop 5 languages:")
        for lang in language_data[:5]:
            print(f"  • {lang['language']}: {lang['percentage']:.1f}%")

    except Exception as e:
        print(f"❌ Error generating statistics: {str(e)}")
        raise

if __name__ == "__main__":
    generate_stats_file()
