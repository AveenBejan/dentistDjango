from datetime import datetime, timedelta  # Import datetime and timedelta
from random import choice  # Import choice from the random module
from .models import Reception1  # Adjust based on your model location
import random


def appointment_context(request):
    # Get the current time
    current_time = datetime.now()

    # Calculate the end time for the next 15 days
    end_time = current_time + timedelta(days=15)

    # Retrieve 'gave' records for the next 15 days
    gaves1 = Reception1.objects.filter(app_data__gte=current_time, app_data__lte=end_time).order_by('-id')

    # Define the week days
    week_days = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    # List of potential colors
    color_choices = ['#FF5733', '#33FF57', '#3357FF', '#FF33A8', '#A833FF']

    # Assign random colors to each time entry
    for gave in gaves1:
        if gave.time:
            times = gave.time.strip("[]").split(",")  # Assuming times are comma-separated
            # Assign a random color from color_choices for each time
            gave.time_colors = [(time.strip(), random.choice(color_choices)) for time in times]

    # Clean 'gave' data if needed
    for gave in gaves1:
        if gave.days:
            gave.days = gave.days.replace("'", "")
        if gave.time:
            gave.time = gave.time.replace("'", "")

    # Render the template with the filtered data

    # Return context data for template rendering
    return {
        'gaves1': gaves1,
        'week_days': week_days,
    }