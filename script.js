function checkServer() {
  const messageEl = document.getElementById("server-message");

  // Immediate feedback
  if (messageEl) {
    messageEl.innerText = "Connecting to server…";
  }

  // Wait 1.5 seconds before attempting the connection
  setTimeout(() => {
    fetch("https://royaggarwal.pythonanywhere.com/hello")
      .then((response) => response.text())
      .then((message) => {
        if (messageEl) {
          messageEl.innerText = message;
        }
      })
      .catch((error) => {
        if (messageEl) {
          messageEl.innerText = "Error contacting server.";
        }
        console.error("Server connection error:", error);
      });
  }, 1500);
}

// Run on normal page load
document.addEventListener("DOMContentLoaded", checkServer);

// Run when navigating back/forward (browser cache restore)
window.addEventListener("pageshow", (event) => {
  if (event.persisted) {
    checkServer();
  }
});
