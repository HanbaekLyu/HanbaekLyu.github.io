# Hanbaek Lyu — personal website

Static personal academic website, hosted for free on **GitHub Pages**.

Live URL (default): <https://hanbaeklyu.github.io>

## Structure
```
index.html          About / home (photo, bio, news, funding, group)
publications.html   Publications grouped by topic
talks.html          Talks (fill in)
teaching.html       Teaching history
reu.html            REU projects
contact.html        Contact info
css/style.css       All styling (UW-Madison red accent)
images/             profile.jpg goes here (falls back to profile.svg placeholder)
files/              CV.pdf, research_statement.pdf, slides, etc.
CNAME               custom domain (www.hanbaeklyu.com)
.nojekyll           tells GitHub Pages to serve files as-is
```

## To do later (by you)
- Add your photo as `images/profile.jpg` (any size ~210×260 or larger; it's cropped to fit).
- Drop `CV.pdf` and `research_statement.pdf` into `files/`.
- Fill in `talks.html`.
- Set your real Google Scholar link (search for `citations?user=` in the HTML).

## Deploy / update
Edit files, then:
```
git add -A && git commit -m "update" && git push
```
GitHub Pages rebuilds automatically in ~1 minute.

## Custom domain (keep www.hanbaeklyu.com, drop the $100/yr host)
Do this **only after** you've confirmed the site looks right at `hanbaeklyu.github.io`.
1. Rename `CNAME.example` to `CNAME` (it contains `www.hanbaeklyu.com`), commit, and push.
2. At your domain registrar's DNS settings:
   - `CNAME` record: `www` → `hanbaeklyu.github.io`
   - Four `A` records for the apex `hanbaeklyu.com` →
     `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
3. In the repo: **Settings → Pages → Custom domain** = `www.hanbaeklyu.com`, enable **Enforce HTTPS**.

If you'd rather not use the custom domain, delete `CNAME` and just use `hanbaeklyu.github.io`.
