"""Format writers.

Each writer exposes ``write_<format>(report, raws, displays, options) -> bytes``
and imports its optional dependency lazily so that exportkit itself stays
dependency-free.
"""
