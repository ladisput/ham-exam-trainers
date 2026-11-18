# Published artifacts

Publish with `publish_files` in `patch` mode, passing the slug and the current version
(get it with `get_artifact` first). Both artifacts declare `db` + `user` (see SPEC.md).

| Exam | Title | Slug | Link |
|---|---|---|---|
| Technician | Technician Class Trainer | d00c70f5-a606-48a8-ac64-5b1842328783 | https://claude.ai/artifact/Sh4cJiGP3fLhWjVSZnyxTL |
| Extra | Extra Class Trainer | 2b21fb82-f2d4-46b4-be2b-52f6ea2966bc | https://claude.ai/artifact/6KvPV3j5FiNQxkDvHqce91 |
| General | (not built yet) | | |
| Technician (preview) | Technician Trainer Preview | | https://claude.ai/artifact/JVa74CyW5j9ktfCoZp2u1o |

Files published per artifact: `index.html`, `pool.json`, `hooks.json`, `fig/*.png`, `families/*.json` (from `exams/<exam>/site/`, after `tools/site.py build <exam>`).

The preview is a test copy for trying a batch before its PR merges. Publish the branch's built site there
(title changed to "Technician Trainer Preview", no `db`/`user`, so it never touches saved progress), then
republish the real artifact from `main` after the merge.
