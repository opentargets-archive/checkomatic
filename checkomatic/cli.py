from __future__ import absolute_import, print_function
import sys
import opentargets as ot
import yaml
import addict
import itertools as iters
import functional as fn


def make_client(host, port):
    return ot.OpenTargetsClient(host=host, port=port)


def make_local_env(*args, **kwargs):
    return addict.Dict(*args, **kwargs).to_dict()


def eval_section(assertion_list, global_dict, local_env):
    def _eval_elem(elem, global_scope, local_scope):
        if '\n' in elem:
            exec(elem, global_scope, local_scope)
            return local_scope['output']
        else:
            return eval(elem, global_scope, local_scope)

    return list(iters.imap(lambda e: _eval_elem(e, global_dict, local_env), assertion_list))


def eval_stats(ot_client, assertion_list, global_env):
    data = ot_client.get_stats()
    print(data)
    if data.total > 0:
        local_env = make_local_env(input=None, output=False)
        stats_o = addict.Dict(fn.seq(data.to_object()).take(1).head())
        local_env['o'] = stats_o
        asserted = eval_section(assertion_list, global_env, local_env)
        print("eval stats asserted", str(asserted))
        return asserted
    else:
        print("eval stats asserted", None)
        return []


def eval_targets(ot_client, section_dict, global_env):
    for i, (k, v) in enumerate(section_dict.items(), start=1):
        data = ot_client.search(k, size=1)
        if data.total > 0:
            local_env = make_local_env(input=None, output=False)
            target_o = addict.Dict(fn.seq(data.to_object()).take(1).head().data)
            local_env['o'] = target_o
            asserted = eval_section(v, global_env, local_env)
            print("eval target", i, k, "asserted", str(asserted))
            return asserted
        else:
            print("eval target", i, k, "asserted", None)
            return []


def main(filename):
    with open(filename) as f:
        c = addict.Dict(yaml.safe_load(f.read()))
        ot_client = make_client(c.checkomatic.client.host, c.checkomatic.client.port)
        _g = globals()
        _g['c'] = ot_client

        results = []
        if c.checkomatic.rules.targets:
            results += eval_targets(ot_client, c.checkomatic.rules.targets.to_dict(), _g)
        if c.checkomatic.rules.stats:
            results += eval_stats(ot_client, c.checkomatic.rules.stats, _g)

        oks = fn.seq(results).filter(lambda e: e == True).count_by_value()
        fails = fn.seq(results).filter(lambda e: e == False).count_by_value()
        print("result", results, "fails", fails, "oks", oks)

        if fails > 0 or oks == 0:
            raise RuntimeError("oks %s fails %s" % (oks, fails))
        return 0


if __name__ == '__main__':
    sys.exit(main(filename="platform.yml"))
