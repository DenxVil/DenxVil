#!/usr/bin/env python3
"""
Simple test script to validate update_readme.py structure
"""

import sys
import os

# Add the scripts directory to path
sys.path.insert(0, os.path.dirname(__file__))

try:
    import update_readme
    
    # Check that all required functions exist
    required_functions = [
        'fetch_user_info',
        'fetch_user_repos',
        'calculate_language_stats',
        'fetch_commit_activity',
        'get_top_repos',
        'generate_stats_svg',
        'generate_languages_svg',
        'generate_top_repos_markdown',
        'update_readme',
        'main'
    ]
    
    missing_functions = []
    for func_name in required_functions:
        if not hasattr(update_readme, func_name):
            missing_functions.append(func_name)
    
    if missing_functions:
        print(f"❌ Missing functions: {', '.join(missing_functions)}")
        sys.exit(1)
    
    # Check that constants are defined
    required_constants = [
        'GITHUB_TOKEN',
        'REPO_OWNER',
        'REPO_NAME',
        'README_PATH',
        'ASSETS_DIR',
        'GITHUB_API_BASE',
        'HEADERS'
    ]
    
    missing_constants = []
    for const_name in required_constants:
        if not hasattr(update_readme, const_name):
            missing_constants.append(const_name)
    
    if missing_constants:
        print(f"❌ Missing constants: {', '.join(missing_constants)}")
        sys.exit(1)
    
    print("✅ All required functions and constants are present")
    print("✅ Script structure is valid")
    
    # Check that marker comments exist in README
    readme_path = os.path.join(os.path.dirname(__file__), '..', 'README.md')
    with open(readme_path, 'r', encoding='utf-8') as f:
        readme_content = f.read()
    
    if '<!-- DYNAMIC_START -->' not in readme_content:
        print("❌ Missing <!-- DYNAMIC_START --> marker in README.md")
        sys.exit(1)
    
    if '<!-- DYNAMIC_END -->' not in readme_content:
        print("❌ Missing <!-- DYNAMIC_END --> marker in README.md")
        sys.exit(1)
    
    print("✅ Dynamic section markers found in README.md")
    
    # Check that assets directory exists
    assets_path = os.path.join(os.path.dirname(__file__), '..', 'assets')
    if not os.path.exists(assets_path):
        print("❌ Assets directory not found")
        sys.exit(1)
    
    print("✅ Assets directory exists")
    
    # Check that required asset files exist
    required_assets = ['3d-hero.svg', 'pro-badge.svg', 'stats.svg', 'top-langs.svg']
    missing_assets = []
    for asset in required_assets:
        asset_path = os.path.join(assets_path, asset)
        if not os.path.exists(asset_path):
            missing_assets.append(asset)
    
    if missing_assets:
        print(f"⚠️  Missing asset files: {', '.join(missing_assets)}")
    else:
        print("✅ All required asset files exist")
    
    print("\n✨ All validation checks passed!")
    
except ImportError as e:
    print(f"❌ Failed to import update_readme: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Validation failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
