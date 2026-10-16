// Anands Vault: pre-fill the email on the login screen (the web vault is a hash-routed SPA).
// The placeholder below is replaced at container start from ANANDS_VAULT_EMAIL (see start.sh).
// Never overwrites anything already typed, and only touches the #/login route.
(function () {
  var EMAIL = "__ANANDS_EMAIL__";
  if (!EMAIL) return;
  var SEL = 'input[type="email"], input[formcontrolname="email"], input[id*="email" i], input[autocomplete="username"]';
  function onLogin() { return /^#\/login(\?|$)/.test(location.hash); }
  function fill() {
    if (!onLogin()) return;
    var el = document.querySelector(SEL);
    if (!el || el.value || el.getAttribute("data-anands-filled")) return;
    el.setAttribute("data-anands-filled", "1");
    var set = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, "value").set;
    set.call(el, EMAIL);
    el.dispatchEvent(new Event("input", { bubbles: true }));
    el.dispatchEvent(new Event("change", { bubbles: true }));
  }
  new MutationObserver(fill).observe(document.documentElement, { childList: true, subtree: true });
  window.addEventListener("hashchange", fill);
  fill();
})();
