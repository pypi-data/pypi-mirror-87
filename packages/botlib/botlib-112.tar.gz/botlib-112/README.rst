README
######

Welcome to BOTLIB,

BOTLIB is a pure python3 bot library you can use to program bots.
BOTLIB uses a JSON in file database with a versioned readonly storage. It 
reconstructs objects based on type information in the path and is a "dump 
OOP and use OP" programming library where the methods are factored out into
functions that use the object as the first argument. This to obtain a clean
namespace object, which has no methods to clutter the namespace. A "clean",
still has hidden methods, loadable from JSON object, that provides load/save
methods to other classes derived from Object.

BOTLIB is placed in the Public Domain and has no COPYRIGHT and no LICENSE.

INSTALL
=======

installation is through pypi:

::

 > sudo pip3 install botlib

if you have previous versions already installed and things fail try to force reinstall:

::

 > sudo pip3 install botlib --upgrade --force-reinstall

if this also doesn't work you'll need to remove all installed previous versions, so you can do a clean install.

you can run directly from the tarball, see https://pypi.org/project/botlib/#files

OBJECT PROGRAMMING
==================

BOTLIB provides a "move all methods to functions" like this:

::

 obj.method(*args) -> method(obj, *args) 

 e.g.

 not:

 >>> from bot.obj import Object
 >>> o = Object()
 >>> o.set("key", "value")
 >>> o.key
 'value'

 but:

 >>> from bot.obj import Object, set
 >>> o = Object()
 >>> set(o, "key", "value")
 >>> o.key
 'value'

it's a way of programming with objects, replacing OOP. Not object-oriented 
programming, but object programming. If you are used to functional programming
you'll like it (or not) ;]

MODULES
=======

BOTLIB provides the following modules:

::

    bot.bus          - messaging
    bot.clk          - clock/repeater
    bot.cmd          - commands
    bot.csl          - console
    bot.dbs          - databases
    bot.hdl          - handler
    bot.irc          - internet relay chat
    bot.obj          - objects
    bot.ofn          - object functions
    bot.prs          - parser
    bot.rss          - rich site syndicate
    bot.thr          - threads
    bot.trm          - terminal
    bot.udp          - udp to irc relay

USAGE
=====

BOTLIB is a library and doesn't have it's own CLI, however a bot test
program is provided with the tarball. you can run the bot command on the prompt, it will return with no response:

:: 

 $ ./bin/bot
 $ 

you can use bot <cmd> to run a command directly, use the cmd command to see a list of commands:

::

 $ ./bin/bot cmd
 cfg,cmd,dne,dpl,fnd,ftc,log,mbx,rem,rss,tdo,tsk,udp,upt,ver

BOTLIB also has it's own shell, use bot -s to start a bot shell:

::

  $ ./bin/bot -s
  > cmd
  cfg,cmd,dne,dpl,fnd,ftc,log,mbx,rem,rss,tdo,tsk,udp,upt,ver

IRC
===

configuration is done with the cfg command:

::

 $ ./bin/bot cfg
 channel=#botlib nick=botlib port=6667 server=localhost

you can use setters to edit fields in a configuration:

::

 $ ./bin/bot cfg server=irc.freenode.net channel=\#botlib nick=botlib
 channel=#botlib nick=botlib port=6667 server=irc.freenode.net

to have the irc bot started use the mods=irc option at start:

::

 $ ./bin/bot mods=irc

RSS
===

BOTLIB provides with the use of feedparser the possibility to server rss
feeds in your channel. BOTLIB itself doesn't depend, you need to install
python3-feedparser first:

::

 $ sudo apt install python3-feedparser
 $

adding rss to mods= will load the rss module and start it's poller.

::

 $ ./bin/bot mods=irc,rss

to add an url use the rss command with an url:

::

 $ ./bin/bot rss https://github.com/bthate/botlib/commits/master.atom
 ok 1

run the rss command to see what urls are registered:

::

 $ ./bin/bot fnd rss
 0 https://github.com/bthate/botlib/commits/master.atom

the ftc (fetch) command can be used to poll the added feeds:

::

 $ ./bin/bot ftc
 fetched 20

UDP
===

BOTLIB also has the possibility to serve as a UDP to IRC relay where you
can send UDP packages to the bot and have txt displayed on the channel.

use the 'bot udp' command to send text via the bot to the channel on the irc server:

::

 $ tail -f /var/log/syslog | ./bin/bot udp

output to the IRC channel can be done with the use python3 code to send a UDP packet 
to botlib, it's unencrypted txt send to the bot and display on the joined channels.

to send a udp packet to botlib in python3:

::

 import socket

 def toudp(host=localhost, port=5500, txt=""):
     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
     sock.sendto(bytes(txt.strip(), "utf-8"), host, port)

CONTACT
=======

"contributed back to society."

you can contact me on IRC/freenode/#dunkbots or email me at bthate@dds.nl

| Bart Thate (bthate@dds.nl, thatebart@gmail.com)
| botfather on #dunkbots irc.freenode.net
