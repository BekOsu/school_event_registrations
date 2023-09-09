# school_event_registrations

# **event_registrations**

The Event Registration App is designed to streamline the registration process for school extracurricular events. It provides an integrated platform that allows administrators to add event details and enables users to register for these events. The app is equipped with advanced features such as event filtering and bulk importing of data.

## **Table of Contents**

1. Features
2. Installation
3. Running the Application
4. API Documentation
5. Tests

## **Features**

- Registration and authentication for users.
- Event management capabilities for administrators.
- Detailed event pages for users to explore.
- Participant registration, including profile picture upload.
- Employee management (create, list)
- Event filtering and sorting functionality.
- Bulk event importing functionality via CSV files.
- Containerization (Docker)

![event-list](https://github.com/BekOsu/school_event_registrations/assets/95960598/d11cc6a2-2eec-4b55-87bb-caf0ba3b8ea5)

## **Installation**

1. Clone the repository:

```
https://github.com/BekOsu/school_event_registrations.git
```

2. Start the application using Docker Compose:

```
cd event_registration/
Run docker-compose build      to build the Docker images.
Run docker-compose up         to start the development server.

```

## Technology Stack & Features:
* Django fresh build
* RestFramework
* Open API and swagger.
* docker with Docker compose.
* Kubernetes.
* makefile.
* Logs.
* Schedule Tasks (Celery Rabbitmq).
* REDIS.
* Celery.
* Custom exception handler.
* CI/CD Pipeline.
* Nginx API-gateway.
* Frontend.
* Linting and Static typing tools.


### **Pre-commit Hooks**

This project uses pre-commit hooks to ensure code quality and consistency. The following hooks are used:

- **`flake8`**
- **`isort`**
- **`black`**
- **`pylint_regular`**
- **`pylint_unittest`**
- **`sort-simple-yaml`**
- **`check-added-large-files`**
- **`check-case-conflict`**
- **`check-symlinks`**
- **`requirements-txt-fixer`**
- **`trailing-whitespace`**
- **`end-of-file-fixer`**
- **`debug-statements`**
- **`fix-encoding-pragma`**
- **`mixed-line-ending`**
- **`add-trailing-comma`**

## CI/CD:
#### Two steps: Build with tests, then Deploy.
#### I commented the part of pushing the images to DockerHub then uploading it to the cloud.
![pipline](https://github.com/BekOsu/school_event_registrations/assets/95960598/2bb5255e-bb9e-49da-ac5d-9f92d32f29fc)


## **API Endpoints**

### **Authentication Endpoints**

- **`POST /api/token/`**: Get an access token by providing valid credentials.
- **`POST /api/token/refresh/`**: Refresh an existing access token.

### **API Endpoints**

**`Functionality:`**
The application has API endpoints for event creation, retrieval, listing, updating, or deleting.
**`Authentication:`**
JWT authentication is used for securing these endpoints.
**`Front-End Compatibility:`**
These API endpoints can be used to implement a single-page application or can be connected to front-end frameworks like React or Vue.js.

## **API Documentation**

API documentation is available at http://127.0.0.1:8001/swagger 

This provides a detailed overview of the available API endpoints, including their input and output formats.

![swagger](https://github.com/BekOsu/school_event_registrations/assets/95960598/bdae315e-6e7a-4ff9-b01b-378bc2451135)

We used Swager open-API to auto document  APIs.

## **Tests**

To run the test suite, execute the following command:

```
python manage.py test
```

## **Application Logic**

1. User Roles: Event creators must sign up and be added to the event-admins group by an admin to gain event management permissions.
2. Participant Registration: Users can register for events, providing essential information like name, email, and phone number. Profile pictures are optional.
3. Event Browsing: Users can view a list of events with details such as name, date, location, and available slots.
4. Event Filtering: Events can be filtered by type or date, and a list of matching events will be displayed.
5. Post-Registration Actions: After registering for an event, users are redirected to their profile page, where they can see their registered events and profile details.
6. API Endpoints: The app includes secured API endpoints for event management, compatible with front-end frameworks for potential SPA (Single Page Application) development.

![profile-page](https://github.com/BekOsu/school_event_registrations/assets/95960598/9bbda497-fe99-4fbc-a66e-06ba875f15ba)


## **Future Work:**

Explore additional features like user suggestions and detailed event information. Technologies such as task queues will be implemented for efficient bulk event CSV uploads. The system will also incorporate a service registry (e.g., Eureka) and a notification service. To improve scalability and maintainability, the system will adopt Domain-Driven Design and Test-Driven Development, as well as design patterns like Pub-Sub, Adapter, Factory, and Singleton.

## **Contributors**

- Abubaker Suliman

## **License**

This project is licensed under the MIT License - see the LICENSE.md file for details.
