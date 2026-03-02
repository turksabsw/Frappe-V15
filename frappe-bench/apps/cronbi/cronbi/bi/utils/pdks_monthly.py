import frappe
from datetime import date
from calendar import monthrange

DAILY_REQUIRED_HOURS = 9
DAILY_REQUIRED_MINUTES = DAILY_REQUIRED_HOURS * 60


def calculate_pdks_monthly(year: int, month: int):
    total_days = monthrange(year, month)[1]
    start_date = date(year, month, 1)
    end_date = date(year, month, total_days)

    workdays = [
        date(year, month, d)
        for d in range(1, total_days + 1)
        if date(year, month, d).weekday() < 5
    ]

    if not workdays:
        return []

    checkins = frappe.db.get_all(
        "Daily Checkin",
        filters={"date": ["between", [start_date, end_date]]},
        fields=["user_email", "date", "work_duration_minutes"]
    )

    if not checkins:
        return []

    users = {}
    for c in checkins:
        users.setdefault(c.user_email, {}).setdefault(c.date, []).append(c)

    results = []

    for user_email, days in users.items():
        present_days = 0
        absent_days = 0
        worked_minutes_total = 0
        missing_minutes_total = 0
        early_exit_count = 0

        for day in workdays:
            day_logs = days.get(day)

            if not day_logs:
                absent_days += 1
                missing_minutes_total += DAILY_REQUIRED_MINUTES
                continue

            worked_minutes = sum((log.work_duration_minutes or 0) for log in day_logs)

            if worked_minutes <= 0:
                absent_days += 1
                missing_minutes_total += DAILY_REQUIRED_MINUTES
                continue

            present_days += 1
            worked_minutes_total += worked_minutes

            daily_missing = max(0, DAILY_REQUIRED_MINUTES - worked_minutes)
            if daily_missing > 0:
                early_exit_count += 1
                missing_minutes_total += daily_missing

        missing_hours = missing_minutes_total / 60
        deduction_days = int(missing_hours // DAILY_REQUIRED_HOURS)
        deduction_hours = round(missing_hours % DAILY_REQUIRED_HOURS, 2)

        #  AYRI SATIR MANTIĞI
        if deduction_days > 0:
            results.append({
                "user_email": user_email,
                "deduction_type": "Day",
                "deduction_value": deduction_days,
                "present_days": present_days,
                "absent_days": absent_days,
                "worked_hours": round(worked_minutes_total / 60, 2),
                "missing_hours": round(missing_hours, 2),
                "early_exit_count": early_exit_count,
            })

        if deduction_hours > 0:
            results.append({
                "user_email": user_email,
                "deduction_type": "Hour",
                "deduction_value": deduction_hours,
                "present_days": present_days,
                "absent_days": absent_days,
                "worked_hours": round(worked_minutes_total / 60, 2),
                "missing_hours": round(missing_hours, 2),
                "early_exit_count": early_exit_count,
            })

        if deduction_days == 0 and deduction_hours == 0:
            results.append({
                "user_email": user_email,
                "deduction_type": "None",
                "deduction_value": 0,
                "present_days": present_days,
                "absent_days": absent_days,
                "worked_hours": round(worked_minutes_total / 60, 2),
                "missing_hours": 0,
                "early_exit_count": early_exit_count,
            })

    return results
