# Dependencies
To run the code you need to have google chrome and python/pip installed.

# Setup
To start the application you first need to setup a virtaul env for the runtime.
Clone the repo then enter the folder and setup the venv, then you can install the dependencies:
```
git clone https://github.com/mmarci96/travian-bot-python.git
cd travian-bot-python
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

# Run
Start the app with the following command inside the root directory of the project
```
python program.py "https://your_server.travian.com" "email/username" "password"
```
This command will now log into the account and save the first village data to json.
There are methods to start building, need a way to add tasks and create a while loop to not shut down until completion.
