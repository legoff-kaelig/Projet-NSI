document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("file-input");
  const previewContainer = document.getElementById("preview-container");
  const previewImage = document.getElementById("preview-image");
  const validateBtn = document.getElementById("validate-btn");

  // Gérer la sélection de fichier
  input.addEventListener("change", () => {
    const file = input.files[0];
    const nameImage = file.name;
    if (!file) return;
    
    // Vérifier que le fichier est une image
    if (!file.type.startsWith("image/")) {
      alert("Veuillez sélectionner une image.");
      return;
    }

    const reader = new FileReader();

    // Afficher l'aperçu de l'image
    reader.onload = () => {
      previewImage.src = reader.result;
      previewContainer.classList.remove("hidden");
    };

    reader.readAsDataURL(file);

    fetch(`http://127.0.0.1/update?plant_id=${nameImage}`)
      .then(response => response.json())
      .then(data => {
        const datasStringify = data
        console.log(datasStringify);
      });
  });
});