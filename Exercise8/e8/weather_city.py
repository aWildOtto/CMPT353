import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

OUTPUT_TEMPLATE = (
    'Model score: {score:.3g}\n'
)
def main():
	data_labelled = pd.read_csv(sys.argv[1])
	data_unlabelled = pd.read_csv(sys.argv[2])

	unknown_x = data_unlabelled.drop(columns = ['city','year']).values
	X = data_labelled.drop(columns = ['city','year']).values
	y = data_labelled['city'].values

	X_train, X_valid, y_train, y_valid = train_test_split(X,y)

	rf_model = make_pipeline(StandardScaler(), RandomForestClassifier(n_estimators=400, max_depth=10, min_samples_leaf=5))
	rf_model.fit(X_train, y_train)
	rf_score = rf_model.score(X_valid, y_valid)

	print(OUTPUT_TEMPLATE.format(score=rf_score))

	predictions = rf_model.predict(unknown_x)
	pd.Series(predictions).to_csv(sys.argv[3], index=False, header=False)
	"""
	df = pd.DataFrame({'truth': y_valid, 'prediction': rf_model.predict(X_valid)})
	print(df[df['truth'] != df['prediction']])
	"""

if __name__ == '__main__':
    main()
