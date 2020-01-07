import sys
import pandas as pd
import numpy as np
import scipy.stats as stats


OUTPUT_TEMPLATE = (
    '"Did more/less users use the search feature?" p-value: {more_users_p:.3g}\n'
    '"Did users search more/less?" p-value: {more_searches_p:.3g}\n'
    '"Did more/less instructors use the search feature?" p-value: {more_instr_p:.3g}\n'
    '"Did instructors search more/less?" p-value: {more_instr_searches_p:.3g}'
)


def main():
    searchdata_file = sys.argv[1]

    search_data = pd.read_json(searchdata_file, orient='records', lines=True)

    even_df = search_data[search_data['uid'] % 2 == 0]
    odd_df = search_data[search_data['uid'] % 2 != 0 ]
    even_nonzero = len(even_df[even_df['search_count'] >= 1])
    odd_nonzero = len(odd_df[odd_df['search_count'] >= 1])
    even_zero = len(even_df[even_df['search_count'] == 0])
    odd_zero = len(odd_df[odd_df['search_count'] == 0])

    # Instructor data
    instructor_even_df = even_df[even_df['is_instructor'] == True]
    instructor_odd_df = odd_df[odd_df['is_instructor'] == True]
    instructor_even_nonzero = len(instructor_even_df[instructor_even_df['search_count'] >= 1])
    instructor_odd_nonzero = len(instructor_odd_df[instructor_odd_df['search_count'] >= 1])
    instructor_even_zero = len(instructor_even_df[instructor_even_df['search_count'] == 0])
    instructor_odd_zero = len(instructor_odd_df[instructor_odd_df['search_count'] == 0])

    # Tests .. contingency table = (even/odd), (nonzero counts, zero counts)
    chi2, p , dof, expected = stats.chi2_contingency([[even_nonzero,even_zero], [odd_nonzero, odd_zero]])
    mannWhitneyPvalue = stats.mannwhitneyu(even_df['search_count'], odd_df['search_count']).pvalue

    i_chi2, i_p , i_dof, i_expected = stats.chi2_contingency([[instructor_even_nonzero,instructor_even_zero], [instructor_odd_nonzero, instructor_odd_zero]])
    i_mannWhitneyPvalue = stats.mannwhitneyu(instructor_even_df['search_count'], instructor_odd_df['search_count']).pvalue
    # Output
    print(OUTPUT_TEMPLATE.format(
        more_users_p=p,
        more_searches_p=mannWhitneyPvalue,
        more_instr_p=i_p,
        more_instr_searches_p=i_mannWhitneyPvalue,
    ))


if __name__ == '__main__':
    main()