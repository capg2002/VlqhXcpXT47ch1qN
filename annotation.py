from pathlib import Path

folder = Path("images/testing2/IMG_4028_frames_pt2")
prefix = "0002_"

for path in folder.iterdir():

    if path.is_file():

        new_name = prefix + path.name

        path.rename(
            path.with_name(new_name)
        )

folder = Path("images/testing2/IMG_4029_frames")
prefix = "0003_"

for path in folder.iterdir():

    if path.is_file():

        new_name = prefix + path.name

        path.rename(
            path.with_name(new_name)
        )