# import dimod
# from typing import Dict, List, Union, Optional
# from abc import ABCMeta
# from jijcloud.post_api import post_instance_and_query
# import pyqubo


# class JijModelSamplerInterface(metaclass=ABCMeta):
#     """Model post Interface
#     Do not use alone
#     """

#     def sample_model(self,
#                      model: pyqubo.core.model.Model,
#                      conditions: Dict[str, str],
#                      multipliers: Dict[str, Union[str, List[str]]],
#                      vartype: str = 'BINARY',
#                      feed_dict: Optional[Dict[str, float]] = None,
#                      search: bool = None,
#                      max_iter=5,
#                      alpha=1.0,
#                      timeout=None,
#                      **kwargs) -> dimod.SampleSet:
#         """Sampling from PyQUBO model

#         Args:
#             model (pyqubo.core.model.Model): compiled PyQUBO model.
#             conditions (Dict[str, str]): key is label of constraints.
#                                          value is conditions (== a or <= a).
#             multipliers (Dict[str, Union[str, List[str]]]): map label of placeholder to constraints. 
#             vartype (str, optional): 'BINARY' or 'SPIN'. Defaluts to 'BINARY'.
#             feed_dict (Optional[Dict[str, float]]): Initial feed_dict. Defaults to None.
#             search (bool): Parameter search flag. Defaluts None.
#             max_iter (int): maximum iteration of parameter search. Defaults to 5.
#             alpha (float): for parameter search. Defaults to 1.0.
#             timeout (float): number of timeout for post request. Defaults to None.

#         Returns:
#             dimod.SampleSet: result.
#         """

#         # validation ----------------------------------
#         if not isinstance(conditions, dict):
#             raise TypeError('conditions is dict')
#         if not isinstance(multipliers, dict):
#             raise TypeError('multipliers is dict')
#         if feed_dict is not None and (not isinstance(feed_dict, dict)):
#             raise TypeError('feed_dict is dict')
#         # ---------------------------------- validation

#         # validation each setting --------------------
#         # if feed_dict is not None:
#         #     for k in feed_dict.keys():
#         #         if k not in multipliers:
#         #             raise ValueError(
#         #                 '{} is not defined in "multipliers".'.format(k))

#         for consts in multipliers.values():
#             if isinstance(consts, list):
#                 for c in consts:
#                     if c not in conditions:
#                         raise ValueError(
#                             '{} is not defined in "conditions".'.format(c)
#                         )
#             elif isinstance(consts, str):
#                 if consts not in conditions:
#                     raise ValueError(
#                         '{} is not defined in "conditions".'.format(consts)
#                     )
#             else:
#                 raise TypeError(
#                     '{} should be list or str.'.format(consts)
#                 )
#         # -------------------- validation each setting

#         # if feed_dict is given
#         # defalut search is False
#         if feed_dict and search is None:
#             search = False
#         else:
#             search = True

#         problem = _pyqubo_to_dict(model)

#         # key convert to str
#         problem['qubo'] = {'{} {}'.format(i, j): Qij
#                            for (i, j), Qij in problem['qubo'].items()}
#         problem['conditions'] = conditions
#         problem['multipliers_constraint'] = multipliers

#         parameters = kwargs
#         parameters['search'] = search
#         parameters['feed_dict'] = feed_dict
#         parameters['max_iter'] = max_iter
#         parameters['alpha'] = alpha

#         body = {
#             'hardware': self.hardware,
#             'algorithm': self.algorithm,
#             'num_variables': len(model.compiled_qubo.variables),
#             'problem': problem,
#             'problem_type': 'PyQUBO-Model',
#             'parameters': parameters,
#             'info': {}
#         }

#         # if timeout is defined in script, use this value
#         if timeout:
#             self.timeout = timeout

#         status_code, response = post_instance_and_query(
#             self.url, self.token, body, self.timeout)
#         res = response['response']
#         additional_info = response['info']
#         res = response['response']
#         additional_info = response['info']
#         sample_set = dimod.SampleSet.from_serializable(res)
#         sample_set.info.update(additional_info)
#         return sample_set


# def _pyqubo_to_dict(model):
#     qubo = model.compiled_qubo.qubo

#     offset = model.compiled_qubo.offset
#     if isinstance(offset, float):
#         offset = [[offset, {}]]
#     else:
#         offset = [
#             [v, k.keys]
#             for k, v in offset.terms.items()
#         ]

#     dict_qubo = {}
#     for key, value in qubo.items():
#         serierized_value = []

#         if isinstance(value, float):
#             serierized_value.append([value, {}])
#         else:
#             for k, v in value.terms.items():
#                 serierized_value.append([v, k.keys])
#         dict_qubo[key] = serierized_value

#     # TODO: Validation check constraints
#     constraints = {}
#     for label, const in model.constraints.items():
#         constraints[label] = []
#         for key, v in const.polynomial.items():
#             constraints[label].append([v] + list(key.keys))

#     return {
#         'qubo': dict_qubo,
#         'constraints': constraints,
#         'offset': offset
#     }
