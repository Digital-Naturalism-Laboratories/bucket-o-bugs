import meerkat as mk
import rich

df = mk.from_csv("datasets/bug/bug.csv")
IMAGE_COL = "img"
LABEL_COL = "label"

df["img"] = mk.image("datasets/bug/" + df["image_path"])

# Unique classes in the dataset.
labels = list(df[LABEL_COL].unique())

# Give the user a way to select a class.
class_selector = mk.gui.Select(
    values=list(labels),
    value=labels[0],
)

# Filter the dataset to the selected class. Use a reactive function.
@mk.reactive()
def filter_by_class(df: mk.DataFrame, label: str):
    return df[df[LABEL_COL] == label]

filtered_df = filter_by_class(df, class_selector.value)

"""Select a random subset of images from the filtered dataset."""
@mk.reactive()
def random_images(df: mk.DataFrame):
    # Sample 16 images from the filtered dataset.
    # `images` will be a `Column` object.
    images = df[IMAGE_COL]
    
    # Encode the images as base64 strings.
    # Use a `Formatter` object to do this.
    formatter = images.formatters['base']

    # All Formatter objects have an `encode` method that
    # can be used to take a data object and encode it in some way.
    return [formatter.encode(img) for img in images]

images = random_images(filtered_df)

# Make a grid with 4 columns
grid = mk.gui.html.gridcols4([
    # Use equal-sized square boxes in the grid
    mk.gui.html.div(
        # Wrap the image in a `mk.gui.Image` component
        mk.gui.Image(data=img),
        style="aspect-ratio: 1 / 1",
    )
    for img in images
], classes="gap-2") # Add some spacing in the grid.

layout = mk.gui.html.flexcol([
    mk.gui.html.div(
        [mk.gui.Caption("Choose a class:"), class_selector],
        classes="flex justify-center items-center mb-2 gap-4"
    ),
    grid,
])

page = mk.gui.Page(component=layout, id="tutorial-2")
page.launch()
