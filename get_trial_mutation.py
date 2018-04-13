from __future__ import print_function

import graphene


# class TrialArgsData(graphene.InputObjectType):
#     name = 'TrialArgsData'
#     description = 'For the celery task: engine:train:get-trial-result'
#
#     dataset = graphene.String()
#     modelchoice = graphene.String()
#     project = graphene.String()
#     train_id = graphene.String()
#     transfo_id = graphene.String()


class TrialArgsInput(graphene.InputObjectType):
    meta = graphene.String()
    data = graphene.String()


class TrialArgsOutPut(graphene.ObjectType):
    meta = graphene.String()
    data = graphene.String()


class TrialResults(graphene.InputObjectType):
    task = graphene.String(required=True)
    kwargs = graphene.String(required=True)
    id_ = graphene.String(required=True)  # TODO: rename id_
    lol = TrialArgsInput(required=True)


class TrialTypeDefinition(graphene.ObjectType):
    task = graphene.String()
    kwargs = graphene.String()
    id_ = graphene.String()
    lol = TrialArgsOutPut()


class CreateTrialMutation(graphene.Mutation):

    class Arguments:
        # trial_results will be replaced by
        # trialResults in graphQL format
        trial_results = TrialResults(required=True)

    Output = TrialTypeDefinition

    def mutate(self, info, trial_results):
        print('Mutate')
        return TrialTypeDefinition(
            task=trial_results.task,
            kwargs=trial_results.kwargs,
            id_=trial_results.id_,
            lol=trial_results.lol
        )


class TrialMutation(graphene.ObjectType):
    # create_trial_mutation will be replaced by
    # createTrialMutation
    # in graphQL format
    create_trial_mutation = CreateTrialMutation.Field()


schema = graphene.Schema(mutation=TrialMutation)


mutate_args1 = '''
task:\"engine:train:get-trial-result\",
kwargs:\"\",
id_:\"ed0f9e10-7b43-42da-93b4-7b3e0f0fb70f\"'''

mutation1 = '''
    mutation toto{
      createTrialMutation(trialResults: { ''' + mutate_args1 + '''}) {
        task
        kwargs
        id_
      }
    }
'''

mutate_arg2_dict = {
    'task': "engine:train:get-trial-result",
    'kwargs': "",
    'id_': "ed0f9e10-7b43-42da-93b4-7b3e0f0fb70f",
    'lol': {
        "meta": "requested",
        "data": "lolo"
    }
}


mutation2 = '''
    mutation toto($param: TrialResults!){
      createTrialMutation(trialResults: $param) {
        task
        kwargs
        id_
        lol
      }
    }
'''


def validateTrialMutation(json_data):
    print("In get_trial_mutation: validateTrialMutation")

    print("<---JSON DATA ---->\n", json_data)

    # muta1
    result1 = schema.execute(mutation1)
    print(mutation1)
    print("<---Results 1 ---->\n", result1)
    print("<---Results 1 / data ---->\n", result1.data)
    # print(result1.data['createAddress']['latlng'])
    print("<---ERRORS ---->\n", result1.errors, "\n")
    # raw_input("muta1 executed\n")

    # muta1
    result2 = schema.execute(mutation2, variable_values={'param': mutate_arg2_dict})
    print(mutation2)
    print("<---Results 2 ---->\n", result2)
    print("<---Results 2 / data ---->\n", result2.data)
    # print(result1.data['createAddress']['latlng'])
    print("<---ERRORS ---->\n", result2.errors, "\n")
    # raw_input("muta1 executed\n")

    return True


if __name__ == '__main__':

    data="{u'task': u'engine:train:get-trial-result', u'id': u'ed0f9e10-7b43-42da-93b4-7b3e0f0fb70f', u'args': [{u'status': u'requested'}, {u'project': u'5ac7a6edf644b20166caf596', u'modelchoice': u'supervised', u'transfo_id': u'5ace094a761e68003c34fda0', u'train_id': u'5ace094a761e68003c34fda1', u'dataset': u'5ac7a6faf644b20166caf597'}], u'kwargs': {}}"

    validateTrialMutation(data)
