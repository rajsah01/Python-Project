import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

import pandas as pd

sample_data = {
    'GrLivArea': [1710, 1262, 1786, 1717, 2198],
    'OverallQual': [7, 6, 7, 7, 8],
    'TotalBsmtSF': [856, 1262, 920, 756, 1145],
    'GarageCars': [2, 2, 2, 3, 3],
    'GarageArea': [548, 460, 608, 642, 836],
    'YearBuilt': [2003, 1976, 2001, 1915, 2000],
    'SalePrice': [208500, 181500, 223500, 140000, 250000],
    'Neighborhood': ['CollgCr', 'Veenker', 'CollgCr', 'Crawfor', 'NoRidge'],
    'LotFrontage': [65.0, 80.0, 68.0, 60.0, 84.0],
    'GarageType': ['Attchd', 'Attchd', 'Attchd', 'Detchd', 'Attchd'],
    'Alley': [None, None, None, None, None],
    'PoolQC': [None, None, None, None, None],
    'Fence': [None, None, None, None, None],
    'MiscFeature': [None, None, None, None, None]
}

df_sample = pd.DataFrame(sample_data)

# Save it to CSV (this will create 'train.csv' in your working directory)
df_sample.to_csv("train.csv", index=False)

print("✅ 'train.csv' file created.")


df = pd.read_csv("train.csv")
print("First 5 rows:")
print(df.head())


print("\nDataset Info:")
print(df.info())

print("\nMissing Values (Top):")
missing = df.isnull().sum()
print(missing[missing > 0].sort_values(ascending=False))

df.drop(['Alley', 'PoolQC', 'Fence', 'MiscFeature'], axis=1, inplace=True)

df['LotFrontage'].fillna(df['LotFrontage'].median(), inplace=True)
df['GarageType'].fillna('None', inplace=True)
df.dropna(inplace=True)  


plt.figure(figsize=(12, 6))
sns.barplot(x='Neighborhood', y='SalePrice', data=df, estimator=np.mean, palette='Blues_d')
plt.xticks(rotation=45)
plt.title("Average House Price by Neighborhood")
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 6))
sns.scatterplot(x='GrLivArea', y='SalePrice', data=df, alpha=0.6)
plt.title("Living Area vs Sale Price")
plt.tight_layout()
plt.show()

corr_matrix = df.corr(numeric_only=True)
top_corr = corr_matrix['SalePrice'].sort_values(ascending=False)[1:11]

plt.figure(figsize=(10, 6))
sns.heatmap(df[top_corr.index.tolist() + ['SalePrice']].corr(), annot=True, cmap='coolwarm')
plt.title("Top Features Correlated with Sale Price")
plt.tight_layout()
plt.show()

features = ['GrLivArea', 'OverallQual', 'TotalBsmtSF', 'GarageCars', 'GarageArea', 'YearBuilt']
X = df[features]
y = df['SalePrice']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print(f"\n📈 Linear Regression Performance:")
print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
print(f"R-squared (R²): {r2:.2f}")

new_data = pd.DataFrame({
    'GrLivArea': [2000],
    'OverallQual': [7],
    'TotalBsmtSF': [1000],
    'GarageCars': [2],
    'GarageArea': [500],
    'YearBuilt': [2005]
})

predicted_price = model.predict(new_data)
print(f"\n🏠 Predicted House Price for Sample Input: ${predicted_price[0]:,.2f}")