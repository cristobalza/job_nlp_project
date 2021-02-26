import pandas as pd
import trainer_model
import torch
import torch.nn as nn
import transformers
from sklearn import metrics, model_selection
from transformers import AdamW, get_linear_schedule_with_warmup


class SalaryModel:
    def __init__(self, review, target):
        self.review = review
        self.target = target
        self.tokenizer = transformers.BertTokenizer.from_pretrained(
            "bert-base-uncased", do_lower_case=True
        )
        self.max_len = 64

    def __len__(self):
        return len(self.review)

    def __getitem__(self, item):
        review = str(self.review[item])
        review = " ".join(review.split())

        inputs = self.tokenizer.encode_plus(
            review,
            None,
            add_special_tokens=True,
            max_length=self.max_len,
            padding="max_length",
            truncation=True,
        )

        ids = inputs["input_ids"]
        mask = inputs["attention_mask"]
        token_type_ids = inputs["token_type_ids"]

        return {
            "ids": torch.tensor(ids, dtype=torch.long),
            "mask": torch.tensor(mask, dtype=torch.long),
            "token_type_ids": torch.tensor(token_type_ids, dtype=torch.long),
            "targets": torch.tensor(self.target[item], dtype=torch.float),
        }


class SalaryModel_Delta(trainer_model.Model):
    def __init__(self, num_train_steps):
        super().__init__()
        self.tokenizer = transformers.BertTokenizer.from_pretrained(
            "bert-base-uncased", do_lower_case=True
        )
        self.bert = transformers.BertModel.from_pretrained(
            "bert-base-uncased", return_dict=False
        )
        self.bert_drop = nn.Dropout(0.3)
        self.out = nn.Linear(768, 1)
        self.num_train_steps = num_train_steps
        self.step_scheduler_after = "batch"

    def fetch_optimizer(self):
        param_optimizer = list(self.named_parameters())
        no_decay = ["bias", "LayerNorm.bias"]
        optimizer_parameters = [
            {
                "params": [
                    p for n, p in param_optimizer if not any(nd in n for nd in no_decay)
                ],
                "weight_decay": 0.001,
            },
            {
                "params": [
                    p for n, p in param_optimizer if any(nd in n for nd in no_decay)
                ],
                "weight_decay": 0.0,
            },
        ]
        opt = AdamW(optimizer_parameters, lr=3e-5)
        return opt

    def fetch_scheduler(self):
        sch = get_linear_schedule_with_warmup(
            self.optimizer, num_warmup_steps=0, num_training_steps=self.num_train_steps
        )
        return sch

    def loss(self, outputs, targets):
        if targets is None:
            return None
        return nn.BCEWithLogitsLoss()(outputs, targets.view(-1, 1))

    def monitor_metrics(self, outputs, targets):
        if targets is None:
            return {}
        outputs = torch.sigmoid(outputs).cpu().detach().numpy() >= 0.5
        targets = targets.cpu().detach().numpy()
        accuracy = metrics.accuracy_score(targets, outputs)
        return {"accuracy": accuracy}

    def forward(self, ids, mask, token_type_ids, targets=None):
        _, o_2 = self.bert(ids, attention_mask=mask, token_type_ids=token_type_ids)
        b_o = self.bert_drop(o_2)
        output = self.out(b_o)
        loss = self.loss(output, targets)
        acc = self.monitor_metrics(output, targets)
        return output, loss, acc


if __name__ == "__main__":
    df = pd.read_csv("./data/final_only_salary_us_data_jobs.csv")

    cut_bins = [0,50000,70000,90000,120000,150000, 300000, 600000]
    df['salary_bins'] = pd.cut(df['yearly_adjusted_salary'],
                                            bins=cut_bins, 
                                            labels = False)

    text = df['combined_text']
    target_class = df['salary_bins'].astype('category')
    X_train, X_test, y_train, y_test = train_test_split(text, target_class, test_size=0.1, random_state=4)

    df_train = df_train.reset_index(drop=True)
    df_valid = df_valid.reset_index(drop=True)

    tdidf = TfidfVectorizer(sublinear_tf = True, min_df=0.01, max_df=0.5, ngram_range=(1,3), stop_words='english')
    fitted_vectorizer = tdidf.fit(X_train)
    tfidf_vectorizer_vectors = fitted_vectorizer.transform(X_train)

    train_dataset = SalaryModel(
        review=tfidf_vectorizer_vectors, target=y_train
    )

    valid_dataset = SalaryModel(
        review=tfidf_vectorizer_vectors, target=y_test
    )

    n_train_steps = int(len(df_train) / 32 * 10)
    model = SalaryModel_Delta(num_train_steps=n_train_steps)

    # es = trainer_model.callbacks.EarlyStopping(monitor="valid_loss", model_path="model.bin")
    model.fit(
        train_dataset,
        valid_dataset=valid_dataset,
        train_bs=32,
        device="cuda",
        epochs=50,
        fp16=True,
    )
    with open(r"./binary_models/fitted_vectorizer.pkl", "wb") as f:
        pickle.dump(tfidf_vectorizer, f)  


    # model = SGDClassifier(alpha=0.0001, max_iter=500, n_jobs=3).fit(tfidf_vectorizer_vectors, y)

    # Create a new pickle file based on the best model
    with open(r"./binary_models/finalized_sgd_model.pkl", "wb") as f:  
        pickle.dump(clf, f)