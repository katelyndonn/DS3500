import sankey as sk
import pandas as pd


def main():
    # reading in the json file as a dateframe
    df = pd.read_json('Artists.json')

    # making a column for the decade
    df['Decade'] = (df['BeginDate'] // 10) * 10

    # Step 1
    # making a dataframe from the existing one,
    # but only with the columns we want
    # (Nationality, Gender, and Decade)
    df = df[['Nationality', 'Gender', 'Decade']]

    # Step 5
    # sankey with Nationality on left and Decade on right
    sankey5 = sk.make_sankey(df, 'Nationality', 'Decade')

    # Step 6
    # sankey with Nationality on left and Gender on right
    sankey6 = sk.make_sankey(df, 'Nationality', 'Gender')

    # Step 7
    # sankey with Gender on left and Decade on right
    sankey7 = sk.make_sankey(df, 'Gender', 'Decade')

    # Step 8
    # multilayered sankey
    stacked_sankey = sk.make_sankey(df, 'Nationality', 'Gender', 'Decade')


if __name__ == '__main__':
    main()
