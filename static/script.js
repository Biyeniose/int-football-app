function displayPlayers() {
  const players = ["Lionel Messi", "Cristiano Ronaldo", "Kylian Mbappe"];
  const playerList = document.getElementById("player-list");

  players.forEach((player) => {
    const li = document.createElement("li");
    li.textContent = player;
    playerList.appendChild(li);
  });
}
