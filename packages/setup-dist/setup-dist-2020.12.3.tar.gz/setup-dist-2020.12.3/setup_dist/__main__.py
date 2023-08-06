#!/usr/bin/env python
"""usage: python -m setup_dist --dist-dir=<dist_dir>"""
import setuptools
import setup_dist


if __name__ == '__main__':
    setuptools.setup(**setup_dist.get_kwargs())
