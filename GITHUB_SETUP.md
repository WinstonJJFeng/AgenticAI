# GitHub Connection Guide

## Quick Setup Steps

### 1. Create a GitHub Repository (if you don't have one)

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the **"+"** icon in the top right → **"New repository"**
3. Name your repository (e.g., `Cursor` or `rilla-project`)
4. Choose **Public** or **Private**
5. **DO NOT** initialize with README, .gitignore, or license (you already have files)
6. Click **"Create repository"**

### 2. Add GitHub Remote

After creating the repository, GitHub will show you commands. Use this format:

```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
```

Or if you prefer SSH (requires SSH key setup):

```bash
git remote add origin git@github.com:YOUR_USERNAME/YOUR_REPO_NAME.git
```

### 3. Authentication Options

#### Option A: Personal Access Token (HTTPS - Recommended for beginners)

1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a name (e.g., "Cursor Project")
4. Select scopes: **repo** (full control of private repositories)
5. Click "Generate token"
6. **Copy the token** (you won't see it again!)
7. When you push, use the token as your password

#### Option B: SSH Key (More secure, no password needed)

1. Check if you have an SSH key:

   ```bash
   ls -al ~/.ssh
   ```

2. If you don't have one, generate it:

   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```

   (Press Enter to accept default file location, optionally set a passphrase)

3. Add SSH key to ssh-agent:

   ```bash
   eval "$(ssh-agent -s)"
   ssh-add ~/.ssh/id_ed25519
   ```

4. Copy your public key:

   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```

5. Add to GitHub:
   - Go to GitHub → Settings → SSH and GPG keys
   - Click "New SSH key"
   - Paste your public key
   - Click "Add SSH key"

### 4. Make Your First Commit

```bash
# Stage all changes
git add .

# Create initial commit
git commit -m "Initial commit: Add project files"

# Push to GitHub
git push -u origin main
```

## Quick Commands Reference

```bash
# Check current remotes
git remote -v

# Add remote (replace with your repo URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Remove remote (if you need to change it)
git remote remove origin

# Push to GitHub
git push -u origin main

# Pull from GitHub
git pull origin main
```

## Troubleshooting

### "Permission denied" error

- Make sure you're using the correct authentication method
- For HTTPS: Use Personal Access Token, not your GitHub password
- For SSH: Make sure your SSH key is added to GitHub

### "Repository not found" error

- Check that the repository name and username are correct
- Verify you have access to the repository

### "Remote origin already exists"

- Remove it first: `git remote remove origin`
- Then add the correct one: `git remote add origin <URL>`

## Next Steps

After connecting:

1. Your code will be backed up on GitHub
2. You can create branches for features
3. You can create Pull Requests (see `.cursor/commands/pr.md`)
4. Collaborate with others
