import os


TG_BOT_TOKEN = os.getenv('TG_BOT_TOKEN')

WORK_DIR = os.getenv('PYTHONPATH')
LOGS_DIR = os.path.join(WORK_DIR, 'bin', 'logs')
STATE_FILE = os.path.join(WORK_DIR, 'bin', 'state.json')


class Jobs:
    class DumpState:
        interval = 300
        first = 300

    class ResetUsersHabits:
        interval = 60
        first = 60


AVAILABLE_HABITS_GOALS_COUNT = 31
HABITS_GOALS_COUNT_PER_KEYBOARD_ROW = 5
