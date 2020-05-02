# Connect to  EC2 Instance

## Prerequistites

The following items are need in order to SSH into an EC2 instance. If you don't have one of these, contact Grant.
- PEM file that contains your access key

## Installation

1. Save your PEM file called `infectionsim-worker.pem` in `~/.ssh`. This acts as your key to authenticate you with AWS.

2. Set the permissions to your PEM file by executing the following at command line

       cd ~/.ssh; chmod 600 ~/.ssh/infectionsim-worker.pem

2. Add the following to `~/.bash_profile`. This will create a useful command to call from command line to connect to machine. 

       ssh_is () { ssh -i ~/.ssh/infectionsim-worker.pem ec2-user@"$1" ; }
       alias start_alex_worker='aws ec2 start-instances --instance-id i-03fe1e6a5ee8eb1ab --region us-east-1 --profile is'
       alias stop_alex_worker='aws ec2 stop-instances --instance-id i-03fe1e6a5ee8eb1ab --region us-east-1 --profile is'
       alias start_joelle_worker='aws ec2 start-instances --instance-id i-0c0e82af81969e2e3 --region us-east-1 --profile is'
       alias stop_joelle_worker='aws ec2 stop-instances --instance-id i-0c0e82af81969e2e3 --region us-east-1 --profile is'
       alias get_alex_worker_ip='aws ec2 describe-instances --profile is --region us-east-1 --instance-id i-03fe1e6a5ee8eb1ab | grep PublicIpAddress'
       alias get_joelle_worker_ip='aws ec2 describe-instances --profile is --region us-east-1 --instance-id i-0c0e82af81969e2e3 | grep PublicIpAddress'
3. Execute `source ~/.bash_profile` to make `ssh_is` executable. Note, you only have to do this now. Whenever you open a new terminal window, `.bash_profile` is automatically sourced.

## Start/Stop Machine

**WARNING:** Only start or stop your own machine. Also, *only stop your machine if you have no active processes running*. Any processes running when a machine stops will be terminated. Data will not be lost.

1. To start your machine, execte `start_[NAME]_worker`
2. To stop your machine, execute `stop_[NAME]_worker`

## Connect
1. Get the IP address by executing `get_[NAME]_worker_ip`. Copy and paste just the IP address (without quoatation marks `"` ) to clipboard.
2. Connect to the machine by executing the following at command line

       ssh_is [IP_ADREESS]
3. If a prompt asks if you are sure you want to connect, type `yes` and hit `Enter`.

## Disconnect

1. Execute `logout`.


## Troubleshooting
If you are unable to connect to the machine, check the following:
- Is your PEM file in `~/.ssh`?
- Is your instance started?
