(function () {
  const blogSidebar = `
    <aside class="blog-sidebar">
      <h3>Categories</h3> 

        <a href="appliedai.html" class="category-nav-link">
          <img src="../images/briefcase.svg" class="sidebar-icon" alt="" />
          Applied AI & Case Studies
        </a>

        <a href="ai-strategy.html" class="category-nav-link">
          <img src="../images/lightbulb.svg" class="sidebar-icon" alt="" />
          AI Strategy
        </a>

        <a href="digital-transformation_blog.html" class="category-nav-link">
          <img src="../images/arrow.svg" class="sidebar-icon" alt="" />
          Digital Transformation
        </a>

        <a href="agentic_blog.html" class="category-nav-link">
          <img src="../images/magic-wand.svg" class="sidebar-icon" alt="" />
          Agentic AI
        </a>

        <a href="human-centred.html" class="category-nav-link">
          <img src="../images/people.svg" class="sidebar-icon" alt="" />
          Human-Centred AI
        </a>

        <a href="ethics_blog.html" class="category-nav-link">
          <img src="../images/scales.svg" class="sidebar-icon" alt="" />
          Governance & Ethics
        </a>

      <nav class="category-nav">
        <a href="../blog.html" class="category-nav-link category-nav-all">
          ← All Categories
        </a>
      </nav>
    </aside>
  `;

  document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("blog-sidebar-container");
    if (!container) return;

    container.innerHTML = blogSidebar;

    // Highlight active category
    const currentPage = window.location.pathname.split("/").pop();

    document.querySelectorAll(".category-nav-link").forEach((link) => {
      const href = link.getAttribute("href");
      if (href === currentPage) {
        link.classList.add("active");
        // The filled pill is a visual cue only; expose it too.
        link.setAttribute("aria-current", "page");
      }
    });
  });
})();

// ----- Shared blog card helpers (Perplexity additions) -----

// Helper so cards work from any page that renders them: index.html, blog.html,
// and the category pages under /blog/.
function getPostUrl(post) {
  const path = post.url; // e.g., "posts/intro-to-trustworthy-ai.html"

  // Under /blog/, "posts/..." already resolves correctly. Anywhere at the site
  // root, including index.html and blog.html, the link needs the blog/ prefix.
  if (window.location.pathname.includes("/blog/")) {
    return path;
  }

  return "blog/" + path; // "blog/posts/intro-to-trustworthy-ai.html"
}

function createBlogPostCard(post, withButton = false) {
  const article = document.createElement("article");
  article.className = "blog-post-card";

  const url = getPostUrl(post);
  const headingTag = withButton ? "h2" : "h3";

  // Only show " · Coursework" when isCoursework is true
  const courseworkLabel = post.isCoursework ? " · Coursework" : "";

  article.innerHTML = `
    <${headingTag}>
      <a href="${url}">
        ${post.title}
      </a>
    </${headingTag}>
    <p class="post-meta">
      ${post.displayDate} · ${post.category}${courseworkLabel}
    </p>
    <p class="post-excerpt">
      ${post.excerpt}
    </p>
  `;

  if (withButton) {
    const button = document.createElement("a");
    button.href = url;
    button.className = "profile-button";
    button.textContent =
      "Read Executive Summary (" + post.minuteRead + " minutes)";
    article.appendChild(document.createElement("br"));
    article.appendChild(button);
  }

  return article;
}

/**
 * Render posts into a container.
 *
 * @param {string} containerId - id of the element to fill
 * @param {Function} filterFn  - function(post) => boolean
 * @param {Object} options
 *   - limit?: number | null
 *   - withButton?: boolean
 *   - archiveContainerId?: string | null
 */
function renderPostsToContainer(containerId, filterFn, options = {}) {
  const container = document.getElementById(containerId);
  if (!container || !Array.isArray(BLOG_POSTS)) return;

  const {
    limit = null,
    withButton = false,
    archiveContainerId = null,
  } = options;

  const posts = BLOG_POSTS.filter(filterFn).sort(
    (a, b) => new Date(b.date) - new Date(a.date),
  );

  const recent = limit ? posts.slice(0, limit) : posts;
  const archived = limit ? posts.slice(limit) : [];

  recent.forEach((post) => {
    container.appendChild(createBlogPostCard(post, withButton));
  });

  if (archiveContainerId && archived.length > 0) {
    const archiveContainer = document.getElementById(archiveContainerId);
    if (!archiveContainer) return;

    archived.forEach((post) => {
      archiveContainer.appendChild(createBlogPostCard(post, false));
    });
  }
}
