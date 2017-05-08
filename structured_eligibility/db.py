from tinydb import TinyDB, Query

db = TinyDB('db/trials.json')
trials_table = db.table('trials')
rules_table = db.table('rules')
mapping_table = db.table('mapping_id')
query = Query()


def _save_update_record(table: TinyDB.table, id_key: str, record: dict) -> int:
    if id_key not in record:
        raise AttributeError('The record dictionary must contain an "' + id_key + '" key!')
    found_records = table.search(query[id_key] == record[id_key])

    if len(found_records) < 1:
        eid = table.insert(record)
    elif len(found_records) > 1:
        raise RuntimeError('Duplicate record id - this should never happen!')
    else:
        eid = found_records[0].eid
        table.update(record, eids=[eid])

    return eid


def get_trial_by_nci_id(nci_id: str) -> dict:
    found_records = trials_table.search(query['nci_id'] == nci_id)
    if len(found_records) < 1:
        return None
    elif len(found_records) > 1:
        raise RuntimeError('Duplicate record id - this should never happen!')
    else:
        return found_records[0]


def get_trial_by_eid(eid: int) -> dict:
    if trials_table.contains(eid=eid):
        return trials_table.get(eid=eid)
    else:
        return None


def get_all_trials() -> list:
    return trials_table.all()


def save_update_trial(trial: dict) -> int:
    return _save_update_record(trials_table, 'nci_id', trial)


def get_rule_by_rule_id(rule_id: str) -> dict:
    found_records = trials_table.search(query['id'] == rule_id)
    if len(found_records) < 1:
        return None
    elif len(found_records) > 1:
        raise RuntimeError('Duplicate record id - this should never happen!')
    else:
        return found_records[0]


def get_all_rules() -> list:
    return rules_table.all()


def save_update_rule(rule: dict) -> int:
    return _save_update_record(trials_table, 'id', rule)


def get_trial_ids_for_rule_id(rule_id: str) -> list:
    found_records = mapping_table.search(query['rule_id'] == rule_id)
    if len(found_records) < 1:
        return []
    elif len(found_records) > 1:
        raise RuntimeError('Duplicate record id - this should never happen!')
    else:
        return found_records[0]['trial_ids']


def get_rule_ids_for_trial_id(nci_id: str):
    found_records = mapping_table.search(query['trial_ids'].any(nci_id))
    rule_ids = []
    for record in found_records:
        rule_ids.append(record['rule_id'])
    return rule_ids


def save_update_trials_by_rule_id_mapping(rule_id: str, trial_ids: list) -> int:
    return _save_update_record(mapping_table, 'rule_id', {'rule_id': rule_id, 'trial_ids': trial_ids})
