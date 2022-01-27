# urlUpdated
Python script to check if a list of URLs has changed since the last time it was ran. Sends SMS via Twilio if page contents have changed.

If you want to check them on an interval, use [Windows Task Scheduler](https://towardsdatascience.com/automate-your-python-scripts-with-task-scheduler-661d0a40b279), or for MacOS/Linux check out [Cron](https://towardsdatascience.com/a-step-by-step-guide-to-scheduling-tasks-for-your-data-science-project-d7df4531fc41)

### URL Config
Add URLs to check via the urls.json file to begin tracking them
```json
{
  "google.com",
  "github.com"
}
```
### SMS Config
Go to [Twilio](https://www.twilio.com/docs/sms/quickstart/python) and create an account (Promocode: TWILIOQUEST may give some free credits, [not an affiliate link](https://www.twilio.com/quest)).
Then fill in the SID and API Key, and To/From config options in the twilio.json file. 
"To" will be the destination phone number, and "From" will be the number registered on Twilio.
```json
{
    "SID":"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "Key":"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "To": "+11234567890",
    "From": "+11234567890"
}
```

