from jijcloud.sampler import JijCloudSampler
from jijcloud.sampler.jijmodel_post import JijModelingInterface

from typing import Dict, Union
from numbers import Number
from jijmodeling.expression.expression import Expression
import numpy as np


class JijSQASampler(JijCloudSampler, JijModelingInterface):
    hardware = 'cpu'
    algorithm = 'SQA'

    def sample(self, bqm, beta=1.0, gamma=1.0, trotter=4,
               num_reads=1, num_sweeps=100, timeout=None, sync=True):
        """sample ising
        Args:
            bqm (:obj:`dimod.BinaryQuadraticModel`): Binary quadratic model.
            beta (float, optional): inverse temperature. Defaults to 1.0.
            gamma (float, optional): minimum beta (initial beta in SA).
            trotter (int, optional): number of trotter slices. should be even.
            num_reads (int, optional): number of samples. Defaults to 1.
            num_sweeps (int, optional): number of MonteCarlo steps
            timeout (float, optional): number of timeout for post request. Defaults to None.

        Returns:
            dimod.SampleSet: store minimum energy samples
                             .info['energy'] store all sample energies
        """

        # number of trotter should be even
        # since c++ implementation
        if trotter % 2 == 1:
            raise ValueError('trotter number should be even.')

        return super().sample(
            bqm, num_reads, num_sweeps,
            gamma=gamma, trotter=trotter, beta=1.0,
            timeout=timeout,
            sync=sync
        )

    def sample_model(
            self,
            model: Expression,
            feed_dict: Dict[str, Union[Number, list, np.ndarray]], 
            multipliers: Dict[str, Number], 
            search: bool=False, timeout=10,
            num_reads:int = 1,
            num_sweeps:int = 100,
            beta=1.0, gamma=1.0, trotter=4,
            sync=False, 
        ):

        return super().sample_model(
            model,
            feed_dict=feed_dict, 
            multipliers=multipliers,
            search=search,
            sync=sync,
            num_reads=num_reads, num_sweeps=num_sweeps,
            beta=beta, gamma=gamma, trotter=trotter, sqa='sqa'
        )
