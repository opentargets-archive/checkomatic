from __future__ import absolute_import, print_function
import sys
import yaml
import addict
import functional as fn
from docopt import docopt

from checkomatic.helpers import make_client, uri_open_and_read
import checkomatic.evaluators as evaluators

ARGS = """OpenTargets Check-O-Matic.

Usage:
  checkomatic eval --file=<filename.yml>
  checkomatic (-h | --help)
  checkomatic --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --file=<filename.yml>  config filename.

"""


def main(filename):
    arguments = docopt(ARGS, version='OT Check-O-Matic v0.0.1')
    print(arguments)

    if arguments['eval']:
        conf_content = uri_open_and_read(arguments['--file'])
        c = addict.Dict(yaml.safe_load(conf_content))

        ot_client = make_client(c.checkomatic.client.host, c.checkomatic.client.port)

        _g = globals()
        _g['c'] = ot_client

        results = []
        if c.checkomatic.rules.targets:
            results += evaluators.eval_targets(ot_client, c.checkomatic.rules.targets.to_dict(), _g)
        if c.checkomatic.rules.diseases:
            results += evaluators.eval_diseases(ot_client, c.checkomatic.rules.diseases.to_dict(), _g)
        if c.checkomatic.rules.stats:
            results += evaluators.eval_stats(ot_client, c.checkomatic.rules.stats, _g)

        oks = fn.seq(results).filter(lambda e: e == True).count_by_value()
        fails = fn.seq(results).filter(lambda e: e == False).count_by_value()
        print("oks", oks, "fails", fails)

        if fails > 0 or oks == 0:
            return 1
        else:
            return 0


if __name__ == '__main__':
    sys.exit(main(filename="platform.yml"))
