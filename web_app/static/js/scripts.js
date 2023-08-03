// static/js/scripts.js
document.addEventListener('DOMContentLoaded', function () {
    const searchForm = document.getElementById('searchForm');
    const loader = document.getElementById('loader');
    const resultsSection = document.getElementById('resultsSection');
    const keywordPlaceholder = document.getElementById('keywordPlaceholder');
    const tweetsList = document.getElementById('tweetsList');

    searchForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const keywordInput = event.target.elements.keyword;
        const keyword = keywordInput.value.trim();

        if (keyword) {
            // Show the loader and hide the results section
            loader.style.display = 'block';
            resultsSection.style.display = 'none';

            // Fetch the sentiment data from the server-side
            fetch('/sentiment_data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ keyword }),
            })
            .then(response => response.json())
            .then(data => {
                // Hide the loader and show the results section
                loader.style.display = 'none';
                resultsSection.style.display = 'block';

                // Update the keyword placeholder
                keywordPlaceholder.textContent = keyword;

                // Create the sentiment chart
                const ctx = document.getElementById('sentimentChart').getContext('2d');
                new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: ['Positive', 'Neutral', 'Negative'],
                        datasets: [{
                            label: 'Sentiment Distribution',
                            data: [data.positive, data.neutral, data.negative],
                            backgroundColor: [
                                'rgba(75, 192, 192, 0.5)',
                                'rgba(255, 206, 86, 0.5)',
                                'rgba(255, 99, 132, 0.5)',
                            ],
                            borderColor: [
                                'rgba(75, 192, 192, 1)',
                                'rgba(255, 206, 86, 1)',
                                'rgba(255, 99, 132, 1)',
                            ],
                            borderWidth: 1
                        }]
                    },
                    options: {
                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        }
                    }
                });

                // Fetch and display the tweets
                fetch('/tweets', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ keyword }),
                })
                .then(response => response.json())
                .then(tweets => {
                    // Clear previous tweets
                    tweetsList.innerHTML = '';

                    // Display the tweets in the list
                    tweets.forEach(tweet => {
                        const listItem = document.createElement('li');
                        listItem.className = 'list-group-item';
                        listItem.textContent = tweet.text;
                        const sentimentBadge = document.createElement('span');
                        sentimentBadge.className = 'badge badge-' + tweet.sentiment.toLowerCase();
                        sentimentBadge.textContent = tweet.sentiment;
                        listItem.appendChild(sentimentBadge);
                        tweetsList.appendChild(listItem);
                    });
                });
            });
        }
    });
});
