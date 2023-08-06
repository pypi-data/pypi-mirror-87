from jijcloud.sampler import JijCloudSampler
import dimod


class JijHUBOSampler(JijCloudSampler):
    hardware = 'CPU'
    algorithm = 'SA'

    def sample_hubo(self, interactions,
                    beta_min=None, beta_max=None,
                    num_reads=1, mc_steps=100, 
                    timeout=None):
        """sample ising
        Args:
            interactions (list of dict): list of coefficients (dict) of each term. must be in ascending order. [h, J, K, ...]
            beta_min (float, optional): minimum beta (initial beta in SA).
            beta_max (float, optional): maximum beta (final beta in SA).
            num_reads (int, optional): number of samples. Defaults to 1.
            mc_steps (int, optional): number of MonteCarlo steps.
            timeout (float, optional): number of timeout for post request. Defaults to None.

        Returns:
            dimod.SampleSet: store minimum energy samples
                             .info['energy'] store all sample energies
        """

        _interactions = []
        for coeff in interactions:
            key_str = ''
            coeff_dict = {}
            for key, value in coeff.items():
                if not isinstance(key, tuple):
                    key_str = str(key)
                else:
                    key_str = str(key[0])
                    for k in key[1:]:
                        key_str += ' ' + str(k)
                coeff_dict[key_str] = value

            _interactions.append(coeff_dict)

        parameters = {
            'num_reads': num_reads,
            'mc_steps': mc_steps,
            'beta_min': beta_min,
            'beta_max': beta_max,
        }

        request_json = self._make_requests_dict(
            _interactions, problem_type='hubo',
            parameters=parameters
        )

        status_code, response = self._post_requests(
            request_json, self.url, self.token
        )

        result = response['result']
        energy = [result['min_energy']]*len(result['samples'])
        info = result['info']
        info['energies'] = result['energies']
        sample_set = dimod.SampleSet.from_samples(
            result['samples'],
            num_occurrences=result['num_occurrences'],
            energy=energy, vartype='SPIN',
            info=info)

        return sample_set
