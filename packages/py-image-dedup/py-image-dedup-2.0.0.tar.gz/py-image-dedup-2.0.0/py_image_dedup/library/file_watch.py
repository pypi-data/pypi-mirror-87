import re
from pathlib import Path

from watchdog.events import FileSystemEventHandler, EVENT_TYPE_MODIFIED, EVENT_TYPE_MOVED, EVENT_TYPE_CREATED, \
    EVENT_TYPE_DELETED

from py_image_dedup.config import DeduplicatorConfig
from py_image_dedup.stats import FILE_EVENT_COUNT
from py_image_dedup.util import echo


class EventHandler(FileSystemEventHandler):

    def __init__(self, processing_manager):
        super().__init__()
        self.processing_manager = processing_manager

        self.config = DeduplicatorConfig()

        self.directory_regex = re.compile(rf"^({'|'.join(list(map(str, self.config.SOURCE_DIRECTORIES.value)))}).*$")
        self.file_regex = re.compile(rf"^.*({'|'.join(self.config.FILE_EXTENSION_FILTER.value)})$", re.IGNORECASE)

    def on_any_event(self, event):
        if not self._event_matches_filter(event):
            return

        FILE_EVENT_COUNT.labels(type=event.event_type).inc()

        echo("FileSystemEvent: {} {} {}".format(event.event_type,
                                                "directory" if event.is_directory else "file",
                                                event.src_path))

        _actions = {
            EVENT_TYPE_CREATED: self.created,
            EVENT_TYPE_MODIFIED: self.modified,
            EVENT_TYPE_MOVED: self.moved,
            EVENT_TYPE_DELETED: self.deleted,
        }
        _actions[event.event_type](event)

    def created(self, event):
        self._process(event.src_path)

    def modified(self, event):
        self._process(event.src_path)

    def moved(self, event):
        self._cleanup(event.src_path)
        self._process(event.dest_path)

    def deleted(self, event):
        self._cleanup(event.src_path)

    def _process(self, path: str):
        self.processing_manager.add(Path(path))

    def _cleanup(self, path: str):
        self.processing_manager.remove(Path(path))

    def _event_matches_filter(self, event) -> bool:
        if event.is_directory:
            return False
        else:
            result = bool(self.directory_regex.match(event.src_path))
            result &= bool(self.file_regex.match(event.src_path))
        return result
