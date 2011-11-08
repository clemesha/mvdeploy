import os
import sys
import glob
import datetime
import boto
from fabric.api import env, run, local, put, cd
from fabric.contrib import files

#local code:
sys.path.insert(0, ".") 
import config
import ec2provision

env.user = config.ENV_USER 
env.key_filename = config.KEY_FILENAME


def bootstrap(target="testing"): 
    """
    'target' will be one of: {'testing', 'staging', 'production'}.
    """
    run("sudo apt-get -q update")
    run("sudo adduser --gecos GECOS --disabled-password %s" % config.APP_USER)
    run("sudo chef-solo -l debug -c /tmp/config.rb -j /tmp/attrs.rb")


def _provision_instance():
    access_key, secret_key = config.AWS_ACCESS_KEY, config.AWS_SECRET_ACCESS_KEY
    ami_id = config.AMI_ID
    key_name = config.KEY_NAME
    instance_type = config.INSTANCE_TYPE
    placement = config.EC2_ZONE
    prov_host = ec2provision.run_instance(access_key, secret_key, ami_id, key_name, instance_type=instance_type, placement=placement) 
    return prov_host.dns_name


def deploy():
    """ Deploy app to AWS."""
    provisioned_host = _provision_instance()
    print "Deploying to '%s' ... bootstraping backend...\n" % (provisioned_host, )
    env.user, env.host_string = config.ENV_USER, provisioned_host #set 'host_string' to EC2 host.
    print "Success.  Host=> %s " % (provisioned_host,)


