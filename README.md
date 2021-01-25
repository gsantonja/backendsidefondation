# backendsidefondation
*Backend Side Fondation is a tools designed  to prepare a  terminal or console application.  It is built using npyscreen framework and django framework in a standalone mode. It can use encrypted field. It has been used on linux terminal, on cygwin terminal on windows and termux terminal on android.*

How it work?
============

You have 2 parts :<br>
Part A : The standalone appplication : the standalone application is called `a_p_p_l_i_c_a_t_i_o_n_N_a_m_e`  and you can launch out of the box it with this command :<br>
>1. active your python environnement and go to backendsidefondation directory <br>
>2. type <br>
    >`python ./fondation/m_y_A_p_p_l_i_c_a_t_i_o_n.py`
>3. you will need login (test) and password (test)<br>

Part B : The replace script : the replace script will generate your application code based on `a_p_p_l_i_c_a_t_i_o_n_N_a_m_e` code and the ini file. After generating this application you will need to customize it<br>

Installation
============

The best solution is to create your own environment
In your directory create your env

    python -m venv ./myvenv
in ./myenv/bin

    source ./activate

it's work with python version 3.7.3

    pip install django npyscreen django-cryptography simple-crypt

if you have a problem please check the version with requirements.txt
go to backendSideFondation/src
verify that youre are in the same directory like manage.py

    python ./fondation/m_y_A_p_p_l_i_c_a_t_i_o_n.py

Documentation
=============

For now there is not a documentation yet.

Here is a brief tuto :/documentation/light_tutorial.md


Official Repository
===================

There is a github repository at:

https://github.com/gsantonja/backendsidefondation


Installation
============


Support
=======
Please use the Issue Tracker on this page to report bugs and other problems, or to make feature requests.


Licence
=======
Backend Side Fondation is released under BSD Licence like npyscreen
----


Python 2 support
================

Thiis application doesn't work with python 2
