import datetime as dt
import re
from enum import Enum


class SetupStage(str, Enum):
    Schedule = "Schedule"
    Categories = "Categories"
    Sources = "Sources"
    Finished = "Finished"


class ScheduleSetupStage(str, Enum):
    Days = "Days"
    Time = "Time"
    Finish = "Finish"


class TimeParsingError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class UserSettingsBuilder:
    def __init__(self):
        self._schedule = {
            "Пн": None,
            "Вт": None,
            "Ср": None,
            "Чт": None,
            "Пт": None,
            "Сб": None,
            "Вс": None,
        }
        self._categories = None
        self._sources = None

    @property
    def schedule(self):
        return self._schedule

    @schedule.setter
    def schedule(self, value):
        self._schedule = value

    @property
    def categories(self):
        return self._categories

    @property
    def sources(self):
        return self._sources

    def is_schedule_setup_finished(self):
        return any(self._schedule.values())

    def is_categories_setup_finished(self):
        return self._categories is not None

    def is_sources_setup_finished(self):
        return self._sources is not None

    def is_setup_finished(self):
        return (
            self.is_schedule_setup_finished()
            and self.is_categories_setup_finished()
            and self.is_sources_setup_finished()
        )

    def update_schedule_time(self, message: str):
        results = self.__parse_time_text(message)
        if len(results) == 1:
            print(self._schedule.keys())
            self._schedule = {
                k: (results[0] if v is not None else None) for k, v in self._schedule.items()
            }
            print(self._schedule.keys())
            return

        old_schedule = self._schedule.copy()
        i = 0
        keys = list(self._schedule.keys())
        for k in keys:
            if self._schedule[k] is None:
                continue
            if i >= len(results):
                self._schedule = old_schedule
                raise TimeParsingError()
            self._schedule[k] = results[i]
            i += 1

    def update_schedule_days(self, selected_day: list):
        print(self._schedule.keys())
        if selected_day == "Ежедневно":
            value = None if all(self._schedule.values()) else [dt.date.min]
            self._schedule = {key: value for key, _ in self._schedule.items()}
            print(self._schedule.keys())
        else:
            value = None if self._schedule[selected_day] else [dt.date.min]
            self._schedule[selected_day] = value

    def __parse_time_text(self, message: str):
        result = []
        message_lines = message.strip().splitlines()

        for i in range(len(message_lines)):
            line = message_lines[i]
            match = re.match("^каждые [0-9]+ [мч]$", line)
            if match is not None:
                _, number, unit = line.split()
                number = int(number)
                td = dt.timedelta(hours=number) if unit == "ч" else dt.timedelta(minutes=number)
                result.append(td)
                continue
            elif line == "+" and i > 0:
                result.append(result[i - 1])
                continue
            try:
                line_split = line.split(", ")
                times = sorted([dt.datetime.strptime(time, "%H:%M").time() for time in line_split])
                result.append(times)
            except Exception:
                raise TimeParsingError()
        return result
