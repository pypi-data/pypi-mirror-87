# Download data from OLX listings

This is a Python script that can download listings from the small ads platform OLX in the following countries: 

- Argentina
- Bulgaria
- Bosnia
- Brazil
- Colombia
- Costa Rica
- Ecuador
- Egypt
- Guatemala
- India
- Indonesia
- Kazakhstan
- Lebanon
- Oman
- Pakistan
- Panama
- Peru
- Poland
- Portugal
- Romania
- San Salvador
- South Africa
- Ukraine
- Uzbekistan

If you use *olxsearch* for scientific research, please cite it in your publication: <br />
Fink, C. (2020): *olxsearch: Python script to download OLX small ads data*. [doi:10.5281/zenodo.3906038](https://doi.org/10.5281/zenodo.3906039).


### Dependencies

The script is written in Python 3 and depends on the Python modules [BeautifulSoup](https://beautiful-soup-4.readthedocs.io/), [dateparser](https://dateparser.readthedocs.io/), [geocoder](https://geocoder.readthedocs.io/), [pandas](https://pandas.pydata.org/) and [Requests](https://2.python-requests.org/en/master/).

To install dependencies on a Debian-based system, run:

```shell
apt-get update -y &&
apt-get install -y python3-dev python3-pip python3-virtualenv
```

(There’s an Archlinux AUR package pulling in all dependencies, see further down)


### Installation

- *using `pip` or similar:*

```shell
pip3 install olxsearch
```

- *OR: manually:*

    - Clone this repository

    ```shell
    git clone https://gitlab.com/christoph.fink/olxsearch.git
    ```

    - Change to the cloned directory    
    - Use the Python `setuptools` to install the package:

    ```shell
    cd olxsearch
    python3 ./setup.py install
    ```

- *OR: (Arch Linux only) from [AUR](https://aur.archlinux.org/packages/python-olxsearch):*

```shell
# e.g. using yay
yay python-olxsearch
```


### Usage

Import the `olxsearch` module.

Then instantiate an `olxsearch.OlxSearch` object, supplying a `country` and a `search_term` as arguments. The object’s `listings` property is a generator providing access to each ad listed on the platform that matches the supplied search term. Its `listings_as_dataframe` property is a `pandas.DataFrame` containing all these ads.

```python
import olxsearch

olx_search_argentina = olxsearch.OlxSearch("Argentina", "Yerba mate")
print(next(olx_search_argentina.listings))
# {'id': '1102114778', 'title': 'YERBA MATE SECADERO X 500 GRS.', 'description': 'YERBA MATE SECADERO \nPAQUETE X 500 GRS. $70\nPACK X 10 UNIDADES VENTA MÍNIMA\nCALIDAD DE EXPORTACIÓN \nEXCELENTE RELACIÓN PRECIO * CALIDAD \nAPROVECHE ANTES QUE SE TERMINEN\nCOMUNÍQUESE A NUESTRO WHATSAPP', 'created_at': '2020-02-18T16:57:38-03:00', 'created_at_first': '2020-02-18T16:57:02-03:00', 'republish_date': None, 'images': ['https://apollo-virginia.akamaized.net:443/v1/files/ns52s6zc369y2-AR/image'], 'price': (70.0, 'ARS'), 'lat': -34.626, 'lon': -58.4}


# pandas DataFrame
olx_search_southafrica = olxsearch.OlxSearch("South Africa", "Biltong")
listings = olx_search_southafrica.listings_as_dataframe
#             id                                              title  ...        lat        lon
# 0   1061464181                                     Biltong slicer  ... -25.703179  28.178248
# 1   1061707900         Claasen Biltong Slicer excellent condition  ... -28.549999  25.233299
# 2   1061884723                                      Biltong maker  ... -26.701476  27.092649
# ...
# 38  1061429395                                      Biltong snyer  ... -29.082081  26.148292
# 39  1059714562  Biltongkas / biltong box / biltong dryers / me...  ... -25.712152  28.002048
# 
# [40 rows x 10 columns]
```
