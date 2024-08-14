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
import json
import uuid

# MVP for testing uses these images, will require re-write to pass options
INPUT_PATH = "test_images"
TAXA_COLS = ["kingdom", "phylum", "class", "order", "family", "genus", "species"]
TAXA_KEYS_CSV = "taxa.csv"
image_list=[]
tags=[]

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


def process_subdirectories(input_path, out_path):
    '''
    Processes subdirectories within the specified input path, excluding "output_path".

    Args:
    input_path: The path to the directory containing subdirectories.
    out_path: Path to the subdirectory to exclude
    '''

    for subdir in os.listdir(input_path):
        subdirectory_path = os.path.join(input_path, subdir)
        if os.path.isdir(subdirectory_path) and subdirectory_path != out_path:

            print(f"Processing subdirectory: {subdirectory_path}")
            process_files_in_directory(subdirectory_path)


def process_files_in_directory(subdirectory_path, classifier):
    '''
    Processes files within a specified subdirectory.

    Args:
    subdirectory_path: The path to the subdirectory containing files.
    '''

    # Example: Print all file names in the subdirectory
    for file in os.listdir(subdirectory_path):
        file_path = os.path.join(subdirectory_path, file)
        if os.path.isfile(file_path):
            print(f"File: {file_path}")

    img_list = [f for f in os.listdir(subdirectory_path) if f.endswith(".jpg")]
    
    if not img_list:
        # No imgs were found in base level
        print("No .jpg images found in the input path: "+subdirectory_path)
    else:
        # Analyze the files
        print(f"Found {len(img_list)} .jpg images.")
        i=1
        for file in img_list:
            filename = os.path.splitext(file)[0]
            #print(filename)
            data = os.path.join(subdirectory_path, file)
            print("\n img # "+str(i)+"  out of "+str(len(img_list)))
            i=i+1
            # Run inference
            print("Predict a new image")

            results = classifier.predict(data)
            sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)
            # Get the highest scoring result
            winner = sorted_results[0]

            # Print the winner
            print(filename+f"  This is the winner: {winner['classification']} with a score of {winner['score']}")

def create_json(image_list, tags):
  """
  Creates a JSON file with the specified structure, containing image filepaths and tags.

  Args:
    image_list: A list of image filepaths.
    tags: A list of tags corresponding to each image.

  Returns:
    None
  """

  if len(image_list) != len(tags):
    raise ValueError("Image list and tags must have the same length")
  samples = []
  #dataset_id = str(uuid.uuid4()) #test and see if it accepts a UUID later! 
  i=0
  for filepath, tag in zip(image_list, tags):
    i=i+1
    sample = {
      "_id": i,
      "filepath": filepath,
      "tags": [tag],
      "_media_type": "image",
      "_dataset_id": "2"
    }
    samples.append(sample)

  data = {"samples": samples}

  with open("samples.json", "w") as f:
    json.dump(data, f, indent=2)


if __name__ == "__main__":
  taxon_keys_list = load_taxon_keys(TAXA_KEYS_CSV)
  print(f"We are predicting from the following {len(taxon_keys_list)} taxon keys: {taxon_keys_list}")

  classifier = CustomLabelsClassifier(taxon_keys_list)
  process_files_in_directory(INPUT_PATH, classifier)
  create_json(image_list, tags)


'''
classifier = CustomLabelsClassifier(["insect", "hole"])
predictions = classifier.predict("example_moth.jpg")
for prediction in predictions:
   print(prediction["classification"], prediction["score"])
'''
