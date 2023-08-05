from sklearn.metrics import confusion_matrix, precision_score, recall_score, roc_curve, auc,f1_score
import json

class TaggingReport:

    def __init__(self, y_test, y_pred, y_scores, num_features, num_examples, average="micro"):
        self.f1_score = f1_score(y_test, y_pred, average=average)
        self.confusion = confusion_matrix(y_test, y_pred)
        self.precision = precision_score(y_test, y_pred, average=average)
        self.recall = recall_score(y_test, y_pred, average=average)
        self.num_features = num_features
        self.num_examples = num_examples
        
    def to_dict(self):
        return {
            "f1_score": round(self.f1_score, 5),
            "precision": round(self.precision, 5),
            "recall": round(self.recall, 5),
            "num_features": self.num_features,
            "num_examples": self.num_examples,
            "confusion_matrix": self.confusion.tolist()
        }
