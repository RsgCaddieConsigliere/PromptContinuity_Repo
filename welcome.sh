#!/bin/bash

REPO_PATH=~/Documents/PromptContinuity_Repo
cd "$REPO_PATH" || { echo "❌ Repo not found at $REPO_PATH"; exit 1; }

echo "📍 Current directory: $(pwd)"
echo "📁 Repo contents:"
ls -alh | grep -v '^total'

echo ""
echo "🔁 Git status:"
git status

echo ""
echo "📦 Submodules:"
git submodule

echo ""
echo "🧠 Helpful next steps:"
echo "1. ./add_submodule.sh <repo_url> <target_path> "<commit_message>""
echo "2. ./push_update.sh "<commit_message>""
