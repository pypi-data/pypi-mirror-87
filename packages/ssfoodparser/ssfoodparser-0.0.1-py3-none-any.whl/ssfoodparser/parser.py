#!/usr/bin/env python3
import datetime
import requests
import re
from ics import Calendar

class FoodSheetParser:

    def __init__(self, key):
        self.food = {}
        self.key = key
        self.calendar = self.download_ical(key)

    def download_ical(self, key):
        calendar = Calendar(requests.get("https://sms.schoolsoft.se/nti/jsp/public/right_public_student_ical.jsp?key=" + key).text)
        self.calendar = calendar
        return calendar

    def get_week_food(self, week_num):
        events = list(self.calendar.timeline)

        food = {}
        for e in events:
            _, week, day = e.uid.split("-")
            if int(week_num) == int(week):
                desc = e.description[e.description.index("lunch")+6:].replace("\n", "")
                if not day in food:
                    food[day] = {"standard": None, "veggie": None}

                if "vegetariska" in e.description:
                    food[day]["veggie"] = desc
                else:
                    food[day]["standard"] = desc
        self.food = food
        return food

    def get_current_week_food(self):
        today = datetime.date.today()
        _, week_num, _ = today.isocalendar()
        food = self.get_week_food(week_num)
        return food
