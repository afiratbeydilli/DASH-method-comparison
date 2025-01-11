from test_environment.single_client_test import SingleClientTest
from clients.bola_client import BOLAClient
from clients.rate_based_client import RateBasedMethodClient
from clients.pd_controller_client import PDControllerClient
from utils.plotter import Plotter
import numpy as np

def compare_methods(segment_duration=2.0, playback_rate=1, max_buffer=20, bitrates=[1, 2, 4, 6, 8, 12], time_ticks=20):
    """
        Compare BOLA, Rate-Based, and PD Controller methods across scenarios.
        Collect metrics and generate comparison plots.
    """
    # Define bandwidth patterns
    constant_bandwidth = [5] * time_ticks  # Constant 5 Mbps
    fluctuating_bandwidth = 5 + 2 * np.sin(np.linspace(0, 2 * np.pi, time_ticks))  # Sinusoidal pattern
    random_bandwidth = np.random.uniform(2, 8, time_ticks).tolist()  # Random between 2 and 8 Mbps

    scenarios = {
        "Constant Bandwidth": constant_bandwidth,
        "Fluctuating Bandwidth": fluctuating_bandwidth,
        "Random Bandwidth": random_bandwidth,
    }

    # Initialize clients
    bola_client = BOLAClient(bitrates, max_buffer, buffer_size=max_buffer/4)
    rate_based_client = RateBasedMethodClient(bitrates, max_buffer, buffer_size=max_buffer/4)
    pd_controller_client = PDControllerClient(bitrates, max_buffer, buffer_size=max_buffer/4,
                                              bk1=2.0, bk2=6.0, T=segment_duration, eta=1.5)

    clients = {
        "BOLA": bola_client,
        "Rate-Based": rate_based_client,
        "PD Controller": pd_controller_client,
    }

    # Results storage
    all_results = {}

    for scenario_name, bandwidth_pattern in scenarios.items():
        print(f"Testing scenario: {scenario_name}")
        all_results[scenario_name] = {}

        for client_name, client in clients.items():
            print(f"  Running test for: {client_name}")

            # Run the single-client test
            test = SingleClientTest(segment_duration, playback_rate)
            result = test.run_test(client, bandwidth_pattern, time_ticks)

            # Collect metrics
            metrics = result["metrics"]
            all_results[scenario_name][client_name] = metrics

            # Plot individual object results.
            Plotter.plot_individual_object(result, title=f"{scenario_name} - {client_name}")

        # Plot metrics for this scenario
        for metric_name in ["Average Bitrate", "Bitrate Switch Count", "Rebuffering Events"]:
            Plotter.plot_metric(metric_name, scenario_name, all_results[scenario_name])

    return all_results