// master_nav.js
// Robust global nav that works from any directory depth (local + prod)

// --------------------------------------------
// Base path resolver
// --------------------------------------------
function getBasePath() {
  // The error page is served at whatever depth was requested, so its own
  // links have to be root-absolute rather than relative to that path.
  if (window.SITE_ERROR_PAGE) {
    return "/";
  }

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
  <a href="#main-content" class="skip-link">Skip to main content</a>
  <header class="top-bar">
    <div class="top-bar-inner">
      <a href="${BASE}index.html" class="logo-link">
        <img src="${BASE}images/logo-mark.png" alt="" class="site-logo" />
        <span class="site-wordmark">ai-yyc.com</span>
      </a>

      <nav class="main-nav">
        <ul class="nav-menu">
          <li><a href="${BASE}index.html">Career</a></li>

          <li><a href="${BASE}education.html">Education</a></li>

          <!-- <li><a href="${BASE}capstone.html">Capstone Project</a></li> -->
          <li><a href="${BASE}blog.html">Blog</a></li>
          <li><a href="${BASE}documents/Resume_Roy_Aggarwal_Fall_2026.pdf" target="_blank" rel="noopener noreferrer">Resum&eacute;</a></li>
          
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
    <nav class="footer-nav" aria-label="Footer">
      <ul>
        <li><a href="${BASE}index.html">Career</a></li>
        <li><a href="${BASE}education.html">Education</a></li>
        <li><a href="${BASE}blog.html">Blog</a></li>
        <li><a href="${BASE}documents/Resume_Roy_Aggarwal_Fall_2026.pdf" target="_blank" rel="noopener noreferrer">Resum&eacute;</a></li>
      </ul>
    </nav>

    <div class="footer-bottom">
      <p>Developed by Roy Aggarwal &copy; <span id="year"></span></p>
      <!-- Privacy link is parked until the Clarity tag ships and privacy.html
           goes back into public_html. Uncomment this line to restore it; the
           bottom row re-splits on its own. -->
      <!--<a href="${BASE}privacy.html" class="footer-privacy">Privacy</a>-->
    </div>
  </footer>
`;

// --------------------------------------------
// Inject header & footer on load
// --------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
  const headerContainer = document.getElementById("site-header");
  if (headerContainer) {
    headerContainer.innerHTML = siteHeader;
    highlightActivePage();
  }

  const footerContainer = document.getElementById("site-footer");
  if (footerContainer) {
    footerContainer.innerHTML = siteFooter;
    document.getElementById("year").textContent = new Date().getFullYear();
  }
});

// --------------------------------------------
// Active page highlighting
// --------------------------------------------
function highlightActivePage() {
  // An error page is not any of the nav destinations, so nothing is current.
  if (window.SITE_ERROR_PAGE) {
    return;
  }

  const path = window.location.pathname;
  const currentPage = path.split("/").pop() || "index.html";

  // Category pages and posts live under /blog/, so they belong to Blog.
  const inBlogSection = path.includes("/blog/") || currentPage === "blog.html";

  // The capstone and the four course pages are children of education.html and
  // no longer have nav entries of their own, so they light up Education the
  // same way a post lights up Blog.
  const inEducationSection = [
    "education.html",
    "capstone.html",
    "management.html",
    "ethics.html",
    "hcai.html",
    "predictive.html",
  ].includes(currentPage);

  document.querySelectorAll(".main-nav a").forEach((link) => {
    // Compare basenames; href is prefixed with BASE and would otherwise
    // match on any path ending with the same string.
    const target = (link.getAttribute("href") || "").split("/").pop();
    if (!target) return;
    if (
      target === currentPage ||
      (inBlogSection && target === "blog.html") ||
      (inEducationSection && target === "education.html")
    ) {
      link.classList.add("active");
      // The gold underline is a visual cue only; aria-current exposes the
      // same fact to assistive tech.
      link.setAttribute("aria-current", "page");
    }
  });
}
