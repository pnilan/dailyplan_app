# DailyPlan: Full-Stack Task Management Application

DailyPlan is a full-stack task management application built using Python, Flask, and Bootstrap. This application allows users to create an account, manage tasks, track completion statistics, and gain insights into their task completion habits. The application is deployed on a Digital Ocean droplet and utilizes NGINX as a proxy server for enhanced performance.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Deployment](#deployment)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

## Introduction

DailyPlan is a simple task management application designed to help users organize their tasks, track their progress, and gain valuable insights into their productivity patterns without the bloat of most modern project management tools.

## Features

- User Authentication: Create an account and securely log in to access your tasks.
- Task Management: Add, update, and delete tasks with ease.
- Subtasks: Break down tasks into smaller subtasks for better organization.
- Task Completion Tracking: Monitor the number of completed tasks and subtasks.
- Insights Dashboard: Gain insights into average task completion time and more.

## Deployment

DailyPlan is deployed on a Digital Ocean droplet and utilizes NGINX as a proxy server for improved performance. The deployment process ensures that the application is accessible online for users to manage their tasks seamlessly.

## Prerequisites

Before you begin, ensure you have the following:

- Python (3.7 or later)
- Flask (1.1 or later)
- Bootstrap (4.x)
- PostgreSQL (or another compatible database)
- Digital Ocean droplet (or alternative hosting solution)
- NGINX (for proxy server)

## Installation

1. Clone this repository to your local machine:

   ```
   git clone https://github.com/your-username/dailyplan_app.git
   ```

2. Navigate to the project directory:

   ```
   cd dailyplan_app
   ```

3. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Set up your database and configure the database URI in the application configuration.

5. Start the Flask development server:

   ```
   flask run
   ```

6. Access the application in your web browser at `http://localhost:5000`.

## Usage

1. Create an account or log in to your existing account.
2. Add tasks and subtasks to your daily plan.
3. Mark tasks and subtasks as completed as you make progress.
4. Explore the insights dashboard to gain valuable productivity insights.

## Technologies Used

![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Digital Ocean](https://img.shields.io/badge/Digital_Ocean-0080FF?style=for-the-badge&logo=DigitalOcean&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)

## Contributing

We welcome contributions to enhance the functionality and features of DailyPlan. To contribute, follow these steps:

1. Fork the repository.
2. Create a new branch for your feature/bugfix.
3. Make your changes and test thoroughly.
4. Create a pull request with a detailed description of your changes.

## License

This project is licensed under the MIT License.