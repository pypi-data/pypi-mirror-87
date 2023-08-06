from pmabstraction import utils, discover, transformation as trans
from pmabstraction.abstraction_support_functions import *
import traceback


def display_user_patterns(patterns):
    print()
    print('*'*50 + 'USER PATTERNS' + '*'*50)
    print('_'*100)
    print('\tID\t | \tName\t | \tPattern\t')
    print('_'*100)

    result = ""
    for data in patterns:
        result = ('\t' + str(data["ID"]) + '\t | ' +
                  '\t' + data["Name"] + '\t | ' + '\t' + str(data["Pattern"]))
        print(result)
    print('_'*100)

if __name__ == '__main__':
    '''
    Desc: To get sets of tandem arrays and maximal
    repeat from their respective modules e.g. discover_ta.py,
    discover_m.py and utils
    Used: main.py --path text.xes --pattern 1 2 3
    [--downloadLog] [--downloadModel]
    Input: Recieve command line arguments
    Output: Display tandem arrays and maximal repeat sets
    '''
    event_log = ''
    export_log = False
    export_model = False
    pattern_path = ''
    pattern_number = ''
    log = None
    user_patterns = ''
    log_ = None

    try:
        parser = argparse.ArgumentParser(
            description='''To transform the logs with the pattern.
                        The --path argument is mandatory.'''
            )

        # definition of --path argument
        parser.add_argument(
            '--path',
            required=True,
            type=argparse.FileType('r'),
            metavar='xes_file_name',
            help='specify the path of xes file. e.g. test.xes'
            )

        # definition of --userPattern argument
        parser.add_argument(
            '--userPattern',
            required=False,
            type=argparse.FileType('r'),
            metavar='user_pattern_file_name',
            help='specify the user pattern path file in json format.'
            )

        # definition of --downloadLog argument
        parser.add_argument(
            '--downloadLog',
            action='store_true',
            help='flag to export/download transformed log'
            )

        # definition of --downloadModel argument
        parser.add_argument(
            '--downloadModel',
            action='store_true',
            help='flag to export/download process model'
            )

        parser.add_argument(
            '-filename',
            type=check_if_xes,
            default=parser.parse_args().path.name,
            metavar='filename',
            help=argparse.SUPPRESS
            )

        # getting the arguments by parse_args
        args = parser.parse_args()
        event_log = args.path.name
        export_log = args.downloadLog
        export_model = args.downloadModel
        if (args.userPattern is not None):
            pattern_path = args.userPattern.name

        filename_prefix = event_log.split('.')[0]
        if (event_log.endswith('.xes') or event_log.endswith('.XES')):
            log = utils.import_log_XES(event_log)
        elif (event_log.endswith('.csv') or event_log.endswith('.CSV')):
            log = utils.import_csv(event_log)
            if log is None:
                raise Exception("log file not set")
        else:
            print("Invalid file type! Please see help and try again")
            exit(0)

        # checking user patterns
        if (pattern_path != ''):
            user_patterns = utils.import_pattern_json(pattern_path)
            if (user_patterns is None):
                print("The user pattern file does not" +
                      " exists or it contains no data")
                exit(0)
            display_user_patterns(user_patterns)

            pattern_dic = read_pattern_file(pattern_path)

            # Extract all ids from user patterns
            ids_user_patterns = [x['ID'] for x in user_patterns]

            # read the activities and timestamps from the given log
            concatenated_traces, concatenated_timestamps = read_log(log)

            # perform pmabstraction on user patterns
            abstracted_traces, abstracted_timestamps = \
                perform_abstractions(
                                ids_user_patterns, user_patterns,
                                concatenated_traces,
                                concatenated_timestamps
                                )

            # get transformed log with artificial case ids to apply filter
            log_content = trans.generate_transformed_log_XES(
                                                event_log,
                                                abstracted_traces,
                                                abstracted_timestamps,
                                                event_log[:-4] + "_header.XES"
                                                )

            # very ugly code to deal with meta data loss of pm4py filters
            user_abstracted = utils.import_log_XES(event_log[:-4] +
                                                   "_header.XES")
            log = user_abstracted
            # there is no meta data in clean because
            # pm4py filters loose that information
            utils.export_log(utils.clean_lifecycle_events(log),
                             event_log[:-4] + "_clean.XES")

            with open(event_log[:-4] + "_header.XES") as headerFile:
                header = []
                for line in headerFile:
                    header.append(line)
                    if ("<trace>" in line):
                        break

            with open(event_log[:-4] + "_clean.XES") as cleanFile:
                content_clean = cleanFile.readlines()

            with open(event_log[:-4] + "_transformed.XES", 'w') as f:
                for line in header:
                    f.write(line)
                for line in content_clean[3:]:
                    f.write(line)

            log = utils.import_log_XES(event_log[:-4] + "_transformed.XES")

            if (os.path.exists(event_log[:-4] + "_header.XES")):
                os.remove(event_log[:-4] + "_header.XES")
            if (os.path.exists(event_log[:-4] + "_clean.XES")):
                os.remove(event_log[:-4] + "_clean.XES")

        # Discover TA and MR sets
        patterns = discover.get_patterns(log)
        with open(event_log[:-4] + '_patterns.json',
                  'w', encoding='utf-8') as f:
            json.dump(patterns, f, ensure_ascii=False, indent=4)
        print('Please see ' + event_log[:-4] +
              '_patterns.json file for a list of found patterns')

        # input pattern sequences in order
        print("Please enter pattern numbers in order e.g. " +
              "1 2 3 1 (Required field): ", end=""),
        input_pattern_seq = input()
        pattern_number = input_pattern_seq.split(' ')

        ids = [x['ID'] for x in patterns]

        for n in pattern_number:
            try:
                if n == '' and len(pattern_number) == 1:
                    continue
                if not int(n) in ids:
                    raise ValueError
            except ValueError as verr:
                print('Please only enter only valid IDs')
                exit(0)

        if (input_pattern_seq != ''):
            print("Info: Performing pmabstraction steps " +
                  "based (TA/MR sets) patterns...")
            # perform pmabstraction and transformation
            if (pattern_path != ''):
                file = event_log[:-4] + "_transformed.XES"
            else:
                file = event_log
            trans.perform_transformation(file,
                                         export_log,
                                         export_model,
                                         pattern_number)
        else:
            print("No patterns selected to abstract!")

            if export_log:
                # bring log into right output format
                if pattern_path != '':
                    log = user_abstracted
                log_content = trans.transform_log(log)
                with open(event_log[:-4] +
                          "_transformed_exported.XES", 'w') as f:
                    f.write(log_content)
                print('The log has been exported')

            dfg = utils.generate_process_model(log)
            print("Process model is generated for " +
                  "transformed log (Popping up)")

            if export_model:
                utils.export_process_model(dfg, log, event_log[:-4] +
                                           "_transformed_exported.svg")

        if (os.path.exists(event_log[:-4] + "_transformed.XES")):
            os.remove(event_log[:-4] + "_transformed.XES")

    except Exception as e:
        print("Exception!!!... -> " + str(e))
        print(traceback.format_exc())
        exit(0)
