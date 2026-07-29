/* assets/quiz.js
 * Reusable single-choice quiz widget.
 * Usage in any lesson:
 *   <div class="quiz" data-correct="2">
 *     <div class="q-prompt">…</div>
 *     <ol><li>…</li><li>…</li><li>…</li><li>…</li></ol>
 *     <button type="button">Reveal</button>
 *     <div class="feedback"></div>
 *   </div>
 * Rules honoured from the skill:
 *  - All options should read identically: same word count, same length profile, no
 *    capitalisation/punctuation tells. Lesson authors enforce that; we don't.
 *  - Feedback is immediate and tied to the chosen option (effortful retrieval).
 *  - No answer leaks through styling until the user commits.
 */
(function () {
  const REVEAL = "Reveal";
  const RESET  = "Reset";

  function attach(root) {
    if (root.dataset.quizBound) return;
    root.dataset.quizBound = "1";

    const correctIdx = parseInt(root.dataset.correct, 10);
    const opts = Array.from(root.querySelectorAll("ol > li"));
    const btn = root.querySelector("button");
    const feedback = root.querySelector(".feedback");
    let picked = null;

    if (Number.isNaN(correctIdx) || !opts.length || !btn || !feedback) return;

    opts.forEach((li, i) => {
      li.style.cursor = "pointer";
      li.addEventListener("click", () => {
        if (root.classList.contains("answered")) return;
        if (picked === i) { picked = null; li.style.outline = ""; return; }
        if (picked !== null) opts[picked].style.outline = "";
        picked = i;
        li.style.outline = "2px solid var(--ink)";
        li.style.outlineOffset = "1px";
      });
    });

    btn.addEventListener("click", () => {
      if (!root.classList.contains("answered")) {
        if (picked === null) {
          feedback.className = "feedback no";
          feedback.textContent = "Pick an option first.";
          return;
        }
        root.classList.add("answered");
        opts.forEach((li, i) => {
          li.style.outline = "";
          li.style.cursor = "default";
          if (i === correctIdx)      li.classList.add("correct");
          else if (i === picked)     li.classList.add("wrong-pick");
        });
        const ok = picked === correctIdx;
        feedback.className = "feedback " + (ok ? "ok" : "no");
        feedback.textContent = ok
          ? "Correct."
          : "Not quite — the right answer is " +
            String.fromCharCode(65 + correctIdx) + ".";
        btn.textContent = RESET;
      } else {
        // Reset.
        root.classList.remove("answered");
        opts.forEach(li => { li.classList.remove("correct", "wrong-pick"); li.style.cursor = "pointer"; });
        picked = null;
        feedback.className = "feedback";
        feedback.textContent = "";
        btn.textContent = REVEAL;
      }
    });
  }

  function initAll() {
    document.querySelectorAll(".quiz[data-correct]").forEach(attach);
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initAll);
  } else {
    initAll();
  }
  // Expose for future lessons that inject quizzes dynamically.
  window.Quiz = { attach, initAll };
})();