from subprocess import check_output, STDOUT
import re
import os


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
    devs = os.listdir(_dir)
    result = list()
    for dev in devs:
        dev = '{}/{}'.format(_dir, dev)
        if any([re.match('{}.*'.format(prefix), dev) for prefix in prefixes]):
            result.append(dev)
    return result


if __name__ == '__main__':
    mounts = check_output('mount', stderr=STDOUT)
    mounted_devs = get_devs_by_mount(mounts)
    connected_devs = get_connected_devs()
    print connected_devs
