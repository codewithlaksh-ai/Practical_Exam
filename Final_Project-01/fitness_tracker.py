# Personal Fitness Tracker Dashboard
from datetime import datetime

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

DATA_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "fitness_activities.csv"
)


COLUMNS = [
    "Date",
    "Activity Type",
    "Duration (Minutes)",
    "Calories Burned",
]


class FitnessTracker:

    def __init__(self, filename=DATA_FILE):
        self.filename = filename
        self.df = self.load_data()

    def load_data(self):
        if not os.path.exists(self.filename):
            df = pd.DataFrame(columns=COLUMNS)
            df.to_csv(self.filename, index=False)
            return df

        try:
            df = pd.read_csv(self.filename)
        except (pd.errors.EmptyDataError, pd.errors.ParserError, OSError) as error:
            print(f"Could not read dataset: {error}")
            return pd.DataFrame(columns=COLUMNS)

        for column in COLUMNS:
            if column not in df.columns:
                df[column] = pd.NA

        df = df[COLUMNS].copy()
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df["Activity Type"] = df["Activity Type"].astype("string").str.strip()
        df["Duration (Minutes)"] = pd.to_numeric(
            df["Duration (Minutes)"], errors="coerce"
        )
        df["Calories Burned"] = pd.to_numeric(
            df["Calories Burned"], errors="coerce"
        )

        valid = (
            df["Date"].notna()
            & df["Activity Type"].notna()
            & df["Activity Type"].ne("")
            & df["Duration (Minutes)"].gt(0)
            & df["Calories Burned"].gt(0)
        )
        removed = len(df) - int(valid.sum())
        df = df.loc[valid].copy()

        df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")
        df["Duration (Minutes)"] = df["Duration (Minutes)"].astype(float)
        df["Calories Burned"] = df["Calories Burned"].astype(float)

        if removed:
            print(f"Note: Removed {removed} invalid row(s) from the dataset.")

        return df.reset_index(drop=True)

    def save_data(self):
        self.df.to_csv(self.filename, index=False)

    def log_activity(self, activity_type, duration, calories, date=None):
        activity_type = str(activity_type).strip()

        if not activity_type:
            print("Error: Activity type cannot be empty.")
            return False

        try:
            duration = float(duration)
            calories = float(calories)
        except (TypeError, ValueError):
            print("Error: Duration and calories must be numbers.")
            return False

        if not np.isfinite(duration) or duration <= 0:
            print("Error: Duration must be a positive number.")
            return False

        if not np.isfinite(calories) or calories <= 0:
            print("Error: Calories must be a positive number.")
            return False

        if date is None or str(date).strip() == "":
            date = datetime.now().strftime("%Y-%m-%d")

        try:
            date = pd.to_datetime(date, errors="raise").strftime("%Y-%m-%d")
        except (ValueError, TypeError):
            print("Error: Enter a valid date in YYYY-MM-DD format.")
            return False

        new_activity = pd.DataFrame(
            [{
                "Date": date,
                "Activity Type": activity_type.title(),
                "Duration (Minutes)": duration,
                "Calories Burned": calories,
            }]
        )

        self.df = pd.concat([self.df, new_activity], ignore_index=True)
        self.save_data()
        print("Activity logged successfully!")
        return True

    def calculate_metrics(self):
        if self.df.empty:
            print("No activity data available to analyze.")
            return {}

        durations = self.df["Duration (Minutes)"].to_numpy(dtype=float)
        calories = self.df["Calories Burned"].to_numpy(dtype=float)

        daily = self.df.groupby("Date", as_index=False).agg(
            Daily_Calories=("Calories Burned", "sum"),
            Daily_Duration=("Duration (Minutes)", "sum"),
        )

        weekly = self.df.copy()
        weekly["Date"] = pd.to_datetime(weekly["Date"])
        weekly = weekly.set_index("Date").resample("W").agg({
        "Duration (Minutes)": "sum",
        "Calories Burned": "sum" })

        print("\nWeekly Fitness Trends:")
        print(weekly,"\n")

        metrics = {
            "total_activities": len(self.df),
            "total_duration": float(np.sum(durations)),
            "total_calories": float(np.sum(calories)),
            "average_duration": float(np.mean(durations)),
            "average_calories": float(np.mean(calories)),
            "average_daily_calories": float(np.mean(daily["Daily_Calories"])),
            "activity_frequency": self.df["Activity Type"].value_counts(),
            "daily_summary": daily,
        }
        
        daily_sorted = daily.sort_values("Date")
        first = float(daily_sorted.iloc[0]["Daily_Calories"])
        last = float(daily_sorted.iloc[-1]["Daily_Calories"])

        if first != 0:
            metrics["calorie_change_percent"] = ((last - first) / first) * 100
        else:
            metrics["calorie_change_percent"] = None

        return metrics

    def filter_activities(self, condition=None, start_date=None, end_date=None):
        filtered = self.df.copy()

        if condition and str(condition).strip():
            filtered = filtered[
                filtered["Activity Type"].str.casefold()
                == str(condition).strip().casefold()
            ]

        if start_date:
            try:
                start = pd.to_datetime(start_date, errors="raise").strftime("%Y-%m-%d")
            except (ValueError, TypeError):
                print("Error: Invalid start date.")
                return pd.DataFrame(columns=COLUMNS)
            filtered = filtered[filtered["Date"] >= start]

        if end_date:
            try:
                end = pd.to_datetime(end_date, errors="raise").strftime("%Y-%m-%d")
            except (ValueError, TypeError):
                print("Error: Invalid end date.")
                return pd.DataFrame(columns=COLUMNS)
            filtered = filtered[filtered["Date"] <= end]

        if start_date and end_date and start_date > end_date:
            print("Error: Start date must not be after end date.")
            return pd.DataFrame(columns=COLUMNS)

        return filtered.reset_index(drop=True)

    def generate_report(self):
        metrics = self.calculate_metrics()

        if not metrics:
            return

        print("\n" + "=" * 42)
        print("          PERSONAL FITNESS REPORT")
        print("=" * 42)
        print(f"Total activities       : {metrics['total_activities']}")
        print(f"Total duration         : {metrics['total_duration']:.1f} minutes")
        print(f"Total calories burned  : {metrics['total_calories']:.1f} kcal")
        print(f"Average activity time  : {metrics['average_duration']:.1f} minutes")
        print(f"Average calories       : {metrics['average_calories']:.1f} kcal/activity")
        print(f"Average daily calories : {metrics['average_daily_calories']:.1f} kcal")

        if metrics["calorie_change_percent"] is not None:
            change = metrics["calorie_change_percent"]
            print(f"First-to-last day change: {change:+.1f}%")
        else:
            print("First-to-last day change: Not available")

        print("\nActivity frequency:")
        for activity, count in metrics["activity_frequency"].items():
            print(f"  {activity}: {count}")

        report_df = self.df.copy()
        report_df["Calories per Minute"] = (
            report_df["Calories Burned"] / report_df["Duration (Minutes)"]
        )
        print("\nActivity totals:")
        summary = report_df.groupby("Activity Type").agg(
            Total_Minutes=("Duration (Minutes)", "sum"),
            Total_Calories=("Calories Burned", "sum"),
            Calories_Per_Minute=("Calories per Minute", "mean"),
        )
        print(summary.round(2).to_string())
        print("=" * 42)

    def show_filter(self):
        print("\nLeave a field blank to skip that filter.")
        activity = input("Activity type (e.g. Running): ").strip()
        start_date = input("Start date YYYY-MM-DD: ").strip()
        end_date = input("End date YYYY-MM-DD: ").strip()

        result = self.filter_activities(
            condition=activity or None,
            start_date=start_date or None,
            end_date=end_date or None,
        )

        if result.empty:
            print("No matching activities found.")
        else:
            print("\nFiltered activities:")
            print(result.to_string(index=False))

    def visualize(self):
        if self.df.empty:
            print("No data available. Add activities before creating charts.")
            return

        df = self.df.copy()
        df["Date"] = pd.to_datetime(df["Date"])
        df["Calories per Minute"] = (
            df["Calories Burned"] / df["Duration (Minutes)"]
        )

        sns.set_theme(style="whitegrid")
        fig, axes = plt.subplots(2, 2, figsize=(16, 10))
        fig.suptitle("Personal Fitness Tracker Dashboard", fontsize=18, fontweight="bold")

        # 1. Bar chart: total time per activity type.
        activity_time = df.groupby("Activity Type")["Duration (Minutes)"].sum()
        activity_time.plot(kind="bar", ax=axes[0, 0])
        axes[0, 0].set_title("Total Time by Activity", fontsize=13, pad=15)
        axes[0, 0].set_xlabel("Activity Type")
        axes[0, 0].set_ylabel("Minutes")
        axes[0, 0].tick_params(axis="x", rotation=25)

        # 2. Line graph: calories burned by date.
        daily_calories = df.groupby("Date")["Calories Burned"].sum().sort_index()
        axes[0, 1].plot(daily_calories.index, daily_calories.values, marker="o", label="Calories burned",)
        
        axes[0, 1].set_title("Calories Burned Over Time", fontsize=13, pad=15)
        axes[0, 1].set_xlabel("Date",  labelpad=8)
        axes[0, 1].set_ylabel("Calories",  labelpad=8)
        axes[0, 1].legend()
        axes[0, 1].tick_params(axis="x",  labelrotation=30)

        # 3. Pie chart: percentage of total duration by activity type.
        activity_time.plot(kind="pie", autopct="%1.1f%%", ax=axes[1, 0])
        axes[1, 0].set_title("Activity Duration Distribution", fontsize=13, pad=15)
        axes[1, 0].set_ylabel("")

        # 4. Heatmap: correlation between duration and calories.
        correlation = df[["Duration (Minutes)", "Calories Burned"]].corr()
        if df["Duration (Minutes)"].nunique() > 1 and df["Calories Burned"].nunique() > 1:
            sns.heatmap(correlation, annot=True, cmap="coolwarm", vmin=-1, vmax=1, ax=axes[1, 1], )
            axes[1, 1].set_title("Duration vs Calories Correlation")
        else:
            axes[1, 1].text(
                0.5, 0.5,
                "Not enough variation for correlation",
                ha="center", va="center",
            )
            axes[1, 1].set_title("Duration vs Calories Correlation", fontsize=13, pad=15)
            axes[1, 1].set_xticks([])
            axes[1, 1].set_yticks([])

        fig.subplots_adjust(left=0.08, right=0.96, top=0.90, bottom=0.10, hspace=0.55, wspace=0.25 )
        plt.show()



