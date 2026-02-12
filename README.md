# artist-index
This is a web application for managing a database that indexes artists I follow on various social media.

This web application is incredibly lightweight and is designed to be run on Railway with a serverless configuration. It uses a combination of Flask and SQLite to manage the database.

# [You can visit the index here](https://artist-index.up.railway.app/)

### Features
- **Insertion, Deletion, and Modification**: All of these operations are supported through custom web forms, allowing an administrator to manage entries in the database entirely through the website.
- **Clean Display of Database Content**: The contents of the database are presented to users in a clean table using a combination of Bootstrap and DataTables. Clicking on a row expands a quick view of that artist's links.
- **Responsive Web Design**: The frontend uses Bootstrap to great effect, ensuring that users on desktop and mobile browsers have a nice experience viewing the web application.
- **User Logins**: Anonymous users can only view the index, the 'About' page, and a short version of an artist's detailed view. Registered users can modify the database, access the control panel, view artists who were set to 'Private', and see the long version of an artist's detailed view.
- **Additional Details for Twitter Users**: Artists with a Twitter account gain additional details in their detailed view. Their profile pictures can be seen and an embed of their Twitter timeline can be viewed.
- **Very Efficient and Low Cost**: When deployed on Railway with a serverless configuration, this web application uses so little resources that the total cost it incurs is well below the monthly usage limit for free tier accounts. Due to only storing links for Twitter profile pictures, the total disk storage usage is also greatly reduced.

