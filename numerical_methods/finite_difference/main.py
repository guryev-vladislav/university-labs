#!/usr/bin/env python3

import sys
import os
import signal
import logging

# Add module paths
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'bridge', 'python'))
sys.path.append(os.path.join(current_dir, 'ui'))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


def signal_handler(signum, frame):
    """Global Ctrl+C handler"""
    logger.info("Application termination requested")
    sys.exit(0)


def main():
    """Main application entry point"""
    signal.signal(signal.SIGINT, signal_handler)

    logger.info("Starting differential equations solver application")

    try:
        from ui.interface import SolverApp
        app = SolverApp()
        app.run()
    except KeyboardInterrupt:
        logger.info("Application terminated by user")
    except Exception as e:
        logger.error(f"Application startup failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()