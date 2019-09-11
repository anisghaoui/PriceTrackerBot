# PriceTrackerBot
A simple bot that tracks a list of items on amazon.com. When one of the item is below the desired price, it sends an email too a given google email address.

## Prequisite
* bs4
* json
* smtplib
* requests
* time
* A Gmail account

## Setup
* Modify "config.json" file with your credentials. 
* Headers can be obtained by searching them in a search engine.
* Activate [Less secure apps](https://myaccount.google.com/lesssecureapps)
* You can use [two factors authentification](https://www.google.com/landing/2step/). This will allow you to use a [dedicated password generated by google](https://accounts.google.com/signin/v2/sl/pwd?service=accountsettings&passive=1209600&osid=1&continue=https%3A%2F%2Fmyaccount.google.com%2Fapppasswords&followup=https%3A%2F%2Fmyaccount.google.com%2Fapppasswords&rart=ANgoxce9uCCYPtNg20SkConOQLlKpizmWGdoyl8hDrhbk7hIfiGv9pn5Kd5r-uWBju-1GI9nbW8kaPE1CU2vgA3nlYBdyWa03A&authuser=0&csig=AF-SEnYrZx1EbFA1bOB2%3A1568231226&flowName=GlifWebSignIn&flowEntry=ServiceLogin) rather yours.
* Add items to the track list in "items list.json"

## Usage
The bot can run in background and can be daemonised while occupying minimum ram usage (38 MB on Win10). It can run for a number of days or indefinitly (if so, you will have kill it manually).

## Acknowledgments
[Dev Ed](https://www.youtube.com/watch?v=Bg9r_yLk7VY)'s video inspired me to do this. 

## License
This project is licensed under the GNU GENERAL PUBLIC LICENSE v3.0 - see the [LICENSE.md](LICENSE.md) file for details
