import csv
from django.contrib import messages
from django.conf import settings
from django.core.files import File
from .models import Event
from datetime import datetime
import logging
import os

logger = logging.getLogger(__name__)


def validate_and_convert_datetime(date_time_str):
    try:
        # Assuming the datetime string is in the format "YYYY-MM-DD HH:MM:SS"
        date_time_obj = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
        return date_time_obj
    except ValueError:
        raise ValueError("Incorrect date_time format, should be YYYY-MM-DD HH:MM:SS")


# Usage
try:
    converted_date_time = validate_and_convert_datetime("2023-09-06 14:30:59")
    print("Converted datetime:", converted_date_time)
except ValueError as e:
    print(e)


def parse_csv(csv_file, request):
    events = []
    csv_reader = csv.DictReader(csv_file.read().decode('utf-8').splitlines())

    for row in csv_reader:
        row = {k.lower(): v for k, v in row.items()}

        # Check if event with this name already exists
        existing_event = Event.objects.filter(name=row['name']).first()

        if existing_event:
            print(f"Event with name {row['name']} already exists.")
            messages.warning(request, f"Event with name {row['name']} already exists. Skipping.")
            continue

        event = Event()
        event.name = row['name']

        try:
            event.date_time = validate_and_convert_datetime(row['date_time'])
        except ValueError as e:
            print(f"Skipping row due to error: {e}")
            continue
        event.location = row['location']
        event.description = row['description']
        event.max_participants = int(row['max_participants'])
        event.event_type = row['event_type']

        image_path = row.get('image_path', '').strip()

        if image_path:
            full_image_path = os.path.join(settings.BASE_DIR, image_path)
            try:
                with open(full_image_path, 'rb') as f:
                    event.image.save(os.path.basename(full_image_path), File(f))
            except Exception as e:
                print(f"Error opening image file {full_image_path}: {e}")
                logger.error(f"Error opening image file {image_path}: {e}")
                event.image = 'default_image.png'

        event.save()
        events.append(event)

    return events