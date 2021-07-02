from datetime import date

import playsound

import requests

age_limit = 45
district_id = 506
dose_no = 1

today = date.today()
date_string = today.strftime("%d-%m-%Y")

sos_sound_path = "C:\somendra\ArdNemos\cowin\\alert.mp3"
base_url = "https://cdn-api.co-vin.in/api/v2"
pin_based_url = base_url + "/appointment/sessions/public/calendarByPin?pincode=302017&date=14/05/2021"
district_based_url = base_url + "/appointment/sessions/public/calendarByDistrict?district_id=" + str(
    district_id) + "&date=" + date_string

payload = {}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
}

print("checking for slots")

while True:
    response = requests.request("GET", district_based_url, headers=headers, data=payload)

    available_centers = []

    if response.status_code == 200:
        response_data = response.json()

        for center in response_data.get("centers"):

            sessions = center.get("sessions")

            for session in sessions:

                if session.get("min_age_limit") == age_limit and session.get("available_capacity_dose" + str(dose_no)) > 0:
                    center_name = center.get("name")
                    available_centers.append(center_name)
                    print(center_name)

        if len(available_centers) > 0:
            print("{} centers are available. Book your appointment now".format(len(available_centers)))
            playsound.playsound(sos_sound_path, block=True)
    else:
        print("Got {} response from server".format(response.status_code))
        break

print("Program terminated due to some errors.")
