import json
import sys
from collections import defaultdict

def count_keys(properties, prefix, counts):
    """Recursively counts keys and nested keys."""
    for key, value in properties.items():
        num_keys = 0
        full_key = f"{prefix}.{key}" if prefix else key

        if isinstance(value, dict):
            # If the field has a "properties" key, recurse into it
            nested_properties = value.get("properties")
            if isinstance(nested_properties, dict):
                num_keys = len(nested_properties)
                count_keys(nested_properties, full_key, counts)

        # Set the value for the current key
        counts[full_key] = num_keys

def main():
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: python analyze_fields.py <path_to_json_file> <index_name> [order]")
        print("Order can be 'key' (default) or 'value'.")
        return

    json_file_path = sys.argv[1]
    index_name = sys.argv[2]
    order = "key"  # Default order

    if len(sys.argv) == 4:
        order = sys.argv[3]

    if order not in ("key", "value"):
        print(f"Error: Order '{order}' is not supported")
        return

    # Read the JSON file
    try:
        with open(json_file_path, "r") as file:
            json_data = json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{json_file_path}' not found")
        return
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return

    # Check if the top-level key exists and is of the correct type
    index_properties = json_data.get(index_name)
    if not isinstance(index_properties, dict):
        print(f"Error: Mappings Group '{index_name}' not found or is not a map in JSON")
        return

    mappings = index_properties.get("mappings")
    if not isinstance(mappings, dict):
        print("Error: 'mappings' key not found in the top-level key")
        return

    properties = mappings.get("properties")
    if not isinstance(properties, dict):
        print("Error: 'properties' key not found in 'mappings'")
        return

    # Prepare a dictionary to hold the counts
    key_counts = defaultdict(int)
    count_keys(properties, "", key_counts)

    if order == "key":
        # Print the map sorted by keys
        for key in sorted(key_counts):
            print(f"{key}: {key_counts[key]}")
    elif order == "value":
        # Print the map sorted by values (descending order)
        sorted_counts = sorted(key_counts.items(), key=lambda item: item[1], reverse=True)
        for key, value in sorted_counts:
            print(f"{key}: {value}")

if __name__ == "__main__":
    main()

