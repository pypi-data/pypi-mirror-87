import numpy as np
import pandas as pd
import warnings


def data_check(array, key):
    """ Function that checks the value of an array for impossible values

    :param array: the array (column) you want to check
    :param key: str, the feature name of the array. Choose from ['age', 'sex', 'education', 'sdmt', 'bvmt', 'cvlt']
    :return: error if a problem is encountered, or prints a message when considered valid
    """
    error_dict = {'age': 'Please use age values between 0 and 125 years, and only use integer values',
                  'sex': 'Please assure the following encoding: Male = 1, Female = 2',
                  'education': 'Please use education levels that are encoded as 6, 12, 13, 15, 17 or 21 years',
                  'sdmt': 'Please use sdmt values between 0 and 110',
                  'bvmt': 'Please use bvmt values between 0 and 36',
                  'cvlt': 'Please use cvlt values between 0 and 80'}

    allowed_range_dict = {'age': set(range(0, 126)),
                          'sex': {1, 2},
                          'education': {6, 12, 13, 15, 17, 21},
                          'sdmt': set(range(0, 111)),
                          'bvmt': set(range(0, 37)),
                          'cvlt': set(range(0, 81))}

    input_set = set(array)
    comparison_set = allowed_range_dict.get(key)

    # Check whether the values of input_set are within the allowed values (comparison_set)
    if not input_set.issubset(comparison_set) or sum(np.isnan(list(array))) > 0:
        raise ValueError(error_dict.get(key))

    print('No errors. Ready for conversion! :)')


def normalization_pipeline(age, sex, edu, raw_score, test, z_cutoff):
    """ Entire normalization pipeline

    :param age: age in years
    :param sex: Male = 1, Female = 2
    :param edu: amount of years education (Choose from 6, 12, 13, 15, 17, 21)
    :param raw_score: int, raw score on the test of interest
    :param test: str, choose from 'sdmt', 'bvmt' or 'cvlt'
    :param z_cutoff: float, the value where you want to declare impairment on the cognitive domain
    :returns: z_score: z-score for the test of interest -- impaired_bool: 1 if impaired, 0 if preserved
    """

    # Check if one of the values is NaN. In that case return NaN.
    problem_detected = _check_impossible_values_or_nans(locals())
    if problem_detected:
        return np.nan, np.nan
    else:
        # Additional required preparations
        age_2 = age**2
        data_vector = [age, age_2, sex, edu]
        conversion_table = _get_conversion_table(test)

        # The pipeline: from raw score to z-score and impairment boolean
        expected_score = _get_expected_score(data_vector, test)
        scaled_score = _raw_to_scaled(raw_score, conversion_table)
        z_score = _to_z_score(scaled_score, expected_score, test)
        impaired_bool = _impaired_or_not(z_score, z_cutoff)

        return z_score, impaired_bool


def _check_impossible_values_or_nans(arguments_dict):
    """

    :param arguments_dict:
    :return:
    """

    error_dict = {'age': 'Please use age values between 0 and 125 years, and only use integer values',
                  'sex': 'Please assure the following encoding: Male = 1, Female = 2',
                  'edu': 'Please use education levels that are encoded as 6, 12, 13, 15, 17 or 21 years',
                  'sdmt': 'Please use sdmt values between 0 and 110',
                  'bvmt': 'Please use bvmt values between 0 and 36',
                  'cvlt': 'Please use cvlt values between 0 and 80'}

    allowed_range_dict = {'age': range(0, 126),
                          'sex': [1, 2],
                          'edu': [6, 12, 13, 15, 17, 21],
                          'sdmt': range(0, 111),
                          'bvmt': range(0, 37),
                          'cvlt': range(0, 81)}

    # By default, no problem detected
    problem_detected = False

    for key, value in arguments_dict.items():

        if key not in ['test', 'z_cutoff']:  # Don't check for value entries of 'test' or 'z_cutoff'

            # Convert the key since we want the key of raw_score to be the test, so that it is e.g.: {'sdmt': 50}
            if key == 'raw_score':
                key = arguments_dict.get('test')

            # Check whether the value is within the allowed ranges. If not, raise a warning
            if value not in allowed_range_dict.get(key):
                warnings.warn(error_dict.get(key))
                problem_detected = True

    return problem_detected


