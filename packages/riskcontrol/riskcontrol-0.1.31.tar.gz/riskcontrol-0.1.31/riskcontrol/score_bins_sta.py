import pandas as pd
import numpy as np


def Data_Woe(df, obj_col, target, value, types='Bin'):
    df_tmp = pd.DataFrame()
    # describes = pd.read_excel(r'D:\MyConfiguration\youliang.deng\Desktop\model\外部数据测试\百融\br_dict.xlsx')
    describes = pd.DataFrame(columns=['colname_Bin', 'colname', 'describe'])

    if len(set(df[target])) == 3:
        for col in obj_col:
            pivo = pd.pivot_table(df, columns=target, index=col, values=value, aggfunc=len, margins=True, fill_value=0)
            pivo.columns = ['good', 'midd', 'bad', 'ALL']
            pivo['good_pcnt'] = pivo['good'] / pivo.iloc[-1]['good']
            pivo['midd_pcnt'] = pivo['midd'] / pivo.iloc[-1]['midd']
            pivo['bad_pcnt'] = pivo['bad'] / pivo.iloc[-1]['bad']
            pivo['ALL_pcnt'] = pivo['ALL'] / pivo.iloc[-1]['ALL']
            pivo['bad_rate'] = pivo['bad'] / (pivo['bad'] + pivo['good'])
            pivo['midd_rate'] = pivo['midd'] / pivo['ALL']
            pivo['IV'] = pivo.apply(
                lambda x: (x.bad_pcnt - x.good_pcnt) * np.log(
                    x.bad_pcnt * 1.0 / x.good_pcnt) if x.good_pcnt != 0 and x.bad_pcnt != 0 else 0,
                axis=1)
            pivo['IV'][-1] = pivo['IV'].sum()
            pivo['WOE'] = pivo.apply(
                lambda x: np.log(x.bad_pcnt * 1.0 / x.good_pcnt) if x.good_pcnt != 0 and x.bad_pcnt != 0 else 0, axis=1)
            pivo['KS'] = abs(
                pivo['good'].cumsum() / pivo.iloc[-1]['good'] - pivo['bad'].cumsum() / pivo.iloc[-1]['bad'])
            # pivo['Gini'] = 2 * pivo['ALL_pcnt'] * (1 - pivo['bad_rate']) * pivo['bad_rate']
            # pivo['Gini'][-1] = pivo['Gini'].sum()
            pivo['Lift'] = pivo['bad_rate'] / pivo.iloc[-1]['bad_rate']
            pivo['col_name'] = col
            # pivo = pivo.sort_index(ascending=True)
            df_tmp = pd.concat([df_tmp, pivo], axis=0)
            df_tmp = df_tmp.append(pd.DataFrame(
                np.array([np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
                          np.nan, np.nan, np.nan, np.nan]).reshape(1, -1),
                columns=pivo.columns))
            # df_tmp = df_tmp.insert(pd.DataFrame(columns=pivo.columns))
        if types == 'Bin':
            describes = describes[['colname_Bin', 'describe']]
            df_tmp = df_tmp.reset_index()
            df_tmp = df_tmp.merge(describes, how='left', left_on='col_name', right_on='colname_Bin')
        else:
            describes = describes[['colname', 'describe']]
            df_tmp = df_tmp.reset_index()
            df_tmp = df_tmp.merge(describes, how='left', left_on='col_name', right_on='colname')
        df_tmp = df_tmp[
            ['col_name', 'describe', 'index', 'good', 'midd', 'bad', 'ALL', 'good_pcnt', 'midd_pcnt', 'bad_pcnt',
             'ALL_pcnt',
             'bad_rate', 'midd_rate', 'IV', 'WOE', 'KS', 'Lift']]
        df_tmp.columns = ['col_name', 'describe', 'Bin', 'good', 'midd', 'bad', 'ALL', 'good_pcnt', 'midd_pcnt',
                          'bad_pcnt', 'ALL_pcnt',
                          'bad_rate', 'midd_rate', 'IV', 'WOE', 'KS', 'Lift']
        df_tmp['good_pcnt'] = df_tmp['good_pcnt'].apply(lambda x: '%.2f%%' % (x * 100))
        df_tmp['midd_pcnt'] = df_tmp['midd_pcnt'].apply(lambda x: '%.2f%%' % (x * 100))
        df_tmp['bad_pcnt'] = df_tmp['bad_pcnt'].apply(lambda x: '%.2f%%' % (x * 100))
        df_tmp['ALL_pcnt'] = df_tmp['ALL_pcnt'].apply(lambda x: '%.2f%%' % (x * 100))
        df_tmp['bad_rate'] = df_tmp['bad_rate'].apply(lambda x: '%.2f%%' % (x * 100))
        df_tmp['midd_rate'] = df_tmp['midd_rate'].apply(lambda x: '%.2f%%' % (x * 100))
        df_tmp['IV'] = df_tmp['IV'].apply(lambda x: '%.3f' % (x))
        df_tmp['WOE'] = df_tmp['WOE'].apply(lambda x: '%.3f' % (x))
        df_tmp['KS'] = df_tmp['KS'].apply(lambda x: '%.3f' % (x))
        df_tmp['Lift'] = df_tmp['Lift'].apply(lambda x: '%.3f' % (x))
        return df_tmp
    elif len(set(df[target])) == 2:
        for col in obj_col:
            pivo = pd.pivot_table(df, columns=target, index=col, values=value, aggfunc=len, margins=True, fill_value=0)
            # pivo.columns = ['good', 'midd', 'bad', 'ALL']
            pivo.columns = ['good', 'bad', 'ALL']
            pivo['good_pcnt'] = pivo['good'] / pivo.iloc[-1]['good']
            pivo['bad_pcnt'] = pivo['bad'] / pivo.iloc[-1]['bad']
            pivo['ALL_pcnt'] = pivo['ALL'] / pivo.iloc[-1]['ALL']
            pivo['bad_rate'] = pivo['bad'] / (pivo['bad'] + pivo['good'])
            pivo['IV'] = pivo.apply(
                lambda x: (x.bad_pcnt - x.good_pcnt) * np.log(
                    x.bad_pcnt * 1.0 / x.good_pcnt) if x.good_pcnt != 0 and x.bad_pcnt != 0 else 0,
                axis=1)
            pivo['IV'][-1] = pivo['IV'].sum()
            pivo['WOE'] = pivo.apply(
                lambda x: np.log(x.bad_pcnt * 1.0 / x.good_pcnt) if x.good_pcnt != 0 and x.bad_pcnt != 0 else 0, axis=1)
            pivo['KS'] = abs(
                pivo['good'].cumsum() / pivo.iloc[-1]['good'] - pivo['bad'].cumsum() / pivo.iloc[-1]['bad'])
            # pivo['Gini'] = 2 * pivo['ALL_pcnt'] * (1 - pivo['bad_rate']) * pivo['bad_rate']
            # pivo['Gini'][-1] = pivo['Gini'].sum()
            pivo['Lift'] = pivo['bad_rate'] / pivo.iloc[-1]['bad_rate']
            pivo['col_name'] = col
            # pivo = pivo.sort_index(ascending=True)
            df_tmp = pd.concat([df_tmp, pivo], axis=0)
            df_tmp = df_tmp.append(pd.DataFrame(
                np.array([np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
                          np.nan]).reshape(1, -1),
                columns=pivo.columns))
            # df_tmp = df_tmp.insert(pd.DataFrame(columns=pivo.columns))
        if types == 'Bin':
            describes = describes[['colname_Bin', 'describe']]
            df_tmp = df_tmp.reset_index()
            df_tmp = df_tmp.merge(describes, how='left', left_on='col_name', right_on='colname_Bin')
        else:
            describes = describes[['colname', 'describe']]
            df_tmp = df_tmp.reset_index()
            df_tmp = df_tmp.merge(describes, how='left', left_on='col_name', right_on='colname')
        df_tmp = df_tmp[['col_name', 'describe', 'index', 'good', 'bad', 'ALL', 'good_pcnt', 'bad_pcnt', 'ALL_pcnt',
                         'bad_rate', 'IV', 'WOE', 'KS', 'Lift']]
        df_tmp.columns = ['col_name', 'describe', 'Bin', 'good', 'bad', 'ALL', 'good_pcnt', 'bad_pcnt', 'ALL_pcnt',
                          'bad_rate', 'IV', 'WOE', 'KS', 'Lift']
        df_tmp['good_pcnt'] = df_tmp['good_pcnt'].apply(lambda x: '%.2f%%' % (x * 100))
        df_tmp['bad_pcnt'] = df_tmp['bad_pcnt'].apply(lambda x: '%.2f%%' % (x * 100))
        df_tmp['ALL_pcnt'] = df_tmp['ALL_pcnt'].apply(lambda x: '%.2f%%' % (x * 100))
        df_tmp['bad_rate'] = df_tmp['bad_rate'].apply(lambda x: '%.2f%%' % (x * 100))
        df_tmp['IV'] = df_tmp['IV'].apply(lambda x: '%.3f' % (x))
        df_tmp['WOE'] = df_tmp['WOE'].apply(lambda x: '%.3f' % (x))
        df_tmp['KS'] = df_tmp['KS'].apply(lambda x: '%.3f' % (x))
        df_tmp['Lift'] = df_tmp['Lift'].apply(lambda x: '%.3f' % (x))

        df_tmp['cum_bads'] = df_tmp['bad'].cumsum()
        df_tmp['cum_goods'] = df_tmp['good'].cumsum()
        df_tmp['cum_bads_prop'] = df_tmp['cum_bads'] / df_tmp[df_tmp['Bin']!='All']['bad'].sum()
        df_tmp['cum_goods_prop'] = df_tmp['cum_goods'] / df_tmp[df_tmp['Bin']!='All']['good'].sum()
        df_tmp['KS'] = df_tmp['cum_bads_prop'] - df_tmp['cum_goods_prop']
        df_tmp['KS'] = df_tmp['KS'].apply(lambda x: '%.3f' % (x))
        df_tmp['cum_bads_prop'] = df_tmp['cum_bads_prop'].apply(lambda x: '%.3f' % (x))
        df_tmp['cum_goods_prop'] = df_tmp['cum_goods_prop'].apply(lambda x: '%.3f' % (x))

        return df_tmp
    else:
        return 'target Error'


