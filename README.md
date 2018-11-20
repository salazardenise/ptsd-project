# <img src="static/img/finding-peace-logo.png" width="10%"> Finding Peace: a resource for people with PTSD

## Contents
* [Summary](#summary)
* [Tech Stack](#techstack)
* [Tests](#tests)
* [Features](#features)
* [Demo](#demo)
* [About the Developer](#aboutTheDeveloper)

## <a name="summary"></a>Summary

The **Finding Peace** web app is a resource for people with PTSD. You can seek help by searching for PTSD programs, practice self-care by listening to relaxing recordings, and send message templates by email or text. The purpose of the message templates is to make it easier to send a message regarding your mental health when you are feeling too much anxiety to reach out to others.

## <a name="techstack"></a>Tech Stack

**Front-end:** Jinja, HTML, CSS, Bootstrap, Javascript, JQuery, AJAX

**Backend:** Python, Flask, SQLAlchemy

**APIs:** VA Web Service, Google Maps JavaScript API, Google Geocoding API, Twilio API, Gmail Oauth, Universal Inspirtational Quotes API

Finding Peace is an app built on a Flask server with a PostgreSQL database. SQLAlchemy is used as the ORM. The front UI is built using Jinja templating, HTML, CSS and the Bootstrap library. Also on the front-end, Javascript uses JQuery and AJAX to interact with the backend. 

## <a name="tests"></a>Tests

Flask server routes are tested using the Python unittest module in tests.py. Selenium is used for end-to-end testing in tests-selenium.py.

## <a name="features"></a>Features

There are 3 main features.

1) Search for PTSD Programs by facility name, state, address, and zipcode and display results on Google Map and table

2) Practice self-case by listening to relaxing recordings

3) Send Text and Email to friends/family/co-workers regarding your mental health

## <a name="demo"></a>Demo

[![Finding Peace Web App Demo](http://img.youtube.com/vi/znszUOUryxw/0.jpg)](http://www.youtube.com/watch?v=znszUOUryxw)

## <a name="aboutTheDeveloper"></a>About The Developer

**Finding Peace** was created by Denise Salazar, a software engineer in Sunnyvale, CA. Learn more about the developer on [LinkedIn](https://www.linkedin.com/in/salazardenise/).
