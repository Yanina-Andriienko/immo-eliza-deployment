# 🏠 Immo Eliza Property Price Prediction

This project aims to deploy a machine learning model to predict property prices through an API endpoint. It also includes a Streamlit web application for easier interaction with the model. The project is structured into two main parts: the API for developers and a user-friendly web application for non-technical users.

## 📚 Table of Contents

- [🌟 Project Overview](#project-overview)
- [🏗 Architecture](#architecture)
- [📄 API Documentation](#api-documentation)
- [🖥 Web Application](#web-application)
- [🚀 Getting Started](#getting-started)
  - [💻 Prerequisites](#prerequisites)
  - [🛠 Installation](#installation)
- [🔧 Usage](#usage)
  - [🔌 API](#api)
  - [🖥 Streamlit App](#streamlit-app)
- [👥 Contributors](#contributors)

## 🌟 Project Overview

The real estate company Immo Eliza requires a solution to estimate property prices based on various attributes. This repository contains the implementation of a machine learning model deployed as an API and a Streamlit web application for interactive price predictions.

## 🏗 Architecture

The architecture includes:

- A machine learning model trained on real estate data.
- A FastAPI application serving the model.
- A Docker container to encapsulate the API environment.
- A Streamlit web application for interactive predictions.

## 📄 API Documentation

The API accepts JSON formatted input and returns the estimated property price. Detailed documentation can be found at `/docs` endpoint of the API.

### Endpoints:

- `/` : GET method to check API status.
- `/predict` : POST method to get property price predictions.

## 🖥 Web Application

The Streamlit application provides a user-friendly interface to input property details and receive price predictions without needing to interact with the API directly.

## 🚀 Getting Started

### 💻 Prerequisites

- Python 3.8 or later
- Docker
- Streamlit

### 🛠 Installation

1. Clone the repository:

   ```sh
   git clone git@github.com:Yanina-Andriienko/immo-eliza-deployment.git

   ```

2. Install required Python packages:
   ```sh
   pip install -r requirements.txt
   ```

## 🔧 Usage

### 🔌 API

To run the API locally:

```sh
uvicorn app:app --reload
```

### 🖥 Streamlit App

To run the Streamlit application:

```sh
streamlit run streamlit_app.py
```

## 👥 Contributors

- [Yanina Andriienko](https://www.linkedin.com/in/yanina-andriienko-7a2984287/)
