from robot_api import get_status, move_robot

def test_status():
    data = get_status()
    assert "status" in data
    assert "position" in data

def test_move_robot():
    response = move_robot("up")
    assert response is not None
    