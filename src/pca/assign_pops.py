#source('https://github.com/macarthur-lab/gnomad_hail/blob/master/utils/generic.py')

import pandas as pd
import numpy as np
from collections import defaultdict, namedtuple, OrderedDict
from sklearn.ensemble import RandomForestClassifier
from typing import *
import random

file_path = '~/NG/pca_analysis/output/continental_level_ancestry/'
tg_file = file_path + '1000G_108003_combined_pcs.txt'
tg_info_file = file_path + 'integrated_call_samples_v3.20130502.ALL.panel'
ng_file = file_path + 'NG_32589_108003_proj_all_1000G.txt'
out_file = file_path + 'ng_pca_pops_rf.txt.gz'

tgp = df = pd.read_table(tg_file, header = 0, sep = '\t').iloc[:,1:]
ng = pd.read_table(ng_file, header=0, sep='\t').iloc[:,1:]
assert len(tgp.columns.values) == len(ng.columns.values)
tgp_info = pd.read_table(tg_info_file, header=0, sep='\t')

tgp_merge = pd.merge(left=tgp, right=tgp_info, left_on='IID', right_on='sample', how='inner')

ng_tgp = pd.concat([tgp_merge, ng])
reheader = ng_tgp.columns.values
reheader[-1] = 'known_pop'
ng_tgp.columns = reheader
#super_pop -> known_pop


def assign_population_pcs(
        pop_pc_pd: pd.DataFrame,
        num_pcs: int,
        pcs_col: str = 'scores',
        known_col: str = 'known_pop',
        fit: RandomForestClassifier = None,
        seed: int = 42,
        prop_train: float = 0.8,
        n_estimators: int = 100,
        min_prob: float = 0.9,
        output_col: str = 'pop',
        missing_label: str = 'oth'
) -> Tuple[pd.DataFrame, RandomForestClassifier]:
    """
    This function uses a random forest model to assign population labels based on the results of PCA.
    Default values for model and assignment parameters are those used in gnomAD.
    :param Table pop_pc_pd: Pandas dataframe containing population PCs as well as a column with population labels
    :param str known_col: Column storing the known population labels
    :param str pcs_col: Columns storing the PCs
    :param RandomForestClassifier fit: fit from a previously trained random forest model (i.e., the output from a previous RandomForestClassifier() call)
    :param int num_pcs: number of population PCs on which to train the model
    :param int seed: Random seed
    :param float prop_train: Proportion of known data used for training
    :param int n_estimators: Number of trees to use in the RF model
    :param float min_prob: Minimum probability of belonging to a given population for the population to be set (otherwise set to `None`)
    :param str output_col: Output column storing the assigned population
    :param str missing_label: Label for samples for which the assignment probability is smaller than `min_prob`
    :return: Dataframe containing sample IDs and imputed population labels, trained random forest model
    :rtype: DataFrame, RandomForestClassifier
    """

    # Expand PC column
    #pop_pc_pd = expand_pd_array_col(pop_pc_pd, pcs_col, num_pcs, 'PC')
    pc_cols = ['PC{}'.format(i + 1) for i in range(num_pcs)]
    print(pc_cols)
    #pop_pc_pd[pc_cols] = pd.DataFrame(pop_pc_pd[pcs_col].values.tolist())[list(range(num_pcs))]
    train_data = pop_pc_pd.loc[~pop_pc_pd[known_col].isnull()]

    N = len(train_data)
    print(train_data.shape)

    # Split training data into subsamples for fitting and evaluating
    if not fit:
        random.seed(seed)
        train_subsample_ridx = random.sample(list(range(0, N)), int(N * prop_train))
        train_fit = train_data.iloc[train_subsample_ridx]
        fit_samples = [x for x in train_fit['IID']]
        evaluate_fit = train_data.loc[~train_data['IID'].isin(fit_samples)]

        # Train RF
        training_set_known_labels = train_fit[known_col].as_matrix()
        training_set_pcs = train_fit[pc_cols].as_matrix()
        evaluation_set_pcs = evaluate_fit[pc_cols].as_matrix()

        pop_clf = RandomForestClassifier(n_estimators=n_estimators, random_state=seed,n_jobs=-1)
        pop_clf.fit(training_set_pcs, training_set_known_labels)
        print('Random forest feature importances are as follows: {}'.format(pop_clf.feature_importances_))

        # Evaluate RF
        predictions = pop_clf.predict(evaluation_set_pcs)
        error_rate = 1 - sum(evaluate_fit[known_col] == predictions) / float(len(predictions))
        print('Estimated error rate for RF model is {}'.format(error_rate))
    else:
        pop_clf = fit

    # Classify data
    print('Classifying data')
    pop_pc_pd[output_col] = pop_clf.predict(pop_pc_pd[pc_cols].as_matrix())
    probs = pop_clf.predict_proba(pop_pc_pd[pc_cols].as_matrix())
    probs = pd.DataFrame(probs, columns=['prob_{0}'.format(p) for p in pop_clf.classes_])
    print('probs shape ' + str(probs.shape))
    print('pop_pc_pd shape ' + str(pop_pc_pd.shape))
    print(probs.iloc[:3,])
    print(pop_pc_pd.iloc[:3,])
    #pop_pc_pd = pd.concat([pop_pc_pd, probs], axis=1, ignore_index=True)
    print(pop_pc_pd.shape)
    probs['max'] = probs.max(axis=1)
    pop_pc_pd.loc[probs['max'] < min_prob, output_col] = missing_label
    #pop_pc_pd = pop_pc_pd.drop(pc_cols, axis='columns')
    print(pop_pc_pd.shape)

    return pop_pc_pd, pop_clf

pcs_df, clf = assign_population_pcs(pop_pc_pd=ng_tgp, num_pcs=6, min_prob = 0.7)

ng_pops = pcs_df.loc[pcs_df['known_pop'].isnull()]
ng_pops['pop'].value_counts()
cols = ['IID', 'pop'] + ['PC{0}'.format(i) for i in range(1, 21)]
ng_pops_df = ng_pops[cols]

ng_pops_df.to_csv(out_file, sep='\t', index=False, compression='gzip')

