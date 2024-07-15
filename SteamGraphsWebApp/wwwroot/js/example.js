// Include this script tag in your HTML to load Plotly
 /*<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>*/

function renderHistoricPriceChart() {
    // Example data
    //const jsonData = [
    //    { "Date": "2024-06-27", "PriceUSD": 5.7695 },
    //    { "Date": "2024-06-28", "PriceUSD": 5.6460 },
    //    { "Date": "2024-06-29", "PriceUSD": 5.5630 },
    //    { "Date": "2024-06-30", "PriceUSD": 5.7410 },
    //    { "Date": "2024-07-01", "PriceUSD": 5.8140 }
    //];

    //// Extract the date and price data
    //let dates = jsonData.map(item => item.Date);
    //let prices = jsonData.map(item => item.PriceUSD);

    dates = date;
    prices = price;

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