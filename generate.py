import json
import os
import requests
import glob
import string
import csv
import operator

GET_BUGS = True

schema_locations = [
    './schemas/',
]
schema_skip = [
    './schemas/context_menus_internal.json',
]
usage_file = 'apiusage.csv'

parsed_schema = {}

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

def print_schema(schema, type_, api):
    if not schema:
        return
    for key, value in schema.items():
        rank = parsed_usage.get(value['usage'], None)
        if not rank:
            continue
        del parsed_usage[value['usage']]
        if value['deprecated']:
            status = "DEP"
        else:
            status = '' if value['supported'] else 'NO'
        print "%-3s %04s %s" % (status, rank, value['full'],)
        if value['deprecated']:
            print "         %s" % value['deprecated']

def process_schemas(directories):
    for directory in directories:
        for fname in glob.glob(directory + '*.json'):
            if fname in schema_skip:
                print 'Skipping:', fname
                continue
            # print 'Parsing:', fname
            lines = open(fname, 'r').readlines()
            # Strip out stupid comments.
            newlines = []
            for line in lines:
                if not line.startswith('//'):
                    newlines.append(line)

            process_json(json.loads('\n'.join(newlines)))


def process_json(data):
    for element in data:
        for k, v in element.items():
            if k == 'namespace' and v != 'manifest':
                parsed_schema['__current__'] = v

    for element in data:
        for k, v in element.items():
            if k == 'functions':
                for function in v:
                    process_type('functions', function)
            if k == 'events':
                for event in v:
                    process_type('events', event)


def process_type(type_, data):
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
    print "OK Rank API"
    apis = {}
    for key, value in sorted(parsed_usage.items(), key=operator.itemgetter(0)):
        apis[key.split('.')[1]]=1

    for api in sorted(apis):
        print "\n======= chrome.%s" % (api,)
        schemas = parsed_schema.get(api, {})
        print_schema(schemas.get('functions', []), 'functions', api)
        print_schema(schemas.get('events', []), 'events', api)
        for key, value in sorted(parsed_usage.items(), key=operator.itemgetter(0)):
            if key.startswith("chrome.%s" % (api,)):
                print "NO  %04s %s" % (value, key,)
        pile_of_bugs = None
        if GET_BUGS:
            pile_of_bugs = bugs(api)
            for bug in pile_of_bugs['bugs']:
                print "Bug      %s: %s" % (bug['id'], bug['summary'],)
            
if __name__=='__main__':
    parsed_usage = parse_usage()
    process_schemas(schema_locations)
    print_usage()
