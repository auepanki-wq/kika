import { apiPost, setError } from "./api.js";

const form = document.getElementById("flask-form");

form?.addEventListener("submit", async (event) => {
  event.preventDefault();
  setError();

  const action = document.getElementById("flask-action").value;
  const output = document.getElementById("flask-output");
  const cookie = document.getElementById("flask-cookie").value;
  const secret = document.getElementById("flask-secret").value;
  const salt = document.getElementById("flask-salt").value;

  try {
    if (action === "decode") {
      const result = await apiPost("/api/flask-unsign/decode", { cookie });
      output.value = JSON.stringify(result, null, 2);
      return;
    }

    if (action === "verify") {
      const result = await apiPost("/api/flask-unsign/verify", { cookie, secret, salt });
      output.value = JSON.stringify(result, null, 2);
      return;
    }

    const result = await apiPost("/api/flask-unsign/sign", {
      payload: JSON.parse(document.getElementById("flask-payload").value || "{}"),
      secret,
      salt,
    });
    output.value = result.cookie;
  } catch (error) {
    setError(error.message);
  }
});
