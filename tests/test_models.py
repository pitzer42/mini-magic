import unittest
import json

from models import Card, Resources, Player, Match, flatten, expand

@unittest.skip
class TestModelInterchangeFormats(unittest.TestCase):

    def test_decode_json_to_model(self):
        expected_value = 42
        json_string = '{"_id": ' + str(expected_value) + '}'
        json_dict = json.loads(json_string)
        model = expand(Match, json_dict)
        self.assertEqual(expected_value, model._id)

    def test_encode_model_to_json(self):
        model = Match()
        model._id = 42
        flat_dict = flatten(model)
        json_string = json.dumps(flat_dict)
        self.assertIn('"_id": 42', json_string)

    def test_model_ignores_attributes_from_dict_that_are_not_defined_in_class(self):
        attribute_name = 'undefined_attribute'
        json_string = '{"' + attribute_name + '": 42}'
        json_dict = json.loads(json_string)
        model = expand(Match, json_dict)
        self.assertFalse(hasattr(model, attribute_name))

    def test_decode_nested_models(self):
        json_string = '{"_id": 1, "attack": 1, "defense": 1, "name": "Vanilla 1", "tapped": false, ' \
                      '"cost": {"b": 0, "a": 1}}'
        json_dict = json.loads(json_string)
        card = expand(Card, json_dict)
        self.assertEqual(card.cost.a, 1)

    def test_encode_nested_models(self):
        model = Card(_id=1, name='Vanilla 1', cost=Resources(a=1), attack=1, defense=1, tapped=False)
        flat_dict = flatten(model)
        json_string = json.dumps(flat_dict)
        self.assertIn('"cost": {', json_string)

    def test_encode_object_id(self):
        self.fail()

    def test_decode_object_id(self):
        self.fail()

@unittest.skip
class TestResource(unittest.TestCase):

    def test_can_empty_a_resource(self):
        resource = Resources()
        resource.a = 10
        resource.empty()
        self.assertEqual(resource.a, 0)

    def test_enough_resources_to_pay_cost(self):
        resource = Resources()
        cost = Resources()
        self.assertTrue(resource.enough(cost))
        for resource_type in cost.__dict__:
            amount = getattr(cost, resource_type)
            setattr(cost, resource_type, amount + 1)
        self.assertFalse(resource.enough(cost))

    def test_consume_another_resource_decreases_amount_of_resources(self):
        resources = Resources()
        resource_type = list(resources.__dict__.keys())[0]
        setattr(resources, resource_type, 10)
        cost = Resources()
        setattr(cost, resource_type, 3)
        resources.consume(cost)
        self.assertEqual(getattr(resources, resource_type), 7)

