async function fetchChartData() {
    const response = await fetch('/get-chart-data/');
    const data = await response.json();
    return data;
}

function createChart(labels, values, criticalValue) {
    const ctx = document.getElementById('myChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Data',
                data: values,
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1,
                fill: false
            }]
        },
        options: {
            plugins: {
                legend: {
                    display: false
                },
                annotation: {
                    annotations: {
                        line1: {
                            type: 'line',
                            yMin: criticalValue,
                            yMax: criticalValue,
                            borderColor: 'red',
                            borderWidth: 2,
                            borderDash: [6, 6],
                            label: {
                                display: false,
                            }
                        }
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Time'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Value'
                    }
                }
            }
        }
    });
}

document.addEventListener('DOMContentLoaded', async () => {
    const chartData = await fetchChartData();
    createChart(chartData.labels, chartData.values, chartData.critical_value);
});

document.getElementById('measure-select').addEventListener('change', async () => {
    const chartData = await fetchChartData();
    createChart(chartData.labels, chartData.values, chartData.critical_value);
});


function addHostClickHandlers() {
    const hostElements = document.querySelectorAll('.host');
    hostElements.forEach(host => {
        host.addEventListener('click', async (event) => {
            const ip = host.querySelector('.ip').textContent;
            await getIp(ip);
        });
    });
}

document.getElementById('measure-select').addEventListener('change', async (event) => {
    const activeMeasure = event.target.value;

    const response = await fetch('/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCsrfToken()
        },
        body: new URLSearchParams({
            'active_measure': activeMeasure
        })
    });

    if (response.ok) {
        const chartData = await response.json();
        createChart(chartData.labels, chartData.values, chartData.critical_value);
});