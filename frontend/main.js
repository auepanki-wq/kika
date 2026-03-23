const form = document.getElementById("transform-form");
const output = document.getElementById("output");
const errorBox = document.getElementById("error");

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  errorBox.textContent = "";
  output.value = "";

  const body = {
    codec: document.getElementById("codec").value,
    direction: document.getElementById("direction").value,
    value: document.getElementById("input").value,
    shift: Number(document.getElementById("shift").value),
    normalization_form: document.getElementById("normalization-form").value,
  };

  const baseUrl = document.getElementById("base-url").value.replace(/\/$/, "");

  try {
    const response = await fetch(`${baseUrl}/api/transform`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || "Unexpected API error");
    }

    output.value = payload.output;
  } catch (error) {
    errorBox.textContent = error.message;
  }
});
