import sys
import getopt
import json
from pmabstraction import discover_mr as discover_mr, utils as utils, discover_ta as discover_ta


def show_help():
    '''Prints user help'''
    print()
    print("Usage: ")
    print(" python discover.py --path example.XES ")
    print()
    print("path:     The path of the input event" +
          "log in xes format, required argument")


def get_patterns(log):
    '''Gets a log. Discovers tandem arrays and maximal repeats.
    Returns a list of pattern dictionary containing all id, name,
    pattern alphabet, type, pattern, instance count (%)
    for each discovered pattern'''
    result = []
    id = 0

    for primitive in discover_ta.findPrimitiveTandemArrays(log):
        print("lrn of primitive ", len(primitive[1]))
        if len(primitive[1]) > 1:
            result.append({'ID': id,
                          'Name': 'Group' + str(id),
                           'PatternAlphabet': sorted(list(set(primitive[1]))),
                           'Type': 'PTA',
                           'Pattern': primitive[1]})
        id = id + 1

    for maximalTA in discover_ta.findTandemArrays(log):
        print("lrn of primitive ", len(maximalTA[1]))
        if len(maximalTA[1]) > 1:

            result.append({'ID': id,
                          'Name': 'Group' + str(id),
                           'PatternAlphabet': sorted(list(set(maximalTA[1]))),
                           'Type': 'MTA',
                           'Pattern': maximalTA[1]})
        id = id + 1

    mrs, smrs, nsmrs = discover_mr.pattern_discover(log)

    for p in mrs:
        print("lrn of primitive ", len(p))
        if len(p) > 1:

            result.append({'ID': id,
                          'Name': 'Group' + str(id),
                           'PatternAlphabet': sorted(list(set(p))),
                           'Type': 'MRS',
                           'Pattern': p})
        id = id + 1

    for p in smrs:
        result.append({'ID': id,
                      'Name': 'Group' + str(id),
                       'PatternAlphabet': sorted(list(set(p))),
                       'Type': 'SMRS',
                       'Pattern': p})
        id = id + 1

    for p in nsmrs:
        result.append({'ID': id,
                      'Name': 'Group' + str(id),
                       'PatternAlphabet': sorted(list(set(p))),
                       'Type': 'NSMRS',
                       'Pattern': p})
        id = id + 1

    result = fill_instance_count(log, result)

    return result


def fill_instance_count(log, patterns):
    '''Gets a log and a list of pattern dictonaries.
    Returns the list of pattern dictionaries with the
    correct value for 'InstanceCount' (%) filled'''

#   reset InstanceCount
    for pattern in patterns:
        pattern['InstanceCount'] = 0

#   refill InstanceCount
    activity_classifier = 'concept:name'
    for trace in log:
        sequence = [event[activity_classifier] for event in trace]
        for pattern in patterns:
            if contains_pattern(sequence, pattern['Pattern']):
                pattern['InstanceCount'] = pattern['InstanceCount'] + 1

    for pattern in patterns:
        pattern['InstanceCount'] = (pattern['InstanceCount']/len(log)) * 100

    return patterns


def contains_pattern(sequence, pattern):
    '''Gets a sequence and a pattern, both as a list of strings.
     Returns weather the sequence contains the pattern'''
    sub_set = False
    if pattern == []:
        sub_set = True
    elif pattern == sequence:
        sub_set = True
    elif len(pattern) > len(sequence):
        sub_set = False

    else:
        for i in range(len(sequence)):
            if sequence[i] == pattern[0]:
                n = 1
                while ((n < len(pattern)) and
                       ((n+i < len(sequence)) and
                        (sequence[i+n] == pattern[n]))):
                    n = n + 1
                if n == len(pattern):
                    sub_set = True

    return sub_set


if __name__ == '__main__':

    event_log = ''
    log = None

    try:
        opts, args = getopt.getopt(sys.argv[1:], "l:h", ["path=", "help"])

        if opts == []:
            print('''Required argument --path is missing.
                  Please see help and try again.''')
            exit(0)

        for opt, arg in opts:
            if opt in ("-l", "--path"):
                event_log = arg
            elif opt in ("-h", "--help"):
                show_help()
                exit(0)
            else:
                print("Invalid arguments! Please see help and try again")
                exit(0)

        if (event_log.endswith('.xes') or event_log.endswith('.XES')):
            log = utils.import_log_XES(event_log)

        elif (event_log.endswith('.csv') or event_log.endswith('.CSV')):
            log = utils.import_csv(event_log)

        else:
            print("Invalid file type! Please see help and try again")
            exit(0)

    except getopt.GetoptError as e:
        print("Invalid arguments! Please see help and try again")
        exit(0)
    except Exception as e:
        print("Exception!!!... -> " + str(e))
        exit(0)

    patterns = get_patterns(log)
    with open(event_log[:-4] + '_patterns.json', 'w', encoding='utf-8') as f:
        json.dump(patterns, f, ensure_ascii=False, indent=4)
    print('See ' + event_log[:-4] +
          '_patterns.json file for a list of found patterns')
