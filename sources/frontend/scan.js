document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("file-input");
  const previewContainer = document.getElementById("preview-container");
  const previewImage = document.getElementById("preview-image");

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

    const fs = require('fs');

    fetch('data.json')
      .then(response => response.json())
      .then(data => console.log(data))

    var donnees = JSON.parse(data);

    donnees.nom = nameImage;
    donnees.run = true;

    const jsonString = JSON.stringify(donnees, null, 2);

    fs.writeFileSync('donnees.json', jsonString, 'utf8');

  });
});