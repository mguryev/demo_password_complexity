# Demo for password complexity

## Why?
When explaining to my kids what is a strong password I wanted to demo:
- how password is being encoded 
- how a brute-force attack would try to guess the password
- how much more time does it take to guess a certain password

And so this demo was born
  
## Installation

This project requires python 3.5+ to run

[virtualenv](https://virtualenv.pypa.io/en/stable/) is also strongly recommended

Once your environment is configured, run `pip install -r requirements.txt` 
  and you should be good to go
  
## Running the demo

The documentation should be up-to-date, so start with
```
$ ./password.py
usage: password.py [-h] {encode,guess,time_to_guess} ...

Password complexity demonstration

positional arguments:
  {encode,guess,time_to_guess}
                        sub-command help
    encode              encode password
    guess               guess encoded password
    time_to_guess       estimate time to guess password

optional arguments:
  -h, --help            show this help message and exit
```




 