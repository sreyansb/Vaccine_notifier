# Vaccine Notifier
Notifies when a Covid-19 vaccine is available. Currently, it sends a notification (rather, makes a beep sound)  when COVAXIN is available.

* Based on the user's requirements, he/she can be notified about the vaccine of their choice.
* Text to Speech has been added for ease of use.

## How to run?

1. Clone the repository.
```bash
git clone https://github.com/sreyansb/Vaccine_notifier.git
```

2. Create a virtual environment and install the dependencies.
```bash
cd Vaccine_notifier
virtualenv env
.\env\Scripts\activate
pip install -r requirements.txt
```

3. Run the following command. (The program should be allowed to run in the background)
```bash
python .\without_whatsapp.py # for the first dose
python .\dose_2.py # for the second dose
```

Works for Windows systems because of the use of 'winsound'. Replace by printing the bell character instead.

Note:

Works only for BBMP district(district id: 294). To use for other states/districts:

1. Use [api-setu's state id API](https://apisetu.gov.in/public/api/cowin#/Metadata%20APIs/states).

2. Get the id of your state and use that for [api-setu's district id API](https://apisetu.gov.in/public/api/cowin#/Metadata%20APIs/districts).

3. Replace the district id in the code: with the required district's id.
