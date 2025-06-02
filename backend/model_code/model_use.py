import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
from sklearn.metrics import classification_report, roc_auc_score, f1_score, accuracy_score, precision_recall_curve
from sklearn.metrics import confusion_matrix
import xgboost as xgb


def get_train_data(files_list):
    combined_data = []
    header_columns = None

    for i, file_path in enumerate(files_list):
        try:
            if i == 0:
                df = pd.read_excel(file_path)
                if df.empty:
                    raise ValueError(f"Первый файл пустой: {file_path}")
                header_columns = df.columns
            else:
                df = pd.read_excel(file_path, header=None, skiprows=1)
                if df.empty:
                    print(f"[SKIP] Пустой файл пропущен: {file_path}")
                    continue
                if df.shape[1] != len(header_columns):
                    raise ValueError(f"Файл {file_path} имеет {df.shape[1]} столбцов, ожидалось {len(header_columns)}")
                df.columns = header_columns

            combined_data.append(df)
        except Exception as e:
            print(f"[ERROR] Ошибка при чтении файла {file_path}: {e}")
            raise

    if not combined_data:
        raise ValueError("Нет данных для объединения")

    result_df = pd.concat(combined_data, ignore_index=True)
    print(f"[SUCCESS] Итоговый размер: {result_df.shape}")
    return result_df


def get_test_data(files_list):
    combined_data = []
    header_columns = None

    for i, file_path in enumerate(files_list):
        try:
            if i == 0:
                df = pd.read_excel(file_path)
                if df.empty:
                    raise ValueError(f"Первый файл пустой: {file_path}")
                header_columns = df.columns
            else:
                df = pd.read_excel(file_path, header=None, skiprows=1)
                if df.empty:
                    print(f"[SKIP] Пустой файл пропущен: {file_path}")
                    continue
                if df.shape[1] != len(header_columns):
                    raise ValueError(f"Файл {file_path} имеет {df.shape[1]} столбцов, ожидалось {len(header_columns)}")
                df.columns = header_columns

            combined_data.append(df)
        except Exception as e:
            print(f"[ERROR] Ошибка при чтении файла {file_path}: {e}")
            raise

    if not combined_data:
        raise ValueError("Нет данных для объединения")

    result_df = pd.concat(combined_data, ignore_index=True)
    print(f"[SUCCESS] Итоговый размер: {result_df.shape}")
    return result_df

def data_preprocessing(df):
    df = df[df['SpecialRight'] == 0]
    df = df.rename(columns={'SE': 'y'})
    df = df.drop('id', axis=1)
    df = df.drop('Entered', axis=1)
    df = df.drop('WithoutExams', axis=1)
    df = df.drop('SpecialRight', axis=1)
    df = df.drop('TargetQuota', axis=1)

    # Разделение
    X = df.drop(columns=['y'])
    y = df['y']
    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=42, test_size=0.2)
    return X_train, X_test, y_train, y_test




def get_scaler_data(X_train, X_test, y_train):

    scaler = StandardScaler()
    cols_to_scale = ['Achievements', 'Exams', 'Dormitory'] 

    X_train[cols_to_scale] = scaler.fit_transform(X_train[cols_to_scale])
    X_test[cols_to_scale] = scaler.transform(X_test[cols_to_scale])

    # Балансируем train через SMOTE
    smote = SMOTE(random_state=42)

    X_resampled, y_resampled = smote.fit_resample(X_train, y_train)
    return X_resampled, y_resampled, scaler

def clf_fit(X_resampled, y_resampled):
    scale_pos_weight = 1  

    clf = xgb.XGBClassifier(
        objective='binary:logistic',
        eval_metric='logloss',
        use_label_encoder=False,
        random_state=42,
        scale_pos_weight=scale_pos_weight, 
        max_depth=5,
        learning_rate=0.1,
        n_estimators=100
    )

    clf.fit(X_resampled, y_resampled)
    return clf

def get_predictions(clf, X_test, y_test):
    y_scores = clf.predict_proba(X_test)[:, 1]

    # Подбор порога threshold по F1
    thresholds = np.linspace(0.01, 0.99, 100)
    f1_scores = [f1_score(y_test, (y_scores >= t).astype(int)) for t in thresholds]

    best_threshold = thresholds[np.argmax(f1_scores)]
    print(f"Лучший threshold по F1: {best_threshold:.3f}, F1: {max(f1_scores):.3f}")

    y_pred = (y_scores >= best_threshold).astype(int)

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    print("ROC AUC:", roc_auc_score(y_test, y_scores))

    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    print("\nConfusion matrix:")
    print(cm)
    return y_pred

def predict_data(X_train, X_new, scaler, clf):

    orig = X_new.copy(deep=True)

    columns_to_drop = ['SE', 'Entered', 'id', 'WithoutExams', 'SpecialRight', 'TargetQuota']
    existing_columns = [col for col in columns_to_drop if col in X_new.columns]
    X_new = X_new.drop(columns=existing_columns)

    # Выбор колонок
    X_new = X_new[X_train.columns]  
    X_new = X_new.fillna(0)
    X_new[['Achievements', 'Exams', 'Dormitory']] = scaler.transform(X_new[['Achievements', 'Exams', 'Dormitory']])

    new_probs = clf.predict_proba(X_new)[:, 1]

    # Оптимальный threshold
    best_threshold = 0.67 
    new_preds = (new_probs >= best_threshold).astype(int)

    # Добавление столбцов
    orig['predicted_class'] = new_preds
    orig['probability'] = new_probs


    # Сохранение с сортировкой

    orig = orig.sort_values(by=['predicted_class', 'Exams'], ascending=False)
    return orig

def get_score(file):

    # Строки, где predicted == 1
    predicted_ones = file[file['predicted_class'] == 1]

    if predicted_ones.empty:
        min_score = 0  
    else:
        # Берем min Exams
        min_score = predicted_ones['Exams'].min()

    return min_score



def merge_excel_files(files_list, empty_files_paths, number=0):
    df = get_train_data(files_list)
    print(111)
    print(empty_files_paths)
    X_new = get_test_data(empty_files_paths)
    print(222)
    X_train, X_test, y_train, y_test = data_preprocessing(df)
    print(333)
    X_resampled, y_resampled, scaler = get_scaler_data(X_train, X_test, y_train)
    print(444)
    clf = clf_fit(X_resampled, y_resampled)
    print(555)
    y_pred = get_predictions(clf, X_test, y_test)
    file = predict_data(X_train, X_new, scaler, clf)
    print(666)
    print('ok')
    min_score = get_score(file)

    return file, min_score

