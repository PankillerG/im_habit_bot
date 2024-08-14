START = """
Welcome to @im_habit_bot. It\'s easy to controll your habits. Use:
- /add - to add new habit.
- /remove - to remove habit. Then click on the habit to remove it.
- /show - to show all your actual habits. The bot will always show actual habits, even if the habit period has been updated (for example, new day/week/month has come). Then click on the habit to mark it as completed.
- /show_all - to show all habits.
- /reset_all - reser all your data
Just try and get high!
"""

HELP = START

WAITING_FOR_HABIT_NAME = """
Write the habit name:
"""

WAITING_FOR_HABIT_RESET_FREQ = """
Select reset frequency for {habit_name}
"""

WAITING_FOR_HABIT_GOAL_COUNT = """
Select goal count for {habit_name} per {habit_reset_freq}
"""

HABIT_HAS_BEEN_ADDED = """
Habit has been added:
Name: {habit_name}
Reset frequency: {habit_reset_freq}
Goal count: {habit_goal_count}

Use:
- /add - to add more habits
- /remove - to remove habits
- /show - to show actual habits
"""

SHOW_HABITS = """
Click on habits to make it done
"""

SHOW_EMPTY_HABITS = """
You don't have any habits right now. Use /add command to add them.
"""

REMOVE_HABITS = """
Click on habit to remove
"""

RESET_ALL = """
You just reseted all your data!

Use /start to begin!
"""


def get_show_habits(empty=False):
    return SHOW_EMPTY_HABITS if empty else SHOW_HABITS


def get_remove_habits(empty=False):
    return SHOW_EMPTY_HABITS if empty else REMOVE_HABITS
