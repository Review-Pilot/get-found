/* Get Found v1.0 — small, dependency-free enhancements.
   The site is fully usable without JavaScript (menu aside). */
(function () {
  "use strict";

  // ---- Mobile menu + dropdowns
  var toggle = document.querySelector(".menu-toggle");
  var nav = document.getElementById("site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.textContent = open ? "Close" : "Menu";
      document.body.style.overflow = open ? "hidden" : "";
    });
  }
  document.querySelectorAll(".has-sub > button").forEach(function (btn) {
    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      var li = btn.parentElement;
      var open = li.classList.toggle("open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
  });
  document.addEventListener("click", function () {
    document.querySelectorAll(".has-sub.open").forEach(function (li) {
      li.classList.remove("open");
      li.firstElementChild.setAttribute("aria-expanded", "false");
    });
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      document.querySelectorAll(".has-sub.open").forEach(function (li) { li.classList.remove("open"); });
      if (nav && nav.classList.contains("open")) toggle.click();
    }
  });

  // ---- Reviews carousel
  document.querySelectorAll("[data-carousel]").forEach(function (c) {
    var track = c.querySelector(".track");
    c.querySelectorAll("[data-dir]").forEach(function (b) {
      b.addEventListener("click", function () {
        var step = track.firstElementChild ? track.firstElementChild.getBoundingClientRect().width + 24 : 320;
        track.scrollBy({ left: step * Number(b.dataset.dir), behavior: "smooth" });
      });
    });
  });

  // ---- Blog category filter
  var chips = document.querySelectorAll("[data-filter]");
  if (chips.length) {
    chips.forEach(function (chip) {
      chip.addEventListener("click", function () {
        chips.forEach(function (c) { c.setAttribute("aria-pressed", c === chip ? "true" : "false"); });
        var f = chip.dataset.filter;
        document.querySelectorAll("[data-cat]").forEach(function (card) {
          card.hidden = !(f === "all" || card.dataset.cat === f);
        });
      });
    });
  }

  // ---- FAQ search
  var fs = document.getElementById("faq-search");
  if (fs) {
    fs.addEventListener("input", function () {
      var q = fs.value.trim().toLowerCase();
      document.querySelectorAll(".faq details").forEach(function (d) {
        d.hidden = q && d.textContent.toLowerCase().indexOf(q) === -1;
      });
    });
  }

  // ---- Contact / audit form
  // v1.0: until a form endpoint is connected (data-endpoint on the <form>),
  // the details open pre-filled in the visitor's email app, addressed to Get Found.
  var form = document.getElementById("audit-form");
  if (form) {
    try {
      if (new URLSearchParams(location.search).get("topic") === "partner") form.interest.value = "White-label / agency partnership";
    } catch (e) {}
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var data = {};
      new FormData(form).forEach(function (v, k) { data[k] = v; });
      if (data.company_website_hp) return; // honeypot
      var status = document.getElementById("form-status");
      var endpoint = form.getAttribute("data-endpoint");
      if (endpoint) {
        fetch(endpoint, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) })
          .then(function (r) { if (!r.ok) throw new Error("bad"); form.reset(); status.textContent = "Thank you! We'll be in touch shortly."; })
          .catch(function () { status.textContent = "Sorry, something went wrong. Please email rian@get-found.co.za or WhatsApp 074 124 2969."; });
        return;
      }
      var lines = [
        "Name: " + (data.first_name || "") + " " + (data.last_name || ""),
        "Email: " + (data.email || ""),
        "Phone: " + (data.phone || ""),
        "Business: " + (data.business || ""),
        "Website: " + (data.website || ""),
        "Interested in: " + (data.interest || ""),
        "", data.message || ""
      ];
      var subject = "Free Visibility Audit request" + (data.business ? " - " + data.business : "");
      window.location.href = "mailto:rian@get-found.co.za?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(lines.join("\n"));
      status.textContent = "Opening your email app… if nothing happens, email rian@get-found.co.za or WhatsApp 074 124 2969.";
    });
  }
})();
