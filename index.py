from IPython.display import display 
from PIL import Image
import random
import json
import os

os.system('cls' if os.name=='nt' else 'clear')

def create_new_image(all_images, config):
    new_image = {}
    for layer in config["layers"]:
      new_image[layer["name"]] = random.choices(layer["values"], layer["weights"])[0]
    
    for incomp in config["incompatibilities"]:
      for attr in new_image:
        if new_image[incomp["layer"]] == incomp["value"] and new_image[attr] in incomp["incompatible_with"]:
          return create_new_image(all_images, config)

    if new_image in all_images:
      return create_new_image(all_images, config)
    else:
      return new_image

def generate_unique_images(amount, config):
  print("Generating {} unique NFTs...".format(amount))
  pad_amount = len(str(amount));
  trait_files = {
  }
  for trait in config["layers"]:
    trait_files[trait["name"]] = {}
    for x, key in enumerate(trait["values"]):
      trait_files[trait["name"]][key] = trait["filename"][x];
  
  all_images = []
  for i in range(amount): 
    new_trait_image = create_new_image(all_images, config)
    all_images.append(new_trait_image)

  i = 0
  for item in all_images:
      item["tokenId"] = i
      i += 1

  for i, token in enumerate(all_images):
    attributes = []
    for key in token:
      if key != "tokenId":
        attributes.append({"trait_type": key, "value": token[key]})
    token_metadata = {
        "image": config["baseURI"] + "/images/" + str(token["tokenId"]) + '.png',
        "tokenId": token["tokenId"],
        "name":  config["name"] + str(token["tokenId"]).zfill(pad_amount),
        "description": config["description"],
        "attributes": attributes
    }
    with open('./metadata/' + str(token["tokenId"]) + '.json', 'w') as outfile:
        json.dump(token_metadata, outfile, indent=4)

  with open('./metadata/all-objects.json', 'w') as outfile:
    json.dump(all_images, outfile, indent=4)
  
  for item in all_images:
    layers = [];
    for index, attr in enumerate(item):
      if attr != 'tokenId':
        layers.append([])
        layers[index] = Image.open(f'{config["layers"][index]["trait_path"]}/{trait_files[attr][item[attr]]}.png').convert('RGBA')

    if len(layers) == 1:
      rgb_im = layers[0].convert('RGB')
      file_name = str(item["tokenId"]) + ".png"
      rgb_im.save("./images/" + file_name)
    elif len(layers) == 2:
      main_composite = Image.alpha_composite(layers[0], layers[1])
      rgb_im = main_composite.convert('RGB')
      file_name = str(item["tokenId"]) + ".png"
      rgb_im.save("./images/" + file_name)
    elif len(layers) >= 3:
      main_composite = Image.alpha_composite(layers[0], layers[1])
      layers.pop(0)
      layers.pop(0)
      for index, remaining in enumerate(layers):
        main_composite = Image.alpha_composite(main_composite, remaining)
      rgb_im = main_composite.convert('RGB')
      file_name = str(item["tokenId"]) + ".png"
      rgb_im.save("./images/" + file_name)
  
  print("\nUnique NFT's generated.")
  cid = input("IPFS Image CID (): ")
  if len(cid) > 0:
    if not cid.startswith("ipfs://"):
      cid = "ipfs://{}".format(cid)
    if cid.endswith("/"):
      cid = cid[:-1]
    for i, item in enumerate(all_images):
      with open('./metadata/' + str(item["tokenId"]) + '.json', 'r') as infile:
        original_json = json.loads(infile.read())
        original_json["image"] = original_json["image"].replace(config["baseURI"]+"/", cid+"/")
        with open('./metadata/' + str(item["tokenId"]) + '.json', 'w') as outfile:
          json.dump(original_json, outfile, indent=4)

generate_unique_images(20, {
  "layers": [
    {
      "name": "gen",
      "values": ["1","2","3","4","5"],
      "trait_path": "./trait-layers/backgrounds",
      "filename": ["1","2","3","4","5"],
      "weights": [20,20,20,20,20]
    },

     {
      "name": "random #",
       "values": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10","11", "12", "13", "14", "15", "16", "17", "18", "19","20", "21", "22", "23", "24", "25", "26", "27", "28","29", "30", "31", "32", "33", "34", "35", "36", "37","38", "39", "40", "41", "42", "43", "44", "45", "46","47", "48", "49", "50", "51", "52", "53", "54", "55","56", "57", "58", "59", "60", "61", "62", "63", "64","65", "66", "67", "68", "69", "70", "71", "72", "73","74", "75", "76", "77", "78", "79", "80", "81", "82","83", "84", "85", "86", "87", "88", "89", "90", "91","92", "93", "94", "95", "96", "97", "98", "99", "100"],
      "trait_path": "./trait-layers/backgrounds",
      "filename": ["text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text","text"],
      "weights": [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    },
     {
     "name": "rarity",
      "values": ["Common", "Uncommon", "Rare", "Epic", "Legendary"],
      "trait_path": "./trait-layers/rarity",
      "filename": ["blue", "orange", "purple", "red", "yellow"],
      "weights": [40,35,15,9.09,0.01]
    },
    {
      "name": "lvl",
      "values": ["1","1"],
      "trait_path": "./trait-layers/backgrounds",
      "filename": ["text", "text"],
      "weights": [50, 50]
      
    },
     {
      "name": "-",
      "values": ["1","1"],
      "trait_path": "./trait-layers/backgrounds",
      "filename": ["text", "text"],
      "weights": [50, 50]
      
    },
    {
      "name": "title",
      "values": ["Cooker", "Octopus","Cat","Witcher","Ilon","Santa","Shrek" ],
      "trait_path": "./trait-layers/nft",
      "filename": ["cooker", "octopus", "cat", "witcher", "ilon","santa","shrek"],
      "weights": [20,20,20,20,20,20,20]
    },
  

  ],
  "incompatibilities": [
    {
      "layer": "title",
      "value": "Cooker",
      "incompatible_with": ["Uncommon", "Rare", "Epic", "Legendary"]
    },
    {
      "layer": "title",
      "value": "Octopus",
      "incompatible_with": ["Common", "Rare", "Epic", "Legendary"]
    },
    {
      "layer": "title",
      "value": "Cat",
      "incompatible_with": ["Common", "Uncommon", "Epic", "Legendary"]
    },
    {
      "layer": "title",
      "value": "Witcher",
      "incompatible_with": ["Common", "Uncommon", "Rare", "Legendary"]
    },
     {
      "layer": "title",
      "value": "Ilon",
      "incompatible_with": ["Common", "Uncommon", "Rare", "Epic"]
    },
     {
      "layer": "title",
      "value": "Shrek",
      "incompatible_with": ["Common", "Rare", "Epic","Legendary"]
    },
     {
      "layer": "title",
      "value": "Santa",
      "incompatible_with": ["Common", "Uncommon", "Epic","Legendary"]
    },
    
  ],
  "baseURI": ".",
  "name": "NFT #",
  "description": "Generation 0"
})
