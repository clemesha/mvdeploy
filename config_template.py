#
# IMPORTANT: Copy this file to 'config.py', and fill in missing values.
#

# *MUST* CHANGE BELOW:
AWS_ACCESS_KEY = ""
AWS_SECRET_ACCESS_KEY = ""
KEY_FILENAME = "" #AWS private keypair name. Must be full path.
KEY_NAME = ""


# POSSIBLY CHANGE BELOW:
AMI_ID = "ami-ab36fbc2" # EBS micro instace, us-east-1 - Ubuntu Ubuntu 10.04 LTS (Lucid Lynx)
INSTANCE_TYPE = "t1.micro"
EC2_ZONE = "us-east-1a"


# MOST LIKELY ACCEPTABLE DEFAULTS:
APP_USER = "app"
ENV_USER = "ubuntu" #Ubuntu 10.04 and up
CHEF_RESOURCES_ROOT = "/opt/chef"
