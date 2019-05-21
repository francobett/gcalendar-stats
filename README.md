# gcalendar-stats

## Working in the virtual env
- Enter: `source myenv/bin/activate`
- Exit: `deactive`
- Update requirements: `pip freeze > requirements.txt`

## Run your calendar stats
1. Setup environment
2. Run `main.py` : `pyton gcalendar-stats/main.py`
- You can specify the number of days and your team label ex: 10 days and myTeam: `pyton gcalendar-stats/main.py 10 "myTeam"`
3. Give access to the app to the G calendar
4. Check results in `/results` folder.

## Setup environment
1. Install virtualenv `pip3 install virtualenv`
2. In the main folder of the project, create virtual env `virtualenv myenv`
3. Activate your virtual env `source myenv/bin/activate`
4. Install requirements `pip install -r requirements.txt`
