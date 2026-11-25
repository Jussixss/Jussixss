# Profile maintenance

- `README.md` is the public profile. All illustrations and technology icons are local SVG assets, with no runtime image service.
- `assets/header.svg` and `assets/typing.svg` animate without JavaScript. Their titles and README alt text provide static fallbacks.
- The two Roblox cards link to place IDs resolved from the owner's supplied share links on 2026-11-25. Their artwork is decorative vector artwork, not game screenshots. No visitor/player counts are hard-coded.
- `Refresh profile assets` generates statistics, the contribution snake and the 3D skyline daily at **03:17 UTC / 06:17 Moscow time**, on relevant code changes, or via **Actions → Refresh profile assets → Run workflow**. GitHub may delay scheduled runs and may disable schedules after 60 days of repository inactivity.
- Generated SVGs are committed to `assets/generated/` on `main`. They use the automatically issued `GITHUB_TOKEN`; no personal access token or extra secret is required. Generation has read access; only the publishing job has `contents: write`.
- A failed generation preserves the previous committed assets. Check the workflow logs before rerunning. The publisher only stages the three generated SVGs.
- Statistics use the GitHub API: public repository count, stars summed across owned public repositories (including forks), followers, and the contribution calendar's last-year total. These are daily snapshots, not live counters. The workflow has no access to unrelated private repositories; private activity and its details are limited to what GitHub exposes to this token and the profile's existing visibility settings.
- The snake and skyline reflect real contribution data, so a quiet calendar produces a sparse image. The 3D skyline is an SVG illustration, not an interactive chart.
- All workflow actions are pinned to full commit SHAs. Upstream generators: [Platane/snk](https://github.com/Platane/snk), [github-profile-3d-contrib](https://github.com/yoshi389111/github-profile-3d-contrib). Permission reference: [GITHUB_TOKEN](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token).

To update a game's name or artwork, edit its SVG and the corresponding README row together. Keep the verified direct Roblox game URL unless the actual place changes.
