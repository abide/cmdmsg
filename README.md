cmdmsg
======

utility class for 'overwrite logging' to the command line using backspace characters

the idea is that a single line message can be overwritten repeatedly to give an up-to-date status display without generating huge amounts of output.

the "say" method updates the one-line message.

the "spit" method clears the current status line, outputs the provided message with a newline and then puts the status message back.

there is a default one-second delay between updates so you can call "say" as often as you like without hurting performance.

to do
=====

* turn this list into issues
* check cross-platform/cross-shell functionality
* use a lambda callback so that complex message creation is only executed if the message is actually going to be displayed
