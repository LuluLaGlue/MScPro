# RECOMMENDER
This repository contains our attemps to process client's purchase history to use it for reporting, furthermore, we used the available data to build a recommender.

## Info
### Preparation
In order to use this project you need <a href='https://www.python.org/downloads/'>python3</a> installed as well as the <code>KaDo.csv</code> file placed in a <code>data/</code> folder at the root of the project.<br />
To install dependencies run <code>pip3 install -r requirements.txt</code><br />
For the project to be usable you need to generate the needed data. For that run :
-   <code>cd utils/</code>
-   <code>python3 format_data.py</code>

Once the needed data has been created you can run <code>streamlit run dashboard.py</code> at the root of the project to start the dashboard.

## Files
-   <code>spotlight.ipynb</code>: A jupyter notebook containing the process used to train our recommender.
-   <code>segmentation.ipynb</code>: A jupyter notebook containing some informations on the dataset (such as ***RFM Matrice***).
-   <code>dashboard.py</code>: A python script containing a dashboard to display informations on this business' data.

## Folders
-   <code>data/</code>: This folder contains several <code>.csv</code> files generated once you have run the <code>format_data.py</code> script.
    *   <code>KaDo.csv</code>: This is the file containing client's purchase history.
    *   <code>KaDo_Timestamps.csv</code>: This file contains the <code>KaDo.csv</code> data with the *MOIS_VENTE* column being of the **datetime** type, and a new *timestamps* column.
    <!-- *   <code>KaDo_Duplicates.csv</code>: This file contains the <code>KaDo_Timestamps.csv</code> data without any duplicate purchase, meaning that each products is considered to have been bought only once per ticket. -->
    *   <code>Products_ids.csv</code>: This file contains a list of all products with a custom generated ID that will be used during training.
    *   <code>RFM.csv</code>: This files contains info on the RFM Matrice for each user.
-   <code>models/</code>: This folder contains several models based on a few different approach for our recommender. The final model is <code>model_spotlight_cnn.pkl</code> and is based on the *CNN* architecture.
-   <code>utils/</code>; This folder contains usefull scripts:
    *   <code>format_data.py</code>: This script is used to created the needed <code>.csv</code> files inside the <code>data/</code> folder.
    *   <code>client_info.py</code>: This script is used to extract info on a specific client (run <code>python client_info.py -h</code> for more information).
    *   <code>kickoff.ipynb</code>: A jupyter notebook containing different informations on the used data.
    *   <code>metrics.ipynb</code>: A jupyter notebook used to calculate the MRR Score of the different models.
