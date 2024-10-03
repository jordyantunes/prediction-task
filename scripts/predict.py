import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import torch
from torch.autograd import Variable

from scripts.train import N_LETTERS, RNN, lineToTensor


def load_model(weights_file: Path, params: Dict) -> RNN:
    rnn = RNN(
        input_size=N_LETTERS,
        hidden_size=params["n_hidden"],
        output_size=params["n_categories"],
    )
    rnn.load_state_dict(torch.load(weights_file, weights_only=True))
    return rnn


# Just return an output given a line
def evaluate(rnn: RNN, line_tensor):
    rnn.eval()
    hidden = rnn.initHidden()

    for i in range(line_tensor.size()[0]):
        output, hidden = rnn(line_tensor[i], hidden)

    return output


def predict(
    name,
    n_predictions: int,
    params: Dict,
    rnn: Optional[RNN] = None,
    weights_file: Optional[Path] = None,
) -> List[Tuple[torch.Tensor, str]]:
    if rnn is None:
        if weights_file is None:
            raise ValueError("Either rnn or weights_file must be provided")
        rnn = load_model(weights_file, params)

    print(f"{N_LETTERS=}, {params['n_hidden']=}, {params['n_categories']=}")
    output = evaluate(rnn, Variable(lineToTensor(name)))

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

    with open(args.p, "r") as f:
        params = json.load(f)

    predict(name=args.name, n_predictions=args.n, weights_file=args.w, params=params)
