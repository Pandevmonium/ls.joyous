# ------------------------------------------------------------------------------
# Joyous template tags
# ------------------------------------------------------------------------------
import datetime as dt
import calendar
from django import template
from ..utils.telltime import timeFormat, dateFormat
from ..models import getAllEventsByDay
from ..models import getAllUpcomingEvents
from ..models import getGroupUpcomingEvents
from ..models import getAllEventsByWeek
from ..models import CalendarPage
from ..utils.weeks import weekday_abbr, weekday_name

register = template.Library()

@register.inclusion_tag('joyous/tags/events_this_week.html')
def events_this_week():
    today = dt.date.today()
    begin_ord = today.toordinal()
    if today.weekday() != 6:
        # Start week with Monday, unless today is Sunday
        begin_ord -= today.weekday()
    end_ord = begin_ord + 6
    date_from = dt.date.fromordinal(begin_ord)
    date_to   = dt.date.fromordinal(end_ord)
    events = getAllEventsByDay(date_from, date_to)
    return {'events': events, 'today':  today }

@register.inclusion_tag('joyous/tags/minicalendar.html',
                        takes_context=True)
def minicalendar(context):
    today = dt.date.today()
    request = context['request']
    home = request.site.root_page
    cal = CalendarPage.objects.live().descendant_of(home).first()
    calUrl = cal.get_url(request) if cal else None
    return {'today':           today,
            'yesterday':       today - dt.timedelta(1),
            'lastweek':        today - dt.timedelta(7),
            'year':            today.year,
            'calendarUrl':     calUrl,
            'monthName':       calendar.month_name[today.month],
            'weekdayInfo':     zip(weekday_abbr, weekday_name),
            'events':          getAllEventsByWeek(today.year, today.month)}

@register.inclusion_tag('joyous/tags/upcoming_events_detailed.html')
def all_upcoming_events():
    return {'events': getAllUpcomingEvents()}

@register.inclusion_tag('joyous/tags/upcoming_events_detailed.html',
                        takes_context=True)
def subsite_upcoming_events(context):
    home = context['request'].site.root_page
    return {'events': getAllUpcomingEvents(home)}

@register.inclusion_tag('joyous/tags/upcoming_events_list.html',
                        takes_context=True)
def group_upcoming_events(context):
    page = context.get('page')
    events = getGroupUpcomingEvents(page) if page is not None else []
    return {'events': events}

# Format times and dates e.g. on event page
@register.filter
def time_display(time):
    return timeFormat(time)

@register.filter
def at_time_display(time):
    return timeFormat(time, prefix="at ")

@register.filter
def date_display(date):
    return dateFormat(date)

