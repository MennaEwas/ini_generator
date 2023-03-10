# ini_Generator

- This project is a way to generate a new ini file for a new device 
from an old ini file Containing configuration details for an old device

- It solves the problem of re-entering the configuration details of a device every time a new device is getting 

- The project is a web-based solution because the traditional user interface to do this kind of reconfiguration is a webpage 

- There is two kind types of users the Admin who is responsible for the website and which parts need to be edited
and this part is made for the admin, the second part is made for the Engineer who will change some parts of the ini file to be generated in the new file 
and the work in this part in the progress 

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install.

```bash
pip install flask 
pip install json
```

## Usage

```python
from configparser import ConfigParser

app = Flask(__name__, static_url_path='/static')

@app.route("/", methods = ['GET', 'POST'])
def index():
    config = ConfigParser()
    config.read('file.ini')
```

## Run the project 
- run the main.py and follow the link
- Page 1: Select from this page which parts you need to be changed in the new ini file from the old one
- page 2: Make some restrictions on the data type of the chosen items 
- page 3: Choose new Friendly names to be shown for the Engineer user 
- Page 4: If this page is shown, it means your deployment is done successfully and your data saved in a json file 

## Contributing
@MennaEwas

## License

[GNU](https://choosealicense.com/licenses/gpl-3.0/)
