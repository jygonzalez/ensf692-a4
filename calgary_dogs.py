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
    # Start a loop for user input to ensure valid breed input is given
    while True:
        # Prompt the user to input a dog breed
        breed = input("Please enter a dog breed: ")
        # Convert the breed input to uppercase and remove leading/trailing spaces
        breed = breed.upper().strip()

        # Check if the entered breed exists in the dataset. If found, exit the loop
        if np.any(df['Breed'] == breed):
            break
      
        # 3. If breed is not found, raise a KeyError and start again
        try:
            raise KeyError
        except KeyError:
            print("Dog breed not found in the data. Please try again.")

    # Data anaylsis stage
    ## Multi-index Pandas DataFrame, index stack Breed > Year
    df = df.set_index(['Breed', 'Year'])

    # 1. Find and print all years where the selected breed was listed in the top breeds.
    ## Slice with found breed, then generate a list with the unique years
    str_list = [str(i) for i in df.loc[breed].index.unique()]
    ## Create a string of years separated by spaces
    unique_years = ' '.join(str_list)
    print(f"The {breed} was found in the top breeds for years: {unique_years}")

    # 2. Calculate and print the total number of registrations of the selected breed.
    ## Slice with found breed, then sum Total column to get total registries
    breed_total_registries = df.loc[breed].Total.sum()
    print(f"There have been {breed_total_registries} {
          breed} dogs registered total.")

    # 3. Calculate and print the percentage of selected breed registrations out of
    # the total percentage for each year it is found.
    ## Sum the 'Total' column for the breed, grouped by 'Year'
    breed_registries_per_year = df.loc[(breed, slice(None)), [
        'Total']].groupby('Year').sum()
    ## Sum the 'Total' column for all breeds, grouped by 'Year'
    total_registries_per_year = df.loc[(), [
        'Total']].groupby('Year').sum()

    # Iterate through each year to calculate and print the percentage for the breed
    for year in breed_registries_per_year.index:
        # Get the total registrations for the breed for the year
        my_breed = breed_registries_per_year.loc[year]['Total']
        # Get the total registrations for all breeds for the year
        all_breeds = total_registries_per_year.loc[year]['Total']
        # Calculate the percentage of registrations for the breed
        percentage = (my_breed / all_breeds) * 100
        print(f"The {breed} was {percentage:.6f}% of top breeds in {year}.")

    # 4. Calculate and print the percentage of selected breed registrations out of the total
    # three-year percentage.
    ## Get the total registrations for all breeds across all years
    total_registries = df.Total.sum()
    ## Calculate the percentage for the breed across all years
    percentage_in_all_years = (breed_total_registries / total_registries) * 100
    print(f"The {breed} was {
          percentage_in_all_years:.6f}% of top breeds across all years.")

    # 5. Find and print the months that were most popular for the selected breed registrations.
    # Print all months that tie.
    ## Count the number of registrations for the breed, grouped by 'Month'
    month_counts = df.loc[breed].groupby('Month').count()
    ## Find the maximum count of registrations in a month
    max_count = np.max(month_counts.values.astype(int))
    ## Create a mask for months that have the maximum count of registrations
    mask_max_count = month_counts.values == max_count
    ## Create a list of months that have the maximum count
    breed_popmonths_list = list(
        month for month in month_counts[mask_max_count].index)
    ## Create a string of popular months separated by spaces
    breed_popmonths = ' '.join(breed_popmonths_list)
    print(f"Most popular month(s) for {breed} dogs: {breed_popmonths}")


if __name__ == '__main__':
    main()
