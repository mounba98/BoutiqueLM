(function () {
  var lang = 'it';
  try {
    var q = new URLSearchParams(location.search).get('lang');
    var saved = localStorage.getItem('lm_lang');
    lang = (q === 'it' || q === 'en') ? q : (saved === 'it' || saved === 'en') ? saved :
      (((navigator.languages && navigator.languages[0]) || navigator.language || 'it').toLowerCase().indexOf('it') === 0 ? 'it' : 'en');
  } catch (e) {}
  function apply(l) {
    lang = l;
    document.documentElement.lang = l;
    document.querySelectorAll('[data-l]').forEach(function (el) { el.hidden = el.getAttribute('data-l') !== l; });
    document.querySelectorAll('[data-lang-btn]').forEach(function (b) {
      var on = b.getAttribute('data-lang-btn') === l;
      b.className = 'border-b pb-0.5 transition ' + (on ? 'text-black border-black' : 'text-zinc-400 border-transparent');
    });
    document.title = document.documentElement.getAttribute('data-title-' + l) || document.title;
    try { localStorage.setItem('lm_lang', l); } catch (e) {}
  }
  window.setLegalLang = apply;
  document.addEventListener('DOMContentLoaded', function () { apply(lang); });
})();
