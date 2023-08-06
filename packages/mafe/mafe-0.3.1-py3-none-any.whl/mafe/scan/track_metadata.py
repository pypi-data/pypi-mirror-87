__author__ = 'Lene Preuss <lene.preuss@gmail.com>'

from typing import Tuple

import audio_metadata

from .types import Metadata

METADATA_COLUMNS = ('artist', 'title', 'album')


def read_track_metadata(file_name: str) -> Metadata:
    try:
        metadata = audio_metadata.load(file_name)
        return dict(_extract_tag(metadata, tag) for tag in METADATA_COLUMNS)
    except audio_metadata.AudioMetadataException as problem:
        raise RuntimeError from problem


def _extract_tag(metadata: audio_metadata.Format, tag: str) -> Tuple[str, str]:
    return tag, metadata['tags'].get(tag, ['...'])[0]
