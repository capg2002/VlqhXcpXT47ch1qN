from pathlib import Path

folder = Path("images/IMG_4267_frames")
prefix = "0004_"

for path in folder.iterdir():

    if path.is_file():

        new_name = prefix + path.name

        path.rename(
            path.with_name(new_name)
        )

folder = Path("images/testing3/flip")
prefix = "0005_"

for path in folder.iterdir():

    if path.is_file():

        new_name = prefix + path.name

        path.rename(
            path.with_name(new_name)
        )

folder = Path("images/testing3/notflip")
prefix = "0005_"

for path in folder.iterdir():

    if path.is_file():

        new_name = prefix + path.name

        path.rename(
            path.with_name(new_name)
        )