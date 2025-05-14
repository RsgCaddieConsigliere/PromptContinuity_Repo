#!/bin/bash

# Usage: ./push_update.sh "Your commit message here"

REPO_PATH=~/Documents/PromptContinuity_Repo

echo "📂 Navigating to repo: $REPO_PATH"
cd "$REPO_PATH" || { echo "❌ Repo not found. Exiting."; exit 1; }

echo "🔄 Pulling remote changes with rebase..."
git pull --rebase origin main

echo "📦 Staging all changes..."
git add .

echo "📝 Committing with message: $1"
git commit -m "$1"

echo "🚀 Pushing to GitHub..."
git push origin main

echo "✅ Done!"
