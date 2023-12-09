# Filmter

## Video Demo:
https://youtu.be/Xc6aL9rSW0k

## Project Description:
We all know it - You want to have a spontaneous movie night with your friends but just can't figure out what to watch, so you spend so much time finding the right movie that there is not enough time left to actually watch it.

*Filmter* is a web application that allows users to search through a database of movies based on keywords and displays general information on each movie. In addition, *Filmter* enables users to keep track of all the movies they have watched and want to watch in the future.

## Installation:
Step-by-step instructions on what to install in order to get the project running.
- Clone or fork this repository.
- Create a virtual environment in your local *Filmter* directory.
- Install the required libraries that are listed in the [requirements.txt](./requirements.txt) file.
- Sign up to [TMDb API](https://developer.themoviedb.org/reference/intro/getting-started) to generate your own API_ID and API_KEY.
- Save your API_ID and API_KEY and copy and paste them to your terminal:

```
$ export API_KEY=YOUR_API_KEY
$ export API_ID=YOUR_API_ID
```

- Run the application using one of the following commands in your *Filmter* directory:

```
$ python3 app.py
```
```
$ flask run
```



# Features

## Log-In Page
Once they have created an account via the register page (view below), users can use their username and password to log in. Through Flask's 'Session,' their account information including the movie data stored in the various SQL databases (i.e. for the "Want-to-Watch" list and the "Watched" list) gets associated with their user ID. If users have not created an account yet, they can click on "Create an Account!" in order to get redirected to the register page.

Using JavaScript, the "Log In" button is disabled until the user has entered text into both input fields.

![Login Page](./static/images/LogInPage.png)


If the username and/or password that the user entered are invalid or the password does not match the entered username, the user gets redirected to the log-in page and informed about the error.

![Login Page Error](./static/images/LogInPageError.png)

## Register page
Before using the web application, users are forced to create an account. Filmter implements validation for both front-end and back-end. When registering, users have to enter a name, a username that has to be alphanumeric, and a password with a minimum of eight characters as well as a password confirmation. That password is hashed first before it gets stored in the user database.
However, for safety reasons, please refrain from using your actual password!

![Register Page](./static/images/RegisterPage.png)

If the user enters a username that is non-alphanumeric, the password and the password confirmation do not correspond, or the entered password is shorter than 8 characters, the user gets redirected to the register page and informed about the error.

![Register Page Error](./static/images/RegisterPageError.png)

## Index Page
After registering or logging in, the user gets redirected to the index page where they are greeted by their name that was stored in the user database when they logged in / registered, and a waving hand that was implemented using CSS.

Users can find movies by entering keywords in the text field and clicking the "Search" button. Via "Get Request," input will be sent to the back-end and is used to retrieve JSON data from TMBD's movie database API.

![Index Page](./static/images/IndexPage.png)

If the user tries to search without entering something into the input field, the user gets redirected to the index page and asked to enter a keyword.

![Index Page Error](./static/images/IndexPageError.png)

## Results Page
Movies that match the user's input based on their appearance in the movie's title or overview will be displayed as cards. They show limited information including the movie image, title, and genres for the user to skim through.

![Results Page](./static/images/ResultsPage.png)

When the user clicks on a movie card, another card pops up that shows more information such as a description (if available), the release date (if available), and an average rating as well as a vote count. This functionality is implemented using Bootstrap modals.

Additionally, these modals display a "Want to Watch" as well as "Watched" button through which users can add movies to the respective databases and the corresponding lists.

![Results Modal](./static/images/ResultsModal.png)

If the user's input does not generate any results, the user will be redirected and prompted to retry with different keywords through a redirection to the index page.

![Results Page Error](./static/images/ResultsPageError.png)

# Want-To-Watch Page
Movies that the user added to the want-to-watch list will be displayed as cards, similar to the results page, and Bootstrap modals are used to provide more information on the movie or to remove it from the list.

![Want-To-Watch Page](./static/images/WantToWatchPage.png)

![Want-To-Watch Modal](./static/images/WantToWatchModal.png)

If the user has not added any movies to their want-to-watch list, the user will be redirected and prompted to browse through the movie database through a redirection to the index page.

![Want-To-Watch Page Error](./static/images/WantToWatchPageError.png)

# Watched Page
Movies that the user marked as "Watched" will be displayed as cards, similarly to the results page and the want-to-watch page, and Bootstrap modals are used to provide more information on the movie or to remove it from the list.

![Watched Page](./static/images/WatchedPage.png)

![Watched Modal](./static/images/WatchedPageModal.png)

If the user has not added any movies to their watched list, the user will be redirected and prompted to browse through the movie database through a redirection to the index page.

![Watched Page Error](./static/images/WatchedPageError.png)

# Account Page
This page allows the user to change their name, username, and password. Again, validation is implemented on the back-end.

### Name
![Account Page Name](./static/images/AccountName.png)

![Account Page Name Changed](./static/images/AccountNameChanged.png)


### Username
The username, again, has to consist of alphanumerical characters only

![Account Page Username](./static/images/AccountUsername.png)

If the username that the user wants to change their user name to is already taken, the user gets redirected and informed about the error.

![Account Page Username Taken](./static/images/AccountUsernameTaken.png)

### Password
The password, again, has to be at least 8 characters long.

![Account Page Password](./static/images/AccountPassword.png)


## Log-Out
The user can log out by clicking on "Log Out" in the navigation bar.

## Additional features
- By monitoring the user activity through JavaScript, the user gets logged out automatically after five minutes of inactivity. This time-out function is implemented through clearing the Flask session.
- At the head of every page, there is a navigation bar that you can use to navigate between the Want-To-Watch page, the Watched page, the Account page, the Log-Out function (and therefore, the Log-In and Register page), and the Index page (by clicking on the *Filmter* logo).
- At the footer of every page, there is a GitHub logo that redirects the user to my GitHub page (@noahsafar).
