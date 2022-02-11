# KICK OFF
## Datasets
### KaDo.csv

We intend to base our study on the *KaDo.csv* file containing **7245523** sales transactions. Each transaction is stored along several informations:
-   **TICKER_ID**: The transaction's id, unique for each order,
-   **MOIS_VENTE**: Month in which the transaction has been conducted, in our analysis we understood as each month in one year (*1* means the sale has been conducted in *January*, *2* means *February*, etc.),
-   **PRIX_NET**: The price of the bought article.
-   **FAMILLE**: The *famille* to which the product is from,
-   **UNIVERS**: The *univers* to which the product is from,
-   **MAILLE**: The *maille* to which the product is from,
-   **LIBELLE**: The name of the product,
-   **CLI_ID**: The client's id attached to the transactions.

### KaDo_Timestamps.csv

In order to add a time aspect to the dataset we will be adding a *timestamp* column to the original file. This column will store a timestamp refering to the month of purchase, it is defined using the following logic: **2020-xx-01 12:50:00** with **xx** being the month of purchase. This will allow us to define a more precise order in purchases in client that have made more than one purchase. It will be most usefull with our ***Recurrent Neural Network*** used for recommendation.

### KaDo_Duplicates.csv

To try out a different approach we will be removing duplicates items in each order (meaning if a user bought an item twice in the same order we will only be counting it once), to do so we will use the *FAMILLE*, *UNIVERS*, *MAILLE* and *LIBELLE* columns to define what are to be considered duplicates. The resulting dataset will be stored in a *KaDo_Duplicates.csv*

### Products_ids.csv

In order to train a *RNN* we will need to convert text informations to integers, to do so we will be using **panda**'s **Categorical** on the *LIBELLE* column, the resulting categories' ids will be stored along side their textual counterpart in *Products_ids.csv*

### RFM.csv

We will be using an RFM matrice to segment clients, in order to save some time once the matrice is calculated we will be storing it a separate *.csv* file, this file will contain several columns:
-   **recency**: The greater the number the older the client's last order is,
-   **frequency**: The greater the number the more the client has placed orders,
-   **monetary**: The greater the number the more money the client has spent,
-   **r/f/m_quartile**: The quartile in which the client is located in *recency*, *frequency* and *monetary* aspects,
-   **RFM_Score**: The resulting RFM Score for each client.

## kickoff.ipynb

A *Jupyter Notebook* file containing a short study based on *KaDo.csv* will also be available.

## Dashboard

Our main results will presented in the form of a **Dashboard**.

## Models

In our attempt to create an accurate recommender we tried several approches, each of which is stored in a *.pkl* file in the *models/* folder.

### model_products*.pkl and model_all.pkl

Those models are product based, they rely on a kMean algorithm to clusterize items, we then run the trained algorithm with a client's pruchase history in order to place him in a cluster of items. We then only need to pick an item from the resulting cluster. The training and testing script can be found in the *old/* folder within the *kMean_old.ipynb* and *kMean_Products.ipynb*

### model_tickets.pkl

We tried here to clusterize purchases instead of products, it resulted in a model randomly clustering whatever we gave it so we decided not to use it at all.

### model_spotlight*.pkl

The models containing *spotlight* in their name are models based on a ***Recurrent Neural Network***, we trained them with the *KaDo_Timestamps.csv* (the one containing *dup* were trained with the *KaDo_Duplicates.csv*). We used architecture based on *Convolutionnal Neural Network*, *Long Short-Term Memory*, *Pooling* and a mixture of *CNN* and *Pooling*. In order to define the best model that we had trained, we measured their ***MRR*** score, the result can be found inside *utils/metrics.ipynb* and show that the *CNN* based *RNN* is the most accurate model with a *MRR* score of ***0.06178***.