Docker: Trivial over network in Python
==============================

This is a little trivial server written in Python, it may not be pretty as I have been patching it along the way but, it works hehe

As always suggestions are welcome ^^

Usage:
------

Here is the help of the trivial server:

```
docker run --rm kalrong/trivial -h 
usage: trivial.py [-h] [-p PORT] [-q QUESTIONS] [-l LOG] [-f FLAG]
                  [-a ANSWERS]

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Specify which port to be used. Default: 8100
  -q QUESTIONS, --questions QUESTIONS
                        File containing the questions for the trivial.
                        Default: ./questions
  -l LOG, --log LOG     Folder where the logs will be saved. Defauld: ./log/
  -f FLAG, --flag FLAG  Flag given at the end of the game to the winners.
                        Default: flag{Tr1v14L-RuL3z}
  -a ANSWERS, --answers ANSWERS
                        Number of correct answers before the flag is given.Connected to Trivial!!!
Name of a famous hacker with the initials KM:
                        Default: 1
```

As the port where the trivial listens can be changed I haven't set any exposed ports so you will need to do it yourself.

To give it a try you can run the container like this:
```
docker run --rm -it -p 8100:8100 kalrong/trivial
```

This should start the trivial with the example question and listen on the local machine at port 8100, you can test it with netcat:
```
nc localhost 8100
```

And you should see this in your netcat session:
```
Connected to Trivial!!!
Name of a famous hacker with the initials KM:
```

And this on docker:
```
[172.17.0.1] Connected
[172.17.0.1] Question: Name of a famous hacker with the initials KM
```
Just answer kevin and you will get the default flag.

Apart from the logs that appear in docker the servers stores a log file per ip in the default location /log inside the container, this can also be changed with the ```-l, --log``` option, if you want to save them locally you can always map the log folder to your machine.

Suggestions, questions, errors, etc:
------------------------------------

If you have any of the above just open an issue on the githu repository and I will deal with them asap.