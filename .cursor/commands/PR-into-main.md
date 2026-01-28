# Create a GitHub pull request from the current branch to the 'main' branch.
# 1. Determine the current git branch.
# 2. Ensure all changes are committed and pushed to the remote branch.
# 3. Use the GitHub CLI (`gh`) to create a PR targeting 'main', 
#    providing a title and body if desired.
# 4. After PR creation, automatically open the PR page in your default web browser.

# Example bash (for command file):
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [[ "$CURRENT_BRANCH" == "main" ]]; then
  echo "⚠️  Cannot create PR from 'main' branch to itself."
  exit 1
fi

echo "✅ Current branch: $CURRENT_BRANCH"

# Ensure all changes are committed
if [[ -n $(git status --porcelain) ]]; then
  echo "❌ There are uncommitted changes. Please commit your changes before creating a PR."
  exit 1
fi

# Ensure branch is pushed to remote
git push -u origin "$CURRENT_BRANCH"

# Create PR with gh CLI
PR_URL=$(gh pr create --base main --head "$CURRENT_BRANCH" --title "Merge $CURRENT_BRANCH into main" --fill --web 2>&1 | grep -E 'https://github.com/.*/pull/[0-9]+')

if [[ -z "$PR_URL" ]]; then
  echo "❌ Failed to create PR or open PR page automatically."
  echo "   Please check for errors above and try again."
  exit 1
fi

echo "🎉 Pull request created successfully for branch '$CURRENT_BRANCH' -> 'main'."

# Try to open the PR page in default browser, if not already opened by gh
if ! [[ "$PR_URL" == *"https://"* ]]; then
    echo "   Open the PR manually in your browser."
else
    echo "🔗 Opening PR page in your default browser: $PR_URL"
    # macOS: open, Linux: xdg-open, Windows: start
    if command -v open >/dev/null 2>&1; then
        open "$PR_URL"
    elif command -v xdg-open >/dev/null 2>&1; then
        xdg-open "$PR_URL"
    elif command -v start >/dev/null 2>&1; then
        start "$PR_URL"
    else
        echo "   Could not detect web browser opener. Please open the URL above manually."
    fi
fi