def get_positive_number(prompt):
    while True:
        value = input(prompt).strip()
        try:
            number = float(value)
            if np.isfinite(number) and number > 0:
                return number
            print("Please enter a number greater than zero.")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")


def main():
    tracker = FitnessTracker()

    while True:
        print("\n====== PERSONAL FITNESS TRACKER ======")
        print("1. Log a new activity")
        print("2. Calculate metrics")
        print("3. Filter activities")
        print("4. Generate fitness report")
        print("5. Show dashboard charts")
        print("6. View all activities")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            activity = input("Enter activity type: ").strip()
            duration = get_positive_number("Enter duration in minutes: ")
            calories = get_positive_number("Enter calories burned: ")
            date = input("Enter date YYYY-MM-DD (blank for today): ").strip()
            tracker.log_activity(activity, duration, calories, date or None)

        elif choice == "2":
            metrics = tracker.calculate_metrics()
            if metrics:
                print(f"Total calories: {metrics['total_calories']:.1f} kcal")
                print(f"Average duration: {metrics['average_duration']:.1f} minutes")
                print(f"Average daily calories: {metrics['average_daily_calories']:.1f} kcal")

        elif choice == "3":
            tracker.show_filter()

        elif choice == "4":
            tracker.generate_report()

        elif choice == "5":
            tracker.visualize()

        elif choice == "6":
            if tracker.df.empty:
                print("No activities recorded yet.")
            else:
                print(tracker.df.to_string(index=False))

        elif choice == "7":
            print("Thank you for using Personal Fitness Tracker!")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 7.")


if __name__ == "__main__":
    main()

