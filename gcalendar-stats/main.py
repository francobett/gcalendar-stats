from __future__ import print_function
import datetime
import dateutil.parser

from constants import events_status
from gcalendarAPI import get_gc_creds


def main():
    """
    Get data about your events in your G Calendar
    """
    # TODO convert this var as arguments for the command call
    days = 14
    team_label = 'xDev meetings'
    work_hours = 8 * days

    gcalendar = get_gc_creds()

    # Call the Calendar API
    now = datetime.datetime.now()
    min_date = now - datetime.timedelta(days=days)
    print('Events from: {} to : {}'.format(
        now.strftime("%H:%M:%S - %d, %b %Y"),
        min_date.strftime("%H:%M:%S - %d, %b %Y"),
    ))

    events_result = gcalendar.events().list(
        calendarId='primary',
        timeMin=min_date.isoformat() + 'Z',
        timeMax=now.isoformat() + 'Z',
        singleEvents=True,
        orderBy='startTime',
    ).execute()
    events = events_result.get('items', [])

    team_events_status = events_status.copy()

    if not events:
        print('No upcoming events found.')
        return

    # TODO optimize this FOR statement
    for event in events:
        # avoid events when guests can see others.
        if not event.get('guestsCanSeeOtherGuests', True):
            continue
        for attendee in event.get('attendees', []):
            # Get your info about the event
            if attendee.get('self'):
                events_status[attendee['responseStatus']]['names'].append(
                    event['summary']
                )
                start = event['start'].get('dateTime',)
                end = event['end'].get('dateTime',)
                if start and end:
                    duration = (
                        dateutil.parser.parse(end) - dateutil.parser.parse(start)
                    ).total_seconds() / 3600
                    events_status[attendee['responseStatus']]['time'] += duration

                # Stats for the team label
                if event['organizer'].get('displayName') == team_label:
                    team_events_status['total'] += 1
                    team_events_status[attendee['responseStatus']]['names'].append(
                        event['summary']
                    )
                    team_events_status[attendee['responseStatus']]['time'] += duration

    # TODO optimize print
    # TODO send this result to a .csv
    # Show results

    print('Work hours {}'.format(work_hours))
    print('% of your time with accepted meetings: {:.2f}%'.format(
        events_status['accepted']['time'] / work_hours * 100
    ))
    print('% of your time with accepted meetings: {:.2f}%'.format(
        team_events_status['accepted']['time'] / work_hours * 100
    ))
    print('GENERAL Calendar stats in the last {} days'.format(
        days,
    ))
    print('COUNT \n\nTOTAL: {} \n CONFIRMED:{} \n DECLINED:{} \n MAYBE:{} \n NO RESPONDED:{} \n'.format(
        len(events),
        len(events_status['accepted']['names']),
        len(events_status['declined']['names']),
        len(events_status['tentative']['names']),
        len(events_status['needsAction']['names']),
    ))
    print('HOURS \n \n CONFIRMED:{} \n DECLINED:{} \n MAYBE:{} \n NO RESPONDED:{} \n'.format(
        events_status['accepted']['time'],
        events_status['declined']['time'],
        events_status['tentative']['time'],
        events_status['needsAction']['time'],
    ))

    print('TEAM: {} Calendar stats in the last {} days'.format(
        team_label,
        days,
    ))
    print('COUNT \n\nTOTAL: {} \n CONFIRMED:{} \n DECLINED:{} \n MAYBE:{} \n NO RESPONDED:{} \n'.format(
        team_events_status['total'],
        len(team_events_status['accepted']['names']),
        len(team_events_status['declined']['names']),
        len(team_events_status['tentative']['names']),
        len(team_events_status['needsAction']['names']),
    ))
    print('HOURS \n \n CONFIRMED:{} \n DECLINED:{} \n MAYBE:{} \n NO RESPONDED:{} \n'.format(
        team_events_status['accepted']['time'],
        team_events_status['declined']['time'],
        team_events_status['tentative']['time'],
        team_events_status['needsAction']['time'],
    ))


if __name__ == '__main__':
    main()
