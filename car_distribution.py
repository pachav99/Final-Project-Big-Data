import matplotlib.pyplot as plt
import numpy as np
from retrieve_neo4j import df  # Import the DataFrame from the retrieve_neo4j module

class StateAnalysis:
    """
    A class for analyzing the distribution of cars by state and their average selling prices.

    Attributes:
        df (pandas.DataFrame): The input DataFrame containing car data.

    Methods:
        plot_state_analysis(): Plots the number of cars and average selling prices for each state.
    """

    def __init__(self, df):
        """
        Initializes the StateAnalysis class.

        Args:
            df (pandas.DataFrame): The input DataFrame containing car data.
        """
        self.df = df

    def plot_state_analysis(self):
        """
        Plots the number of cars and average selling prices for each state.

        Returns:
            None
        """
        # Calculate state counts
        state_counts = self.df.loc[~self.df['state'].str.startswith('3'), 'state'].value_counts().head(10)

        # Calculate average selling prices for each state
        state_avg_prices = self.df.groupby('state')['sellingprice'].mean().loc[state_counts.index]

        # Create a line plot
        plt.figure(figsize=(10, 6))

        # Plot state counts
        plt.plot(state_counts.index, state_counts.values, label='Number of Cars')

        # Plot average selling prices
        plt.plot(state_avg_prices.index, state_avg_prices.values, color='red', label='Average Selling Price')

        plt.xticks(rotation=0)
        plt.xlabel('State', fontsize=14)
        plt.ylabel('Number of Cars / Average Selling Price', fontsize=14)
        plt.title('Distribution of Cars by State', fontsize=16)
        plt.legend()
        plt.show()

# Example usage
state_analysis = StateAnalysis(df)
state_analysis.plot_state_analysis()