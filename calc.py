from abc import abstractmethod
import json

class State(object):
    def __init__(self):
        self.operators = ['+', '-', '*', '/']
        self.equals = '='

    def nextState(self,input):
        number = self.parseInt(input)
        if (number != None and 0 <= number and number <= 9):
            return self.handleNumber(number)
        elif self.isOperation(input):
            return self.handleOperation(input)
        elif self.isEquals(input):
            return self.handleEquals()
        else:
            return self.handleOther()

    def parseInt(self,input):
        try:
            output = int(input)
            return output
        except ValueError:
            return None

    def isOperation(self,input):
        return input in self.operators

    def isEquals(self,input):
        return self.equals == input

    def toJson(self):
        display = self.getDisplay()
        state = type(self).__name__
        jsonObject = {'display': display, 'state': state}
        self.addAdditionalFields(jsonObject)
        return json.dumps(jsonObject)

    def calculateOperation(self,num1,op,num2):
        if op == '+':
            return num1 + num2
        elif op == '-':
            return num1 - num2
        elif op == '*':
            return num1 * num2
        elif op == '/':
            return num1 / num2

    @abstractmethod
    def getDisplay(self):
        pass

    @abstractmethod
    def addAdditionalFields(self,jsonObject):
        pass

    @abstractmethod
    def handleNumber(self,number):
        pass
    @abstractmethod
    def handleOperation(self,operation):
        pass

    @abstractmethod
    def handleEquals(self):
        pass

    @abstractmethod
    def handleOther(self):
        pass

class InitialState(State):
    def __init__(self):
        super(InitialState,self).__init__()

    def handleNumber(self, number):
        return NumberState(number)

    def handleOperation(self,operation):
        return NumberOperationState(0, operation)

    def handleEquals(self):
        return self

    def handleOther(self):
        return self

    def getDisplay(self):
        return 0

    def addAdditionalFields(self,jsonObject):
        pass

class NumberState(State):
    def __init__(self,number):
        super(NumberState,self).__init__()
        self.number = number

    def handleNumber(self,number):
        return NumberState(self.number*10+number)

    def handleOperation(self,operation):
        return NumberOperationState(self.number,operation)

    def handleEquals(self):
        return NumberAfterEqualsState(self.number,'+',0)

    def handleOther(self):
        return self

    def getDisplay(self):
        return self.number

    def addAdditionalFields(self,jsonObject):
        jsonObject['number'] = self.number

class NumberOperationState(State):
    def __init__(self,number,operation):
        super(NumberOperationState,self).__init__()
        self.number = number
        self.operation = operation

    def handleNumber(self,number):
        return NumberOperationNumberState(self.number,self.operation,number)

    def handleOperation(self,operation):
        return NumberOperationState(self.number,operation)

    def handleEquals(self):
        result = self.calculateOperation(self.number,self.operation,self.number)
        return NumberAfterEqualsState(result,self.operation,self.number)

    def handleOther(self):
        return self

    def getDisplay(self):
        return self.number

    def addAdditionalFields(self,jsonObject):
        jsonObject['number'] = self.number
        jsonObject['operation'] = self.operation

class NumberOperationNumberState(State):
    def __init__(self,number1,operation,number2):
        super(NumberOperationNumberState,self).__init__()
        self.number1 = number1
        self.operation = operation
        self.number2 = number2

    def handleNumber(self,number):
        newNumber2 = self.number2*10+number
        return NumberOperationNumberState(self.number1,self.operation,newNumber2)

    def handleOperation(self,operation):
        number = self.calculateOperation(self.number1,self.operation,self.number2)
        return NumberOperationState(number,operation)

    def handleEquals(self):
        result = self.calculateOperation(self.number1,self.operation,self.number2)
        return NumberAfterEqualsState(result,self.operation,self.number2)

    def handleOther(self):
        return self

    def getDisplay(self):
        return self.number2

    def addAdditionalFields(self,jsonObject):
        jsonObject['number1'] = self.number1
        jsonObject['operation'] = self.operation
        jsonObject['number2'] = self.number2

class NumberAfterEqualsState(NumberState):
    def __init__(self,number_result,last_operation,last_input_number):
        super(NumberAfterEqualsState,self).__init__(number_result)
        self.last_operation = last_operation
        self.last_input_number = last_input_number

    def handleNumber(self,number):
        return NumberState(number)

    def handleEquals(self):
        new_number = self.calculateOperation(self.number,self.last_operation,self.last_input_number)
        return NumberAfterEqualsState(new_number,self.last_operation,self.last_input_number)

    def addAdditionalFields(self,jsonObject):
        jsonObject['number'] = self.number
        jsonObject['last_operation'] = self.last_operation
        jsonObject['last_input_number'] = self.last_input_number

class StateFactory():
    def __init__(self,json):
        self.json = json

    def create(self):
        if self.json is None:
            return InitialState()
        else:
            if type(self.json) is dict:
                jsonObject = self.json
            else:
                jsonObject = json.loads(self.json)
            state = jsonObject['state']
            if state == InitialState.__name__:
                return InitialState()
            elif state == NumberState.__name__:
                number = jsonObject['number']
                return NumberState(number)
            elif state == NumberOperationState.__name__:
                number = jsonObject['number']
                operation = jsonObject['operation']
                return NumberOperationState(number,operation)
            elif state == NumberOperationNumberState.__name__:
                number1 = jsonObject['number1']
                operation = jsonObject['operation']
                number2 = jsonObject['number2']
                return NumberOperationNumberState(number1,operation,number2)
            elif state == NumberAfterEqualsState.__name__:
                number = jsonObject['number']
                last_operation = jsonObject['last_operation']
                last_input_number = jsonObject['last_input_number']
                return NumberAfterEqualsState(number,last_operation,last_input_number)

def calculateNextState(json,input):
    currentState = StateFactory(json).create()
    nextState = currentState.nextState(input)
    return nextState.toJson()
