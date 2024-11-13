// static/script.js

function submitForm() {
    const content = document.getElementById("content").value;
    const type = document.getElementById("type").value;

    fetch("/analyze_content", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ content, type })
    })
    .then(response => response.json())
    .then(data => {
        const resultsDiv = document.getElementById("results");
        resultsDiv.innerHTML = "";  // Clear previous results

        if (data.error) {
            resultsDiv.innerHTML = `<p style="color: red;">Error: ${data.error}</p>`;
        } else {
            const scores = data.confidence_scores;

            resultsDiv.innerHTML += `<p><strong>Content:</strong> ${data.content}</p>`;
            resultsDiv.innerHTML += `<p><strong>Content Type:</strong> ${data.type}</p>`;
            resultsDiv.innerHTML += `<p><strong>Confidence Scores:</strong></p>`;

            const scoreList = document.createElement("ul");
            for (const [category, score] of Object.entries(scores)) {
                const listItem = document.createElement("li");
                listItem.innerText = `${category}: ${(score * 100).toFixed(2)}%`;
                scoreList.appendChild(listItem);
            }
            resultsDiv.appendChild(scoreList);
        }
    })
    .catch(error => {
        const resultsDiv = document.getElementById("results");
        resultsDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
    });
}
