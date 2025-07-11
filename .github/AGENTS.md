# Repository Overview

Tamga is a modern, high-performance Python logging library with colorful console output, multiple output formats, and async capabilities. The project uses modern Python 3.7+ features and achieves 10x performance through buffered writing.

## Python Style Guide

- **Modern Python:** Use Python 3.7+ features including f-strings, type hints, and async/await. Include type hints for public methods.
- **Docstrings:** Focus on what the method does for the user, not implementation details. Keep them concise and user-focused.
- **Performance:** This is a performance-critical library. Always consider buffer efficiency and use cached values (see `_color_cache` pattern).
- **Thread Safety:** All buffer operations must use `self._buffer_lock`. Never let logging errors crash the user's application.
- **Simplicity:** Follow existing patterns in the codebase. New code should match the straightforward style already present.

## Development Guidelines

- **Running Tests:** `python -m unittest tests.test_core -v`
- **Testing Changes:** Test with different buffer sizes (1, 50, 1000) and multiple output formats
- **Color System:** Use only Tailwind CSS color names from `constants.py`
- **Examples:** Update relevant examples in `examples/` when adding features
- **Performance:** For performance changes, include benchmarks in PR description
