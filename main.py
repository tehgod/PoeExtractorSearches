import json
from math import floor

master_patch_data = "data.json" #https://github.com/grindinggear/skilltree-export/blob/master/data.json
annoitments_filename = "annoitments.json"
config_filename = "config.json"
searches_filename = "searches.json"
output_filename = "output.json"


with open(config_filename) as myfile: 
    data=json.load(myfile)
    prices = data["Prices"]
    profit_target = data["ProfitPerTrade"]
with open(annoitments_filename) as myfile: annoitments = json.load(myfile)
with open(searches_filename) as myfile: searches = json.load(myfile)

def generate_skill_annoitments_mappings(data:json): 
    with open(master_patch_data) as myfile:
        data =json.load(myfile)
    skills = data["nodes"]
    annoitments=[]
    for skill in skills:
        if "recipe" in skills[skill]:
            annoitments.append({
                "Oil #1": skills[skill]["recipe"][0].replace("Oil", " Oil"),
                "Oil #2": skills[skill]["recipe"][1].replace("Oil", " Oil"),
                "Oil #3": skills[skill]["recipe"][2].replace("Oil", " Oil"),
                "Outcome": skills[skill]["name"]
            })
    with open("skill_annoitments.json", "w") as myfile:
        json.dump(annoitments, myfile)

def calculate_value(annoitment):
    try:
        name = annoitment["Outcome"]
    except:
        name = "Does Not Exist"
    oil1_value=prices[annoitment['Oil #1']]
    oil2_value=prices[annoitment['Oil #2']]
    oil3_value=prices[annoitment['Oil #3']] if annoitment['Oil #3']!=None else None
    extractor_value=prices["Oil Extractor"]
    if oil3_value==None:
        expected_value =((oil1_value+oil2_value)-(2*extractor_value))/2
    else:
        expected_value =((oil1_value+oil2_value+oil3_value)-(3*extractor_value))/3
    return {"Name":name, "Value":expected_value}

def calculate_all_values():
    values = []
    for annoitment in annoitments:
        values.append(calculate_value(annoitment))
    return sorted(values, key=lambda d: d['Value'], reverse=True)

def generate_url(profit_tier:int):
    for endpoint in searches["endpoints"]:
        if endpoint["tier"]==profit_tier:
            url = searches["baseURL"]+endpoint["urlEndpoint"]
            return url

def calculate_max_buyprice(annoitment_values:list, annoitments):
    minimum_value = profit_target*2
    if type(annoitments)==str:
        for item in annoitment_values:
            if item["Name"]==annoitments:
                return floor(item["Value"]-minimum_value)
    if type(annoitments)==list:
        lowest_value = prices["Golden Oil"]
        for item in annoitments:
            for item2 in annoitment_values:
                if item == item2["Name"]:
                    if lowest_value>item2["Value"]:
                        lowest_value=item2["Value"]
        return floor(lowest_value-minimum_value)
    if type(annoitments)==int:
        for search in searches["endpoints"]:
            if search["tier"]==annoitments:
                annoitments_list = search["annoitments"]
        return calculate_max_buyprice(annoitment_values, annoitments_list)



if __name__=="__main__":
    search_tiers = [x for x in range(1,len(searches["endpoints"])+1,1)]
    annoitment_values = calculate_all_values()
    output_strings = []
    for tier in search_tiers:
        max_buyprice = calculate_max_buyprice(annoitment_values, tier)
        if max_buyprice>2:
            output_strings.append(f"Tier: {tier}\nURL: {generate_url(tier)}\nMax Price: {max_buyprice}\n\n")
    with open(output_filename, "w") as myfile:
        myfile.writelines(output_strings)
    