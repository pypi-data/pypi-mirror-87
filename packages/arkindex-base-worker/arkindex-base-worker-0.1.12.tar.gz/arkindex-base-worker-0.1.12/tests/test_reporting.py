# -*- coding: utf-8 -*-
import pytest
from apistar.exceptions import ErrorResponse

from arkindex_worker.reporting import Reporter


def test_init():
    reporter = Reporter("worker")
    assert "started" in reporter.report_data
    del reporter.report_data["started"]
    assert reporter.report_data == {"slug": "worker", "version": "0.0", "elements": {}}


def test_process():
    reporter = Reporter("worker")
    reporter.process("myelement")
    assert "myelement" in reporter.report_data["elements"]
    element_data = reporter.report_data["elements"]["myelement"]
    assert "started" in element_data
    del element_data["started"]
    assert element_data == {
        "elements": {},
        "transcriptions": 0,
        "classifications": {},
        "entities": [],
        "errors": [],
    }


def test_add_element():
    reporter = Reporter("worker")
    reporter.add_element("myelement", type="text_line")
    assert "myelement" in reporter.report_data["elements"]
    element_data = reporter.report_data["elements"]["myelement"]
    del element_data["started"]
    assert element_data == {
        "elements": {"text_line": 1},
        "transcriptions": 0,
        "classifications": {},
        "entities": [],
        "errors": [],
    }


def test_add_element_count():
    """
    Report multiple elements with the same parent and type
    """
    reporter = Reporter("worker")
    reporter.add_element("myelement", type="text_line", type_count=42)
    assert "myelement" in reporter.report_data["elements"]
    element_data = reporter.report_data["elements"]["myelement"]
    del element_data["started"]
    assert element_data == {
        "elements": {"text_line": 42},
        "transcriptions": 0,
        "classifications": {},
        "entities": [],
        "errors": [],
    }


def test_add_classification():
    reporter = Reporter("worker")
    reporter.add_classification("myelement", "three")
    assert "myelement" in reporter.report_data["elements"]
    element_data = reporter.report_data["elements"]["myelement"]
    del element_data["started"]
    assert element_data == {
        "elements": {},
        "transcriptions": 0,
        "classifications": {"three": 1},
        "entities": [],
        "errors": [],
    }


def test_add_classifications():
    reporter = Reporter("worker")
    with pytest.raises(AssertionError):
        reporter.add_classifications("myelement", {"not": "a list"})

    reporter.add_classifications(
        "myelement", [{"class_name": "three"}, {"class_name": "two"}]
    )
    reporter.add_classifications(
        "myelement",
        [
            {"class_name": "three"},
            {"class_name": "two", "high_confidence": True},
            {"class_name": "three", "confidence": 0.42},
        ],
    )

    assert "myelement" in reporter.report_data["elements"]
    element_data = reporter.report_data["elements"]["myelement"]
    del element_data["started"]
    assert element_data == {
        "elements": {},
        "transcriptions": 0,
        "classifications": {"three": 3, "two": 2},
        "entities": [],
        "errors": [],
    }


def test_add_transcription():
    reporter = Reporter("worker")
    reporter.add_transcription("myelement")
    assert "myelement" in reporter.report_data["elements"]
    element_data = reporter.report_data["elements"]["myelement"]
    del element_data["started"]
    assert element_data == {
        "elements": {},
        "transcriptions": 1,
        "classifications": {},
        "entities": [],
        "errors": [],
    }


def test_add_transcription_warning():
    reporter = Reporter("worker")

    with pytest.warns(FutureWarning) as w:
        reporter.add_transcription("myelement", "word")
    assert len(w) == 1
    assert (
        w[0].message.args[0]
        == "Transcription types have been deprecated and will be removed in the next release."
    )

    assert "myelement" in reporter.report_data["elements"]
    element_data = reporter.report_data["elements"]["myelement"]
    del element_data["started"]
    assert element_data == {
        "elements": {},
        "transcriptions": 1,
        "classifications": {},
        "entities": [],
        "errors": [],
    }


def test_add_transcription_count():
    """
    Report multiple transcriptions with the same element and type
    """
    reporter = Reporter("worker")
    reporter.add_transcription("myelement", type_count=1337)
    assert "myelement" in reporter.report_data["elements"]
    element_data = reporter.report_data["elements"]["myelement"]
    del element_data["started"]
    assert element_data == {
        "elements": {},
        "transcriptions": 1337,
        "classifications": {},
        "entities": [],
        "errors": [],
    }


def test_add_transcriptions():
    reporter = Reporter("worker")
    with pytest.raises(AssertionError):
        reporter.add_transcriptions("myelement", {"not": "a list"})

    with pytest.warns(FutureWarning) as w:
        reporter.add_transcriptions("myelement", [{"type": "word"}, {"type": "line"}])
        reporter.add_transcriptions(
            "myelement",
            [
                {"type": "word"},
                {"type": "line", "text": "something"},
                {"type": "word", "confidence": 0.42},
            ],
        )
    assert len(w) == 2
    assert set(warning.message.args[0] for warning in w) == {
        "Reporter.add_transcriptions is deprecated due to transcription types being removed. Please use Reporter.add_transcription(element_id, count) instead."
    }

    assert "myelement" in reporter.report_data["elements"]
    element_data = reporter.report_data["elements"]["myelement"]
    del element_data["started"]
    assert element_data == {
        "elements": {},
        "transcriptions": 5,
        "classifications": {},
        "entities": [],
        "errors": [],
    }


def test_add_entity():
    reporter = Reporter("worker")
    reporter.add_entity(
        "myelement", "12341234-1234-1234-1234-123412341234", "person", "Bob Bob"
    )
    assert "myelement" in reporter.report_data["elements"]
    element_data = reporter.report_data["elements"]["myelement"]
    del element_data["started"]
    assert element_data == {
        "elements": {},
        "transcriptions": 0,
        "classifications": {},
        "entities": [
            {
                "id": "12341234-1234-1234-1234-123412341234",
                "type": "person",
                "name": "Bob Bob",
            }
        ],
        "errors": [],
    }


def test_error():
    reporter = Reporter("worker")
    reporter.error("myelement", ZeroDivisionError("What have you done"))
    reporter.error(
        "myelement",
        ErrorResponse(
            title="I'm a teapot",
            status_code=418,
            content='{"coffee": "Can\'t touch this"}',
        ),
    )
    assert reporter.report_data["elements"]["myelement"]["errors"] == [
        {"class": "ZeroDivisionError", "message": "What have you done"},
        {
            "class": "ErrorResponse",
            "message": "I'm a teapot",
            "status_code": 418,
            "content": '{"coffee": "Can\'t touch this"}',
        },
    ]
