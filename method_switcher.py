"""
    An example MethodSwitcher that can be used for future work. By looking
    at the test results of different methods we can talk about which
    method is useful in what kind of network condition. After that,
    using this method switcher, we can transition between different methods
    based on some heuristic that we form (based on our observations).
    This class is left as an example and will be discussed in the report
    thoroughly.
"""

CRITICAL_BUFFER_LEVEL = 4.0  # Seconds
BANDWIDTH_FLUCTUATION_THRESHOLD = 2.0  # Mbps

class MethodSwitcher:
    def __init__(self, bola_client, rate_based_client, pd_controller_client):
        self.bola = bola_client
        self.rate_based = rate_based_client
        self.pd_controller = pd_controller_client
        self.current_method = self.bola  # Start with BOLA by default

    def select_method(self, buffer_level, bandwidth, prev_bandwidth):
        """
        Decide which method to use based on current conditions.
        :param buffer_level: Current buffer level in seconds
        :param bandwidth: Current available bandwidth in Mbps
        :param prev_bandwidth
        """
        bandwidth_change = abs(bandwidth - prev_bandwidth)

        if buffer_level < CRITICAL_BUFFER_LEVEL:
            self.current_method = self.pd_controller
        elif bandwidth_change > BANDWIDTH_FLUCTUATION_THRESHOLD:
            self.current_method = self.rate_based
        else:  # Everything is stable.
            self.current_method = self.bola

    def select_bitrate(self, buffer_level, bandwidth, prev_bandwidth):
        """
        Select bitrate using the currently chosen method.
        """
        self.select_method(buffer_level, bandwidth, prev_bandwidth)
        return self.current_method.select_bitrate(bandwidth)