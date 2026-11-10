# Setup — Sharingan GitHub Profile

## Upload

1. Create or open your public repository **C0dingPaper/C0dingPaper** (the repo name must match your username).
2. Extract the package; upload **its contents**, not the enclosing folder.
3. In KDE Dolphin, press **Ctrl+H** to reveal `.github`. Make sure `.github/workflows/snake.yml` and `charts.yml` are uploaded.
4. If GitHub says a file already exists, replace the old version, especially `README.md` and the `.github/workflows` files. Delete obsolete Matrix-themed assets/workflows if you no longer use them.
5. Use a `main` default branch, or update both workflow `branches:` values and the chart push behavior to your actual default branch.

## Activate the animated contributions

1. In the repository, go to **Settings → Actions → General**. Ensure Actions are allowed and **Workflow permissions → Read and write permissions** is enabled where your account exposes this option. The workflow also explicitly declares `contents: write`.
2. Go to **Actions → Sharingan Contribution Snake → Run workflow** and trigger it manually once.
3. When the run succeeds, confirm the **output** branch exists and contains `sharingan-snake.svg`.
4. Open https://raw.githubusercontent.com/C0dingPaper/C0dingPaper/output/sharingan-snake.svg to verify the image. Then reload https://github.com/C0dingPaper. GitHub image caching may delay the refreshed graphic.
5. The workflow is also scheduled daily. Scheduled workflows can be delayed by GitHub and can be disabled automatically after prolonged repository inactivity.

**If the image is broken:** inspect the Actions run logs (Generate animated scarlet contribution snake / Publish animation to output branch), the `output` branch, and the exact URL above. A workflow that has not run cannot display a freshly generated image. If branch protection or organization policy blocks pushing, adjust repository permissions. Forks can have actions disabled by default.

**If the SVG does not visibly move:** open it directly in a browser. Browser reduced-motion settings or specific image renderers may stop animations; GitHub's own green contribution grid is separate and cannot be styled by a README.

**Graph size:** the README uses `width="100%"` and the snake itself spans the available README width. It cannot exceed GitHub's content column without a separate hosted web page.

## Edit focus charts

Edit `focus.json` weights (0–10; **learning emphasis**, not proficiency), then run:

```bash
python scripts/generate_focus.py
```

Commit the generated assets. The charts workflow will also update them after changes to `focus.json` on `main`.

## LeetCode

No username was provided. The LeetCode section intentionally does not show fabricated counts. Add your real profile URL later, optionally along with a third-party stats card.

## Notes

- External stats, badges, icons and typing effects depend on third-party availability; custom header/footer/charts are stored locally.
- The `output` branch contains generated animation; do not upload it manually.
- The full-width contribution snake displays **real GitHub contributions** after the workflow runs; the decorative Sharingan eye in the header is original SVG artwork.
- The main GitHub contribution calendar below the README will remain GitHub's regular, unstyled calendar.


## Repair for broken images

The `.github` directory is hidden in Linux. Drag-and-drop upload can silently omit it. For reliable deployment, copy the complete contents including hidden `.github` folder with `cp -a SOURCE/. CLONED_REPOSITORY/` and push with git.

Under GitHub Actions, run **Sharingan Contribution Snake** and **Sharingan GitHub Metrics** separately. The snake workflow generates the `output` branch; the metrics workflow updates the two local SVG stats images.

The native GitHub contribution calendar cannot be styled from a README; the animation is a separate SVG embedded within the README.

## Sharingan profile-view counter (starts at 2,477)

The red badge in `README.md` uses the Komarev profile-view counter with `base=2477`.
It uses its own tracking key (`C0dingPaper-Sharingan-Views-20261110`) so older counts
under the regular GitHub handle do not inflate the intended starting value.

This number is **a configured starting offset, not 2,477 verified historical visits**.
It increments when the counter service receives eligible image requests. GitHub's
Camo/image caching, bots, refreshes, and browser behavior mean it cannot guarantee
exactly one increment for each human page opening or identify unique visitors.
Do not change the tracking key unless you intend to start a new counter.

No JavaScript, token, or GitHub Action is needed for this badge.
