import datetime as dt
import pandas as pd
import os

print("Looking For TIMESTAMPS")
try:
    df = pd.read_csv("..{}data{}KaDo_Timestamps.csv".format(os.sep, os.sep),
                     sep=",")
    print("TIMESTAMPS Found")
except:
    print("Creating TIMESTAMPS")
    df = pd.read_csv("..{}data{}KaDo.csv".format(os.sep, os.sep), sep=",")

    df["timestamps"] = df["MOIS_VENTE"].apply(lambda x: dt.datetime.strptime(
        "2020-{}-01 12:50:00".format(x), "%Y-%m-%d %H:%M:%S").timestamp())
    df = df.assign(QUANTITY=lambda x: 1)

    df.to_csv("..{}data{}KaDo_Timestamps.csv".format(os.sep, os.sep),
              sep=",",
              index=False)
    print("TIMESTAMPS Created")

print("Looking for DUPLICATES")
try:
    df_duplicates = pd.read_csv("..{}data{}KaDo_Duplicates.csv".format(
        os.sep, os.sep),
                                sep=",")
    print("DUPLICATES Found")
except:
    print("Creating DUPLICATES")
    df_duplicates = pd.read_csv("..{}data{}KaDo_Timestamps.csv".format(
        os.sep, os.sep),
                                sep=",")
    df_duplicates = df_duplicates.drop_duplicates(
        subset=["FAMILLE", "UNIVERS", "MAILLE", "LIBELLE", "TICKET_ID"])
    df_duplicates.to_csv("..{}data{}KaDo_Duplicates.csv".format(
        os.sep, os.sep),
                         sep=",",
                         index=False)
    print("DUPLICATES Created")

print("Looking For PRODUCTS IDS")
try:
    df_products = pd.read_csv("..{}data{}Products_ids.csv".format(
        os.sep, os.sep),
                              sep=",")
    print("PRODUCTS IDS Found")
except:
    print("Creating PRODUCTS IDS")
    CATEGORIES = []

    CATEGORIES.extend(df["FAMILLE"].unique().tolist())
    CATEGORIES.extend(df["MAILLE"].unique().tolist())
    CATEGORIES.extend(df["UNIVERS"].unique().tolist())
    CATEGORIES.extend(df["TICKET_ID"].unique().tolist())
    CATEGORIES.extend(df["LIBELLE"].unique().tolist())

    CATEGORIES = list(dict.fromkeys(CATEGORIES))

    df["ITEM_ID"] = pd.Categorical(df["LIBELLE"], categories=CATEGORIES)
    df["ITEM_ID"] = df["ITEM_ID"].cat.codes

    df_products = df.copy()
    df_products = df_products[["LIBELLE", "ITEM_ID"]]

    df_products.drop_duplicates(inplace=True)

    df_products.to_csv("..{}data{}Products_ids.csv".format(os.sep, os.sep),
                       sep=",",
                       index=False)
    print("PRODUCTS IDS Created")

# print("Looking For RFM")
# try:
#     rfm = pd.read_csv("..{}data{}RFM.csv".format(os.sep, os.sep))
#     print("RFM Found")
# except:
#     print("Creating RFM")
#     PRESENT = dt.datetime(2022, 1, 1)

#     filtered_data = df.copy()
#     filtered_data = filtered_data[[
#         "CLI_ID", "MOIS_VENTE", "TICKET_ID", "QUANTITY", "PRIX_NET"
#     ]]
#     filtered_data["MOIS_VENTE"] = pd.to_datetime(filtered_data["MOIS_VENTE"])

#     rfm = filtered_data.groupby("CLI_ID").agg({
#         "MOIS_VENTE":
#         lambda date: (PRESENT - date.max()).days,
#         "TICKET_ID":
#         lambda num: len(num),
#         "PRIX_NET":
#         lambda price: price.sum()
#     })

#     rfm.rename(columns={
#         "PRIX_NET": "monetary",
#         "TICKET_ID": "frequency",
#         "MOIS_VENTE": "recency"
#     },
#                inplace=True)
#     rfm["recency"] = rfm["recency"].astype(int)
#     rfm['r_quartile'] = pd.qcut(rfm['recency'],
#                                 q=3,
#                                 labels=['1', '2', '3'],
#                                 duplicates='drop')
#     rfm["f_quartile"] = pd.qcut(rfm["frequency"],
#                                 q=3,
#                                 labels=['3', '2', '1'],
#                                 duplicates='drop')
#     rfm["m_quartile"] = pd.qcut(rfm["monetary"],
#                                 q=3,
#                                 labels=['3', '2', '1'],
#                                 duplicates='drop')

#     rfm["RFM_Score"] = rfm.r_quartile.astype(str) + rfm.f_quartile.astype(
#         str) + rfm.m_quartile.astype(str)

#     rfm_display = rfm.copy()

#     rfm_display["recency"] = rfm_display["recency"] / 30
#     rfm_display["recency"] = round(rfm_display["recency"], 0).astype(int)

#     rfm_display = rfm_display.sort_values("recency")
#     rfm_display.to_csv("..{}data{}RFM.csv".format(os.sep, os.sep),
#                        sep=",",
#                        index=False)
#     print("RFM Created")
