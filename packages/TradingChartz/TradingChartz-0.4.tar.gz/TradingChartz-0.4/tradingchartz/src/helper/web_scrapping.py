# external standard
import pandas as pd


def read_csv_from_web_as_df(csv_web_url: str) -> pd.DataFrame:
    """
    Reads csv web url adn returns pandas dataframe
    :param csv_web_url: complete url for csv
    :return: pd.Dataframe with csv data
    """
    return pd.read_csv(csv_web_url)
