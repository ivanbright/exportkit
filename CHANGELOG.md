# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/) and
[Semantic Versioning](https://semver.org/).

## [0.1.1] - 2026-10-14

### Fixed
- Excel export now accepts timezone-aware datetimes (Excel has no time-zone
  support); aware values are converted to UTC and made naive. Unsupported cell
  types fall back to their string representation.

## [0.1.0] - 2026-10-14

### Added
- `Report` and `Column` declarative data model (sequence or mapping rows).
- `render` / `render_to` entry points returning bytes or writing to a path/stream.
- `Format` enum with extension, MIME type and tolerant `coerce` (names,
  extensions, aliases and MIME types).
- Excel writer (openpyxl), Word writer (python-docx) and PDF writer (fpdf2),
  each behind an optional extra.
- Optional-dependency errors that explain which extra to install.
