import time
from datetime import datetime
from yt_dlp.postprocessor.common import PostProcessor

class SimpleMtimePP(PostProcessor):
    def run(self, info):
        now = time.time()
        self.to_screen("Update Timestamp")
        # Update file timestamp ke waktu sekarang
        self.try_utime(
            info["filepath"],
            atime=now,  # access time
            mtime=now,  # modify time
            errnote="Gagal update timestamp",
        )

        # Atau set ke upload date
        upload_date = info.get("upload_date")
        if upload_date:
            dt = datetime.strptime(upload_date, "%Y%m%d")
            timestamp = dt.timestamp()
            self.try_utime(info["filepath"], timestamp, timestamp)

        return [], info