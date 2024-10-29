# Copyright (C) 2024 LewdDevelopment
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import argparse
import json
import logging
import os
import shutil
import sys
import time
from pathlib import Path

import filetype
import yaml
from ruamel.yaml import YAML
from voluptuous import ALLOW_EXTRA, All, Optional, Range, Schema, Union, Url

CURRENT_FORMAT = "1.1"

PATH = Path(__file__).parent
DEFAULT_PACK = PATH / "default_pack.yml"


class Source:
    def __init__(self, root: str):
        self.root = PATH / root

        # Directories
        self.media = self.root / "media"
        self.subliminals = self.root / "subliminals"
        self.wallpapers = self.root / "wallpapers"

        # Files
        self.icon = self.root / "icon.ico"
        self.pack = self.root / "pack.yml"
        self.splash = self.root / "loading_splash"


class Build:
    def __init__(self, root: str):
        self.root = PATH / root

        # Directories
        self.audio = self.root / "aud"
        self.image = self.root / "img"
        self.subliminals = self.root / "subliminals"
        self.video = self.root / "vid"

        # Files
        self.captions = self.root / "captions.json"
        self.config = self.root / "config.json"
        self.corruption = self.root / "corruption.json"
        self.discord = self.root / "discord.dat"
        self.icon = self.root / "icon.ico"
        self.info = self.root / "info.json"
        self.splash = self.root / "loading_splash"
        self.media = self.root / "media.json"
        self.prompt = self.root / "prompt.json"
        self.wallpaper = self.root / "wallpaper.png"
        self.web = self.root / "web.json"


def write_json(data: dict, path: Path) -> None:
    logging.info(f"Writing {path.name}")
    with open(path, "w") as f:
        json.dump(data, f)


def make_media(source: Source, build: Build) -> set[str]:
    """Returns a set of existing, valid moods"""

    media = {}

    if not source.media.is_dir():
        logging.error(f"{source.media} does not exist or is not a directory, unable to read media")
        return set()

    moods = os.listdir(source.media)
    if len(moods) == 0:
        logging.error("Media directory exists, but it is empty")
        return set()

    for mood in moods:
        mood_path = source.media / mood
        if not mood_path.is_dir():
            logging.warning(f"{mood_path} is not a directory")
            continue

        mood_media = os.listdir(mood_path)
        if len(mood_media) == 0:
            logging.warning(f"Mood directory {mood} exists, but it is empty")
            continue

        logging.info(f"Copying media from mood {mood}")
        media[mood] = []
        for filename in mood_media:
            file_path = mood_path / filename

            location = None
            if filetype.is_image(file_path):
                location = build.image
            elif filetype.is_video(file_path):
                location = build.video
            elif filetype.is_audio(file_path):
                location = build.audion

            if location:
                location.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(file_path, location / filename)
                media[mood].append(filename)
            else:
                logging.warning(f"{file_path} is not an image, video, or audio file")

    write_json(media, build.media)
    return set(media.keys())


def make_subliminals(source: Source, build: Build) -> None:
    if not source.subliminals.is_dir():
        return

    subliminals = os.listdir(source.subliminals)
    if len(subliminals) == 0:
        logging.warning("Subliminals directory exists, but it is empty")
        return

    logging.info("Copying subliminals")
    build.subliminals.mkdir(parents=True, exist_ok=True)
    for filename in subliminals:
        file_path = source.subliminals / filename
        if filetype.is_image(file_path):
            shutil.copyfile(file_path, build.subliminals / filename)
        else:
            logging.warning(f"{file_path} is not an image")


