# Team Picker

## 📄 Description

🎲 Discover an application designed to randomly pick a member of your team for various activities or tasks.

🤔 “Who should be the next to speak?” This application helps answer this question by providing a fun and fair way to select a random team member. Whether it's for a meeting, a presentation, or any team activity, let chance decide!

Here's a tool that allows you to manage team members, add or remove members, and perform a random selection with a fun twist. Ideal for teams who want to add an element of surprise and fairness to their processes.

🌐 Access the app and start your random selection now at [https://teampicker.sotisanalytics.com](https://teampicker.sotisanalytics.com).

![Image1](images/image1.png)

---

## Prerequisites
- Anaconda or Miniconda
- Docker (for Docker deployment)

---

## ⚒️ Installation

### Prerequisites
- Python 3.11
- Python libraries
    ```sh
    pip install -r requirements.txt
    ```

---

## 📝 Usage

### Running without Docker

1. **Clone the repository and navigate to the directory**
    ```bash
    git pull https://github.com/LudovicGardy/app_team_picker
    cd team_picker_repos/app_folder
    ```

2. **Environment setup**
    - Create and/or activate the virtual environment:
        ```bash
        conda create -n myenv python=3.11
        conda activate myenv
        ```
        or
        ```bash
        source .venv/bin/activate
        ```

3. **Launch the Streamlit App**
    - Run the Streamlit application:
        ```bash
        streamlit run main.py
        ```

### Running with Docker

1. **Prepare Docker environment**
    - Ensure Docker is installed and running on your system.

2. **Navigate to project directory**
    - For multiple containers:
        ```bash
        cd [path-to-app-folder-containing-docker-compose.yml]
        ```
    - For a single container:
        ```bash
        cd [path-to-app-folder-containing-Dockerfile]
        ```

3. **Build the image (if does not already exist)**
    - For multiple containers:
        ```bash
        docker-compose up --build
        ```
    - For a single container:
        ```bash
        docker build -t my-app-title .
        ```

4. **Run the containers**
    - For multiple containers:
        ```bash
        docker run -p 8501:8501 my-app-title
        ```
    - The application will be accessible at `http://localhost:8501`.

5. **Other notes**
    - ⚠️ If you encounter issues with `pymssql`, adjust its version in `requirements.txt` or remove it before building the Docker image.
    - ⚠️ If you encounter issues with `pyspark`, you might need to uninstall and reinstall it. Additionally, ensure that Java is installed and properly configured on your system, as `pyspark` depends on Java. You can install Java by following the instructions on the [official Java website](https://www.java.com/en/download/help/download_options.html). Make sure to set the `JAVA_HOME` environment variable to point to your Java installation directory.

---

## 👤 Author
- LinkedIn: [Ludovic Gardy](https://www.linkedin.com/in/ludovic-gardy/)
- Website: [https://www.sotisanalytics.com](https://www.sotisanalytics.com)
