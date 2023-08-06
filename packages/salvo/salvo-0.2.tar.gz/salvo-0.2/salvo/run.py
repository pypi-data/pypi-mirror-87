import argparse
import logging
import sys

from salvo import __version__
from salvo.output import RunResults
from salvo.util import get_server_info, print_server_info


logger = logging.getLogger("break")
_VERBS = ("GET", "POST", "DELETE", "PUT", "HEAD", "OPTIONS")
_DATA_VERBS = ("POST", "PUT")
_H = "--------"


def load(url, args, stream=sys.stdout):
    server_info = get_server_info(url, args.method, headers=args.headers)

    if not args.quiet:
        print_server_info(server_info, stream)
        if args.duration is None:
            print(
                _H + f" Running {args.requests} queries - concurrency "
                f"{args.concurrency} " + _H
            )
        else:
            print(
                _H + f" Running for ~{args.duration} seconds - concurrency "
                f"{args.concurrency} " + _H
            )

        print("")

    if args.duration is not None:
        num = None
    else:
        num = args.concurrency * args.requests

    res = RunResults(server_info, num=num, duration=args.duration, quiet=args.quiet)

    from salvo.scenario import run_test

    try:
        molotov_res = run_test(url, res, args)
    except SystemExit as e:
        raise Exception(f"Molotov exit {e.code}")
    finally:
        if not args.quiet:
            print("")

    return res, molotov_res


def main():
    parser = argparse.ArgumentParser(
        description="Simple HTTP Load runner based on Molotov."
    )

    parser.add_argument(
        "--version",
        action="store_true",
        default=False,
        help="Displays version and exits.",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help=(
            "Verbosity level. -v will display "
            "tracebacks. -vv requests and responses."
        ),
    )

    parser.add_argument(
        "-m", "--method", help="HTTP Method", type=str, default="GET", choices=_VERBS
    )

    parser.add_argument(
        "--content-type", help="Content-Type", type=str, default="text/plain"
    )

    parser.add_argument(
        "-D",
        "--data",
        help=('Data. Prefixed by "py:" to point ' "a python callable."),
        type=str,
        default=None,
    )

    parser.add_argument("-c", "--concurrency", help="Concurrency", type=int, default=1)

    parser.add_argument(
        "-a",
        "--auth",
        help="Basic authentication user:password",
        type=str,
        default=None,
    )

    parser.add_argument(
        "--header", help="Custom header. name:value", type=str, action="append"
    )

    parser.add_argument(
        "--pre-hook",
        help=(
            "Python module path (eg: mymodule.pre_hook) "
            "to a callable which will be executed before "
            "doing a request for example: "
            "pre_hook(method, url, options). "
            "It must return a tuple of parameters given in "
            "function definition"
        ),
        type=str,
        default=None,
    )

    parser.add_argument(
        "--post-hook",
        help=(
            "Python module path (eg: mymodule.post_hook) "
            "to a callable which will be executed after "
            "a request is done for example: "
            "eg. post_hook(response). "
            "It must return a given response parameter or "
            "call `salvo.util.raise_response_error` for "
            "a failed request."
        ),
        type=str,
        default=None,
    )

    parser.add_argument(
        "--json-output",
        help="Prints the results in JSON instead of the default format",
        action="store_true",
        default=False,
    )

    parser.add_argument(
        "-q",
        "--quiet",
        help="Don't display the progress bar",
        action="store_true",
        default=False,
    )

    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        "-n", "--requests", help="Number of requests", type=int, default=1
    )

    group.add_argument(
        "-d", "--duration", help="Duration in seconds", type=int, default=None
    )

    parser.add_argument("url", help="URL to hit", nargs="?")
    args = parser.parse_args()

    if args.version:
        print(__version__)
        sys.exit(0)

    if args.url is None:
        print("You need to provide an URL.")
        parser.print_usage()
        sys.exit(1)

    if args.data is not None and args.method not in _DATA_VERBS:
        print("You can't provide data with %r" % args.method)
        parser.print_usage()
        sys.exit(1)

    if args.quiet and args.verbose > 0:
        print("You can't use --quiet and --verbose at the same time")
        parser.print_usage()
        sys.exit(1)

    def _split(header):
        header = header.split(":")

        if len(header) != 2:
            print("A header must be of the form name:value")
            parser.print_usage()
            sys.exit(1)

        return header

    if args.header is None:
        headers = {}
    else:
        headers = dict([_split(header) for header in args.header])

    args.headers = headers

    res, molotov_res = load(args.url, args)
    if molotov_res["SETUP_FAILED"] > 0 or molotov_res["SESSION_SETUP_FAILED"] > 0:
        sys.exit(1)

    if not args.json_output:
        if len(res.errors) > 0:
            print("")
            print("-------- Errors --------")
            print("")
            for code, desc in res.errors_desc.items():
                print("%s (%d occurences)" % (desc, res.errors[code]))
        res.print_stats()
        print("Want to build a more powerful load test ? Try Molotov !")
        print("Bye!")
    else:
        res.print_json()

    return res, molotov_res


def console_main():
    main()
    return 0


if __name__ == "__main__":
    main()
