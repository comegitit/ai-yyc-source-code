// blog_posts.js
const BLOG_POSTS = [
  {
    id: "intro-to-trustworthy-ai",
    url: "posts/intro-to-trustworthy-ai.html", // relative to /blog/
    title: "Building Trustworthy AI in Organizations",
    date: "2026-02-01", // ISO for sorting
    displayDate: "February 2026",
    category: "Governance & Ethics",
    isCoursework: true,
    excerpt:
      'A summarized introduction from "Trustworthy AI: A Business Guide For Navigating Trust & Ethics in AI".',
    minuteRead: 3,
  },
  {
    id: "ada-health-case-study",
    url: "posts/ada-health-case-study.html",
    title: "Case Study: Human-Centred AI: A Medical Chatbot Example",
    date: "2026-01-01",
    displayDate: "January 2026",
    category: "Human Centred AI",
    isCoursework: true,
    excerpt:
      "Coursework analysis of the Ada Health chatbot, examining human-in-the-loop design, accessibility standards, and automation bias in healthcare AI.",
    minuteRead: 2,
  },

  {
    id: "agentic-primer",
    url: "posts/agentic-primer.html",
    title: "Agentic AI: A Primer",
    date: "2026-02-21",
    displayDate: "February 2026",
    category: "Agentic AI",
    isCoursework: false,
    excerpt:
      "Agentic AI is transforming industries through autonomous decision making.",
    minuteRead: 3,
  },

  {
    id: "ai-strategy-post",
    url: "posts/why-your-ai-strategy-is-failing.html",
    title: "Why Your AI Strategy is Failing",
    date: "2026-03-01",
    displayDate: "March 2026",
    category: "AI Strategy",
    isCoursework: false,
    excerpt: "Why your AI Strategy is failing and what to do about it.",
    minuteRead: 4,
  },

  {
    id: "pentagon-vs-anthropic",
    url: "posts/pentagon-vs-anthropic.html",
    title: "Pentagon vs Anthropic",
    date: "2026-02-27",
    displayDate: "February 2026",
    category: "Governance & Ethics",
    isCoursework: false,
    excerpt: "Who decides what guardrails should be implemented & allowed?",
    minuteRead: 4,
  },
  {
    id: "pentagon-vs-anthropic-2",
    url: "posts/pentagon-vs-anthropic-2.html",
    title: "Pentagon vs Anthropic - Update March 2026",
    date: "2026-03-08",
    displayDate: "March 2026",
    category: "Human Centred AI",
    isCoursework: false,
    excerpt: "The dispute through a human centred lens.",
    minuteRead: 4,
  },

  {
    id: "applied-ai-walmart-supply-chain",
    url: "posts/applied-ai-walmart-supply-chain.html",
    title: "From Hype to Hard Results: What Applied AI Looks Like in Practice",
    date: "2026-03-09",
    displayDate: "March 2026",
    category: "Applied AI",
    isCoursework: false,
    excerpt: "Walmart's Supply Chain: A Case Study in Applied AI.",
    minuteRead: 3,
  },

  {
    id: "ethics-of-romantic-ai",
    url: "posts/ethics_of_romantic_ai.html",
    title: "AI Companions and the Ethics of Engineered Connection",
    date: "2026-04-05",
    displayDate: "April 2026",
    category: "Governance & Ethics",
    isCoursework: false,
    excerpt:
      "When does an AI relationship cross from helpful to harmful, and who should be responsible for drawing that line?",
    minuteRead: 6,
  },

  {
    id: "calgary_aidt",
    url: "posts/calgary_aidt.html",
    title: "AI Digital Transformation in 2026: The Calgary Landscape",
    date: "2026-04-13",
    displayDate: "April 2026",
    category: "Digital Transformation",
    isCoursework: false,
    excerpt:
      "An executive summary of the state of AI Digital Transformation in Calgary's business community in 2026",
    minuteRead: 4,
  },

  {
    id: "ai-and-quantum-computing",
    url: "posts/ai-and-quantum-computing.html",
    title: "Quantum Computing and AI: Real Opportunities, Real Constraints",
    date: "2026-04-24",
    displayDate: "April 2026",
    category: "Applied AI",
    isCoursework: false,
    excerpt: "Is Quantum Computing the future of AI?",
    minuteRead: 3,
  },

  {
    id: "agentic-job-match",
    url: "posts/agentic-job-match.html",
    title:
      "An Agentic AI Solution Automating Job Searching & Document Creation",
    date: "2026-05-08",
    displayDate: "May 2026",
    category: "Agentic AI",
    isCoursework: false,
    excerpt:
      "Job matching, scoring, and autonomous document creation using agentic AI.",
    minuteRead: 5,
  },

  {
    id: "AI-legal-and-compliance-landscape-in-calgary",
    url: "posts/AI-legal-and-compliance-landscape-in-calgary.html",
    title: "AI Legal & Compliance in Calgary: Past, Present, and Future",
    date: "2026-05-28",
    displayDate: "May 2026",
    category: "Governance & Ethics",
    isCoursework: false,
    excerpt: "The AI Legal & Compliance Landscape in Calgary in the 2020s.",
    minuteRead: 4,
  },

  {
    id: "canada-ai-for-all-strategy-not-yet-law",
    url: "posts/canada-ai-for-all-strategy-not-yet-law.html",
    title:
      "Canada's AI for All: A Strategy, Not Yet a Law, and Why the Distinction Matters",
    date: "2026-06-06",
    displayDate: "June 2026",
    category: "AI Strategy",
    isCoursework: false,
    excerpt:
      "A federal strategy, not a law. Here is what that means for Calgary organizations.",
    minuteRead: 4,
  },

  {
    id: "claude-design-release",
    url: "posts/claude-design-release.html",
    title: "Claude Design: The Next Revolution",
    date: "2026-06-18",
    displayDate: "June 2026",
    category: "Digital Transformation",
    isCoursework: false,
    excerpt:
      "Claude Design is a paradigm shift for digital transformation, compressing weeks of design and stakeholder alignment into minutes.",
    minuteRead: 3,
  },

  // Add future posts here as new objects, for example:
  // {
  //   id: "my-new-post",
  //   url: "posts/my-new-post.html",
  //   title: "My New Post Title",
  //   date: "2026-03-15",
  //   displayDate: "March 2026",
  //   category: "Some Category",
  //   isCoursework: false,
  //   excerpt: "Short description shown in cards and listings.",
  //   minuteRead: 4,
  // },
];
