// Docs page behaviour: copy buttons, tabs, the product switcher, and the
// table-of-contents highlight. Everything degrades to plain HTML without it.
(function () {
  // Copy buttons on code blocks.
  document.querySelectorAll("[data-code-copy]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const code = btn.closest(".code-block")?.querySelector("pre code");
      if (!code) return;
      try {
        await navigator.clipboard.writeText(code.innerText.replace(/\n$/, ""));
        btn.textContent = "Copied";
      } catch {
        btn.textContent = "Copy failed";
      }
      setTimeout(() => (btn.textContent = "Copy"), 1500);
    });
  });

  // Tabs. The chosen tab name is remembered, so picking "pip" once picks it
  // on every page that offers it.
  const KEY = "mlaify-docs-tab";
  let remembered = null;
  try {
    remembered = localStorage.getItem(KEY);
  } catch {}

  function select(group, index, store) {
    const tabs = group.querySelectorAll('[role="tab"]');
    const panels = group.querySelectorAll('[role="tabpanel"]');
    tabs.forEach((t, i) => t.setAttribute("aria-selected", String(i === index)));
    panels.forEach((p, i) => (p.hidden = i !== index));
    if (store) {
      try {
        localStorage.setItem(KEY, tabs[index].textContent.trim());
      } catch {}
    }
  }

  document.querySelectorAll("[data-tabs]").forEach((group) => {
    group.classList.add("tabs-ready");
    const tabs = [...group.querySelectorAll('[role="tab"]')];
    const start = Math.max(0, tabs.findIndex((t) => t.textContent.trim() === remembered));
    select(group, start, false);
    tabs.forEach((tab, i) => {
      tab.addEventListener("click", () => select(group, i, true));
      tab.addEventListener("keydown", (e) => {
        const step = e.key === "ArrowRight" ? 1 : e.key === "ArrowLeft" ? -1 : 0;
        if (!step) return;
        const next = (i + step + tabs.length) % tabs.length;
        select(group, next, true);
        tabs[next].focus();
      });
    });
  });

  // Close the product switcher on an outside click or Escape.
  const switcher = document.querySelector("[data-product-switcher]");
  if (switcher) {
    document.addEventListener("click", (e) => {
      if (switcher.open && !switcher.contains(e.target)) switcher.open = false;
    });
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") switcher.open = false;
    });
  }

  // Highlight the heading being read in the "On this page" list.
  const links = [...document.querySelectorAll(".docs-toc a[href^='#']")];
  if (links.length && "IntersectionObserver" in window) {
    const byId = new Map(links.map((a) => [decodeURIComponent(a.hash.slice(1)), a]));
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          links.forEach((a) => a.classList.remove("active"));
          byId.get(entry.target.id)?.classList.add("active");
        });
      },
      { rootMargin: "-80px 0px -70% 0px" },
    );
    byId.forEach((_, id) => {
      const h = document.getElementById(id);
      if (h) observer.observe(h);
    });
  }
})();
