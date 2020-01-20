import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier

iris_dataset = pd.read_csv("Iris.csv")

print(iris_dataset.head())

s = (iris_dataset.dtypes == 'object')
object_cols = list(s[s].index)
print(object_cols)

ir_cop = iris_dataset.copy()
label = LabelEncoder()
ir_cop['Species'] = label.fit_transform(iris_dataset['Species'])
print(ir_cop.head())

y = ir_cop.Species
iris_features = ['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm']
X = ir_cop[iris_features].copy()

X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=0.8, test_size=0.2,
                                                      random_state=0)

clf = RandomForestClassifier(random_state=0, n_estimators=100)
clf.fit(X_train, y_train)
clf.score(X_valid, y_valid)

scores = cross_val_score(clf, X, y, cv=5)
print(scores)
