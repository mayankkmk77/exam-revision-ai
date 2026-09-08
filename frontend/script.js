const uploadButton = document.getElementById("uploadButton");
const pdfFile = document.getElementById("pdfFile");
const result = document.getElementById("result");

uploadButton.addEventListener("click", function () {

    if (pdfFile.files.length === 0) {
        result.textContent = "Please select a PDF first.";
        return;
    }

    const file = pdfFile.files[0];

    result.textContent = `Selected file: ${file.name}`;

});