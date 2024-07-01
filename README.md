# Weather Text
Automates morning texts of the daily weather forecast and gives recommendations for your clothing.

## Setup
1. Create environment variables for .env file
  - API Key from [OpenWeatherMap](https://openweathermap.org/api/one-call-3) (specifically One Call API 3.0, very cheap)
  - City (i.e., College Station, TX, USA)
  - Personal phone number
  - Account SID, Auth Token, and Twilio phone number from [Twilio](twilio.com)
  - API Key from [OpenAI](https://platform.openai.com/api-keys)
2. Clone this repository.
3. Set up virtual environment and install the requirements:
  ```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
4. Update your shell script with the proper file paths to your virtual environment, interpreter, and script.
5. Create cron job, you can use these [instructions](https://medium.com/@jameshamann/automation-with-cron-d10f7cbbb638). It should point towards the path of your shell script.

There you have it! Right now, your computer will have to be on in order for the cron job to work, so I'm looking into ways to change this. 

## To Do
- [x] Utilize new weather API to access 24 hour forecasts
- [x] Integrate OpenAI API to pull weather data and get insights on what to wear for the day
- [ ] Add personalization features for clothing insights
- [ ] Host on DigitalOcean
- [ ] Build out frontend with dropdown options for users

## Need To Fix
- [x] Accuracy of geocoder, maybe use different library where city name is necessary
