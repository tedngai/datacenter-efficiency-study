# Publishing checklist

GitHub Pages publishes the dashboard at
<https://tedngai.github.io/datacenter-efficiency-study/>.

`index.html` is a build output. Do not edit it by hand. Change
`pipeline/frontend/` and run the build.

## How GitHub Pages serves the site

The repository root is the site root. GitHub Pages serves the files as they
are, with no build step, because `.nojekyll` is present.

`.nojekyll` is necessary. Without it, Pages runs Jekyll over the tree. That
slows the deploy, drops paths that start with an underscore, and reprocesses
Markdown.

The data is inside `index.html`. The page also links to `data/` and `docs/`
with relative paths, so the site works from the `/datacenter-efficiency-study/`
prefix. Do not add a link that starts with a single `/`.

## Before you push

1. Run `python pipeline/build.py`. It checks the canonical CSV and rebuilds
   `index.html`, `data/published/data_centers.csv` and
   `data/published/data_centers.json`.
2. Run `python pipeline/build_gpu_cooling.py` if you changed
   `data/canonical/` or the GPU tables.
3. Open `index.html` from a local server and check the atlas, the charts and
   the scenario lab.
4. Check that the working tree has no uncommitted build output. The published
   files must match the canonical CSV.
5. Check that `.env` stays out of git and out of the commit.

## Publish

1. Commit the change.
2. Run `powershell -File scripts/push.ps1`.
3. Pages rebuilds from `main` in about one minute.

## Check after publish

1. Open <https://tedngai.github.io/datacenter-efficiency-study/>.
2. Check that `index.html` loads and that the atlas tiles draw.
3. Check that `data/published/data_centers.csv` and
   `data/us_utility_impacts.csv` download.
4. Check that the four `docs/*.md` links open.
5. Check the page at 375 px width.

## Limits to know

- The site limit is 1 GB. The repository is about 4 MB.
- The soft bandwidth limit is 100 GB each month. The gzipped page is about
  204 KB, so this is about 500,000 page views.
- Pages sets no custom cache headers. The CDN caches for about ten minutes.

## Known gap

The dashboard links to `docs/*.md` files. Pages serves them as plain text, not
as rendered pages. To render them, add an HTML step to the build. Until then,
a reader who wants formatted pages can use the GitHub view.
