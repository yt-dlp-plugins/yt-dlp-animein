import time
from datetime import datetime
from yt_dlp.postprocessor.common import PostProcessor


class SimpleMtimePP(PostProcessor):
    def __init__(self, downloader=None):
        super().__init__(downloader)

    def run(self, info):
        file = info.get("filepath")
        if not file:
            return [], info
        else:
            try:
                self.to_screen("Fix Timestamp")
                timestamp = info.get("timestamp")
                upload_date = info.get("upload_date")
                if timestamp:
                    self.try_utime(file, atime=timestamp, mtime=timestamp)
                elif upload_date:
                    if upload_date:
                        dt = datetime.strptime(upload_date, "%Y%m%d")
                        timestamp = dt.timestamp()
                        self.try_utime(file, atime=timestamp, mtime=timestamp)
                else:
                    now = time.time()
                    self.try_utime(file, atime=now, mtime=now)
            except  Exception as e:
                self.to_screen(f"ERORR: {e}")
        return [], info
                    

