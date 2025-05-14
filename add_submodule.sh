#!/bin/bash

if [ "$#" -ne 3 ]; then
    echo "Usage: ./add_submodule.sh <repo_url> <target_path> "<commit_message>""
    exit 1
fi

REPO_URL=$1
TARGET_PATH=$2
COMMIT_MSG=$3

REPO_DIR=~/Documents/PromptContinuity_Repo
cd "$REPO_DIR" || { echo "❌ Repo not found at $REPO_DIR"; exit 1; }

echo "🔗 Adding submodule from: $REPO_URL to $TARGET_PATH"
git submodule add "$REPO_URL" "$TARGET_PATH"

echo "📦 Staging submodule and config"
git add .gitmodules "$TARGET_PATH"

echo "📝 Committing: $COMMIT_MSG"
git commit -m "$COMMIT_MSG"

echo "🚀 Pushing to GitHub..."
git push origin main

echo "✅ Submodule added and pushed."
