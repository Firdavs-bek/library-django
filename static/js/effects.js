/* ================================================================
   Umumiy effektlar (qorong‘i rejim, animatsiya, qidiruv, o‘qish).
   Kitoblar va matnlar bu yerda emas — ular bazada, admin paneldan qo‘shiladi.
   ================================================================ */
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];

/* 1. Qorong‘i / yorug‘ rejim */
const root = document.documentElement;
function setTheme(t) {
  root.dataset.bsTheme = t; localStorage.setItem('theme', t);
  const icon = $('#theme i'); if (icon) icon.className = 'bi ' + (t === 'dark' ? 'bi-sun' : 'bi-moon-stars');
}
setTheme(localStorage.getItem('theme') || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'));
document.addEventListener('click', e => { if (e.target.closest('#theme')) setTheme(root.dataset.bsTheme === 'dark' ? 'light' : 'dark'); });

/* 2. Animatsiya: .reveal paydo bo‘ladi, [data-count] sanaladi */
const io = new IntersectionObserver(items => items.forEach(i => { if (i.isIntersecting) { i.target.classList.add('show'); io.unobserve(i.target); } }), { threshold: 0.1 });
$$('.reveal').forEach(el => io.observe(el));
$$('[data-count]').forEach(el => {
  const n = +el.dataset.count; let t0;
  const step = t => { t0 ??= t; const k = Math.min((t - t0) / 900, 1); el.textContent = Math.round(n * k); if (k < 1) requestAnimationFrame(step); };
  requestAnimationFrame(step);
});

/* 3. Katalog: qidiruv va janr bo‘yicha saralash */
const search = $('#search');
if (search) {
  let genre = 'all';
  const apply = () => {
    $$('#list [data-genre]').forEach(c => c.hidden = !((genre === 'all' || c.dataset.genre === genre) && c.textContent.toLowerCase().includes(search.value.toLowerCase())));
    $('#none').hidden = !!$('#list [data-genre]:not([hidden])');
  };
  search.oninput = apply; apply();
  $('#chips').onclick = e => {
    const b = e.target.closest('[data-filter]'); if (!b) return;
    genre = b.dataset.filter;
    $$('[data-filter]').forEach(x => x.className = 'btn btn-sm rounded-pill ' + (x === b ? 'btn-primary' : 'btn-outline-primary'));
    apply();
  };
}

/* 4. O‘qish sahifasi: shrift o‘lchami va o‘qish chizig‘i */
const text = $('#text');
if (text) {
  let size = +localStorage.getItem('size') || 20;
  const resize = d => { size = Math.min(30, Math.max(14, size + d)); localStorage.setItem('size', size); text.style.fontSize = size + 'px'; };
  resize(0); $('#smaller').onclick = () => resize(-1); $('#bigger').onclick = () => resize(1);
  addEventListener('scroll', () => $('#scrollBar').style.width = scrollY / Math.max(1, document.body.scrollHeight - innerHeight) * 100 + '%');
}
const src = book.cover_url.startsWith('http') ? book.cover_url : '/media/' + book.cover_url;