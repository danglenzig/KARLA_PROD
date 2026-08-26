import os
import shutil
import subprocess
import sys
from pathlib import Path
import asyncio

SRC_ROOT: Path = Path(__file__).parent.parent # this is the src/ folder
sys.path.insert(0, str(SRC_ROOT))

from image_generator_agent.image_generator_models import ArtAssetManifest
from misc_models.misc_models import DemoCreativeData

SEED_PROJECT_PATH: str = "/mnt/c/RENPY/BLANK_PROJECT/"
DEFAULT_RENPY_ROOT: Path = Path("/mnt/c/RENPY")

class RenPyPublisher():
    _INVALID_WINDOWS_FILENAME_CHARS: set[str] = set('<>:"/\\|?*')
    _WINDOWS_RESERVED_NAMES: set[str] = {
        "CON", "PRN", "AUX", "NUL",
        "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
        "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9",
    }

    def _validate_game_title(self, game_title: str) -> str:
        normalized_title = game_title.strip()
        if not normalized_title:
            raise ValueError("game_title must not be empty")
        if normalized_title.endswith((".", " ")):
            raise ValueError("game_title cannot end with a period or space on Windows")
        if any(char in self._INVALID_WINDOWS_FILENAME_CHARS for char in normalized_title):
            raise ValueError(f"game_title contains invalid Windows filename characters: {game_title}")
        if normalized_title.upper() in self._WINDOWS_RESERVED_NAMES:
            raise ValueError(f"game_title cannot be a reserved Windows device name: {game_title}")
        return normalized_title

    def _resolve_seed_project_path(self) -> Path:
        seed_project_path = Path(SEED_PROJECT_PATH).resolve()
        if not seed_project_path.is_dir():
            raise FileNotFoundError(f"Seed Ren'Py project not found: {seed_project_path}")
        if not any(seed_project_path.iterdir()):
            raise FileNotFoundError(f"Seed Ren'Py project is empty: {seed_project_path}")
        return seed_project_path

    def _resolve_target_root(self, target_folder_path: str) -> Path:
        target_root = Path(target_folder_path).resolve()
        if not target_root.is_dir():
            raise FileNotFoundError(f"Target Ren'Py folder does not exist: {target_root}")
        return target_root

    def _prepare_target_project_path(self, target_root: Path, game_title: str) -> Path:
        project_path = target_root / game_title
        if project_path.exists() and any(project_path.iterdir()):
            raise FileExistsError(f"Target project folder already exists and is not empty: {project_path}")
        project_path.mkdir(parents=True, exist_ok=True)
        return project_path

    def _copy_seed_project(self, seed_project_path: Path, target_project_path: Path) -> None:
        for source_path in seed_project_path.iterdir():
            destination_path = target_project_path / source_path.name
            if source_path.is_dir():
                shutil.copytree(source_path, destination_path, dirs_exist_ok=False)
            else:
                shutil.copy2(source_path, destination_path)

    def _patch_options_file(self, target_project_path: Path, game_title: str) -> None:
        options_path = target_project_path / "game" / "options.rpy"
        if not options_path.is_file():
            raise FileNotFoundError(f"Ren'Py options file not found: {options_path}")

        options_text = options_path.read_text(encoding="utf-8")
        if "BLANK_PROJECT" not in options_text:
            raise ValueError(f"Expected BLANK_PROJECT marker not found in {options_path}")

        options_path.write_text(options_text.replace("BLANK_PROJECT", game_title), encoding="utf-8")

    def _delete_compiled_script_if_present(self, target_project_path: Path) -> None:
        compiled_script_path = target_project_path / "game" / "script.rpyc"
        if compiled_script_path.exists():
            compiled_script_path.unlink()

    def _copy_script(self, script_file_path: str, target_project_path: Path) -> Path:
        source_script_path = Path(script_file_path).resolve()
        if not source_script_path.is_file():
            raise FileNotFoundError(f"Generated script file not found: {source_script_path}")

        destination_script_path = target_project_path / "game" / "script.rpy"
        if not destination_script_path.parent.is_dir():
            raise FileNotFoundError(f"Ren'Py game folder not found: {destination_script_path.parent}")

        shutil.copy2(source_script_path, destination_script_path)
        return destination_script_path

    def _copy_art_assets(self, art_manifest: ArtAssetManifest, target_project_path: Path) -> list[Path]:
        images_path = target_project_path / "game" / "images"
        images_path.mkdir(parents=True, exist_ok=True)

        copied_paths: list[Path] = []
        claimed_destination_names: set[str] = set()
        asset_paths = [
            *art_manifest.character_portrait_paths,
            *art_manifest.scene_background_paths,
        ]

        for asset_path_string in asset_paths:
            source_asset_path = Path(asset_path_string).resolve()
            if not source_asset_path.is_file():
                raise FileNotFoundError(f"Art asset not found: {source_asset_path}")

            destination_path = images_path / source_asset_path.name
            destination_key = destination_path.name.lower()
            if destination_key in claimed_destination_names:
                raise ValueError(f"Duplicate asset filename would overwrite in Ren'Py images folder: {destination_path.name}")

            shutil.copy2(source_asset_path, destination_path)
            claimed_destination_names.add(destination_key)
            copied_paths.append(destination_path)

        return copied_paths

    def _resolve_renpy_sdk_path(self, target_root: Path) -> Path:
        candidate_paths: list[Path] = []
        renpy_sdk_override = os.getenv("RENPY_SDK_PATH")
        if renpy_sdk_override:
            candidate_paths.append(Path(renpy_sdk_override))

        candidate_paths.extend(sorted(DEFAULT_RENPY_ROOT.glob("renpy-*-sdk"), reverse=True))
        if target_root != DEFAULT_RENPY_ROOT:
            candidate_paths.extend(sorted(target_root.glob("renpy-*-sdk"), reverse=True))

        for candidate_path in candidate_paths:
            if candidate_path.is_dir() and (candidate_path / "renpy.sh").is_file():
                return candidate_path

        raise FileNotFoundError(
            "Could not find a Ren'Py SDK with renpy.sh under the target root. "
            "Expected something like /mnt/c/RENPY/renpy-8.5.2-sdk"
        )

    def _run_renpy_command(self, sdk_path: Path, project_path: Path, *args: str) -> subprocess.CompletedProcess[str]:
        command = [str(sdk_path / "renpy.sh"), str(project_path), *args]
        return subprocess.run(
            command,
            cwd=sdk_path,
            capture_output=True,
            text=True,
            check=False,
        )

    def _validate_published_project(self, sdk_path: Path, project_path: Path) -> None:
        lint_result = self._run_renpy_command(sdk_path, project_path, "lint")
        if lint_result.returncode != 0:
            raise RuntimeError(
                "Ren'Py lint failed.\n"
                f"STDOUT:\n{lint_result.stdout}\n"
                f"STDERR:\n{lint_result.stderr}"
            )

        compile_result = self._run_renpy_command(sdk_path, project_path, "compile")
        if compile_result.returncode != 0:
            raise RuntimeError(
                "Ren'Py compile failed.\n"
                f"STDOUT:\n{compile_result.stdout}\n"
                f"STDERR:\n{compile_result.stderr}"
            )

    async def run_workflow(
            self,

            game_title:str,

            script_file_path: str, # Will look something like: "/mnt/c/SchoolRepos/PYTHON/KARLA_RECOVER/KARLA_PROD/KARLA_GAMES/my_cool_game_name/RENPY_SCRPTS/script.rpy

            art_manifest: ArtAssetManifest, # contains path strings to where the generated images live

            target_folder_path:str = "/mnt/c/RENPY/", # TODO change this to environment variable
    )->bool:

        r"""
        1) Create an empty folder at target_folder_path, named game_title
            - if target_folder_path doesn't exist, raise an error
            - if game_title is not a valid Windows folder name, raise an error
            - if using the function defauts, there should now be a new windows folder:
                - In Windows File Explorer: "C:\RENPY\{game_title}\"
                - Seen from the linux venv of this tool, it's: "/mnt/c/RENPY/{game_title}/

        2) Copy the *entire contents* of SEED_PROJECT_PATH into ^^that new folder.
            - if SEED_PROJECT_PATH is doesn't exist or is empty, raise an error
            - The seed project is a new, fresh Ren'Py project, already configured with the proper defaults

        3) In the new folder, find the /game/options.rpy file and patch it so the `config.name`,
            `config.save_directory`, and `build.name` values match the game_title.
            - This should be a simple matter of search-replacing `BLANK_PROJECT` with the game_title string.

        4) Delete {new_game_folder}/game/script.rpyc if it exists.
            - RenPy will make a new one when the game compiles

        5) Copy the script.rpy file at script_file_path into {target_folder_path}{game_title}/game/script.rpy,
            *overwriting* the existing script.rpy file in the destination folder.
            - This workflow can trust that the new script.rpy file is already validated

        6) Copy the file at each path in art_manifest (portraits and backgrounds) 
            into {new_game_folder}/game/images/

        7) Run Ren'Py CLI lint and compile on the target project as a post-publish
            validation step.

        8) Print a log message telling the user that their game is ready.
        """

        normalized_game_title = self._validate_game_title(game_title)
        target_root = self._resolve_target_root(target_folder_path)
        seed_project_path = self._resolve_seed_project_path()
        target_project_path = self._prepare_target_project_path(target_root, normalized_game_title)

        self._copy_seed_project(seed_project_path, target_project_path)
        self._patch_options_file(target_project_path, normalized_game_title)
        self._delete_compiled_script_if_present(target_project_path)

        destination_script_path = self._copy_script(script_file_path, target_project_path)
        copied_asset_paths = self._copy_art_assets(art_manifest, target_project_path)

        renpy_sdk_path = self._resolve_renpy_sdk_path(target_root)
        self._validate_published_project(renpy_sdk_path, target_project_path)

        print(
            "Published Ren'Py project successfully:\n"
            f"  Project: {target_project_path}\n"
            f"  Script: {destination_script_path}\n"
            f"  Images copied: {len(copied_asset_paths)}"
        )

        return True

async def main():

    game_path_str: str = "/mnt/c/SchoolRepos/PYTHON/KARLA_RECOVER/KARLA_PROD/KARLA_GAMES/"
    game_title: str = "velvet _freight"
    creative_data_path_str: str = f"{game_path_str}{game_title}/DATA/creative_data.json"
    script_path_str: str = f"{game_path_str}{game_title}/RENPY_SCRIPTS/script.rpy"

    with open(creative_data_path_str, 'r') as f:
        json_str = f.read().strip()
    creative_data: DemoCreativeData = DemoCreativeData.model_validate_json(json_str)
    art_manifest: ArtAssetManifest = creative_data.art_assets

    success = await RenPyPublisher().run_workflow(
        game_title=game_title,
        script_file_path=script_path_str,
        art_manifest=art_manifest
    )
    

if __name__ == "__main__":
    asyncio.run(main())