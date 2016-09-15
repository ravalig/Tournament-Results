TOURNAMENT RESULTS:

In this project developed a database schema to store the game matches between players.
Code uses postgresql to query this data and determine the winners of various games.

This project has three modules:

tournament.sql  - this file is used to set up your database schema (the table representation of your data structure).

tournament.py - this file is used to provide access to your database via a library of functions which can add, delete or
                query data in your database to another python program (tournament_test.py).

tournament_test.py - this is a client program which will use your functions written in the tournament.py module.

SETUP:

1. Install Vagrant
   (https://www.vagrantup.com)

2. Install Virtual Box
   (https://www.virtualbox.org)

3. Clone the fullstack-nanodegree-vm repository from github
   (https://github.com/udacity/fullstack-nanodegree-vm)

4. Navigate to the full-stack-nanodegree-vm/tournament directory in the terminal

5. Type the command vagrant up (powers on the virtual machine)

6. Type the command vagrant ssh (logs into the virtual machine)

7. Change to vagrant directory cd /vagrant

8. Type psql command to launch psql command line interface

9. Type \c tournament which connects to the database

10.Type \i tournament.sql which executes the sql commands

11.Type \q to exit the psql command line interface

12.Run the application using 'python tournament_test.py' from command line

13.Displays the success message