# Robot Dashboard System

A web-based Robot Monitoring and Control Dashboard built using Flask.  
The system allows users to monitor robot status and control movement through a role-based access system.

---

## Features

-  User Registration and Authentication
- Role-Based Access Control (Viewer / Commander)
- Robot Movement Controls (Up, Down, Left, Right)
- Real-time Status Monitoring (Battery, Position)
- Command Logging System
- API Failure Handling:
  - Reconnecting (network issue)
  - Signal Lost (robot offline)
- Automated Testing using pytest
- Docker Support

---

## Technologies Used

- Python (Flask)
- SQLite
- HTML / CSS
- REST API Integration
- Docker

---

##  How to Run

### Option 1: Using Docker (Recommended)

1. Install Docker
2. Open terminal in project folder
3. Run:

```bash
docker-compose up --build