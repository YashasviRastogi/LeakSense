// LeakSense Charts and Gauges

// Chart.js configuration
Chart.defaults.color = '#94a3b8';
Chart.defaults.borderColor = '#334155';
Chart.defaults.font.family = 'Inter, sans-serif';

// Gauge charts
let pressureGauge, moistureGauge, acousticGauge;
let mainChart;

// Initialize gauge charts
function initializeGauges() {
    // Pressure Gauge
    const pressureCtx = document.getElementById('pressureGauge').getContext('2d');
    pressureGauge = new Chart(pressureCtx, {
        type: 'doughnut',
        data: {
            datasets: [{
                data: [0, 100],
                backgroundColor: [
                    'rgba(59, 130, 246, 0.8)',
                    'rgba(51, 65, 85, 0.3)'
                ],
                borderWidth: 0,
                circumference: 180,
                rotation: 270
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '75%',
            plugins: {
                legend: { display: false },
                tooltip: { enabled: false }
            }
        }
    });

    // Moisture Gauge
    const moistureCtx = document.getElementById('moistureGauge').getContext('2d');
    moistureGauge = new Chart(moistureCtx, {
        type: 'doughnut',
        data: {
            datasets: [{
                data: [0, 100],
                backgroundColor: [
                    'rgba(6, 182, 212, 0.8)',
                    'rgba(51, 65, 85, 0.3)'
                ],
                borderWidth: 0,
                circumference: 180,
                rotation: 270
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '75%',
            plugins: {
                legend: { display: false },
                tooltip: { enabled: false }
            }
        }
    });

    // Acoustic Gauge
    const acousticCtx = document.getElementById('acousticGauge').getContext('2d');
    acousticGauge = new Chart(acousticCtx, {
        type: 'doughnut',
        data: {
            datasets: [{
                data: [0, 70],
                backgroundColor: [
                    'rgba(139, 92, 246, 0.8)',
                    'rgba(51, 65, 85, 0.3)'
                ],
                borderWidth: 0,
                circumference: 180,
                rotation: 270
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '75%',
            plugins: {
                legend: { display: false },
                tooltip: { enabled: false }
            }
        }
    });
}

// Update gauge chart
function updateGauge(gaugeId, value, min, max) {
    let gauge;
    let color;
    
    switch(gaugeId) {
        case 'pressureGauge':
            gauge = pressureGauge;
            color = 'rgba(59, 130, 246, 0.8)';
            break;
        case 'moistureGauge':
            gauge = moistureGauge;
            color = 'rgba(6, 182, 212, 0.8)';
            // Change color based on threshold
            if (value > 70) color = 'rgba(239, 68, 68, 0.8)';
            else if (value > 60) color = 'rgba(245, 158, 11, 0.8)';
            break;
        case 'acousticGauge':
            gauge = acousticGauge;
            color = 'rgba(139, 92, 246, 0.8)';
            // Change color based on threshold
            if (value > 75) color = 'rgba(239, 68, 68, 0.8)';
            else if (value > 70) color = 'rgba(245, 158, 11, 0.8)';
            break;
    }
    
    const range = max - min;
    const normalizedValue = ((value - min) / range) * 100;
    const remaining = 100 - normalizedValue;
    
    gauge.data.datasets[0].data = [normalizedValue, remaining];
    gauge.data.datasets[0].backgroundColor[0] = color;
    gauge.update('none'); // Update without animation for smoother updates
}

// Initialize main chart
function initializeChart() {
    const ctx = document.getElementById('mainChart').getContext('2d');
    
    mainChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Pressure (PSI)',
                    data: [],
                    borderColor: 'rgba(59, 130, 246, 1)',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 0,
                    pointHoverRadius: 6,
                    yAxisID: 'y'
                },
                {
                    label: 'Moisture (%)',
                    data: [],
                    borderColor: 'rgba(6, 182, 212, 1)',
                    backgroundColor: 'rgba(6, 182, 212, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 0,
                    pointHoverRadius: 6,
                    yAxisID: 'y1'
                },
                {
                    label: 'Acoustic (dB)',
                    data: [],
                    borderColor: 'rgba(139, 92, 246, 1)',
                    backgroundColor: 'rgba(139, 92, 246, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 0,
                    pointHoverRadius: 6,
                    yAxisID: 'y2'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 20,
                        font: {
                            size: 12,
                            weight: '500'
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(30, 41, 59, 0.95)',
                    padding: 12,
                    titleFont: {
                        size: 14,
                        weight: '600'
                    },
                    bodyFont: {
                        size: 13
                    },
                    borderColor: 'rgba(59, 130, 246, 0.5)',
                    borderWidth: 1,
                    displayColors: true,
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) {
                                label += ': ';
                            }
                            label += context.parsed.y.toFixed(2);
                            return label;
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        maxTicksLimit: 10,
                        font: {
                            size: 11
                        }
                    }
                },
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: {
                        display: true,
                        text: 'Pressure (PSI)',
                        font: {
                            size: 12,
                            weight: '600'
                        }
                    },
                    grid: {
                        color: 'rgba(51, 65, 85, 0.5)'
                    },
                    ticks: {
                        font: {
                            size: 11
                        }
                    }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    title: {
                        display: true,
                        text: 'Moisture (%)',
                        font: {
                            size: 12,
                            weight: '600'
                        }
                    },
                    grid: {
                        drawOnChartArea: false
                    },
                    ticks: {
                        font: {
                            size: 11
                        }
                    }
                },
                y2: {
                    type: 'linear',
                    display: false,
                    position: 'right',
                    grid: {
                        drawOnChartArea: false
                    }
                }
            },
            animation: {
                duration: 750,
                easing: 'easeInOutQuart'
            }
        }
    });
}

// Update main chart with new data
function updateMainChart(data) {
    if (!mainChart) return;
    
    // Limit data points for performance
    const maxDataPoints = 100;
    
    if (data.labels.length > maxDataPoints) {
        const step = Math.ceil(data.labels.length / maxDataPoints);
        data.labels = data.labels.filter((_, i) => i % step === 0);
        data.pressure = data.pressure.filter((_, i) => i % step === 0);
        data.moisture = data.moisture.filter((_, i) => i % step === 0);
        data.acoustic = data.acoustic.filter((_, i) => i % step === 0);
    }
    
    mainChart.data.labels = data.labels;
    mainChart.data.datasets[0].data = data.pressure;
    mainChart.data.datasets[1].data = data.moisture;
    mainChart.data.datasets[2].data = data.acoustic;
    
    mainChart.update('active');
}

// Add animation to chart updates
function animateChartUpdate(chart) {
    chart.update({
        duration: 800,
        easing: 'easeInOutQuart'
    });
}

// Destroy charts on cleanup
function destroyCharts() {
    if (pressureGauge) pressureGauge.destroy();
    if (moistureGauge) moistureGauge.destroy();
    if (acousticGauge) acousticGauge.destroy();
    if (mainChart) mainChart.destroy();
}

// Export functions
window.initializeGauges = initializeGauges;
window.updateGauge = updateGauge;
window.initializeChart = initializeChart;
window.updateMainChart = updateMainChart;
window.destroyCharts = destroyCharts;
