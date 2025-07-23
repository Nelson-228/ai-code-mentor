import pytest
import sys
import os

# Add the parent directory to the path so we can import cli
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cli import build_parser

def test_cli_flags():
    """Test that --verbose and --color flags are parsed correctly"""
    parser = build_parser()
    args = parser.parse_args(["test_file.py", "--verbose", "--color", "always"])
    
    assert args.verbose is True
    assert args.color == "always"

def test_cli_defaults():
    """Test that default values are set correctly"""
    parser = build_parser()
    args = parser.parse_args(["test_file.py"])
    
    assert args.verbose is False
    assert args.color == "auto"

def test_colorize_function():
    """Test the colorize function"""
    from cli import colorize
    
    # Test with colors enabled
    colored_text = colorize("test", "green", True)
    assert "\033[32m" in colored_text
    assert "\033[0m" in colored_text
    
    # Test with colors disabled
    plain_text = colorize("test", "green", False)
    assert plain_text == "test" 