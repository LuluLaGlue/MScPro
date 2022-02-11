import streamlit as st
import datetime as dt
import pandas as pd
import numpy as np
import pickle
import os

st.set_page_config(layout="wide")


def saveRFM(data):
    PRESENT = dt.datetime(2022, 1, 1)

    filtered_data = data.copy()
    filtered_data = filtered_data[[
        "CLI_ID", "MOIS_VENTE", "TICKET_ID", "QUANTITY", "PRIX_NET"
    ]]
    filtered_data["MOIS_VENTE"] = pd.to_datetime(filtered_data["MOIS_VENTE"])

    rfm = filtered_data.groupby("CLI_ID").agg({
        "MOIS_VENTE":
        lambda date: (PRESENT - date.max()).days,
        "TICKET_ID":
        lambda num: len(num),
        "PRIX_NET":
        lambda price: price.sum()
    })

    rfm.rename(columns={
        "PRIX_NET": "monetary",
        "TICKET_ID": "frequency",
        "MOIS_VENTE": "recency"
    },
               inplace=True)
    rfm["recency"] = rfm["recency"].astype(int)
    rfm['r_quartile'] = pd.qcut(rfm['recency'],
                                3, ['1', '2', '3'],
                                duplicates='drop')
    rfm["f_quartile"] = pd.qcut(rfm["frequency"],
                                3, ['3', '2', '1'],
                                duplicates='drop')
    rfm["m_quartile"] = pd.qcut(rfm["monetary"],
                                3, ['3', '2', '1'],
                                duplicates='drop')

    rfm["RFM_Score"] = rfm.r_quartile.astype(str) + rfm.f_quartile.astype(
        str) + rfm.m_quartile.astype(str)

    rfm_display = rfm.copy()

    rfm_display["recency"] = rfm_display["recency"] / 30
    rfm_display["recency"] = round(rfm_display["recency"], 0).astype(int)

    rfm_display = rfm_display.sort_values("recency")
    rfm_display.to_csv("data{}RFM_client.csv".format(os.sep), sep=",")


def save_products():
    try:
        df = pd.read_csv("data{}KaDo_Timestamps.csv".format(os.sep), sep=",")
    except:
        df = pd.read_csv("data{}KaDo.csv".format(os.sep), sep=",")

        df["timestamps"] = df["MOIS_VENTE"].apply(
            lambda x: dt.datetime.strptime("2020-{}-01 12:50:00".format(x),
                                           "%Y-%m-%d %H:%M:%S").timestamp())

        df.to_csv("data{}KaDo_Timestamps.csv".format(os.sep),
                  sep=",",
                  index=False)

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

    df_products.to_csv("data{}Products_ids.csv".format(os.sep),
                       sep=",",
                       index=False)


@st.cache
def get_rfm(df):
    PRESENT = dt.datetime(2022, 1, 1)

    filtered_data = df.copy()
    filtered_data = filtered_data[[
        "CLI_ID", "MOIS_VENTE", "TICKET_ID", "QUANTITY", "PRIX_NET"
    ]]
    filtered_data["MOIS_VENTE"] = pd.to_datetime(filtered_data["MOIS_VENTE"])

    rfm = filtered_data.groupby("CLI_ID").agg({
        "MOIS_VENTE":
        lambda date: (PRESENT - date.max()).days,
        "TICKET_ID":
        lambda num: len(num),
        "PRIX_NET":
        lambda price: price.sum()
    })

    rfm.rename(columns={
        "PRIX_NET": "monetary",
        "TICKET_ID": "frequency",
        "MOIS_VENTE": "recency"
    },
               inplace=True)
    rfm["recency"] = rfm["recency"].astype(int)
    rfm['r_quartile'] = pd.qcut(rfm['recency'],
                                3, ['1', '2', '3'],
                                duplicates='drop')
    rfm["f_quartile"] = pd.qcut(rfm["frequency"],
                                3, ['3', '2', '1'],
                                duplicates='drop')
    rfm["m_quartile"] = pd.qcut(rfm["monetary"],
                                3, ['3', '2', '1'],
                                duplicates='drop')

    rfm["RFM_Score"] = rfm.r_quartile.astype(str) + rfm.f_quartile.astype(
        str) + rfm.m_quartile.astype(str)

    return rfm


