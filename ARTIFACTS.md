# Published artifacts

Publish with the Artifact tool (`url` + `file_path` + a `files` map; read a file first if the tool says it changed).
All three real artifacts declare `db` (root read/write `owner`; `data/users/{self}` read/write `interact`) + `user` (see SPEC.md).

| Exam | Title | Slug | Link |
|---|---|---|---|
| Technician | Technician Class Trainer | d00c70f5-a606-48a8-ac64-5b1842328783 | https://claude.ai/artifact/Sh4cJiGP3fLhWjVSZnyxTL |
| Extra | Extra Class Trainer | 2b21fb82-f2d4-46b4-be2b-52f6ea2966bc | https://claude.ai/artifact/6KvPV3j5FiNQxkDvHqce91 |
| General | General Class Trainer | | https://claude.ai/artifact/6ybQ4odexMzPKbgtAhoHux |
| Preview (test copy) | General Trainer Preview (shows whichever exam's batch is being tested) | | https://claude.ai/artifact/JVa74CyW5j9ktfCoZp2u1o |

Files published per artifact: `index.html`, `pool.json`, `hooks.json`, `fig/*.png`, `families/*.json` (from `exams/<exam>/site/`, after `tools/site.py build <exam>`).

The preview is a test copy for trying a batch before its PR merges. Publish the branch's built site there
(title changed to "<Exam> Trainer Preview", no `db`/`user`, so it never touches saved progress), then
republish the real artifact from `main` after the merge.
When the preview switches exams, remove the other exam's files from it (pass `null` for each stale path).

# Public website

The `web/` folder, served by Cloudflare Pages from this repo (free plan, Brooke's Cloudflare account).
Settings: production branch `main`, no build command, build output directory `web`. Every merge to `main`
updates the site in about a minute; every other branch gets a preview link (shown on its PR).

| Page | Link |
|---|---|
| Hub | https://ham-trainers.pages.dev/ |
| Technician | https://ham-trainers.pages.dev/technician/ |

Cloudflare project name: `ham-trainers`. A branch's preview is at `https://<branch>.ham-trainers.pages.dev/`.
