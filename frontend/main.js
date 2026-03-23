const errorBox = document.getElementById("error");

const getBaseUrl = () => document.getElementById("base-url").value.replace(/\/$/, "");

async function apiPost(path, payload) {
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

function setError(message = "") {
  errorBox.textContent = message;
}

document.getElementById("transform-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  setError();

  try {
    const payload = {
      codec: document.getElementById("codec").value,
      direction: document.getElementById("direction").value,
      value: document.getElementById("transform-input").value,
      shift: Number(document.getElementById("shift").value),
      normalization_form: document.getElementById("normalization-form").value,
    };

    const result = await apiPost("/api/transform", payload);
    document.getElementById("transform-output").value = result.output;
  } catch (error) {
    setError(error.message);
  }
});

document.getElementById("jwt-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  setError();

  const action = document.getElementById("jwt-action").value;
  const output = document.getElementById("jwt-output");

  try {
    if (action === "decode") {
      const result = await apiPost("/api/jwt/decode", {
        token: document.getElementById("jwt-token").value,
      });
      output.value = JSON.stringify(result, null, 2);
      return;
    }

    if (action === "verify") {
      const result = await apiPost("/api/jwt/verify", {
        token: document.getElementById("jwt-token").value,
        secret: document.getElementById("jwt-secret").value,
      });
      output.value = JSON.stringify(result, null, 2);
      return;
    }

    const header = JSON.parse(document.getElementById("jwt-header").value || "{}");
    const payload = JSON.parse(document.getElementById("jwt-payload").value || "{}");
    const result = await apiPost("/api/jwt/sign", {
      header,
      payload,
      secret: document.getElementById("jwt-secret").value,
      algorithm: document.getElementById("jwt-algorithm").value,
    });
    output.value = result.token;
  } catch (error) {
    setError(error.message);
  }
});

document.getElementById("flask-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  setError();

  const action = document.getElementById("flask-action").value;
  const output = document.getElementById("flask-output");
  const secret = document.getElementById("flask-secret").value;
  const salt = document.getElementById("flask-salt").value;

  try {
    if (action === "decode") {
      const result = await apiPost("/api/flask-unsign/decode", {
        cookie: document.getElementById("flask-cookie").value,
      });
      output.value = JSON.stringify(result, null, 2);
      return;
    }

    if (action === "verify") {
      const result = await apiPost("/api/flask-unsign/verify", {
        cookie: document.getElementById("flask-cookie").value,
        secret,
        salt,
      });
      output.value = JSON.stringify(result, null, 2);
      return;
    }

    const payload = JSON.parse(document.getElementById("flask-payload").value || "{}");
    const result = await apiPost("/api/flask-unsign/sign", { payload, secret, salt });
    output.value = result.cookie;
  } catch (error) {
    setError(error.message);
  }
});
