import os
from nipype import Workflow, Node, Function

def sum(a, b):
    return a + b

wf = Workflow('hello')

adder = Node(Function(input_names=['a', 'b'],
                      output_names=['sum'],
                      function=sum),
             name='a_plus_b')

adder.inputs.a = 1
adder.inputs.b = 3

wf.add_nodes([adder])

wf.base_dir = os.getcwd()

eg = wf.run()

list(eg.nodes())[0].result.outputs

def concat(a, b):
    return [a, b]


concater = Node(Function(input_names=['a', 'b'],
                         output_names=['some_list'],
                         function=concat),
                name='concat_a_b')

wf.connect(adder, 'sum', concater, 'a')
concater.inputs.b = 3

eg = wf.run()
print(eg.nodes())

list(eg.nodes())[-1].result.outputs

def plus_one(a):
    return a + 1

plusone = Node(Function(input_names=['a'],
                        output_names=['out'],
                        function=plus_one),
               name='add_1')

wf.connect(concater, 'some_list', plusone, 'a')

try:
    eg = wf.run()
except(RuntimeError) as err:
    print("RuntimeError:", err)
else:
    raise
