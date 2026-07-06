import argparse
import sys

import iotrace


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="iotrace",
        description="Control NI IO Trace from the command line.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # start
    start_parser = subparsers.add_parser("start", help="Start tracing driver calls.")
    start_parser.add_argument(
        "--log-format",
        choices=["none", "io-trace", "plain-text", "csv", "xml"],
        default="none",
        help="Log file format (default: none).",
    )
    start_parser.add_argument(
        "--file",
        default=None,
        help="Path to the log file.",
    )
    start_parser.add_argument(
        "--write-mode",
        choices=["create", "append", "overwrite"],
        default="create",
        help="File write mode (default: create).",
    )

    # stop
    stop_parser = subparsers.add_parser("stop", help="Stop tracing driver calls.")
    stop_parser.add_argument(
        "--close",
        action="store_true",
        help="Close NI IO Trace after stopping.",
    )

    args = parser.parse_args(argv)

    try:
        if args.command == "start":
            iotrace.launch_io_trace(window_state=iotrace.WindowState.MINIMIZED)
            log_format_map = {
                "none": iotrace.LogFileSetting.NO_FILE,
                "io-trace": iotrace.LogFileSetting.IO_TRACE,
                "plain-text": iotrace.LogFileSetting.PLAIN_TEXT,
                "csv": iotrace.LogFileSetting.COMMA_SEPARATED,
                "xml": iotrace.LogFileSetting.XML,
            }
            write_mode_map = {
                "create": iotrace.FileWriteMode.CREATE_ONLY,
                "append": iotrace.FileWriteMode.CREATE_OR_APPEND,
                "overwrite": iotrace.FileWriteMode.CREATE_OR_OVERWRITE,
            }
            iotrace.start_tracing(
                log_file_setting=log_format_map[args.log_format],
                file_path=args.file,
                file_write_mode=write_mode_map[args.write_mode],
            )
            print("Tracing started.")

        elif args.command == "stop":
            iotrace.stop_tracing()
            print("Tracing stopped.")
            if args.close:
                iotrace.close_io_trace()
                print("NI IO Trace closed.")

    except iotrace.IOTraceError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
