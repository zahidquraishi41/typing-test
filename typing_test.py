from datetime import datetime as dt
from collections import defaultdict


class TypingTest:
    def __init__(self) -> None:
        self._start_time = None
        self._key_record = defaultdict(lambda: 0)

    def start_timer(self) -> dt:
        self._start_time = dt.now()

    def get_wpm(self, user_input: str) -> int:
        stop_time = dt.now()
        time_taken = (stop_time - self._start_time).total_seconds()
        if time_taken < 2:
            return 0
        words = len(user_input.split(' '))
        return int((words / time_taken) * 60)

    def time_taken(self) -> str:
        stop_time = dt.now()
        time_taken = str(stop_time - self._start_time).rsplit('.')[0]
        return time_taken

    def difficult_keys(self, user_input, actual_text):
        if not user_input:
            return
        i = len(user_input) - 1
        if user_input[i] != actual_text[i]:
            self._key_record[actual_text[i]] += 1
        sorted_keys = sorted(self._key_record.items(),
                             key=lambda x: x[1], reverse=True)
        top3 = sorted_keys[:3]
        val = ''
        for k, v in top3:
            val += f'{k}({v}), '
        return val[:-2]

    @classmethod
    def measure_accuracy(cls, user_input, text_to_type) -> int:
        if len(user_input) == 0:
            return 100
        accuracy = 100
        count = 0
        dec = 100 / len(user_input)
        for i in range(len(user_input)):
            if user_input[i] != text_to_type[i]:
                accuracy -= dec
                count += 1
        return int(accuracy)
