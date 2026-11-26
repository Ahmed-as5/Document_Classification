# DocClassifier – Frontend

## How to Run

### 1. Requirements

- A modern browser (Chrome, Edge, Firefox or Safari)
- Python 3 (only to serve the files), or VS Code with the Live Server extension
- The backend API must be running and reachable

### 2. Project structure

Make sure the files are arranged like this:

```
frontend/
├── index.html
├── css/
│   └── style.css
├── js/
│   ├── config.js
│   ├── api.js
│   └── app.js
└── README.md
```

### 3. Set the backend address

Set the backend URL in `js/config.js`. The default points to the local API at
`http://127.0.0.1:8000`.

```javascript
window.APP_CONFIG = Object.freeze({ API_BASE_URL: "https://api.your-domain.com" });
```

### 4. Start the frontend

**Option A: Python**

```bash
cd frontend
python -m http.server 5500
```

Then open the address shown in the terminal in your browser.

**Option B: VS Code**

1. Install the **Live Server** extension.
2. Right-click `index.html`.
3. Choose **Open with Live Server**.

### 5. Use the app

1. Paste your text in the box, or click **Upload file** (`.txt`, `.json`, `.md`, `.csv`).
2. Click **Classify document** (or press `Ctrl + Enter`).
3. The predicted category, confidence and suggested department will appear below.

### Troubleshooting

| Problem | Fix |
|---------|-----|
| "Unable to reach the server" | Make sure the backend is running and `API_BASE_URL` in `js/config.js` is correct. |
| CORS error in the browser console | Allow the frontend's origin in the backend's CORS settings. |
| Page looks unstyled or buttons do nothing | Check that the folder structure matches the one above. |