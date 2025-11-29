#!/usr/bin/env python3
"""
GitHub Profile README Updater
Fetches dynamic GitHub data and updates the README.md file between markers.
Uses GitHub REST API with GITHUB_TOKEN for authentication.
Enhanced with retry logic, caching, and improved SVG generation.
"""

import os
import sys
import json
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from datetime import datetime, timedelta
from collections import defaultdict
from functools import lru_cache
import re

# Configuration
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '')
REPO_OWNER = 'DenxVil'
REPO_NAME = 'DenxVil'
README_PATH = 'README.md'
ASSETS_DIR = 'assets'

# Theme configuration
THEME = {
    'primary': '#00d9ff',
    'secondary': '#5b86e5',
    'accent': '#ff6b6b',
    'success': '#4ecdc4',
    'bg_dark': '#0d1117',
    'bg_light': '#161b22',
    'bg_lighter': '#21262d',
    'text': '#c9d1d9',
    'text_muted': '#8b949e'
}

# Language colors - extended list
LANGUAGE_COLORS = {
    'Python': '#3776AB',
    'JavaScript': '#F7DF1E',
    'TypeScript': '#007ACC',
    'HTML': '#E34F26',
    'CSS': '#1572B6',
    'Java': '#007396',
    'C++': '#00599C',
    'C': '#A8B9CC',
    'Go': '#00ADD8',
    'Rust': '#DEA584',
    'Ruby': '#CC342D',
    'PHP': '#777BB4',
    'Swift': '#FA7343',
    'Kotlin': '#A97BFF',
    'Dart': '#0175C2',
    'Shell': '#89e051',
    'Dockerfile': '#384d54',
    'Vue': '#4FC08D',
    'SCSS': '#c6538c',
    'Jupyter Notebook': '#DA5B0B'
}

# API endpoints
GITHUB_API_BASE = 'https://api.github.com'
HEADERS = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}


def create_session_with_retry():
    """Create a requests session with retry logic."""
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


# Create session with retry logic
session = create_session_with_retry()


@lru_cache(maxsize=1)
def fetch_user_info():
    """Fetch basic user profile information with caching."""
    url = f'{GITHUB_API_BASE}/users/{REPO_OWNER}'
    # Use headers only if token is available
    headers = HEADERS if GITHUB_TOKEN else {'Accept': 'application/vnd.github.v3+json'}
    response = session.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()


def fetch_user_repos():
    """Fetch all user repositories with retry logic."""
    repos = []
    page = 1
    per_page = 100
    # Use headers only if token is available
    headers = HEADERS if GITHUB_TOKEN else {'Accept': 'application/vnd.github.v3+json'}
    
    while True:
        url = f'{GITHUB_API_BASE}/users/{REPO_OWNER}/repos'
        params = {'per_page': per_page, 'page': page, 'sort': 'updated'}
        response = session.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        if not data:
            break
            
        repos.extend(data)
        page += 1
        
        # Safety limit
        if page > 10:
            break
    
    return repos


