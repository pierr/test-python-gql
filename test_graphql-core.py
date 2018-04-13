from __future__ import print_function

from graphql import graphql

from graphql.type import (GraphQLArgument,
                          GraphQLField, GraphQLNonNull, GraphQLObjectType,
                          GraphQLSchema, GraphQLString,
                          GraphQLInputObjectType,
                          GraphQLInputObjectField)

from graphql.language.parser import parse as parse_gql
from graphql.language.source import Source as Source_gql
from graphql.validation import validate as validate_gql

# GraphQLArgument, GraphQLEnumType, GraphQLEnumValue,
# GraphQLInterfaceType, GraphQLList, GraphQLInputObjectField

'''
    The query types
'''
# Define the meta part of the task
metaType = GraphQLObjectType('Meta', description='The meta informations', fields=lambda: {
'status': GraphQLField(
            GraphQLString,
            description='The status of the metadata',
        )
})
# Define the data part of the task
dataType = GraphQLObjectType('Data', description='The meta informations', fields=lambda: {
'name': GraphQLField(
        GraphQLString,
        description='The name of the data',
    )
})
# Define args type, which contains
# - metaType
# - dataType
argsType = GraphQLObjectType(
    'Args',
    description='The args container',
    fields=lambda: {
        'meta': GraphQLField(metaType),
        'data': GraphQLField(dataType),
        }
    )

# Define a query task type
taskType = GraphQLObjectType(
    'Task',
    description='A rabitMQ task from api to engine.',
    fields=lambda: {
        'id': GraphQLField(
            GraphQLNonNull(GraphQLString),
            description='The id of the task.'
        ),
        'args': GraphQLField(argsType),
        # 'meta': GraphQLField(metaType),
        # 'data': GraphQLField(dataType)
    }
)
# Define the query type of graphql
queryType = GraphQLObjectType(
    'Query',
    fields=lambda: {
        'startTraining': GraphQLField(
            taskType,
            # default arguments
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
    print('mutation_task_resolver')
    print(args)
    print(info)
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
def validation_errors(query):
    source = Source_gql(query, 'task.graphql')
    print(source.body)
    print(source.name)
    ast = parse_gql(source)
    return validate_gql(TaskSchema, ast)
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
    print("test_mutation :", variables)
    # print(" ##### mutation_query  ####### ")
    # print(mutation_query)
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


def validate_start_training(muta_vars):
    test_mutation(mq, {'task': muta_vars})


def validate(task_name, muta_vars):
    return {
        'engine:start': validate_start_training
    }[task_name](muta_vars)


muta_vars = {'id': '1', 'meta': {'status': 1}, 'data': {'name': 'Pierre'}}
validate('engine:start', muta_vars)
