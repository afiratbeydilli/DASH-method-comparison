import math
from clients.base_client import BaseClient

"""
    This class implements the PD controller described in the 
    paper cited in the references (see README.md file). Different
    than a regular PD controller, the paper presents a model that 
    makes a rate adaptation if buffer content is lower than a threshold (bk1)
    or higher than a threshold (bk2). If buffer content resides in between,
    there is no adaptation at all. The parameters of PD controller
    is rather cumbersome but it was not so hard to make some calculations.
    So, the client using PD Controller as rate adaptation algorithm in DASH
    is correctly presented in below class.
"""
class PDControllerClient(BaseClient):
    def __init__(self, bitrates, max_buffer, bk1, bk2, sliding_window_size=5, T=2.0, eta=1.0):
        """
        :param bitrates: List of available bitrates in Mbps ([1, 2, 4, 6, 8, 12])
        :param max_buffer: Maximum buffer size in seconds
        :param bk1: Lower buffer threshold in seconds
        :param bk2: Upper buffer threshold in seconds
        :param T: Segment duration in seconds
        :param eta: Control aggressiveness factor (so the internet says)
        """
        super().__init__(bitrates, max_buffer)
        # Parameters that are going to be used while calculation of kp and kd.
        self.bk1 = bk1  # Lower buffer threshold
        self.bk2 = bk2  # Upper buffer threshold
        self.T = T  # Segment duration
        self.eta = eta  # Control aggressiveness factor
        self.sliding_window_size = sliding_window_size

        # Calculation of kd and kp itself
        # IMPORTANT!! kp calculation should DEFINITELY be after kd.
        self.kd = self.compute_kd()  # Derivative gain
        self.kp = self.compute_kp()  # Proportional gain

        # Parameters that are going to be used in bitrate selection.
        # This part resembles to RateBasedMethodClient, see that section.
        self.prev_bitrate = min(bitrates)  # Start with the lowest bitrate
        self.prev_download_time = None  # Store the previous download time
        self.bandwidth_estimates = []

    def compute_kd(self):
        """
        Compute the derivative gain (kd) using the constraint from the paper.
        Starts with T/2 and validates it. Adjusts kd if necessary.
        """
        kd = self.T / 2  # Initial guess
        if not self.validate_kd(kd):
            # Adjust kd iteratively if the initial guess is invalid
            kd = self.find_valid_kd()
        return kd

    def validate_kd(self, kd):
        """
        Validate kd using the inequality from the paper.
        :param kd: Derivative gain to validate
        :return: True if valid, False otherwise
        """
        rhs = (1 / self.T) * math.sqrt((self.T + kd) / (self.T - kd)) * math.log(20 * self.T / (self.T + kd))
        return self.eta >= rhs

    def find_valid_kd(self):
        """
        Find a valid kd within (0, T) using a decremental approach.
        :return: A valid kd value
        """
        kd = self.T / 2  # Start with T/2
        step = self.T / 10  # Decremental step
        while kd > 0:
            if self.validate_kd(kd):
                return kd
            kd -= step  # Decrease kd incrementally
        raise ValueError("Unable to find a valid kd within the range (0, T).")

    def compute_kp(self):
        """
        Compute the proportional gain (kp) based on kd.
        """
        return self.eta * math.sqrt((self.T + self.kd) / (self.T - self.kd))

    def estimate_bandwidth(self, bandwidth):
        """
        Update and return the estimated bandwidth.
        see: RateBasedMethodClient
        """
        self.bandwidth_estimates.append(bandwidth)
        if len(self.bandwidth_estimates) > self.sliding_window_size:
            self.bandwidth_estimates.pop(0)
        return sum(self.bandwidth_estimates) / len(self.bandwidth_estimates)

    def compute_bitrate(self, current_buffer, bandwidth):
        """
        Compute the new bitrate based on buffer thresholds and PD control.
        """
        beta_est = self.estimate_bandwidth(bandwidth)

        if current_buffer < self.bk1:
            error = current_buffer - self.bk1
        elif current_buffer > self.bk2:
            error = current_buffer - self.bk2
        else:
            return self.prev_bitrate  # Stable region

        delta_r = (1 / (self.T * beta_est)) * (
            self.kp * error + self.kd * (self.T - self.prev_download_time) / self.prev_download_time
        )
        return self.prev_bitrate + delta_r

    def select_bitrate(self, bandwidth):
        """
        Select the closest bitrate to the computed bitrate.
        """
        current_buffer = self.buffer_size  # Step 1: Get the current buffer level
        bitrate = self.compute_bitrate(current_buffer, bandwidth)  # Step 2: Compute the ideal bitrate

        closest_bitrate = min(self.bitrates, key=lambda x: abs(x - bitrate))  # Step 3: Find the closest bitrate
        self.prev_bitrate = closest_bitrate  # Step 4: Renew our 'previous'
        return closest_bitrate  # One of our bitrates.