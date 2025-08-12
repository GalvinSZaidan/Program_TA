import numpy as np
import pandas as pd
import tensorflow as tf
import joblib
from sklearn.preprocessing import StandardScaler

# Load the trained model
save_model_path = 'C:\\Users\galvi\Documents\Kuliah\Tugas Akhir/Program/model_ann_8/modelann91.h5'  # Sesuaikan dengan path model yang disimpan
model = tf.keras.models.load_model(save_model_path)

# Load the scaler
scaler_path = 'C:\\Users\galvi\Documents\Kuliah\Tugas Akhir\Program\model_ann_8/scaler91.pkl'  # Sesuaikan dengan path scaler yang disimpan
scaler = joblib.load(scaler_path)

# Load and preprocess new data for inference
url_new_data = 'C:\\Users\galvi\Documents\Kuliah\Tugas Akhir\Data\Hasil Perekaman Alat 5 lead\Hasil Klasifikasi\HasilOlahDataDuduk-oldmean.xlsx'  # Path to the new dataset for inference
data_new = pd.read_excel(url_new_data)

# Split features and target
X_new = data_new.drop(columns=['aktual']).values
y_new = data_new['aktual'].values  # If you want to compare predictions with actual labels

# Normalize features using the same scaler used during training
X_new_normalized = scaler.transform(X_new)  # Use transform instead of fit_transform

# Make predictions
y_pred_new = model.predict(X_new_normalized)
y_pred_classes_new = np.argmax(y_pred_new, axis=1) + 1  # Add 1 to return to original class labels (1-4)

# Map the predicted classes to the respective labels
class_mapping = {
    1: 'Abnormal',
    2: 'Normal',
    3: 'Berpotensi Aritmia',
    4: 'Sangat Berpotensi Aritmia'
}
y_pred_labels_new = np.vectorize(class_mapping.get)(y_pred_classes_new)

# Print predicted classes
print("Prediksi kelas untuk data baru:")
print(y_pred_labels_new)

# Create a DataFrame with original data and predicted classes
data_new['Klasifikasi Model'] = y_pred_labels_new

# Save the DataFrame to an Excel file
output_file = 'C:\\Users\galvi\Documents\Kuliah\Tugas Akhir\Data\Hasil Perekaman Alat 5 lead\Hasil Klasifikasi/hasil_prediksi_oldmean.xlsx'  # Sesuaikan dengan path yang diinginkan
data_new.to_excel(output_file, index=False)
print(f"Hasil prediksi telah disimpan ke {output_file}")
