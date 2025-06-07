from bert_score import score as bert_score

def evaluate_bertscore(user_inputs, bot_replies):
    P, R, F1 = bert_score(bot_replies, user_inputs, lang="zh", verbose=False)
    return [round(float(x), 4) for x in P.tolist()], \
           [round(float(x), 4) for x in R.tolist()], \
           [round(float(x), 4) for x in F1.tolist()]
