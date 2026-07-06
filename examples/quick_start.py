from pathlib import Path

import iotrace

# Launch the application (minimized by default)
iotrace.launch_io_trace()

# Start tracing to a plain-text log file
iotrace.start_tracing(
    log_file_setting=iotrace.LogFileSetting.IO_TRACE,
    file_path=Path.cwd() / "trace.nitrace",
    file_write_mode=iotrace.FileWriteMode.CREATE_OR_OVERWRITE,
)

# Insert a marker into the trace log
iotrace.log_message("Test started")

# ... run your NI driver calls ...

# Stop tracing and leave the application running to inspect the log.
iotrace.stop_tracing()

print("Trace complete. Log file saved to:", Path.cwd() / "trace.nitrace")
