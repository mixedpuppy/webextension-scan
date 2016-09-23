import json
import os
import requests
import glob
import string
import csv
import operator

GET_BUGS = True

schema_locations = [
    './schemas/nightly/',
    './schemas/aurora/',
    './schemas/beta/',
    './schemas/release/',
]
schema_skip = [
    'context_menus_internal.json',
]
usage_file = 'apiusage.csv'

versioned_schemas = {}

def bugs(whiteboard):
    # print "search bugs for %s" % whiteboard
    res = requests.get(
        'https://bugzilla.mozilla.org/rest/bug',
        params={
            'product': 'Toolkit',
            'component': ['WebExtensions',
    'WebExtensions: Android', 'WebExtensions: Compatibility', 'WebExtensions: Untriaged',
    'WebExtensions: Developer tools', 'WebExtensions: Experiments', 'WebExtensions: Frontend',
    'WebExtensions: General', 'WebExtensions: Request Handling'],
            'whiteboard': '[%s]' % whiteboard,
            'summary': whiteboard,
            'include_fields': 'summary,status,resolution,id',
            'status': ['NEW', 'ASSIGNED', 'UNCONFIRMED', 'REOPENED']
        }
    )
    # print res.request.url
    return res.json()


def parse_usage():
    res = {}
    with open(usage_file) as csvfile:
        reader = csv.DictReader(csvfile)
        for k, row in enumerate(reader):
            api = row["API"]
            count = len(api.split("."))
            if count < 3:
                continue
            if count > 3:
                api = ".".join(api.split(".")[:3])
            res[api] = k + 1
    return res

def get_status(schema, type_, api):
    if not schema:
        return None
    res = []
    for key, value in schema.items():
        rank = parsed_usage.get(value['usage'], None)
        if not rank:
            continue
        if value['deprecated']:
            status = "D"
        else:
            status = '' if value['supported'] else 'N'
        res.append((status, rank, value['full'], value['deprecated']))
    return res

def process_schemas(directories):
    for directory in directories:
        version = os.path.basename(directory[:-1])
        for fname in glob.glob(directory + '*.json'):
            if os.path.basename(fname) in schema_skip:
                # print 'Skipping:', fname
                continue
            lines = open(fname, 'r').readlines()
            # Strip out stupid comments.
            newlines = []
            for line in lines:
                if not line.startswith('//'):
                    newlines.append(line)

            process_json(version, json.loads('\n'.join(newlines)))


def process_json(version, data):
    versioned_schemas.setdefault(version, {})
    parsed_schema = versioned_schemas.get(version)
    for element in data:
        for k, v in element.items():
            if k == 'namespace' and v != 'manifest':
                parsed_schema['__current__'] = v

    for element in data:
        for k, v in element.items():
            if k == 'functions':
                for function in v:
                    process_type(parsed_schema, 'functions', function)
            if k == 'events':
                for event in v:
                    process_type(parsed_schema, 'events', event)

def process_type(parsed_schema, type_, data):
    namespace = parsed_schema['__current__']
    parsed_schema.setdefault(namespace, {})
    parsed_schema[namespace].setdefault(type_, {})
    full = 'chrome.%s.%s' % (namespace, data['name'])
    mdn = full[:]
    parsed_schema[namespace][type_][data['name']] = {
        'usage': full,
        'full': mdn,
        'supported': not(data.get('unsupported')),
        'deprecated': data.get('deprecated'),
        'data': data
    }

def print_usage():
    print "N A B R Rank API"
    apis = {}
    for key, value in sorted(parsed_usage.items(), key=operator.itemgetter(0)):
        apis[key.split('.')[1]]=1

    v = {}
    for api in sorted(apis):
        print "\n======= chrome.%s" % (api,)
        r = v[api] = {}
        # scan oldest to newest to catch deprecation data
        for version in ['release', 'beta', 'aurora', 'nightly']:
            parsed_schema = versioned_schemas[version]
            schemas = parsed_schema.get(api, {})
            # print version, api
            res = get_status(schemas.get('functions', []), 'functions', api) or \
                get_status(schemas.get('events', []), 'events', api)
            if not res:
                continue
            for a in res:
                e = r.setdefault(a[2], {})
                e.setdefault('release', 'N')
                e.setdefault('beta', 'N')
                e.setdefault('aurora', 'N')
                e.setdefault('nightly', 'N')
                e["full"] = a[2]
                e["rank"] = a[1]
                e["deprecated"] = a[3] or ''
                e[version] = a[0]

        for key, value in sorted(parsed_usage.items(), key=operator.itemgetter(0)):
            d = r.get(key, None)
            if d:
                print "{nightly:1} {aurora:1} {beta:1} {release:1} {rank:4} {full} {deprecated}".format(**d)
            elif key.startswith("chrome.%s" % (api,)):
                print "N N N N %04s %s" % (value, key,)

        pile_of_bugs = None
        if GET_BUGS:
            pile_of_bugs = bugs(api)
            for bug in pile_of_bugs['bugs']:
                print "Bug      %s: %s" % (bug['id'], bug['summary'],)
            
if __name__=='__main__':
    parsed_usage = parse_usage()
    process_schemas(schema_locations)
    print_usage()
