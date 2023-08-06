import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import math
from aiopslibs.utils import FeaturesHandler, PlotUtilities
import  json
class SimpleTextClassifier(nn.Module):  # inherit pytorch's nn.Module
    """Text Classifier with 1 hidden layer 
    """
    def __init__(self, num_labels, vocab_size):
        super(SimpleTextClassifier, self).__init__() # call parent init

        # Define model with one hidden layer with 128 neurons
        self.linear1 = nn.Linear(vocab_size, 128)
        self.linear2 = nn.Linear(128, num_labels)

    def forward(self, feature_vec):
        # Define how data is passed through the model

        hidden1 = self.linear1(feature_vec).clamp(min=0) # ReLU
        output = self.linear2(hidden1)
        return F.log_softmax(output, dim=1)


class ModelsEvaluator:
    def __init__(self):
        self.featuresHandler = FeaturesHandler()

    def evaluate_model(self,model, eval_data, text_data):
        """Evaluate the model on the held-out evaluation data

        Return the f-value for disaster-related and the AUC
        """
        
        X_eval, y_eval, ids = eval_data

        related_confs = [] # related items and their confidence of being related
        not_related_confs = [] # not related items and their confidence of being _related_

        precision = 0.0
        recall = 0.0

        true_pos = 0.0 # true positives, etc 
        false_pos = 0.0
        false_neg = 0.0
        true_neg = 0.0
        
        true_pos_text = []
        false_neg_text = []
        false_pos_text = []
        true_neg_text = []

        with torch.no_grad():
            print("torch.no_grad() go:")
            for feature_vector, label, _id in zip(X_eval, y_eval, ids):
                log_probs = model(feature_vector)
                # get confidence that item is disaster-related
                prob_related = math.exp(log_probs.data.tolist()[0][1])

                #print("type(label) : ", type(label))
                if ((type(label) == str) & (label == "1")) |  ((type(label) == int) & (label == 1)):
                    # true label is disaster related
                    related_confs.append(prob_related)
                    if prob_related > 0.5:
                        true_pos += 1.0
                        true_pos_text.append(text_data[str(_id)][1])
                    else:
                        false_neg += 1.0
                        false_neg_text.append(text_data[str(_id)][1])
                else:
                    # not disaster-related
                    not_related_confs.append(prob_related)
                    if prob_related > 0.5:
                        false_pos += 1.0
                        false_pos_text.append(text_data[str(_id)][1])
                    else:
                        true_neg += 1.0
                        true_neg_text.append(text_data[str(_id)][1])

        # Get FScore
        if true_pos == 0.0:
            fscore = 0.0
        else:
            precision = true_pos / (true_pos + false_pos)
            recall = true_pos / (true_pos + false_neg)
            fscore = (2 * precision * recall) / (precision + recall)

        #print("precision :", precision)
        #print("recall :", recall)

        # GET AUC
        not_related_confs.sort()
        total_greater = 0 # count of how many total have higher confidence
        for conf in related_confs:
            for conf2 in not_related_confs:
                if conf < conf2:
                    break
                else:                  
                    total_greater += 1


        denom = len(not_related_confs) * len(related_confs)
        if denom == 0:
            auc = 0
        else:
            auc = total_greater / denom

        return[fscore, auc, precision, recall, true_pos, false_pos, false_neg, true_neg, true_pos_text, false_neg_text, false_pos_text, true_neg_text]

