# %%
import pandas as pd 
import numpy as np 
import argparse
from scipy.sparse import lil_matrix
import datetime
import mySQL
from sklearn.model_selection import train_test_split
from sklearn.metrics import hamming_loss, jaccard_score, f1_score
from collections import Counter

# %%
class PerctAction(argparse.Action):
    def __init__(self, option_strings, dest, **kwargs):
        super(PerctAction, self).__init__(option_strings, dest, **kwargs)
    def __call__(self, parser, namespace, values, option_strings=None):
        if values > 1:
            raise ValueError("You must use a value under 1.0")
        setattr(namespace, self.dest, values)

# %%
def handle_args():
    '''
    Helper function to handle arguments using argparse module
    '''
    parser = argparse.ArgumentParser(description="Evaluates cosine similarity predictions for selected metric")
    parser.add_argument("--pred", required=True, help = "Predictions from cosine similarity")
    parser.add_argument("--likes", required=True, help = "File with character likes - use as ground truth")
    parser.add_argument("--sample", type = float, default = 1.0, help = "Percentage of users to evaluate over", action=PerctAction)
    parser.add_argument("--type", 
        required = True, 
        choices = ["top_n", "percentile"], 
        help = "Type of evaluation to perform - compare top n characters predicted or look at cosine similarities of liked characters")
    parser.add_argument("--num_chrs", 
        required = "--type" in sys.argv, 
        type = int, 
        default = 5, 
        help = "Number of characters to consider")
    parser.add_argument("--m", 
        required = "--type" in sys.argv, 
        default = "F1", 
        choices = ["F1", "Hamming", "Jaccard"], 
        help = "Stats metrics to use")
    return parser.parse_args()

# %%
def top_n_keys(x, col, n=5):
    '''
    Return top n
    Inputs: 
    x - row of dataframe containing dictionary
    col - column where dictionary exists
    n - number of highest values to consider
    Output: keys where dictionary has top n values
    '''
    return [i for i, j in Counter(x[col]).most_common(5)]


# %%
def eval_top_n(pred, likes, n_chars, score_type):
    '''
    Evaluate quality of prediction by comparing top n characters in actual likes and predictions
    Input:
    pred - pandas dataframe of cosine similarity values of characters relative to users 
        -> not sure what format this will be in atm
    likes - pandas dataframe cataloguing character likes for all users 
        -> assume same format as likeable_likes in database
    n_chars - number of characters to consider (will take top n_chars unique likes from likes 
        and top n_chars predictions (i.e. with highest cosine similarities) from pred)
    Output: returns evaluation score 
    '''
    # Combining all data for filtering.
    user_info = likes.merge(pred, on = "user_id")

    ### Getting rid of these time related steps for now - not sure if recency is actually relevant enough
    # # Getting rid of any likes that occur too far away in time from character matching
    # user_info["lastupdate"] = pd.to_datetime(user_info["lastupdate"], format=r"%Y-%m-%d %H:%M:%S")
    # user_info["updated_at"] = pd.to_datetime(user_info["updated_at"], format=r"%Y-%m-%d %H:%M:%S")
    # user_info = user_info[abs(user_info["updated_at"] - user_info["lastupdate"]) < datetime.timedelta(days=60)]
    # # Getting rid of any matches that occured too far in the past
    # today = datetime.date.today()
    # user_info = user_info[today - user_info["lastupdate"].dt.date < datetime.timedelta(days=1095)]
    
    # Getting rid of duplicate character likes, if there are any
    user_info = user_info.sort_values(by="updated_at", ignore_index=True)\
        .drop_duplicates(subset=["user_id", "likable_id"], keep = "first", ignore_index=True)
    return user_info
   
    # Take sample of user_ids from those with more than n likes
    qual_u_ids = user_info.groupby(["user_id"], as_index=False)\
        .count()\
        .query("likable_id > @n_chars")["user_id"]
    sample_size = int(len(qual_u_ids)*args.sample)
    qual_u_ids = qual_u_ids.sample(n = sample_size, random_state=42)
    user_info = user_info["user_id"].isin(qual_u_ids.to_list())

    # How should I choose which characters to evaluate, if a user has liked more characters than we want to predict? Will use most recent timestamps for now
    # TODO - numpy function to grab all top characters for each individual and add to matrix (may need to use numba)
    top_n_likes = user_info.sort_values(by=["user_id", "updated_at"], ignore_index=True) \
        .groupby('user_id', as_index=False) \
        .head(n_chars).reset_index(drop=True)
    top_likes = top_n_likes["likable_id"].to_numpy(dtype=np.int32) - 1
    top_matches = top_n_likes[["user_id", "matches"]].groupby("user_id", as_index=False).head(1)
    matches_dict = pd.DataFrame(top_matches.pop("matches").apply(lambda x: dict(eval(x))))
    top_pred = matches_dict.apply(top_n_matches, axis=1, result_type="expand", col="matches", n=5) \
        .to_numpy(dtype=np.int32).flatten() - 1

    true = np.zeros((sample_size, 5341), dtype=np.int8)
    pred = np.zeros((sample_size, 5341), dtype=np.int8)
    idx = np.repeat(np.arange(0, sample_size), n_chars)
    true[idx, top_likes] = 1
    pred[idx, top_pred] = 1

    # sparse matrix
    # true = csr_matrix(true)
    # pred = csr_matrix(pred)

    # TODO - implement weights using percentile score from cosine similarity 
    if score_type == "F1":
        # explore parameters more https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html#sklearn.metrics.f1_score
        return f1_score(true, pred, average = "macro")
    elif score_type == "Hamming":
        return hamming_loss(true, pred)
    elif score_type == "Jaccard":
        return jaccard_score(true, pred, average = "macro")
    else:
        raise ValueError("The type of score specified ({}) has not been implemented.".format(score_type))

# %%

def eval_perct(pred, likes):
    '''
    Evaluate quality of predictions by checking user likes relative to their cosine similarity profiles
    Input:

    Output: ndarray of cosine similarity percentiles for user likes (can be sparse)
    '''
    '''
    Quality control on likes data (avoid users with too few likes)
    Convert likes dataframe into numpy array with missing values to pad stuff out (convert to long dataframe) see https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.pivot_table.html
    Consider returning object with precalculated mean
    '''
    pass

# %%
if __name__ == "__main__":
    args = handle_args()
    # Assume same format as usermatchcharacters table in database
    pred = pd.read_csv(args.pred)
    likes = pd.read_csv(args.likes)

    if(args.type == "top_n"):
        print(eval_top_n(pred, likes, args.num_chars, args.m))
    elif(args.type == "percentile"):


        print(np.mean())

    
    


'''
Inputs: assume cosine similarity prediction is already taken care of (no need for test splitting, just evaluate predicitons)
Need to get number of characters liked first (5331 as of data in database)
-In future, may want to use sparse array due to large number of 0s -> https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csr_matrix.html#scipy.sparse.csr_matrix

-For more information on multi-labeling specific classification, look into http://scikit.ml/
'''
# %%
