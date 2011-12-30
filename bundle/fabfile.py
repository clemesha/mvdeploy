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

env.user = config.ENV_USER 
env.key_filename = config.KEY_FILENAME

AMI_DIR = "/mnt/ami"
BUNDLE_VOL = "euca-bundle-vol -d %(ami_dir)s -k %(pk)s -c %(cert)s -u %(account_number)s -r %(arch)s -p %(image_name)s"
BUNDLE_UPLOAD="euca-upload-bundle -b %(bucket)s -m %(image_name)s.manifest.xml -a %(access_key)s -s %(secret_key)s -U https://s3.amazonaws.com"
REGISTER_AMI="euca-register --debug -a %(access_key)s -s %(secret_key)s -U https://ec2.amazonaws.com %(bucket)s/%(image_name)s.manifest.xml"


def bundle():
    """STEPS: 1) put creds 2) create image 3) upload image 4) register """
    image_name = "%s-%s" % (config.BUCKET_NAME, datetime.datetime.now().isoformat().split("T")[0])
    sudo("if [ ! -d %s ]; then mkdir %s; fi" % (AMI_DIR, AMI_DIR))
    sudo("chown ubuntu:ubuntu %s" % AMI_DIR)
    put(os.path.join(config.PEM_FILE_DIR, config.PK_PEM_FILE), os.path.join(AMI_DIR, config.PK_PEM_FILE))
    put(os.path.join(config.PEM_FILE_DIR, config.CERT_PEM_FILE), os.path.join(AMI_DIR, config.CERT_PEM_FILE))
    env = {
        "pk":config.PK_PEM_FILE,
        "cert":config.CERT_PEM_FILE,
        "ami_dir":AMI_DIR,
        "arch":"i386",
        "bucket":config.BUCKET_NAME,
        "image_name":image_name,
        "account_number":config.AWS_ACCOUNT_NUMBER,
        "access_key":config.AWS_ACCESS_KEY,
        "secret_key":config.AWS_SECRET_ACCESS_KEY
    }
    with cd(AMI_DIR):
        bundle_cmd = (BUNDLE_VOL % env)
        sudo(bundle_cmd)
        bundle_upload_cmd = (BUNDLE_UPLOAD % env)
        sudo(bundle_upload_cmd)
        register_ami_cmd = (REGISTER_AMI % env)
        sudo(register_ami_cmd)