def make_wallpapers(source: Source, build: Build) -> None:
    if not source.wallpapers.is_dir():
        logging.warning(f"{source.wallpapers} does not exist or is not a directory")
        return

    wallpapers = os.listdir(source.wallpapers)
    if len(wallpapers) == 0:
        logging.warning("Wallpaper directory exists, but it is empty")
        return

    logging.info("Copying wallpapers")
    default_found = False
    for filename in wallpapers:
        file_path = source.wallpapers / filename
        default_found = default_found or filename == "wallpaper.png"
        if filetype.is_image(file_path):
            shutil.copyfile(file_path, build.root / filename)
        else:
            logging.warning(f"{file_path} is not an image")

    if not default_found:
        logging.warning("No default wallpaper.png found")


def make_icon(source: Source, build: Build) -> None:
    if not os.path.exists(source.icon):
        return

    if filetype.is_image(source.icon):
        logging.info("Copying icon")
        shutil.copyfile(source.icon, build.icon)
    else:
        logging.warning(f"{source.icon} is not an image")


def make_loading_splash(source: Source, build: Build) -> None:
    loading_splash_found = False
    for extension in [".png", ".gif", ".jpg", ".jpeg", ".bmp"]:
        loading_splash_path = source.splash.with_suffix(extension)
        if not os.path.exists(loading_splash_path):
            continue

        if loading_splash_found:
            logging.warning(f"Found multiple loading splashes, ignoring {loading_splash_path}")
            continue

        if filetype.is_image(loading_splash_path):
            logging.info("Copying loading splash")
            shutil.copyfile(loading_splash_path, build.splash.with_suffix(extension))
            loading_splash_found = True
        else:
            logging.warning(f"{loading_splash_path} is not an image")


def make_info(pack: yaml.Node, build: Build) -> None:
    if not pack["info"]["generate"]:
        logging.info("Skipping info.json")
        return

    Schema(
        {
            "generate": bool,
            "name": str,
            "id": str,
            "creator": str,
            "version": str,
            "description": str,
        },
        required=True,
        extra=ALLOW_EXTRA,
    )(pack["info"])

    info = {
        "name": pack["info"]["name"],
        "id": pack["info"]["id"],
        "creator": pack["info"]["creator"],
        "version": pack["info"]["version"],
        "description": pack["info"]["description"].strip(),
    }

    write_json(info, build.info)


def make_discord(pack: yaml.Node, build: Build) -> None:
    if not pack["discord"]["generate"]:
        logging.info("Skipping discord.dat")
        return

    Schema({"generate": bool, "status": str}, required=True, extra=ALLOW_EXTRA)(pack["discord"])

    with open(build.discord, "w") as f:
        logging.info("Writing discord.dat")
        f.write(pack["discord"]["status"])


def make_captions(pack: yaml.Node, build: Build) -> None:
    if not pack["captions"]["generate"]:
        logging.info("Skipping captions.json")
        return

    Schema(
        {
            "generate": bool,
            "close-text": str,
            "denial": Union([str], None),
            "default-captions": [str],
            "subliminal-messages": Union([str], None),
            "notifications": Union([str], None),
            "prefixes": Union(
                [
                    {
                        "name": str,
                        Optional("chance"): All(Union(int, float), Range(min=0, max=100)),
                        Optional("max-clicks"): All(int, Range(min=1)),
                        "captions": [str],
                    }
                ],
                None,
            ),
        },
        required=True,
        extra=ALLOW_EXTRA,
    )(pack["captions"])

    captions = {
        "subtext": pack["captions"]["close-text"],
        "default": pack["captions"]["default-captions"],
        "prefix": [],
        "prefix_settings": {},
    }

    denial = pack["captions"]["denial"]
    if denial:
        captions["denial"] = denial

    subliminal_messages = pack["captions"]["subliminal-messages"]
    if subliminal_messages:
        captions["subliminals"] = subliminal_messages

    notifications = pack["captions"]["notifications"]
    if notifications:
        captions["notifications"] = notifications

    prefixes = pack["captions"]["prefixes"]
    if prefixes:
        for prefix in prefixes:
            prefix_name = prefix["name"]

            captions["prefix"].append(prefix_name)
            captions[prefix_name] = prefix["captions"]

            prefix_settings = {}
            if "chance" in prefix:
                prefix_settings["chance"] = prefix["chance"]
            if "max-clicks" in prefix:
                prefix_settings["max"] = prefix["max-clicks"]

            if prefix_settings:
                captions["prefix_settings"][prefix_name] = prefix_settings

    write_json(captions, build.captions)


