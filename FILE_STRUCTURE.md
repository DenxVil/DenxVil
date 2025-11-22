# Project File Structure

## Complete Directory Layout

```
DenxVil/
├── .github/
│   └── workflows/
│       └── update-readme.yml        # GitHub Actions workflow (3KB)
│
├── assets/                          # SVG assets directory
│   ├── 3d-hero.svg                 # Animated 3D hero banner (6.5KB)
│   ├── pro-badge.svg               # GitHub Pro badge with animation (2.5KB)
│   ├── stats.svg                   # Dynamic stats card (auto-generated)
│   └── top-langs.svg               # Top languages chart (auto-generated)
│
├── img/                            # Existing images directory
│   ├── .gitkeep
│   ├── IMG_4934.jpeg
│   ├── IMG_6597.png
│   └── img.txt
│
├── scripts/                        # Update scripts
│   ├── update_readme.py           # Main update script (14KB)
│   └── test_update.py             # Validation test script (3KB)
│
├── .gitignore                     # Git ignore patterns (346B)
├── DYNAMIC_README_GUIDE.md        # Complete user guide (7KB)
├── FILE_STRUCTURE.md              # This file
├── PR_SUMMARY.md                  # Detailed PR summary (10KB)
├── PREVIEW.md                     # (Existing file)
├── README.md                      # Main profile README (redesigned)
├── README_SETUP.md                # (Existing file)
└── requirements.txt               # Python dependencies (17B)
```

## File Descriptions

### Core Files

#### `README.md` (Main Profile README)
**Modified** - The main GitHub profile README, now featuring:
- 3D animated hero banner
- GitHub Pro badge display
- Dynamic statistics section (between markers)
- Call-to-action buttons
- Social links and highlights
- Preserved existing content

**Key Sections:**
- `<!-- DYNAMIC_START -->` to `<!-- DYNAMIC_END -->` - Auto-updated daily
- Static sections - Manually maintained

---

### Assets Directory (`/assets`)

#### `3d-hero.svg` (6.5KB)
**New** - Animated SVG hero banner featuring:
- Floating geometric shapes with animations
- Gradient backgrounds (dark theme)
- Glowing effects and shadows
- Modern typography
- "DenxVil" text with 3D effect
- Subtitle: "AI Engineer & Full Stack Developer"
- Decorative corner elements
- Tech stack icon representations

**Animations:**
- Float animations (6-8s cycles)
- Rotation (20s)
- Pulse effects (3s)

#### `pro-badge.svg` (2.5KB)
**New** - Animated GitHub Pro badge with:
- Purple gradient background
- GitHub logo
- "PRO" text
- Shine effect animation (3s loop)
- Gold star decoration
- Glow filter

#### `stats.svg` (~2KB, auto-generated)
**New** - Placeholder initially, then auto-generated daily
Displays:
- Total commits (last year)
- Public repositories count
- Followers count
- Following count
- Last updated timestamp

