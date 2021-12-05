# Talk-talk

A spanish speaking conversational agent

## Set up

1. Install dependencies:
* Python
* [Requirements](https://stackoverflow.com/questions/7225900/how-can-i-install-packages-using-pip-according-to-the-requirements-txt-file-from)
* [Uvicorn](https://www.uvicorn.org/)
* [Ngrok](https://dashboard.ngrok.com/get-started/setup)

2. Create a `config.py` file based on config.git.py structure. 

3. Start the API: `python -m uvicorn main:app --reload`

4. Expose port 8000 with ngronk: `./ngrok http 80`

5. [Config Slack wekhook URL](https://api.slack.com/apps/A02E1B4N6TE/event-subscriptions?)
