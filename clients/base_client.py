# Note : [360p, 480p, 720p, 1080p, 1440p, 4K] <=> [1 2 4 6 8 12]Mbps
"""
    Base client methods that should be specialized in the derived classes.
"""
class BaseClient:
    def __init__(self, bitrates, max_buffer, buffer_size):
        """
        Base properties for a streaming client.
        :param bitrates: List of available bitrates in Mbps (e.g., [1, 2, 4, 6, 8, 12])
        :param max_buffer: Maximum buffer size in seconds
        """
        self.bitrates = bitrates
        self.max_buffer = max_buffer
        self.buffer_size = buffer_size

    def select_bitrate(self, bandwidth):
        """
        The derived classes must implement a method (their own method) to select a bitrate,
        which corresponds to DASH rate selection method.
        :param bandwidth: Current available bandwidth in Mbps
        :return: Selected bitrate in Mbps
        """
        raise NotImplementedError("This method should be implemented by subclasses.")