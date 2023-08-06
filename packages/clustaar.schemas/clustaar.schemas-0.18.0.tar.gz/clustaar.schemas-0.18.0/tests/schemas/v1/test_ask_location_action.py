import pytest
from clustaar.schemas.v1 import ASK_LOCATION_ACTION
from clustaar.schemas.models import StepTarget, GoToAction, AskLocationAction


@pytest.fixture
def action():
    target = StepTarget(step_id="a1" * 12, name="a step")
    go_to = GoToAction(target=target)
    return AskLocationAction(message="Where are you?", callback_action=go_to)


@pytest.fixture
def data():
    return {
        "type": "ask_location_action",
        "message": "Where are you?",
        "action": {
            "type": "go_to_action",
            "target": {"type": "step", "name": "a step", "id": "a1" * 12},
            "sessionValues": None,
        },
    }


@pytest.fixture
def malicious_data():
    return {
        "type": "ask_location_action",
        "message": "<script>void();</script>Where are you?",
        "action": {
            "type": "go_to_action",
            "target": {"type": "step", "name": "a step", "id": "a1" * 12},
            "sessionValues": None,
        },
    }


class TestDump:
    def test_returns_a_dict(self, action, data, mapper):
        result = ASK_LOCATION_ACTION.dump(action, mapper)
        assert result == data


class TestLoad:
    def test_returns_an_action(self, data, mapper):
        action = mapper.load(data, ASK_LOCATION_ACTION)
        assert isinstance(action, AskLocationAction)
        assert action.message == "Where are you?"
        assert isinstance(action.callback_action, GoToAction)
        assert action.callback_action.target.step_id == "a1" * 12


class TestLoadMalicious:
    def test_returns_an_action(self, malicious_data, mapper):
        action = mapper.load(malicious_data, ASK_LOCATION_ACTION)
        assert isinstance(action, AskLocationAction)
        assert action.message == "&lt;script&gt;void();&lt;/script&gt;Where are you?"
