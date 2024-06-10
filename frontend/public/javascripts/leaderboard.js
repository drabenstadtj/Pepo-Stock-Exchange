document.addEventListener("DOMContentLoaded", () => {
  const leaderboardBody = document.getElementById('leaderboard-body');

  async function fetchLeaderboard() {
    try {
      // Fetch the leaderboard data from the server
      const response = await fetch(`http://192.168.68.250:${backendPort}/leaderboard`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include'
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const users = await response.json();

      // Update the leaderboard table with the fetched data
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

      // Create and append the rank cell
      const rankCell = document.createElement('td');
      rankCell.textContent = index + 1;
      row.appendChild(rankCell);

      // Create and append the username cell
      const nameCell = document.createElement('td');
      nameCell.textContent = user.username;
      row.appendChild(nameCell);

      // Create and append the title cell
      const titleCell = document.createElement('td');
      titleCell.textContent = user.title;
      row.appendChild(titleCell);

      // Create and append the liquid assets cell
      const liquidAssetsCell = document.createElement('td');
      liquidAssetsCell.textContent = formatMoney(user.liquidAssets);
      row.appendChild(liquidAssetsCell);

      // Create and append the invested assets cell
      const investedAssetsCell = document.createElement('td');
      investedAssetsCell.textContent = formatMoney(user.investedAssets);
      row.appendChild(investedAssetsCell);

      // Create and append the net worth cell
      const netWorthCell = document.createElement('td');
      netWorthCell.textContent = formatMoney(user.netWorth);
      row.appendChild(netWorthCell);

      // Append the row to the leaderboard table body
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
