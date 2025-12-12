import re
import shutil
from pathlib import Path
from yt_dlp.postprocessor.common import PostProcessor

"""
Fungsi nya buat auto sorting sesuai pattern di bawah,
kalo mau tambahin monggo,
kalo code nya salah, maaf ye,
kalo mau pake wajib pake --restrict-filenames
"""


class AutoSorterPP(PostProcessor):
    def __init__(self, downloader=None):
        super().__init__(downloader)

        self.patterns = {
            r"mine[\s_-]*craft": "Minecraft",
            r"blue[\s_-]*archive": "Blue_Archive",
            r"nigh[\s_-]*tcore": "Nightcore",
            r"hard[\s_-]*style": "Hardstyle",
            r"ultra[\s_-]*funk": "Ultrafunk",
            r"jump[\s_-]*style": "Jumpstyle",
            r"monta[\s_-]*gem": "Montagem",
            r"ah+h?[\s_-]*beat": "Ahh_Beat",
            r"euro[\s_-]*beat": "Eurobeat",
            r"caramell?[\s_-]*dansen": "Caramell_dansen",
            r"hard[\s_-]*tek": "Hardtek",
            r"phonk": "Phonk",
            r"funk": "Funk",
            r"lo[\s_-]*fi": "Lofi",
            r"m[\s_-]*t[\s_-]*g": "Mtg",
        }

    def run(self, info):
        try:
            filepath_str = info.get("filepath")
            if not filepath_str:
                self.to_screen("No filepath found, skipping.")
                return [], info
            filepath = Path(filepath_str)
            base_path = filepath.parent
            filename = filepath.name
            for pattern, new_folder_name in self.patterns.items():
                if re.search(pattern, filename, re.IGNORECASE):
                    target_path = base_path / new_folder_name
                    target_path.mkdir(parents=True, exist_ok=True)
            
                    new_filepath = target_path / filename
                    if new_filepath.exists():
                        self.to_screen(f"{new_filepath} exists, skipping this file.")
                        return [], info
                    else:
                        shutil.move(str(filepath), str(new_filepath))
                        self.to_screen(f"📁 Auto-sorted {filepath} → {new_filepath}")
                        info['filepath'] = str(new_filepath)
                    break
            else:
                self.to_screen("File does not match, skipping sorting")
            return [], info

        except Exception as e:
            self.to_screen(f"ERROR {e}")
            return [], info


# NANAMI ARITUMETO SPEKTAKURUUU YEAYYY 