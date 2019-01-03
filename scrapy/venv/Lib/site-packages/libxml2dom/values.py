#!/usr/bin/env python

"""
Python value emulation.

Copyright (C) 2008 Paul Boddie <paul@boddie.org.uk>

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU Lesser General Public License as published by the Free
Software Foundation; either version 3 of the License, or (at your option) any
later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
details.

You should have received a copy of the GNU Lesser General Public License along
with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

class ContentValue:

    """
    Equality support for nodes having contents which should have some
    interoperability with normal Python objects.
    """

    def __eq__(self, other):
        if hasattr(other, "contents"):
            return self.contents == other.contents
        else:
            return self.contents == other

    def __ne__(self, other):
        return not self.__eq__(other)

class SequenceValue:

    """
    Equality and access support for nodes having sequence-like contents.
    """

    def __eq__(self, other):
        for i, j in map(None, self, other):
            if i != j:
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __len__(self):
        return len(self.values())

    def __getitem__(self, i):
        return self.values()[i]

# vim: tabstop=4 expandtab shiftwidth=4
