from io import BytesIO

from agents.file_agent import extract_text_from_pdf


class DummyPage:
    def get_text(self) -> str:
        return "dummy"


class DummyDoc:
    def __init__(self) -> None:
        self.closed = False

    def __iter__(self):
        return iter([DummyPage()])

    def close(self) -> None:
        self.closed = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()


def test_extract_text_from_pdf_closes_doc(monkeypatch):
    dummy_doc = DummyDoc()

    def fake_open(*args, **kwargs):
        return dummy_doc

    import agents.file_agent as file_agent

    monkeypatch.setattr(file_agent.fitz, "open", fake_open)
    text = extract_text_from_pdf(BytesIO(b"dummy"))
    assert text == "dummy"
    assert dummy_doc.closed is True
