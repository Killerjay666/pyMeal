from datetime import datetime, timedelta, UTC

from meal import Meal


def generate_ics(meals):
    ics_content = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Dish Dealer//Meal Calendar//EN\n\n"
    ]

    weekdays = ["MO", "TU", "WE", "TH", "FR", "SA", "SU"]

    # Always start on Monday, starting next Monday
    start_date = datetime.now(UTC)
    while start_date.weekday() != 0:
        start_date += timedelta(days=1)

    for i, meal in enumerate(meals):
        event_date = start_date + timedelta(days=i)

        event = [
            "BEGIN:VEVENT",
            f"UID:{meal.name}@dishdealer",
            f"DTSTAMP:{datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')}",
            f"DTSTART;VALUE=DATE:{event_date.strftime('%Y%m%d')}",
            f"SUMMARY:{meal.name}",
            f"RRULE:FREQ=WEEKLY;INTERVAL={meal.frequency};BYDAY={weekdays[event_date.weekday()]}",
            f"DESCRIPTION:{meal.url}",
            "END:VEVENT\n"
        ]
        ics_content.extend(event)

    ics_content.append("\nEND:VCALENDAR")
    return "\n".join(ics_content)

if __name__ == '__main__':
    from example_meals import meals
    ics_file_content = generate_ics(meals)

    # Write to file
    with open("meal_plan.ics", "w") as f:
        f.write(ics_file_content)
