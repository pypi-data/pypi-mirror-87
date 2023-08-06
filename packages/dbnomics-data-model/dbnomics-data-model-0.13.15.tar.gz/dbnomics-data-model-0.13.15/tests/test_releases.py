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


"""Tests for the releases module."""


import pytest
from pydantic import ValidationError

from dbnomics_data_model.releases import Releases


@pytest.fixture
def invalid_release_codes():
    return ["a b", "a ", " a", " a ", "latest", "", " "]


@pytest.fixture
def make_releases_data():
    def _make_releases_data(releases=None):
        return {
            "dataset_releases": [
                {
                    "dataset_code_prefix": "WEO",
                    "name": "World Economic Outlook",
                    "releases": releases or [
                        {
                            "code": "2020-04"
                        },
                        {
                            "code": "2020-10"
                        }
                    ]
                }
            ]
        }

    return _make_releases_data


def test_valid_releases(make_releases_data):
    releases_data = make_releases_data()
    Releases.parse_obj(releases_data)


def test_invalid_releases(make_releases_data, invalid_release_codes):
    for release_code in invalid_release_codes:
        releases_data = make_releases_data(releases=[{"code": release_code}])
        with pytest.raises(ValidationError):
            Releases.parse_obj(releases_data)


def test_find_dataset_releases_item(make_releases_data):
    releases_data = make_releases_data()
    releases = Releases.parse_obj(releases_data)

    dataset_releases_item = releases.find_dataset_releases_item("WEO")
    assert dataset_releases_item is not None
    assert dataset_releases_item.dataset_code_prefix == "WEO"

    dataset_releases_item = releases.find_dataset_releases_item("foo")
    assert dataset_releases_item is None


def test_resolve_release_code(make_releases_data, invalid_release_codes):
    releases_data = make_releases_data()
    releases = Releases.parse_obj(releases_data)

    resolved_dataset_code = releases.resolve_release_code("WEO")
    assert resolved_dataset_code == "WEO"

    resolved_dataset_code = releases.resolve_release_code("WEO:latest")
    assert resolved_dataset_code == "WEO:2020-10"

    with pytest.raises(ValueError):
        for release_code in invalid_release_codes:
            releases.resolve_release_code(f"WEO:{release_code}")
