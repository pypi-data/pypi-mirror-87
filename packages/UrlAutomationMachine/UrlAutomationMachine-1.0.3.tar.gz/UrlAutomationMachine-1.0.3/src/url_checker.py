"""The main module that runs the program to check whether a URL is broken or not """
import threading
import sys
import argparse

try:
    from src import url_class
except ModuleNotFoundError:
    import url_class


def check_url(file_input, is_json=False):
    """Creates a machine object to process a single URL"""
    if is_json:
        url_machine = url_class.urlAutomationMachine(file_input, is_json)
        url_machine.processUrl()
    else:
        url_machine = url_class.urlAutomationMachine(file_input)
        url_machine.processUrl()


def check_file(file_input, is_json=False, ignore=None):
    """Creates a machine object to process a file of URLs"""
    if is_json:
        url_machine = url_class.urlAutomationMachine(file_input, is_json, ignore)
        url_machine.processFile()
    else:
        url_machine = url_class.urlAutomationMachine(file_input, False, ignore)
        url_machine.processFile()


def check_telescope(file_input=None, is_json=False):
    """Creates a machine object to process the 10 latest telescope posts"""
    if is_json:
        url_machine = url_class.urlAutomationMachine(file_input, is_json)
        url_machine.processTelescope()
    else:
        url_machine = url_class.urlAutomationMachine(file_input)
        url_machine.processTelescope()


def main():
    """Main function creates a thread based on argument passed to main program"""
    arguments = setupArgs()
    if arguments.f:
        try:
            threading.Thread(
                target=check_file(arguments.f, arguments.j, arguments.i)
            ).start()
        except ValueError as error_exception:
            sys.stderr.write(str(error_exception))
            sys.exit(1)
        sys.exit(0)
    elif arguments.u:
        try:
            threading.Thread(target=check_url(arguments.u, arguments.j)).start()
        except ValueError as error_exception:
            sys.stderr.write(str(error_exception))
            sys.exit(1)
        sys.exit(0)
    elif arguments.t:
        try:
            threading.Thread(target=check_telescope(arguments.t, arguments.j)).start()
        except ValueError as error_exception:
            sys.stderr.write(str(error_exception))
            sys.exit(1)
        sys.exit(0)
    else:
        print(
            """This program has two arguments, one for inputting the file,
        the second one displays the current version of the program"""
        )
        print("Usage: urlChecker [-f] inputFile: The input file to be processed")
        print("Usage: urlChecker [-u] inputUrl: Checks URL to see if it works or not")
        print("Usage: urlChecker [-j]: Displays result in JSON format")
        print("Usage: urlChecker [-i]: Ignores the URL that's passed as an argument")
        print(
            "Usage: urlChecker [-t]: Checks the urls of the 10 latest telescope posts"
        )


def setupArgs():
    parse = argparse.ArgumentParser(
        description="Checks the file input for any broken HTML urls"
    )
    parse.add_argument("-f", help="The input file to check")
    parse.add_argument("-u", help="The URL to check")
    parse.add_argument("-j", action="store_true", help="Displays output in JSON format")
    parse.add_argument("-i", help="Ignores any url that matches the argument")
    parse.add_argument(
        "-t",
        action="store_true",
        help="Will check the 10 latest posts to telescope",
    )
    args = parse.parse_args()

    return args


if __name__ == "__main__":
    main()
