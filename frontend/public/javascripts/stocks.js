document.addEventListener("DOMContentLoaded", () => {
  const apiUrl = window.apiUrl;  // Use the global apiUrl variable
  
  const stocksBody = document.getElementById('stocks-body');

  async function fetchStocks() {
    try {
      const response = await fetch(`${apiUrl}/stocks/`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include'
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const stocks = await response.json();
      updateStocks(stocks);
    } catch (error) {
      console.error('Error fetching stocks data:', error);
    }
  }

  function updateStocks(stocks) {
    console.log('Updating stocks table...');  // Debug: Log when updating
    stocksBody.innerHTML = '';  // Clear existing content
    stocks.forEach(stock => {
      const row = document.createElement('tr');

      const symbolCell = document.createElement('td');
      symbolCell.classList.add('stock-popup');
      const symbolSpan = document.createElement('span');
      symbolSpan.textContent = stock.symbol;
      const popupDiv = document.createElement('div');
      popupDiv.classList.add('popuptext');
      popupDiv.innerHTML = `
        <h3>${stock.symbol}</h3>
        <p>Name: ${stock.name}</p>
        <p>Sector: ${stock.sector}</p>
        <p>Low: $${stock.low.toFixed(2)}</p>
        <p>High: $${stock.high.toFixed(2)}</p>
      `;
      symbolCell.appendChild(symbolSpan);
      symbolCell.appendChild(popupDiv);
      row.appendChild(symbolCell);

      const priceCell = document.createElement('td');
      priceCell.textContent = "$" + stock.price.toFixed(2);
      row.appendChild(priceCell);

      const changeCell = document.createElement('td');
      changeCell.textContent = stock.change.toFixed(2);
      changeCell.classList.add(stock.change >= 0 ? 'positive-change' : 'negative-change');
      row.appendChild(changeCell);

      stocksBody.appendChild(row);
    });
  }

  fetchStocks();
  setInterval(fetchStocks, 10000); // Update every 10 seconds
});
