import matplotlib.pyplot as plt
import numpy as np

class CarDataVisualizer:
    """
    A class to visualize car data using Matplotlib.

    Attributes:
        df (pandas.DataFrame): The DataFrame containing the car data.
        specified_makes (list): A list of specific makes to visualize.

    Methods:
        visualize_data(): Generates scatter plots for selling price vs. odometer for specified makes.
    """

    def __init__(self, df, specified_makes):
        """
        Initialize the CarDataVisualizer instance.

        Args:
            df (pandas.DataFrame): The DataFrame containing the car data.
            specified_makes (list): A list of specific makes to visualize.
        """
        self.df = df
        self.specified_makes = specified_makes

    def visualize_data(self):
        """
        Generate scatter plots for selling price vs. odometer for specified makes.
        """
        # Determine the number of rows needed based on the number of specified makes
        num_rows = len(self.specified_makes) // 2 + len(self.specified_makes) % 2

        # Create subplots
        fig, axes = plt.subplots(num_rows, 2, figsize=(10, 5 * num_rows), sharey=True)

        # Define colors for 'automatic' and 'manual' transmissions
        transmission_colors = {'automatic': 'blue', 'manual': 'green'}

        # Iterate over specified makes
        for i, make in enumerate(self.specified_makes):
            # Calculate the subplot indices
            row_index = i // 2
            col_index = i % 2

            # Filter data for the current make
            make_data = self.df[self.df['make'] == make]

            # Scatter plot for the current make
            ax = axes[row_index, col_index]
            for transmission, color in transmission_colors.items():
                transmission_data = make_data[make_data['transmission'] == transmission]
                ax.scatter(transmission_data['odometer'], transmission_data['sellingprice'], c=color, label=transmission, alpha=0.8, s=10)
            ax.set_xlabel('Odometer')
            ax.set_ylabel('Selling Price')
            ax.set_title(f'{make} - Selling Price vs Odometer')
            ax.grid(True)
            ax.legend(title='Transmission')

        # If the number of specified makes is odd, remove the last subplot in the last row
        if len(self.specified_makes) % 2 == 1:
            fig.delaxes(axes[num_rows - 1, 1])

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    from retrieve_neo4j import df
    specified_makes = ['Ford', 'Chevrolet', 'Nissan', 'Toyota']
    visualizer = CarDataVisualizer(df, specified_makes)
    visualizer.visualize_data()