The plan:

- Create one blank Ren'Py project manually once, using the same SDK version you plan to support. Treat that folder as your Karla seed template.

- After orchestrator Stage 5, right after the current script assembly/write, add a publish step that copies the seed template to a new target folder named after the generated game title.

- In that copied project, patch game/options.rpy so config.name, config.save_directory, and build.name match the generated title. The Ren'Py template-project docs explicitly say the launcher does this when it creates from a template; if you bypass the launcher and use copytree, you need to do that part yourself.

- Copy the generated script.rpy into target_project/game/script.rpy. Delete target_project/game/script.rpyc if it exists, or just run Ren'Py compile immediately after publishing so it regenerates cleanly.

- Copy every path from ArtAssetManifest into target_project/game/images. You do not need to scan folders or infer names; the manifest already gives you the authoritative sources.

- Run Ren'Py CLI lint and compile on the target project as a post-publish validation step. That gives you a cheap machine check before launch.

- If you want the launcher to show the project automatically, either create it inside the launcher’s projects directory or register an external path through the projects.txt mechanism described in the launcher docs.

I would not recommend trying to reverse-engineer the launcher’s Create New Project flow or drive it as a subprocess/UI macro. It is more brittle than copying a seed project, and the CLI docs explicitly warn that the CLI is not a stable interface across releases. A seed-template approach is simpler, version-safe, and fits your current architecture.

One useful follow-on is GUI automation. Your color agent already produces hex-ready colors via gui_colors_models.py:18 and gui_colors_models.py:33. Ren'Py’s launcher CLI can generate or replace GUI assets for an existing project, so later you could feed the accent color into that step after the template copy.

One small project note: your workflow doc says the script ends up under DATA in MODULE_WORKFLOW.md:15, but the orchestrator actually writes it to RENPY_SCRIPTS via orchestrator.py:62. That doc drift is worth fixing when you add the publish phase.
