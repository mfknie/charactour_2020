import pandas as pd 
import numpy as np 
import argparse
import scipy 
import datetime
from sklearn.model_selection import train_test_split
from sklearn.metrics import hamming_loss, jaccard_score, f1_score
def make_generator(parameters):
    if not parameters:
        yield dict()
    else:
        key_to_iterate = list(parameters.keys())[0]
        next_round_parameters = {p : parameters[p]
                    for p in parameters if p != key_to_iterate}
        for val in parameters[key_to_iterate]:
            for pars in make_generator(next_round_parameters):
                temp_res = pars
                temp_res[key_to_iterate] = val
                yield temp_res

def handle_args():
    parser = ArgumentParser(description="Evaluates cosine similarity predictions for selected metric")
    parser.add_argument("--pred", required=True, help = "Predictions from cosine similarity ")
    parser.add_argument("--likes", required=True, help = "File with character likes - use as ground truth")
    parser.add_argument("--sample", type = int, required=True, help = "Number of users to evaluate over")
    parser.add_argument("--num_chrs", type = int, default = -1, help = "Number of characters to consider")
    parser.add_argument("--m", choices = ["F1", "Hamming", "Jaccard"], required=True, help = "metrics to use")
    return parser.parse_args()

if __name__ == "__main__":
    args = handle_args()
    # Assume same format as usermatchcharacters table in database
    pred = pd.read_csv(args.pred)
    likes = pd.read_csv(args.likes)

    # Filtering predictions
    # By recency of last previous update
    pred["lastupdate"] = pd.to_datetime(pred["last_update"], format=r"%Y-%m-%d %H:%M:%S")
    today = datetime.today()
    pred = pred[today - pred.lastupdate.date < datetime.delta(days=365)]
    # By number of characters liked
    if(args.num_chrs == -1):
        n_chars = 5 # default for now
    else:
        n_chars = args.num_chrs

    user_likes = likes.merge(pred["id"], left_on = "user_id", right_on = "id")
    # Getting rid of nonunique char likes per user 
    user_likes["updated_at"] = pd.to_datetime(user_likes["updated_at"], format=r"%Y-%m-%d %H:%M:%S")
    user_likes = user_likes.sort_values(by="updated_at", ignore_index=True).drop_duplicates(subset=["user_id", "likable_id"], keep = "first", ignore_index=True)
    
    qual_u_ids = user_likes.groupby(["user_id"]).count().query("likable_id > @n_chars")["user_id"]
    user_likes = user_likes.merge(qual_u_ids, left_on = "user_id", right_on = "user_id")
    

    # How should I choose which characters to evaluate, if a user has liked more characters than we want to predict? Will use most recent timestamps for now
    # TODO - numpy function to grab all top characters for each individual and add to matrix (may need to use numba)
    user_likes[["user_id", "likable_id"]].groupby('user_id').head(n_chars).reset_index(drop=True)
    true = np.zeros((args.sample, 5341)) 
    for i in range(args.sample):
        true[]

    if args.m == "F1":
        #explore parameters more https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html#sklearn.metrics.f1_score
        print(f1_score(true, pred, average = "macro"))
    elif args.m == "Hamming":
        print(hamming_loss(true, pred))
    else:
        print(jaccard_score(true, pred, average = "macro"))
    


'''
Inputs: assume cosine similarity prediction is already taken care of (no need for test splitting, just evaluate predicitons)
Need to get number of characters liked first (5331 as of data in database)
-In future, may want to use sparse array due to large number of 0s.


Look into http://scikit.ml/
'''