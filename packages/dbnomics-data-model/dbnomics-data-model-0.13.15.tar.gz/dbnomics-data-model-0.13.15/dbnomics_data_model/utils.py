# dbnomics-data-model -- Define, validate and transform DBnomics data.
# By: Christophe Benz <christophe.benz@cepremap.org>
#
# Copyright (C) 2017-2020 Cepremap
# https://git.nomics.world/dbnomics/dbnomics-data-model
#
# dbnomics-data-model is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# dbnomics-data-model is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


"""Utility functions."""


from typing import Callable, Iterable, Optional, TypeVar

T = TypeVar("T")


def find(predicate: Callable[[T], bool], items: Iterable[T], default=None) -> Optional[T]:
    """Find the first item in ``items`` satisfying ``predicate(item)``.

    Return the found item, or return ``default`` if no item was found.

    >>> find(lambda item: item > 2, [1, 2, 3, 4])
    3
    >>> find(lambda item: item > 10, [1, 2, 3, 4])
    >>> find(lambda item: item > 10, [1, 2, 3, 4], default=42)
    42
    """
    for item in items:
        if predicate(item):
            return item
    return default
