from datetime import datetime

import pytz

tz = pytz.timezone('Africa/Lagos')


def default(request):
    now = datetime.now(tz)
    if 0 < now.hour <= 12:
        time_of_day = "morning"
    elif 12 < now.hour <= 17:
        time_of_day = "afternoon"
    else:
        time_of_day = "evening"

    default_context = {
        'time_of_day': time_of_day,
    }

    if request.user and request.user.is_authenticated:
        default_context['user'] = request.user

    return default_context
