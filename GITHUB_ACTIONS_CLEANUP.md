# GitHub Actions Cleanup Instructions

## Files to Delete

Delete these workflow files from the `.github/workflows` directory:

1. `preserve-readme-sections.yml`
2. `enhanced-api-discovery.yml`
3. `update-all-on-push.yml`
4. `update-apis.yml`
5. `update-trending-api-repos.yml`
6. `update-trending-repos.yml`

## Keep Only This File

Keep only this workflow file:
- `update-api-data.yml`

## How to Delete These Files

### Option 1: Using GitHub Web Interface
1. Go to your GitHub repository
2. Navigate to `.github/workflows`
3. Open each file you want to delete
4. Click the trash icon in the top-right corner
5. Commit the deletion with a message like "Remove unnecessary workflow files"

### Option 2: Using Git Command Line
```bash
# Clone the repository if you haven't already
git clone https://github.com/yourusername/awesome-public-free-apis.git
cd awesome-public-free-apis

# Delete the files
git rm .github/workflows/preserve-readme-sections.yml
git rm .github/workflows/enhanced-api-discovery.yml
git rm .github/workflows/update-all-on-push.yml
git rm .github/workflows/update-apis.yml
git rm .github/workflows/update-trending-api-repos.yml
git rm .github/workflows/update-trending-repos.yml

# Commit and push the changes
git commit -m "Remove unnecessary workflow files"
git push
```

### Option 3: Using GitHub Desktop
1. Open GitHub Desktop
2. Navigate to the repository
3. Go to the `.github/workflows` directory
4. Right-click on each file you want to delete and select "Delete"
5. Commit the changes with a message like "Remove unnecessary workflow files"
6. Push the changes to GitHub

After deleting these files, the GitHub Actions errors should be resolved, and your README.md file should stop resetting.
