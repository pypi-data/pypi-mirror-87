from .tagger import Tagger

class CrossTrainer:

    def __init__(self, workers=1):
        self.workers = workers
        # best tagger model
        self.tagger = None
        # architecture for the best model
        self.arch = None
        self.reports = []


    def _get_taggers(self):
        """
        Retrieves all Tagger model option combinations.
        :return: List of Tagger objects.
        """
        taggers = []
        for classifier in Tagger.CLASSIFIERS:
            for vectorizer in Tagger.VECTORIZERS:
                tagger = Tagger(classifier=classifier, vectorizer=vectorizer, workers=self.workers)
                taggers.append(tagger)
        return taggers


    def train(self, data_sample, field_list=[]):
        """
        Trains best Tagger model.
        :param dict data_sample: Dict containing training data. Dict keys are labels and values are either lists of texts or list of documents.
        :param list field_list: List of fieldnames used in training the model, e.g. ["text"].
        :return: Tagger object.
        """
        highest_score = 0
        for tagger in self._get_taggers():
            arch = {"classifier": tagger.classifier, "vectorizer": tagger.vectorizer}
            report = tagger.train(data_sample, field_list=field_list)
            if report.f1_score > highest_score:
                highest_score = report.f1_score
                self.tagger = tagger
                self.arch = arch
            # add report with architecture choices
            self.reports.append((arch, report.to_dict()))
        # return best tagger model
        return self.tagger
