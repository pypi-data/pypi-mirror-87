---
id: version-0.0.7-scripts
title: Scripts
sidebar_label: Scripts
original_id: scripts
---

There are two categories of scripts one can write when developing a SOIL application: scripts that run when something happens for example when new data arrives and scripts that run on a schedule.

The entry points for these scripts are defined in the `soil.yml` file on the top of the project.

An example syntax of the file is the following:

```yml
on_new_data:            # Defines pipeline to execute on new data arrival
    - first_script:
        path: PATH      # Path to script to execute
        partial: true   # The results are not final and are passed as input to next script
    - second_script:
        ...
    ...
    - last_script:        # Last script to be executed


schedules:              # Defines scripts that will be executed on a schedule
    - retrain:
        path: PATH1
        schedule: 0 0 * * *         # Every day at 00:00
    - delete_last_year:
        path: PATH2
        schedule: 0 0 1 1 *         # 1st Jan at 00:00
    - saturday_night_predictions:
        path: PATH3
        schedule: 30 23 * * 6       # Saturdays at 23:30 
    - update_every_5m:
        path: PATH4
        schedule: */5 * * * *       # Every 5 minutes
```

Do not manipulate the file manually, use `soil` command instead with `pipeline` and `schedule` options. It will keep the file updated and syntactically correct.

Both of them allow to list, insert or delete scripts. See `soil pipeline --help` or `soil schedule --help` for more detail.

## Adding scripts to event triggered pipelines
To add a script to an event triggered pipeline using `soil` command use the following syntax:

```bash
soil pipeline add --event EVENT_NAME [ [--after | --before] SCRIPT_NAME ] NEW_SCRIPT_NAME PATH [--partial]
```

Where:

* **EVENT_NAME** is the event which will trigger the pipeline containing the script. For now, the only event available is `on_new_data`.
* **SCRIPT_NAME** is the name of an exsting script in the pipeline that will precede (if used with `--after`) or succeed (if used with `--before`) the inserted script.
* **NEW_SCRIPT_NAME** is the name of the inserted script in the pipeline. If no name is provided, the script filename will be used.
* **PATH** is the path of the script to insert.

## Adding scheduled scripts
In the same way, to add a scheduled script using `soil` command use:

```bash
soil schedule add SCRIPT_NAME SCHEDULE PATH
```

Where:
* **SCRIPT_NAME** is a name for the scheduled script. If no name is provided, the script filename will be used.
* **SCHEDULE** is the schedule in [crontab format](https://en.wikipedia.org/wiki/Cron#Overview)
* **PATH** is the path of the script to schedule.


## Syncronization issues
It is responsibility of the programmer to ensure there are no race conditions and to implement, if necessary, the required data locks to avoid syncronization issues.
