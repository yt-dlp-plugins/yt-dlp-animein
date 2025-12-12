
import re
from pathlib import Path
from yt_dlp.postprocessor.common import PostProcessor

"""
ya gw tau tinggal pake --restrict-filenames,
tapi gw ga suka, soalnya pasti bakalan ada _-_ jadi jelek
jadi gw bikin custom prosesor sendiri, OKAY!.
tapi kalo [C++ something] bakal jadi [C_something]
sorry kalo nama" variaable nya aneh
"""

class CleanNamePP(PostProcessor):
    def __init__(self, downloader=None):
        super().__init__(downloader)

    def run(self, info):
        self.to_screen("Processing filename cleanup...")
        # Nama lama
        old_name = Path(info.get("filepath"))
        # nama tanpa ekstensi
        dirty_name = old_name.stem

        clean_name = re.sub(r"[+=><\-|&$@#%^*()\[\]{}._]", "_", dirty_name)
        
        new_name = re.sub(r"[\s_]+", "_", clean_name)
        
        new_clean_name = new_name.strip(" -_.")

        try:
            if not old_name:
                return [], info
            else:
                if new_clean_name != old_name:
                    new_name = old_name.with_name(f"{new_clean_name}{old_name.suffix}")
                    old_name.rename(new_name)
                    info['filepath'] = str(new_name)
                    self.to_screen(f"Renaming {old_name} → {new_name}")
                    return [], info
        except Exception as e:
            self.to_screen(f"[CleanNamePP] ERORR: {e}")
            return [], info