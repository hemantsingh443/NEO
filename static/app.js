const form = document.querySelector('form');

form.addEventListener('submit', (event) => {
    event.preventDefault(); // Prevent default form submission

    const formData = new FormData(form);
    const data = {};
    for (const [key, value] of formData.entries()) {
        data[key] = value;
    }

    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        // Display the prediction result (update the HTML)
        const predictionElement = document.getElementById('prediction');
        predictionElement.textContent = `Prediction: ${result.prediction}`;
    })
    .catch(error => {
        console.error('Error:', error);
        // Display an error message to the user
    });
});