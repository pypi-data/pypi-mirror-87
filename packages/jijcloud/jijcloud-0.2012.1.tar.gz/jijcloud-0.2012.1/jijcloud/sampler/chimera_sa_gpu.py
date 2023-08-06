from jijcloud.sampler import JijCloudSampler


class JijChimeraGPUSASampler(JijCloudSampler):
    hardware = 'gpu'
    algorithm = 'chimera-sa'

    def sample(self, bqm,
               unit_num_L=None,
               beta_min=None, beta_max=None,
               num_reads=1, num_sweeps=100,
               timeout=None, sync=True):
        """sample ising
        Args:
            bqm (:obj:`dimod.BinaryQuadraticModel`): Binary quadratic model.
            unit_num_L (float, optional): the width of Chimera unit. The sampler generates Chimera graph with unit_num_L * unit_num_L Chimera units (unit_num_L * unit_num_L * 8 spins)
            beta_min (float, optional): minimum beta (initial beta in SA).
            beta_max (float, optional): maximum beta (final beta in SA).
            num_reads (int, optional): number of samples. Defaults to 1.
            num_sweeps (int, optional): number of MonteCarlo steps.
            timeout (float optional): number of timeout for post request. Defaults to None. 
        Returns:
            dimod.SampleSet: store minimum energy samples
                             .info['energy'] store all sample energies
        """

        if beta_min and beta_max:
            if beta_min > beta_max:
                raise ValueError('beta_min < beta_max')

        if unit_num_L == None:
            raise ValueError('please input unit_num_L')

        return super().sample(
            bqm, num_reads, num_sweeps,
            unit_num_L=unit_num_L,
            beta_min=beta_min, beta_max=beta_max,
            timeout=timeout,
            sync=sync
        )
