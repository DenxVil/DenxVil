#!/usr/bin/env bash

################################################################################
# 3D Profile README Assets Generator
################################################################################
#
# Purpose: Generate and update dynamic SVG assets and README content sections
#          for the 3D profile design.
#
# Components this script should generate (when fully implemented):
#   1. stats.svg - GitHub statistics visualization
#   2. top-langs.svg - Top programming languages chart
#   3. Dynamic README content between DYNAMIC_START and DYNAMIC_END markers
#
# Current Status: PLACEHOLDER
# This is a skeleton script that will be implemented to call a Node.js or
# Python generator for creating the actual SVG assets and updating README.
#
# Usage:
#   ./scripts/generate_readme_assets.sh
#
# Environment Variables:
#   GITHUB_TOKEN - Required for GitHub API access (set in CI/CD)
#
# Exit Codes:
#   0 - Success
#   1 - Error occurred
#
################################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  🎨 3D Profile README Assets Generator${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

################################################################################
# 1. Environment Check
################################################################################

echo -e "${YELLOW}🔍 Checking environment...${NC}"

# Check if GITHUB_TOKEN is set
if [ -z "$GITHUB_TOKEN" ]; then
    echo -e "${YELLOW}⚠️  Warning: GITHUB_TOKEN is not set${NC}"
    echo -e "${YELLOW}   API rate limits will apply for unauthenticated requests${NC}"
else
    echo -e "${GREEN}✅ GITHUB_TOKEN is set${NC}"
fi

# Check if required directories exist
if [ ! -d "assets" ]; then
    echo -e "${YELLOW}⚠️  Creating assets directory...${NC}"
    mkdir -p assets
fi

################################################################################
# 2. Check for Update Scripts
################################################################################

echo ""
echo -e "${YELLOW}🔍 Checking for update scripts...${NC}"

# Priority 1: Python script (preferred - currently exists)
# This is checked first because the repository already has a Python implementation
if [ -f "scripts/update_readme.py" ]; then
    echo -e "${GREEN}✅ Found Python update script${NC}"
    echo -e "${BLUE}📊 Running Python update script...${NC}"
    
    # Check if Python is available
    if command -v python3 &> /dev/null; then
        python3 scripts/update_readme.py
        EXIT_CODE=$?
        
        if [ $EXIT_CODE -eq 0 ]; then
            echo -e "${GREEN}✅ Successfully generated assets with Python script${NC}"
            exit 0
        else
            echo -e "${RED}❌ Python script failed with exit code $EXIT_CODE${NC}"
            exit 1
        fi
    else
        echo -e "${RED}❌ Python 3 is not installed${NC}"
        exit 1
    fi
fi

# Priority 2: Node.js script (alternative if Python not available)
# Note: If both Python and Node.js scripts exist, Python takes precedence
if [ -f "scripts/update_readme.js" ]; then
    echo -e "${GREEN}✅ Found Node.js update script${NC}"
    echo -e "${BLUE}📊 Running Node.js update script...${NC}"
    
    # Check if Node.js is available
    if command -v node &> /dev/null; then
        node scripts/update_readme.js
        EXIT_CODE=$?
        
        if [ $EXIT_CODE -eq 0 ]; then
            echo -e "${GREEN}✅ Successfully generated assets with Node.js script${NC}"
            exit 0
        else
            echo -e "${RED}❌ Node.js script failed with exit code $EXIT_CODE${NC}"
            exit 1
        fi
    else
        echo -e "${RED}❌ Node.js is not installed${NC}"
        exit 1
    fi
fi

################################################################################
# 3. Fallback: Placeholder Mode
################################################################################

echo ""
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}⚠️  No update script found - Running in placeholder mode${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${BLUE}💡 To enable automated asset generation, create one of:${NC}"
echo -e "   • scripts/update_readme.py (Python - recommended)"
echo -e "   • scripts/update_readme.js (Node.js alternative)"
echo ""
echo -e "${BLUE}📝 The script should:${NC}"
echo -e "   1. Fetch GitHub user statistics via API"
echo -e "   2. Generate stats.svg and top-langs.svg in assets/"
echo -e "   3. Update README.md content between DYNAMIC_START and DYNAMIC_END markers"
echo ""
echo -e "${GREEN}✅ Placeholder mode: Exiting gracefully${NC}"
echo ""

################################################################################
# 4. Example Implementation Template (for future reference)
################################################################################

# Uncomment and modify this section when implementing the actual generator:
#
# echo -e "${BLUE}🎨 Generating SVG assets...${NC}"
#
# # Example: Call a Python script to generate SVGs
# python3 << 'EOF'
# import requests
# import os
#
# GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '')
# # ... fetch data from GitHub API
# # ... generate stats.svg
# # ... generate top-langs.svg
# # ... update README.md
# EOF
#
# echo -e "${GREEN}✅ Assets generated successfully${NC}"

################################################################################
# 5. Exit
################################################################################

exit 0
