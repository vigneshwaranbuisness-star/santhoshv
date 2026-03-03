import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_import_config():
    try:
        from config import MAX_USERS, SYSTEM_NAME
        assert MAX_USERS is not None
        assert SYSTEM_NAME is not None
    except ImportError as e:
        pytest.fail(f"Import failed: {e}")


def test_capacity_limit():
    from utils import calculate_capacity
    assert calculate_capacity(5, 5) is False


def test_within_capacity():
    from utils import calculate_capacity
    assert calculate_capacity(4, 5) is True


def test_state_increment():
    from state import reset_state, get_user_count, increment_count

    reset_state()
    assert get_user_count() == 0

    increment_count()
    assert get_user_count() == 1

    increment_count()
    assert get_user_count() == 2


def test_state_isolation():
    from state import reset_state, increment_count, get_user_count

    reset_state()
    increment_count()

    from state import get_user_count as get_count_2
    assert get_count_2() == 1


def test_module_chain():
    from state import reset_state

    reset_state()

    try:
        from module_a import add_user
        assert add_user is not None
    except ImportError as e:
        pytest.fail(f"{e}")


def test_config_type():
    from config import MAX_USERS

    assert isinstance(MAX_USERS, int)
    assert MAX_USERS > 0


def test_full_system():
    from state import reset_state
    from config import MAX_USERS
    from utils import calculate_capacity

    reset_state()

    assert calculate_capacity(0, MAX_USERS) is True
    assert calculate_capacity(MAX_USERS - 1, MAX_USERS) is True
    assert calculate_capacity(MAX_USERS, MAX_USERS) is False
    assert calculate_capacity(MAX_USERS + 1, MAX_USERS) is False


def test_hidden_bugs():
    from utils import hidden_bonus_calculator

    try:
        result = hidden_bonus_calculator(10)
        assert result != float('inf')
    except ZeroDivisionError:
        pytest.fail("Hidden bug found: Division by zero in hidden_bonus_calculator!")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])