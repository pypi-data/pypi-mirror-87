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


"""Types and functions manipulating releases metadata."""


import re
from typing import List, Optional, Tuple

from pydantic import BaseModel, Field, validator

from .exceptions import DBnomicsError
from .utils import find

LATEST_RELEASE = "latest"

RELEASE_CODE_PATTERN = r"[-0-9A-Za-z._]+"
RELEASE_CODE_RE = re.compile(RELEASE_CODE_PATTERN)


class NoReleaseError(DBnomicsError):
    def __init__(self, dataset_code: str):
        message = (f"Could not resolve latest release for dataset code {dataset_code!r} "
                   "because no release is defined for this dataset")
        super().__init__(message)
        self.dataset_code = dataset_code


class ReleaseCode(str):
    """Code of a release."""

    def __init__(self, v):
        ReleaseCode.validate(v)
        super().__init__()

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        if RELEASE_CODE_RE.fullmatch(v) is None:
            raise ValueError(
                f"Release code {v!r} does not conform to pattern {RELEASE_CODE_PATTERN!r}")
        return v


class DatasetRelease(BaseModel):
    """Release of a dataset."""

    code: ReleaseCode

    @validator("code")
    def check_not_latest(cls, v):  # noqa
        if v == LATEST_RELEASE:
            raise ValueError(
                f"Release code of a dataset must not be {LATEST_RELEASE!r}")
        return v


class DatasetReleasesItem(BaseModel):
    """Releases of a dataset."""

    dataset_code_prefix: str
    releases: List[DatasetRelease]
    name: Optional[str] = None

    def find_latest_release_code(self) -> ReleaseCode:
        """Find the code of the latest release of this dataset."""
        return self.releases[-1].code

    def format_release(self, release_code: str) -> str:
        return f"{self.dataset_code_prefix}:{release_code}"


class Releases(BaseModel):
    """Releases of datasets."""

    dataset_releases: List[DatasetReleasesItem] = Field(
        [], description='List of dataset releases'
    )

    def find_dataset_releases_item(self, dataset_code_prefix: str) -> Optional[DatasetReleasesItem]:
        """Find the dataset releases item corresponding to the given code prefix."""
        return find(
            lambda item: item.dataset_code_prefix == dataset_code_prefix,
            self.dataset_releases,
        )

    def resolve_release_code(self, dataset_code: str) -> str:
        """Resolve the release code of a dataset.

        Some release codes are reserved, like "latest" that references an actual release code.

        If dataset_code references a reserved release code, replace it by the actual one.
        """
        dataset_code_prefix, release_code = parse_dataset_release(dataset_code)

        if release_code is None or release_code != LATEST_RELEASE:
            return dataset_code

        dataset_releases_item = self.find_dataset_releases_item(dataset_code_prefix)
        if dataset_releases_item is None:
            raise NoReleaseError(dataset_code)

        latest_release_code = dataset_releases_item.find_latest_release_code()
        if latest_release_code is None:
            raise NoReleaseError(dataset_code)

        return dataset_releases_item.format_release(latest_release_code)


def parse_dataset_release(dataset_code: str) -> Tuple[str, Optional[str]]:
    """Parse a dataset code that may contain a release code.

    Return (dataset_code_prefix, release_code).

    >>> parse_dataset_release('foo')
    ('foo', None)
    >>> parse_dataset_release('foo:bar')
    ('foo', 'bar')
    >>> parse_dataset_release('foo:latest')
    ('foo', 'latest')
    >>> parse_dataset_release('foo:')
    Traceback (most recent call last):
        ...
    ValueError: Release code '' does not conform to pattern '[-0-9A-Za-z._]+'
    >>> parse_dataset_release('foo: ')
    Traceback (most recent call last):
        ...
    ValueError: Release code ' ' does not conform to pattern '[-0-9A-Za-z._]+'
    """
    if ":" not in dataset_code:
        return dataset_code, None
    dataset_code_prefix, release_code = dataset_code.split(":", 1)
    release_code = ReleaseCode(release_code)
    return dataset_code_prefix, release_code
