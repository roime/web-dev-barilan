import json
import string
import calc
import unittest
import random
import urllib2

operators = ['+', '-', '*', '/']

def sendRequest(state,input):
    request_json = json.dumps({"calculatorState": state, "input": input})
    request = urllib2.Request('http://localhost:3000/calculate')
    request.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(request, request_json)
    data = json.load(response)
    return json.dumps(data)

class TestCasesFactory():
    def get_number_test_cases(self,json):
        #correct input case
        number = random.randint(0,9)
        result = sendRequest(json,number)
        return [(number,result)]

    def get_operation_test_cases(self,json):
        test_cases = []
        for operator in operators:
            result = sendRequest(json,operator)
            test_cases.append((operator,result))
        return test_cases

    def get_equals_test_cases(self,json):
        return [('=', sendRequest(json,'='))]

    def get_other_test_cases(self,json):
        #more than one digit number
        test_cases = []
        number = random.randint(10,99999)
        result = sendRequest(json,number)
        test_cases.append((number,result))
        #float number
        number = random.random() + random.randint(0,99999)
        result = sendRequest(json,number)
        test_cases.append((number, result))
        #negative number
        number = -random.randint(1,9)
        result = sendRequest(json,number)
        test_cases.append((number, result))
        #any char not in operators or equal
        char_list = string.ascii_letters + ''.join(set(string.punctuation) - {'+','-','=','*','/'})
        input = random.choice(char_list)
        result = sendRequest(json,number)
        test_cases.append((input,result))
        # any other string
        input = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(random.randint(2,15)))
        result = sendRequest(json,input)
        test_cases.append((input,result))
        return test_cases

    def get_initial_state_json(self):
        state = json.dumps({'display': 0, 'state': calc.InitialState.__name__ })
        return random.choice([None, state])

    def get_number_state_json(self, number):
        return json.dumps({'display': number, 'state': calc.NumberState.__name__, 'number':number})

    def get_number_operation_state_json(self, number, operator):
        return json.dumps({'display': number, 'state': calc.NumberOperationState.__name__, 'number': number, 'operation': operator})

    def get_number_operation_number_state_json(self, number, operator, number2):
        return json.dumps({'display': number2, 'state': calc.NumberOperationNumberState.__name__, 'number1': number, 'number2': number2,'operation': operator})

    def get_number_after_equals_state_json(self, number, last_operation, last_input_number):
        return json.dumps({'display': number, 'state': calc.NumberAfterEqualsState.__name__, 'number': number, 'last_input_number': last_input_number,'last_operation': last_operation})


test_cases_creator = TestCasesFactory()

class TestInitialState(unittest.TestCase):

    def testNumberCase(self):
        state = test_cases_creator.get_initial_state_json()
        test_cases = test_cases_creator.get_number_test_cases(state)
        for number,result in test_cases:
            expected_subset = {'display': number}
            self.assertDictContainsSubset(expected_subset, json.loads(result))

    def testOperationCase(self):
        state = test_cases_creator.get_initial_state_json()
        test_cases = test_cases_creator.get_operation_test_cases(state)
        for operation,result in test_cases:
            expected_subset = {'display': 0}
            self.assertDictContainsSubset(expected_subset, json.loads(result))

    def testOtherCase(self):
        state = test_cases_creator.get_initial_state_json()
        test_cases = test_cases_creator.get_other_test_cases(state)
        for other,result in test_cases:
            expected_subset = {'display': 0}
            self.assertDictContainsSubset(expected_subset, json.loads(result))

    def testEqualsCase(self):
        state = test_cases_creator.get_initial_state_json()
        test_cases = test_cases_creator.get_equals_test_cases(state)
        for equals,result in test_cases:
            expected_subset = {'display': 0}
            self.assertDictContainsSubset(expected_subset, json.loads(result))

class TestNumberState(unittest.TestCase):

    def testNumberCase(self):
        random_number = random.randint(0,99999)
        state = test_cases_creator.get_number_state_json(random_number)
        test_cases = test_cases_creator.get_number_test_cases(state)
        for number,result in test_cases:
            expected_subset = {'display': int(str(random_number)+str(number))}
            self.assertDictContainsSubset(expected_subset, json.loads(result))

    def testOperationCase(self):
        random_number = random.randint(0, 99999)
        state = test_cases_creator.get_number_state_json(random_number)
        test_cases = test_cases_creator.get_operation_test_cases(state)
        for operation,result in test_cases:
            expected_subset = {'display': random_number}
            self.assertDictContainsSubset(expected_subset, json.loads(result))

    def testOtherCase(self):
        random_number = random.randint(0, 99999)
        state = test_cases_creator.get_number_state_json(random_number)
        test_cases = test_cases_creator.get_other_test_cases(state)
        for other,result in test_cases:
            expected_subset = {'display': random_number}
            self.assertDictContainsSubset(expected_subset, json.loads(result))

    def testEqualsCase(self):
        random_number = random.randint(0, 99999)
        state = test_cases_creator.get_number_state_json(random_number)
        test_cases = test_cases_creator.get_equals_test_cases(state)
        for equals,result in test_cases:
            expected_subset = {'display': random_number}
            self.assertDictContainsSubset(expected_subset, json.loads(result))

