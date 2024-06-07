"""
    calgary_dogs.py
    Author: Yael Gonzalez

    A terminal-based application for computing and printing statistics based on given input.
    Detailed specifications are provided via the Assignment 4 README file.
    You must include the main listed below. You may add your own additional classes, 
    functions, variables, etc. 
    You may import any modules from the standard Python library.
    Remember to include docstrings and comments.
"""

# TODO: Add comments throughout the code to explain the functionality
# TODO: Review variable names are clear and 
import numpy as np
import pandas as pd


def main():
    """
    Main function to execute the program and print dogs statistics.
    """

    # Import data here
    df = pd.read_excel("CalgaryDogBreeds.xlsx")

    print("ENSF 692 Dogs of Calgary")

    # User input stage
    while True:
        breed = input("Please enter a dog breed: ")
        breed = breed.upper().strip()

        if np.any(df['Breed'] == breed):
            break

        try:
            raise KeyError
        except KeyError:
            print("Dog breed not found in the data. Please try again.")

    # Data anaylsis stage
    # multi-index Pandas DataFrame
    df = df.set_index(['Breed', 'Year'])

    # 1. Find and print all years where the selected breed was listed in the top breeds.
    str_list = [str(i) for i in df.loc[breed, :].index.unique()]
    unique_years = ' '.join(str_list)
    print(f"The {breed} was found in the top breeds for years: {unique_years}")

    # 2. Calculate and print the total number of registrations of the selected breed.
    breed_total_registries = df.loc[breed].Total.sum()
    print(f"There have been {breed_total_registries} {
          breed} dogs registered total.")

    #  3. Calculate and print the percentage of selected breed registrations out of
    # the total percentage for each year it is found.
    breed_registries_per_year = df.loc[(breed, slice(None)), [
        'Total']].groupby('Year').sum()

    total_registries_per_year = df.loc[(), [
        'Total']].groupby('Year').sum()

    for year in breed_registries_per_year.index:
        my_breed = breed_registries_per_year.loc[year]['Total']
        all_breeds = total_registries_per_year.loc[year]['Total']
        percentage = (my_breed / all_breeds) * 100
        print(f"The {breed} was {percentage:.6f}% of top breeds in {year}.")

    # 4. Calculate and print the percentage of selected breed registrations out of the total
    # three-year percentage.
    total_registries = df.Total.sum()
    percentage_in_all_years = (breed_total_registries / total_registries) * 100
    print(f"The {breed} was {
          percentage_in_all_years:.6f}% of top breeds across all years.")

    # 5. Find and print the months that were most popular for the selected breed registrations.
    # Print all months that tie.
    month_counts = df.loc[breed].groupby('Month').count()
    max_count = np.max(month_counts.values.astype(int))
    mask_max_count = month_counts.values == max_count
    breed_popmonths_list = list(
        month for month in month_counts[mask_max_count].index)
    breed_popmonths = ' '.join(breed_popmonths_list)
    print(f"Most popular month(s) for {breed} dogs: {breed_popmonths}")


if __name__ == '__main__':
    main()
