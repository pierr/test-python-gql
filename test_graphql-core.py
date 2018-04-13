from graphql import graphql

from graphql.type import (GraphQLArgument,
                          GraphQLField, GraphQLNonNull, GraphQLObjectType,
                          GraphQLSchema, GraphQLString,
                          GraphQLInputObjectType,
                          GraphQLInputObjectField)

# GraphQLArgument, GraphQLEnumType, GraphQLEnumValue,
# GraphQLInterfaceType, GraphQLList, GraphQLInputObjectField

'''
    The query types
'''# Define the meta part of the task
metaType = GraphQLObjectType('Meta', description='The meta informations', fields=lambda: {
    'status': GraphQLField(
            GraphQLString,
            description='The status of the metadata',
        )
})
# Define the data part of the task
dataType =  GraphQLObjectType('Data', description='The meta informations', fields=lambda: {
'name': GraphQLField(
        GraphQLString,
        description='The name of the data',
    )
})
# Define a query task type
taskType = GraphQLObjectType(
    'Task',
    description='A rabitMQ task from api to engine.',
    fields=lambda: {
        'id': GraphQLField(
            GraphQLNonNull(GraphQLString),
            description='The id of the task.'
        ),
        'meta': GraphQLField(metaType),
        'data': GraphQLField(dataType)
    }
)
# Define the query type of graphql
queryType = GraphQLObjectType(
    'Query',
    fields=lambda: {
        'startTraining': GraphQLField(
            taskType,
            resolver=lambda root, info, **args: {'id': '1', 'meta': {'status': 'error'}, 'data': {'name': 'Pierre'}}
        )

    }
)



'''
The mutation part
'''

# Define the meta part of the task
metaInputType = GraphQLInputObjectType('MetaInput', description='The meta informations', fields=lambda: {
    'status': GraphQLInputObjectField(
            GraphQLString,
            description='The status of the metadata',
        )
})
# Define the data part of the task
dataInputType =  GraphQLInputObjectType('DataInput', description='The meta informations', fields=lambda: {
'name': GraphQLInputObjectField(
        GraphQLString,
        description='The name of the data',
    )
})
# Define a query task type
taskInputType = GraphQLInputObjectType(
    'TaskInput',
    description='A rabitMQ task from api to engine.',
    fields=lambda: {
        'id': GraphQLInputObjectField(
            GraphQLNonNull(GraphQLString),
            description='The id of the task.'
        ),
        'meta': GraphQLInputObjectField(metaInputType),
        'data': GraphQLInputObjectField(dataInputType)
    }
)

def mutation_task_resolver(root, info, **args):
    print 'mutation_task_resolver'
    print args
    print info
    return {'id': '1', 'meta': {'status': 'error'}, 'data': {'name': 'Pierre'}}
# Define the query type of graphql
mutationTask = GraphQLObjectType(
    'Mutation',
    fields=lambda: {
        'startTraining': GraphQLField(
            taskType,
            args={'task': GraphQLArgument(
                description='The task argument',
                type=taskInputType
            )},
            resolver=mutation_task_resolver
        )

    }
)

'''
Building the final schema
'''
TaskSchema = GraphQLSchema(query=queryType, mutation=mutationTask , types=[metaType, dataType, taskType])

### Test on some schema validation
from graphql.language.parser import parse
from graphql.language.source import Source
from graphql.validation import validate
def validation_errors(query):
    source = Source(query, 'task.graphql')
    print(source.body)
    print(source.name)
    ast = parse(source)
    return validate(TaskSchema, ast)
q = '''
    query TestTask1 {
       startTraining {
           meta { status }
       }
    }
'''
print(validation_errors(q))


#### from graphql import graphql
def test_mutation(mutation_query, variables):
    print variables
    res = graphql(TaskSchema, mutation_query, variable_values=variables)
    print (res.data)
    print (res.errors)

mq = '''
mutation TryStartTrain($task: TaskInput) {
            startTraining(task: $task) {
                data {
                    name
                }
            }
        }

'''
mv = {'task': {'id': '1', 'meta': {'statas': 1}, 'data': {'name': 'Pierre'}}}
test_mutation(mq, mv)

print("\n\n")

mv = {'task': {'id': '1', 'meta': {'status': 1}, 'data': {'name': 'Pierre'}}}
test_mutation(mq, mv)


var = {'id': '1', 'meta': {'status': 1}, 'data': {'name': 'Pierre'}}


def validate_start_training(parameters):
    test_mutation(mq, {'task': parameters})


def validate(task_name, parameters):
    return {
        'engine:start': validate_start_training
    }[task_name](parameters)


validate('engine:start', var)