@st.cache
def importDF():
    df = pd.read_csv("data{}KaDo.csv".format(os.sep), sep=",")
    df["MOIS_VENTE"] = df["MOIS_VENTE"].apply(
        lambda x: "2021-{}-01 12:50:00".format(x))
    df = df.assign(QUANTITY=lambda x: 1)

    return df


@st.cache
def importRFM(df):
    try:
        rfm = pd.read_csv("data{}RFM_client.csv".format(os.sep))
    except:
        saveRFM(df)
        rfm = pd.read_csv("data{}RFM_client.csv".format(os.sep))

    return rfm


@st.cache
def importProducts():
    try:
        products = pd.read_csv("data{}Products_ids.csv".format(os.sep),
                               sep=",")
    except:
        save_products()
        products = pd.read_csv("data{}Products_ids.csv".format(os.sep),
                               sep=",")

    return products


@st.cache
def replaceProductsById(df_history, df_products):
    df_history["MOIS_VENTE"] = pd.to_datetime(df_history["MOIS_VENTE"])
    df_history["MOIS_VENTE"] = df_history["MOIS_VENTE"].values.astype(
        np.int64) // 10**9
    df_history = df_history.sort_values("MOIS_VENTE")
    ids = []

    for l in df_history["LIBELLE"]:
        ids.append(
            df_products[df_products["LIBELLE"] == l]["ITEM_ID"].values[0])

    df_history["ITEM_ID"] = ids
    return df_history


df = importDF()
products = importProducts()

rfm = importRFM(df)
rfm_all = get_rfm(df)

st.sidebar.title("Navigation")
st.title("Dashboard")

display = st.sidebar.radio("View: ",
                           ("All Data", "Search Client", "Search Product"))

if display == "All Data":
    st.header("All Data")
    with st.expander("DataFrame", expanded=False):
        st.write(df.head(100))

    with st.expander("Sales Informations", expanded=False):
        t = df["MOIS_VENTE"].value_counts(sort=False)
        t.index = pd.to_datetime(t.index)
        i = []
        for d in t.index:
            i.append(int(str(d).split('-')[1]))
        t.index = i
        st.subheader("Sales per Month")
        st.bar_chart(t, height=400)

        col1, col2, col3 = st.columns(3)

        fam = df["FAMILLE"].value_counts().sort_values(ascending=False)
        mai = df["MAILLE"].value_counts().sort_values(ascending=False)[:10]
        uni = df["UNIVERS"].value_counts().sort_values(ascending=False)[:10]
        lib = df["LIBELLE"].value_counts().sort_values(ascending=False)[:20]
        with col1:
            st.subheader("Sales per Family")
            st.bar_chart(fam, height=400)
        with col2:
            st.subheader("Sales per Maille")
            st.bar_chart(mai, height=500)

        with col3:
            st.subheader("Sales per Univers")
            st.bar_chart(uni, height=500)

        st.subheader("Sales per Product")
        st.bar_chart(lib, height=550)

    with st.expander("RFM", expanded=False):
        r, f, m = st.columns(3)

        with r:
            st.subheader("Recency")
            st.bar_chart(rfm["recency"].value_counts(sort=False))

        with f:
            st.subheader("Frequency")
            freq = rfm.loc[rfm["frequency"] < 70]
            st.area_chart(freq["frequency"].value_counts(sort=False))

        with m:
            st.subheader("Monetary")
            mon = rfm.loc[rfm["monetary"] < 500]
            st.line_chart(mon["monetary"].value_counts(sort=False))

        a, b, c = st.columns([1, 3, 1])

        with a:
            st.write("")

        with b:
            st.subheader("RFM Score")
            rfm = rfm.sort_values("RFM_Score")
            st.bar_chart(rfm["RFM_Score"].value_counts(sort=False))

        with c:
            st.write("")

