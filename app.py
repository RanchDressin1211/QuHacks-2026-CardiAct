from flask import Flask, request, jsonify, send_from_directory


import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from lightgbm import LGBMClassifier

df = pd.read_csv("heart.csv")

def find_prediction(Age, Sex, ChestPainType, RestingBP, Cholesterol, FastingBS,
       RestingECG, MaxHR, ExerciseAngina, Oldpeak, ST_Slope):

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

  new_data = pd.DataFrame({
    'Age': [Age],
    'Sex': [Sex],
    'ChestPainType': [ChestPainType],
    'RestingBP': [RestingBP],
    'Cholesterol': [Cholesterol],
    'FastingBS': [FastingBS],
    'RestingECG': [RestingECG],
    'MaxHR': [MaxHR],
    'ExerciseAngina': [ExerciseAngina],
    'Oldpeak': [Oldpeak],
    'ST_Slope': [ST_Slope],
  })


  my_pred = model.predict(new_data)

  return max(0.0, round(my_pred[0], 2))

app = Flask(__name__)


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json() or {}
    try:
        age = float(data.get('Age', 0))
        sex = 1 if data.get('Sex', 0)=="M" else 0
        chestpain = ["ASY","NAP","ATA","TA"].index(data.get('ChestPainType', 0))
        restingbp = float(data.get('RestingBP', 0))
        cholesterol = float(data.get('Cholesterol', 0))
        fastingbs = float(data.get('FastingBS', 0))
        restingecg = ["LVH","Normal","ST"].index(data.get('RestingECG', 0))
        maxhr = float(data.get('MaxHR', 0))
        exerciseangina = 0 if data.get('ExerciseAngina', 0)=="N" else 1
        oldpeak = float(data.get('Oldpeak', 0))
        stslope = ["Down","Flat","Up"].index(data.get('ST_Slope', 0))
    except (TypeError, ValueError):
        return jsonify({'error': 'invalid input'}), 400

    prediction = find_prediction(age, sex, chestpain, restingbp, cholesterol, fastingbs, restingecg, maxhr, exerciseangina, oldpeak, stslope)

    return jsonify({'prediction': int(prediction)})


@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory('.', path)


@app.route('/')
def root():
    return send_from_directory('.', 'index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
