import matplotlib.pyplot as plt

"""
    Class that will be used in the visualization of the given metrics.
"""
class Plotter:
    @staticmethod
    def plot_metric(metric_name, scenario_name, results):
        """
        :param metric_name: Name of the metric to plot (ex: "Average Bitrate")
        :param scenario_name: Name of the scenario (ex: "Constant Bandwidth")
        :param results: Dictionary of results for all methods -> Compliant with what 'BaseTest' produces.
        """
        methods = results.keys()
        metric_values = [results[method][metric_name] for method in methods]

        plt.figure(figsize=(10, 6))
        plt.bar(methods, metric_values, color=['blue', 'green', 'orange'])
        plt.title(f"{metric_name} Comparison - {scenario_name}")
        plt.xlabel("Methods")
        plt.ylabel(metric_name)
        plt.show()

    @staticmethod
    def plot_individual_object(results, title="Test Results"):
        """
        :param results: The results dictionary from the simulation
        :param title
        """
        time = len(results["bandwidth"])
        plt.figure(figsize=(12, 6))
        plt.plot(range(time), results["bandwidth"], label="Bandwidth (Mbps)", linestyle="--", linewidth=2)
        plt.plot(range(time), results["bitrates"], label="Selected Bitrate (Mbps)", marker="o", linewidth=1.5)
        plt.plot(range(time), results["buffer_levels"], label="Buffer Level (s)", marker="x", linewidth=1.5)
        plt.title(title)
        plt.xlabel("Time (s)")
        plt.ylabel("Value")
        plt.legend()
        plt.grid(True)
        plt.show()