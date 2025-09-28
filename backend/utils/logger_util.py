import logging
import sys


class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for different log levels."""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'        # Reset color
    }
    
    def format(self, record):
        # Get the original formatted message
        original = super().format(record)
        
        # Add color to the log level
        if record.levelname in self.COLORS:
            colored_level = f"{self.COLORS[record.levelname]}{record.levelname}{self.COLORS['RESET']}"
            # Replace the level name in the original message with the colored version
            original = original.replace(record.levelname, colored_level)
        
        return original


class CustomLogger:
    """
    A customized logger class that supports console logging with specific format.
    Format includes: filename, line number, and module name.
    """
    
    def __init__(self, module_name: str):
        """
        Initialize the custom logger.
        
        Args:
            module_name (str): Name of the module using this logger
        """
        self.module_name = module_name
        
        # Create logger with module name
        self.logger = logging.getLogger(module_name)
        self.logger.setLevel(logging.DEBUG)
        
        # Prevent duplicate handlers
        if not self.logger.handlers:
            # Create console handler
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.DEBUG)
            
            # Create colored formatter with module name in brackets, filename, line number, and log level
            formatter = ColoredFormatter(
                fmt='%(levelname)s : [%(name)s] - %(filename)s:%(lineno)d - %(message)s'
            )
            
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
    
    def debug(self, message: str):
        """Log debug message."""
        self.logger.debug(message)
    
    def info(self, message: str):
        """Log info message."""
        self.logger.info(message)
    
    def warning(self, message: str):
        """Log warning message."""
        self.logger.warning(message)
    
    def error(self, message: str):
        """Log error message."""
        self.logger.error(message)
    
    def critical(self, message: str):
        """Log critical message."""
        self.logger.critical(message)