'''
Filter JSON following pybioclip and V51 pass.
'''

#from bioclip import CustomLabelsClassifier
import polars as pl
import json
import argparse
#import uuid

EXPECTED_COLS = ["filepath", "kingdom", "phylum", "class", "order", "family", "genus", "species", "unknown", "abiotic"]
TAXA_COLS = EXPECTED_COLS[:-2]


def get_json_tags(v51_json):
  '''
  Creates a DataFrame with all images and the ranks that were classified for images in V51.
  
  Args:

  '''
  taxa_by_image = {}
  df = pl.DataFrame(schema = EXPECTED_COLS)
  for i in range(len(v51_json["samples"])):
    img_info = v51_json["samples"][i]
    taxa_by_image["filepath"] = img_info["filepath"]
    for tag in img_info["tags"]:
      tag_parts = tag.split("_")
      if tag_parts[0] not in EXPECTED_COLS:
        print(f"The preface {tag_parts[0]} associated with image {taxa_by_image['filepath']} is not an column ({EXPECTED_COLS}), please note it will not be included")
        continue
      taxa_by_image[tag_parts[0]] = tag_parts[1]
    df = pl.concat([df, pl.DataFrame(data = taxa_by_image)], how = "diagonal_relaxed")

  return df


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--json-path", required = True, help = "path to json output from V51")
  parser.add_argument("--output-path", required = True, help = "where to save classification CSV (ex: V51_first_classification.csv)")
  args = parser.parse_args()
  with open(args.json_path) as file:
    v51_json = json.load(file)
  df = get_json_tags(v51_json)
  print(f"Writing prediction table to {args.output_path}")
  df.write_csv(args.output_path)

'''
classifier = CustomLabelsClassifier(["insect", "hole"])
predictions = classifier.predict("example_moth.jpg")
for prediction in predictions:
   print(prediction["classification"], prediction["score"])
'''
