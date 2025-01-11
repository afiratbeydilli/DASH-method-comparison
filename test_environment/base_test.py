"""
    Base class for test methods that are going to be applied.
    Below attributes are common among all the tests.
"""
class BaseTest:
    def __init__(self, segment_duration, playback_rate):
        """
        Base class for test environments.
        :param segment_duration: Duration of each video segment in seconds -> Fixed in DASH
        :param playback_rate:  Video playback rate in seconds per second (1x, 1.5x etc.)
        """
        self.segment_duration = segment_duration  # Fixed segment duration
        self.playback_rate = playback_rate  # Video playback rate

    def update_buffer(self, client, bandwidth, bitrate):
        """
        Simulates downloading a segment and updating the buffer.
        :param client: The client object
        :param bandwidth: Available bandwidth in Mbps
        :param bitrate: Selected bitrate in Mbps
        """
        # Calculate the time taken to download the segment
        download_time = bitrate / bandwidth

        # Buffer change: Segment duration minus download time
        buffer_change = self.segment_duration - download_time
        client.buffer_size += buffer_change

        # Simulate buffer consumption
        if client.buffer_size <= 0:
            print(f"Playback stalled at time {t} seconds.")
            client.buffer_size = 0
        else:
            client.buffer_size -= self.playback_rate

        client.buffer_size = max(0, min(client.buffer_size, client.max_buffer))  # Clamp buffer

    @staticmethod
    def calculate_metrics(bitrates, buffer_levels):
        """
        Static method that calculates the performance metrics of the clients, which
        can be used in their comparison.
        :param bitrates: List of bitrates selected over time (by the client)
        :param buffer_levels: List of buffer levels over time (of the client)
        :return: Dictionary of metrics
        """
        # Average bitrate
        avg_bitrate = sum(bitrates) / len(bitrates)

        # Bitrate switch count
        bitrate_switch_count = sum(
            1 for i in range(1, len(bitrates)) if bitrates[i] != bitrates[i - 1]
        )

        # Rebuffering events
        rebuffer_count = sum(1 for buffer in buffer_levels if buffer == 0)

        return {
            "Average Bitrate": avg_bitrate,
            "Bitrate Switch Count": bitrate_switch_count,
            "Rebuffering Events": rebuffer_count,
        }