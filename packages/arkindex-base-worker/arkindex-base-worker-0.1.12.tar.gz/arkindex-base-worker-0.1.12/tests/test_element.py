# -*- coding: utf-8 -*-
import pytest
from requests import HTTPError

from arkindex_worker.models import Element


def test_no_image_url():
    url = Element({"zone": None}).image_url()
    assert not url


def test_image_url_iiif():
    url = Element({"zone": {"image": {"url": "http://something/"}}}).image_url()
    assert url == "http://something/full/full/0/default.jpg"


def test_image_url_iiif_resize():
    url = Element({"zone": {"image": {"url": "http://something/"}}}).image_url(500)
    assert url == "http://something/full/500/0/default.jpg"


def test_image_url_iiif_append_slash():
    url = Element({"zone": {"image": {"url": "http://something"}}}).image_url()
    assert url == "http://something/full/full/0/default.jpg"


def test_image_url_s3():
    url = Element(
        {
            "zone": {
                "image": {"s3_url": "http://s3/something", "url": "http://something/"}
            }
        }
    ).image_url()
    assert url == "http://s3/something"


def test_image_url_s3_resize():
    url = Element(
        {
            "zone": {
                "image": {"s3_url": "http://s3/something", "url": "http://something/"}
            }
        }
    ).image_url(500)
    assert url == "http://s3/something"


def test_open_image(mocker):
    open_mock = mocker.patch(
        "arkindex_worker.models.open_image", return_value="an image!"
    )
    elt = Element(
        {
            "zone": {
                "image": {
                    "url": "http://something",
                    "server": {"max_width": None, "max_height": None},
                },
                "polygon": [[0, 0], [181, 0], [181, 240], [0, 240], [0, 0]],
            }
        }
    )
    assert elt.open_image() == "an image!"
    assert open_mock.call_count == 1
    assert open_mock.call_args == mocker.call(
        "http://something/full/full/0/default.jpg"
    )


def test_open_image_resize_portrait(mocker):
    open_mock = mocker.patch(
        "arkindex_worker.models.open_image", return_value="an image!"
    )
    elt = Element(
        {
            "zone": {
                "image": {
                    "url": "http://something",
                    "width": 400,
                    "height": 600,
                    "server": {"max_width": None, "max_height": None},
                },
                "polygon": [[0, 0], [400, 0], [400, 600], [0, 600], [0, 0]],
            }
        }
    )
    # Resize = original size
    assert elt.open_image(max_size=600) == "an image!"
    assert open_mock.call_count == 1
    assert open_mock.call_args == mocker.call(
        "http://something/full/full/0/default.jpg"
    )
    # Resize = smaller height
    assert elt.open_image(max_size=400) == "an image!"
    assert open_mock.call_count == 2
    assert open_mock.call_args == mocker.call(
        "http://something/full/266,400/0/default.jpg"
    )
    # Resize = bigger height
    assert elt.open_image(max_size=800) == "an image!"
    assert open_mock.call_count == 3
    assert open_mock.call_args == mocker.call(
        "http://something/full/full/0/default.jpg"
    )


def test_open_image_resize_partial_element(mocker):
    open_mock = mocker.patch(
        "arkindex_worker.models.open_image", return_value="an image!"
    )
    elt = Element(
        {
            "zone": {
                "image": {
                    "url": "http://something",
                    "width": 400,
                    "height": 600,
                    "server": {"max_width": None, "max_height": None},
                },
                "polygon": [[0, 0], [200, 0], [200, 600], [0, 600], [0, 0]],
            }
        }
    )
    assert elt.open_image(max_size=400) == "an image!"
    assert open_mock.call_count == 1
    assert open_mock.call_args == mocker.call(
        "http://something/full/full/0/default.jpg"
    )


