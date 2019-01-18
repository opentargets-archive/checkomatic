from __future__ import absolute_import, print_function
import sys
import opentargets as ot
import yaml
import addict


def main():
    m_local = {'input': 'asdf', 'output': None}
    c = addict.Dict(yaml.safe_load(open("rules.yml").read()))
    exec(c.rules[0].code, globals(), m_local)
    print(str(m_local))
    print(c.to_dict())


if __name__ == '__main__':
    sys.exit(main())
