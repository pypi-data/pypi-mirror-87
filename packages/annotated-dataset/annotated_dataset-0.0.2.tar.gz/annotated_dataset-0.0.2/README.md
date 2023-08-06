# Annotated Dataset


## Install
```BASH
pip install annotated-dataset
```

## Usage
```
logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


# Create client for inception server
inception_client = InceptionClient.create_client(
    host='https://mapa.pangeamt.com/',
    username='xxx',
    password='xxx'
)

# Config
config = {
    'dataset_name': 'MAPA_BG',
    'inception_projects': [
        {
            'name': 'Bulgarian_Legal_1',
            'use_segmentation_by_newline': True,
            'inception_client': inception_client
        },
        {
            'name': 'Bulgarian_Legal_2',
            'use_segmentation_by_newline': True,
            'inception_client': inception_client
        }
    ],
    'gold_corpus_preferred_resources': ['Bulgarian_Legal_1'],
    'export_dir': './'
}


export(config)
```
