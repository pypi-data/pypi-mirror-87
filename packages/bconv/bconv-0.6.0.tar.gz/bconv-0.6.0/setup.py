# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bconv', 'bconv.doc', 'bconv.fmt', 'bconv.nlp', 'bconv.util']

package_data = \
{'': ['*']}

install_requires = \
['lxml>=4.3,<5.0', 'nltk>=3.4,<4.0']

setup_kwargs = {
    'name': 'bconv',
    'version': '0.6.0',
    'description': 'Convert between BioNLP formats',
    'long_description': "# `bconv`: Python library for converting between BioNLP formats\n\n`bconv` offers format conversion and manipulation of documents with text and annotations.\nIt supports various popular formats used in natural-language processing for biomedical texts.\n\n\n## Supported formats\n\nThe following formats are currently supported:\n\n| Name                               | I | O | T | A | Description |\n| ---------------------------------- | - | - | - | - | ----------- |\n| `bioc_xml`, `bioc_json`            | ✓ | ✓ | ✓ | ✓ | [BioC][1] |\n| `bionlp`                           |   | ✓ |   | ✓ | [BioNLP stand-off][2] |\n| `brat`                             |   | ✓ |   | ✓ | [brat stand-off][2] |\n| `conll`                            | ✓ | ✓ | ✓ | ✓ | [CoNLL][3] |\n| `europepmc`, `europepmc.zip`       |   | ✓ |   | ✓ | [Europe-PMC JSON][4] |\n| `pubtator`, `pubtator_fbk`         | ✓ | ✓ | ✓ | ✓ | [PubTator][5] |\n| `pubmed`, `pxml`                   | ✓ |   | ✓ |   | [PubMed abstracts][6] |\n| `pmc`, `nxml`                      | ✓ |   | ✓ |   | [PMC full-text][6] |\n| `pubanno_json`, `pubanno_json.tgz` |   | ✓ | ✓ | ✓ | [PubAnnotation JSON][7] |\n| `csv`, `tsv`                       |   | ✓ |   | ✓ | [comma/tab-separated values][8] |\n| `text_csv`, `text_tsv`             |   | ✓ | ✓ | ✓ | [comma/tab-separated values][8] |\n| `txt`                              | ✓ | ✓ | ✓ |   | [plain text][9] |\n| `txt.json`                         | ✓ | ✓ | ✓ |   | [collection of plain-text documents][9] |\n\n**I**: input format;\n**O**: output format;\n**T**: can represent text;\n**A**: can represent annotations (entities).\n\n[1]: https://github.com/lfurrer/bconv/wiki/BioC\n[2]: https://github.com/lfurrer/bconv/wiki/Brat\n[3]: https://github.com/lfurrer/bconv/wiki/CoNLL\n[4]: https://github.com/lfurrer/bconv/wiki/EuropePMC\n[5]: https://github.com/lfurrer/bconv/wiki/PubTator\n[6]: https://github.com/lfurrer/bconv/wiki/PubMed\n[7]: https://github.com/lfurrer/bconv/wiki/PubAnnotation\n[8]: https://github.com/lfurrer/bconv/wiki/CSV\n[9]: https://github.com/lfurrer/bconv/wiki/TXT\n\n\n## Installation\n\n`bconv` is hosted on [PyPI](https://pypi.org/project/bconv/), so you can use `pip` to install it:\n```sh\n$ pip install bconv\n```\nBy default, `pip` attempts a system-level installation, which might require admin privileges.\nAlternatively, use `pip`'s `--user` flag for an installation owned by the current user.\n\n\n## Usage\n\nLoad an annotated collection in BioC XML format:\n```pycon\n>>> import bconv\n>>> coll = bconv.load('path/to/example.xml', fmt='bioc_xml')\n>>> coll\n<Collection with 37 subelements at 0x7f1966e4b3c8>\n```\nA Collection is a sequence of Document objects:\n```pycon\n>>> coll[0]\n<Document with 12 subelements at 0x7f1966e2f6d8>\n```\nDocuments contain Sections, which contain Sentences:\n```pycon\n>>> sent = coll[0][3][5]\n>>> sent.text\n'A Live cell imaging reveals that expression of GFP‐KSHV‐TK, but not GFP induces contraction of HeLa cells.'\n```\nFind the first annotation for this sentence:\n```pycon\n>>> e = next(sent.iter_entities())\n>>> e.start, e.end, e.text\n(571, 578, 'KSHV‐TK')\n>>> e.info\n{'type': 'gene/protein', 'ui': 'Uniprot:F5HB62'}\n```\nWrite the whole collection to a new file in CoNLL format:\n```pycon\n>>> with open('path/to/example.conll', 'w', encoding='utf8') as f:\n...     bconv.dump(coll, f, fmt='conll', tagset='IOBES', include_offsets=True)\n```\n\n\n## Documentation\n\n`bconv` is documented in the [GitHub wiki](https://github.com/lfurrer/bconv/wiki).\n",
    'author': 'Lenz Furrer',
    'author_email': 'lenz.furrer@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lfurrer/bconv',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
