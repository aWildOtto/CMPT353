import sys
import pandas as pd
import numpy as np
import datetime
import scipy.stats as stats
import matplotlib as plt


OUTPUT_TEMPLATE = (
    "Initial (invalid) T-test p-value: {initial_ttest_p:.3g}\n"
    "Original data normality p-values: {initial_weekday_normality_p:.3g} {initial_weekend_normality_p:.3g}\n"
    "Original data equal-variance p-value: {initial_levene_p:.3g}\n"
    "Transformed data normality p-values: {transformed_weekday_normality_p:.3g} {transformed_weekend_normality_p:.3g}\n"
    "Transformed data equal-variance p-value: {transformed_levene_p:.3g}\n"
    "Weekly data normality p-values: {weekly_weekday_normality_p:.3g} {weekly_weekend_normality_p:.3g}\n"
    "Weekly data equal-variance p-value: {weekly_levene_p:.3g}\n"
    "Weekly T-test p-value: {weekly_ttest_p:.3g}\n"
    "Mann–Whitney U-test p-value: {utest_p:.3g}"
)


def main():
    reddit_counts = sys.argv[1]

    counts = pd.read_json(reddit_counts, lines=True)

    counts = counts[counts['date'] >= datetime.date(2012, 1, 1)]
    counts = counts[counts['date'] <= datetime.date(2013, 12, 31)]
    counts = counts[counts['subreddit'] == 'canada']

    weekdays = counts[(counts['date'].apply(datetime.date.weekday) != 5) & (counts['date'].apply(datetime.date.weekday) != 6)]
    weekends = counts[(counts['date'].apply(datetime.date.weekday) == 5) | (counts['date'].apply(datetime.date.weekday) == 6)]

    # initial tests
    init_ttest_p = stats.ttest_ind(weekends['comment_count'], weekdays['comment_count']).pvalue
    init_weekday_norm_p = stats.normaltest(weekdays['comment_count']).pvalue
    init_weekend_norm_p = stats.normaltest(weekends['comment_count']).pvalue
    init_levene = stats.levene(weekends['comment_count'], weekdays['comment_count']).pvalue

    # transformed: log
    weekends_log = weekends['comment_count'].apply(np.log)
    weekdays_log = weekdays['comment_count'].apply(np.log)

    weekday_log_norm = stats.normaltest(weekdays_log).pvalue
    weekend_log_norm = stats.normaltest(weekends_log).pvalue
    log_levene = stats.levene(weekends_log, weekdays_log).pvalue

    # transformed: exp
    """
    weekends_exp = weekends['comment_count'].apply(np.exp)
    weekdays_exp = weekdays['comment_count'].apply(np.exp)

    weekday_exp_norm = stats.normaltest(weekdays_exp).pvalue
    weekend_exp_norm = stats.normaltest(weekends_exp).pvalue
    exp_levene = stats.levene(weekends_exp, weekdays_exp).pvalue
    """

    # transformed: sqrt. Best result
    weekends_sqrt = weekends['comment_count'].apply(np.sqrt)
    weekdays_sqrt = weekdays['comment_count'].apply(np.sqrt)

    weekday_sqrt_norm = stats.normaltest(weekdays_sqrt).pvalue
    weekend_sqrt_norm = stats.normaltest(weekends_sqrt).pvalue
    sqrt_levene = stats.levene(weekends_sqrt, weekdays_sqrt).pvalue

    # transformed: sq2
    weekends_sq2 = weekends['comment_count']**2
    weekdays_sq2 = weekdays['comment_count']**2

    weekdays_sq2_norm = stats.normaltest(weekdays_sq2).pvalue
    weekends_sq2_norm = stats.normaltest(weekends_sq2).pvalue
    sq2_levene = stats.levene(weekends_sq2, weekdays_sq2)

    # central limit theorem
    weekdays_isodate = weekdays['date'].apply(datetime.date.isocalendar).apply(pd.Series)
    del weekdays_isodate[2]
    weekdays_isodate.columns = ['year','week']
    weekdays_group = pd.concat([weekdays, weekdays_isodate], axis = 1)
    weekdays_group = weekdays_group.groupby(['year','week']).agg('mean')

    weekends_isodate = weekends['date'].apply(datetime.date.isocalendar).apply(pd.Series)
    del weekends_isodate[2]
    weekends_isodate.columns = ['year','week']
    weekends_group = pd.concat([weekends, weekends_isodate], axis = 1)
    weekends_group = weekends_group.groupby(['year','week']).agg('mean')

    weekly_weekday_norm_p = stats.normaltest(weekdays_group['comment_count']).pvalue
    weekly_weekend_norm_p = stats.normaltest(weekends_group['comment_count']).pvalue
    weekly_levene_pval = stats.levene(weekdays_group['comment_count'], weekends_group['comment_count']).pvalue
    weekly_ttest_pval = stats.ttest_ind(weekends_group['comment_count'], weekdays_group['comment_count']).pvalue

    # Mann-Whitney U-test
    utest_pval = stats.mannwhitneyu(weekends['comment_count'],weekdays['comment_count']).pvalue



    print(OUTPUT_TEMPLATE.format(
        initial_ttest_p=init_ttest_p,
        initial_weekday_normality_p=init_weekday_norm_p,
        initial_weekend_normality_p=init_weekend_norm_p,
        initial_levene_p=init_levene,
        transformed_weekday_normality_p=weekday_sqrt_norm,
        transformed_weekend_normality_p=weekend_sqrt_norm,
        transformed_levene_p=sqrt_levene,
        weekly_weekday_normality_p=weekly_weekday_norm_p,
        weekly_weekend_normality_p=weekly_weekend_norm_p,
        weekly_levene_p=weekly_levene_pval,
        weekly_ttest_p=weekly_ttest_pval,
        utest_p=utest_pval,
    ))


if __name__ == '__main__':
    main()