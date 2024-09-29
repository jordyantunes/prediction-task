from pathlib import Path
from typing import List, Tuple
import torch
from torch.autograd import Variable
import json
from scripts.train import (
    N_LETTERS,
    lineToTensor,
    RNN,
)


# Just return an output given a line
def evaluate(line_tensor, weights_file: Path, params):
    rnn = RNN(
        input_size=N_LETTERS,
        hidden_size=params["n_hidden"],
        output_size=params["n_categories"],
    )
    rnn.load_state_dict(torch.load(weights_file, weights_only=True))
    rnn.eval()
    hidden = rnn.initHidden()

    for i in range(line_tensor.size()[0]):
        output, hidden = rnn(line_tensor[i], hidden)

    return output


def predict(
    name, n_predictions: int, weights_file: Path, params_file: Path
) -> List[Tuple[torch.Tensor, str]]:
    with open(params_file, "r") as f:
        params = json.load(f)
    print(f"{N_LETTERS=}, {params['n_hidden']=}, {params['n_categories']=}")
    output = evaluate(
        Variable(lineToTensor(name)), weights_file=weights_file, params=params
    )

    # Get top N categories
    topv, topi = output.data.topk(n_predictions, 1, True)
    predictions = []

    for i in range(n_predictions):
        value = topv[0][i]
        category_index = topi[0][i]
        # print("(%.2f) %s" % (value, all_categories[category_index]))
        predictions.append([value, params["all_categories"][category_index]])

    return predictions


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument(
        "-w",
        type=Path,
        default=Path("./experiments/weights.pt"),
        help="path to model weights",
    )
    parser.add_argument(
        "-p",
        type=Path,
        default=Path("./experiments/params.json"),
        help="path to trained model params",
    )
    parser.add_argument(
        "-n", type=int, default=3, help="return top n mosty likely classes"
    )
    parser.add_argument("name", type=str, help="name to classify")
    args = parser.parse_args()

    predict(
        name=args.name, n_predictions=args.n, weights_file=args.w, params_file=args.p
    )
