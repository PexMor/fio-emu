#!/usr/bin/env python
"""Main entry point for FIO emulator."""
import argparse
import sys
from pathlib import Path

# Add parent directory to path if module not found (for development)
_parent_dir = Path(__file__).parent.parent
if str(_parent_dir) not in sys.path:
    sys.path.insert(0, str(_parent_dir))

import uvicorn

from fioemu.app import create_app
from fioemu.config import Config
from fioemu.routers import (
    by_id,
    emu,
    import_,
    last,
    last_statement,
    merchant,
    periods,
    set_last_date,
    set_last_id,
)


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="FIO Banking API Emulator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--host",
        type=str,
        help="Host to bind to (default: from config or 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        help="Port to bind to (default: from config or 8000)",
    )
    parser.add_argument(
        "--config-dir",
        type=str,
        help="Config directory (default: ~/.config/fioemu)",
    )
    parser.add_argument(
        "--examples-dir",
        type=str,
        help="Examples directory (default: config_dir/examples)",
    )

    return parser.parse_args()


def main() -> None:
    """Main entry point."""
    args = parse_args()

    # Load configuration
    config_kwargs = {}
    if args.host:
        config_kwargs["host"] = args.host
    if args.port:
        config_kwargs["port"] = args.port
    if args.config_dir:
        config_kwargs["config_dir"] = args.config_dir
    if args.examples_dir:
        config_kwargs["examples_dir"] = args.examples_dir

    config = Config.load(**config_kwargs)
    config.ensure_directories()

    # Create FastAPI app
    app = create_app(config)

    # Include routers
    app.include_router(emu.router)  # Emulator control endpoints
    app.include_router(periods.router)
    app.include_router(by_id.router)
    app.include_router(last.router)
    app.include_router(set_last_id.router)
    app.include_router(set_last_date.router)
    app.include_router(merchant.router)
    app.include_router(last_statement.router)
    app.include_router(import_.router)

    # Run server
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()
