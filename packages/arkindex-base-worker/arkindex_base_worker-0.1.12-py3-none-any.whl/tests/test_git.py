# -*- coding: utf-8 -*-
from pathlib import Path

import pytest

from arkindex_worker.git import GitlabHelper


def test_clone_done(fake_git_helper):
    assert not fake_git_helper.is_clone_finished
    fake_git_helper._clone_done(None, None, None)
    assert fake_git_helper.is_clone_finished


def test_clone(fake_git_helper):
    command = fake_git_helper.run_clone_in_background()
    cmd_str = " ".join(list(map(str, command.cmd)))

    assert "git" in cmd_str
    assert "clone" in cmd_str


def _get_fn_name_from_call(call):
    # call.add(2, 3) => "add"
    return str(call)[len("call.") :].split("(")[0]


def test_save_files(fake_git_helper, mocker):
    mocker.patch("sh.wc", return_value=2)
    fake_git_helper._git = mocker.MagicMock()
    fake_git_helper.is_clone_finished = True
    fake_git_helper.success = True

    fake_git_helper.save_files(Path("/tmp/test_1234/tmp/"))

    expected_calls = ["checkout", "add", "commit", "show", "push"]
    actual_calls = list(map(_get_fn_name_from_call, fake_git_helper._git.mock_calls))

    assert actual_calls == expected_calls
    assert fake_git_helper.gitlab_helper.merge.call_count == 1


def test_save_files__fail_with_failed_clone(fake_git_helper, mocker):
    mocker.patch("sh.wc", return_value=2)
    fake_git_helper._git = mocker.MagicMock()
    fake_git_helper.is_clone_finished = True

    with pytest.raises(Exception) as execinfo:
        fake_git_helper.save_files(Path("/tmp/test_1234/tmp/"))

    assert execinfo.value.args[0] == "Clone was not a success"


def test_merge(mocker):
    api = mocker.MagicMock()
    project = mocker.MagicMock()
    api.projects.get.return_value = project
    merqe_request = mocker.MagicMock()
    project.mergerequests.create.return_value = merqe_request
    mocker.patch("gitlab.Gitlab", return_value=api)

    gitlab_helper = GitlabHelper("project_id", "url", "token", "branch")

    success = gitlab_helper.merge("source", "merge title")

    assert success
    assert project.mergerequests.create.call_count == 1
    assert merqe_request.merge.call_count == 1


def test_merge_request(responses, fake_gitlab_helper_factory):
    project_id = 21259233
    merge_request_id = 7
    source_branch = "new_branch"
    target_branch = "master"
    mr_title = "merge request title"

    responses.add(
        responses.GET,
        "https://gitlab.com/api/v4/projects/balsac_exporter%2Fbalsac-exported-xmls-testing",
        json={
            "id": project_id,
            # several fields omitted
        },
    )

    responses.add(
        responses.POST,
        f"https://gitlab.com/api/v4/projects/{project_id}/merge_requests",
        json={
            "id": 107,
            "iid": merge_request_id,
            "project_id": project_id,
            "title": mr_title,
            "target_branch": target_branch,
            "source_branch": source_branch,
            # several fields omitted
        },
    )

    responses.add(
        responses.PUT,
        f"https://gitlab.com/api/v4/projects/{project_id}/merge_requests/{merge_request_id}/merge",
        json={
            "iid": merge_request_id,
            "state": "merged",
            # several fields omitted
        },
    )

    # the responses are defined in the same order as they are expected to be called
    expected_http_methods = [r.method for r in responses._matches]
    expected_urls = [r.url for r in responses._matches]

    gitlab_helper = fake_gitlab_helper_factory()

    success = gitlab_helper.merge(source_branch, mr_title)

    assert success
    assert len(responses.calls) == 3
    assert [c.request.method for c in responses.calls] == expected_http_methods
    assert [c.request.url for c in responses.calls] == expected_urls


def test_merge_request_fail(responses, fake_gitlab_helper_factory):
    project_id = 21259233
    merge_request_id = 7
    source_branch = "new_branch"
    target_branch = "master"
    mr_title = "merge request title"

    responses.add(
        responses.GET,
        "https://gitlab.com/api/v4/projects/balsac_exporter%2Fbalsac-exported-xmls-testing",
        json={
            "id": project_id,
            # several fields omitted
        },
    )

    responses.add(
        responses.POST,
        f"https://gitlab.com/api/v4/projects/{project_id}/merge_requests",
        json={
            "id": 107,
            "iid": merge_request_id,
            "project_id": project_id,
            "title": mr_title,
            "target_branch": target_branch,
            "source_branch": source_branch,
            # several fields omitted
        },
    )

    responses.add(
        responses.PUT,
        f"https://gitlab.com/api/v4/projects/{project_id}/merge_requests/{merge_request_id}/merge",
        json={"error": "Method not allowed"},
        status=405,
    )

    # the responses are defined in the same order as they are expected to be called
    expected_http_methods = [r.method for r in responses._matches]
    expected_urls = [r.url for r in responses._matches]

    gitlab_helper = fake_gitlab_helper_factory()
    success = gitlab_helper.merge(source_branch, mr_title)

    assert not success
    assert len(responses.calls) == 3
    assert [c.request.method for c in responses.calls] == expected_http_methods
    assert [c.request.url for c in responses.calls] == expected_urls