def make_prompt(pack: yaml.Node, build: Build) -> None:
    if not pack["prompt"]["generate"]:
        logging.info("Skipping prompt.json")
        return

    Schema(
        {
            "generate": bool,
            "command": Union(str, None),
            "submit-text": str,
            "minimum-length": All(int, Range(min=1)),
            "maximum-length": All(int, Range(min=pack["prompt"]["minimum-length"])),
            "default-prompts": {
                "weight": All(int, Range(min=0)),
                "prompts": Union([str], None),
            },
            "moods": Union(
                [
                    {
                        "name": str,
                        "weight": All(int, Range(min=0)),
                        "prompts": [str],
                    }
                ],
                None,
            ),
        },
        required=True,
        extra=ALLOW_EXTRA,
    )(pack["prompt"])

    prompt = {
        "subtext": pack["prompt"]["submit-text"],
        "minLen": pack["prompt"]["minimum-length"],
        "maxLen": pack["prompt"]["maximum-length"],
        "moods": [],
        "freqList": [],
    }

    command = pack["prompt"]["command"]
    if command:
        prompt["commandtext"] = command

    default = pack["prompt"]["default-prompts"]
    if default["prompts"]:
        prompt["moods"].append("default")
        prompt["freqList"].append(default["weight"])
        prompt["default"] = default["prompts"]

    moods = pack["prompt"]["moods"]
    if moods:
        for mood in moods:
            mood_name = mood["name"]

            prompt["moods"].append(mood_name)
            prompt["freqList"].append(mood["weight"])
            prompt[mood_name] = mood["prompts"]

    write_json(prompt, build.prompt)


def make_web(pack: yaml.Node, build: Build) -> None:
    if not pack["web"]["generate"]:
        logging.info("Skipping web.json")
        return

    Schema(
        {
            "generate": bool,
            "urls": [{"url": Url(), "mood": str, Optional("args"): [str]}],
        },
        required=True,
        extra=ALLOW_EXTRA,
    )(pack["web"])

    web = {"urls": [], "moods": [], "args": []}

    for url in pack["web"]["urls"]:
        web["urls"].append(url["url"])
        web["moods"].append(url["mood"])

        args_string = ""
        if "args" in url:
            for arg in url["args"]:
                if "," in arg:
                    logging.error(f"Web args must not contain commas, invalid arg: {arg}")
                else:
                    if args_string != "":
                        args_string += ","
                    args_string += f"{arg}"

        web["args"].append(args_string)

    write_json(web, build.web)


def make_corruption(pack: yaml.Node, build: Build, moods: set[str]) -> None:
    if not pack["corruption"]["generate"]:
        logging.info("Skipping corruption.json")
        return

    Schema(
        {
            "generate": bool,
            "levels": [
                {
                    Optional("add-moods"): [str],
                    Optional("remove-moods"): [str],
                    Optional("wallpaper"): str,
                    Optional("config"): dict,
                }
            ],
        },
        required=True,
        extra=ALLOW_EXTRA,
    )(pack["corruption"])

    corruption = {"moods": {}, "wallpapers": {}, "config": {}}

    active_moods = set()
    for i, level in enumerate(pack["corruption"]["levels"]):
        n = str(i + 1)
        corruption["moods"][n] = {}

        remove = []
        if "remove-moods" in level:
            for mood in level["remove-moods"]:
                if mood in active_moods:
                    remove.append(mood)
                    active_moods.remove(mood)
                else:
                    logging.warning(f"Corruption level {n} is trying to remove an inactive mood {mood}, skipping")
        corruption["moods"][n]["remove"] = remove

        add = []
        if "add-moods" in level:
            for mood in level["add-moods"]:
                if mood in moods:
                    add.append(mood)
                    active_moods.add(mood)
                else:
                    logging.warning(f"Corruption level {n} is trying to add a nonexistent mood {mood}, skipping")
        corruption["moods"][n]["add"] = add

        if "wallpaper" in level:
            corruption["wallpapers"][n] = level["wallpaper"]

        if "config" in level:
            corruption["config"][n] = level["config"]

    write_json(corruption, build.corruption)


