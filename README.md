![alt text](https://github.com/MiquelEspinosa/BTime/blob/main/BTime.png?raw=true)

# :clock4: BTime 
>*Never be late*


**BTime**, your new personal command line assistant that manages all your personal daily and weekly reminders.

Sounds fancy, but under the hood, it's just a python script that helps you schedule and manage more efficiently your **cron** time-based Unix-like tasks. 
  

## Installation
To install *BTime* in a Unix system, follow these steps:

### Requirements

+ Make sure you have `git` installed.
    ```
    sudo apt-get install git
    ```


+ Make sure you have `pip` or `pip3` installed.
    ```
    sudo apt-get install python3-pip
    ```


### Steps

+ Install `python-crontab` library:
    ```
    pip3 install python-crontab
    ```


+ Install `simple-term-menu` library 
    ```
    pip3 install simple-term-menu
    ```


+ Navigate to the directory you want to install *BTime*
    ```
    cd /home/username/<my_btime_directory>
    ```
    
    
+ Clone this repository
    ```
    git clone https://github.com/MiquelEspinosa/BTime.git
    ```


+ Move inside *Never-be-late* directory:
    ```
    cd BTime
    ```
    

+ Add **btime** alias to your bash profile (if you are using bash). (**Important:** Make sure you run this command inside the *Never-be-late* directory.)
    ```
    echo 'alias btime="python3 '$(pwd)'/main.py"'  >> ~/.bashrc
    ```
    + If you are using zsh, run instead
        ```
        echo 'alias btime="python3 '$(pwd)'/main.py"' >> ~/.zshrc
        ```


+ Source your bash or zsh profile by running: 
 	+ For bash
      ```
      source ~/.bashrc
      ```
 	+ For zsh
      ```
      source ~/.zshrc
      ```


+ Finally, you should see a welcoming message when you run:
    ```
    btime show
    ```

## Basic usage
To see the basic options that can be run, type `btime help`:
```
Please, type: `btime <option>´ where <option> can be: 
  <empty>    (if its left empty it will show your timetable for today)
  reset      (to reset your daily tasks)
  addtoday   (to define your daily tasks)
  week       (to show your timetable for the entire week)
  edit       (to edit any task)
  addfixed   (to define your weekly tasks)
  delevent   (to delete an event)
  resetall   (to delete all your cron tasks)
  wifioff    (to disable internet connection)
  wifion     (to enable internet connection)
  show       (to show BTime message)
  help       (to show this message)
```

&nbsp;
&nbsp;

Leave any comments, suggestions, bugs or issues and don't hesitate to let me know any features you would like to see implemented.
&nbsp;

And, of course, last but not least, you can buy me a coffee. :wink: :coffee: 
****
Tested on Ubuntu 18.04

