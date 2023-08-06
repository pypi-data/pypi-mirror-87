# library.qai.utilities

A REST server and helper functions and classes for interacting with the rest of the Qordoba platform.

See GitHub history for older docs.

## 4.2.0
Extending issue meta.
Spacy factor on init accepts:
- issue_type: str, 
- simple_description: str, 
- description (default: None), 
- debug (default: False)

## Upgrading to v4.0.12
Added support for extensions bigtable:
Documents from platform are represented by `DocumentBigTable`
Documents coming from extensions (chrome, office, ...etc) are represented by `ExtensionBigTable`

Usage:
```python
extension_bigtable = ExtensionBigTable(project, instance_id, table_id_extension, column_family_id_extension, column_qualifier_extension)
extension_bigtable.fetch_document_content(document_id, organization_id, workspace_id, persona_id)  # returns formatted text with new lines \n
extension_bigtable.fetch_document_text(document_id, organization_id, workspace_id, persona_id)  # returns plain text
```
                                  
## Upgrading to v4.0.9

### New optional `storage` module

Has extra dependencies, install like:

`pip install qai[storage]`

or locally

`pip install ../some/path[storage]`

(Note, in 4.0.8 these were not extra, so `pip install qai==4.0.8` would also install the needed storage deps)

Then use like:

```python
from qai.storage.bigtable import DocumentBigTable


dbt = DocumentBigTable(project, instance_id, table_id, column_family_id, column_qualifier)
# then you probably want to pass to Analyzer and have it set self.bt = dbt in __init__ or something, but you can do
dbt.fetch_document_content(document_id, organization_id)  # returns HTML
dbt.fetch_document_text(document_id, organization_id)  # returns text
```

## Upgrading to v.4.0.3

`Analyzer()` object in dependant services must have `nlp` object as an attribute. If this is not met, single token predictions produce the following traceback:

```python
[E030] Sentence boundaries unset. You can add the 'sentencizer' component to the pipeline with: nlp.add_pipe(nlp.create_pipe('sentencizer')) Alternatively, add the dependency parser, or set sentence boundaries by setting doc[i].is_sent_start.
```

## Changes in 3.0.0

Remove code for processing older pipeline formats. We now only process the new style, which has `chain`.

## Changes in 2.4.0

* We now enforce `if QRest.batching == True: QRest.workers = 1`
* If you don't specify `QRest.workers` on instantiating, before setting `workers=cpu_count` we first check the configs, and use the value `"WORKER_COUNT"` @yakivy

## Upgrading to v2.3.5

Dependant services *must* include `nltk==3.4.5` in `requirements.txt` (`setup.py` bug).

Docker file of the dependant service *must* include the line (assure printing payload does not cause encoding exceptions):

`ENV PYTHONIOENCODING=utf-8`

Dependant services *can* pass to `QRest` extra flags:

* `debug` (default: `False`) - if `True` don't escape exceptions (don't use in prod)
* `batching` (default: `False`) - if `True` pass array of segments to qallback instead of consecutive qallback calls
* `verbose` (default: `False`) - if `True` print full output
* `ignore_html` (default: `True`) - if `batching=False` ignore sentences with html tags
* `sentence_token_limit` (default: `1024`) - if `batching=False` ignore sentences longer than 1024 words/tokens

## Upgrading to v2

Upgrading to v2 does require a few changes. Some noteable one:

* `get_config` will break. Sorry, you have to deal with that yourself
* `QConnect` is gone, and `QRest` is imported more explicitly
* There is no more `qai` Docker image. You are free to use whatever base image you want. May I recommend `qsam/spacy_alpine`.
* `qai` is now a pip dependency, so must be in your `requirements.txt`

However! There's help. Follow these steps:

```sh
cd qai_v1_service
vactivate  # or however you go into a virtualenv
pip uninstall -y qai
# uninstalls old qai
pip install qai
# installs qai from PyPi
python -m qai.upgrade .
# shows you how it would change your files to make the project ready for v2
# n to reject, y to accept
```

Now all that remains is seeing if you use `get_configs`, and if so: **pass `get_configs` an absolute path (v2), instead of a relative path split into a list (v1).**

Note: I went a bit fast, and long story short, versions 2.0.x and 2.1.x are not salvageable. Just use 2.2.0+.

## Things to know

See [The Changelog](CHANGELOG.md) for details.

### Required "conventions"

All projects *must* have a `config.json`, and that config *must* specify `SUPPORTED_LANGUAGES`, which is either a string or list of strings, of the form `"en"` or `["en", "de", "zh"]` (the prefix of the ISO code). QAI will not let your service start unless it thinks you have a valid `SUPPORTED_LANGUAGES` field. By default, QAI will look for this in `conf/config.json`. This is overridable. Here is the minimal config:

