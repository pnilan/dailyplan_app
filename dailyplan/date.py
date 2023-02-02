from datetime import datetime, date

def add_suffix(d):
	if 11 <= d <13:
		return f"{d}th"
	last_digit = d % 10
	if last_digit == 1:
		return f"{d}st"
	elif last_digit == 2:
		return f"{d}nd"
	elif last_digit == 3:
		return f"{d}rd"
	else:
		return f"{d}th"

def date_to_text(date_string, date_format="%m/%d/%Y"):
	day = datetime.strptime(date_string, date_format).day
	return datetime.strptime(date_string, date_format).strftime(f'%A %B {add_suffix(day)}')
