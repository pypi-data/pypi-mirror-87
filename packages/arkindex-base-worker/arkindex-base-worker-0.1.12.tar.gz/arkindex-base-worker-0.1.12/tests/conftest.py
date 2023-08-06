# -*- coding: utf-8 -*-
import json
import os
import sys
from pathlib import Path

import pytest

from arkindex.mock import MockApiClient
from arkindex_worker.git import GitHelper, GitlabHelper
from arkindex_worker.worker import ElementsWorker

FIXTURES_DIR = Path(__file__).resolve().parent / "data"


@pytest.fixture(autouse=True)
def setup_api(responses, monkeypatch):

    # Always use the environment variable first
    schema_url = os.environ.get("ARKINDEX_API_SCHEMA_URL")
    if schema_url is None:
        # Try to load a local schema as the current developer of base-worker
        # may also work on the backend nearby
        paths = [
            "~/dev/ark/backend/schema.yml",
            "~/dev/ark/backend/output/schema.yml",
        ]
        for path in paths:
            path = Path(path).expanduser().absolute()
            if path.exists():
                monkeypatch.setenv("ARKINDEX_API_SCHEMA_URL", str(path))
                schema_url = str(path)
                break

    # Fallback to prod environment
    if schema_url is None:
        schema_url = "https://arkindex.teklia.com/api/v1/openapi/?format=openapi-json"
        monkeypatch.setenv("ARKINDEX_API_SCHEMA_URL", schema_url)

    # Allow accessing remote API schemas
    responses.add_passthru(schema_url)

    # Force api requests on a dummy server with dummy credentials
    monkeypatch.setenv("ARKINDEX_API_URL", "http://testserver/api/v1")
    monkeypatch.setenv("ARKINDEX_API_TOKEN", "unittest1234")


@pytest.fixture(autouse=True)
def give_worker_version_id_env_variable(monkeypatch):
    monkeypatch.setenv("WORKER_VERSION_ID", "12341234-1234-1234-1234-123412341234")


@pytest.fixture
def mock_worker_version_api(responses):
    """Provide a mock API response to get worker configuration"""
    payload = {
        "id": "12341234-1234-1234-1234-123412341234",
        "configuration": {
            "docker": {"image": "python:3"},
            "configuration": {"someKey": "someValue"},
            "secrets": [],
        },
        "revision": {
            "hash": "deadbeef1234",
            "name": "some git revision",
        },
        "docker_image": "python:3",
        "docker_image_name": "python:3",
        "state": "created",
        "worker": {
            "id": "deadbeef-1234-5678-1234-worker",
            "name": "Fake worker",
            "slug": "fake_worker",
            "type": "classifier",
        },
    }
    responses.add(
        responses.GET,
        "http://testserver/api/v1/workers/versions/12341234-1234-1234-1234-123412341234/",
        status=200,
        body=json.dumps(payload),
        content_type="application/json",
    )


@pytest.fixture
def mock_elements_worker(monkeypatch, mock_worker_version_api):
    """Build and configure an ElementsWorker with fixed CLI parameters to avoid issues with pytest"""
    monkeypatch.setattr(sys, "argv", ["worker"])

    worker = ElementsWorker()
    worker.configure()
    return worker


@pytest.fixture
def fake_page_element():
    with open(FIXTURES_DIR / "page_element.json", "r") as f:
        return json.load(f)


@pytest.fixture
def fake_ufcn_worker_version():
    with open(FIXTURES_DIR / "ufcn_line_historical_worker_version.json", "r") as f:
        return json.load(f)


@pytest.fixture
def fake_transcriptions_small():
    with open(FIXTURES_DIR / "line_transcriptions_small.json", "r") as f:
        return json.load(f)


@pytest.fixture
def fake_dummy_worker():
    api_client = MockApiClient()
    worker = ElementsWorker()
    worker.api_client = api_client
    return worker


@pytest.fixture
def fake_git_helper(mocker):
    gitlab_helper = mocker.MagicMock()
    return GitHelper(
        "repo_url",
        "/tmp/git_test/foo/",
        "/tmp/test/path/",
        "tmp_workflow_id",
        gitlab_helper,
    )


@pytest.fixture
def fake_gitlab_helper_factory():
    # have to set up the responses, before creating the client
    def run():
        return GitlabHelper(
            "balsac_exporter/balsac-exported-xmls-testing",
            "https://gitlab.com",
            "<GITLAB_TOKEN>",
            "gitlab_branch",
        )

    return run
