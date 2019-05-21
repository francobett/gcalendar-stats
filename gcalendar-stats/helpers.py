import csv
import datetime

from constants import (
    csv_fields,
    events_states,
)


def export_results_to_csv(
    data,
    days,
    teams_fields,
    now,
):
    # TODO optimize csv export

    work_hours = 8 * days
    min_date = now - datetime.timedelta(days=days)

    with open(
        './results/calendar_stats_{}.csv'.format(
            now.strftime('%m-%d-%y_%H:%M:%S')
        ),
        mode='w',
    ) as csv_file:
        w = csv.DictWriter(csv_file, fieldnames=csv_fields)
        # General fields
        w.writerow({
            csv_fields[0]: 'From'.format(
                min_date.strftime("%H:%M:%S - %d, %b %Y")
            ),
            csv_fields[1]: 'To:'.format(
                now.strftime("%H:%M:%S - %d, %b %Y"),
            ),
            csv_fields[2]: 'Work hours: {}'.format(work_hours),
        })

        for team in data.keys():
            w.writerow({csv_fields[0]: team})
            w.writeheader()

            for state in events_states:
                w.writerow({
                    csv_fields[0]: state,
                    csv_fields[1]: len(data[team][state]['names']),
                    csv_fields[2]: data[team][state]['time'],
                    csv_fields[3]: data[team][state]['time'] / work_hours * 100,
                })