class TestNumberOperationState(unittest.TestCase):
    def testNumberCase(self):
        random_number = random.randint(0,99999)
        random_operator = random.choice(operators)
        state = test_cases_creator.get_number_operation_state_json(random_number,random_operator)
        test_cases = test_cases_creator.get_number_test_cases(state)
        for number,result in test_cases:
            expected_subset = {'display': number}
            self.assertDictContainsSubset(expected_subset, json.loads(result))

    def testOperationCase(self):
        random_number = random.randint(0,99999)
        random_operator = random.choice(operators)
        state = test_cases_creator.get_number_operation_state_json(random_number,random_operator)
        test_cases = test_cases_creator.get_operation_test_cases(state)
        for operation,result in test_cases:
            expected_subset = {'display': random_number}
            self.assertDictContainsSubset(expected_subset, json.loads(result))

    def testOtherCase(self):
        random_number = random.randint(0,99999)
        random_operator = random.choice(operators)
        state = test_cases_creator.get_number_operation_state_json(random_number,random_operator)
        test_cases = test_cases_creator.get_other_test_cases(state)
        for other,result in test_cases:
            expected_subset = {'display': random_number}
            self.assertDictContainsSubset(expected_subset, json.loads(result))

    def testEqualsCase(self):
        random_number = random.randint(0,99999)
        random_operator = random.choice(operators)
        state = test_cases_creator.get_number_operation_state_json(random_number,random_operator)
        test_cases = test_cases_creator.get_equals_test_cases(state)
        for equals,result in test_cases:
            expected_subset = {'display': eval(str(random_number) + random_operator + str(random_number))}
            self.assertDictContainsSubset(expected_subset, json.loads(result))

class TestNumberOperationNumberState(unittest.TestCase):
    def testNumberCase(self):
        random_number = random.randint(0,9999)
        random_operator = random.choice(operators)
        random_number2 = random.randint(0,9999)
        state = test_cases_creator.get_number_operation_number_state_json(random_number,random_operator,random_number2)
        test_cases = test_cases_creator.get_number_test_cases(state)
        for number,result in test_cases:
            expected_subset = {'display': int(str(random_number2)+str(number))}
            self.assertDictContainsSubset(expected_subset, json.loads(result))

    def testOperationCase(self):
        random_number = random.randint(0,200)
        random_operator = random.choice(operators)
        random_number2 = random.randint(0,200)
        state = test_cases_creator.get_number_operation_number_state_json(random_number,random_operator,random_number2)
        test_cases = test_cases_creator.get_operation_test_cases(state)
        for operation,result in test_cases:
            expected_subset = {'display': eval(str(random_number) + random_operator + str(random_number2))}
            self.assertDictContainsSubset(expected_subset, json.loads(result))

    def testOtherCase(self):
        random_number = random.randint(0,9999)
        random_operator = random.choice(operators)
        random_number2 = random.randint(0,9999)
        state = test_cases_creator.get_number_operation_number_state_json(random_number,random_operator,random_number2)
        test_cases = test_cases_creator.get_other_test_cases(state)
        for other,result in test_cases:
            expected_subset = {'display': random_number2}
            self.assertDictContainsSubset(expected_subset, json.loads(result))

    def testEqualsCase(self):
        random_number = random.randint(0,9999)
        random_operator = random.choice(operators)
        random_number2 = random.randint(0,9999)
        state = test_cases_creator.get_number_operation_number_state_json(random_number,random_operator,random_number2)
        test_cases = test_cases_creator.get_equals_test_cases(state)
        for equals,result in test_cases:
            expected_subset = {'display': eval(str(random_number) + random_operator + str(random_number2))}
            self.assertDictContainsSubset(expected_subset, json.loads(result))

class TestNumberAfterEqualsState(unittest.TestCase):
    def testNumberCase(self):
        random_number = random.randint(0,9999)
        random_operator = random.choice(operators)
        random_number2 = random.randint(0,9999)
        state = test_cases_creator.get_number_after_equals_state_json(random_number,random_operator,random_number2)
        test_cases = test_cases_creator.get_number_test_cases(state)
        for number,result in test_cases:
            expected_subset = {'display': number}
            self.assertDictContainsSubset(expected_subset, json.loads(result))

    def testOperationCase(self):
        random_number = random.randint(0,200)
        random_operator = random.choice(operators)
        random_number2 = random.randint(0,200)
        state = test_cases_creator.get_number_after_equals_state_json(random_number,random_operator,random_number2)
        test_cases = test_cases_creator.get_operation_test_cases(state)
        for operation,result in test_cases:
            expected_subset = {'display': random_number}
            self.assertDictContainsSubset(expected_subset, json.loads(result))

    def testOtherCase(self):
        random_number = random.randint(0,200)
        random_operator = random.choice(operators)
        random_number2 = random.randint(0,200)
        state = test_cases_creator.get_number_after_equals_state_json(random_number,random_operator,random_number2)
        test_cases = test_cases_creator.get_other_test_cases(state)
        for other,result in test_cases:
            expected_subset = {'display': random_number}
            self.assertDictContainsSubset(expected_subset, json.loads(result))

    def testEqualsCase(self):
        random_number = random.randint(0,200)
        random_operator = random.choice(operators)
        random_number2 = random.randint(0,200)
        state = test_cases_creator.get_number_after_equals_state_json(random_number,random_operator,random_number2)
        test_cases = test_cases_creator.get_equals_test_cases(state)
        for equals,result in test_cases:
            expected_subset = {'display': eval(str(random_number) + random_operator + str(random_number2))}
            self.assertDictContainsSubset(expected_subset, json.loads(result))

if __name__ == '__main__':
    unittest.main()