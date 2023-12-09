# Design

## Used Technologies
- API (by TMDb)
- Bootstrap
- CSS
- Flask
- HTML
- JavaScript
- jQuery
- Python
- SQL

## Breakdown of all the files
- ["static" directory](./static) - Contains static files such as CSS files, JavaScript files and images
    - ["css" directory](./static/css) - Contains CSS files
        - [styles.css](./static/css/styles.css) - CSS file that contains the stylistic customizations of each HTML file and web pag
- ["templates" directory](./templates) - Contains JavaScript files and HTML documents
    - ["js" directory](./templates/js) - Contains JavaScript files
        - [activity.js](./templates/js/activity.js) - JavaScript file that is responsible for monitoring the user activity for the sake of the time-out (automatic log-out after five minutes of user inactivity) function
        - [enable_button.js](./templates/js/enable_button.js) - JavaScript file that is responsible for enabling the log-in and register button when all input fields are filled
        - [previews.js](./templates/js/previews.js) - JavaScript file that is responsible for carouseling through preview movie images on the log-in and register page
    - [account.html](./templates/account.html) - web page where users can change their account information
    - [index.html](./templates/index.html) - "Homepage" of the website
    - [layout.html](./templates/layout.html) - Layout structure of the web page, in order to avoid HTML code repetition
    - [login.html](./templates/login.html) - Users input their username and password in order to log into an account that already exists in the database
    - [register.html](./templates/register.html) - Users input a name, a username, a password and a password confirmation in order to create an account in the database
    - [results.html](./templates/results.html) - Web page that displays movies as search results based on the keywords the user entered on the index page; here, users receive information on movies that said keywords apply to, and can add movies to their want-to-watch list or their watched list
    - [want-to-watch.html](./templates/want-to-watch.html) - Web page that displays movies that the user has marked as "Want to Watch"; here, the user can also remove movies from the want-to-watch list
    - [watched.html](./templates/watched.html) - Web page that displays movies that the user has marked as "Watched"; here, the user can also remove movies from the watched list
- [app.py](./app.py) - Python code that includes all the routes and the implementation of Flask and thus, is responsible for making all of the web page's functionalities happen
- [filmter.db](./filmter.db) - Relational database containing tables of users, their want-to-watch list, and their watched list
- [helpers.py](./helpers.py) - Contains helper functions that ensure that the user is logged in and fetch data from TMDb's movie database API
- [requirements.txt](./requirements.txt) - Text file that contains the list of all Python libraries and modules used and imported in the program

## The SQL Databases
```
CREATE TABLE "users" (
    "id" INTEGER NOT NULL,
    "name" TEXT NOT NULL,
    "username" TEXT NOT NULL UNIQUE,
    "hash" TEXT NOT NULL,
    PRIMARY KEY("id" AUTOINCREMENT)
    );
    ;
    CREATE UNIQUE INDEX "username" ON "users" (
    "username"
);

CREATE TABLE 'watchedlist' (
    "user_id" INTEGER NOT NULL,
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "title" TEXT NOT NULL,
    "poster_path" TEXT,'genre_ids' INTEGER,
    "overview" TEXT,
    "vote_average" FLOAT NOT NULL,
    "vote_count" INTEGER NOT NULL,
    "release_date" TEXT,
    FOREIGN KEY("user_id") REFERENCES "users"("id")
);

CREATE TABLE 'watchlist' (
    "user_id" INTEGER NOT NULL,
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "title" TEXT NOT NULL,
    "poster_path" TEXT,'genre_ids' INTEGER,
    "overview" TEXT,
    "vote_average" FLOAT NOT NULL,
    "vote_count" INTEGER NOT NULL,
    "release_date" TEXT,
    FOREIGN KEY("user_id") REFERENCES "users"("id")
);
```

