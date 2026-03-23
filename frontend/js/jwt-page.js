import { apiPost, setError } from "./api.js";

const form = document.getElementById("jwt-form");

form?.addEventListener("submit", async (event) => {
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

    const result = await apiPost("/api/jwt/sign", {
      header: JSON.parse(document.getElementById("jwt-header").value || "{}"),
      payload: JSON.parse(document.getElementById("jwt-payload").value || "{}"),
      secret: document.getElementById("jwt-secret").value,
      algorithm: document.getElementById("jwt-algorithm").value,
    });
    output.value = result.token;
  } catch (error) {
    setError(error.message);
  }
});
