import os
import sys
import glob
import datetime
import boto
from fabric.api import env, run, local, put, cd, sudo
from fabric.contrib import files

#local code:
sys.path.insert(0, ".") 
import config
import ec2provision

env.user = config.ENV_USER 
env.key_filename = config.KEY_FILENAME


def _provision_instance():
    access_key, secret_key = config.AWS_ACCESS_KEY, config.AWS_SECRET_ACCESS_KEY
    ami_id = config.AMI_ID
    key_name = config.KEY_NAME
    instance_type = config.INSTANCE_TYPE
    placement = config.EC2_ZONE
    prov_host = ec2provision.run_instance(access_key, secret_key, ami_id, key_name, instance_type=instance_type, placement=placement) 
    return prov_host.dns_name


def provision():
    """Deploy app to AWS."""
    provisioned_host = _provision_instance()
    print "Success. Hostname: %s " % (provisioned_host,)


def bootstrap(): 
    """ 
    Install Chef, then install all Chef cookbooks.
    """
    sudo("apt-get -q update")
    sudo("adduser --gecos GECOS --disabled-password %s" % config.APP_USER)
    install_chef()
    setup_chef_env()
    sudo("chef-solo -l debug -c %(root_dir)s/chef_config.rb -j %(root_dir)s/chef_attrs.rb" % {"root_dir":config.CHEF_RESOURCES_ROOT})


def install_chef():
    """Get a recent version of Chef"""
    sudo('echo "deb http://apt.opscode.com/ `lsb_release -cs`-0.10 main" | sudo tee /etc/apt/sources.list.d/opscode.list')
    sudo('sudo mkdir -p /etc/apt/trusted.gpg.d')
    sudo('gpg --keyserver keys.gnupg.net --recv-keys 83EF826A')
    sudo('gpg --export packages@opscode.com | sudo tee /etc/apt/trusted.gpg.d/opscode-keyring.gpg > /dev/null')
    sudo("apt-get update")
    sudo("apt-get -y install chef")


def setup_chef_env():
    root_dir = config.CHEF_RESOURCES_ROOT
    sudo("mkdir -p %(root_dir)s/cookbooks" % {"root_dir":root_dir})
    put("chef_config.rb", "/tmp/chef_config.rb")
    sudo("mv /tmp/chef_config.rb %(root_dir)s/" % {"root_dir":root_dir})
    put("chef_attrs.rb", "/tmp/chef_attrs.rb")
    sudo("mv /tmp/chef_attrs.rb %(root_dir)s/" % {"root_dir":root_dir})
    local("tar -cf cookbooks.tar cookbooks && gzip cookbooks.tar")
    put("cookbooks.tar.gz", "/tmp/cookbooks.tar.gz")
    local("rm cookbooks.tar.gz")
    sudo("mv /tmp/cookbooks.tar.gz %(root_dir)s/" % {"root_dir":root_dir}) 
    sudo("cd %(root_dir)s/ && tar -zxf cookbooks.tar.gz" % {"root_dir":root_dir})
