import rule_engine

ai_generated_image = rule_engine.Rule(
    'ais >= 0.5 and qs < 0.85'
)

modified_image = rule_engine.Rule(
    'ais < 0.1 and qs < 0.85'
)
outputs = [
{"message":"Image processed successfully","error":False,"data":{"status":"success","request":{"id":"req_hmuLMoqdu8nDYbDdX4Ymv","timestamp":1731511871.19806,"operations":6},"type":{"ai_generated":0.02},"quality":{"score":0.93},"media":{"id":"id1","uri":"media"}}},
{"message":"Image processed successfully","error":False,"data":{"status":"success","request":{"id":"req_hmuLMoqdu8nDYbDdX4Ymv","timestamp":1731511871.19806,"operations":6},"type":{"ai_generated":0.03},"quality":{"score":0.85},"media":{"id":"id2","uri":"media"}}},
{"message":"Image processed successfully","error":False,"data":{"status":"success","request":{"id":"req_hmuLMoqdu8nDYbDdX4Ymv","timestamp":1731511871.19806,"operations":6},"type":{"ai_generated":0.04},"quality":{"score":0.97},"media":{"id":"id3","uri":"media"}}},
{"message":"Image processed successfully","error":False,"data":{"status":"success","request":{"id":"req_hmuLMoqdu8nDYbDdX4Ymv","timestamp":1731511871.19806,"operations":6},"type":{"ai_generated":0.95},"quality":{"score":0.71},"media":{"id":"id4","uri":"media"}}},
{"message":"Image processed successfully","error":False,"data":{"status":"success","request":{"id":"req_hmuLMoqdu8nDYbDdX4Ymv","timestamp":1731511871.19806,"operations":6},"type":{"ai_generated":0.93},"quality":{"score":0.80},"media":{"id":"id5","uri":"media"}}},
{"message":"Image processed successfully","error":False,"data":{"status":"success","request":{"id":"req_hmuLMoqdu8nDYbDdX4Ymv","timestamp":1731511871.19806,"operations":6},"type":{"ai_generated":0.90},"quality":{"score":0.82},"media":{"id":"id6","uri":"media"}}},
{"message":"Image processed successfully","error":False,"data":{"status":"success","request":{"id":"req_hmuLMoqdu8nDYbDdX4Ymv","timestamp":1731511871.19806,"operations":6},"type":{"ai_generated":0.02},"quality":{"score":0.84},"media":{"id":"id7","uri":"media"}}},
{"message":"Image processed successfully","error":False,"data":{"status":"success","request":{"id":"req_hmuLMoqdu8nDYbDdX4Ymv","timestamp":1731511871.19806,"operations":6},"type":{"ai_generated":0.02},"quality":{"score":0.85},"media":{"id":"id8","uri":"media"}}},
]

for output in outputs:
    print('{id}: ai_score: {ais} quality_score: {qs}'.format(
        id=output.get('data').get('media').get('id'),
        ais=output.get('data').get('type').get('ai_generated'),
        qs=output.get('data').get('quality').get('score')))

    scoring_data = {
        "id": output.get('data').get('media').get('id'),
        "ais": output.get('data').get('type').get('ai_generated'),
        "qs": output.get('data').get('quality').get('score')
    }

    if ai_generated_image.matches(scoring_data):
        print('{id} - AI generated image: score 1.0'.format(id=scoring_data.get('id')))
    elif modified_image.matches(scoring_data):
        print('{id} - Modified image: score 0.5'.format(id=scoring_data.get('id')))
    else:
        print('{id} - Good image: score 0.0'.format(id=scoring_data.get('id')))

