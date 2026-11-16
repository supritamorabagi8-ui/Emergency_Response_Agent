# 🚨 Emergency Response Agent AI

## 📌 About the Project

Emergency Response Agent AI is a Python-based project developed to help manage emergency situations on a college campus.

The system helps identify safe evacuation routes during emergencies using pathfinding algorithms. It also provides a dashboard to monitor campus incidents, risks, emergency routes, and response activities.

The main aim of this project is to make campus emergency management easier, faster, and more organized with the help of Artificial Intelligence concepts and graph algorithms.

## 🎯 Project Objectives

- To identify safe evacuation routes during emergency situations.
- To find suitable paths to the nearest emergency exits.
- To monitor campus incidents and potential risks.
- To provide useful information through an interactive dashboard.
- To improve emergency response planning and decision-making.

## ✨ Key Features

- **Emergency Dashboard:** Displays important emergency information in one place.
- **Route Planning:** Finds suitable evacuation routes using BFS and A* algorithms.
- **Live Campus Map:** Helps users understand campus locations and routes.
- **Incident Management:** Supports monitoring and managing emergency incidents.
- **Risk Monitoring:** Provides information about possible campus risks.
- **What-If Simulation:** Helps explore different emergency situations.
- **Performance Analytics:** Displays information about route and system performance.
- **Emergency Reports:** Provides emergency-related reports.
- **Decision Support:** Uses predefined decision rules to support emergency response.

## 🏫 Campus Locations

The project uses the following campus locations:

| ID | Location |
|---|---|
| A | Academic Block A |
| B | Academic Block B |
| L | Library |
| C | Canteen |
| M | Medical Centre |
| P | Parking Area |
| G1 | Main Gate |
| G2 | Gate 2 |

The Main Gate (G1) and Gate 2 (G2) are considered emergency exit points.

## 🧠 Algorithms Used

### 1. Breadth-First Search (BFS)

BFS is used to explore connected campus locations level by level and find a path through the campus graph.

### 2. A* Search Algorithm

A* is used for route planning by evaluating possible paths and selecting a suitable route based on its search cost and heuristic.

### 3. Decision Rules

The project also uses predefined decision rules to support emergency-related decisions based on different conditions.

## 🛠️ Technologies Used

- **Python** – Main programming language
- **Streamlit** – Interactive web application
- **BFS** – Pathfinding algorithm
- **A* Search** – Route planning algorithm
- **NetworkX / Graph Concepts** – Campus graph representation, where applicable
- **Pandas** – Data handling, where applicable
- **HTML and CSS** – Dashboard styling

## 📂 Project Structure

```text
Emergency_Response_Agent/
│
├── algorithms/
│   ├── bfs.py
│   └── astar.py
│
├── environment/
│   ├── campus_graph.py
│   ├── state.py
│   └── validation.py
│
├── performance/
│   └── route_metrics.py
│
├── ui/
│   └── theme.py
│
├── received/
│
├── app.py
├── requirements.txt
└── README.md
```

*Note: This is an overview of the main project components. Your actual folder structure may contain additional files and folders.*

## ⚙️ Installation and Setup

Follow these steps to run the project on your computer.

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/Emergency_Response_Agent.git
```

### Step 2: Open the Project Folder

```bash
cd Emergency_Response_Agent
```

### Step 3: Create a Virtual Environment (Optional)

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### Step 4: Install Required Libraries

```bash
pip install -r requirements.txt
```

### Step 5: Run the Application

```bash
python -m streamlit run app.py
```

The application will open in your browser. If it does not open automatically, visit:

`http://localhost:8501`

## 📊 Expected Outcome

The project provides an interactive dashboard for campus emergency management. Users can explore campus locations, view evacuation routes, monitor incidents, and understand emergency-related information.

It demonstrates how Python, graph algorithms, and a web-based dashboard can be combined to support campus safety planning.

## 🚀 Future Improvements

- Improve real-time emergency notifications.
- Add more detailed campus maps.
- Include additional emergency scenarios.
- Improve route selection based on blocked or unsafe paths.
- Add more visual reports and analytics.
- Explore integration with real-time campus information.

## 👩‍💻 Project Information

**Project Name:** Emergency Response Agent AI

**Domain:** Artificial Intelligence and Emergency Management

**Technology:** Python and Streamlit

**Project Type:** Academic Project

## ⚠️ Disclaimer

This project is developed for academic and demonstration purposes. The suggested routes and emergency information should not replace official campus emergency procedures or instructions from emergency personnel.

## ⭐ Support

If you find this project interesting, consider giving the repository a star on GitHub!