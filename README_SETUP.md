# DenxVil Profile README - Logo Setup Instructions

## Logo Setup

### Step 1: Prepare Your Logo
- Create or obtain your custom logo image
- Recommended specifications:
  - Format: PNG (supports transparency)
  - Size: 150x150 pixels (or larger, will be resized)
  - Shape: Works best with square aspect ratio
  - Background: Transparent or solid color

### Step 2: Upload Logo
1. Upload your logo to the `/img/` directory
2. Name the file exactly: `Denvil.png`
3. The file path should be: `/img/Denvil.png`

### Step 3: Activate Custom Logo
1. Edit the `README.md` file
2. Find line 2-3 in the header section:
   ```html
   <img src="https://github.com/DenxVil.png" alt="DenxVil Avatar" width="150" height="150" style="border-radius: 50%;">
   <!-- Replace with custom logo: <img src="./img/Denvil.png" alt="DenxVil Logo" width="150" height="150" style="border-radius: 50%;"> -->
   ```
3. Comment out the GitHub avatar line and uncomment the custom logo line:
   ```html
   <!-- GitHub avatar fallback: <img src="https://github.com/DenxVil.png" alt="DenxVil Avatar" width="150" height="150" style="border-radius: 50%;"> -->
   <img src="./img/Denvil.png" alt="DenxVil Logo" width="150" height="150" style="border-radius: 50%;">
   ```

### Current Features

✅ **Professional Header** with animated typing effect  
✅ **About Section** with JavaScript-style personal info  
✅ **Comprehensive Tech Stack** with categorized badges  
✅ **Featured Projects** with detailed descriptions:
- Shan-D Superadvanced AI (Ultra-Human AI Assistant)
- NexusAi (Advanced Telegram Bot Platform)
- Shan (Modular AI Chatbot)
- Synapse (Interactive Web Application)
- DenxVil.github.io (Personal Portfolio)

✅ **GitHub Analytics** with multiple chart types  
✅ **Contact & Social Links**  
✅ **Visual Elements** and animations  

### File Structure
```
DenxVil/
├── README.md          # Main profile README
├── img/               # Logo directory
│   ├── .gitkeep      # Keeps directory in git
│   └── Denvil.png    # Your custom logo (to be uploaded)
└── README_SETUP.md   # This instructions file
```

### Notes
- The current README uses your GitHub avatar as a fallback
- All project information was extracted from your actual repositories
- Technologies and skills listed are based on your real projects
- Contact information includes your actual Telegram bot and email
- The README is optimized for both desktop and mobile viewing