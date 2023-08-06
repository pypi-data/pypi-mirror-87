from jijcloud.sampler import JijCloudSampler
from jijcloud.sampler.jijmodel_post import JijModelingInterface

from typing import Dict, Union
from numbers import Number
from jijmodeling.expression.expression import Expression
import numpy as np


class JijSASampler(JijCloudSampler, JijModelingInterface):
    hardware = 'cpu'
    algorithm = 'SA'

    def sample(self, bqm,
               beta_min=None, beta_max=None,
               num_reads=1, num_sweeps=100,
               timeout=None, sync=True):
        """sample ising
        Args:
            bqm (:obj:`dimod.BinaryQuadraticModel`): Binary quadratic model.
            beta_min (float, optional): minimum beta (initial beta in SA).
            beta_max (float, optional): maximum beta (final beta in SA).
            num_reads (int, optional): number of samples. Defaults to 1.
            num_sweeps (int, optional): number of MonteCarlo steps.
            timeout (float, optional): number of timeout for post request. Defaults to None.

        Returns:
            dimod.SampleSet: store minimum energy samples
                             .info['energy'] store all sample energies
        """

        if beta_min and beta_max:
            if beta_min > beta_max:
                raise ValueError('beta_min < beta_max')

        return super().sample(
            bqm, num_reads, num_sweeps, timeout,
            beta_min=beta_min, beta_max=beta_max, sa='sa',
            sync=sync
        )

    def sample_model(self, 
                    model: Expression, 
                    feed_dict: Dict[str, Union[Number, list, np.ndarray]], 
                    multipliers: Dict[str, Number], 
                    search: bool=False, timeout=10,
                    num_reads:int = 1,
                    num_sweeps:int = 100,
                    beta_min=None, beta_max=None,
                    sync=False
                    ):

        return super().sample_model(
            model,
            feed_dict=feed_dict, 
            multipliers=multipliers,
            search=search,
            sync=sync,
            num_reads=num_reads, num_sweeps=num_sweeps,
            beta_min=beta_min, beta_max=beta_max
        )
1