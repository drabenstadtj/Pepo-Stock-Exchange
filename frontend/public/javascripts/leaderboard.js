document.addEventListener("DOMContentLoaded", () => {
    const leaderboardBody = document.getElementById('leaderboard-body');
  
    async function fetchLeaderboard() {
      try {
        const response = await fetch('http://localhost:5000/leaderboard');  // Adjusted for relative path
        const textResponse = await response.text();
  
        // Parse the JSON response
        const users = JSON.parse(textResponse);
  
        updateLeaderboard(users);
      } catch (error) {
        console.error('Error fetching leaderboard data:', error);
      }
    }
  
    function updateLeaderboard(users) {
      console.log('Updating leaderboard table...');  // Debug: Log when updating
      leaderboardBody.innerHTML = '';  // Clear existing content
      users.forEach((user, index) => {
        const row = document.createElement('tr');
  
        const rankCell = document.createElement('td');
        rankCell.textContent = index + 1;
        row.appendChild(rankCell);
  
        const nameCell = document.createElement('td');
        nameCell.textContent = user.username;
        row.appendChild(nameCell);
  
        const titleCell = document.createElement('td');
        titleCell.textContent = user.title;
        row.appendChild(titleCell);
  
        const liquidAssetsCell = document.createElement('td');
        liquidAssetsCell.textContent = formatMoney(user.liquidAssets);
        row.appendChild(liquidAssetsCell);
  
        const investedAssetsCell = document.createElement('td');
        investedAssetsCell.textContent = formatMoney(user.investedAssets);
        row.appendChild(investedAssetsCell);
  
        const netWorthCell = document.createElement('td');
        netWorthCell.textContent = formatMoney(user.netWorth);
        row.appendChild(netWorthCell);
  
        leaderboardBody.appendChild(row);
      });
    }
  
    function formatMoney(value) {
      return `$${value.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ",")}`;
    }
  
    // Fetch leaderboard data immediately and then every 10 seconds
    fetchLeaderboard();
    setInterval(fetchLeaderboard, 10000); // Update every 10 seconds
  });
  