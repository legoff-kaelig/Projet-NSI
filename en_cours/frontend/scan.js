const dropZone = document.getElementById("drop-zone");
const fileInput = document.getElementById("file-input");
const previewContainer = document.getElementById("preview-container");
const previewImage = document.getElementById("preview-image");

dropZone.addEventListener("click", () => fileInput.click());

dropZone.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropZone.classList.add("dragover");
});

dropZone.addEventListener("dragleave", () => {
  dropZone.classList.remove("dragover");
});

dropZone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropZone.classList.remove("dragover");
  handleFile(e.dataTransfer.files[0]);
});

fileInput.addEventListener("change", () => {
  handleFile(fileInput.files[0]);
});

function handleFile(file) {
  if (!file || !file.type.startsWith("image/")) return;

  const reader = new FileReader();
  reader.onload = () => {
    previewImage.src = reader.result;
    previewContainer.classList.remove("hidden");
  };
  reader.readAsDataURL(file);
}