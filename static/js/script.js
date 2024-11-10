document.addEventListener('DOMContentLoaded', () => {
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('imageUpload');
    const analyzeButton = document.getElementById('btn-analyze');
    const resultSpan = document.getElementById('result');
    const medicineParagraph = document.getElementById('medicine');
    const causeParagraph = document.getElementById('cause');
    const loader = document.getElementById('loader');
    const resultContainer = document.getElementById('result-container');

    dropzone.addEventListener('click', () => fileInput.click());
    dropzone.addEventListener('dragover', (event) => {
        event.preventDefault();
        dropzone.style.backgroundColor = '#e9ecef';
    });
    dropzone.addEventListener('dragleave', () => {
        dropzone.style.backgroundColor = '#f8f9fa';
    });
    dropzone.addEventListener('drop', (event) => {
        event.preventDefault();
        dropzone.style.backgroundColor = '#f8f9fa';
        fileInput.files = event.dataTransfer.files;
    });

    analyzeButton.addEventListener('click', async () => {
        analyzeButton.classList.add('clicked');
        loader.style.display = 'block';
        resultContainer.style.display = 'none';

        const formData = new FormData(document.getElementById('upload-file'));

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();

            if (data.error) {
                resultSpan.textContent = `Error: ${data.error}`;
                medicineParagraph.textContent = '';
                causeParagraph.textContent = '';
            } else {
                resultSpan.textContent = data.result;
                medicineParagraph.textContent = data.medicine || 'Not available';
                causeParagraph.textContent = data.cause || 'Not available';
            }
        } catch (error) {
            resultSpan.textContent = `Error: ${error.message}`;
            medicineParagraph.textContent = '';
            causeParagraph.textContent = '';
        } finally {
            loader.style.display = 'none';
            resultContainer.style.display = 'block';
        }
    });
});
