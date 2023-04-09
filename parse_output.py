import sys

def parse(filename):
    stats = {}
    with open(filename, 'r') as statfile:
        curr_stat = {}
        curr_node_name = None
        for l in statfile:
            if l == '\n':
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
    stats = parse(sys.argv[1])

    print('Free GPUs: ')
    gpu_avlbl_key = 'resources_available.ngpus'
    gpu_ass_key = 'resources_assigned.ngpus'
    for node, stat in stats.items():
        if stat['state'] != 'free':
            continue
        if gpu_avlbl_key in stat:
            if gpu_ass_key not in stat:
                print(f'{node} has no assigned GPUs?')
            elif int(stat[gpu_avlbl_key]) > int(stat[gpu_ass_key]):
                print(node)

