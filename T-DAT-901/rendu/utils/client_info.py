import datetime as dt
import pandas as pd
import numpy as np
import argparse
import os


class ClientInfo():
    def __init__(self, client_id):
        self.client_id = client_id

        self.df = pd.read_csv("..{}data{}KaDo.csv".format(os.sep, os.sep),
                              sep=',')
        self.df_all = self.df.copy()
        self.df = self.df[self.df["CLI_ID"] == client_id]

        if self.df.empty:
            print("Invalid client ID")

    def get_client_data(self):
        self.client_data = self.__set_client_info__()

        return self.client_data

    def get_client_id(self):
        return self.client_id

    def get_rfm(self):
        rfm_df = pd.read_csv("..{}data{}RFM_client.csv".format(os.sep, os.sep),
                             sep=',')

        rfm_client = rfm_df[rfm_df["CLI_ID"] == self.client_id]
        rfm_client.set_index("CLI_ID", drop=True, inplace=True)
        # PRESENT = dt.datetime(2022, 1, 1)

        # filtered_data = self.df_all.copy()
        # filtered_data = filtered_data[[
        #     "CLI_ID", "MOIS_VENTE", "TICKET_ID", "PRIX_NET"
        # ]]

        # filtered_data["MOIS_VENTE"] = filtered_data["MOIS_VENTE"].apply(
        #     lambda x: "2021-{}-01 12:50:00".format(x))
        # filtered_data = filtered_data.assign(QUANTITY=lambda x: 1)

        # filtered_data["MOIS_VENTE"] = pd.to_datetime(
        #     filtered_data["MOIS_VENTE"])

        # rfm = filtered_data.groupby("CLI_ID").agg({
        #     "MOIS_VENTE":
        #     lambda date: (PRESENT - date.max()).days,
        #     "TICKET_ID":
        #     lambda num: len(num),
        #     "PRIX_NET":
        #     lambda price: price.sum()
        # })

        # rfm.rename(columns={
        #     "PRIX_NET": "monetary",
        #     "TICKET_ID": "frequency",
        #     "MOIS_VENTE": "recency"
        # },
        #            inplace=True)
        # rfm["recency"] = rfm["recency"].astype(int)

        # rfm['r_quartile'] = pd.qcut(rfm['recency'],
        #                             3, ['1', '2', '3'],
        #                             duplicates='drop')
        # rfm["f_quartile"] = pd.qcut(rfm["frequency"],
        #                             3, ['3', '2', '1'],
        #                             duplicates='drop')
        # rfm["m_quartile"] = pd.qcut(rfm["monetary"],
        #                             3, ['3', '2', '1'],
        #                             duplicates='drop')
        # rfm["RFM_Score"] = rfm.r_quartile.astype(str) + rfm.f_quartile.astype(
        #     str) + rfm.m_quartile.astype(str)
        # rfm.to_csv("..{}data{}RFM_client.csv".format(os.sep, os.sep), sep=',')

        # rfm_score = rfm["RFM_Score"][self.client_id]

        return rfm_client

    def __set_client_info__(self):
        data = {}

        data["all_ticket"] = len(self.df["TICKET_ID"].unique())
        data["all_items"] = self.df.shape[0]
        data['all_mean_price'] = np.round(self.df["PRIX_NET"].mean(), 2)
        data["all_mean_items"] = np.round(
            self.df.groupby(['TICKET_ID'
                             ]).size().reset_index(name="count").sort_values(
                                 "count", ascending=False)["count"].mean(), 2)

        data["most_expensive_item"] = {}
        id_most_expensive = self.df["PRIX_NET"].idxmax()

        data["most_expensive_item"]["price"] = self.df["PRIX_NET"].max()
        data["most_expensive_item"]["id"] = id_most_expensive
        data["most_expensive_item"]["libelle"] = self.df["LIBELLE"][
            id_most_expensive]
        data["most_expensive_item"]["famille"] = self.df["FAMILLE"][
            id_most_expensive]
        data["most_expensive_item"]["maille"] = self.df["MAILLE"][
            id_most_expensive]
        data["most_expensive_item"]["univers"] = self.df["UNIVERS"][
            id_most_expensive]

        data["per_ticket"] = {}
        data["per_ticket"]["price"] = self.df.groupby(
            ["TICKET_ID"])["PRIX_NET"].sum().reset_index(
                name="PRIX_NET").apply(lambda x: np.round(x, 2)).sort_values(
                    "PRIX_NET", ascending=False)
        data["per_ticket"]["mean_price"] = self.df.groupby(
            ["TICKET_ID"])["PRIX_NET"].mean().reset_index(
                name="PRIX_NET").apply(lambda x: np.round(x, 2)).sort_values(
                    "PRIX_NET", ascending=False)

        data["per_ticket"]["nbr_items"] = self.df.groupby([
            "TICKET_ID"
        ]).size().reset_index(name="count").sort_values("count",
                                                        ascending=False)

        return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Client Data")
    parser.add_argument(
        "-i",
        "--client-id",
        type=int,
        required=True,
        help="Client Id",
    )
    parser.add_argument(
        "-r",
        "--rfm",
        action='store_true',
        dest="rfm",
        help="RFM Score",
    )
    parser.add_argument(
        "-d",
        "--data",
        action='store_true',
        dest="data",
        help="Client Data",
    )

    args = parser.parse_args()

    client = ClientInfo(args.client_id)

    print("CLIENT ID: {}".format(client.get_client_id()))
    if args.data:
        print(client.get_client_data())
    if args.rfm:
        print(client.get_rfm())