def Prob2Score(df, target, basescores, PDO, model, Features, report='scores', y=0.5):
    '''
    :param df: 清洗后准备训练模型的所有数据（包含训练集和测试集）
    :param target: 目标变量  （1为坏样本，0为好样本）
    :param basescores: 基础分数（一般设600）
    :param PDO: 指定违约概率翻倍的分数
    :param model: 训练好的模型
    :param Features: 入模特征
    :param report: 需要输出的数据格式
    :param y: 目标变量是否包含0.5
    :return: 计算分数的A、B系数
    '''
    prob = model.predict_proba(df[Features].values)[:, 1]
    # B = PDO / np.log(2)
    # A = basescores + B * np.log(len(df[df[target] == 1]) / len(df[df[target] == 0]))
    B = 50 / np.log(2)
    A = 600 + 50 / np.log(2) * np.log(6195 / 60233)
    all_score = pd.DataFrame(prob).set_axis(['pro_g'], axis='columns', inplace=False)
    all_score['score'] = round(A - B * (np.log(all_score['pro_g'] / (1 - all_score['pro_g']))))

    over_rate_desc = all_score.copy()
    over_rate_desc[target] = list(df[target])
    over_rate_desc = over_rate_desc[(over_rate_desc[target] == 0) | (over_rate_desc[target] == 1)]
    over_rate_desc = over_rate_desc.sort_values(by='score', ascending=False)
    over_rate_desc['over_rate'] = over_rate_desc[target].cumsum() / over_rate_desc[target].count()
    over_rate_desc['times'] = over_rate_desc['over_rate'] / (
            over_rate_desc[target].sum() / over_rate_desc[target].count())

    score_cut = all_score.copy()
    # bin.score[bin.score > over_rate_score.score.max()] = Max + 1
    # bin.score[bin.score < Min] = Min
    # bins = ls
    socre_bin = all_score.describe(percentiles=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])['score'].iloc[
                3:].values.tolist()
    socre_bin[0] = socre_bin[0] - 1
    score_cut['score_bins'] = pd.DataFrame(pd.cut(score_cut['score'], bins=socre_bin))
    score_cut[target] = list(df[target])
    if y == 0.5:
        score_cut_group = pd.pivot_table(score_cut, index=['score_bins'], columns=[target], values=['score'],
            aggfunc=[len],
            fill_value=0).set_axis(['good', 'midd', 'bad'], axis='columns', inplace=False)
        score_cut_group['t_all'] = score_cut_group['good'] + score_cut_group['bad'] + score_cut_group['midd']

        score_cut_group['badCumRate'] = score_cut_group['bad'].cumsum() / score_cut_group['bad'].sum()
        score_cut_group['goodCumRate'] = score_cut_group['good'].cumsum() / score_cut_group['good'].sum()
        score_cut_group['over_rate'] = score_cut_group['bad'] / (score_cut_group['good'] + score_cut_group['bad'])
        score_cut_group['ks'] = score_cut_group['badCumRate'] - score_cut_group['goodCumRate']
    else:
        score_cut = score_cut[score_cut[target] != 0.5]
        score_cut_group = pd.pivot_table(score_cut, index=['score_bins'], columns=[target], values=['score'],
            aggfunc=[len],
            fill_value=0).set_axis(['good', 'bad'], axis='columns', inplace=False)
        score_cut_group['t_all'] = score_cut_group['good'] + score_cut_group['bad']
        score_cut_group['badCumRate'] = score_cut_group['bad'].cumsum() / score_cut_group['bad'].sum()
        score_cut_group['goodCumRate'] = score_cut_group['good'].cumsum() / score_cut_group['good'].sum()
        score_cut_group['over_rate'] = score_cut_group['bad'] / score_cut_group['t_all']
        score_cut_group['ks'] = score_cut_group['badCumRate'] - score_cut_group['goodCumRate']

    g_b_score = all_score.copy()
    g_b_score['score_bins'] = pd.DataFrame(pd.cut(g_b_score['score'], bins=list(
        range(int(min(socre_bin) - min(socre_bin) % 10), int(max(socre_bin) + (30 - max(socre_bin) % 10)), 20))))
    g_b_score[target] = list(df[target])
    if y == 0.5:
        g_b_score_bin = pd.pivot_table(g_b_score, index=['score_bins'], columns=[target], values=['score'],
            aggfunc=[len],
            fill_value=0).set_axis(['good', 'midd', 'bad'], axis='columns', inplace=False)
        g_b_score_bin = g_b_score_bin[['good', 'midd', 'bad']]
    else:
        g_b_score = g_b_score[g_b_score[target] != 0.5]
        g_b_score_bin = pd.pivot_table(g_b_score, index=['score_bins'], columns=[target], values=['score'],
            aggfunc=[len],
            fill_value=0).set_axis(['good', 'bad'], axis='columns', inplace=False)
        g_b_score_bin = g_b_score_bin[['good', 'bad']]

    if report == 'scores':
        return all_score
    elif report == 'rate_fb':
        return over_rate_desc
    elif report == 'bin':
        return score_cut_group
    elif report == 'g_b_pic':
        return g_b_score_bin
    else:
        return '请输入正确的报告形式！'


