from engine import RulesEditor, RuleSet

patient = {'age': 44, 'gender': 'MALE', 'disease': 'bar', 'stage': 'II', 'grade': 2, 'lab': 2500}

max_age = RulesEditor.define_max_numeric_value('age', 50)
min_age = RulesEditor.define_min_numeric_value('age', 18)
gender = RulesEditor.define_value_contained_in_collection('gender', ['MALE', 'FEMALE'])
rs1 = RuleSet({max_age, min_age, gender}, 'rs1')
print(rs1.conjunction())

diseases = RulesEditor.define_value_contained_in_collection('disease', ['foo', 'bar', 'foobar'])
stages = RulesEditor.define_value_contained_in_collection('stage', ['I', 'II', 'III'])
rs2 = RuleSet({diseases, stages}, 'rs2')
print(rs2.disjunction())

grade = RulesEditor.define_value_contained_in_collection('grade', [1, 2, 3])
labv = RulesEditor.define_min_numeric_value('lab', 2000)
rs3 = RuleSet({grade, labv}, 'rs3')
print(rs3.conjunction())

rsa = RuleSet({rs1.conjunction(), rs2.disjunction(), rs3.conjunction()}, 'all rules')
print(rsa.conjunction())

RulesEditor.write_rules_yaml(rsa.conjunction(), 'bar.yaml')
RulesEditor.write_rules_json(rsa.conjunction(), 'bar.json')

rule_orig = rsa.conjunction()
rule_yaml_recon = RulesEditor.read_rules_yaml('bar.yaml')
rule_json_recon = RulesEditor.read_rules_json('bar.json')

print(RulesEditor.evaluate(rule_orig.definition, patient))
print(RulesEditor.evaluate(rule_yaml_recon.definition, patient))
print(RulesEditor.evaluate(rule_json_recon.definition, patient))

print(rule_orig.definition)
print(rule_yaml_recon.definition)
print(rule_json_recon.definition)
