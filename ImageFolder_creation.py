import pandas as pd
import os
from sklearn.model_selection import train_test_split

# First data cleaning
df = pd.read_csv('labels.csv', sep =",")

df = df.dropna()

# On enlève les lignes en trop à cause des multiples enregistrements de la dataframe
df.drop_duplicates(keep = 'first', inplace=True)


df.to_csv("labels_clean.csv")


#Creation of the folders
train = r"C:\Users\jeronimo\OneDrive - IMT MINES ALES\Documents\3A\Oedeep\Dataset\train"
valid = r"C:\Users\jeronimo\OneDrive - IMT MINES ALES\Documents\3A\Oedeep\Dataset\val"
test = r"C:\Users\jeronimo\OneDrive - IMT MINES ALES\Documents\3A\Oedeep\Dataset\test"
for i in range(0, 41):
    valid_path = os.path.join(valid, str(i))
    train_path = os.path.join(train, str(i))
    test_path = os.path.join(test, str(i))
    os.makedirs(test_path)
    os.makedirs(valid_path)
    os.makedirs(train_path)


# Filling the folders with images
X = df["id_img"]
y = df["labels"]
X_train, X_rem, y_train, y_rem = train_test_split(X, y, test_size=0.3, random_state=42)
X_valid, X_test, y_valid, y_test = train_test_split(X_rem, y_rem, test_size=0.5)
path_img = r"C:\Users\jeronimo\OneDrive - IMT MINES ALES\Documents\3A\Oedeep\jpg_files"
parent_dir = r"C:\Users\jeronimo\OneDrive - IMT MINES ALES\Documents\3A\Oedeep\Dataset"

for index, row in df.iterrows():
    ind = int(row["id_img"])
    genre = int(row["labels"])
    file = str(int(ind)) + ".jpg"
    path = r'C:\Users\jeronimo\OneDrive - IMT MINES ALES\Documents\3A\Oedeep\jpg_files\%s' % file
    print(path)
    new_path = os.path.join(parent_dir, str(genre))
    if ind in X_train.unique():
        new_path = os.path.join(train, str(genre))

    elif ind in X_test.unique():
        new_path = os.path.join(test, str(genre))
    else:
        new_path = os.path.join(valid, str(genre))
    new_path = os.path.join(new_path, str(int(ind)) + ".jpg")
    print(new_path)
    os.rename(path, new_path)

