from jijcloud.sampler import JijCloudSampler


class JijChimeraGPUSQASampler(JijCloudSampler):
    hardware = 'gpu'
    algorithm = 'chimera-sqa'

    def sample(self, bqm, unit_num_L=None, beta=1.0, gamma=1.0, trotter=4,
               num_reads=1, num_sweeps=100, timeout=None, sync=True):
        """sample ising
        Args:
            bqm (:obj:`dimod.BinaryQuadraticModel`): Binary quadratic model.
            unit_num_L (float, optional): the width of Chimera unit. The sampler generates Chimera graph with unit_num_L * unit_num_L Chimera units (unit_num_L * unit_num_L * 8 spins)
            beta (float, optional): inverse temperature. Defaults to 1.0.
            gamma (float, optional): minimum beta (initial beta in SA).
            trotter (int, optional): number of trotter slices. should be even.
            num_reads (int, optional): number of samples. Defaults to 1.
            num_sweeps (int, optional): number of MonteCarlo steps
            timeout (float, model): number of timeout for post request. Defaults to None.

        Returns:
            dimod.SampleSet: store minimum energy samples
                             .info['energy'] store all sample energies
        """

        # number of trotter should be even
        # since c++ implementation
        if trotter % 2 == 1:
            raise ValueError('trotter number should be even.')

        if unit_num_L == None:
            raise ValueError('please input unit_num_L')

        return super().sample(
            bqm, num_reads, num_sweeps,
            unit_num_L=unit_num_L,
            gamma=gamma, trotter=trotter, beta=1.0, 
            timeout=timeout,
            sync=sync
        )