elif display == "Search Product":
    st.header("Per Product")
    filter = st.selectbox(
        "Select a Filter",
        ("Filter", "Famille", "Maille", "Univers", "Libelle"),
        index=0)

    if filter != "Filter":
        select = st.selectbox("Select a {}".format(filter),
                              df[filter.upper()].unique(),
                              index=0)
        data = df[df[filter.upper()] == select].drop("QUANTITY", axis=1)
        index = [
            "Mean price of article", "Total number of articles",
            "Total number of articles bought", "Total money",
            "Total number of orders"
        ]
        values = {
            "Values": [
                np.round(df["PRIX_NET"].unique().mean(), 0),
                len(df["LIBELLE"].unique()), data.shape[0],
                np.round(df["PRIX_NET"].sum(), 0),
                len(df["TICKET_ID"].unique())
            ]
        }

        info = pd.DataFrame(values, index=index, dtype=int)
        a, b = st.columns([1, 2])
        with a:
            st.subheader("General Informations")
            st.write(info)

        with b:
            t = data["MOIS_VENTE"].value_counts(sort=False)
            t.index = pd.to_datetime(t.index)
            i = []
            for d in t.index:
                i.append(int(str(d).split('-')[1]))
            t.index = i
            st.subheader("Sales per Month")
            st.bar_chart(t, height=400)

        # st.write(data.sample(frac=0.1))
else:
    st.header("Per Client")
    client_id = st.number_input("Client ID",
                                value=0,
                                help="{} unique clients".format(
                                    len(df["CLI_ID"].unique())))
    if client_id != 0:
        df_client = df.copy()
        df_client = df_client.loc[df_client["CLI_ID"] == client_id]
        if len(df_client.index) > 0:
            rfm_client = rfm_all.loc[[int(client_id)]]
            rfm_client = rfm_client[[
                "recency", "frequency", "monetary", "RFM_Score"
            ]]

            with st.expander("Client Informations", expanded=False):
                price_per_ticket = df_client.groupby([
                    "TICKET_ID"
                ])["PRIX_NET"].sum().reset_index(name="PRIX_NET").apply(
                    lambda x: np.round(x, 2)).sort_values("PRIX_NET",
                                                          ascending=False)
                items_per_ticket = df_client.groupby(
                    ["TICKET_ID"])["LIBELLE"].unique().str.len()

                index = [
                    "Total number of orders",
                    "Total number of unique items bought",
                    "Mean number of unique items per order", "Total spent",
                    "Mean Amount Spent per Order"
                ]
                values = {
                    "Values": [
                        np.round(len(df_client["TICKET_ID"].unique()), 0),
                        np.round(len(df_client["LIBELLE"].unique()), 0),
                        np.round(items_per_ticket.values.mean(), 2),
                        np.round(price_per_ticket["PRIX_NET"].sum(), 2),
                        np.round(price_per_ticket["PRIX_NET"].mean(), 2)
                    ]
                }
                info = pd.DataFrame(values, index=index, dtype=str)

                model_type = st.selectbox(
                    "Which model to use",
                    ("CNN", "Pooling", "LSTM", "Mixture"))
                if model_type == "Pooling":
                    model = pickle.load(
                        open("models{}model_spotlight.pkl".format(os.sep),
                             "rb"))
                elif model_type == "LSTM":
                    model = pickle.load(
                        open("models{}model_spotlight_lstm.pkl".format(os.sep),
                             "rb"))
                elif model_type == "Mixture":
                    model = pickle.load(
                        open(
                            "models{}model_spotlight_mixture.pkl".format(
                                os.sep), "rb"))
                else:
                    model = pickle.load(
                        open("models{}model_spotlight_cnn.pkl".format(os.sep),
                             "rb"))

                df_pred = df_client.copy().sort_values("MOIS_VENTE",
                                                       ascending=False)
                df_pred = df_pred[["LIBELLE", "MOIS_VENTE"]]
                df_pred = replaceProductsById(df_pred, products)

                prediction = model.predict(df_pred["ITEM_ID"])
                prediction = np.argmax(prediction)
                prediction = products[products["ITEM_ID"] ==
                                      prediction]["LIBELLE"]

                rfm_client["recommendation"] = [prediction.values[0]]

                a, b, c = st.columns([2, 3, 1])
                with a:
                    st.write("")
                with b:
                    st.write(info)
                with c:
                    st.write("")
                a, b, c = st.columns([1, 3, 1])
                with a:
                    st.write("")
                with b:
                    st.write(rfm_client)
                with c:
                    st.write("")

            with st.expander("Client History", expanded=False):
                df_client = df_client.drop("QUANTITY",
                                           axis=1).sort_values("MOIS_VENTE")
                st.write(df_client)

        else:
            st.error("Invalid Client ID")
