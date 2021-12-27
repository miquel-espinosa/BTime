![alt text](https://github.com/MiquelEspinosa/BTime/blob/main/BTime.png?raw=true)

# :clock4: BTime 
>*Never be late*


**BTime**, your new personal command line assistant that manages all your personal daily and weekly reminders.

Sounds fancy, but under the hood, it's just a python script that helps you schedule and manage more efficiently your **cron** time-based Unix-like tasks. 
  

## Installation
To install *BTime* in a Unix system, follow these steps:

### Requirements

+ Make sure you have `git` and `pip3` installed .
    ```
    sudo apt install git python3-pip
    ```

### Steps


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
+ Run autoinstall script (If do this don't need next steps):
    ```
    sudo ./install.sh
    ```

+ Install `requirements` :
    ```
    pip3 install -r requirements.txt
    ```
    

+ Add **btime** symbolic link to `/usr/local/bin/btime`. (**Important:** Make sure you run this command inside the *Never-be-late* directory.)
    ```
    sudo ln -sf $(realpath main.py) /usr/local/bin/btime
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

Tested on Ubuntu 20.04
