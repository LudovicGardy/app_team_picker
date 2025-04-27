# Team Picker

## 📄 Description

🎲 Discover an application designed to randomly pick a member of your team for various activities or tasks.

🤔 “Who should be the next to speak?” This application helps answer this question by providing a fun and fair way to select a random team member. Whether it's for a meeting, a presentation, or any team activity, let chance decide!

Here's a tool that allows you to manage team members, add or remove members, and perform a random selection with a fun twist. Ideal for teams who want to add an element of surprise and fairness to their processes.

🌐 Access the app and start your random selection now at [https://teampicker.sotisai.com](https://teampicker.sotisai.com).

![Image1](images/image1.png)

---

## ⚙️ Setup & Usage

You can run the application in two ways:

- **Locally using `uv`**
- **Using Docker Compose**

### 🔧 Option 1 — Run Locally with `uv`

> `uv` is a fast and modern Python tool that handles virtual environments and dependencies via `pyproject.toml`.

1. **Install `uv`** (if not already installed)  
   ```bash
   curl -Ls https://astral.sh/uv/install.sh | sh
   ```

2. **Clone the repository**  
   ```bash
   git clone https://github.com/LudovicGardy/app_name
   cd app_folder/
   ```

3. **Create and activate the environment**  
   ```bash
   uv venv
   ```

   - On **macOS/Linux**:
     ```bash
     source .venv/bin/activate
     ```

   - On **Windows** (PowerShell):
     ```powershell
     .venv\Scripts\Activate.ps1
     ```

4. **(Optional) If the virtual environment doesn't behave properly**

   Sometimes, on macOS in particular, the environment might be missing some tooling (like `pip`). You can try the following fixes:

   ```bash
   .venv/bin/python -m ensurepip --upgrade
   .venv/bin/python -m pip install --upgrade pip
   # Optional: Only if you need to use Jupyter notebooks
   .venv/bin/python -m pip install ipykernel -U --force-reinstall
   ```

5. **Launch the app**  
   ```bash
   streamlit run main.py
   ```

### 🐳 Option 2 — Run with Docker Compose

1. **Make sure Docker and Docker Compose are installed and running**

2. **Go to the project directory**
   ```bash
   cd path/to/app_folder
   ```

3. **Build and start the app**
   ```bash
   docker-compose up --build
   ```

4. **Access the app**
   Open your browser at: [http://localhost:8504](http://localhost:8504)

---

## 👤 Author
- LinkedIn: [Ludovic Gardy](https://www.linkedin.com/in/ludovic-gardy/)
- Website: [https://www.sotisai.com](https://www.sotisai.com)
