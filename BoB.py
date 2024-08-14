'''
Get list of taxa from just specific region in GBIF
ex:
country = 'PA' #2 letter country code https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2 "Panama"==PA
classKey = '216'

FEED THAT LIST to Bioclip

Feed the folder to bioclip of images
'''

from bioclip import CustomLabelsClassifier
import polars as pl
import os
import sys
import json
#import uuid

# MVP for testing uses these images, will require re-write to pass options
DATA_PATH = "datasets/test_images/data"
JSON_PATH = f"{DATA_PATH.split(sep = '/data')[0]}/samples.json"
TAXA_COLS = ["kingdom", "phylum", "class", "order", "family", "genus", "species"]
TAXA_KEYS_CSV = "taxa.csv"


def load_taxon_keys(file_path, taxon_rank = "order", filter_holes = True):
  '''
  Loads taxon keys from a tab-delimited CSV file into a list.

  Args:
    file_path: String. Path to the taxa CSV file.
    taxon_rank: String. Taxonomic rank to which to classify images (must be present as column in the taxa csv at file_path). Default: "order".
    filter_holes: Boolean. Whether to filter holes and smudges (adds "hole" and "circle" to taxon_keys). Default: True.

  Returns:
    taxon_keys: List. A list of taxon keys to feed to the CustomClassifier for bioCLIP classification.
  '''
  df = pl.read_csv(file_path, low_memory = False).select(TAXA_COLS).filter(pl.col(taxon_rank).is_not_null())
  taxon_keys = pl.Series(df.select(pl.col(taxon_rank)).unique()).to_list()
  
  if filter_holes:
    taxon_keys.append("circle")
    taxon_keys.append("hole")
  
  return taxon_keys


def process_files_in_directory(input_path, classifier, taxon_rank = "order"):
    '''
    Processes files within a specified subdirectory.

    Args:
    input_path: String. The path to the directory containing files.
    classifier: CustomLabelsClassifier object from TAXA_KEYS_CSV.
    taxon_rank: String. Taxonomic rank to which to classify images (must be present as column in the taxa csv at file_path). Default: "order".
    '''

    # Example: Print all file names in the subdirectory
    for file in os.listdir(input_path):
        file_path = os.path.join(input_path, file)
        if os.path.isfile(file_path):
            print(f"File: {file_path}")

    img_list = [f for f in os.listdir(input_path) if f.endswith(".jpg")]
    
    if not img_list:
        # No imgs were found in base level
        sys.exit("No .jpg images found in the input path: " + input_path)
    else:
        predictions = {}
        # Analyze the files
        print(f"Found {len(img_list)} .jpg images. \n Getting predictions...")
        i=1
        for file in img_list:
            filename = os.path.splitext(file)[0]
            #print(filename)
            data = os.path.join(input_path, file)
            print(f"\n img # {str(i)} out of {str(len(img_list))}")
            i=i+1
            
            # Run inference
            results = classifier.predict(data)
            sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)
            # Get the highest scoring result
            winner = sorted_results[0]

            # Print the winner
            print(filename+f"  This is the winner: {winner['classification']} with a score of {winner['score']}")
            key = f"data/{file}"
            predictions[key] = taxon_rank + "_" + winner['classification']
    return predictions


def create_json(predictions, json_path):
  """
  Creates a JSON file with the specified structure, containing image filepaths and tags.

  Args:
    predictions: Dictionary with image filepaths as keys and prediction at given rank as values.
    json_path: String. Path to image directory (they must be in a 'data' folder at the lowest level for V51);
        JSON for V51 must be saved in directory containing the data directory.

  Returns:
    None
  """
  samples = []
  #dataset_id = str(uuid.uuid4()) #test and see if it accepts a UUID later! 
  i=0
  for filepath in predictions.keys():
    # revist structure of JSON for V51
    i=i+1
    sample = {
      "_id": i,
      "filepath": filepath,
      "tags": [predictions[filepath]],
      "_media_type": "image",
      "_dataset_id": "2"
    }
    samples.append(sample)

  data = {"samples": samples}
  with open(json_path, "w") as f:
    json.dump(data, f, indent=2)


if __name__ == "__main__":
  taxon_keys_list = load_taxon_keys(TAXA_KEYS_CSV)
  print(f"We are predicting from the following {len(taxon_keys_list)} taxon keys: {taxon_keys_list}")

  print("Loading CustomLabelsClassifier...")
  classifier = CustomLabelsClassifier(taxon_keys_list)
  predictions = process_files_in_directory(DATA_PATH, classifier)
  
  create_json(predictions, JSON_PATH)


'''
classifier = CustomLabelsClassifier(["insect", "hole"])
predictions = classifier.predict("example_moth.jpg")
for prediction in predictions:
   print(prediction["classification"], prediction["score"])
'''
