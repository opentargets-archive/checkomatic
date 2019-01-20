from __future__ import absolute_import, print_function
import sys
import yaml
import addict
import functional as fn
import jsonpath_rw as jp
from docopt import docopt

from opentargets_checkomatic.helpers import make_client, uri_open_and_read
from opentargets_checkomatic.helpers import to_vlist, to_vset
import opentargets_checkomatic.evaluators as evaluators

ARGS = """OpenTargets Check-O-Matic.

Usage:
  checkomatic --file=<filename.yml> eval
  checkomatic --file=<filename.yml> eval rule <rule-name>
  checkomatic (-h | --help)
  checkomatic --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  -f --file=<filename.yml>  config filename.

"""


def main():
    arguments = docopt(ARGS, version='OT Check-O-Matic v0.0.1')

    if arguments['eval']:
        conf_content = uri_open_and_read(arguments['--file'])
        c = addict.Dict(yaml.safe_load(conf_content))
        ot_client = make_client(c.checkomatic.client.host, c.checkomatic.client.port)

        _g = globals()
        _g['c'] = ot_client

        results = []

        p = jp.parse('asdf')
        p.find

        # remove all rules except <rule-name>
        if arguments['rule']:
            rule_name = arguments['<rule-name>']
            rules = c.checkomatic.rules.keys()
            rules_to_remove = list(set(rules) - set([rule_name]))
            for r in rules_to_remove:
                c.checkomatic.rules.pop(r, None)

        if c.checkomatic.rules.targets:
            results += evaluators.eval_targets(ot_client, c.checkomatic.rules.targets.to_dict(), _g)

        if c.checkomatic.rules.diseases:
            results += evaluators.eval_diseases(ot_client, c.checkomatic.rules.diseases.to_dict(), _g)

        if c.checkomatic.rules.stats:
            results += evaluators.eval_stats(ot_client, c.checkomatic.rules.stats, _g)

        if c.checkomatic.rules.associations.targets:
            results += evaluators.eval_associations(ot_client,
                                                    'target',
                                                    c.checkomatic.rules.associations.targets.to_dict(),
                                                    _g)

        if c.checkomatic.rules.associations.diseases:
            results += evaluators.eval_associations(ot_client,
                                                    'disease',
                                                    c.checkomatic.rules.associations.diseases.to_dict(),
                                                    _g)

        if c.checkomatic.rules.evidences:
            results += evaluators.eval_evidences(ot_client,
                                                 c.checkomatic.rules.evidences.to_dict(),
                                                 _g,
                                                 c.checkomatic.client.size)

        if c.checkomatic.rules.searches.targets:
            results += evaluators.eval_searches(ot_client,
                                                'target',
                                                c.checkomatic.rules.searches.targets.to_dict(),
                                                _g,
                                                c.checkomatic.client.size)

        if c.checkomatic.rules.searches.diseases:
            results += evaluators.eval_searches(ot_client,
                                                'disease',
                                                c.checkomatic.rules.searches.diseases.to_dict(),
                                                _g,
                                                c.checkomatic.client.size)

        oks = fn.seq(results).filter(lambda e: e == True).count_by_value()
        fails = fn.seq(results).filter(lambda e: e == False).count_by_value()
        print("oks", oks, "fails", fails)

        if fails > 0 or oks == 0:
            return 1
        else:
            return 0


def cli():
    sys.exit(main())


if __name__ == '__main__':
    cli()
