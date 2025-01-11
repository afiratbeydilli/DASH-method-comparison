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
    def plot_time_series(data, labels, title, xlabel, ylabel):
        """
        :param data: List of lists, where each inner list is a time series
        :param labels: List of labels for each time series
        :param title:
        :param xlabel:
        :param ylabel:
        """
        plt.figure(figsize=(12, 6))
        for i, series in enumerate(data):
            plt.plot(series, label=labels[i])
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend()
        plt.show()