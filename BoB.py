'''
from bioclip import TreeOfLifeClassifier, Rank

classifier = TreeOfLifeClassifier()
predictions = classifier.predict("Ursus-arctos.jpeg", Rank.SPECIES)
df = pd.DataFrame(predictions)




C:\RPI\Liquid Serau Radio Hill\2024-08-09\detected_and_cropped_images





Import list of taxa from just specific region in GBIF

FEED THAT LIST to Bioclip

Fee the folder to bioclip of images
'''


#import pygbif
#from pygbif import occurrences as occ
import sys
sys.path.append('/home/pi/.local/lib/python3.10/site-packages/')
#import pandas as pd
sys.path.append('/home/pi/.local/lib/python3/dist-packages') 
#import '/home/pi/.local/lib/python3.10/site-packages/pandas' as pd
import bioclip
from bioclip import CustomLabelsClassifier
import csv
import os


def get_taxa_by_geo_and_class(_country, _class):
  """
  Retrieves a list of taxa for a given country and taxonomic rank.

  Args:
    country: The name of the country.
    rank: The desired taxonomic rank.

  """

  # Perform the GBIF occurrence search
  #occ_search = occ.search(params)
  
  occ_search= occ.search(country=_country, 
                         #q='Insecta',
                         #order='Lepidoptera',
                         #taxon='H6',
                         classKey =_class,
                         #kingdom='Animals',
                         #limit=1
                         )
  #occ_search =  occ.search(taxonKey = x, limit=0)
  
  results = occ_search['results'] # get the results as a list
  print(len(results))
  #print(results)



def load_taxon_keys(file_path, encoding='utf-8'):
  """Loads taxon keys from a tab-delimited CSV file into a list.

  Args:
    file_path: Path to the CSV file.
    encoding: Encoding of the CSV file (default: 'utf-8').

  Returns:
    A list of taxon keys.
  """

  taxon_keys = []
  with open(file_path, 'r', encoding=encoding) as csvfile:
    reader = csv.DictReader(csvfile, delimiter='\t')
    for row in reader:
      taxon_keys.append(row['order'])
  return taxon_keys

def remove_duplicates(taxon_keys):
  """Removes duplicate entries from a list of taxon keys.

  Args:
    taxon_keys: A list of taxon keys.

  Returns:
    A list of unique taxon keys.
  """

  unique_keys = list(set(taxon_keys))
  return unique_keys


def process_subdirectories(input_path, out_path):
    """Processes subdirectories within the specified input path, excluding "output_path".

    Args:
    input_path: The path to the directory containing subdirectories.
    out_path: Path to the subdirectory to exclude
    """

    for subdir in os.listdir(input_path):
        subdirectory_path = os.path.join(input_path, subdir)
        if os.path.isdir(subdirectory_path) and subdirectory_path != out_path:

            print(f"Processing subdirectory: {subdirectory_path}")
            process_files_in_directory(subdirectory_path)

def process_files_in_directory(subdirectory_path):
    """Processes files within a specified subdirectory.

    Args:
    subdirectory_path: The path to the subdirectory containing files.
    """

    # Example: Print all file names in the subdirectory
    for file in os.listdir(subdirectory_path):
        file_path = os.path.join(subdirectory_path, file)
        if os.path.isfile(file_path):
            print(f"File: {file_path}")
    
    sub_output_folder="detected_and_cropped_images"
    #sub_output_path = subdirectory_path+"/"+output_folder
    # Create the output directory if it doesn't exist
    #if not os.path.exists(sub_output_path):
    #    os.makedirs(sub_output_path)


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
            
            classifier = CustomLabelsClassifier(taxon_keys_list)
            #classifier = CustomLabelsClassifier(["insect","bear","stopsign","car", "hole", "circle", "lepidopteran", "beetle"])
            #classifier = CustomLabelsClassifier(["insect","bear","stopsign","car","other", "hole", "circle", "lepidopteran", "beetle"])

            results = classifier.predict(data)
            #results = model.predict(source=data, imgsz=1024)
            # Extract OBB coordinates and crop
            #for result in results:
            #  print(result["classification"], result["score"])

            sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)

            # Get the highest scoring result
            winner = sorted_results[0]

            # Print the winner
            print(filename+f"  This is the winner: {winner['classification']} with a score of {winner['score']}")





'''
country = 'PA' #2 letter country code https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2 "Panama"==PA
classKey = '216'
taxa_df = get_taxa_by_geo_and_class(country, classKey)
#print(taxa_df.head())
'''

taxon_keys_list = load_taxon_keys('taxa.csv')
print(len(taxon_keys_list))
taxon_keys_list=remove_duplicates(taxon_keys_list)
print(len(taxon_keys_list))

#classifier = CustomLabelsClassifier(taxon_keys_list)
print(taxon_keys_list)

input_path=r"C:\BoB\BucketsofBugs\TestFolder5" #raw string
print(input_path)
#input_path = input_path.encode('utf-8').decode('mbcs')
input_path= os.path.normpath(input_path)
print(input_path)
process_files_in_directory(input_path)

'''
classifier = CustomLabelsClassifier(["insect", "hole"])
predictions = classifier.predict("example_moth.jpg")
for prediction in predictions:
   print(prediction["classification"], prediction["score"])
'''