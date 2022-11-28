from wc_predict import load_data

if __name__ == '__main__':
    df = load_data()
    print(df)
    print(sorted(set(df.loc[:, 'home_team'])))