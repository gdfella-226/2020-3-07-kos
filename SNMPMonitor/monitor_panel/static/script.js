let myChart;

async function fetchChartData() {
    const response = await fetch('/get_chart_data/');
    const data = await response.json();
    return data;
}

function createChart(labels, values, criticalValue) {
    const ctx = document.getElementById('myChart').getContext('2d');

    if (myChart) {
        myChart.destroy();
    }

    myChart = new Chart(ctx, {
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

document.getElementById('chart-select').addEventListener('change', async (event) => {
    const activeMeasure = event.target.value;
    const response = await fetch('/set_active_measure/', {
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
        const chartData = await fetchChartData();
        createChart(chartData.labels, chartData.values, chartData.critical_value);
    } else {
        console.error('Get drop-list data error');
    }
})

document.addEventListener('DOMContentLoaded', async () => {
    const chartData = await fetchChartData();
    createChart(chartData.labels, chartData.values, chartData.critical_value);
});


function addHostClickHandlers() {
    const hostElements = document.querySelectorAll('.host');
    hostElements.forEach(host => {
        host.addEventListener('click', async (event) => {
            console.log('Click');
            const ip = host.querySelector('.ip').textContent;
            await getIp(ip);
        });
    });
}

async function getIp(ip) {
    const response = await fetch('/set_active_host/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCsrfToken()
        },
        body: new URLSearchParams({
            'ip': ip
        })
    });
    if (response.ok) {
        console.log(`IP ${ip} сохранен на сервере.`);
    } else {
        console.error('Get IP data error');
    }
}

function getCsrfToken() {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, 10) === 'csrftoken=') {
                cookieValue = decodeURIComponent(cookie.substring(10));
                break;
            }
        }
    }
    return cookieValue;
}