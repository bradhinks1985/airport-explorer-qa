// Javascript scripts shared by all app pages

// sliding amazon style menu
document.addEventListener("DOMContentLoaded", function() {
  const menuButton = document.getElementById("menuButton");
  const closeMenuButton = document.getElementById("closeMenuButton");
  const navLinks = document.getElementById("navLinks");
  const menuOverlay = document.getElementById("menuOverlay");

    // Function to open the slide-out menu drawer
  function openMenu() {
    navLinks.classList.add("show");
    menuOverlay.classList.add("show");
    document.body.style.overflow = "hidden"; /* Disables scrolling the background page */
  }

    // Function to close the slide-out menu drawer
  function closeMenu() {
    navLinks.classList.remove("show");
    menuOverlay.classList.remove("show");
    document.body.style.overflow = ""; /* Restores background page scroll behavior */
  }

    // Event Listeners for click/touch actions
  if (menuButton) menuButton.addEventListener("click", openMenu);
  if (closeMenuButton) closeMenuButton.addEventListener("click", closeMenu);
  if (menuOverlay) menuOverlay.addEventListener("click", closeMenu);
});



//  Mobile Navbar Script 
const button = document.getElementById("menuButton");
const links = document.getElementById("navLinks");

button.addEventListener("click", () => {

    links.classList.toggle("show");

});



//  PWA 
if ("serviceWorker" in navigator) {

    navigator.serviceWorker.register(
        "/static/service-worker.js"
    )
    .then(() => {
        console.log("Service worker registered");
    });

}



// page back button for mobile
function safeBack() {
  // If length is 1, the user likely opened this page directly
  if (window.history.length <= 1) {
    window.location.href = '/'; // Change to your PWA home route
  } else {
    window.history.back();
  }
}

