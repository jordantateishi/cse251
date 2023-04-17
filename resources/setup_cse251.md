# Setting up your development environment for CSE 251

- [ ] [Install Visual Studio Code IDE](#install-vscode)
- [ ] [Remove old Python](#remove-old-versions-of-python)
- [ ] [Install Python](#install-python)
- [ ] [Install Python Modules](#install-modules)
- [ ] [Install Git](#install-git)

## <a name="install-vscode">Install Visual Studio Code IDE
There are a number of IDEs [Integrated Development Environments](https://en.wikipedia.org/wiki/Integrated_development_environment) available to programmers. You are free to use any editor that you want.  However, the course will use Visual Studio Code as the editor in video examples and during class time.  VSCode can be downloaded at [VSCode](https://code.visualstudio.com).

## Remove old versions of Python
See [remove old versions of Python](remove-old-versions-of-python.md)

### Packages to install in VSCode 

Within VS Code, click on Extensions:

![image](vscode-extensions.PNG)

Then search for Python and install the Microsoft one (it will have millions of downloads). This is not the same Python that you will use to run your code. This extension will enable the VS Code IDE to offer feedback as you type your code. One of the benefits of typing your code in an IDE is that it can help you with code completion, show errors before you run your code, documentation, and code navigation. 

## <a name="install-python"></a>**Install Python**
We will be using Python throughout the course. Please ensure that you have version 3.11 or higher.  Python can be [downloaded here](python.org/downloads). This semester we will be using [python-version](python-version.md).

Python needs to be installed on your computer (separate from installing Python in VS Code). After you install Python on your computer, open a terminal (command prompt) 
and type either `py --version` or `python3 --version` (this should show you the version that you installed). 

![image](python-version.png)

You want to use this version of Python when you press the RUN button in VS Code. To make this happen, in VS Code, press Ctrl+3 (if you are on a Mac, go to Help and click 'Show All Commands'). Then type "Python: Select Interpreter":

![image](https://user-images.githubusercontent.com/8828821/207205249-efb963f1-b62a-4672-9534-5b722febd847.png)

Select the version of Python that you downloaded. VS Code will recommend that you use the Microsoft version, but it is old:

![image](https://user-images.githubusercontent.com/8828821/207205435-745e1eba-bb2d-46c7-9510-c4ce0e193feb.png)

## <a name="install-modules"></a> **Install Python Modules**
In this class, we will be using some modules/packages that do not come installed by default with the base Python install. To install modules/packages in python, we will use an app called 'pip' (see https://www.w3schools.com/python/python_pip.asp). 

### Install pip
Open a terminal inside of VS Code and check if you have pip installed by typing:
>pip --version
(Note: mac users may need to type pip3)

https://phoenixnap.com/kb/install-pip-mac

If it doesn't recognize what "pip" is than install pip:
Windows --> https://www.geeksforgeeks.org/how-to-install-pip-on-windows/
Mac --> https://phoenixnap.com/kb/install-pip-mac

### Install necessary modules using pip
From a terminal inside of VS Code, type:
>py -m pip install \<name of the module shown below\>

The following modules/packages need to be installed for use in our CSE251 class:
1. requests 
2. numpy
3. matplotlib
4. Pillow
5. opencv-python

## <a name="install-git"></a> **Install Git**
Git comes preinstalled with your VS Code. You only need to clone our class repo. If you are reading this page in a browser, then you are inside of the the class repo. To clone it, go to the top most directory of the repo. The name of the repo changes each semester, but follows the pattern of "https://github.com/brandonfoushee/cse251\<semesterYY\>" where semester is 's', 'f', 'w' (for spring, fall, winter) and YY is the last two digits of the year.

So if this semester was Winter 2023, then the repo name would be https://github.com/brandonfoushee/cse251s23. You can always see the directory structure using the breadcrumb at the top in GitHub:

![](breadcrumb.PNG)

Click on the repo name in the breadcrumb and then click the "Code" button to get a copy of the repo path, use the HTTPS link.

You would then open a terminal in VS Code (using cd, navigate to where you want to clone the repo) and type:
git clone https://github.com/brandonfoushee/cse251s23.git  (or paste in the link that you copied)

This will create a cse251s23 (or whatever the semester and year is) directory in the directory in which you are in. 

Now you have all the files for the class.
