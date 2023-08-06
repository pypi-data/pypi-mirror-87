# -*- coding: utf-8 -*-
import logging
import os
import sys
from pathlib import Path

import gnupg
import pytest

from arkindex.mock import MockApiClient
from arkindex_worker import logger
from arkindex_worker.worker import BaseWorker


def test_init_default_local_share():
    worker = BaseWorker()

    assert worker.work_dir == os.path.expanduser("~/.local/share/arkindex")
    assert worker.worker_version_id == "12341234-1234-1234-1234-123412341234"


def test_init_default_xdg_data_home(monkeypatch):
    path = str(Path(__file__).absolute().parent)
    monkeypatch.setenv("XDG_DATA_HOME", path)
    worker = BaseWorker()

    assert worker.work_dir == f"{path}/arkindex"
    assert worker.worker_version_id == "12341234-1234-1234-1234-123412341234"


def test_init_var_ponos_data_given(monkeypatch):
    path = str(Path(__file__).absolute().parent)
    monkeypatch.setenv("PONOS_DATA", path)
    worker = BaseWorker()

    assert worker.work_dir == f"{path}/current"
    assert worker.worker_version_id == "12341234-1234-1234-1234-123412341234"


def test_init_var_worker_version_id_missing(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["worker"])
    monkeypatch.delenv("WORKER_VERSION_ID")
    worker = BaseWorker()
    worker.configure()
    assert worker.worker_version_id is None
    assert worker.is_read_only is True
    assert worker.config == {}  # default empty case


def test_init_var_worker_local_file(monkeypatch, tmp_path):
    # Build a dummy yaml config file
    config = tmp_path / "config.yml"
    config.write_text("---\nlocalKey: abcdef123")

    monkeypatch.setattr(sys, "argv", ["worker", "-c", str(config)])
    monkeypatch.delenv("WORKER_VERSION_ID")
    worker = BaseWorker()
    worker.configure()
    assert worker.worker_version_id is None
    assert worker.is_read_only is True
    assert worker.config == {"localKey": "abcdef123"}  # Use a local file for devs

    config.unlink()


def test_cli_default(mocker, mock_worker_version_api):
    worker = BaseWorker()
    spy = mocker.spy(worker, "add_arguments")
    assert not spy.called
    assert logger.level == logging.NOTSET
    assert not hasattr(worker, "api_client")

    mocker.patch.object(sys, "argv", ["worker"])
    worker.configure()

    assert spy.called
    assert spy.call_count == 1
    assert not worker.args.verbose
    assert logger.level == logging.NOTSET
    assert worker.api_client
    assert worker.worker_version_id == "12341234-1234-1234-1234-123412341234"
    assert worker.is_read_only is False
    assert worker.config == {"someKey": "someValue"}  # from API

    logger.setLevel(logging.NOTSET)


def test_cli_arg_verbose_given(mocker, mock_worker_version_api):
    worker = BaseWorker()
    spy = mocker.spy(worker, "add_arguments")
    assert not spy.called
    assert logger.level == logging.NOTSET
    assert not hasattr(worker, "api_client")

    mocker.patch.object(sys, "argv", ["worker", "-v"])
    worker.configure()

    assert spy.called
    assert spy.call_count == 1
    assert worker.args.verbose
    assert logger.level == logging.DEBUG
    assert worker.api_client
    assert worker.worker_version_id == "12341234-1234-1234-1234-123412341234"
    assert worker.is_read_only is False
    assert worker.config == {"someKey": "someValue"}  # from API

    logger.setLevel(logging.NOTSET)


def test_load_missing_secret():
    worker = BaseWorker()
    worker.api_client = MockApiClient()

    with pytest.raises(
        Exception, match="Secret missing/secret is not available on the API nor locally"
    ):
        worker.load_secret("missing/secret")


def test_load_remote_secret():
    worker = BaseWorker()
    worker.api_client = MockApiClient()
    worker.api_client.add_response(
        "RetrieveSecret",
        name="testRemote",
        response={"content": "this is a secret value !"},
    )

    assert worker.load_secret("testRemote") == "this is a secret value !"

    # The one mocked call has been used
    assert len(worker.api_client.history) == 1
    assert len(worker.api_client.responses) == 0


def test_load_json_secret():
    worker = BaseWorker()
    worker.api_client = MockApiClient()
    worker.api_client.add_response(
        "RetrieveSecret",
        name="path/to/file.json",
        response={"content": '{"key": "value", "number": 42}'},
    )

    assert worker.load_secret("path/to/file.json") == {
        "key": "value",
        "number": 42,
    }

    # The one mocked call has been used
    assert len(worker.api_client.history) == 1
    assert len(worker.api_client.responses) == 0


def test_load_yaml_secret():
    worker = BaseWorker()
    worker.api_client = MockApiClient()
    worker.api_client.add_response(
        "RetrieveSecret",
        name="path/to/file.yaml",
        response={
            "content": """---
somekey: value
aList:
  - A
  - B
  - C
struct:
 level:
   X
"""
        },
    )

    assert worker.load_secret("path/to/file.yaml") == {
        "aList": ["A", "B", "C"],
        "somekey": "value",
        "struct": {"level": "X"},
    }

    # The one mocked call has been used
    assert len(worker.api_client.history) == 1
    assert len(worker.api_client.responses) == 0


def test_load_local_secret(monkeypatch, tmpdir):
    # Setup arkindex config dir in a temp directory
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmpdir))

    # Write a dummy secret
    secrets_dir = tmpdir / "arkindex" / "secrets"
    os.makedirs(secrets_dir)
    secret = secrets_dir / "testLocal"
    secret.write_text("this is a local secret value", encoding="utf-8")

    # Mock GPG decryption
    class GpgDecrypt(object):
        def __init__(self, fd):
            self.ok = True
            self.data = fd.read()

    monkeypatch.setattr(gnupg.GPG, "decrypt_file", lambda gpg, f: GpgDecrypt(f))

    worker = BaseWorker()
    worker.api_client = MockApiClient()

    assert worker.load_secret("testLocal") == "this is a local secret value"

    # The remote api is checked first
    assert len(worker.api_client.history) == 1
    assert worker.api_client.history[0].operation == "RetrieveSecret"
