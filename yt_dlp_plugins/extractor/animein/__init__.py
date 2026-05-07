from .animein import (
    AnimeinEpisodeIE,
    AnimeinPlaylistIE,
    AnimeinSearchIE,
)

for _cls in (
    AnimeinEpisodeIE,
    AnimeinPlaylistIE,
    AnimeinSearchIE,
):
    _cls.__module__ = 'yt_dlp_plugins.extractor.animein'
