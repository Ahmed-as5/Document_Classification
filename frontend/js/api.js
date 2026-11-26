
const API_BASE_URL = "https://api.your-domain.com"; 

const API_CONFIG = Object.freeze({
    BASE_URL: (window.APP_CONFIG && window.APP_CONFIG.API_BASE_URL) || API_BASE_URL,
    ENDPOINTS: Object.freeze({
        CLASSIFY: "/classify",
    }),
    TIMEOUT_MS: 30000, 
});

/**
 * Builds a full URL from the configured base URL and an endpoint path.
 * @param {string} path - Endpoint path, e.g. "/classify".
 * @returns {string}
 */
function buildUrl(path) {
    return `${API_CONFIG.BASE_URL.replace(/\/+$/, "")}${path}`;
}

/**
 * Sends a document's text to the classification API.
 *
 * Resolves with the raw fetch Response so the caller can check `response.ok`
 * and read the body. Rejects with a descriptive Error on timeout or when the
 * server cannot be reached.
 *
 * @param {string} text - The document content.
 * @returns {Promise<Response>}
 */
async function apiClassifyDocument(text) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), API_CONFIG.TIMEOUT_MS);

    try {
        return await fetch(buildUrl(API_CONFIG.ENDPOINTS.CLASSIFY), {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            body: JSON.stringify({ text }),
            signal: controller.signal,
        });
    } catch (error) {
        if (error.name === "AbortError") {
            throw new Error("The request timed out. Please try again.");
        }
        throw new Error("Unable to reach the server. Please check your connection and try again.");
    } finally {
        clearTimeout(timer);
    }
}