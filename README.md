# Typing Level Analyzer

A browser-based typing speed and accuracy analyzer. The app runs fully in the browser, so it works on GitHub Pages over HTTPS without needing a Python server.

## Run Locally

Open `index.html` in a browser.

You can also run the optional Python static server:

```powershell
python typingTest.py
```

Then open `http://127.0.0.1:8000/`.

## Publish With GitHub Pages

1. Create a new GitHub repository.
2. Upload or push these files:
   - `index.html`
   - `styles.css`
   - `typingTest.py`
   - `.gitignore`
   - `README.md`
3. In the GitHub repository, open **Settings > Pages**.
4. Under **Build and deployment**, select **Deploy from a branch**.
5. Select the `main` branch and `/ (root)` folder, then save.

GitHub Pages will publish the site at an HTTPS URL like:

```text
https://your-username.github.io/your-repository-name/
```

## Important

GitHub Pages cannot run Python backend code. That is why the public version calculates the typing result directly in the browser.
