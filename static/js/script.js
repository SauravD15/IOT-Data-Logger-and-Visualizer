// Global variables
let temperatureChart, humidityChart;
let updateInterval;

// Chart.js configuration
const chartConfig = {
    type: 'line',
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                labels: {
                    color: '#ffffff',
                    font: {
                        size: 12
                    }
                }
            }
        },
        scales: {
            x: {
                ticks: {
                    color: '#ffffff',
                    maxRotation: 45,
                    minRotation: 45
                },
                grid: {
                    color: 'rgba(255, 255, 255, 0.1)'
                }
            },
            y: {
                ticks: {
                    color: '#ffffff'
                },
                grid: {
                    color: 'rgba(255, 255, 255, 0.1)'
                }
            }
        },
        animation: {
            duration: 750,
            easing: 'easeInOutQuart'
        }
    }
};

// Initialize charts
function initializeCharts() {
    const tempCtx = document.getElementById('temperatureChart').getContext('2d');
    const humCtx = document.getElementById('humidityChart').getContext('2d');

    temperatureChart = new Chart(tempCtx, {
        ...chartConfig,
        data: {
            labels: [],
            datasets: [{
                label: 'Temperature (°C)',
                data: [],
                borderColor: '#ff6b6b',
                backgroundColor: 'rgba(255, 107, 107, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: '#ff6b6b',
                pointBorderColor: '#ffffff',
                pointBorderWidth: 2,
                pointRadius: 5,
                pointHoverRadius: 7
            }]
        }
    });

    humidityChart = new Chart(humCtx, {
        ...chartConfig,
        data: {
            labels: [],
            datasets: [{
                label: 'Humidity (%)',
                data: [],
                borderColor: '#4ecdc4',
                backgroundColor: 'rgba(78, 205, 196, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: '#4ecdc4',
                pointBorderColor: '#ffffff',
                pointBorderWidth: 2,
                pointRadius: 5,
                pointHoverRadius: 7
            }]
        }
    });
}

// Fetch data from API
async function fetchData() {
    try {
        const response = await fetch('/data');
        const result = await response.json();
        
        if (result.success) {
            updateCharts(result.data);
            updateTable(result.data);
            updateStatus(result.data.length);
        } else {
            console.error('Error fetching data:', result.error);
            showMessage('Error fetching data: ' + result.error, 'error');
        }
    } catch (error) {
        console.error('Network error:', error);
        showMessage('Network error while fetching data', 'error');
    }
}

// Update charts with new data
function updateCharts(data) {
    if (!data || data.length === 0) return;

    const labels = data.map(item => {
        const date = new Date(item.timestamp);
        return date.toLocaleTimeString();
    });

    const temperatures = data.map(item => item.temperature);
    const humidities = data.map(item => item.humidity);

    // Update temperature chart
    temperatureChart.data.labels = labels;
    temperatureChart.data.datasets[0].data = temperatures;
    temperatureChart.update('active');

    // Update humidity chart
    humidityChart.data.labels = labels;
    humidityChart.data.datasets[0].data = humidities;
    humidityChart.update('active');
}

// Update data table
function updateTable(data) {
    const tableBody = document.getElementById('dataTableBody');
    tableBody.innerHTML = '';

    if (!data || data.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="4" style="text-align: center;">No data available</td></tr>';
        return;
    }

    data.forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${item.id}</td>
            <td>${item.timestamp}</td>
            <td>${item.temperature}°C</td>
            <td>${item.humidity}%</td>
        `;
        tableBody.appendChild(row);
    });
}

// Update status information
function updateStatus(count) {
    const lastUpdate = document.getElementById('lastUpdate');
    const dataCount = document.getElementById('dataCount');
    
    lastUpdate.textContent = `Last update: ${new Date().toLocaleTimeString()}`;
    dataCount.textContent = `Data points: ${count}`;
}

// Simulate new data
async function simulateData() {
    const simulateBtn = document.getElementById('simulateBtn');
    const originalText = simulateBtn.textContent;
    
    try {
        simulateBtn.textContent = '🔄 Simulating...';
        simulateBtn.disabled = true;
        
        const response = await fetch('/simulate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const result = await response.json();
        
        if (result.success) {
            showMessage('New data simulated successfully!', 'success');
            // Fetch updated data immediately
            await fetchData();
        } else {
            showMessage('Error simulating data: ' + result.error, 'error');
        }
    } catch (error) {
        console.error('Error simulating data:', error);
        showMessage('Network error while simulating data', 'error');
    } finally {
        simulateBtn.textContent = originalText;
        simulateBtn.disabled = false;
    }
}

// Clear all data
async function clearData() {
    if (!confirm('Are you sure you want to clear all data? This action cannot be undone.')) {
        return;
    }
    
    const clearBtn = document.getElementById('clearBtn');
    const originalText = clearBtn.textContent;
    
    try {
        clearBtn.textContent = '🔄 Clearing...';
        clearBtn.disabled = true;
        
        const response = await fetch('/clear');
        const result = await response.json();
        
        if (result.success) {
            showMessage('All data cleared successfully!', 'success');
            // Clear charts and table
            updateCharts([]);
            updateTable([]);
            updateStatus(0);
        } else {
            showMessage('Error clearing data: ' + result.error, 'error');
        }
    } catch (error) {
        console.error('Error clearing data:', error);
        showMessage('Network error while clearing data', 'error');
    } finally {
        clearBtn.textContent = originalText;
        clearBtn.disabled = false;
    }
}

// Show message to user
function showMessage(message, type = 'success') {
    // Remove existing messages
    const existingMessages = document.querySelectorAll('.message');
    existingMessages.forEach(msg => msg.remove());
    
    // Create new message
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = message;
    
    // Insert at the top of the container
    const container = document.querySelector('.container');
    container.insertBefore(messageDiv, container.firstChild);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (messageDiv.parentNode) {
            messageDiv.remove();
        }
    }, 5000);
}

// Start automatic updates
function startAutoUpdate() {
    // Fetch data immediately
    fetchData();
    
    // Set up interval for every 5 seconds
    updateInterval = setInterval(fetchData, 5000);
}

// Stop automatic updates
function stopAutoUpdate() {
    if (updateInterval) {
        clearInterval(updateInterval);
        updateInterval = null;
    }
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Initialize charts
    initializeCharts();
    
    // Set up event listeners
    document.getElementById('simulateBtn').addEventListener('click', simulateData);
    document.getElementById('clearBtn').addEventListener('click', clearData);
    
    // Start automatic updates
    startAutoUpdate();
    
    // Handle page visibility changes
    document.addEventListener('visibilitychange', function() {
        if (document.hidden) {
            stopAutoUpdate();
        } else {
            startAutoUpdate();
        }
    });
    
    // Handle window focus/blur
    window.addEventListener('focus', startAutoUpdate);
    window.addEventListener('blur', stopAutoUpdate);
});

// Handle page unload
window.addEventListener('beforeunload', function() {
    stopAutoUpdate();
}); 