// ===== Generic helpers =====

function setStatus(text, isError = false) {
    const el = document.getElementById("status-line");
    if (!el) return;
    el.textContent = text;
    el.classList.toggle("error", isError);
}

async function submitForm(formId, endpoint) {
    const form = document.getElementById(formId);
    const formData = new FormData(form);
    const submitBtn = form.querySelector("button[type=submit]");

    submitBtn.disabled = true;
    setStatus("Processing...");

    try {
        const res = await fetch(endpoint, { method: "POST", body: formData });

        if (!res.ok) {
            let message = "Something went wrong.";
            try {
                const errJson = await res.json();
                message = errJson.detail || message;
            } catch (_) {}
            setStatus(message, true);
            submitBtn.disabled = false;
            return null;
        }

        setStatus("Done.");
        submitBtn.disabled = false;
        return res;

    } catch (err) {
        setStatus("Network error. Please try again.", true);
        submitBtn.disabled = false;
        return null;
    }
}

// ===== For tools that return a downloadable image (QR gen, compress, convert, watermark) =====

function initImageResultForm({ formId, endpoint, downloadName, dynamicExtensionFieldId = null }) {
    const form = document.getElementById(formId);
    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const res = await submitForm(formId, endpoint);
        if (!res) return;

        const blob = await res.blob();
        const url = URL.createObjectURL(blob);

        document.getElementById("result-empty").style.display = "none";

        const img = document.getElementById("result-image");
        img.src = url;
        img.style.display = "block";

        let finalName = downloadName;
        if (dynamicExtensionFieldId) {
            const ext = document.getElementById(dynamicExtensionFieldId).value;
            finalName = `converted.${ext === "jpeg" ? "jpg" : ext}`;
        }

        const link = document.getElementById("download-link");
        link.href = url;
        link.download = finalName;
        link.style.display = "inline-block";
    });
}

// ===== For tools that return a downloadable file directly (PDF/ZIP outputs) =====

function initFileResultForm({ formId, endpoint, downloadName }) {
    const form = document.getElementById(formId);
    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const res = await submitForm(formId, endpoint);
        if (!res) return;

        const blob = await res.blob();
        const url = URL.createObjectURL(blob);

        document.getElementById("result-empty").style.display = "none";

        const link = document.getElementById("download-link");
        link.href = url;
        link.download = downloadName;
        link.style.display = "inline-block";

        // Auto-trigger the download so the user doesn't have to click twice
        link.click();
    });
}

// ===== QR Scanner - special case, shows decoded text list instead of an image =====

function initQrScanForm() {
    const form = document.getElementById("qr-scan-form");
    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const res = await submitForm("qr-scan-form", "/api/qr/scan");
        if (!res) return;

        const data = await res.json();
        document.getElementById("result-empty").style.display = "none";

        const resultsDiv = document.getElementById("scan-results");
        resultsDiv.style.display = "block";
        resultsDiv.innerHTML = "";

        if (!data.found) {
            resultsDiv.innerHTML = `<p class="no-data-text">No QR code detected in this image.</p>`;
            return;
        }

        data.results.forEach((text, i) => {
            const isUrl = /^https?:\/\//i.test(text);
            const item = document.createElement("div");
            item.className = "scan-result-item";
            item.innerHTML = isUrl
                ? `<span class="scan-result-label">Result ${i + 1}</span><a href="${text}" target="_blank" rel="noopener">${text}</a>`
                : `<span class="scan-result-label">Result ${i + 1}</span><p>${text}</p>`;
            resultsDiv.appendChild(item);
        });
    });
}