# TODO: config.json


def new_pack(source: Source) -> None:
    if source.root.exists():
        logging.error(f"{source.root} already exists")
    else:
        (source.media / "default").mkdir(parents=True, exist_ok=True)
        source.subliminals.mkdir(parents=True, exist_ok=True)
        source.wallpapers.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(DEFAULT_PACK, source.pack)

        logging.info(f"Created a template for a new pack at {source.root}")

    sys.exit()


def upgrade_pack(source: Source) -> None:
    current_time = time.asctime().replace(" ", "_").replace(":", "-")
    backup = source.pack.with_suffix(f".yml.{current_time}.bak")
    shutil.copyfile(source.pack, backup)
    logging.info(f"Created a backup {backup.name} of pack.yml")

    with open(DEFAULT_PACK, "r") as default_f, open(source.pack, "r") as pack_f:
        ruamel_yaml = YAML()
        ruamel_yaml.indent(mapping=2, sequence=4, offset=2)
        ruamel_yaml.preserve_quotes = True

        upgrade = ruamel_yaml.load(default_f)
        original = ruamel_yaml.load(pack_f)

        for a in original:
            if a == "format":
                continue

            for b in original[a]:
                if a == "prompt" and b == "default-prompts":
                    for c in original[a][b]:
                        upgrade[a][b][c] = original[a][b][c]
                else:
                    upgrade[a][b] = original[a][b]

        ruamel_yaml.dump(upgrade, source.pack)

    logging.info(f"Pack format upgraded to {CURRENT_FORMAT}, but some comments may be incorrect, please check default_pack.yml for correct comments")
    sys.exit()


def check_version(source: Source) -> None:
    with open(source.pack, "r") as f:
        pack = yaml.safe_load(f)

        format = pack["format"]
        major, minor = format.split(".")
        current_major, current_minor = CURRENT_FORMAT.split(".")

        if current_major < major or current_minor < minor:
            logging.error(f"Your pack's format {format} is not supported by this version of Pack Tool, please upgrade Pack Tool to the newest version")
            sys.exit()

        if current_major > major or current_minor > minor:
            logging.info(
                f"Your pack's format {format} is outdated (current version is {CURRENT_FORMAT}), please run Pack Tool again with the -u flag to upgrade your pack"
            )
            sys.exit()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="pack source directory")
    parser.add_argument("-o", "--output", default="build", help="output directory name")
    parser.add_argument("-n", "--new", action="store_true", help="create a new pack template and exit")
    parser.add_argument("-u", "--upgrade", action="store_true", help="upgrades an outdated pack format")
    args = parser.parse_args()

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    source = Source(args.source)
    build = Build(args.output)

    if args.new:
        new_pack(source)
    elif not source.root.is_dir():
        logging.error(f"{source.root} does not exist or is not a direcory")
        sys.exit()

    if args.upgrade:
        upgrade_pack(source)

    check_version(source)

    try:
        build.root.mkdir(parents=True, exist_ok=True)
        moods = make_media(source, build)
        make_subliminals(source, build)
        make_wallpapers(source, build)
        make_icon(source, build)
        make_loading_splash(source, build)

        with open(source.pack, "r") as f:
            pack = yaml.safe_load(f)
            make_info(pack, build)
            make_discord(pack, build)
            make_captions(pack, build)
            make_prompt(pack, build)
            make_web(pack, build)
            make_corruption(pack, build, moods)
    except Exception as e:
        logging.error(e)


if __name__ == "__main__":
    main()
