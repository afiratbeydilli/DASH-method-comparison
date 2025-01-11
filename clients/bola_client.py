import numpy as np
from clients.base_client import BaseClient

"""
    BOLA stands for Buffer Occupancy based Lyapunov Algorithm.
    The paper reference is presented in README.md file. One should
    note that the mathematical operations presented in the paper is 
    rather hard to implement. However, the paper selected an example
    for utility function and that example is illustrated here. In that
    example, qk = ln(bitrate). We select buffer stability term as 
    alpha * (buffer_level / max_buffer) -> See compute_utility() method.
"""

class BOLAClient(BaseClient):
    def __init__(self, bitrates, max_buffer, alpha=1.0):
        """
        BOLA client for adaptive bitrate streaming.
        :param alpha: Weighting factor for buffer utility.
        """
        super().__init__(bitrates, max_buffer)
        self.alpha = alpha

    def compute_utility(self, bitrate, buffer_level):
        # Note: np.log = ln, np.log10 = log10.
        return np.log(bitrate) + self.alpha * (buffer_level / self.max_buffer)

    def select_bitrate(self, bandwidth):
        utilities = [
            (bitrate, self.compute_utility(bitrate, self.buffer_size))
            for bitrate in self.bitrates if bitrate <= bandwidth
        ]  # Compute utility for a given bitrate if it is smaller than bandwidth.
        if utilities:  # If utilities is not empty, return the bitrate that has max. utility.
            return max(utilities, key=lambda x: x[1])[0]
        return min(self.bitrates)  # Else, return the smallest available bitrate.