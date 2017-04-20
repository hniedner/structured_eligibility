from engine import RulesEditor, RuleSet

patient = {'age_in_years': 44,
           'biological_gender': 'MALE',
           'disease_nci_thesaurus_id': 'C23456',
           'ajcc_v7_stage': 'II',
           'hemoglobin_grams_per_deciliter': 10,
           'white_blood_cells_per_microliter': 2500}

max_age = RulesEditor.define_max_numeric_value('age_in_years', 50, 'The subject must not be older than 50 years!')
min_age = RulesEditor.define_min_numeric_value('age_in_years', 18, 'The subject must be at least 18 years old!')
gender = RulesEditor.define_value_contained_in_collection('biological_gender', ['MALE', 'FEMALE'],
                                                          'Both male and female subjects are eligible.')
rs1 = RuleSet({max_age, min_age, gender}, 'rs1')
rs1_conjunction = rs1.conjunction(
    'The subject must be at least 18 years old and not older than 50 years old. '
    'Both male and female subjects are eligible.',
    'Age Range and Gender constraints')
print(rs1_conjunction)

diseases = RulesEditor.define_value_contained_in_collection(
    'disease_nci_thesaurus_id', ['C12345', 'C23456', 'C76543'],
    'The subject must have diagnosis defined by one of the following NCI Thesaurus Concept Ids: '
    '"C12345", "C23456", "C76543"'
                                                            )
stages = RulesEditor.define_value_contained_in_collection(
    'ajcc_v7_stage', ['II', 'III'],
    'The subject have a disease stage of "II" or "III" as defined by AJCC v7!')

rs2 = RuleSet({diseases, stages}, 'rs2')
rs2_disjunction = rs2.disjunction(
    'The subject must have diagnosis befined by one of the following NCI Thesaurus Concept Ids: '
    '"C12345", "C23456", "C76543" or an AJCC v7 stage of "II" or "III"!', 'Diagnosis or Stage constraints')
print(rs2_disjunction)

hb = RulesEditor.define_min_numeric_value(
    'hemoglobin_grams_per_deciliter', 8,
    'The subject must have a hemoglobin of no less than 8 g/dl!')

wbc = RulesEditor.define_min_numeric_value(
    'white_blood_cells_per_microliter', 2000,
    'The subject must have a white blood cell count of no less than 2000 cells/ul!')

rs3 = RuleSet({hb, wbc}, 'rs3')
rs3_conjunction = rs3.conjunction(
    'The subject must have a hemoglobin of no less than 8 g/dl '
    'and a white blood cell count of no less than 2000 cells/ul!',
    'Lab Value constraints')
print(rs3_conjunction)

rsa = RuleSet({rs1_conjunction, rs2_disjunction, rs3_conjunction}, 'all rules')
rsa_conjunction = rsa.conjunction('Combined eligibility criteria.', 'Eligibility Criteria')
print(rsa_conjunction)

RulesEditor.write_rules_yaml(rsa_conjunction, 'bar.yaml')
RulesEditor.write_rules_json(rsa_conjunction, 'bar.json')

rule_yaml_recon = RulesEditor.read_rules_yaml('bar.yaml')
rule_json_recon = RulesEditor.read_rules_json('bar.json')

print(RulesEditor.evaluate(rsa_conjunction.definition, patient))
print(RulesEditor.evaluate(rule_yaml_recon.definition, patient))
print(RulesEditor.evaluate(rule_json_recon.definition, patient))

print(rsa_conjunction.definition)
print(rule_yaml_recon.definition)
print(rule_json_recon.definition)
