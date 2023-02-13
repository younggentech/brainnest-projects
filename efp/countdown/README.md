# CounterDown APP
This is small web development project, the aim was to create a kitchen timer like application.
## Modules used
* Flask - For handling web interface
* Pytest - For handling single test.

# Aim of App
The app should be able to run and do the following:
 * Set amount of time for timer format HH:MM:SS
 * Have the ability to Start time or Rest given input
 * By click Start button user is redirected to new page that display timer
 * View with timer should be able to go back to set a new timer.

# Limitations and Thoughts
Code has not been tested enough so these might need some refactoring work especially to
code that handles responses.
Timer cannot be stored have not implemented any Database backend. Mostly due to time constrains.
Final thoughts, although this was small project with a bit of Flask development and a bit of JavaScript (JS),
I've discovered that limitation in knowledge when it comes to JS. This made me lose a lot of time
trying to get expected outputs.

# How to download app
The easiest way is to clone repository in GitHub.


# How to install dependencies
You can install all the module and other hot stuff used in the project by doing the command below:
```shell
pip install -r /path/to/dev-requirements.txt
```

# How start run app
This app is run via the terminal and the user needs to navigate to directory countdown/countdown.
```shell
python countdownapp.py
```
In the terminal you should see a http:// tolocalhost be displayed,
## How to quit app
The is will terminate the app and for now this is the only way to quit it.
<kbd>Ctrl</kbd> + <kbd>C</kbd>
or
<kbd>Ctrl</kbd> + <kbd>Break</kbd>

# Thanks for the Read
Well you made it to the bottom, good for you know things can only go up :-) .
