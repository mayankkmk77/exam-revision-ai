const uploadButton = document.getElementById("uploadButton");
const pdfFile = document.getElementById("pdfFile");
const result = document.getElementById("result");


uploadButton.addEventListener("click", async function () {

    if (pdfFile.files.length === 0) {
        result.textContent = "Please select a PDF first.";
        return;
    }

    const file = pdfFile.files[0];

    result.textContent = "Uploading and extracting text...";

    const formData = new FormData();

    formData.append("file", file);


    try {

        const response = await fetch("http://127.0.0.1:8000/upload", {
            method: "POST",
            body: formData
        });

        const data = await response.json();


        if (!data.text) {

            result.textContent =
                `${data.filename}\n\n${data.message}`;

            return;
        }


        result.textContent =
            `File: ${data.filename}\n\n` +
            `${data.message}\n\n` +
            `------------------------------\n\n` +
            data.text;


    } catch (error) {

        result.textContent =
            "Error connecting to the backend.";

        console.error(error);
    }

});