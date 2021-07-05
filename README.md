[![Tests](https://github.com/solalem/ckanext-datagovet-theme/workflows/Tests/badge.svg?branch=main)](https://github.com/solalem/ckanext-datagovet-theme/actions)

# ckanext-datagovet-theme

[ Based largely on [DataGovRo](https://github.com/john21ro/ckanext-datagovro_theme) repo. ]

Main CKAN extension theme for data.gov.et portal.


## Requirements

If your extension works across different versions you can add the following table:

Compatibility with core CKAN versions:

| CKAN version    | Compatible?   |
| --------------- | ------------- |
| 2.6 and earlier | no            |
| 2.7             | not tested    |
| 2.8             | not tested    |
| 2.9             | yes           |

Suggested values:

* "yes"
* "not tested" - I can't think of a reason why it wouldn't work
* "not yet" - there is an intention to get it working
* "no"


## Installation

To install ckanext-datagovet-theme:

1. Activate your CKAN virtual environment, for example:

     . /usr/lib/ckan/default/bin/activate

2. Clone the source and install it on the virtualenv

    ```
    git clone https://github.com/solalem/ckanext-datagovet-theme.git
    cd ckanext-datagovet-theme
    pip install -e .
    pip install -r requirements.txt
    ```

3. Add `datagovet_theme` to the `ckan.plugins` setting in your CKAN
   config file (by default the config file is located at
   `/etc/ckan/default/ckan.ini`).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu:

    ```sudo service apache2 reload```
    
    or for jetty
    
    ```sudo service jetty9 restart```

## Config settings

None at present

## Developer installation

To install ckanext-datagovet-theme for development, activate your CKAN virtualenv and
do:
    ```
    git clone https://github.com/solalem/ckanext-datagovet-theme.git
    cd ckanext-datagovet-theme
    python setup.py develop
    pip install -r dev-requirements.txt
    ```

## Tests

To run the tests, do:

    pytest --ckan-ini=test.ini


## Releasing a new version of ckanext-datagovet-theme

If ckanext-datagovet-theme should be available on PyPI you can follow these steps to publish a new version:

1. Update the version number in the `setup.py` file. See [PEP 440](http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers) for how to choose version numbers.

2. Make sure you have the latest version of necessary packages:

    pip install --upgrade setuptools wheel twine

3. Create a source and binary distributions of the new version:

       python setup.py sdist bdist_wheel && twine check dist/*

   Fix any errors you get.

4. Upload the source distribution to PyPI:

       twine upload dist/*

5. Commit any outstanding changes:

       git commit -a
       git push

6. Tag the new release of the project on GitHub with the version number from
   the `setup.py` file. For example if the version number in `setup.py` is
   0.0.1 then do:

       git tag 0.0.1
       git push --tags

## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
