from subprocess import check_output, STDOUT
import re
import os
import argparse


def get_devs_by_mount(input, prefixes=['/dev/mm.', '/dev/mapper']):
    """Return list of mounted devices by mount input"""
    if type(input) is str:
        input = input.split('\n')
    result = list()
    for line in input:
        hit = [re.match('({}[^\s]+)\son\s([^\s]+).*'.format(prefix), line) for prefix in prefixes]
        if any(hit):
            result.append(re.match('([^\s]+).*', line).group(1))
    return result


def get_connected_devs(_dir='/dev', prefixes=['/dev/mm.', '/dev/mapper']):
    """Return connected partitions"""
    prefixes = prefixes.split(',')
    devs = os.listdir(_dir)
    result = list()
    for dev in devs:
        dev = '{}/{}'.format(_dir, dev)
        if any([re.match('{}.*'.format(prefix), dev) for prefix in prefixes]):
            result.append(dev)
    return result


def mount_device(dev, mountroot='/mnt'):
    """Mount device"""
    dev_dir = '{}/{}'.format(mountroot, dev.split('/')[-1])
    if not os.path.isdir(dev_dir):
        os.mkdir(dev_dir)
    print 'Mounting {} to {}'.format(dev, dev_dir)
    check_output('mount {} {}'.format(dev, dev_dir), shell=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Application for mounting unmounted devices')
    parser.add_argument('--device_prefixes', help='default: /dev/sd[a-z][1-9]', metavar='device', default='/dev/sd[a-z][1-9]')
    parser.add_argument('--mount_root', metavar='dir', help='default: /mnt', default='/mnt')
    parser.add_argument('--device_dir', metavar='dir', help='default: /dev/', default='/dev')
    args = parser.parse_args()
    mounts = check_output('mount', stderr=STDOUT)
    mounted_devs = get_devs_by_mount(mounts, prefixes=args.device_prefixes)
    connected_devs = get_connected_devs(_dir=args.device_dir, prefixes=args.device_prefixes)

    for connected_dev in connected_devs:
        if not connected_dev in mounted_devs:
            mount_device(connected_dev, mountroot=args.mount_root)
