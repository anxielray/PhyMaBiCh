# PhyMaBiCh

PhyMaBiCh is an AI project made for the nerdy brains for learning Mathematics, crazy Physics, reactive chemistry and experimental Biologists. This is the home tutor of STEM

## Contents

- [PhyMaBiCh](#phymabich)
  - [Contents](#contents)
  - [Installation](#installation)
  - [Project Structure](#project-structure)
    - [Documentation](#documentation)
    - [Backend](#backend)
    - [Frontend](#frontend)
  - [Tech Stack](#tech-stack)
  - [How To Use PhiMaBiCh](#how-to-use-phimabich)
    - [As a Developer](#as-a-developer)

## Installation

- _The application is dockerized. Run this command to compose up the file;_

```sh
docker-compose up --build
```

## Project Structure

- _PhyMaBiCh has a modular approach on the project structure, having the projrct application divided into three; documentation, frontend and the backend._

```sh
PhyMaBiCh/
  ├─ backend/
  |   └─ main.py
  ├─ docs/
  ├─ /frontend
  ├─ README.md
```

### Documentation

- _This section provides comprehensive guidance on the project, including an overview of its purpose, detailed usage instructions, and clear contribution guidelines to facilitate collaboration and community engagement._

### Backend

- _The backend is a robust Python-based application server, architected with FastAPI to deliver high-performance, asynchronous request handling. It seamlessly integrates with the OpenAI API to power advanced AI-driven functionalities and deliver a sophisticated user experience._

### Frontend

- _The frontend leverages the Vue.js framework, offering a scalable and maintainable architecture that effectively manages the application's complexity while ensuring a responsive and intuitive user interface._

## Tech Stack

- _PhyMaBiCh application leverages the cobined work of Python API servers backend and Vue framework frontend to render the application AI._

## How To Use PhiMaBiCh

### As a Developer

- _To run the application, you will have it installed in your machine, probably from Github.com._
- _Change directory into the appliation and run the folliwing command with the backend server:_

- _To sart the application, execute the script, `start_app.sh`. Optionally to know, what the script commands mean in depth;
- _Since the backend runs on Python, I would recommend having the latest Python installed before proceeding if necessary, after which, in a virtual environment, run the commands:_

```sh
pip install fastapi uvicorn openai
```

_and finally run the application server;_

```sh
uvicorn main:app --reload
```

- _For the frontend part, install the Vue CLI if not already installed;_

```sh
npm install -g @vue/cli
vue create frontend
```

- _After which the application frontend will be started with the following commands from the working directory;_

```sh
cd frontend
npm run serve
```
