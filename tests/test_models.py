import unittest
import json
import models


class TestModelInterchangeFormats(unittest.TestCase):

    def test_decode_json_to_model(self):
        expected_value = 42
        json_string = '{"_id": ' + str(expected_value) + '}'
        json_dict = json.loads(json_string)
        model = models.create_match(json_dict)
        self.assertEqual(expected_value, model['_id'])

    def test_encode_model_to_json(self):
        model = models.create_match()
        model['_id'] = 42
        json_string = json.dumps(model)
        self.assertIn('"_id": 42', json_string)

    def test_encode_nested_models(self):
        model = models.create_card(_id=1, name='Vanilla 1', cost=models.create_resources(a=1), attack=1, defense=1, tapped=False)
        json_string = json.dumps(model)
        self.assertIn('"cost": {', json_string)


class TestResource(unittest.TestCase):

    def test_can_empty_a_resource(self):
        resource = models.create_resources(a=10)
        models.empty_resources(resource)
        self.assertEqual(resource['a'], 0)

    def test_enough_resources_to_pay_cost(self):
        resource = models.create_resources()
        cost = models.create_resources()
        self.assertFalse(models.not_enough_resources(resource, cost))
        for resource_type in cost:
            cost[resource_type] += 1
        self.assertTrue(models.not_enough_resources(resource, cost))

    def test_consume_another_resource_decreases_amount_of_resources(self):
        resource = models.create_resources(a=10)
        cost = models.create_resources(a=3)
        models.consume(resource, cost)
        self.assertEqual(resource['a'], 7)

