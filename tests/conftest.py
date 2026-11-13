from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def android_24h():
    return (FIXTURES / "android_24h.txt").read_text(encoding="utf-8")


@pytest.fixture
def android_12h():
    return (FIXTURES / "android_12h.txt").read_text(encoding="utf-8")


@pytest.fixture
def ios_export():
    return (FIXTURES / "ios_export.txt").read_text(encoding="utf-8")
