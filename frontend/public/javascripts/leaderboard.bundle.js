document.addEventListener("DOMContentLoaded",(()=>{const e=window.apiUrl,t=document.getElementById("leaderboard-body");async function n(){try{const o=await fetch(`${e}/leaderboard`,{method:"GET",headers:{"Content-Type":"application/json"},credentials:"include"});if(!o.ok)throw new Error(`HTTP error! Status: ${o.status}`);n=await o.json(),console.log("Updating leaderboard table..."),t.innerHTML="",n.forEach(((e,n)=>{const o=document.createElement("tr"),a=document.createElement("td");a.textContent=n+1,o.appendChild(a);const r=document.createElement("td");r.textContent=e.username,o.appendChild(r);const c=document.createElement("td");c.textContent=e.title,o.appendChild(c);const l=document.createElement("td");l.textContent=d(e.liquidAssets),o.appendChild(l);const s=document.createElement("td");s.textContent=d(e.investedAssets),o.appendChild(s);const i=document.createElement("td");i.textContent=d(e.netWorth),o.appendChild(i),t.appendChild(o)}))}catch(e){console.error("Error fetching leaderboard data:",e)}var n}function d(e){return`$${e.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g,",")}`}n(),setInterval(n,1e4)}));