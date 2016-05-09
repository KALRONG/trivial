# -*- coding: utf-8 -*
import socket
import threading
import random
import re
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("-p","--port", help="Specify which port to be used. Default: 8100", type=int,default=8100)
parser.add_argument("-q","--questions", help="File containing the questions for the trivial. Default: /root/questions", default="/root/questions")
parser.add_argument("-l","--log",help="Folder where the logs will be saved. Defauld: ./log/", default="./log/")
parser.add_argument("-f","--flag",help="Flag given at the end of the game to the winners. Default: flag{Tr1v14L-RuL3z}", default="flag{Tr1v14L-RuL3z}")
parser.add_argument("-a","--answers",help="Number of correct answers before the flag is given. Default: 1",type=int,default=1)
args = parser.parse_args()

if os.path.exists(args.questions):
  with open(args.questions) as archivopreguntas:
        questions=archivopreguntas.read().splitlines()
else:
    print "Error opening questions file"
    raise SystemExit

if not os.path.exists(args.log):
  try:
    os.makedirs(args.log)
  except:
    print "Error creating log folder."
    raise SystemExit

longitud=len(questions)

# Our thread class:
class ClientThread ( threading.Thread ):

   # Override Thread's __init__ method to accept the parameters needed:
   def __init__ ( self, channel, details ):

      self.channel = channel
      self.details = details
      threading.Thread.__init__ ( self )

   def run ( self ):
      logfile=open(args.log+'trivial-'+self.details[0]+'.log','a')
      logfile.write("["+self.details [0]+"] Connected\n")
      print "["+self.details [0]+"] Connected"
      preguntas = random.sample(range(0, longitud), args.answers)
      self.channel.send ('Connected to Trivial!!!\n')
      for x in preguntas:
        splitquestion=questions[x].split(":")
        self.channel.send (splitquestion[0]+":")
        logfile.write("["+self.details [0]+"] Question: "+splitquestion[0]+"\n")
        print "["+self.details [0]+"] Question: "+splitquestion[0]
        reply = ""
        data = True
        while data:
            data = self.channel.recv(4096)
            reply += data
            if reply.find("\n") != -1:
                break
        reply = reply.rstrip().lower();
        logfile.write("["+self.details [0]+"] Answer: "+reply+"\n")
        print "["+self.details [0]+"] Answer: "+reply
        p = re.compile(splitquestion[1].lower(), re.IGNORECASE)
        if not p.match(reply):
            self.channel.send ("Try again!!!\n")
            self.channel.close()
            logfile.write("["+self.details [0]+"] Disconnected\n")
            print "["+self.details [0]+"] Disconnected"
            return
        else:
            self.channel.send ('\rCorrect!!!\n')
            continue
      self.channel.send ("You won!!! The flag is "+args.flag+"\n")
      self.channel.close()
      logfile.write("["+self.details [0]+"] Disconnected\n")
      print "["+self.details [0]+"] Disconnected"

# Set up the server:
server = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
server.bind ( ( '', args.port ) )
server.listen ( 5 )

# Have the server serve "forever":
while True:
   channel, details = server.accept()
   ClientThread ( channel, details ).start()


