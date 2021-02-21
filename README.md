# Textbook View API

for the sproul.club Backend Take Home Assignment

By Nicholas Cho

## Overview

This is an API built for a website in which student users would be able to maintain a list of textbooks from their school library. The students would be able to add textbooks from a larger list of books, while also being able to remove textbooks from their current list. Lastly, the students would be able to share their list of textbook titles with anyone through a link-embedded QR code.

The API is built on Flask with a MongoDB backend.

## Setup

Download all dependencies from the requirements.txt file. 

Once in the textbooks folder, run python3 textbookview.py to run the application on your local server.

## Limitations

The API was built under many assumptions. There is no user authentication in place; the user's list is queried by using the full name of the user as a URL variable. This is meant to be a temporary simplification. 

The add/delete textbooks function does not work since they rely on request data to be passed in in order to query for the appropriate textbook object. Possible future implementations could involve passing in the textbook object information through an onclick event or a form.

Lastly, the QR code is a placeholder image for what is to be an actual functioning QR barcode. The placeholder "qrcode.jpg" is used in the code to represent that.


