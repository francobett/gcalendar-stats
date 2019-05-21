from __future__ import print_function
import copy
import datetime
import dateutil.parser
import sys

from constants import (
    events_dict,
    team_general,
)
from gcalendarAPI import get_gc_creds
from helpers import export_results_to_csv


def main(days, team_label):
    """
    Get data about your events in your G Calendar
    """
    data = {}
    teams_fields = [team_general, team_label]
    for team in teams_fields:
        data[team] = copy.deepcopy(events_dict)

    gcalendar = get_gc_creds()

    now = datetime.datetime.now()
    min_date = now - datetime.timedelta(days=days)

    # Call the Calendar API
    events_result = gcalendar.events().list(
        calendarId='primary',
        timeMin=min_date.isoformat() + 'Z',
        timeMax=now.isoformat() + 'Z',
        singleEvents=True,
        orderBy='startTime',
    ).execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
        return

    # TODO optimize this FOR statement
    for event in events:
        # avoid events when guests can't see others.
        if not event.get('guestsCanSeeOtherGuests', True):
            continue
        for attendee in event.get('attendees', []):
            # Get your info about the event
            if attendee.get('self'):
                data[team_general][attendee['responseStatus']]['names'].append(
                    event['summary']
                )
                data[team_general]['total']['names'].append(
                    event['summary']
                )
                start = event['start'].get('dateTime',)
                end = event['end'].get('dateTime',)
                if start and end:
                    duration = (
                        dateutil.parser.parse(end) - dateutil.parser.parse(start)
                    ).total_seconds() / 3600
                    data[team_general]['total']['time'] += duration
                    data[team_general][attendee['responseStatus']]['time'] += duration

                # Stats for the team label
                if event['organizer'].get('displayName') == team_label:
                    data[team_label]['total']['names'].append(
                        event['summary']
                    )
                    data[team_label]['total']['time'] += duration
                    data[team_label][attendee['responseStatus']]['names'].append(
                        event['summary']
                    )
                    data[team_label][attendee['responseStatus']]['time'] += duration

    export_results_to_csv(
        data,
        days,
        teams_fields,
        now,
    )


if __name__ == '__main__':
    try:
        days = int(sys.argv[1])
    except IndexError:
        days = 14
    try:
        team_label = str(sys.argv[2])
    except IndexError:
        team_label = 'xDev meetings'

    main(days, team_label)
