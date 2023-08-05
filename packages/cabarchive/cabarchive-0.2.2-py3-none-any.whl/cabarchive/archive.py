#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015-2020 Richard Hughes <richard@hughsie.com>
#
# SPDX-License-Identifier: LGPL-2.1+
#
# pylint: disable=protected-access,too-few-public-methods

import fnmatch

from typing import Optional, List

from cabarchive.file import CabFile


class CabArchive(dict):
    """An object representing a Microsoft Cab archive """

    def __init__(self, buf: Optional[bytes] = None, flattern: bool = False):
        """ Parses a MS Cabinet archive """
        dict.__init__(self)

        self.set_id: int = 0

        # load archive
        if buf:
            from cabarchive.parser import _CabArchiveParser

            _CabArchiveParser(self, flattern=flattern).parse(buf)

    def __setitem__(self, key: str, val: CabFile) -> None:
        assert isinstance(key, str)
        assert isinstance(val, CabFile)
        val.filename = key
        dict.__setitem__(self, key, val)

    def parse(self, buf: bytes) -> None:
        """ Parse .cab data """
        from cabarchive.parser import _CabArchiveParser

        _CabArchiveParser(self).parse(buf)

    def find_file(self, glob: str) -> Optional[CabFile]:
        """ Gets a file from the archive using a glob """
        for fn in self:
            if fnmatch.fnmatch(fn, glob):
                return self[fn]
        return None

    def find_files(self, glob: str) -> List[CabFile]:
        """ Gets files from the archive using a glob """
        arr = []
        for fn in self:
            if fnmatch.fnmatch(fn, glob):
                arr.append(self[fn])
        return arr

    def save(self, compress: bool = False, sort: bool = True) -> bytes:
        """ Returns cabinet file data """
        from cabarchive.writer import _CabArchiveWriter

        return _CabArchiveWriter(self, compress=compress, sort=sort).write()

    def __repr__(self) -> str:
        return "CabArchive({})".format([str(self[cabfile]) for cabfile in self])
