import addict
import itertools as iters
import functional as fn

from opentargets_checkomatic.helpers import failed_at, make_local_env


def eval_section(assertion_list, global_dict, local_env):
    def _eval_elem(elem, global_scope, local_scope):
        if '\n' in elem:
            exec(elem, global_scope, local_scope)
            r = local_scope['output']
            if not r:
                failed_at(elem)
            return r
        else:
            r = eval(elem, global_scope, local_scope)
            if not r:
                failed_at(elem)
            return r

    return list(iters.imap(lambda e: _eval_elem(e, global_dict, local_env),
                           assertion_list if assertion_list is not None else []))


def eval_stats(ot_client, assertion_list, global_env):
    data = ot_client.get_stats()
    if data.total > 0:
        local_env = make_local_env(input=None, output=False)
        stats_o = addict.Dict(fn.seq(data.to_object()).take(1).head())
        local_env['o'] = stats_o
        asserted = eval_section(assertion_list, global_env, local_env)
        return asserted
    else:
        return []


def eval_targets(ot_client, section_dict, global_env):
    asserted = []
    for ((k, v), i) in fn.seq(section_dict.items()).zip_with_index(start=1).to_list():
        data = ot_client.search(k, size=1, filter="target")
        if data.total > 0:
            local_env = make_local_env(input=None, output=False)
            target_o = addict.Dict(fn.seq(data.to_object()).take(1).head().data)
            local_env['o'] = target_o
            asserted_k = eval_section(v, global_env, local_env)
            asserted += asserted_k
        else:
            asserted += [False]

    return asserted


def eval_diseases(ot_client, section_dict, global_env):
    asserted = []
    for ((k, v), i) in fn.seq(section_dict.items()).zip_with_index(start=1).to_list():
        data = ot_client.search(k, size=1, filter="disease")
        if data.total > 0:
            local_env = make_local_env(input=None, output=False)
            disease_o = addict.Dict(fn.seq(data.to_object()).take(1).head().data)
            local_env['o'] = disease_o
            asserted_k = eval_section(v, global_env, local_env)
            asserted += asserted_k
        else:
            asserted += [False]

    return asserted


def eval_associations(ot_client, by_type, section_dict, global_env):
    asserted = []
    for ((k, v), i) in fn.seq(section_dict.items()).zip_with_index(start=1).to_list():
        if by_type == 'target':
            data = ot_client.get_associations_for_target(k)
        else:
            data = ot_client.get_associations_for_disease(k)

        if data.total > 0:
            local_env = make_local_env(input=None, output=False)
            data_t = data.to_dataframe()
            local_env['t'] = data_t
            asserted_k = eval_section(v, global_env, local_env)
            asserted += asserted_k
        else:
            asserted += [False]

    return asserted