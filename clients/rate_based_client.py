from clients.base_client import BaseClient
"""
    This client calculates & selects bitrate of the video on DASH based on
    estimations on available bandwidth. This is implemented by saving
    historical throughput. The history of the throughput is saved into a list, 
    and we estimate an average throughput based on our saved samples. Furthermore,
    we have a sliding window in our history list so that we do not inspect
    very old examples even though so many time has been passed (up to date).
"""
class RateBasedMethodClient(BaseClient):
    def __init__(self, bitrates, max_buffer, sliding_window_size=5):
        super().__init__(bitrates, max_buffer)
        self.sliding_window_size = sliding_window_size
        self.throughput_history = []  # Store recent throughput estimates

    def estimate_throughput(self, bandwidth):
        """
        Estimate throughput based on the current and historical bandwidth.
        :param bandwidth: Current available bandwidth in Mbps
        :return: Estimated throughput in Mbps
        """
        # Add the latest bandwidth sample to history
        self.throughput_history.append(bandwidth)

        # Limit the size of history (e.g., sliding window of 5 samples)
        if len(self.throughput_history) > self.sliding_window_size:
            self.throughput_history.pop(0)

        # Return the average of the history as the estimated throughput
        return sum(self.throughput_history) / len(self.throughput_history)

    def select_bitrate(self, bandwidth):
        """
        Select the highest bitrate that fits within the estimated throughput.
        :param bandwidth: Current available bandwidth (Mbps)
        :return: Selected bitrate (Mbps)
        """
        estimated_throughput = self.estimate_throughput(bandwidth)

        # Choose the highest bitrate <= estimated throughput
        # Assumption: self.bitrates is given in ascending order.
        for bitrate in reversed(self.bitrates):
            if bitrate <= estimated_throughput:
                return bitrate

        # If no bitrate fits, select the lowest available bitrate
        return min(self.bitrates)