def _get_conversion_table(test):
    """ Get conversion table that corresponds with the test of interest

    :param test: str, choose from 'sdmt', 'bvmt' or 'cvlt'
    :return: dict, conversion table
    """
    sdmt_ct_dict = {'scaled_score': [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
                    'sdmt_lower': [0, 38, 41, 44, 48, 51, 55, 58, 61, 65, 68, 72, 75, 78, 82, 85, 89],
                    'sdmt_upper': [37, 40, 43, 47, 50, 54, 57, 60, 64, 67, 71, 74, 77, 81, 84, 88, 1000]}
    bvmt_ct_dict = {'scaled_score': [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
                    'bvmt_lower': [0, 17, 19, 20, 22, 24, 25, 27, 29, 30, 32, 34, 36],
                    'bvmt_upper': [16, 18, 19, 21, 23, 24, 26, 28, 29, 31, 33, 35, 1000]}
    cvlt_ct_dict = {'scaled_score': [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                    'cvlt_lower': [0, 39, 42, 46, 49, 52, 55, 59, 62, 65, 68, 71, 75, 78],
                    'cvlt_upper': [38, 41, 45, 48, 51, 54, 58, 61, 64, 67, 70, 74, 77, 1000]}

    # Dictionary with the tests and the according conversion tables
    conversion_dict = {'sdmt': pd.DataFrame(sdmt_ct_dict),
                       'bvmt': pd.DataFrame(bvmt_ct_dict),
                       'cvlt': pd.DataFrame(cvlt_ct_dict)}

    # Get conversion table from test
    return conversion_dict.get(test)


def _get_expected_score(data_vector, test):
    """ Get the expected score on a subtest of the BICAMS

    :param data_vector: 1-D vector consisting in following order: [age, age^2, sex, education]
    :param test: str, choose from 'sdmt', 'bvmt' or 'cvlt'
    :return: the expected score on the respective test
    """
    weight_dict = {'sdmt': [10.648, -0.289, 0.002, -0.05, 0.479],
                   'cvlt': [9.052, -0.230, 0.002, 2.182, 0.323],
                   'bvmt': [16.902, -0.473, 0.005, -1.427, 0.341]}

    weight_vector = weight_dict.get(test)
    data_vector = [1] + list(data_vector)  # Add 1 to multiply with bias term in regression equation
    expected_score = np.dot(weight_vector, data_vector)

    return expected_score


def _raw_to_scaled(raw_score, conversion_table):
    """ Convert raw score to a categorical, scaled value

    :param raw_score: int, raw score on the test of interest
    :param conversion_table: pd dataframe, being the conversion table for the test of interest
    :return: categorical, scaled score
    """

    scaled_scores = conversion_table.iloc[:,0]
    lower_values = conversion_table.iloc[:,1]
    upper_values = conversion_table.iloc[:,2]

    for scaled_score, lower_value, upper_value in zip(scaled_scores, lower_values, upper_values):
        if lower_value <= raw_score <= upper_value:
            return scaled_score


def _to_z_score(scaled_score, expected_score, test):
    """ Turn scaled and expected score to a z score

    :param scaled_score: scaled score, result from raw_to_scaled function
    :param expected_score: expected score, result from get_expected_score function
    :param test: test of interest
    :return: z-score for the test of interest
    """
    denominator_dict = {'sdmt': 2.790,
                        'bvmt': 2.793,
                        'cvlt': 2.801}

    denominator = denominator_dict.get(test)

    z_score = (scaled_score - expected_score)/denominator

    return z_score


def _impaired_or_not(z_score, cutoff):
    """ Dichotimize z-score by applying a cutoff

    :param z_score: the z-score, i.e. performance relative to a reference population
    :param cutoff: the cut-off to decide impaired (<=) or preserved (>) on the cognitive domain
    :return: 1 if impaired, 0 if preserved
    """
    if z_score <= cutoff:
        return 1
    else:
        return 0


def pipeline_for_pandas(row, test, z_cutoff):
    """ This pipeline allows to use the ".apply" function of pandas to perform calculations on entire dataframe
    Copy/paste following code snippets (please also perform additional action below each step)
    1. new_columns = ['z_test', 'imp_test']
    --> replace 'test' with the test you are converting
    2. input_columns = ['column_name_age', 'column_name_sex', 'column_name_edu', 'column_name_test']
    --> Adapt the names according to your columnnames.
    3. df[new_columns] = df[input_columns].apply(pipeline_for_pandas, args = (test, z_cutoff), axis = 1)
    --> replace 'test' with the string 'sdmt', 'bvmt' or 'cvlt'. Also choose the cut-off.

    :param row: row of pandas dataframe
    :param test: choose from 'sdmt', 'bvmt', 'cvlt'
    :param z_cutoff: float, at which cutoff you want to declare impairment
    :return: series object that you can unpack in 2 pandas columns
    """

    return pd.Series(normalization_pipeline(row[0], row[1], row[2], row[3], test, z_cutoff))
