# 🚀 Quick Start Guide

Get Notion Template Maker running in under 5 minutes!

## Step 1: Prerequisites Check

```bash
# Check Python version (need 3.11+)
python --version

# Check Node.js version (need 18+)
node --version

# If missing, install from:
# Python: https://www.python.org/downloads/
# Node.js: https://nodejs.org/
```

## Step 2: Clone & Install

```bash
# Clone the repository
git clone https://github.com/yourusername/notion-template-maker.git
cd notion-template-maker

# One command to install everything
make install
```

This installs:
- ✅ Python backend dependencies (FastAPI, etc.)
- ✅ Node.js frontend dependencies (React, etc.)

## Step 3: Get API Keys

### OpenRouter API Key (Required)

1. Go to https://openrouter.ai/
2. Click **"Sign Up"** or **"Log In"**
3. Navigate to **"API Keys"** (https://openrouter.ai/keys)
4. Click **"Create API Key"**
5. Copy the key (starts with `sk-or-...`)

### Notion Internal Integration (Required for Import)

1. Go to https://www.notion.so/my-integrations
2. Click **"+ New integration"**
3. Fill in:
   - **Name**: `Template Maker`
   - **Logo**: (optional)
   - **Associated workspace**: Select your workspace
4. Set **Capabilities**:
   - ✅ **Read content**
   - ✅ **Insert content**
   - ✅ **Update content**
   - ⬜ Update comments (optional)
   - ⬜ No user information
5. Click **"Submit"**
6. Copy the **"Internal Integration Secret"** (starts with `secret_...`)

## Step 4: Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Open in your favorite editor
nano .env
# or
code .env
```

Paste your keys:

```env
# Required: OpenRouter API Key
OPENROUTER_API_KEY=sk-or-v1-YOUR_KEY_HERE

# Required: Notion Integration Secret
NOTION_INTEGRATION_SECRET=secret_YOUR_SECRET_HERE

# Optional: Leave defaults for development
APP_ENV=development
DEBUG=true
LOG_LEVEL=INFO
```

**Save the file!**

## Step 5: Share Notion Pages with Integration

**Important**: Your integration can only access pages you explicitly share with it.

1. Open Notion and navigate to a page/database
2. Click the **"..."** menu (top right)
3. Scroll down to **"Add connections"**
4. Search for your integration name (`Template Maker`)
5. Click to connect

Do this for any page where you want to import templates.

## Step 6: Run the Application

```bash
# Start both backend and frontend
make dev
```

You should see:

```
🚀 Starting Notion Template Maker...
Backend: http://localhost:8000
Frontend: http://localhost:5173
API Docs: http://localhost:8000/api/docs
```

## Step 7: Open in Browser

Open your browser to: **http://localhost:5173**

You should see the Template Maker homepage!

## Step 8: First Template Generation

1. **Configure API Keys**
   - Click the ⚙️ **settings icon** (top right)
   - Paste your **OpenRouter API key**
   - Paste your **Notion Integration Secret** (optional)
   - Click **"Save Configuration"**

2. **Generate a Template**
   - Select template type: **"Project Management"**
   - Title: **"My First Project"**
   - Description: **"A project management system with tasks and milestones"**
   - Complexity: **Simple**
   - Click **"Generate Template"**

3. **Wait ~30 seconds** for AI generation

4. **Review the Template**
   - Browse the **Overview**, **Pages**, and **Databases** tabs
   - Check the generated structure

5. **Import to Notion** (optional)
   - Click **"Import to Notion"**
   - Template will be created in your workspace!

## 🎉 Success!

You're now running Notion Template Maker!

## Common Issues & Solutions

### Issue: `make: command not found`

**Solution**: Install make or use manual commands:

```bash
# Instead of `make install`
pip install -r requirements-backend.txt
cd frontend && npm install

# Instead of `make dev`
# Terminal 1:
cd backend && python main.py

# Terminal 2:
cd frontend && npm run dev
```

### Issue: `Python version too old`

**Solution**: Install Python 3.11+:

```bash
# macOS
brew install python@3.11

# Ubuntu/Debian
sudo apt-get install python3.11

# Windows
# Download from https://www.python.org/downloads/
```

### Issue: `node: command not found`

**Solution**: Install Node.js:

```bash
# macOS
brew install node

# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Windows
# Download from https://nodejs.org/
```

### Issue: Backend won't start

**Check**:
1. Is port 8000 already in use?
   ```bash
   lsof -i :8000  # macOS/Linux
   netstat -ano | findstr :8000  # Windows
   ```
2. Are environment variables set correctly?
   ```bash
   cat .env  # Check file exists and has correct values
   ```
3. Check logs:
   ```bash
   tail -f logs/app.log
   ```

### Issue: Frontend can't connect to backend

**Check**:
1. Is backend running? Visit http://localhost:8000/health
2. Check CORS settings in `.env`:
   ```env
   ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
   ```
3. Check browser console for errors (F12 → Console tab)

### Issue: "Invalid API key" error

**Check**:
1. Did you copy the complete key? (OpenRouter keys start with `sk-or-v1-`)
2. Did you paste it correctly in the Settings modal?
3. Is the key still valid? Check https://openrouter.ai/keys

### Issue: Notion import fails

**Check**:
1. Did you share the target page with your integration?
2. Is the Integration Secret correct? (starts with `secret_`)
3. Does the integration have correct permissions?
   - ✅ Insert content
   - ✅ Update content

### Issue: Template generation is slow

**Normal**: AI generation typically takes 20-60 seconds

**If longer**:
1. Check your OpenRouter account limits
2. Check network connection
3. Try a simpler template (lower complexity)

## Next Steps

- 📖 Read the full [README.md](README.md)
- 🤝 Check [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
- 🐳 Try [Docker deployment](DEPLOYMENT.md)
- 🧪 Run tests with `make test`
- 🎨 Customize templates in `src/services/template_generator.py`

## Need Help?

- 🐛 [Report an issue](https://github.com/yourusername/notion-template-maker/issues)
- 💬 [Ask in discussions](https://github.com/yourusername/notion-template-maker/discussions)
- 📧 Email: support@notiontemplate.com

---

**Happy Template Making! 🎨✨**
