from test_environment.base_test import BaseTest
"""
    Based on given bandwidth pattern, tests the client's properties.
    The evaluated metrics are given in the base class. This class just
    conducts the test, saves the results and uses the method given in the
    base class to produce our final report (output).
"""
class SingleClientTest(BaseTest):
    def __init__(self, segment_duration, playback_rate):
        super().__init__(segment_duration, playback_rate)

    def run_test(self, client, bandwidth_pattern, time=30):
        """
        :param client: Streaming client (BOLAClient, PDControllerClient)
        :param bandwidth_pattern: List of bandwidth values over time
        :param time: Simulation duration in seconds
        :return: Results as a dictionary (bitrates, buffer levels, bandwidth, metrics)
        """
        selected_bitrates = []
        buffer_levels = []

        for t in range(time):
            # Get the bandwidth for the current time step
            bandwidth = bandwidth_pattern[t]

            # Select the bitrate using the client's logic
            bitrate = client.select_bitrate(bandwidth)

            # Update the buffer state
            self.update_buffer(client, bandwidth, bitrate)

            # Store results for analysis
            selected_bitrates.append(bitrate)
            buffer_levels.append(client.buffer_size)

        # Calculate metrics
        metrics = self.calculate_metrics(selected_bitrates, buffer_levels)

        return {
            "bitrates": selected_bitrates,
            "buffer_levels": buffer_levels,
            "bandwidth": bandwidth_pattern,
            "metrics": metrics,
        }