#!/usr/bin/env python3
"""
GitHub Profile README Updater
Fetches dynamic GitHub data and updates the README.md file between markers.
Uses GitHub REST API with GITHUB_TOKEN for authentication.
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta
from collections import defaultdict
import re

# Configuration
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '')
REPO_OWNER = 'DenxVil'
REPO_NAME = 'DenxVil'
README_PATH = 'README.md'
ASSETS_DIR = 'assets'

# API endpoints
GITHUB_API_BASE = 'https://api.github.com'
HEADERS = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}


def fetch_user_info():
    """Fetch basic user profile information."""
    url = f'{GITHUB_API_BASE}/users/{REPO_OWNER}'
    # Use headers only if token is available
    headers = HEADERS if GITHUB_TOKEN else {'Accept': 'application/vnd.github.v3+json'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def fetch_user_repos():
    """Fetch all user repositories."""
    repos = []
    page = 1
    per_page = 100
    # Use headers only if token is available
    headers = HEADERS if GITHUB_TOKEN else {'Accept': 'application/vnd.github.v3+json'}
    
    while True:
        url = f'{GITHUB_API_BASE}/users/{REPO_OWNER}/repos'
        params = {'per_page': per_page, 'page': page, 'sort': 'updated'}
        response = requests.get(url, headers=headers, params=params)
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
    """Calculate language statistics from repositories."""
    language_bytes = defaultdict(int)
    # Use headers only if token is available
    headers = HEADERS if GITHUB_TOKEN else {'Accept': 'application/vnd.github.v3+json'}
    
    for repo in repos:
        if repo.get('fork', False):
            continue
            
        # Fetch language stats for each repo
        lang_url = repo['languages_url']
        response = requests.get(lang_url, headers=headers)
        
        if response.status_code == 200:
            languages = response.json()
            for lang, bytes_count in languages.items():
                language_bytes[lang] += bytes_count
    
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
            'bytes': bytes_count
        })
    
    # Sort by percentage
    language_stats.sort(key=lambda x: x['percentage'], reverse=True)
    return language_stats[:10]  # Top 10 languages


def fetch_commit_activity():
    """Fetch commit activity for the last year."""
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
            response = requests.get(url, headers=headers, params=params)
            
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
        except Exception as e:
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
    """Generate stats SVG."""
    public_repos = user_info.get('public_repos', 0)
    followers = user_info.get('followers', 0)
    following = user_info.get('following', 0)
    
    svg_content = f'''<svg width="495" height="195" viewBox="0 0 495 195" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="stats-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#1a1a2e;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#16213e;stop-opacity:1" />
    </linearGradient>
    <style>
      .stat-title {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 14px; fill: #a0a0a0; }}
      .stat-value {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 28px; font-weight: bold; fill: #00d9ff; }}
      .stat-label {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 12px; fill: #808080; }}
    </style>
  </defs>
  
  <rect width="495" height="195" rx="10" fill="url(#stats-bg)"/>
  <rect x="2" y="2" width="491" height="191" rx="8" fill="none" stroke="#00d9ff" stroke-width="2" opacity="0.3"/>
  
  <text x="20" y="30" class="stat-title">GitHub Statistics</text>
  
  <!-- Total Commits (Last Year) -->
  <text x="30" y="80" class="stat-value">{total_commits:,}</text>
  <text x="30" y="95" class="stat-label">Total Commits</text>
  <text x="30" y="107" class="stat-label">(Last Year)</text>
  
  <!-- Public Repos -->
  <text x="190" y="80" class="stat-value">{public_repos}</text>
  <text x="190" y="95" class="stat-label">Public Repos</text>
  
  <!-- Followers -->
  <text x="320" y="80" class="stat-value">{followers}</text>
  <text x="320" y="95" class="stat-label">Followers</text>
  
  <!-- Following -->
  <text x="420" y="80" class="stat-value">{following}</text>
  <text x="420" y="95" class="stat-label">Following</text>
  
  <!-- Decorative line -->
  <line x1="20" y1="130" x2="475" y2="130" stroke="#00d9ff" stroke-width="1" opacity="0.2"/>
  
  <!-- Last updated -->
  <text x="247.5" y="165" class="stat-label" text-anchor="middle">
    Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}
  </text>
</svg>'''
    
    return svg_content


def generate_languages_svg(language_stats):
    """Generate top languages SVG."""
    colors = {
        'Python': '#3776AB',
        'JavaScript': '#F7DF1E',
        'TypeScript': '#007ACC',
        'HTML': '#E34F26',
        'CSS': '#1572B6',
        'Java': '#007396',
        'C++': '#00599C',
        'C': '#A8B9CC',
        'Go': '#00ADD8',
        'Rust': '#000000',
    }
    
    svg_content = '''<svg width="495" height="195" viewBox="0 0 495 195" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="langs-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#1a1a2e;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#16213e;stop-opacity:1" />
    </linearGradient>
    <style>
      .lang-title { font-family: 'Segoe UI', Arial, sans-serif; font-size: 14px; fill: #a0a0a0; }
      .lang-name { font-family: 'Segoe UI', Arial, sans-serif; font-size: 12px; fill: #ffffff; }
      .lang-percent { font-family: 'Segoe UI', Arial, sans-serif; font-size: 12px; fill: #a0a0a0; }
    </style>
  </defs>
  
  <rect width="495" height="195" rx="10" fill="url(#langs-bg)"/>
  <rect x="2" y="2" width="491" height="191" rx="8" fill="none" stroke="#36d1dc" stroke-width="2" opacity="0.3"/>
  
  <text x="20" y="30" class="lang-title">Top Languages</text>
'''
    
    y_offset = 55
    for i, lang in enumerate(language_stats[:5]):
        lang_name = lang['name']
        percentage = lang['percentage']
        color = colors.get(lang_name, '#808080')
        
        bar_width = (percentage / 100) * 420
        
        svg_content += f'''
  <!-- {lang_name} -->
  <circle cx="30" cy="{y_offset}" r="5" fill="{color}"/>
  <text x="45" y="{y_offset + 4}" class="lang-name">{lang_name}</text>
  <text x="460" y="{y_offset + 4}" class="lang-percent" text-anchor="end">{percentage:.1f}%</text>
  <rect x="45" y="{y_offset + 8}" width="410" height="4" rx="2" fill="#2d2d2d"/>
  <rect x="45" y="{y_offset + 8}" width="{bar_width}" height="4" rx="2" fill="{color}"/>
'''
        y_offset += 25
    
    svg_content += '''
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
