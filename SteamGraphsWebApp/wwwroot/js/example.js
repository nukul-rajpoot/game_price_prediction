function renderHistoricPriceChart() {
    // Create the plot
    var trace = {
        type: "scatter",
        mode: "lines+markers",
        name: 'Price USD',
        x: dates,
        y: prices,
        line: { color: '#17BECF' }
    };

    var data = [trace];

    var layout = {
        title: 'Historic Price over Time',
        xaxis: {
            title: 'Date',
            type: 'date',
            rangeslider: { visible: true }
        },
        yaxis: {
            title: 'Price USD',
            titlefont: { size: 16 },
            tickfont: { size: 14 }
        },
        showlegend: true
    };

    Plotly.newPlot('historicPriceChart', data, layout);
}

// Add an event listener to call the function when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', renderHistoricPriceChart);