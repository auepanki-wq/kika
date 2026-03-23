export function getBaseUrl() {
  const input = document.getElementById("base-url");
  const base = input ? input.value.trim() : "";
  return base ? base.replace(/\/$/, "") : "";
}

export async function apiPost(path, payload) {
  const response = await fetch(`${getBaseUrl()}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  const body = await response.json();
  if (!response.ok) {
    throw new Error(body.detail || "Unexpected API error");
  }

  return body;
}

export function setError(message = "") {
  const box = document.getElementById("error");
  if (box) box.textContent = message;
}
