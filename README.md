# artist-index
<p align="center">
  <img width="960" height="540" alt="Screenshot_20260825_031530" src="https://github.com/user-attachments/assets/d03d494d-f73c-4ef9-a512-d7fe06780769" />
</p>
This is a web application for managing a database that indexes artists I follow on various social media.

This web application is incredibly lightweight and is designed to be run on Railway with a serverless configuration. It uses a combination of Flask and SQLite to manage the database.

# [You can visit the index here](https://artist-index.up.railway.app/)

### Features
- **Insertion, Deletion, and Modification**: All of these operations are supported through custom web forms, allowing an administrator to manage entries in the database entirely through the website.
- **Clean Display of Database Content**: The contents of the database are presented to users in a clean table using a combination of Bootstrap and DataTables. Clicking on a row expands a quick view of that artist's links.
- **Beautiful Image Gallery**: A really nice image gallery for showcasing some artwork that the artists in the database have made. You can click on an image to see more details about it, like the artist who made it and the source where they posted it.
- **Responsive Web Design**: The frontend uses Bootstrap, ensuring that users on desktop and mobile browsers have a nice experience viewing the web application.
- **User Logins**: Anonymous users can only view the index, the 'About' page, the 'Changelog' page, and a short version of an artist's detailed view. Registered users can modify the database, access the control panel, view artists who were set to 'Private', and see the long version of an artist's detailed view.
- **Very Efficient and Low Cost**: When deployed on Railway with a serverless configuration, this web application uses so little resources that the total cost it incurs is well below the monthly usage limit for free tier accounts.

### Gallery
<p align="center">
  <img width="405" height="810" alt="image" src="https://github.com/user-attachments/assets/89ab0b76-9e09-4dee-a293-ae342f14a2e5" /><br>
  Example of viewing an artist's page with a mobile browser.
</p><br>

<p align="center">
  <img width="960" height="540" alt="Screenshot_20260825_030325" src="https://github.com/user-attachments/assets/3bb29de0-e8e1-4215-b8bb-0683e7211227" /><br>
  Looking at the image gallery.
</p>

### Languages & Libraries
- HTML
- CSS
- JavaScript
  - Bootstrap
  - DataTables
  - JQuery
  - Masonry
- Python
  - Alembic
  - Flask (and all of its extensions like Flask-Login, Flask-WTF, etc.)
  - Gunicorn
  - Jinja
  - SQLAlchemy
  - Werkzeug
- SQL
  - SQLite
