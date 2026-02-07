import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from lightgbm import LGBMClassifier

df = pd.read_csv("/content/heart.csv")

def find_prediction(Age, Sex, ChestPainType, RestingBP, Cholesterol, FastingBS, RestingECG, MaxHR, ExerciseAngina, Oldpeak, ST_Slope):
  
  label_encoder = LabelEncoder()

  df['Sex'] = label_encoder.fit_transform(df['Sex'])  # Male: 1, Female: 0

  df['ChestPainType'] = label_encoder.fit_transform(df['ChestPainType'])  # ASY:0, NAP:1, ATA:2, TA:3

  df['RestingECG'] = label_encoder.fit_transform(df['RestingECG'])  # Normal:1, LVH:0, ST:2

  df['ExerciseAngina'] = label_encoder.fit_transform(df['ExerciseAngina'])  # N: 0, Y: 1

  df['ST_Slope'] = label_encoder.fit_transform(df['ST_Slope'])  # Flat: 1, Up: 2, Down: 0

  X = df[['Age', 'Sex', 'ChestPainType', 'RestingBP', 'Cholesterol', 'FastingBS', 'RestingECG', 'MaxHR', 'ExerciseAngina', 'Oldpeak', 'ST_Slope']]
  y = df["HeartDisease"]

  scaler = StandardScaler()
  X_scaled = scaler.fit_transform(X)

  X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

  model = LGBMClassifier(colsample_bytree=0.8334, force_row_wise=True, learning_rate=0.141, max_bin=90, max_depth=3, min_child_samples= 3, n_estimators= 40, num_leaves= 8, random_state= 38, verbose= -1)
  model.fit(X_train,y_train)

  my_pred = new_model.predict(Age, Sex, ChestPainType, RestingBP, Cholesterol, FastingBS, RestingECG, MaxHR, ExerciseAngina, Oldpeak, ST_Slope)
  
  return max(0.0, round(my_pred[0], 2))
