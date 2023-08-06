import numpy as np
import sys
import time

def deepwalk_sim(sim_matrix, mani_record, specific_phase):

    if specific_phase:
        phase_operation = {'initial': ['import_packages', 'sort_index', 'load_data', 'save_data', 'sort_index', 'index_info', 'column_name_all', 'dataset_shape', 'dataset_dtype', 'dataset_describe', 'head_overview'],
                    'preprocessing': ['group_by_column', 'nan_matrix', 'where_nan', 'drop_na', 'fill_na', 'drop_duplicates', 'extract_duplicates', 'one_hot_encoding'],
                    'feature engineering': ['scaler', 'correlation_matrix', 'feature_selection', 'feature_selection_collinear', 'feature_selection_pca', 'feature_selection_missing', 'feature_selection_importance', 'feature_selection_variance', 'feature_selection_single_unique'],
                    'model construction': ['sampling', 'train_test_split', 'regression_model', 'classification_model'],
                    'pipeline workflow': ['regression_model_pipeline', 'classification_model_pipeline']}

        res = []
        for word in mani_record:
            temp = sim_matrix[word][:10]
            res.extend([x[0] for x in temp])
        res = set(res) - set(mani_record)

        res = list(res & set(phase_operation[specific_phase]))

        return res

    else:
        res = []
        for word in mani_record:
            temp = sim_matrix[word][:3]
            res.extend([x[0] for x in temp])
        res = list(set(res) - set(mani_record))
        
        return res



