# Motivation

- Often we create secure connections to remote machines (i.e. ssh into a machine) 
  as part of our work flow
- For security purposes, these connections cannot remain open indefinitely, 
  and the connection is terminated after a set period of time, whether or not 
  there are processes running
- The `tmux` package offers a work around

# Getting Started
  
For ease of use, add the following to your `~/.bash_profile`, then restart your 
shell or execute `source ~/.bash_profile`.
```shell
alias tls='tmux ls'
alias tattach='tmux a -t'
alias tnew='tmux new'
alias tkill='tmux kill-ses -t'
```

# Instructions

- Create a new window with the `tnew` command
![](https://cdn.cacher.io/attachments/u/3cfsxkosk01w7/FvjgzqHIwCDZHon4MqpxqRDi1S977vbS/new_tmux_window.png)
You'll know that you are in a `tmux` window by the green bar at the bottom.

- By default, `tmux` names the windows with sequential integers. I prefer to 
  rename my windows. You can do this by hitting `ctrl+b;$` (`x;y` denoting press `x`, release, and then press `y`). 
![](https://cdn.cacher.io/attachments/u/3cfsxkosk01w7/bYSEVYwkaW3PDRlXf4loX8sl0iUpbhYM/rename_tmux_window.png)
You'll know you are in "Rename Mode", because the bar at the bottom changes to a mustard color.

 - Delete the existing name, typing a new name (I use "example"), and . `Enter`. The bar should turn green again.
 - To detach from a window *while keeping it running the brackground*, press `ctrl+b;d`. 
   The green bar will disappear, and you will see (with "example" replaced by whatever you renamed your window)
 ```shell
 [detached (from session example)]
  ```
  - To re-attach to this window, use the command `tattach example`,  replace `example` with the window name to which you'd like to attach.
  - If you need to see what active windows you have, use the command `tls`.
  - To permanently close a window and terminate all processes, use the command `tkill example`, replacing `example` with the window name.
