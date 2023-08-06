# coding=utf-8
import logging

__author__ = 'ThucNC'

import re

_logger = logging.getLogger(__name__)


def find_section(pattern, lines, start_index=0, once=False):
    indices = []
    content = {}
    for i in range(start_index, len(lines)):
        if re.match(pattern, lines[i], re.I):
            indices.append(i)
            for j in range(i + 1, len(lines)):
                if lines[j].startswith('#'):
                    break
                content.setdefault(i, [])
                content[i].append(lines[j])
            if once:
                break

    return indices, content