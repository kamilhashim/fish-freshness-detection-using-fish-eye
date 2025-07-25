// Wait for the DOM to load
document.addEventListener("DOMContentLoaded", () => {
    const fileInput = document.getElementById("fileInput");
    const fileLabel = document.querySelector("label.custom-file-label");

    // Update file label and show a preview when a file is selected
    fileInput.addEventListener("change", (event) => {
        const file = event.target.files[0];
        const previewContainer = document.getElementById("previewContainer");
        const previewImage = document.getElementById("previewImage");

        if (file) {
            // Update the label
            fileLabel.textContent = `Selected: ${file.name}`;

            // Display a preview of the selected image
            const reader = new FileReader();
            reader.onload = (e) => {
                previewImage.src = e.target.result;
                previewImage.style.display = "block";
            };
            reader.readAsDataURL(file);
        } else {
            fileLabel.textContent = "Choose an image";
            previewImage.style.display = "none";
        }
    });
});
