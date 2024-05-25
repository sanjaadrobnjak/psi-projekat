from .evaluator import evaluate, EvaluatorError
from django.test import TestCase


class EvaluatorTestCase(TestCase):
    
    def test_no_oper(self):
        self.assertEqual(evaluate('2', nums=[2]), 2)

    def test_evaluate_simple_expr(self):
        self.assertEqual(evaluate('2 + 2', nums=[2, 2]), 4)

    def test_unmatched_parenthesis(self):
        with self.assertRaises(EvaluatorError):
            evaluate('(2+', nums=[2])
    
    def test_number_not_in_alloed(self):
        with self.assertRaises(EvaluatorError):
            evaluate('2 + 3', [2])
    
    def test_calculates_ok(self):
        self.assertEqual(evaluate('(50+7)*10-7-4',[7, 4, 7, 5, 10, 50]), 559)