```json
{
  "SUPPORTED_LANGUAGES": "en"
}
```

You can specify the service name in the config file with

```json
{
  "SUPPORTED_LANGUAGES": "en",
  "SERVICE_NAME": "hey look at me service",
}
```

To change the config path to, for example, `./my_config_dir/a_sub_dir/my_wacky_config.json`:

```python
QRest(analyzer,
         category='service name, e.g. formality',
         white_lister=white_lister,
         config_path=['my_config_dir', 'a_sub_dir', 'my_wacky_config.json'])
```
By default, QAI sends `no-issues-response` whenever a call to dependant library fails. To turn on the `debug` mode:

```python
QRest(analyzer,
         category='service name, e.g. formality',
         white_lister=white_lister,
         debug=True)
```
Print out input segments:

```python
QRest(analyzer,
         category='service name, e.g. formality',
         white_lister=white_lister,
         verbose = True)
```

* `verbose` (default: `False`) - print full output

To process batches instead of looping over segments (send by a mediator):

```python
QRest(analyzer,
         category='service name, e.g. formality',
         white_lister=white_lister,
         batching=True)
```

Important: QAI does not define batch size, if batching enabled, just passes the entire mediator input. In order to change mediator batch size look for `segmentDelegator.read.batchSize` in `config/application.conf` of the dependant service.

To customize input filters:

```python
QRest(analyzer,
         category='service name, e.g. formality',
         white_lister=white_lister,
         batching=False,
         sentence_token_limit=1024,
         ignore_html=True)
```

* `ignore_html` (default: `True`) - if `batching=False` ignore sentences with html tags
* `sentence_token_limit` (default: `1024`) - if `batching=False` ignore sentences longer than 1024 words/tokens


## Usage

You can explicitly create a REST connection like this:

```python
from app import Analyzer, whitelist

from qai.qconnect.qrest import QRest


SERVICE_NAME = 'service_name'
host = '0.0.0.0'
port = 5000


if __name__ == '__main__':
    analyzer = Analyzer()
    rest_connection = QRest(analyzer,
                            category=category,
                            white_lister=white_lister,
                            host=host,
                            port=port)
    # create a blocking connection:
    rest_connection.connect()
```

The above will create *as many workers as you have cores.* This is great, _unless_ you are using AutoML. There is a known bug where AutoML crashes if you are using more than one worker.

So if you're using AutoML, the above would look like:

```python
from app import Analyzer, whitelist

from qai.qconnect.qrest import QRest


SERVICE_NAME = 'service_name'
host = '0.0.0.0'
port = 5000
workers = 1


if __name__ == '__main__':
    analyzer = Analyzer()
    rest_connection = QRest(analyzer,
                            category=category,
                            white_lister=white_lister,
                            host=host,
                            port=port,
                            workers=workers)
    # create a blocking connection:
    rest_connection.connect()
```

There is also a helper class for turning spaCy `Span`s into issues the rest of the platform can process:

```python
from spacy.tokens import Span
from app.factor import SpacyFactor


SOV = SpacyFactor(
    "subject_object_verb_spacing",
    "Keep the subject, verb, and object of a sentence close together to help the reader understand the sentence."
)

Span.set_extension("score", default=0)
Span.set_extension("suggestions", default=[])

doc = nlp("Holders of the Class A and Class B-1 certificates will be entitled to receive on each Payment Date, to the extent monies are available therefor (but not more than the Class A Certificate Balance or Class B-1 Certificate Balance then outstanding), a distribution.")
score = analyze(doc)
if score is not None:
    span = Span(doc, 0, len(doc))  # or whichever TOKENS are the issue (don't have to worry about character indexes)
    span._.score = score
    span._.suggestions = get_suggestions(doc)
    issues = SOV(span)
```

## Installation

`pip install qai`

## Testing

See Confluence for docs on input format expectations.

`scripts/test_qai.sh` has some helpful testing functions.

## Development

Source of truth is `VERSION` file, read by `setup.py` and `Jenkinsfile`. When you run `python setup.py sdist/bdist`, this creates `qai/version.py`, which is read in `qai/__init__.py`. This was done for reasons having to do with python's module system being frustrating. It allows one to not have to know the absolute path of a file at runtime, which is a big bonus in Python. Anyway, that means `VERSION` is the source of truth.

### CI/CD

Jenkins will push to PyPi when you build `master` or `v2` branch. It also might automatically build v2 branch on git push, testing that now.

To get Jenkins to build this, we had to throw it in Docker... so the Jenkinsfile calls the Dockerfile which calls the release script... It's a house of cards, but seems to work.

### License

This software is not licensed. If you do not work at Qordoba, you are not legally allowed to use it. Also, it's just helper functions that really won't help you. If something in it does look interesting, and you would like access, open an issue.
