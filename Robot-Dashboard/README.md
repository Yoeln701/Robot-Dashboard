# Robot Dashboard System

## Overview
This project is a web-based dashboard for controlling and monitoring a virtual robot using a REST API.

## How to Run
1. Install Docker
2. Open terminal in project folder
3. Run:
   docker-compose up --build
4. Open browser:
   http://localhost:5000

## Features
- Robot movement controls (Up, Down, Left, Right)
- Real-time status monitoring (battery, position)
- 2D grid visualization
- Role-based access control
- Command logging
- Error handling for API failures
- Automated testing using pytest

## Ports
- Dashboard: http://localhost:5000
- Robot API: http://localhost:5001

## Testing
Run:
pytest

All tests pass successfully.