import torch
import torch.nn as nn
import torch.nn.functional as F


class ClassificatorModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(in_features=1024, out_features=14)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.fc1(x)
        return x

class Classificator(nn.Module):
    def __init__(self):
        super().__init__()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = ClassificatorModel().to(self.device)
        self.model.load_state_dict(
            torch.load('endpoints/views/local_model/model_weights_v1.pth',
                       map_location=self.device)
        )
        self.model.eval()
        self.categories_names = ['Окружающая среда', 'Внутренняя политика',
        'Финансы и рынки', 'Криптовалюта и блокчейн', 'Внешняя политика', 'Криминал',
        'Культура и традиции', 'Бизнес и стартапы', 'Международная политика',
        'Кибербезопасность', 'Гаджеты и софт', 'ИИ и BigData', 'Наука',
        'Социальные проблемы']

    def predict(self, embedding):
        with torch.no_grad():
            probabilities = F.softmax(self.model(embedding))
        category_prob_pairs = list(zip(self.categories_names, probabilities.cpu().tolist()))
        result = []
        for category, probability in category_prob_pairs:
            if probability > 0.1:
                result.append(category)
        return result
