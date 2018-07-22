import unittest
from entities import Resources


class TestResource(unittest.TestCase):

    def test_can_empty_a_resource(self):
        resource = Resources(a=10)
        resource.empty()
        self.assertEqual(resource.a, 0)

    def test_enough_resources_to_pay_cost(self):
        resource = Resources()
        cost = Resources()
        self.assertTrue(resource.enough(cost))
        for resource_type in cost.__dict__:
            setattr(cost, resource_type, 1)
        self.assertFalse(resource.enough(cost))

    def test_consume_another_resource_decreases_amount_of_resources(self):
        resource = Resources(a=10)
        cost = Resources(a=3)
        resource.consume(cost)
        self.assertEqual(resource.a, 7)