def CUT_BIN(df, Features, step, target, value, type='Norm'):
    score_lst = []
    for col in Features:
        # *********************标准切分***************************
        if type == 'Norm':
            socre_bin = df.describe(percentiles=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])[col].iloc[
                        3:].values.tolist()
            socre_bin[0] = socre_bin[0] - 1
            df[col + 'score_bins'] = pd.DataFrame(pd.cut(df[col], bins=list(
                range(int(min(socre_bin) - min(socre_bin) % 10),
                    int(max(socre_bin) + (step + 10 - max(socre_bin) % 10)), step))))
            # df[col + 'score_bins'] = pd.DataFrame(pd.cut(df[col], bins=socre_bin, duplicates='drop'))
        # *********************等频***************************
        elif type == 'dp':
            print(col)
            df[col + 'score_bins'] = pd.DataFrame(pd.qcut(df[col], q=step, duplicates='drop'))
        # *********************等距***************************
        else:
            df[col + 'score_bins'] = pd.DataFrame(pd.cut(df[col], bins=step, duplicates='drop'))
        df[col + 'score_bins'] = df[col + 'score_bins'].fillna('MISSING')
        score_lst.append(col + 'score_bins')
    bin_data = Data_Woe(df, score_lst, target, value, types='tt')


    return bin_data


if __name__ == '__main__':
    filePath = r'E:\HusseinWorkFiles\***'
    data = pd.read_csv(filePath+r'\score.csv')
    bin = CUT_BIN(data, ['score'] + ['y'], 10, 'y', value='apply_id', type='Norm')
    bin.to_csv(filePath + r'\score_bins.csv')
