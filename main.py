import argparse
import pandas as pd
import os.path as op
import os
from re import search


def convert_tsv_to_csv(input_file_path: str, output_file: str):
    """Get a csv file format and return path to a tsv format
    :param input_file_path: path to tsv file
    :param output_file: name of converted file, *.csv (the file will be located in project directory)
    """

    csv_df = pd.read_csv(input_file_path, sep='\t')
    csv_df.to_csv(op.join(os.getcwd(), output_file), sep=',')


def add_column_to_csv_file(input_file_path: str, output_file: str):
    """Get a csv file format and add new column called 'price_edited'-
    contains float values of 'price' column
    :param input_file_path: path to csv file
    :param output_file: path to output file (the file will be located in project directory)
    """

    # read data from csv file to dataframe object
    csv_df = pd.read_csv(input_file_path, sep='\t')
    numeric_pattern = r'(\d*\.\d+|\d+)'
    # create a new column contain the numerical values from 'price' column, set type=float64
    csv_df["price_edited"] = csv_df["price"].str.extract(pat=numeric_pattern).astype("float64")
    csv_df.to_csv(op.join(os.getcwd(), output_file))


def regex_filter_by_given_values(input_file_path: str, output_file: str, include_item: str = "knit", exclude_item: str = "jumper"):
    """
    search for a substring in a string by using search method in re module
    :param input_file_path: path to csv file
    :param include_item: substring to look for
    :param exclude_item: substring to avoid
    :param output_file: path to output file (the file will be located in project directory)
    """

    csv_df = pd.read_csv(input_file_path)
    prepared_df = pd.DataFrame()
    for (index, row) in csv_df.iterrows():
        elem = row["product_name"].lower()
        if search(include_item, elem):
            if search(exclude_item, elem):
                continue
            prepared_df = prepared_df.append(row)
    prepared_df.to_csv(op.join(os.getcwd(), output_file))


def create_parser():
    parser = argparse.ArgumentParser(description='Syte task')
    parser.add_argument("-i", "--infile", type=str, required=True, help="Path to input file")
    parser.add_argument("-o", "--outfile", type=str, required=True, help="Path to output file")
    parser.add_argument("-op", "--operation", type=int, required=True, help="1-tsv to csv\n2-add new column\n3-regex")
    return parser.parse_args()


def perform_operations(arguments):
    """if you wish to execute first TSV to CSV task:
        --infile <feed.csv> --outfile <feed_mission1.csv> --operation 1
        --infile <feed.csv> --outfile <feed_mission2.csv> --operation 2
        --infile <feed_sample.csv> --outfile <regex.csv> --operation 3"""

    if op.exists(op.join(os.getcwd(), arguments.infile)):
        if arguments.operation == 1:
            convert_tsv_to_csv(op.join(os.getcwd(), arguments.infile), arguments.outfile)
        elif arguments.operation == 2:
            add_column_to_csv_file(op.join(os.getcwd(), arguments.infile), arguments.outfile)
        elif arguments.operation == 3:
            regex_filter_by_given_values(op.join(os.getcwd(), arguments.infile), arguments.outfile)

    else:
        print(f"File: {op.join(os.getcwd(), arguments.infile)} does not exists!")


if __name__ == "__main__":
    args = create_parser()
    perform_operations(args)

# regex_filter_by_given_values("C:\\Users\Zehavit\PycharmProjects\syteTask\\feed_sample.csv")