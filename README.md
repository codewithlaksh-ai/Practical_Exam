# 🏋️ Personal Fitness Tracker Dashboard

A Python-based Personal Fitness Tracker Dashboard that helps users record their physical activities, track calories burned, analyze fitness metrics, filter activity records, and visualize fitness trends using charts.

This project demonstrates **Object-Oriented Programming (OOP), Control Structures, NumPy, Pandas, Matplotlib, Seaborn, and CSV file handling**.

## 📌 Features

- **Log a New Activity:** Record activity type, duration, calories burned, and date.
- **Calculate Fitness Metrics:** Calculate total activities, total duration, total calories, average duration, and average daily calories.
- **Filter Activities:** Filter records by activity type, start date, and end date.
- **Generate Fitness Report:** Display a detailed fitness summary, activity frequency, and activity-wise statistics.
- **Visualize Fitness Data:** Generate charts to understand fitness trends and activity performance.
- **View All Activities:** Display all recorded fitness activities.
- **Data Validation:** Validate user inputs, dates, durations, and calories.
- **CSV Data Storage:** Save activity records in a CSV file for future use.

## 📊 Dashboard Visualizations

The project generates four visualizations:

1. **Bar Chart:** Total workout duration by activity type.
2. **Line Chart:** Calories burned over time.
3. **Pie Chart:** Distribution of activity duration by activity type.
4. **Heatmap:** Correlation between workout duration and calories burned.

## 🛠️ Technologies Used

- **Python** – Core programming language
- **NumPy** – Numerical calculations and array operations
- **Pandas** – Data manipulation, analysis, and CSV handling
- **Matplotlib** – Data visualization
- **Seaborn** – Statistical charts and heatmaps
- **Datetime** – Date and time handling
- **OS** – File path and file existence management

## 🧠 Python Concepts Used

- Variables and data types
- Control structures and loops
- Conditional statements
- Functions
- Object-Oriented Programming (classes, objects, and methods)
- Lists and arrays
- DataFrames and data analysis
- Exception handling
- File handling
- Data validation
- Data aggregation and grouping

## 📂 Project Structure

```text
Personal-Fitness-Tracker/
│
├── fitness_tracker.py
├── fitness_activities.csv
└── README.md
```

- `fitness_tracker.py` – Main Python application.
- `fitness_activities.csv` – Stores fitness activity records.
- `README.md` – Project documentation.

The CSV file is automatically created when it does not exist.

## ⚙️ Installation

### 1. Install Python

Make sure Python is installed on your computer.

Check the version:

```bash
python --version
```

### 2. Install Required Libraries

Open the terminal and run:

```bash
pip install numpy pandas matplotlib seaborn
```

### 3. Download the Project

Download or clone the repository and open the project folder in your code editor.

### 4. Run the Application

Execute the following command:

```bash
python fitness_tracker.py
```

## ▶️ Application Menu

When the program starts, the following menu is displayed:

```text
====== PERSONAL FITNESS TRACKER ======
1. Log a new activity
2. Calculate metrics
3. Filter activities
4. Generate fitness report
5. Show dashboard charts
6. View all activities
7. Exit
```

Select an option to perform the desired operation.

## 📋 Sample Data

The CSV file contains the following columns:

| Column | Description |
|---|---|
| Date | Date of the activity |
| Activity Type | Type of physical activity |
| Duration (Minutes) | Duration of the activity |
| Calories Burned | Calories burned during the activity |

Example:

```text
Date,Activity Type,Duration (Minutes),Calories Burned
2026-10-01,Running,30,300
2026-10-02,Cycling,45,400
2026-10-03,Walking,25,120
```

## 📈 Fitness Metrics

The application calculates:

- Total number of activities
- Total workout duration
- Total calories burned
- Average activity duration
- Average calories burned per activity
- Average daily calories burned
- Activity frequency
- First-to-last day calorie change percentage

## 📚 What I Learned

Through this project, I learned how to:

- Build a menu-driven Python application.
- Apply OOP concepts to organize program functionality.
- Store and manage datasets using CSV files.
- Perform numerical calculations with NumPy.
- Clean, filter, group, and analyze data using Pandas.
- Calculate fitness metrics and summarize activity records.
- Create charts using Matplotlib and Seaborn.
- Validate user input and handle exceptions.
- Analyze relationships between workout duration and calories burned.

## 🎯 Project Objective

The objective of this project is to develop a fitness tracking application that combines Python programming, data analysis, and data visualization to help users understand their physical activity patterns and monitor fitness progress.

## 👨‍💻 Author

**Laksh Prajapat**

BCA Student | Python & AI/ML Learner

---

⭐ If you find this project useful, consider giving the repository a star!

