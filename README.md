# api-experimentation
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)   [![HitCount](https://hits.dwyl.com/dbedi3311/api-experimentation.svg?style=flat-square)](http://hits.dwyl.com/dbedi3311/api-experimentation)

Experimenting with open source APIs and parsing their outputs with Python (using requests library)
- Streaming APIs
- (Long) Polling

**Goals:** To learn API retrieval fundamentals, be able to pass parameters of my choosing to query an API, and to be able to process and handle the output response. This is highly valuable when needing to build an application on top of a microservice architecture and extremely useful when gathering data in real-time (or almost real-time) to ingest into a database. I have a deeper satiable desire to understand api-retrieval libraries from a fine-grained perspective while also improving my skills in data manipulation and extraction. 

--- 
I have taken the notes below to help me understand how to replicate this setup. 
## Getting Started

1. Clone the repository on your local machine using: 
```
git clone https://github.com/dbedi3311/api-experimentation.git
```

2. Create a python virtualenv called aq_venv (this can be substituded for a name of your choosing)
```
python3 -m venv aq_venv
```
and activate using 
```
source aq_venv/bin/activate
```

3. Install the package requirements with
```
pip install -r requirements.txt
```

Now you're ready to begin working with `airquality_ingest.py` 
Take a look at the code while reading the comments (they'll be helpful, I promise).

If you want to launch the openAQ demo application that uses mapbox configuration to view TileJSON, I've developed a small flask application to serve the html template provided by querying the API. Simply run: `flask run` in your terminal when in the directory containing app.py. You can view the html and javascript code that renders the map in the `templates/tileviewer.html` file.

I've provided a screenshot of how the demo looks:
<img width="1792" alt="image" src="https://user-images.githubusercontent.com/29437601/171939295-993ac73d-69b6-49a3-9fdb-f70be239617f.png">


## Personal Notes for Later Use
Command that I used to make the .gitignore from toptal
```
curl -o .gitignore https://www.toptal.com/developers/gitignore/api/python,pycharm
```

### TODO:
- Using a cache to store the data (perhaps Redis)
- Handling time-data formats
