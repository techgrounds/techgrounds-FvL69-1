## BASH SCRIPTING:

A BASH script is a file containing a series of commands. The shell
reads this file and carries out the commands as though they have been 
entered directly on the command line.

To successfully create and run a shell script, we need to do three things:
* Write a script. 
* Make the script executable.
* Put the script somewhere the shell can find it.

## KEY-TERMS

* **BASH** = Bourne Again Shell, the LINUX/UNIX CLI (command line interface)
* **nano** = text editor (to write the script)
* **$PATH** = environment variable used to set the path to an executable file
* **HTTPd** = Apaches Hyper Text Transfer Protocol deamon
* **script** = Scripting allows for an automatic commands execution 

## ASSIGNMENT:

### Exercise 1
* Create a directory called 'scripts'
* Add scripts dir to $PATH
* Create a script that appends a line of text to a text file
* Create a script that installs the httpd package, activates httpd and enables httpd
* Finally, your script prints the status of httpd to the terminal

### Exercise 2
* Create a script that generates a random number between 1 and 10.
* Stores it in a variable and appends it to a text file.

### Execise 3
* Create a script that generates a random number between 1 and 10.
* Stores it in a variable and appends it to a text file if the number is bigger than 5.
* The script appends a line of text if the number is less than or equal to 5.


## USED RESOURCES:

[LNX-scripting](https://linuxconfig.org/bash-scripting-tutorial-for-beginners)

[LNX-appnd](https://linuxhint.com/bash_append_line_to_file/)

[Apache-Install](https://www.digitalocean.com/community/tutorials/how-to-install-the-apache-web-server-on-ubuntu-20-04#step-3-checking-your-web-server)

[Init-server-setup](https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-20-04)

[Random_num](https://linuxhint.com/generate-random-number-bash/)


## DIFFICULTIES:

## Exercise 1:
* I had no real difficulties.

## Exercise 2:
* None.

## Exercise 3:
* None.

## RESULT:

## Exercise 1:
### Creating scripts directory
### Add scripts dir to $PATH permanently by adding it to the .bashrc file

![PrntScr](../00_includes/SCREENSHOTS/Linux/scripts1.png)

![PrntScr](../00_includes/SCREENSHOTS/Linux/SetPATH.png)



### This bash script takes any text file as positional parameter in which you want to append text.


![PrntScr](../00_includes/SCREENSHOTS/Linux/scripts3.png)

### The bash script code in nano

![PrntScr](../00_includes/SCREENSHOTS/Linux/scripts4.png)


### Prerequisites for apache2 set up , setting up a basic firewall

![PrntScr](../00_includes/SCREENSHOTS/Linux/init_server_setup.png)

![PrntScr](../00_includes/SCREENSHOTS/Linux/allowApache.png)

### Installed, activated and enabled apache2 by bash script.

![PrntScr](../00_includes/SCREENSHOTS/Linux/nanoApacheScript.png)

![PrntScr](../00_includes/week1/SCREENSHOTS/apache2server.png)


## Exercise 2:

### Creating a script that produces a random number.

![PrntScr](../00_includes/SCREENSHOTS/Linux/randomNum1.1.png)

![PrntScr](../00_includes/SCREENSHOTS/Linux/randomNum1.0.png)

## Exercise 3:

### Creating a script that produces a random number with added functionality.

![PrntScr](../00_includes/SCREENSHOTS/Linux/randomNum2.0.png)

![PrntScr](../00_includes/SCREENSHOTS/Linux/randomNum2.1.png)