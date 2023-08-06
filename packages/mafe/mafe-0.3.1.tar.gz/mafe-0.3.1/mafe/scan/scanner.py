__author__ = 'Lene Preuss <lene.preuss@gmail.com>'

from pathlib import Path
from shutil import get_terminal_size
from typing import List, Optional

from zlib import error as zlib_error
from audioread.exceptions import NoBackendError
import magic
import pandas as pd

from .track_data import TrackData, TrackTooLong
from .track_data_storage import DEFAULT_STORE_EVERY, TrackDataStorage

AUDIO_EXTENSIONS = ('mp3', 'ogg', 'flac', 'wav', 'm4a', 'aif', 'aiff')
RED = '\033[91m'
NORMAL = '\033[0m'


class Scanner:

    def __init__(
            self, file_name: str, base_folders: List[str], quiet: bool,
            store_every: int = DEFAULT_STORE_EVERY
    ) -> None:
        self.csv_file = file_name
        self.files = [
            file for folder in base_folders
            for file in Path(folder).rglob('*')
            if file.is_file()
            if is_audio(file)
        ]
        self.quiet = quiet
        self.store_every = store_every
        self.done = 0
        self.failed = 0
        self.interrupted = False

    def run(self) -> pd.DataFrame:
        with TrackDataStorage(Path(self.csv_file), self.quiet, self.store_every) as storage:
            try:
                for track in sorted(self.files):
                    self.process_track(storage, track)
            except KeyboardInterrupt:
                pass
        return storage.tracks

    def process_track(self, storage: TrackDataStorage, track: Path) -> None:
        try:
            features = TrackData(storage, track)
        except (
                FileNotFoundError, IndexError, NoBackendError, TrackTooLong,
                UnicodeEncodeError, UserWarning, ValueError, ZeroDivisionError, zlib_error
        ) as problem:
            self.log_problem(track, problem)
            return
        except KeyboardInterrupt:
            if self.interrupted:
                raise
            print(
                f"{RED}Interrupting {track}.{NORMAL} "
                f"A second keyboard interrupt will terminate the scan.")
            self.interrupted = True
            features = None

        self.done += 1
        self.store_track(storage, features)

    def log_problem(self, track: Path, problem: Exception) -> None:
        self.failed += 1
        track_part = track.name.encode('utf-8', 'surrogateescape').decode('utf-8', 'replace')
        problem_part = f"{type(problem).__name__}: {problem}"
        progress = self.progress()
        length = len(problem_part) + len(progress) + 7
        self.print(
            f"{cut(track_part, term_width() - length)} "
            f"{RED}{problem_part}{NORMAL}   [{progress}]"
        )

    def store_track(self, storage: TrackDataStorage, track: Optional[TrackData]) -> None:
        if track is None:
            return
        self.print_info(track)
        storage.add_track(track)

    def print_info(self, track: TrackData) -> None:
        hash_part = track.data_frame.iloc[0]['hash'][:8]
        duration = f"{int(track.data_frame.iloc[0]['duration']):4}s"
        tempo = f"{int(track.data_frame.iloc[0]['tempo']):3}BPM"
        progress = self.progress()
        length = len(hash_part) + len(duration) + len(tempo) + len(progress) + 9
        self.print(
            f"{cut(track.data_frame.iloc[0]['file_name'], term_width() - length)} "
            f"{hash_part} {duration}@{tempo}   [{progress}]"
        )

    def progress(self) -> str:
        return f"{self.done:3} ok/{self.failed:2} fail/ {len(self.files)} tot"

    def print(self, *args, **kwargs):
        if not self.quiet:
            print(*args, **kwargs)


def is_audio(track: Path):
    if track.suffix[1:].lower() in AUDIO_EXTENSIONS:
        return True
    file_magic = magic.from_file(str(track), mime=True)
    return file_magic.startswith('audio/')


def cut(string: str, length: int, min_width: int = 10) -> str:
    if len(string) <= length:
        return string.ljust(length)
    length = max(length, min_width)
    return string[:length - 3] + '...'


def term_width() -> int:
    return get_terminal_size((80, 20))[0]
