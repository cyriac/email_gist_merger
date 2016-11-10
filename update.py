import json
import requests
import time

CONFIG = {}
with open('config.json') as f:
    CONFIG = json.load(f)

def github(url):
    r = requests.get(url, auth=(CONFIG['username'], CONFIG['token']))
    return r.json()


def get_gist_data(gist_id):
    return github('https://api.github.com/gists/{}'.format(gist_id))

def get_gist_forks(gist_id):
    return github('https://api.github.com/gists/{}/forks'.format(gist_id))

if __name__ == '__main__':
    gist_ids = [CONFIG['root'], CONFIG['destination']]
    gist_ids.extend([gist['id'] for gist in get_gist_forks(CONFIG['root'])])
    gist_ids.extend([gist['id'] for gist in get_gist_forks(CONFIG['destination'])])

    gist_ids = set(gist_ids)

    gist_data = []
    for i, gist_id in enumerate(list(gist_ids)):
        print("Fetching data for {} ({}/{})".format(gist_id, i+1, len(gist_ids)))
        time.sleep(1)
        gist_data.append(get_gist_data(gist_id))


    final_data = []
    for gist in gist_data:
        if CONFIG['file'] in gist['files']:
            final_data.extend(gist['files'][CONFIG['file']]['content'].split('\n'))
    final_data = list(set(final_data))
    final_data.sort()
    with open(CONFIG['file'], 'w') as f:
        for item in final_data:
            f.write("%s\n" % item)