def test_open_image_resize_landscape(mocker):
    open_mock = mocker.patch(
        "arkindex_worker.models.open_image", return_value="an image!"
    )
    elt = Element(
        {
            "zone": {
                "image": {
                    "url": "http://something",
                    "width": 600,
                    "height": 400,
                    "server": {"max_width": None, "max_height": None},
                },
                "polygon": [[0, 0], [600, 0], [600, 400], [0, 400], [0, 0]],
            }
        }
    )
    # Resize = original size
    assert elt.open_image(max_size=600) == "an image!"
    assert open_mock.call_count == 1
    assert open_mock.call_args == mocker.call(
        "http://something/full/full/0/default.jpg"
    )
    # Resize = smaller width
    assert elt.open_image(max_size=400) == "an image!"
    assert open_mock.call_count == 2
    assert open_mock.call_args == mocker.call(
        "http://something/full/400,266/0/default.jpg"
    )
    # Resize = bigger width
    assert elt.open_image(max_size=800) == "an image!"
    assert open_mock.call_count == 3
    assert open_mock.call_args == mocker.call(
        "http://something/full/full/0/default.jpg"
    )


def test_open_image_resize_square(mocker):
    open_mock = mocker.patch(
        "arkindex_worker.models.open_image", return_value="an image!"
    )
    elt = Element(
        {
            "zone": {
                "image": {
                    "url": "http://something",
                    "width": 400,
                    "height": 400,
                    "server": {"max_width": None, "max_height": None},
                },
                "polygon": [[0, 0], [400, 0], [400, 400], [0, 400], [0, 0]],
            }
        }
    )
    # Resize = original size
    assert elt.open_image(max_size=400) == "an image!"
    assert open_mock.call_count == 1
    assert open_mock.call_args == mocker.call(
        "http://something/full/full/0/default.jpg"
    )
    # Resize = smaller
    assert elt.open_image(max_size=200) == "an image!"
    assert open_mock.call_count == 2
    assert open_mock.call_args == mocker.call(
        "http://something/full/200,200/0/default.jpg"
    )
    # Resize = bigger
    assert elt.open_image(max_size=800) == "an image!"
    assert open_mock.call_count == 3
    assert open_mock.call_args == mocker.call(
        "http://something/full/full/0/default.jpg"
    )


def test_open_image_resize_tiles(mocker):
    mocker.patch("arkindex_worker.models.open_image", return_value="an image!")
    elt = Element(
        {
            "zone": {
                "image": {
                    "url": "http://something",
                    "server": {"max_width": 600, "max_height": 600},
                },
                "polygon": [[0, 0], [800, 0], [800, 800], [0, 800], [0, 0]],
            }
        }
    )
    with pytest.raises(NotImplementedError):
        elt.open_image(max_size=400)


def test_open_image_requires_zone():
    with pytest.raises(ValueError) as e:
        Element({"id": "42"}).open_image()
    assert str(e.value) == "Element 42 has no zone"


def test_open_image_s3(mocker):
    open_mock = mocker.patch(
        "arkindex_worker.models.open_image", return_value="an image!"
    )
    elt = Element(
        {"zone": {"image": {"url": "http://something", "s3_url": "http://s3url"}}}
    )
    assert elt.open_image() == "an image!"
    assert open_mock.call_count == 1
    assert open_mock.call_args == mocker.call("http://s3url")


def test_open_image_s3_retry(mocker):
    response_mock = mocker.MagicMock()
    response_mock.status_code = 403
    mocker.patch(
        "arkindex_worker.models.open_image",
        return_value="an image!",
        side_effect=HTTPError(response=response_mock),
    )

    elt = Element(
        {
            "id": "cafe",
            "zone": {"image": {"url": "http://something", "s3_url": "http://oldurl"}},
        }
    )

    with pytest.raises(NotImplementedError):
        elt.open_image()


def test_open_image_s3_retry_once(mocker):
    response_mock = mocker.MagicMock()
    response_mock.status_code = 403
    mocker.patch(
        "arkindex_worker.models.open_image",
        side_effect=HTTPError(response=response_mock),
    )
    elt = Element(
        {
            "id": "cafe",
            "zone": {"image": {"url": "http://something", "s3_url": "http://oldurl"}},
        }
    )

    with pytest.raises(NotImplementedError):
        elt.open_image()
