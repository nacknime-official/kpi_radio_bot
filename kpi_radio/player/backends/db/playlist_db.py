from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from consts import config
from utils import db, DateTime
from .._base import LocalPlaylistProviderBase, Playlist, PlaylistItem


def _get_start_time(prev_item: PlaylistItem = None):
    if prev_item:
        return prev_item.stop_time
    return DateTime.now()


class DBPlaylistProvider(LocalPlaylistProviderBase):
    PATH_BASE = config.PATH_STUFF / 'playlists'

    async def get_playlist(self) -> Playlist:
        pl_ = db.Tracklist.get_by_broadcast(*self._broadcast)

        pl: List[PlaylistItem] = []
        for track in pl_:
            pl.append(self.internal_to_playlist_item(
                track, start_time=_get_start_time(pl[-1] if pl else None)
            ))
        return Playlist(pl)

    async def add_track(self, track: PlaylistItem, position: Optional[int]) -> PlaylistItem:
        assert track.track_info is not None, "Local playlist need track info!"
        if position == -2:
            position = 0
        if position == -1:
            position = None
        db.Tracklist.add(
            position, track.path, track.performer, track.title, track.duration,
            track.track_info.user_id, track.track_info.user_name, track.track_info.moderation_id,
            self._broadcast.day, self._broadcast.num
        )
        pl = await self.get_playlist()
        return pl.find_by_path(track.path)[0]

    async def remove_track(self, track_path: Path) -> Optional[PlaylistItem]:
        track = db.Tracklist.remove_track(self._broadcast.day, self._broadcast.num, track_path)
        if not track:
            return None
        return self.internal_to_playlist_item(track)

    async def clear(self):
        db.Tracklist.remove_tracks(self._broadcast.day, self._broadcast.num)

    @staticmethod
    def internal_to_playlist_item(track: db.Tracklist, start_time=None) -> PlaylistItem:
        return PlaylistItem(
            performer=track.track_performer,
            title=track.track_title,
            path=Path(track.track_path),
            duration=track.track_duration,
            start_time=start_time
        ).add_track_info(
            user_id=track.info_user_id,
            user_name=track.info_user_name,
            moderation_msg_id=track.info_message_id
        )
