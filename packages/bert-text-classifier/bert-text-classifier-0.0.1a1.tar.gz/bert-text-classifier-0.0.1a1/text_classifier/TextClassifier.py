# Libraries
import matplotlib.pyplot as plt
import pandas as pd
import torch
from torchtext.data import Field, TabularDataset, BucketIterator, Iterator
import torch.nn as nn
from transformers import BertTokenizer, BertForSequenceClassification
import torch.optim as optim
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import seaborn as sns


# Internal Functions
if __name__ == "__main__":
    from BERT import BERT, save_checkpoint, load_checkpoint, save_metrics, load_metrics
else:
    from .BERT import BERT, save_checkpoint, load_checkpoint, save_metrics, load_metrics

class TextClassifier():
    """
    Allows classification of text with BERT and minimal effort
    """
    def __init__(self, num_logits = 2, device='auto', fn=None):
        """Initialize the model .

        Args:
            num_logits (int, optional): Number of classes being predicted. Defaults to 2.
            device (str, optional): 'auto' will select the first cuda device if available, otherwise CPU. You can also provide a device string. Defaults to 'auto'.
            fn (str, optional): Path to a .pt model file to load, if None it will start from a pretrained BERT model. Defaults to None.
        """
        self.num_logits = num_logits
        # Setup device
        if device == 'auto':
            self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        else:
            self.device = device
        self.model = BERT(num_logits).to(self.device)
        if fn is not None:
            self.load(fn)
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased') #TODO Configurable tokenizer

    def setup_folders(self, source_folder, destination_folder, batch_size=16):
        """Setup the fields, data, and iterators for training/evaluation .

        Args:
            source_folder (str): Folder containing a train.csv, valid.csv, and test.csv with columns [label, input_text] in that order with no index column
            destination_folder (str): Folder within which to save the model and metadata
            batch_size (int, optional): Batch size to use for training the model. Defaults to 16.
        """
        self.destination_folder = destination_folder
        
        # PASTA JUNK

        # Model parameter
        self.MAX_SEQ_LEN = 128
        self.PAD_INDEX = self.tokenizer.convert_tokens_to_ids(self.tokenizer.pad_token) #TODO: What is this?
        self.UNK_INDEX = self.tokenizer.convert_tokens_to_ids(self.tokenizer.unk_token) #TODO: What is this?

        # Fields

        self.label_field = Field(sequential=False, use_vocab=False, batch_first=True, dtype=torch.float)
        self.text_field = Field(use_vocab=False, tokenize=self.tokenizer.encode, lower=False, include_lengths=False, batch_first=True,
                        fix_length=self.MAX_SEQ_LEN, pad_token=self.PAD_INDEX, unk_token=self.UNK_INDEX)
        
        colnames = pd.read_csv(f"{source_folder}/train.csv", nrows=0).columns.tolist()
        colname_to_field = {'label' : self.label_field, 'input_text' : self.text_field}
        self.fields = [(colname, colname_to_field[colname]) for colname in colnames]

        # TabularDataset

        self.train_data, self.valid_data, self.test_data = TabularDataset.splits(path=source_folder, train='train.csv', validation='valid.csv',
                                                test='test.csv', format='CSV', fields=self.fields, skip_header=True)

        # Iterators

        self.train_iter = BucketIterator(self.train_data, batch_size=batch_size, sort_key=lambda x: len(x.input_text),
                                    device=self.device, train=True, sort=True, sort_within_batch=True)
        self.valid_iter = BucketIterator(self.valid_data, batch_size=batch_size, sort_key=lambda x: len(x.input_text),
                                    device=self.device, train=True, sort=True, sort_within_batch=True)
        self.test_iter = Iterator(self.test_data, batch_size=batch_size, device=self.device, train=False, shuffle=False, sort=False)
    
    def save(self, save_path, valid_loss=999999999):
        """Save model to file .

        Args:
            save_path (str): path to save the model at, should end in '.pt'
            valid_loss (int, optional): Validation loss for this model. Defaults to 999999999.
        """
        save_checkpoint(save_path, self.model, valid_loss)

    def load(self, save_path):
        """Loads the model from disk .

        Args:
            save_path (str): Path to the model file (.pt)
        """
        load_checkpoint(save_path, self.model, self.device)
        
    def train(self,
            criterion = nn.BCELoss(),
            num_epochs = 5,
            best_valid_loss = float("Inf"),
            lr=2e-5):
        """Train the model on the device .

        Args:
            criterion (pytorch loss to use, optional): [description]. Defaults to nn.BCELoss().
            num_epochs (int, optional): Number of epochs to train for. Defaults to 5.
            best_valid_loss (float, optional): Validation loss of the starting model. Defaults to float("Inf").
        """
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)

        eval_every = len(self.train_iter) // 2
        model = self.model
        optimizer = self.optimizer
        file_path = self.destination_folder
        train_loader = self.train_iter
        valid_loader = self.valid_iter
        # initialize running values
        running_loss = 0.0
        valid_running_loss = 0.0
        global_step = 0
        train_loss_list = []
        valid_loss_list = []
        global_steps_list = []

        # training loop
        model.train()
        for epoch in range(num_epochs):
            for (labels, input_text), _ in train_loader:
                labels = labels.type(torch.LongTensor)           
                labels = labels.to(self.device)
                input_text = input_text.type(torch.LongTensor)  
                input_text = input_text.to(self.device)
                output = model(input_text, labels)
                loss, _ = output

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                # update running values
                running_loss += loss.item()
                global_step += 1

                # evaluation step
                if global_step % eval_every == 0:
                    model.eval()
                    with torch.no_grad():                    

                        # validation loop
                        for (labels, input_text), _ in valid_loader:
                            labels = labels.type(torch.LongTensor)           
                            labels = labels.to(self.device)
                            input_text = input_text.type(torch.LongTensor)  
                            input_text = input_text.to(self.device)
                            output = model(input_text, labels)
                            loss, _ = output
                            
                            valid_running_loss += loss.item()

                    # evaluation
                    average_train_loss = running_loss / eval_every
                    average_valid_loss = valid_running_loss / len(valid_loader)
                    train_loss_list.append(average_train_loss)
                    valid_loss_list.append(average_valid_loss)
                    global_steps_list.append(global_step)

                    # resetting running values
                    running_loss = 0.0                
                    valid_running_loss = 0.0
                    model.train()

                    # print progress
                    print('Epoch [{}/{}], Step [{}/{}], Train Loss: {:.4f}, Valid Loss: {:.4f}'
                        .format(epoch+1, num_epochs, global_step, num_epochs*len(train_loader),
                                average_train_loss, average_valid_loss))
                    
                    # checkpoint
                    if best_valid_loss > average_valid_loss:
                        best_valid_loss = average_valid_loss
                        save_checkpoint(file_path + '/' + 'model.pt', model, best_valid_loss)
                        save_metrics(file_path + '/' + 'metrics.pt', train_loss_list, valid_loss_list, global_steps_list)
        
        save_metrics(file_path + '/' + 'metrics.pt', train_loss_list, valid_loss_list, global_steps_list)
        print('Finished Training!')
    
    def predict(self, text_data):
        """Predict with the model for the given text_data .

        Args:
            text_data (str): input text

        Returns:
            tensor: model outputs
        """
        # TODO : code to handle batched inputs
        self.model.eval()
        with torch.no_grad():
            input_text = torch.tensor([self.tokenizer.encode(text_data, padding='max_length', max_length=self.MAX_SEQ_LEN)])
            input_text = input_text.type(torch.LongTensor)
            input_text = input_text.to(self.device)
            output = self.model(input_text)
            return output

    def evaluate(self):
        """Evaluate the model on the test set .
        """
        y_pred = []
        y_true = []
        
        model = self.model
        test_loader = self.test_iter

        model.eval()
        with torch.no_grad():
            for (labels, input_text), _ in test_loader:
                    labels = labels.type(torch.LongTensor)           
                    labels = labels.to(self.device)
                    input_text = input_text.type(torch.LongTensor)  
                    input_text = input_text.to(self.device)
                    output = model(input_text, labels)

                    _, output = output
                    y_pred.extend(torch.argmax(output, 1).tolist())
                    y_true.extend(labels.tolist())
        
        print('Classification Report:')
        print(classification_report(y_true, y_pred, labels=[1,0], digits=4))
        
        # cm = confusion_matrix(y_true, y_pred, labels=[1,0])
        # ax= plt.subplot()
        # sns.heatmap(cm, annot=True, ax = ax, cmap='Blues', fmt="d")

        # ax.set_title('Confusion Matrix')

        # ax.set_xlabel('Predicted Labels')
        # ax.set_ylabel('True Labels')

        # ax.xaxis.set_ticklabels(['FAKE', 'REAL'])
        # ax.yaxis.set_ticklabels(['FAKE', 'REAL'])

if __name__ == "__main__":
    source_folder = 'comment_data'#'news_data'
    destination_folder = 'comment_output'#'news_output'
    tc = TextClassifier()
    tc.setup_folders(source_folder, destination_folder)
    tc.evaluate()
    print(tc.predict("Rogue marines take hold of small towns across Afghanistan"))
    tc.train()
    tc.evaluate()
    print(tc.predict("Rogue marines take hold of small towns across Afghanistan"))