class SGDEngine:
    def __init__(self):
        self.fscores = []
        self.aucs = []
        self.precisions = []
        self.recalls = []

        self.featuresHandler = FeaturesHandler()
        self.modelsEvaluator = ModelsEvaluator()

    def get_trained_model(self):
        if self.model == None:
            raise Exception("You first had to execute process method before retrieve the trained model.")
        return self.model

    def get_metrics_by_batch(self):
        return self.fscores, self.aucs, self.precisions, self.recalls

    def process(self, model, eval_data, text_data, epochs, select_per_epoch):
        if model == None:
            raise Exception("model cannot be None")

        X_train, y_train, ids_train = eval_data

        self.model = model
        loss_function = nn.NLLLoss()
        optimizer = optim.SGD(self.model.parameters(), lr=0.01)

        #data = zip(X_train, y_train)

        for epoch in range(epochs):
            print("Epoch: " + str(epoch))

            
            epoch_X_train = X_train[:select_per_epoch]
            epoch_y_train = y_train[:select_per_epoch]
            epoch_ids_train = ids_train[:select_per_epoch]
            for item in zip(epoch_X_train, epoch_y_train):
                x, y = item

                self.model.zero_grad()
                target = torch.LongTensor([int(y)]) # pylint: disable=no-member
                log_probs = self.model(x)

                # compute loss function, do backward pass, and update the gradient
                loss = loss_function(log_probs, target)
                loss.backward()
                optimizer.step()

            train_data = epoch_X_train,epoch_y_train,epoch_ids_train
            fscore, auc, precision, recall, _, _, _, _, _, _, _, _ = self.modelsEvaluator.evaluate_model(self.model, train_data,text_data)
            self.fscores.append(fscore)
            self.aucs.append(auc)
            self.precisions.append(precision)
            self.recalls.append(recall)



class EvalModelPloter:
    def __init__(self, run):
        self.run = run
        self.modelsEvaluator = ModelsEvaluator()

    def _log_confusion_matrix_artefact(self, true_pos_text, false_neg_text,false_pos_text,true_neg_text):
        data = {}
        data["true_pos_text"] = true_pos_text
        data["false_neg_text"] = false_neg_text
        data["false_pos_text"] = false_pos_text
        data["true_neg_text"] = true_neg_text
        confusion_matrix_log = "confusion_matrix_log.json"
        with open("confusion_matrix_log.json", 'w') as outfile:
                json.dump(data, outfile)
        
        self.run.upload_file(name="confusion_matrix_log", path_or_stream=confusion_matrix_log)

    def evaluate(self, model, eval_data, text_data):
        """retrieve model metrics and log them in the Workspace

        Arguments:
            model {object} -- model object containing weights necessary for inference
            data {obejct} -- data used to evaluate the model
            feature_index {dict} -- bag-of-words 

        Raises:
            Exception: model cannot be empty
            Exception: data cannot be empty
            Exception: feature_index cannot be empty
        """
        #X_eval, y_eval,ids = eval_data

        if not model :
            raise Exception("model cannot be empty") 

        if not model :
            raise Exception("data cannot be empty") 

        if not model :
            raise Exception("feature_index cannot be empty") 

        # Evaluation of trained model thanks to evaluation data (evaluation_data)
        result = self.modelsEvaluator.evaluate_model(model, eval_data, text_data)
        fscore, auc, precision, recall, true_pos, false_pos, false_neg, true_neg,true_pos_text, false_neg_text, false_pos_text, true_neg_text = result
        # log fscore metric to azure experiment
        self.run.log("fscore", round(fscore,5))
        # log auc metric to azure experiment
        self.run.log("auc", round(auc,5))
        # log precision metric to azure experiment
        self.run.log("precision", round(precision,5))
        #log recall metric to azure experiment
        self.run.log("recall", round(recall,5)) 


        #self.run.log_list("true_pos_text",true_pos_text)
        #self.run.log_list("false_neg_text",false_neg_text)
        #self.run.log_list("false_pos_text",false_pos_text)
        #self.run.log_list("true_neg_text",true_neg_text)

        self._log_confusion_matrix_artefact(true_pos_text,false_neg_text,false_pos_text,true_neg_text)

        #plot cofusion matrix
        cm = [[int(true_pos), int(false_pos)], [int(false_neg), int(true_neg)]]
        cm_plot = PlotUtilities._get_confusion_matrix_plot(cm)
        self.run.log_image("Confusion Matrix", plot = cm_plot)


        return fscore, auc, precision, recall


