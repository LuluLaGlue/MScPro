# API

### **_AI_**

-   Our AI is accessible via the heroku hosted Flask API located <a href="https://api-aia.herokuapp.com">here</a>.
    -   NLP: The NLP Part is exposed via the endpoint <code>/get_cities</code>:
        -   Method: <code>POST</code>
        -   Body: <code>{"text": "Your Query Containing a Valid Command such as 'Je veux aller de Gap à Grenoble'."}</code>
        -   /!\\: The query must be in french,
        -   Return: <code>{"cities": ["Gap", "Grenoblee"]}</code>
    -   Shortest Path: The Shortest Path algorithm is exposed via the endpoint <code>/path</code>:
        -   Method: <code>POST</code>
        -   Body: <code>{"start": "Gare de Gap", "end": "Gare de Grenoble"}</code>,
        -   /!\\: The stations must be valid (_refer to <code>/stations</code> for a list of stations_) but not case sensitive,
        -   Return: <code>{"path": ["Gare de Gap", "Gare de Grenoble"]}</code>.
    -   Stations: The list of train stations can be retrieved via <code>/stations</code>:
        -   Method: <code>GET</code>,
        -   Return: <code>{"stations": ["Gare de Gap", "Gare de Figeac", "Gare de Paris-Austerlitz", ...]}</code>
    -   Search Stations: You can search for a train stations via <code>/stations</code>:
        -   Method: <code>POST</code>,
        -   Body: <code>{"query": "Paris"}</code>
        -   Return: <code>{"stations": ["Gare de Paris Montparnasse", "Gare de Paris-St-Lazare", "Gare de paris-montp.3-vaug.", "Gare de paris-bercy", "Gare de paris-est", "Gare de paris gare du nord", "Gare de paris-gare-de-lyon", "Gare de paris-austerlitz"]}</code>
    -   Multi Path: You can search for stations and get the shortest path between them by using the <code>/multi_path</code> endpoint:
        -   Method: <code>POST</code>,
        -   Body: <code>{"start": "Grenoble", "end": "Lyon"}</code>
        -   Return: <code>{"path": [{"path": ["Gare de Grenoble", "Gare de Lyob-Part-Dieu"], "time": 82, "start": "gare de grenoble", "end": "gare de lyon-part-dieu}, {"path": ["grenoble-gare-routiere", "lyon-part-dieu-gare-rou"], "time": 119, "end": "lyon-part-dieu-gare-rou", "start": "grenoble-gare-routiere"}]}</code>
    -   Query To Path: Based on a French Text Query return all possible train routes by using <code>/query_to_path</code>:
        -   Method: <code>POST</code>,
        -   Body: <code>{"query": "Je veux aller de Grenoble a Lyon"}</code>,
        -   Return: <code>{"path": [{"path": ["Gare de Grenoble", "Gare de Lyob-Part-Dieu"], "time": 82, "start": "gare de grenoble", "end": "gare de lyon-part-dieu}, {"path": ["grenoble-gare-routiere", "lyon-part-dieu-gare-rou"], "time": 119, "end": "lyon-part-dieu-gare-rou", "start": "grenoble-gare-routiere"}]}</code>
-   You can run the API locally (if you have <code>python 3.9</code> installed) by running:
    -   <code>cd api/</code>,
    -   <code>pip3 install -r requirements.txt</code>,
    -   <code>python3 main.py</code>.
