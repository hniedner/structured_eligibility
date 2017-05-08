from tinydb import TinyDB, Query

db = TinyDB('db/trials.json')
query = Query()


def save_update_trial(trial: dict) -> int:
    if 'nci_id' not in trial:
        raise AttributeError('The trial dictionary must contain an "nci_id"')
    trial_id = trial['nci_id']
    found_trials = db.search(query.nct_id == trial_id)

    if len(found_trials) < 1:
        eid = db.insert(trial)
    elif len(found_trials) > 1:
        raise RuntimeError('Duplicate record id - this should never happen')
    else:
        eid = found_trials[0].eid
        db.update(trial, eids=[eid])

    return eid


def get_all_records() -> list:
    return db.all()