**Styling:**
- Dark gradient background
- Cyan accent color (#00d9ff)
- Modern font (Segoe UI)
- Glass-morphism border

#### `top-langs.svg` (~2KB, auto-generated)
**New** - Placeholder initially, then auto-generated daily
Shows:
- Top 5 programming languages
- Percentage bars with colors
- Language icons (colored circles)
- Percentage labels

**Color Scheme:**
- Python: #3776AB
- JavaScript: #F7DF1E
- TypeScript: #007ACC
- HTML: #E34F26
- CSS: #1572B6
- And more...

---

### Scripts Directory (`/scripts`)

#### `update_readme.py` (14KB)
**New** - Main Python script that:

**Functions:**
- `fetch_user_info()` - Get GitHub user profile
- `fetch_user_repos()` - List all public repositories
- `calculate_language_stats()` - Analyze language usage
- `fetch_commit_activity()` - Count commits (last year)
- `get_top_repos()` - Find top 6 repos by stars+forks
- `generate_stats_svg()` - Create stats visualization
- `generate_languages_svg()` - Create language chart
- `generate_top_repos_markdown()` - Format repo list
- `update_readme()` - Update README dynamic section
- `main()` - Orchestrate the update process

**Features:**
- GitHub REST API integration
- Dry-run mode (`--dry-run` flag)
- Error handling and logging
- Rate limit awareness
- Preserves static content
- Only updates between markers

**Requirements:**
- Python 3.8+
- `requests` library
- `GITHUB_TOKEN` environment variable (optional but recommended)

#### `test_update.py` (3KB)
**New** - Validation script that checks:
- All required functions exist
- All constants defined
- Dynamic markers present in README
- Assets directory exists
- All asset files present
- Script imports successfully

**Usage:**
```bash
python scripts/test_update.py
```

**Output:**
- ✅ Validation passed messages
- ❌ Error messages if issues found
- Exit code 0 on success, 1 on failure

---

### Workflow File (`.github/workflows`)

#### `update-readme.yml` (3KB)
**New** - GitHub Actions workflow that:

**Triggers:**
- Schedule: Daily at 00:00 UTC (cron)
- Push: On push to main branch
- Manual: Workflow dispatch with dry-run option

**Steps:**
1. Checkout repository
2. Setup Python 3.11
3. Install dependencies from requirements.txt
4. Run update script (with GITHUB_TOKEN)
5. Check for changes
6. Commit and push (if changes exist)
7. Generate workflow summary

**Configuration:**
- Permissions: `contents: write`
- Runs on: `ubuntu-latest`
- Python cache: Enabled
- Commit message: `🤖 Auto-update README [skip ci]`
- Committer: `github-actions[bot]`

---

### Documentation Files

#### `DYNAMIC_README_GUIDE.md` (7KB)
**New** - Complete documentation covering:
- Project structure overview
- How the system works
- Local testing instructions
- GitHub Actions explanation
- Customization options
- Troubleshooting guide
- Security considerations
- Maintenance schedule
- FAQ section

**Sections:**
1. Features overview
2. Technical architecture
3. Testing procedures
4. Customization guide
5. Security notes
6. Troubleshooting
7. Maintenance tips

#### `PR_SUMMARY.md` (10KB)
**New** - Detailed pull request summary:
- Objectives and deliverables
- Complete file list with sizes
- Design specifications
- Color scheme and animations
- Security analysis
- Testing performed
- Deployment instructions
- Expected results
- Success criteria

#### `FILE_STRUCTURE.md` (This File)
**New** - Visual representation of project structure with:
- Directory tree
- File descriptions
- Size information
- Status (new/modified)
- Purpose explanations

---

### Configuration Files

#### `requirements.txt` (17B)
**New** - Python dependencies:
```
requests>=2.31.0
```

**Why requests?**
- For GitHub REST API calls
- Widely used, stable, secure
- No additional dependencies needed

#### `.gitignore` (346B)
**New** - Patterns to ignore:
- Python artifacts (`__pycache__`, `*.pyc`)
- Virtual environments (`venv/`, `env/`)
- IDE files (`.vscode/`, `.idea/`)
- OS files (`.DS_Store`, `Thumbs.db`)
- Temporary files (`*.tmp`, `*.bak`)
- Build directories (`dist/`, `build/`)

---

### Existing Files (Preserved)

#### `PREVIEW.md`
**Unchanged** - Existing file preserved

#### `README_SETUP.md`
**Unchanged** - Existing file preserved

#### `img/` directory
**Unchanged** - Existing images preserved

---

## File Size Summary

| Category | Files | Total Size |
|----------|-------|------------|
| Assets | 4 | ~12 KB |
| Scripts | 2 | ~17 KB |
| Documentation | 3 | ~26 KB |
| Workflow | 1 | 3 KB |
| Config | 2 | ~400 B |
| **Total New** | **12** | **~58 KB** |
| Modified | 1 | README.md |

---

## Dynamic vs Static Files

### Dynamic (Auto-Updated Daily)
- `assets/stats.svg` - Regenerated with latest stats
- `assets/top-langs.svg` - Regenerated with language data
- `README.md` (dynamic section) - Updated between markers

### Static (Manually Maintained)
- `assets/3d-hero.svg` - Hero banner design
- `assets/pro-badge.svg` - Badge design
- `scripts/update_readme.py` - Update logic
- `.github/workflows/update-readme.yml` - Workflow config
- Documentation files
- `README.md` (static sections) - Content outside markers

---

## Workflow Dependencies

```
Workflow (update-readme.yml)
    ↓
Python 3.11 + requirements.txt
    ↓
update_readme.py
    ↓
GitHub REST API (with GITHUB_TOKEN)
    ↓
Generate: stats.svg, top-langs.svg
    ↓
Update: README.md (dynamic section)
    ↓
Commit & Push changes
```

---

## Version Control Status

### New Files (12):
- ✅ `.github/workflows/update-readme.yml`
- ✅ `.gitignore`
- ✅ `DYNAMIC_README_GUIDE.md`
- ✅ `FILE_STRUCTURE.md`
- ✅ `PR_SUMMARY.md`
- ✅ `assets/3d-hero.svg`
- ✅ `assets/pro-badge.svg`
- ✅ `assets/stats.svg`
- ✅ `assets/top-langs.svg`
- ✅ `requirements.txt`
- ✅ `scripts/update_readme.py`
- ✅ `scripts/test_update.py`

### Modified Files (1):
- ✅ `README.md`

### Unchanged Files:
- All files in `img/` directory
- `PREVIEW.md`
- `README_SETUP.md`

---

## Access Patterns

### Read by Workflow:
- `requirements.txt`
- `scripts/update_readme.py`
- `README.md` (to update)

### Written by Workflow:
- `assets/stats.svg`
- `assets/top-langs.svg`
- `README.md` (dynamic section)

### Read by Users:
- `README.md` (GitHub profile view)
- `DYNAMIC_README_GUIDE.md` (documentation)
- `PR_SUMMARY.md` (PR details)
- All asset SVGs (embedded in README)

### Executed:
- `scripts/update_readme.py` (by workflow)
- `scripts/test_update.py` (for validation)

---

## Maintenance Schedule

### Daily (Automated):
- Generate new `stats.svg`
- Generate new `top-langs.svg`
- Update `README.md` dynamic section
- Commit changes (if any)

### Weekly (Manual Review):
- Check workflow logs
- Verify stats accuracy
- Review any errors

### Monthly (Maintenance):
- Update dependencies (if needed)
- Review and optimize script
- Check for API changes
- Update documentation

### As Needed:
- Customize colors/styling
- Add new statistics
- Modify hero banner
- Adjust update frequency

---

## Security Considerations

### Public Files (Safe to Share):
- All files in this repository are public
- No secrets or credentials stored
- Uses only `GITHUB_TOKEN` (auto-provided by GitHub)

### Generated Files:
- SVGs contain only public GitHub data
- No personal or sensitive information
- Safe to display on public profile

### Script Safety:
- Only reads public data via GitHub API
- Writes only to repository files
- No external API calls
- No data sent to third parties

---

**Last Updated**: 2024  
**Maintained By**: DenxVil  
**Status**: ✅ Complete and Documented
