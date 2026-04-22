import requests
import time

BASE_URL = "http://localhost:5001/api"


def get_status():
    for _ in range(3):
        try:
            response = requests.get(f"{BASE_URL}/status", timeout=2)
            return response.json()
        except requests.exceptions.RequestException:
            time.sleep(1)

    return {
        "status": "offline",
        "battery": 0,
        "position": {"x": 0, "y": 0}
    }


def move_robot(direction):
    try:
        # Get current position
        current = requests.get(f"{BASE_URL}/status", timeout=2).json()

        x = current.get("position", {}).get("x", 0)
        y = current.get("position", {}).get("y", 0)

        # Update position
        if direction == "right":
            x += 1
        elif direction == "left":
            x -= 1
        elif direction == "up":
            y += 1
        elif direction == "down":
            y -= 1

        # 🔥 ADD IT RIGHT HERE (VERY IMPORTANT)
        x = max(0, min(10, x))
        y = max(0, min(10, y))

        # Send new position
        response = requests.post(
            f"{BASE_URL}/move",
            json={"x": x, "y": y}
        )

        return response.json()

    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": str(e)}