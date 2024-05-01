import matplotlib.pyplot as plt

class CarDataVisualizer:
    """
    A class to visualize car data using Matplotlib.

    Attributes:
        df (pandas.DataFrame): The DataFrame containing the car data.

    Methods:
        visualize_data(): Generates plots for top makes, body types, and average selling prices.
    """

    def __init__(self, df):
        """
        Initialize the CarDataVisualizer instance.

        Args:
            df (pandas.DataFrame): The DataFrame containing the car data.
        """
        self.df = df
        self.preprocess_data()

    def preprocess_data(self):
        """
        Preprocess the data by converting the "body" column values to lowercase.
        """
        self.df['body'] = self.df['body'].str.lower()

    def visualize_data(self):
        """
        Generate plots for top makes, body types, and average selling prices.
        """
        # Get top 5 makes based on the number of cars
        top_makes = self.df['make'].value_counts().head(5).index

        # Create subplots
        fig, axes = plt.subplots(3, 2, figsize=(15, 10))
        axes = axes.ravel()  # Flatten the axes array for easy indexing

        # Plot 1: Top 5 makes
        ax = axes[0]
        ax.bar(top_makes, self.df[self.df['make'].isin(top_makes)]['make'].value_counts(), color='navy')
        ax.set_title('Top 5 Makes')
        ax.set_xlabel('Make')
        ax.set_ylabel('Number of Cars')

        # Subplots for top 5 body types and their average selling prices for each make
        for i, make in enumerate(top_makes, start=1):
            ax = axes[i]
            make_data = self.df[self.df['make'] == make]
            top_body_types = make_data['body'].value_counts().head(5).index
            # Combine occurrences of "Sedan" and "sedan"
            top_body_types = [body.capitalize() for body in top_body_types]
            body_avg_prices = [make_data[make_data['body'] == body.lower()]['sellingprice'].mean() for body in top_body_types]
            sorted_body_avg_prices, sorted_top_body_types = zip(*sorted(zip(body_avg_prices, top_body_types), reverse=True))
            ax.bar(sorted_top_body_types, sorted_body_avg_prices, color='skyblue')
            ax.set_title(f'{make} - Top 5 Body Types and Average Selling Prices')
            ax.set_xlabel('Body Type')
            ax.set_ylabel('Average Selling Price')

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    from retrieve_neo4j import df
    visualizer = CarDataVisualizer(df)
    visualizer.visualize_data()