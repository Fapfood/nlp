import jellyfish
import yaml
from project2.inflection import inflection


def load_config(file_name):
    with open('{}'.format(file_name), encoding='utf8') as stream:
        dic = yaml.load(stream)
        return dic


def get_names(root):
    all_names = []
    names = inflection(root['name'], root['type'])
    all_names += names
    for alias in root.get('aliases', []):
        names = inflection(alias['name'], alias['type'])
        all_names += names
    return all_names


def all_substrings(string):
    res = [string[i: j] for i in range(len(string)) for j in range(i + 1, len(string) + 1)]
    return res


def match_string(string, templates, max_distance=2):
    min_distance = float('inf')
    min_index = None
    for i, template in enumerate(templates):
        distance = jellyfish.levenshtein_distance(string, template)
        if distance < min_distance:
            min_distance = distance
            min_index = i
    if min_distance <= max_distance:
        return min_index, min_distance
    else:
        return None


def match_substrings(substrings, templates, max_distance=2):
    res = []
    for string in substrings:
        m = match_string(string, templates, max_distance)
        if m is not None:
            res.append((string, m[1], templates[m[0]]))
    if len(res) > 0:
        """sorting firstly by distance and secondly by length"""
        m = min(res, key=lambda x: x[1] * 100 - len(x[0]))
        """return matched substring, distance"""
        return m[0], m[1]
    else:
        return None


def remover(string, substring):
    return string.replace(substring, '')


def cleaner(string):
    return ' '.join(string.lower().split())


def house_matcher(string, root):
    commands = root.get('commands', [])
    if len(commands) == 0:  # None or empty
        return 'Error: No commands found in: "{}"'.format(root['name'])

    string = cleaner(string)
    res = []
    err = []
    for command in commands:
        command_match = command_matcher(string, command)
        if type(command_match[0]) is not str:
            res.append(command_match)
        else:
            err.append(command_match)
    if len(res) > 0:
        """sorting firstly by distance and secondly by length"""
        m = min(res, key=lambda x: x[2] * 100 - len(x[1]))
        return m[0], m[1]
    else:
        """sorting firstly by depth and secondly by length"""
        m = max(err, key=lambda x: x[1])
        return m[0]


def command_matcher(string, root):
    match = match_substrings(all_substrings(string), get_names(root))
    if match is None:  # not found in substrings
        return 'Error: Command not found: "{}"'.format(string), 0
    matched_string, distance = match
    if len(root.get('configs', [])) == 0:  # None or empty // stop recurrence
        return (root['code'],), matched_string, distance
    commands = []
    for config in root['configs']:
        tmp_conf = load_config(config)
        if len(tmp_conf.get('commands', [])) > 0:  # Not empty
            commands += tmp_conf['commands']
    if len(commands) == 0:  # None or empty
        return 'Error: No commands found in: "{}"'.format(root['name']), 0

    string = cleaner(remover(string, matched_string))
    res = []
    err = []
    for command in commands:
        command_match = command_matcher(string, command)
        if type(command_match[0]) is not str:
            res.append(command_match)
        else:
            err.append(command_match)
    if len(res) > 0:
        """sorting firstly by distance and secondly by length"""
        m = min(res, key=lambda x: x[2] * 100 - len(x[1]))
        return (root['code'], *m[0]), '{} | {}'.format(matched_string, m[1]), distance + m[2]
    else:
        """sorting firstly by depth and secondly by length"""
        m = max(err, key=lambda x: x[1])
        return '{} in: "{}"'.format(m[0], root['name']), m[1] + 1


def post_processor(res):
    if type(res) is str:
        return res
    else:
        res = res[0]
        return ' '.join([res[2], res[1], *res[3:]])


if __name__ == '__main__':
    conf = load_config('rooms.yml')

    with open('data.txt', encoding='utf8') as f:
        tests = f.read().splitlines()

    for test in tests:
        query, answer, _ = test.split(';')
        hm = house_matcher(query, conf)
        print(post_processor(hm), '|', answer, '|', query)

    while True:
        print(house_matcher(input(), conf))
