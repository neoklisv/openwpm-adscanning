import json
import glob
import os
import networkx as nx
import matplotlib.pyplot as plt

def find_json_filenames(folder_path):
    sites = []
    
    # Construct the search pattern
    search_pattern = os.path.join(folder_path, '*.json')
    
    # Use glob.glob to find all files matching the search pattern
    json_files = glob.glob(search_pattern)


    # Print the list of json file names
    for filename in json_files:
        website = filename.split(".json",1)[0].rsplit("_",1)[1]
        sites.append((filename,website))

    return sites
       

def find_values(json_input, key):
    if isinstance(json_input, dict):
        for k, v in json_input.items():
            if k == key:
                yield v
            if isinstance(v, (dict, list)):
                yield from find_values(v, key)
    elif isinstance(json_input, list):
        for item in json_input:
            yield from find_values(item, key)

def unpack_string_from_nested_list(nested_list):
    for item in nested_list:
        if isinstance(item, list):  # If the item is a list, dive deeper
            result = unpack_string_from_nested_list(item)
            if result is not None:  # If a string was found in the deeper list, return it
                return result
        elif isinstance(item, str):  # If the item is a string, return it
            return item
    return None 

def main():

    # Specify the path to the folder you want to search
    folder_path = './null_persona_first_half/website_bids/'  # Change this to your folder path
    sites = find_json_filenames(folder_path)

    global_advertisers = {}


    for filename,website in sites:
        print('===============================')
        print("ADVERTISERS IN ", website)

        advertisers = []

        # Load the JSON file
        with open(filename, 'r') as file:

            for line in file:

                data = json.loads(line)

                # Replace 'your_key_here' with the key you're looking for
                values1 = unpack_string_from_nested_list(list(find_values(data, 'advertiserDomains')))
                values2 = unpack_string_from_nested_list(list(find_values(data, 'hb_adomain')))

                if values1 is not None and len(values1)>0 and values1 not in advertisers:
                    advertisers.append(values1)
                
                if values2 is not None and len(values2)>0 and values2 not in advertisers:
                    advertisers.append(values2)

        for ad in advertisers:
            print(ad)
            if ad not in global_advertisers:
                global_advertisers[ad] = {website}
            else:
                global_advertisers[ad].add(website)


    print('=========FINAL==========')
    print(global_advertisers)



    # Create a graph
    G = nx.Graph()

    # Add nodes and edges
    for advertiser, websites in global_advertisers.items():
        G.add_node(advertiser, type='advertiser')
        for website in websites:
            G.add_node(website, type='website')
            G.add_edge(advertiser, website)

    # Define node colors based on type
    color_map = []
    for node in G:
        if G.nodes[node]['type'] == 'advertiser':
            color_map.append('lightblue')
        else:  # Website
            color_map.append('lightgreen')

    # Draw the network
    plt.figure(figsize=(120, 110))
    nx.draw(G, with_labels=True, node_color=color_map, node_size=2000, font_size=10, font_weight='bold')
    plt.title('Network Graph of Advertisers and Websites')
    plt.show()

    for key in global_advertisers.keys():
        print(key)




    

if __name__ == "__main__":
    main()