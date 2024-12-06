# ESMapping-Analyzer

## Analysis tool for index OpenSearch mapping files

This tool will open .json files with OpenSearch mappings and analyze the number of keys for each index.

The json file can be created by calling your OpenSearch API as follows:

```bash
curl -X GET "http://<opensearch-host>:9200/*/_mapping/" -H 'Content-Type: application/json' > mappings.json
```

This curl command retrieves all the indexes.
Note this is a generic url and needs to be setup with your specific one.

After creating the `mappings.json` file open it to get the names of the indexes exported.
The resulting file will have a structure similat to this:

```json
{
  "index-name": {
    "mappings": {
      "properties": {
        "field1": {
          "type": "text",
          "analyzer": "standard"
        },
        "field2": {
          "type": "keyword"
        },
        "field3": {
          "type": "date"
        }
      }
    }
  },
  "index-name2": {
    "mappings": {
      "properties": {
        "field1": {
          "type": "text",
          "analyzer": "standard"
        }
      }
    }
  }
}
```

The ESMapping-analyzer requires 2 mandatory command line arguments:

* filename
* index name

There is also an optional argument to change the order of the output results and can be set to the following values:

* key (default if ommited)
* value

To run the analyzer execute it with your Python runtime binary:

```bash
python ESMapping-analyzer.py mappings.json index-name
```
