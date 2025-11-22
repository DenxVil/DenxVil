# Dynamic 3D README System Guide

This guide explains how the dynamic 3D README system works and how to maintain it.

## 📁 Project Structure

```
DenxVil/
├── README.md                          # Main profile README (with dynamic sections)
├── assets/
│   ├── 3d-hero.svg                   # 3D animated hero banner
│   ├── pro-badge.svg                 # GitHub Pro badge
│   ├── stats.svg                     # Auto-generated stats (updated daily)
│   └── top-langs.svg                 # Auto-generated language stats (updated daily)
├── scripts/
│   └── update_readme.py              # Python script to fetch GitHub data & update README
├── .github/
│   └── workflows/
│       └── update-readme.yml         # GitHub Actions workflow (runs daily)
└── requirements.txt                  # Python dependencies
```

## 🎨 Features

### 1. **3D Hero Banner** (`assets/3d-hero.svg`)
- Modern, animated SVG with floating geometric shapes
- Gradient backgrounds and glowing effects
- Responsive design that works across all devices
- Cross-platform compatible (no external dependencies)

### 2. **GitHub Pro Badge** (`assets/pro-badge.svg`)
- Custom animated badge with shine effect
- Fallback for shields.io badge
- Highlights GitHub Pro subscription

### 3. **Dynamic Statistics** (Auto-updated daily)
The script fetches and displays:
- Total commits (last year)
- Public repositories count
- Followers and following counts
- Top 5 programming languages with percentages
- Top 6 repositories by stars + forks
- Real-time activity graphs

### 4. **Automated Updates**
- Runs daily at 00:00 UTC via GitHub Actions
- Triggers on push to main branch
- Can be manually triggered via workflow dispatch
- Uses only `GITHUB_TOKEN` (no additional secrets needed)

## 🚀 How It Works

### Update Script (`scripts/update_readme.py`)

The Python script performs the following:

1. **Fetches User Profile Data**
   - Uses GitHub REST API
   - Retrieves basic profile info (name, bio, followers, etc.)

2. **Analyzes Repositories**
   - Fetches all public repositories
   - Calculates language statistics
   - Identifies top repositories by popularity

3. **Generates SVG Assets**
   - Creates `assets/stats.svg` with current statistics
   - Creates `assets/top-langs.svg` with language breakdown
   - Updates with current timestamp

4. **Updates README**
   - Finds content between `<!-- DYNAMIC_START -->` and `<!-- DYNAMIC_END -->` markers
   - Replaces only the dynamic section
   - Preserves all static content

### GitHub Actions Workflow (`.github/workflows/update-readme.yml`)

The workflow:
- **Schedule**: Runs daily at 00:00 UTC
- **Push trigger**: Runs when code is pushed to main
- **Manual trigger**: Can be run manually with optional dry-run mode

**Workflow Steps:**
1. Checkout repository
2. Set up Python 3.11
3. Install dependencies from `requirements.txt`
4. Run update script with `GITHUB_TOKEN`
5. Commit and push changes (if any)
6. Generate summary report

## 🛠️ Testing Locally

### Prerequisites
```bash
# Install Python 3.8+
python3 --version

# Install dependencies
pip install -r requirements.txt

# Set GitHub token (optional, but recommended to avoid rate limits)
export GITHUB_TOKEN=your_github_token_here
```

### Dry Run Mode
Test the script without modifying files:
```bash
python scripts/update_readme.py --dry-run
```

### Full Update
Run the script to update README and assets:
```bash
python scripts/update_readme.py
```

## 🔧 Customization

### Changing Update Frequency

Edit `.github/workflows/update-readme.yml`:

```yaml
schedule:
  - cron: '0 0 * * *'  # Daily at 00:00 UTC
  # Examples:
  # - cron: '0 */6 * * *'  # Every 6 hours
  # - cron: '0 0 * * 0'    # Weekly on Sunday
  # - cron: '0 0 1 * *'    # Monthly on 1st
```

### Modifying Dynamic Section

The dynamic section is between markers in `README.md`:

```markdown
<!-- DYNAMIC_START -->
... dynamic content here ...
<!-- DYNAMIC_END -->
```

**Important**: Don't remove these markers! The script uses them to know where to update.

### Customizing Stats Display

Edit `scripts/update_readme.py`:

**Change top languages count:**
```python
language_stats = calculate_language_stats(repos)[:10]  # Change 10 to desired number
```

**Change top repos count:**
```python
top_repos = get_top_repos(repos, limit=6)  # Change 6 to desired number
```

**Modify SVG styling:**
- Edit the `generate_stats_svg()` function for stats appearance
- Edit the `generate_languages_svg()` function for language chart appearance

### Adding New Data Points

To add new statistics:

1. Add a new function to fetch the data in `scripts/update_readme.py`
2. Update the `generate_stats_svg()` or create a new SVG generator
3. Call the function in `main()` and pass data to `update_readme()`

## 🐛 Troubleshooting

### Script fails with "403 Forbidden"
**Solution**: The GitHub API rate limit is exceeded. This shouldn't happen in GitHub Actions as `GITHUB_TOKEN` is automatically provided. For local testing, set your token:
```bash
export GITHUB_TOKEN=your_token
```

### Changes not appearing in README
1. Check that dynamic markers exist in README.md
2. Verify workflow is enabled in repository settings
3. Check workflow run logs in Actions tab
4. Ensure `GITHUB_TOKEN` has write permissions

### SVG not displaying
- Clear browser cache
- Check that SVG files exist in `assets/` directory
- Verify SVG syntax is valid (test in browser DevTools)

### Workflow not running on schedule
- GitHub may delay scheduled workflows during high load
- Workflow must be in the default branch (usually `main`)
- Repository must have activity in the last 60 days

## 📊 Understanding the Metrics

### Total Commits (Last Year)
- Counts commits authored by you across all repositories
- Only includes the last 365 days
- Limited to top 20 most active repositories (to respect API rate limits)

### Top Languages
- Calculated from bytes of code in all non-forked repositories
- Shows percentage distribution
- Colors match official GitHub language colors

### Top Repositories
- Ranked by score: (stars + forks)
- Excludes forked repositories
- Shows description, language, and statistics

## 🔒 Security

- **No secrets required**: Uses only the built-in `GITHUB_TOKEN`
- **Permissions**: Workflow has `contents: write` to commit changes
- **Rate limiting**: Respects GitHub API rate limits
- **Safe updates**: Only modifies content between markers

## 📝 Maintenance

### Weekly Checks
- ✅ Verify README displays correctly on GitHub
- ✅ Check that workflow runs successfully
- ✅ Review generated SVG files for accuracy

### Monthly Reviews
- 📊 Review top repositories list
- 🎨 Update hero banner if needed
- 🔄 Check for dependency updates

### When Things Change
If you:
- Rename your username → Update `REPO_OWNER` in script
- Move to organization → Update `REPO_OWNER` in script
- Archive repositories → Script automatically excludes them
- Make repositories private → They won't appear in public stats

## 🆘 Getting Help

1. **Check Workflow Logs**: Go to Actions tab → Update README workflow → View logs
2. **Test Locally**: Run with `--dry-run` flag to see what would change
3. **Validate Workflow**: Use GitHub's workflow validator
4. **Review Changes**: Check the git diff before pushing

## 📜 License

This README system is part of the DenxVil profile repository and is free to use and modify.

---

**Last Updated**: 2024
**Maintained By**: DenxVil
**Status**: ✅ Active and Auto-updating