def calculate_language_stats(repos):
    """Calculate language statistics from repositories with caching."""
    language_bytes = defaultdict(int)
    # Use headers only if token is available
    headers = HEADERS if GITHUB_TOKEN else {'Accept': 'application/vnd.github.v3+json'}
    
    for repo in repos:
        if repo.get('fork', False):
            continue
            
        # Fetch language stats for each repo
        lang_url = repo['languages_url']
        try:
            response = session.get(lang_url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                languages = response.json()
                for lang, bytes_count in languages.items():
                    language_bytes[lang] += bytes_count
        except requests.exceptions.RequestException:
            continue
    
    # Calculate percentages
    total_bytes = sum(language_bytes.values())
    if total_bytes == 0:
        return []
    
    language_stats = []
    for lang, bytes_count in language_bytes.items():
        percentage = (bytes_count / total_bytes) * 100
        language_stats.append({
            'name': lang,
            'percentage': percentage,
            'bytes': bytes_count,
            'color': LANGUAGE_COLORS.get(lang, '#808080')
        })
    
    # Sort by percentage
    language_stats.sort(key=lambda x: x['percentage'], reverse=True)
    return language_stats[:10]  # Top 10 languages


def fetch_commit_activity():
    """Fetch commit activity for the last year with retry logic."""
    # This endpoint requires authentication and repo access
    # We'll estimate from recent commits across all repos
    total_commits = 0
    one_year_ago = (datetime.now() - timedelta(days=365)).isoformat()
    # Use headers only if token is available
    headers = HEADERS if GITHUB_TOKEN else {'Accept': 'application/vnd.github.v3+json'}
    
    repos = fetch_user_repos()
    
    for repo in repos[:20]:  # Check top 20 repos to avoid rate limits
        try:
            url = f"{GITHUB_API_BASE}/repos/{REPO_OWNER}/{repo['name']}/commits"
            params = {'since': one_year_ago, 'per_page': 100, 'author': REPO_OWNER}
            response = session.get(url, headers=headers, params=params, timeout=30)
            
            if response.status_code == 200:
                commits = response.json()
                total_commits += len(commits)
                
                # Check if there are more pages
                if 'Link' in response.headers:
                    link_header = response.headers['Link']
                    if 'rel="last"' in link_header:
                        # Extract the last page number
                        match = re.search(r'page=(\d+)>; rel="last"', link_header)
                        if match:
                            last_page = int(match.group(1))
                            # Estimate total commits
                            total_commits += (last_page - 1) * 100
        except requests.exceptions.RequestException as e:
            print(f"Error fetching commits for {repo['name']}: {e}")
            continue
    
    return total_commits


def get_top_repos(repos, limit=6):
    """Get top repositories by stars + forks."""
    # Filter out forks
    non_fork_repos = [r for r in repos if not r.get('fork', False)]
    
    # Calculate score (stars + forks)
    for repo in non_fork_repos:
        repo['score'] = repo['stargazers_count'] + repo['forks_count']
    
    # Sort by score
    non_fork_repos.sort(key=lambda x: x['score'], reverse=True)
    
    return non_fork_repos[:limit]


def generate_stats_svg(user_info, total_commits, repos):
    """Generate enhanced stats SVG with animations."""
    public_repos = user_info.get('public_repos', 0)
    followers = user_info.get('followers', 0)
    following = user_info.get('following', 0)
    
    # Calculate total stars
    total_stars = sum(repo.get('stargazers_count', 0) for repo in repos if not repo.get('fork', False))
    
    svg_content = f'''<svg width="495" height="195" viewBox="0 0 495 195" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="stats-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{THEME['bg_dark']};stop-opacity:1" />
      <stop offset="50%" style="stop-color:{THEME['bg_light']};stop-opacity:1" />
      <stop offset="100%" style="stop-color:{THEME['bg_lighter']};stop-opacity:1" />
    </linearGradient>
    
    <linearGradient id="stat-gradient" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:{THEME['primary']}"/>
      <stop offset="100%" style="stop-color:{THEME['secondary']}"/>
    </linearGradient>
    
    <filter id="glow">
      <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    
    <style>
      @keyframes countUp {{ 0% {{ opacity: 0; transform: translateY(10px); }} 100% {{ opacity: 1; transform: translateY(0); }} }}
      @keyframes pulse {{ 0%, 100% {{ opacity: 0.6; }} 50% {{ opacity: 1; }} }}
      .count-up {{ animation: countUp 1s ease-out forwards; }}
      .stat-title {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 14px; fill: {THEME['text']}; font-weight: 600; }}
      .stat-value {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 28px; font-weight: bold; fill: url(#stat-gradient); }}
      .stat-label {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 11px; fill: {THEME['text_muted']}; }}
      .pulse {{ animation: pulse 3s ease-in-out infinite; }}
    </style>
  </defs>
  
  <rect width="495" height="195" rx="10" fill="url(#stats-bg)"/>
  <rect x="2" y="2" width="491" height="191" rx="8" fill="none" stroke="{THEME['primary']}" stroke-width="1.5" opacity="0.4"/>
  
  <!-- Header -->
  <text x="20" y="30" class="stat-title">📊 GitHub Statistics</text>
  <line x1="20" y1="45" x2="475" y2="45" stroke="{THEME['primary']}" stroke-width="0.5" opacity="0.3"/>
  
  <!-- Stats Grid -->
  <g class="count-up" style="animation-delay: 0.2s">
    <text x="60" y="85" class="stat-value" text-anchor="middle" filter="url(#glow)">{total_commits:,}</text>
    <text x="60" y="105" class="stat-label" text-anchor="middle">Commits</text>
    <text x="60" y="118" class="stat-label" text-anchor="middle">(Last Year)</text>
  </g>
  
  <g class="count-up" style="animation-delay: 0.4s">
    <text x="170" y="85" class="stat-value" text-anchor="middle" filter="url(#glow)">{public_repos}</text>
    <text x="170" y="105" class="stat-label" text-anchor="middle">Public Repos</text>
  </g>
  
  <g class="count-up" style="animation-delay: 0.6s">
    <text x="280" y="85" class="stat-value" text-anchor="middle" filter="url(#glow)">{followers}</text>
    <text x="280" y="105" class="stat-label" text-anchor="middle">Followers</text>
  </g>
  
  <g class="count-up" style="animation-delay: 0.8s">
    <text x="390" y="85" class="stat-value" text-anchor="middle" filter="url(#glow)">{total_stars}</text>
    <text x="390" y="105" class="stat-label" text-anchor="middle">Total Stars</text>
  </g>
  
  <!-- Progress Bar -->
  <rect x="20" y="140" width="455" height="6" rx="3" fill="{THEME['bg_lighter']}"/>
  <rect x="20" y="140" width="0" height="6" rx="3" fill="url(#stat-gradient)" class="pulse">
    <animate attributeName="width" from="0" to="350" dur="2s" fill="freeze"/>
  </rect>
  
  <!-- Footer -->
  <line x1="20" y1="160" x2="475" y2="160" stroke="{THEME['primary']}" stroke-width="0.5" opacity="0.2"/>
  <text x="247.5" y="180" class="stat-label" text-anchor="middle">
    ✨ Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}
  </text>
</svg>'''
    
    return svg_content


def generate_languages_svg(language_stats):
    """Generate enhanced top languages SVG with donut chart and animations."""
    
    # Calculate donut chart segments
    total_circumference = 251.2  # 2 * pi * 40
    segments = []
    offset = 0
    
    for lang in language_stats[:5]:
        segment_length = (lang['percentage'] / 100) * total_circumference
        color = lang.get('color', LANGUAGE_COLORS.get(lang['name'], '#808080'))
        segments.append({
            'name': lang['name'],
            'percentage': lang['percentage'],
            'color': color,
            'length': segment_length,
            'offset': offset
        })
        offset += segment_length
    
    svg_content = f'''<svg width="495" height="195" viewBox="0 0 495 195" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="langs-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{THEME['bg_dark']};stop-opacity:1" />
      <stop offset="50%" style="stop-color:{THEME['bg_light']};stop-opacity:1" />
      <stop offset="100%" style="stop-color:{THEME['bg_lighter']};stop-opacity:1" />
    </linearGradient>
    
    <style>
      @keyframes rotate {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}
      @keyframes fadeIn {{ 0% {{ opacity: 0; }} 100% {{ opacity: 1; }} }}
      @keyframes drawSegment {{ 0% {{ stroke-dashoffset: 251.2; }} 100% {{ stroke-dashoffset: 0; }} }}
      .lang-title {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 14px; fill: {THEME['text']}; font-weight: 600; }}
      .lang-name {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 12px; fill: {THEME['text']}; }}
      .lang-percent {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 11px; fill: {THEME['text_muted']}; }}
      .donut-segment {{ animation: drawSegment 1.5s ease-out forwards; }}
      .fade-in {{ animation: fadeIn 0.5s ease-out forwards; }}
    </style>
  </defs>
  
  <rect width="495" height="195" rx="10" fill="url(#langs-bg)"/>
  <rect x="2" y="2" width="491" height="191" rx="8" fill="none" stroke="{THEME['primary']}" stroke-width="1.5" opacity="0.4"/>
  
  <!-- Header -->
  <text x="20" y="30" class="lang-title">💻 Top Languages</text>
  <line x1="20" y1="45" x2="475" y2="45" stroke="{THEME['primary']}" stroke-width="0.5" opacity="0.3"/>
  
  <!-- Donut Chart -->
  <g transform="translate(100, 115)">
    <!-- Background circle -->
    <circle cx="0" cy="0" r="40" fill="none" stroke="{THEME['bg_lighter']}" stroke-width="12"/>
'''
    
    # Add donut segments
    for i, seg in enumerate(segments):
        delay = i * 0.3
        svg_content += f'''
    <!-- {seg['name']} segment -->
    <circle cx="0" cy="0" r="40" fill="none" stroke="{seg['color']}" stroke-width="12"
            stroke-dasharray="{seg['length']} {total_circumference}" stroke-dashoffset="-{seg['offset']}" 
            class="donut-segment" transform="rotate(-90)" style="animation-delay: {delay}s"/>
'''
    
    # Center text
    num_languages = len(language_stats)
    svg_content += f'''
    <!-- Center text -->
    <text x="0" y="5" text-anchor="middle" font-family="'Segoe UI', Arial, sans-serif" 
          font-size="14" fill="{THEME['text']}" font-weight="600">{num_languages}+</text>
    <text x="0" y="18" text-anchor="middle" font-family="'Segoe UI', Arial, sans-serif" 
          font-size="8" fill="{THEME['text_muted']}">Languages</text>
  </g>
  
  <!-- Legend -->
  <g transform="translate(200, 60)" class="fade-in">
'''
    
    # Add legend items
    for i, seg in enumerate(segments):
        y_pos = i * 25 + 8
        bar_width = (seg['percentage'] / 100) * 100
        svg_content += f'''
    <!-- {seg['name']} -->
    <circle cx="0" cy="{y_pos}" r="5" fill="{seg['color']}"/>
    <text x="15" y="{y_pos + 4}" class="lang-name">{seg['name']}</text>
    <text x="140" y="{y_pos + 4}" class="lang-percent">{seg['percentage']:.1f}%</text>
'''
    
    svg_content += '''  </g>
  
  <!-- Progress bars -->
  <g transform="translate(365, 60)" class="fade-in" style="animation-delay: 0.5s">
'''
    
    # Add progress bars
    for i, seg in enumerate(segments):
        y_pos = i * 25 + 3
        bar_width = (seg['percentage'] / 100) * 100
        svg_content += f'''
    <rect x="0" y="{y_pos}" width="100" height="6" rx="3" fill="{THEME['bg_lighter']}"/>
    <rect x="0" y="{y_pos}" width="{bar_width}" height="6" rx="3" fill="{seg['color']}"/>
'''
    
    svg_content += '''  </g>
</svg>'''
    
    return svg_content


def generate_top_repos_markdown(top_repos):
    """Generate markdown for top repositories."""
    markdown = ''
    
    for i, repo in enumerate(top_repos):
        name = repo['name']
        description = repo.get('description', 'No description provided')
        stars = repo['stargazers_count']
        forks = repo['forks_count']
        language = repo.get('language', 'N/A')
        html_url = repo['html_url']
        
        # Truncate description if too long
        if len(description) > 100:
            description = description[:97] + '...'
        
        markdown += f'''
#### 🚀 [{name}]({html_url})
{description}

![{language}](https://img.shields.io/badge/{language}-informational?style=flat-square)
⭐ {stars} | 🍴 {forks}

'''
    
    return markdown


def update_readme(user_info, total_commits, language_stats, top_repos):
    """Update README.md with dynamic content between markers."""
    
    # Read current README
    with open(README_PATH, 'r', encoding='utf-8') as f:
        readme_content = f.read()
    
    # Generate SVG files
    stats_svg = generate_stats_svg(user_info, total_commits, fetch_user_repos())
    langs_svg = generate_languages_svg(language_stats)
    
    # Save SVG files
    with open(f'{ASSETS_DIR}/stats.svg', 'w', encoding='utf-8') as f:
        f.write(stats_svg)
    
    with open(f'{ASSETS_DIR}/top-langs.svg', 'w', encoding='utf-8') as f:
        f.write(langs_svg)
    
    # Generate dynamic content
    dynamic_content = f'''<!-- DYNAMIC_START -->
## 📊 Live GitHub Statistics

<div align="center">
  
  <img src="./assets/stats.svg" alt="GitHub Statistics" />
  <img src="./assets/top-langs.svg" alt="Top Languages" />
  
</div>

<div align="center">
  
  [![GitHub Streak](https://streak-stats.demolab.com/?user={REPO_OWNER}&theme=tokyonight)](https://git.io/streak-stats)
  
</div>

<div align="center">
  
  <img src="https://github-readme-activity-graph.vercel.app/graph?username={REPO_OWNER}&theme=tokyo-night&hide_border=true&area=true" width="100%">
  
</div>

---

## 🌟 Top Repositories

<div align="center">

{generate_top_repos_markdown(top_repos)}

</div>

<!-- DYNAMIC_END -->'''
    
    # Replace content between markers
    pattern = r'<!-- DYNAMIC_START -->.*?<!-- DYNAMIC_END -->'
    
    if '<!-- DYNAMIC_START -->' in readme_content:
        # Update existing dynamic section
        readme_content = re.sub(pattern, dynamic_content, readme_content, flags=re.DOTALL)
    else:
        # Append dynamic section before the last closing div
        readme_content = readme_content.rstrip() + '\n\n' + dynamic_content + '\n'
    
    # Write updated README
    with open(README_PATH, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✅ README.md updated successfully!")


def main(dry_run=False):
    """Main execution function."""
    print("🚀 Starting GitHub README update...")
    
    if not GITHUB_TOKEN:
        print("⚠️  Warning: GITHUB_TOKEN not set. API rate limits will apply.")
        print("💡 The script will attempt to fetch public data without authentication.")
    
    try:
        # Fetch data
        print("📊 Fetching user information...")
        user_info = fetch_user_info()
        
        print("📦 Fetching repositories...")
        repos = fetch_user_repos()
        
        print("💻 Calculating language statistics...")
        language_stats = calculate_language_stats(repos)
        
        print("📈 Fetching commit activity...")
        total_commits = fetch_commit_activity()
        
        print("⭐ Finding top repositories...")
        top_repos = get_top_repos(repos)
        
        # Debug output
        print(f"\n📋 Summary:")
        print(f"   - User: {user_info['login']}")
        print(f"   - Public Repos: {user_info['public_repos']}")
        print(f"   - Total Commits (last year): {total_commits}")
        print(f"   - Top Languages: {', '.join([l['name'] for l in language_stats[:5]])}")
        print(f"   - Top Repos: {', '.join([r['name'] for r in top_repos])}")
        
        if dry_run:
            print("\n🔍 Dry run mode - no files will be modified.")
            return
        
        # Update README
        print("\n✏️  Updating README.md...")
        update_readme(user_info, total_commits, language_stats, top_repos)
        
        print("\n✨ Update completed successfully!")
        
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            print(f"❌ API rate limit exceeded: {e}")
            print("💡 This script requires a GITHUB_TOKEN to avoid rate limits.")
            print("   Set it as an environment variable: export GITHUB_TOKEN=your_token")
            sys.exit(1)
        else:
            print(f"❌ API request failed: {e}")
            sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    # Check for dry-run flag
    dry_run = '--dry-run' in sys.argv or '-d' in sys.argv
    main(dry_run=dry_run)
