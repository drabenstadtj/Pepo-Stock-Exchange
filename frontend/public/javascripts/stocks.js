document.addEventListener("DOMContentLoaded", () => {
    const stocksBody = document.getElementById('stocks-body');
  
    async function fetchStocks() {
      try {
        // Fetch the stock data from the server
        const response = await fetch(`https://db.copland.lol/stocks/`, {
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
  
        // Update the stocks table with the fetched data
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
  
        // Create and append the symbol cell with popup
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
          <p>Low: ${stock.low.toFixed(2)}</p>
          <p>High: ${stock.high.toFixed(2)}</p>
        `;
        symbolCell.appendChild(symbolSpan);
        symbolCell.appendChild(popupDiv);
        row.appendChild(symbolCell);
  
        // Create and append the price cell
        const priceCell = document.createElement('td');
        priceCell.textContent = stock.price.toFixed(2);
        row.appendChild(priceCell);
  
        // Create and append the change cell
        const changeCell = document.createElement('td');
        changeCell.textContent = stock.change.toFixed(2);
        changeCell.classList.add(stock.change >= 0 ? 'positive-change' : 'negative-change');
        row.appendChild(changeCell);
  
        // Append the row to the stocks table body
        stocksBody.appendChild(row);
      });
    }
  
    // Fetch stocks data immediately and then every 10 seconds
    fetchStocks();
    setInterval(fetchStocks, 10000); // Update every 10 seconds
  });
  