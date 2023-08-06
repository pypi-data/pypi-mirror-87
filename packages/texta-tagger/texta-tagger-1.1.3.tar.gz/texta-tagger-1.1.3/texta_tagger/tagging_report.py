from sklearn.metrics import confusion_matrix, precision_score, recall_score, roc_curve, auc, f1_score
import json

class TaggingReport:

    def __init__(self, y_test, y_pred, y_scores, num_features, num_examples, classes):
        # check number of classes
        # if binary problem calculate roc
        if len(classes) == 2:
            self.average = "binary"
            # translate y_test to numerical on binary problems, because sklearn complains otherwise
            y_map = {k:i for i,k in enumerate(set(y_test))}
            y_test = [y_map[c] for c in y_test]
            y_pred = [y_map[c] for c in y_pred]
            fpr, tpr, _ = roc_curve(y_test, y_scores)
            self.true_positive_rate = tpr.tolist()
            self.false_positive_rate = fpr.tolist()
            self.area_under_curve = auc(fpr, tpr)
        else:
            self.average = "micro"
            self.area_under_curve = 0.0
            self.true_positive_rate = []
            self.false_positive_rate = []
        # general stats
        self.f1_score = f1_score(y_test, y_pred, average=self.average)
        self.confusion = confusion_matrix(y_test, y_pred)
        self.precision = precision_score(y_test, y_pred, average=self.average)
        self.recall = recall_score(y_test, y_pred, average=self.average)
        self.num_features = num_features
        self.num_examples = num_examples
        self.classes = classes
        
    def to_dict(self):
        return {
            "f1_score": round(self.f1_score, 5),
            "precision": round(self.precision, 5),
            "recall": round(self.recall, 5),
            "num_features": self.num_features,
            "num_examples": self.num_examples,
            "confusion_matrix": self.confusion.tolist(),
            "area_under_curve": round(self.area_under_curve, 5),
            "true_positive_rate": self.true_positive_rate, 
            "false_positive_rate": self.false_positive_rate,
            "classes": self.classes
        }
