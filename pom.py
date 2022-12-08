import os
import time
from datetime import datetime, timedelta
import argparse

_myDir = os.path.abspath(os.path.dirname(__file__))

parser = argparse.ArgumentParser()
parser.add_argument('--sessions', '-s', type=int)
parser.add_argument('--work', '-w', type=int)
parser.add_argument('--rest', '-b', type=int) # 'break' is a Python keyword.
args = parser.parse_args()

sessions = 4 if args.sessions is None else args.sessions
session_dur = 25 if args.work is None else args.work
break_dur = 5 if args.rest is None else args.rest

def do_pom(count, session_dur):
	print(f'Session {count}/{sessions} started at {datetime.now().strftime("%-I:%M:%S %p")} and will end at {(datetime.now() + timedelta(minutes = session_dur)).strftime("%-I:%M:%S %p")}.')
	time.sleep(session_dur * 60)

def do_break(count, break_dur):
	os.system(f'''
		osascript -e 'display dialog "{count} of {sessions} sessions completed." with title "Take a break!" with icon POSIX file "{_myDir}/images/break.icns" buttons {{"OK"}} default button 1'
		''')
	print(f'Break {count}/{sessions-1} started at {datetime.now().strftime("%-I:%M:%S %p")} and will end at {(datetime.now() + timedelta(minutes = break_dur)).strftime("%-I:%M:%S %p")}.')
	time.sleep(break_dur * 60)
	os.system(f'''
		osascript -e 'display dialog "Starting session {count + 1} of {sessions}." with title "Get back to work!" with icon POSIX file "{_myDir}/images/work.icns" buttons {{"OK"}} default button 1'
		''')

os.system('echo "Beginning pomodoro."')
for session in range(1, sessions + 1):
	do_pom(session, session_dur)
	if session < sessions:
		do_break(session, break_dur)
	else:
		os.system(f'''
			osascript -e 'display dialog "{session} of {sessions} sessions completed." with title "Congrats!" with icon POSIX file "{_myDir}/images/congrats.icns" buttons {{"OK"}} default button 1'
			''')