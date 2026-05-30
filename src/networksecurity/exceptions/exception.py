import sys

from networksecurity.logging import logger


class NetworkSecurityException(Exception):
    """Custom exception that captures filename and line number from the traceback."""

    def __init__(self, error_message: object, error_details: sys) -> None:
        """Store error location information from the current traceback."""
        self.error_message = error_message
        _, _, exc_tb = error_details.exc_info()

        self.lineno = exc_tb.tb_lineno
        self.file_name = exc_tb.tb_frame.f_code.co_filename

    def __str__(self) -> str:
        """Return a formatted string with script name, line number, and message."""
        return (
            f"Error occured in python script name [{self.file_name}] "
            f"line number [{self.lineno}] "
            f"error message [{self.error_message}]"
        )


if __name__ == "__main__":
    try:
        logger.logging.info("Enter the try block")
        a = 1 / 0
        print("This will not be printed", a)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
