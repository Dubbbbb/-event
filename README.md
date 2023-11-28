# +event

Welcome to my "+event" project! This project is a system for tracking and managing events, to-do lists, and price lists. Below, you will find a brief documentation for using and deploying the application.

## Key Features

- **Events:** Create, edit, and manage various events.
- **To-Do Lists and Price Lists:** Attach to-do lists and price lists to your events for convenient planning and organization.
- **Notifications:** Automatic notifications through Celery and Redis when inviting or excluding users from events.
- **REST API:** Use the API to get information about public events, user profiles, and event details.

## Installation

The project is easily deployed using Docker Compose. Navigate to the root directory of the project and run the following commands:

```bash
docker-compose build
docker-compose up
```

This will start the application and all necessary services, including the database, Celery, and Redis.

## Usage

### Web Interface

- Visit the web interface: Go to http://localhost:8000 to interact with the application through the web interface.

### REST API

- **Public Events:** Get a list of public events:
```http
  GET /api/public_events/
```
- **User Events:** Get user events using a JWT token:
```http
  GET /api/events/
```
- **User Event Details:** Get details of a specific user event using a JWT token:
```http
  GET /api/events/<event_id>/
```
- **JWT token:** Get JWT token and refresh token:
```http
  POST /api/login/
```
  - `username` (str) - user name.
  - `password` (str) - user password.
