# Finish and Publish Checklist

The file list is in the [README](../README.md#source-code-files). There is no build step or `node_modules`.

## 1. Keep private data out of GitHub
Never upload API keys, `.env` files, `thunai_data.json`, `__pycache__/` folders or PyInstaller output.

Create a `.gitignore` file containing:

```
.env
thunai_data.json
__pycache__/
build/
dist/
*.spec
```

Check that `index.html` and the Python files contain no real Gemini key.

## 2. Test
1. Run the app as described in the README.
2. Go through [TESTING.md](TESTING.md) and tick only what you checked.
3. Update the status in [FEATURES.md](FEATURES.md) to match.

## 3. Finish the README
Add the live link if you have one, then make sure every claim matches the app.

## 4. Publish
1. Use one shared public repository. Add teammates as collaborators instead of creating copies.
2. Open the repository in a private/incognito window and check that the README, images and links all work.
