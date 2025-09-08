#!/bin/bash
#
# Setup Git hooks for the repository

# Create hooks directory if it doesn't exist
mkdir -p .git/hooks

# Copy pre-commit hook
cp .github/hooks/pre-commit .git/hooks/
chmod +x .git/hooks/pre-commit

echo "Git hooks installed successfully!"
