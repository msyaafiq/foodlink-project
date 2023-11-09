// After initializing Firebase and other chart setup...

// Get the canvas element and render the chart
const ctx = document.getElementById('myBarChart').getContext('2d');
const config = {
  type: 'bar',
  data: {
    labels: labels,
    datasets: [{
      label: 'Food Inventory',
      data: [food_value, water_value], // Use the fetched values
      backgroundColor: [
        'rgba(255, 99, 132, 0.2)',
        'rgba(255, 205, 86, 0.2)',
      ],
      borderColor: [
        'rgb(255, 99, 132)',
        'rgb(255, 205, 86)',
      ],
      borderWidth: 1,
    }],
  },
  options: {
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  },
};

new Chart(ctx, config);
