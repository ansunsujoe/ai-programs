from data import data1
import numpy as np
from sklearn.preprocessing import LabelEncoder

def interval_round(num, interval):
    return (num // interval) * interval

def gini_impurity(array):
    return 1 - np.sum(np.square(array / array.sum()))

class Index:
    def __init__(self):
        pass
    
    def add(self, dataset):
        pass
    
    def clear(self):
        pass
    
class ContainsIndex(Index):
    def __init__(self, attr_name, interval):
        super().__init__()
        self.attr_name = attr_name
        self.interval = interval
        self.index_dict = {}
        
    def add(self, dataset):
        for d in dataset.data:
            l = self.encode_label(d)
            for val in d.get(self.attr_name):
                key = interval_round(val, self.interval)
                if key not in self.index_dict:
                    self.index_dict[key] = np.zeros(self.n_classes)
                self.index_dict[key][l] += 1
                
    def clear(self):
        self.index_dict = {}

class Dataset:
    def __init__(self, data, label_name):
        self.data = data
        self.label_name = label_name
        self.indices = {}
        
    def init_classes(self):
        # Gather all the labels
        labels = []
        for d in self.data:
            labels.append(d.get(self.label_name))
            
        # Label encoding
        self.le = LabelEncoder()
        self.le.fit(labels)
        self.n_classes = self.le.classes_.shape[0]
        
    def encode_label(self, d):
        return self.le.transform([d.get(self.label_name)])[0]
        
    def add_index(self, index_type, attr_name, **kwargs):
        if index_type == "contains":
            self.add_contains_index(attr_name, kwargs.get("interval"))
    
    def add_contains_index(self, attr_name, interval):
        index_dict = {}
        
        self.indices[f"contains_{attr_name}"] = index_dict

class DTree:
    def __init__(self):
        self.indices = {}
    
    def fit(self, data):
        self.init_classes(data)


if __name__ == "__main__":
    dataset = Dataset(data1, label_name="label")
    print(dataset.add_index("contains", "abc", interval=1))