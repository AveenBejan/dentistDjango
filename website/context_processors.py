from datetime import datetime, timedelta  # Import datetime and timedelta
from random import choice  # Import choice from the random module
from .models import Reception1  # Adjust based on your model location


def appointment_context(request):
    # Retrieve 'gave' records within the last 24 hours
    current_time = datetime.now()
    gaves1 = Reception1.objects.filter(app_data__gte=current_time - timedelta(hours=360)).order_by('-id')
    week_days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

    # List of potential colors
    color_choices = ['#FF5733', '#33FF57', '#3357FF', '#FF33A8', '#A833FF']

    # Assign random colors to each time entry
    for gave in gaves1:
        if gave.time:
            times = gave.time.strip("[]").split(",")  # Assuming times are comma-separated
            gave.time_colors = [(time.strip(), choice(color_choices)) for time in times]  # Random color for each time

    # Clean 'gave' data if needed
    for gave in gaves1:
        if gave.days:
            gave.days = gave.days.replace("'", "")
        if gave.time:
            gave.time = gave.time.replace("'", "")

    return {
        'gaves1': gaves1,
        'week_days': week_days,
    }