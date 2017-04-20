import json
import uuid

import ruamel.yaml
from json_logic import jsonLogic


class Rule:
    """ Encapsulate a rule or criterion """

    def __init__(self, definition: dict, description: str, name: str, uid: str = None):
        self._definition = definition
        self._description = description
        self._name = name
        self._id = uuid.uuid4().hex if uid is None else uid

    @property
    def id(self) -> str:
        return self._id

    @property
    def definition(self) -> dict:
        return self._definition

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    def __repr__(self):
        return {**self._definition, **{"id": self._id, "label": self._name, "description": self._description}}

    def __str__(self):
        return 'Rule (' + self._id + ') ' + self._name + ' -> definition: ' + json.dumps(
            self._definition) + '\n' + self._description


class RuleSet:
    """ Encapsulate a set of rules and emit them as conjunction of disjunction"""

    def __init__(self, rulez: set, name: str):
        self._disjunction_id = None
        self._conjunction_id = None
        self._rules = {}
        for rule in rulez:
            self._rules[rule.id] = rule
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @property
    def definitions(self) -> list:
        definitions = []
        for rule_id in self._rules:
            definitions.append(self._rules[rule_id].__repr__())
        return definitions

    def conjunction(self, rule_description: str, rule_name: str = None) -> Rule:
        if rule_name is None:
            rule_name = self.name
        if self._disjunction_id is None:
            rule = Rule({"and": self.definitions}, rule_description, rule_name)
            self._disjunction_id = rule.id
        else:
            rule = Rule({"and": self.definitions}, rule_description, rule_name, self._disjunction_id)
        return rule

    def disjunction(self, rule_description: str, rule_name: str = None) -> Rule:
        if rule_name is None:
            rule_name = self.name
        if self._disjunction_id is None:
            rule = Rule({"or": self.definitions}, rule_description, rule_name)
            self._disjunction_id = rule.id
        else:
            rule = Rule({"or": self.definitions}, rule_description, rule_name, self._disjunction_id)
        return rule

    def add_rule(self, rule: Rule):
        self._rules[rule.id] = rule

    def remove_rule(self, rule_id: str) -> bool:
        return self._rules.pop(rule_id, None) is not None

    def __repr__(self):
        return {
            "label": self._name,
            "rules": self._rules
        }

    def __str__(self):
        strval = ['Ruleset (' + self._name + ') -> rules: ']
        for rule_id in self._rules:
            strval.append('\t' + str(self._rules[rule_id]))
        return '\n'.join(strval)


class RulesEditor:
    """ Authoring tool for inclusion or exclusion criteria in the form of logic rules """

    @staticmethod
    def define_min_numeric_value(var_name: str, numeric_value: [int, float], description: str, name: str = None,
                                 typematch_required: bool = False) -> Rule:
        if not name:
            predicate = '>==' if typematch_required else '>='
            name = ' '.join([var_name, predicate, str(numeric_value)])
        return Rule({predicate: [{'var': var_name}, numeric_value]}, description, name)

    @staticmethod
    def define_max_numeric_value(var_name: str, numeric_value: [int, float], description: str, name: str = None,
                                 typematch_required: bool = False) -> Rule:
        if not name:
            predicate = '<==' if typematch_required else '<='
            name = ' '.join([var_name, predicate, str(numeric_value)])
        return Rule({predicate: [{'var': var_name}, numeric_value]}, description, name)

    @staticmethod
    def define_value_exact_match(var_name: str, value, description: str, name: str = None,
                                 typematch_required: bool = False) -> Rule:
        if not name:
            predicate = '===' if typematch_required else '=='
            name = ' '.join([var_name, predicate, str(value)])
            return Rule({predicate: [{'var': var_name}, value]}, description, name)

    @staticmethod
    def define_value_contained_in_collection(var_name: str, collection: list, description: str,
                                             name: str = None) -> Rule:
        if not name:
            name = var_name + ' in [' + ' ,'.join("'{0}'".format(n) for n in collection) + ']'
            return Rule({'in': [{'var': var_name}, collection]}, description, name)

    @staticmethod
    def read_rules_json(filename: str):
        fp = open(filename, 'r', encoding='utf-8')
        rulez = json.load(fp)
        rule_id = rulez.pop('id')
        label = rulez.pop('label')
        rule = Rule(rulez, label, rule_id)
        fp.close()
        return rule

    @staticmethod
    def read_rules_yaml(filename):
        fp = open(filename, 'r', encoding='utf-8')
        rulez = ruamel.yaml.safe_load(fp.read())
        rule_id = rulez.pop('id')
        label = rulez.pop('label')
        rule = Rule(rulez, label, rule_id)
        fp.close()
        return rule

    @staticmethod
    def write_rules_json(rule: Rule, filename: str):
        fp = open(filename, 'w', encoding='utf-8')
        json.dump(rule.__repr__(), fp, indent=2)
        fp.close()

    @staticmethod
    def write_rules_yaml(rule: Rule, filename: str):
        fp = open(filename, 'w', encoding='utf-8')
        ruamel.yaml.round_trip_dump(rule.__repr__(), fp)
        fp.close()

    @staticmethod
    def evaluate(rules, subject):
        return jsonLogic(rules, subject)
