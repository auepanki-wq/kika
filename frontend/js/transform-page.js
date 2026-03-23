import { apiPost, setError } from "./api.js";

const form = document.querySelector(".transform-form");

form?.addEventListener("submit", async (event) => {
  event.preventDefault();
  setError();

  const codec = form.dataset.codec;
  const direction = form.querySelector("select[name='direction']")?.value ?? "encode";
  const input = form.querySelector("textarea[name='input']").value;
  const output = form.querySelector("textarea[name='output']");
  const shift = Number(form.querySelector("input[name='shift']")?.value ?? 3);
  const normalizationForm = form.querySelector("select[name='normalization_form']")?.value ?? "NFC";

  try {
    const result = await apiPost("/api/transform", {
      codec,
      direction,
      value: input,
      shift,
      normalization_form: normalizationForm,
    });

    output.value = result.output;
  } catch (error) {
    setError(error.message);
  }
});
