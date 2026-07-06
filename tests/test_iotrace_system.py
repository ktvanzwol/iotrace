from pathlib import Path

import pytest

import iotrace
from iotrace import (
    FileWriteMode,
    IOTraceError,
    LogFileSetting,
    StatusCode,
)

pytestmark = pytest.mark.system


@pytest.fixture()
def _ensure_closed():
    """Guarantee IO Trace is not running and shut down after each test."""
    try:
        iotrace.close_io_trace()
    except IOTraceError:
        pass
    yield
    try:
        iotrace.stop_tracing()
    except IOTraceError:
        pass
    try:
        iotrace.close_io_trace()
    except IOTraceError:
        pass


class TestGetApplicationPath:
    def test_returns_existing_executable(self):
        result = iotrace.get_application_path()
        assert isinstance(result, Path)
        assert result.exists()
        assert result.suffix.lower() == ".exe"


class TestTracingLifecycle:
    def test_start_stop_close(self, _ensure_closed):
        iotrace.launch_io_trace()

        iotrace.start_tracing()
        iotrace.stop_tracing()
        iotrace.close_io_trace()

    def test_log_message_written_to_file(self, _ensure_closed, tmp_path):
        log_file = tmp_path / "trace.txt"

        iotrace.launch_io_trace()

        iotrace.start_tracing(
            log_file_setting=LogFileSetting.PLAIN_TEXT,
            file_path=log_file,
            file_write_mode=FileWriteMode.CREATE_OR_OVERWRITE,
        )

        marker = "iotrace-test-marker"
        iotrace.log_message(marker)
        iotrace.stop_tracing()
        iotrace.close_io_trace()

        contents = log_file.read_text(encoding="utf-8", errors="replace")
        assert marker in contents

    def test_create_only_rejects_existing_file(self, _ensure_closed, tmp_path):
        log_file = tmp_path / "trace.txt"
        log_file.write_text("existing")

        iotrace.launch_io_trace()

        with pytest.raises(IOTraceError) as exc_info:
            iotrace.start_tracing(
                log_file_setting=LogFileSetting.PLAIN_TEXT,
                file_path=log_file,
                file_write_mode=FileWriteMode.CREATE_ONLY,
            )
        assert exc_info.value.status == StatusCode.FAILED_FILE_ALREADY_EXISTS

    def test_rejects_invalid_file(self, _ensure_closed):
        log_file = "none_existing.txt"

        iotrace.launch_io_trace()

        with pytest.raises(IOTraceError) as exc_info:
            iotrace.start_tracing(
                log_file_setting=LogFileSetting.PLAIN_TEXT,
                file_path=log_file,
                file_write_mode=FileWriteMode.CREATE_ONLY,
            )
        assert exc_info.value.status == StatusCode.FAILED_UNABLE_TO_OPEN_LOG_FILE
