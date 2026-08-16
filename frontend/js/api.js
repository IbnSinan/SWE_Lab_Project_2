/*
 * js/api.js
 * --------------------------------------------------------
 * Module owner : 2203137
 * Feature branch: feature/frontend-module
 * --------------------------------------------------------
 * Tiny fetch() wrapper shared by every page. All requests are
 * same-origin (the Flask app in /backend serves this frontend
 * directly), so the session cookie set by the auth API is sent
 * automatically - no manual token handling needed for this MVP.
 */

async function apiRequest(method, path, body) {
    const options = {
        method,
        headers: { "Content-Type": "application/json" },
    };
    if (body !== undefined) {
        options.body = JSON.stringify(body);
    }

    const response = await fetch(path, options);
    let data = null;
    try {
        data = await response.json();
    } catch (err) {
        data = null;
    }

    if (!response.ok) {
        const message = (data && data.error) ? data.error : `Request failed (${response.status})`;
        throw new Error(message);
    }
    return data;
}

const api = {
    get: (path) => apiRequest("GET", path),
    post: (path, body) => apiRequest("POST", path, body),
    put: (path, body) => apiRequest("PUT", path, body),
    patch: (path, body) => apiRequest("PATCH", path, body),
    del: (path) => apiRequest("DELETE", path),
};
