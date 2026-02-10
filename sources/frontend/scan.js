// Ce script permet de sélectionner ou déposer une image
// puis de l'afficher en aperçu avant validation

document.addEventListener("DOMContentLoaded", () => {

  // Zone de dépôt
  const dropZone = document.getElementById("drop-zone");

  // Bouton personnalisé pour ouvrir l'explorateur de fichiers
  const fileButton = document.getElementById("file-input");

  // Conteneur de prévisualisation
  const previewContainer = document.getElementById("preview-container");
  const previewImage = document.getElementById("preview-image");

  // Bouton de validation (pour plus tard)
  const validateBtn = document.getElementById("validate-btn");

  // Input file caché (créé en JS pour garder ton HTML propre)
  const fileInput = document.createElement("input");
  fileInput.type = "file";
  fileInput.accept = "image/*";
  fileInput.style.display = "none";
  document.body.appendChild(fileInput);

  /* -----------------------------
     OUVERTURE DE L'EXPLORATEUR
  ------------------------------ */
  fileButton.addEventListener("click", () => {
    fileInput.click();
  });

  /* -----------------------------
     IMAGE CHOISIE VIA FICHIERS
  ------------------------------ */
  fileInput.addEventListener("change", () => {
    const file = fileInput.files[0];
    if (file) {
      showPreview(file);
    }
  });

  /* -----------------------------
     DRAG & DROP
  ------------------------------ */
  dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("drag-over");
  });

  dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("drag-over");
  });

  dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.classList.remove("drag-over");

    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith("image/")) {
      showPreview(file);
    }
  });

  /* -----------------------------
     AFFICHAGE DE L'IMAGE
  ------------------------------ */
  function showPreview(file) {
    const reader = new FileReader();

    reader.onload = () => {
      previewImage.src = reader.result;
      previewContainer.classList.remove("hidden");
    };

    reader.readAsDataURL(file);
  }

  /* -----------------------------
     BOUTON VALIDER (placeholder)
  ------------------------------ */
  validateBtn.addEventListener("click", () => {
    alert("Image prête à être analysée (fonction à venir)");
  });

});