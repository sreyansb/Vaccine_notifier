# Vaccine Notifier
Notifies when a Covid-19 vaccine is available. Currently, it sends a notification when COVAXIN is available.

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
pip install -r requirements.tct
```

3. Run the following command.
```bash
python .\<File_name>.py
```

Works for Windows systems because of the use of 'winsound'. Replace by printing the bell character instead.
