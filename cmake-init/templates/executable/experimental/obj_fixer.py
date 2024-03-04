import argparse
from pathlib import Path
import shutil

OBJ_EXT = ".obj"
MSVC_MODULE_EXT = ".ixx"
MSVC_MODULE_OBJ_EXT = f"{MSVC_MODULE_EXT}{OBJ_EXT}"


def parse_args() -> str:
    parser = argparse.ArgumentParser(
        description="Changes the file extension of object files produced by modules in MSVC."
    )

    parser.add_argument("build_dir")
    parser.add_argument("target")
    parser.add_argument("config_type")

    args = parser.parse_args()

    return f"{args.build_dir}/{args.target}.dir/{args.config_type}"


def replace_extension(path: Path, prev: str, new: str) -> Path:
    return Path(str(path).replace(prev, new))


def main():
    dir = parse_args()

    print(f"Searching for {MSVC_MODULE_OBJ_EXT} files in:\n{dir}")

    obj_files = Path(dir).glob("*.ixx.obj")
    for obj_file in obj_files:
        old_obj_file_path = Path(obj_file)
        new_obj_file_path = replace_extension(
            old_obj_file_path, MSVC_MODULE_OBJ_EXT, OBJ_EXT
        )
        print(f"Copying: {old_obj_file_path} -> {new_obj_file_path}")
        shutil.copy2(old_obj_file_path, new_obj_file_path)


if __name__ == "__main__":
    main()
