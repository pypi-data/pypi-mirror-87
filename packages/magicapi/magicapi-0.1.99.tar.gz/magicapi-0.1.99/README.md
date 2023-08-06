# Magic API

The Magic API!

1) incr the toml version
2) poetry publish --build


For CLI:
# Magic CLI (magicapi has this built in)

The best server maker.

Steps:

1) pip install magicapi (make sure the pip points to the correct python (3.6+))

2) cd into the directory you want the server to be in

// use the cli to create the app

3) magic create < app name >

4) cd < app name >

// now make the virtual env and pip install the requirements
5) python3 -m venv venv

6) source venv/bin/activate

7) `pip install -r requirements.txt`
8) `pip install --upgrade magicdb magicapi`

// files needed to run
8) Create an .env file in the < app name > directory.

a) Use the ".example_env" as a template. Fill in the env variables for the services you will need to use.

b) The SERVICE and TASKS_TABLE_NAME are required for the app.

// add firestore
1) add the firestore service account json to the < app name > and name it "my-service-account.json"

// to deploy to aws lambda

1) Create a user on AWS and sign in via the CLI (https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)
 
2) npm i

2) magic deploy

That should be it for the setup!

Time to run it!

To start a local server: magic start

To test local server (while local server is running): magic test

To deploy for the first time or any time you change the serverless yaml: magic deploy

To deploy when you just edited the app code: magic deploy_again

To update magicapi:
pip install --upgrade magicapi
