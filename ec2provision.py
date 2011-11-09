import os
import sys
import time

import boto


def run_instance(access_key, secret_key, ami_id, key_name, instance_type="t1.micro", placement="us-east-1a", timeout=500, cntstep=5):
    print "Running instance_type='%s' with ami_id='%s' using key_name='%s'..." % (instance_type, ami_id, key_name)
    conn = boto.connect_ec2(access_key, secret_key)
    instances = conn.run_instances(ami_id, instance_type=instance_type, key_name=key_name, placement=placement)
    instance = instances.instances[0]
    time.sleep(5) #Wait a couple seconds to avoid <Code>InvalidInstanceID.NotFound</Code>
    print "===Waiting %d seconds for instance to be running...===" % timeout
    cnt = 0
    while instance.update() != "running":
        cnt += cntstep
        time.sleep(cntstep)
        print "Waiting for instance to be running now for %d seconds..." % cnt
        if cnt == timeout:
            print "FAILED: Timeout reached! Stopping Instance and aborting"
            instance.stop()
            return None 
    return instance
