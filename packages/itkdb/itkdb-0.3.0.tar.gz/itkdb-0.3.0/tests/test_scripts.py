import pytest

import sys, os

sys.path.append(os.path.realpath(os.path.dirname(__file__) + "/.."))

import getInventory

import betamax

import itkdb

try:
    from types import SimpleNamespace
except:
    from argparse import Namespace as SimpleNamespace


@pytest.mark.parametrize(
    "param",
    [
        ("listInstitutions", "INST"),
        ("listComponentTypes", None),
        ("listInventory", None),
        ("trashUnassembled", None),
    ],
    ids=["listInstitutions", "listComponentTypes", "listInventory", "trashUnassembled"],
)
def test_getInventory(auth_client, param):
    command, institution = param
    args = SimpleNamespace(
        command=command,
        componentType=None,
        includeTrashed=False,
        institution=institution,
        project='S',
        savePath=None,
        useCurrentLocation=False,
    )
    with betamax.Betamax(
        auth_client, cassette_library_dir=itkdb.settings.ITKDB_CASSETTE_LIBRARY_DIR
    ) as recorder:
        recorder.use_cassette(
            'test_scripts.test_getInventory.{0:s}'.format(command), record='once'
        )
        inventory = getInventory.Inventory(args, auth_client)
        assert inventory.main()
