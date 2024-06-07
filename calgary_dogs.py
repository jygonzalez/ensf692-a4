"""
    calgary_dogs.py
    Author: Yael Gonzalez

    A terminal-based application for computing and printing statistics based on given input.
    Detailed specifications are provided via the Assignment 4 README file.
    You must include the main listed below. You may add your own additional classes, 
    functions, variables, etc. 
    You may import any modules from the standard Python library.
    Remember to include docstrings and comments.

* Stage 1: DataFrame Creation
  1. Import the provided data into a Pandas DataFrame. 
  2. You may not change or sort the Excel file.
  3. You may not hard-code/copy-paste any information into your program 
  except for the expected years and column header names.
  4. You may index the information in any way.

* Stage 2: User Entry
  1. Prompt the user to enter a dog breed.
  2. If the name does not exist within the given data, raise a KeyError to print 
  “Dog breed not found in the data. Please try again.” 
  3. Users should be prompted continually until a correct input is provided.
  4. As long as the entry is spelled correctly, your program should accept entries in uppercase, 
  lowercase, camel case, and mixed case.
  5. You may assume that the user knows how the breed names are identified in the database.
  6. After successful data entry and analysis, your program should end.

* Stage 3: Data Analysis
  1. Find and print all years where the selected breed was listed in the top breeds.
  2. Calculate and print the total number of registrations of the selected breed.
  3. Calculate and print the percentage of selected breed registrations out of the total 
  percentage for each year (2021, 2022, 2023).
  4. Calculate and print the percentage of selected breed registrations out of the total 
  three-year percentage.
  5. Find and print the months that were most popular for the selected breed registrations. 
  Print all months that tie.
"""
import numpy as np
import pandas as pd


def main():

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
    df_reindexed = df.set_index(['Breed', 'Year'])

    # 1. Find and print all years where the selected breed was listed in the top breeds.
    str_list = [str(i) for i in df_reindexed.loc[breed, :].index.unique()]
    unique_years = ' '.join(str_list)
    print(f"The {breed} was found in the top breeds for years: {unique_years}")

    # 2. Calculate and print the total number of registrations of the selected breed.
    breed_total_registries = df_reindexed.loc[breed, :].Total.sum()
    print(f"There have been {breed_total_registries} {
          breed} dogs registered total.")

    #  3. Calculate and print the percentage of selected breed registrations out of
    # the total percentage for each year (2021, 2022, 2023).
    breed_registries_per_year = df_reindexed.loc[(breed, slice(None)), [
        'Total']].groupby('Year').sum()
    
    total_registries_per_year = df_reindexed.loc[(), [
        'Total']].groupby('Year').sum()

    for year in breed_registries_per_year.index:
        breed_count = breed_registries_per_year.loc[year]['Total']
        total_count = total_registries_per_year.loc[year]['Total']
        percentage = (breed_count / total_count) * 100
        print(f"The {breed} was {percentage:.6f}% of top breeds in {year}.")

    # 4. Calculate and print the percentage of selected breed registrations out of the total
    # three-year percentage.
    total_registries = df_reindexed.Total.sum()
    percentage_in_all_years = (breed_total_registries / total_registries) * 100
    print(f"The {breed} was {
          percentage_in_all_years:.6f}% of top breeds across all years.")

    # 5. Find and print the months that were most popular for the selected breed registrations.
    # Print all months that tie.
    month_counts = df_reindexed.loc[breed].groupby('Month').count()
    max_count = np.max(month_counts.values.astype(int))
    mask_max_count = month_counts.values == max_count
    breed_popmonths_list = list(
        month for month in month_counts[mask_max_count].index)
    breed_popmonths = ' '.join(breed_popmonths_list)
    print(f"Most popular month(s) for {breed} dogs: {breed_popmonths}")


if __name__ == '__main__':
    main()
