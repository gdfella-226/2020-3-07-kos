let myChart;

async function fetchChartData() {
    const response = await fetch('/get-chart-data/');
    const data = await response.json();
    return data;
}


function createChart(labels, values, criticalValue) {
    const ctx = $('#myChart').getContext('2d');

    if (myChart) {
        myChart.destroy();
    }

    myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Workload',
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


$('#chart-select').addEventListener('change', async (event) => {
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
    }
})


document.addEventListener('DOMContentLoaded', async () => {

});


function addHostClickHandlers() {
    const hostElements = $('.host');
    hostElements.forEach(host => {
        host.addEventListener('click', async (event) => {
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
}


$(document).ready(async function() {
    const chartData = await fetchChartData();
    createChart(chartData.labels, chartData.values, chartData.critical_value);

    $(document).click(function() {
        $('.context-menu').css('visibility', 'hidden'); // Hide context menus when clicking outside
    });
});


function showContextMenu(event, ip) {
    event.stopPropagation(); // Prevent triggering the host click event
    $('.context-menu').css('visibility', 'hidden'); // Hide all other context menus
    $('#context-menu-' + ip).css('visibility', 'visible'); // Show the current context menu
}

function restartHost(ip) {
    alert('Restarting host: ' + ip);
    // Implement your logic here
}

function disableNetworkAdapter(ip) {
    alert('Disabling network adapter for host: ' + ip);
    // Implement your logic here
}

function disableUsbPort(ip) {
    alert('Disabling USB port for host: ' + ip);
    // Implement your logic here
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