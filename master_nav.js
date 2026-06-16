// master_nav.js
// Robust global nav that works from any directory depth (local + prod)

// --------------------------------------------
// Base path resolver
// --------------------------------------------
function getBasePath() {
  const path = window.location.pathname;

  // If we're inside /blog/posts/, go up two levels
  if (path.includes("/blog/posts/")) {
    return "../../";
  }

  // If we're inside /blog/, go up one level
  if (path.includes("/blog/")) {
    return "../";
  }

  // Otherwise we're at site root
  return "";
}

const BASE = getBasePath();

// --------------------------------------------
// Header HTML
// --------------------------------------------
const siteHeader = `
  <header class="top-bar">
    <div class="top-bar-inner">
      <a href="${BASE}index.html" class="logo-link">
        <img src="${BASE}images/logo.png" alt="ai-yyc.com logo" class="site-logo" />
      </a>

      <nav class="main-nav">
        <ul class="nav-menu">
          <li><a href="${BASE}index.html">Career</a></li>

          <li class="has-submenu">
            <button
              class="submenu-toggle"
              type="button"
              aria-expanded="false"
            >
              Coursework
            </button>
            <ul class="submenu">
              <li><a href="${BASE}management.html">AI Management</a></li>
              <li><a href="${BASE}ethics.html">Governance & Ethics</a></li>
              <li><a href="${BASE}hcai.html">Human Centred AI</a></li>
              <li><a href="${BASE}predictive.html">Predictive Analytics</a></li>
              <!--<li><a href="${BASE}statistics.html">Statistics</a></li>-->
              <!--<li><a href="${BASE}webdev.html">Web Dev</a></li>-->
            </ul>
          </li>

          <!-- <li><a href="${BASE}capstone.html">Capstone Project</a></li> -->
          <li><a href="${BASE}blog.html">Blog</a></li>
          <li><a href="${BASE}documents/Resume_Roy_Aggarwal_Summer_2026.pdf" target="_blank" rel="noopener noreferrer">Resum&eacute;</a></li>
          
        </ul>
      </nav>
    </div>
  </header>
`;

// --------------------------------------------
// Footer HTML
// --------------------------------------------
const siteFooter = `
  <footer>
    <p>Developed by Roy Aggarwal &copy; <span id="year"></span></p>
  </footer>
`;

// --------------------------------------------
// Inject header & footer on load
// --------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
  const headerContainer = document.getElementById("site-header");
  if (headerContainer) {
    headerContainer.innerHTML = siteHeader;
    initSubmenuToggle();
    highlightActivePage();
  }

  const footerContainer = document.getElementById("site-footer");
  if (footerContainer) {
    footerContainer.innerHTML = siteFooter;
    document.getElementById("year").textContent = new Date().getFullYear();
  }
});

// --------------------------------------------
// Submenu toggle logic
// --------------------------------------------
function initSubmenuToggle() {
  const toggles = document.querySelectorAll(".submenu-toggle");

  toggles.forEach((toggle) => {
    toggle.addEventListener("click", (e) => {
      e.stopPropagation();

      const parent = toggle.closest(".has-submenu");
      const isOpen = parent.classList.contains("open");

      document.querySelectorAll(".has-submenu.open").forEach((item) => {
        if (item !== parent) {
          item.classList.remove("open");
          item
            .querySelector(".submenu-toggle")
            ?.setAttribute("aria-expanded", "false");
        }
      });

      parent.classList.toggle("open", !isOpen);
      toggle.setAttribute("aria-expanded", String(!isOpen));
    });
  });

  document.addEventListener("click", () => {
    document.querySelectorAll(".has-submenu.open").forEach((item) => {
      item.classList.remove("open");
      item
        .querySelector(".submenu-toggle")
        ?.setAttribute("aria-expanded", "false");
    });
  });
}

// --------------------------------------------
// Active page highlighting
// --------------------------------------------
function highlightActivePage() {
  const currentPage = window.location.pathname.split("/").pop() || "index.html";

  document.querySelectorAll(".main-nav a").forEach((link) => {
    const href = link.getAttribute("href");
    if (href && href.endsWith(currentPage)) {
      link.classList.add("active");
    }
  });
}
