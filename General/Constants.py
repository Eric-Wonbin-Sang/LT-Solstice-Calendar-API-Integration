from General import Functions


# !/usr/bin/env python
# title           :	main.py
# description     :	This script posts Google calendar events to a Pod/Display
# author          :	Kelli Webber
# date            :	2018-12-12
# last updated    :	2019-10-08
# usage           :	main.py
# notes           :	calendarSettings.csv required (Column 1: Pod IPs | Column 2: Calendar IDs)
# When prompted to allow access, use account with permission to view all
# calendars in CSV file
# python_version  :	3.7
# ==============================================================================================

# Script assumes admin password data is uniform across all Pods


admin_password = open(Functions.get_curr_parent_dir("\\API Keys\\Stevens LT Solstice Password.txt")).read()

solstice_pod_cvs_path = 'calendarSettings.csv'
calendar_api_token_path = Functions.get_curr_parent_dir(
    "\\API Keys\\Stevens LT Solstice token.json")
google_calendar_credentials_path = Functions.get_curr_parent_dir(
    "\\API Keys\\Google Calendar credentials (eric.wonbin.sang).json")
