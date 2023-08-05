<img src="http://zed.uchicago.edu/logo/logozed1.png" alt="logo" width="500" />

# Data Smashing

Quantifier of universal similarity amongst arbitrary data streams without a priori knowledge, features, or training.

Can be used to solve time series clustering and classification problems.

Featurization algorithms: SymbolicDerivative, InferredHMMLikelihood, Csmash
	
Distance measure: LikelihoodDistance

For questions or suggestions contact:zed@uchicago.edu

##	Usage examples	
### SymbolicDerivative
	from timesmash import SymbolicDerivative
	from sklearn.ensemble import RandomForestClassifier

	train = [[1, 0, 1, 0, 1, 0], [1, 1, 0, 1, 1, 0]]
	train_label = [[0], [1]]
	test = [[0, 1, 1, 0, 1, 1]]
	train_features, test_features = SymbolicDerivative().fit_transform(
	    train=train, test=test, label=train_label
	)
	clf = RandomForestClassifier(random_state=1).fit(train_features, train_label)
	label = clf.predict(test_features)
	print("Predicted label: ", label)
	
###	LikelihoodDistance	
	from timesmash import LikelihoodDistance
	from sklearn.cluster import KMeans
	train = [[1, 0, 1.1, 0, 11.2, 0], [1, 1, 0, 1, 1, 0], [0, 0.9, 0, 1, 0, 1], [0, 1, 1, 0, 1, 1]]
	dist_calc = LikelihoodDistance().fit(train)
	dist = dist_calc.produce()
	from sklearn.cluster import KMeans
	clusters = KMeans(n_clusters = 2).fit(dist).labels_
	print("Clusters: " clusters)
	
###	InferredHMMLikelihood	
	from timesmash import InferredHMMLikelihood
	from sklearn.ensemble import RandomForestClassifier

	train = [[1, 0, 1, 0, 1, 0], [1, 1, 0, 1, 1, 0]]
	train_label = [[0], [1]]
	test = [[0, 1, 1, 0, 1, 1]]
	train_features, test_features = InferredHMMLikelihood().fit_transform(
	    train=train, test=test, label=train_label
	)
	clf = RandomForestClassifier(random_state=1).fit(train_features, train_label)
	label = clf.predict(test_features)
	print("Predicted label: ", label)

###	ClusteredHMMClassifier:	
	from timesmash import Quantizer, InferredHMMLikelihood, LikelihoodDistance
	from sklearn.cluster import KMeans
	from sklearn.ensemble import RandomForestClassifier
	import pandas as pd

	train = pd.DataFrame(
	    [[1, 0, 1, 0, 1, 0], [1, 1, 0, 1, 1, 0], [1, 0, 1, 0, 1, 0], [1, 1, 0, 1, 1, 0]]
	)
	train_label = pd.DataFrame([[0], [1], [0], [1]])
	test = pd.DataFrame([[0, 1, 1, 0, 1, 1]])

	qtz = Quantizer().fit(train, label=train_label)
	new_labels = train_label.copy()
	for label, dataframe in train_label.groupby(train_label.columns[0]):
	    dist = LikelihoodDistance(quantizer=qtz).fit(train.loc[dataframe.index]).produce()
	    sub_labels = KMeans(n_clusters=2, random_state=0).fit(dist).labels_
	    new_label_names = [str(label) + "_" + str(i) for i in sub_labels]
	    new_labels.loc[dataframe.index, train_label.columns[0]] = new_label_names

	featurizer = InferredHMMLikelihood(quantizer=qtz, epsilon=0.01)
	train_features, test_features = featurizer.fit_transform(
	    train=train, test=test, label=new_labels
	)

	clf = RandomForestClassifier().fit(train_features, train_label)
	print("Predicted label: ", clf.predict(test_features))
	


