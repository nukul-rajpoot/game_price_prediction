<><script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
<div id="historicPriceChart" style="width:100%; height:500px;"></div></>


document.addEventListener('DOMContentLoaded', function () {
    // Get the JSON data from the script tag
    const jsonData = document.getElementById('data-json').textContent;

    // Parse the JSON data
    const data = JSON.parse(jsonData);

    // Extract the date, price, and volume data
    let dates = data.Columns[0].Data;
    let prices = data.Columns[1].Data;

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
});
