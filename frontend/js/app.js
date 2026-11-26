

(() => {
    'use strict';


    const THEME_KEY = 'theme';
    const MAX_FILE_SIZE = 1024 * 1024; 
    const ALLOWED_EXTENSIONS = ['txt', 'json', 'md', 'csv'];

    const MESSAGES = {
        loading:      'Analyzing document…',
        emptyInput:   'Please enter or upload some document text first.',
        requestError: 'Classification failed',
        fileRead:     'Could not read the selected file.',
        fileType:     `Unsupported file type. Allowed: ${ALLOWED_EXTENSIONS.map((e) => '.' + e).join(', ')}`,
        fileSize:     'The file is too large. Maximum size is 1 MB.',
    };


    const $ = (id) => document.getElementById(id);

    const els = {
        classifyBtn:   $('classifyBtn'),
        clearBtn:      $('clearBtn'),
        fileBtn:       $('fileBtn'),
        fileInput:     $('fileInput'),
        textInput:     $('textInput'),
        charCount:     $('charCount'),
        status:        $('status'),
        result:        $('result'),
        label:         $('label'),
        confidence:    $('confidence'),
        confidenceBar: $('confidenceBar'),
        suggestion:    $('suggestion'),
        themeToggle:   $('themeToggle'),
    };

    
    const storage = {
        get(key) {
            try { return localStorage.getItem(key); } catch { return null; }
        },
        set(key, value) {
            try { localStorage.setItem(key, value); } catch { /* storage unavailable */ }
        },
    };

    function applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        els.themeToggle.setAttribute(
            'aria-label',
            theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'
        );
    }

    function initTheme() {
        const saved = storage.get(THEME_KEY);
        const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        applyTheme(saved || (systemPrefersDark ? 'dark' : 'light'));
    }

    function toggleTheme() {
        const next = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
        applyTheme(next);
        storage.set(THEME_KEY, next);
    }

   
    function showLoading() {
        els.status.className = 'status loading';
        els.status.innerHTML = `<div class="spinner"></div><span>${MESSAGES.loading}</span>`;
        els.result.classList.add('hidden');
    }

    function showError(message) {
        els.status.className = 'status error';
        els.status.textContent = message;
        els.result.classList.add('hidden');
    }

    function hideStatus() {
        els.status.classList.add('hidden');
    }

    function setBusy(isBusy) {
        els.classifyBtn.disabled = isBusy;
        els.classifyBtn.setAttribute('aria-busy', String(isBusy));
    }

    function updateCharCount() {
        els.charCount.textContent = els.textInput.value.length.toLocaleString();
    }

    
    function toPercent(value) {
        if (typeof value !== 'number' || Number.isNaN(value)) return null;
        const percent = value <= 1 ? value * 100 : value;
        return Math.min(100, Math.max(0, percent));
    }

    function renderResult(data) {
        const percent = toPercent(data.confidence);

        els.label.textContent      = data.label || '—';
        els.suggestion.textContent = data.suggestion || '—';
        els.confidence.textContent = percent === null ? '—' : `${percent.toFixed(1)}%`;

        const meter = els.confidenceBar.parentElement;
        meter.setAttribute('aria-valuenow', percent === null ? '0' : percent.toFixed(0));

        hideStatus();
        els.result.classList.remove('hidden');

       
        els.confidenceBar.style.width = '0';
        requestAnimationFrame(() => {
            els.confidenceBar.style.width = percent === null ? '0' : `${percent}%`;
        });
    }


    async function readErrorMessage(response) {
        const fallback = `Server responded with status ${response.status}.`;
        try {
            const body = await response.json();
            if (typeof body.detail === 'string') return body.detail;  
            if (typeof body.message === 'string') return body.message;
            if (typeof body.error === 'string') return body.error;
        } catch {
            
        }
        return fallback;
    }

   
    async function classify() {
        const text = els.textInput.value.trim();

        if (!text) {
            showError(MESSAGES.emptyInput);
            els.textInput.focus();
            return;
        }

        showLoading();
        setBusy(true);

        try {
            const response = await apiClassifyDocument(text);

            if (!response.ok) {
                throw new Error(await readErrorMessage(response));
            }

            renderResult(await response.json());
        } catch (error) {
            console.error('[classify]', error);
            showError(`${MESSAGES.requestError}: ${error.message}`);
        } finally {
            setBusy(false);
        }
    }

    function clearAll() {
        els.textInput.value = '';
        els.fileInput.value = '';
        updateCharCount();
        hideStatus();
        els.result.classList.add('hidden');
        els.textInput.focus();
    }

    function handleFileSelected() {
        const file = els.fileInput.files[0];
        if (!file) return;

        const extension = file.name.split('.').pop().toLowerCase();

        if (!ALLOWED_EXTENSIONS.includes(extension)) {
            showError(MESSAGES.fileType);
            els.fileInput.value = '';
            return;
        }
        if (file.size > MAX_FILE_SIZE) {
            showError(MESSAGES.fileSize);
            els.fileInput.value = '';
            return;
        }

        const reader = new FileReader();
        reader.onload = () => {
            els.textInput.value = reader.result;
            updateCharCount();
            hideStatus();
        };
        reader.onerror = () => showError(MESSAGES.fileRead);
        reader.readAsText(file);
    }


    function init() {
        initTheme();
        updateCharCount();

        els.themeToggle.addEventListener('click', toggleTheme);
        els.textInput.addEventListener('input', updateCharCount);
        els.fileBtn.addEventListener('click', () => els.fileInput.click());
        els.fileInput.addEventListener('change', handleFileSelected);
        els.clearBtn.addEventListener('click', clearAll);
        els.classifyBtn.addEventListener('click', classify);

        
        els.textInput.addEventListener('keydown', (event) => {
            if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
                classify();
            }
        });
    }

    document.addEventListener('DOMContentLoaded', init);
})();