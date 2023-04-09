import sys
import subprocess

def parse(statfile):
    stats = {}
    curr_stat = {}
    curr_node_name = None
    for l in statfile:
        if l == '':
            stats[curr_node_name] = curr_stat
            curr_stat = {}
            curr_node_name = None
        elif l.startswith('    '):
            key, value = l.strip().split(' = ')
            if key == 'jobs':
                joblist = {}
                jobs = value.split(', ')
                for j in jobs:
                    job, core = j.split('/')
                    joblist[int(core)] = job
                curr_stat[key] = joblist
            else:
                curr_stat[key] = value
        else:
            curr_node_name = l.strip()
    return stats

if __name__ == "__main__":
    raw_stats = subprocess.run(['pbsnodes', '-a'], encoding='utf-8', stdout=subprocess.PIPE)
    stats = parse(raw_stats.stdout.split('\n'))

    nokhas = False
    if (len(sys.argv) > 1 and sys.argv[1] == '--nokhas'):
        nokhas = True

    print('Free GPUs: ')
    gpu_avlbl_key = 'resources_available.ngpus'
    gpu_ass_key = 'resources_assigned.ngpus'
    for node, stat in stats.items():
        if not stat or stat['state'] != 'free':
            continue
        if nokhas and node.startswith('khas'):
            continue
        if gpu_avlbl_key in stat:
            if gpu_ass_key not in stat:
                print(f'{node} has no assigned GPUs?')
            elif int(stat[gpu_avlbl_key]) > int(stat[gpu_ass_key]):
                print(node)

