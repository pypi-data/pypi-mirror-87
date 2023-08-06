# 统计基金表现的def

import pandas as pd
import numpy as np
from datetime import datetime
from sqlalchemy import create_engine
import pymysql
from .load_data import load_funds_data

pymysql.install_as_MySQLdb()


def ret(data_df):
    funds = data_df.columns.tolist()
    date_col = 't_date'
    if 't_date' in funds:
        funds.remove(date_col)
    elif '日期' in funds:
        date_col = '日期'
        funds.remove('日期')

    result_all = data_df['t_date']

    for i in funds:
        single_df = data_df[[date_col, i]].copy()
        single_df['ret'] = single_df[i] / single_df[i].shift(1) - 1

        result_all = pd.merge(result_all, single_df[['t_date', 'ret']], on='t_date').rename(columns={'ret': i})

    return result_all


# 计算每只产品的年化收益，年华波动，夏普，最大回撤等指标
def performance_analysis(
        data_df,
        risk_free=0.015,
        start_date=datetime(2019, 1, 1).date(),
        end_date=datetime(2099, 12, 31).date(),
        ret_num_per_year=52
):

    funds = data_df.columns.tolist()
    date_col = 't_date'
    if 't_date' in funds:
        funds.remove(date_col)
    elif '日期' in funds:
        date_col = '日期'
        funds.remove('日期')
    # data_df['ret'] = data_df['nav'] / data_df['nav'].shift(1)

    result_all = pd.DataFrame()
    dd_all = data_df[[date_col]].copy()
    ret_all = data_df[[date_col]].copy()
    for i in funds:
        single_df = data_df[[date_col, i]]
        data_before = single_df[single_df[date_col] < start_date][date_col].tolist()
        if len(data_before) > 0:
            start_date_lag1 = data_before[-1]
        else:
            start_date_lag1 = start_date
        single_df = single_df[
            np.array(single_df[date_col] >= start_date_lag1) & np.array(single_df[date_col] <= end_date)
            ].reset_index(drop=True)

        single_data = single_df[single_df[i] > 0]
        if len(single_data) > 1:
            print('\t计算 ' + i + ' 指标')
            start_index = single_data.index[0]
            single_df = single_df.iloc[start_index:].reset_index(drop=True)

            # 剔除最新净值之后的空置（若产品最新净值未按时更新）
            single_df = single_df[single_df[i] > 0].reset_index(drop=True)

            single_df['ret'] = single_df[i] / single_df[i].shift(1) - 1
            single_df['highest'] = single_df[i].cummax()
            single_df['dd'] = (single_df[i] - single_df['highest']) / single_df['highest']
            max_dd = min(single_df['dd'])

            fund_last_days = single_df[date_col][len(single_df) - 1] - single_df[date_col][0]
            annualized_return = (single_df[i][len(single_df) - 1] / single_df[i][0]) ** (365 / fund_last_days.days) - 1
            annualized_return_mean = np.mean(single_df['ret'][1:] + 1) ** ret_num_per_year - 1  # 复利年化
            annualized_return_mean_simple = np.mean(single_df['ret'][1:]) * ret_num_per_year
            annualized_vol = np.std(single_df['ret'][1:], ddof=1) * np.sqrt(ret_num_per_year)

            single_df['downside_risk'] = single_df['ret'] #- risk_free
            single_df['downside_risk'][single_df['downside_risk'] > 0] = 0
            downside_vol = np.std(single_df['downside_risk'][1:], ddof=1) * np.sqrt(ret_num_per_year)
            sharpe = (annualized_return - risk_free) / annualized_vol
            sortino = (annualized_return - risk_free) / downside_vol
            if max_dd < 0:
                calmar = annualized_return / -max_dd
            else:
                calmar = None

            win_rate = sum(single_df['ret'] > 0) / (len(single_df) - 1)
            win_loss = (
                    np.average(single_df[single_df['ret'] > 0]['ret'])
                    / np.average(-single_df[single_df['ret'] < 0]['ret'])
            )
            if i in ['德劭锐哲中国', '腾胜中国聚量1号']:
                annualized_return_mean = np.nan
                annualized_vol = np.nan
                sharpe = np.nan
                sortino = np.nan
                win_rate = np.nan
                win_loss = np.nan
        else:
            annualized_return = np.nan
            annualized_return_mean = np.nan
            annualized_return_mean_simple = np.nan
            annualized_vol = np.nan
            max_dd = np.nan
            sharpe = np.nan
            sortino = np.nan
            calmar = np.nan
            win_rate = np.nan
            win_loss = np.nan

        result_single = pd.DataFrame(
            {
                start_date.strftime('%Y%m%d') + '以来年化': annualized_return,
                '平均周收益年化(复利)': annualized_return_mean,
                # '平均年化收益(单利)': annualized_return_mean_simple,
                '年化波动率': annualized_vol,
                '最大回撤': max_dd,
                'Sharpe': sharpe,
                'Sortino': sortino,
                # '收益峰度': single_df['ret'][1:].kurt(),
                # '收益偏度': single_df['ret'][1:].skew(),
                'Calmar': calmar,
                '投资胜率': win_rate,
                '平均损益比': win_loss

            }, index={i}
        ).T.reset_index()
        if len(result_all) == 0:
            result_all = result_single
        else:
            result_all = result_all.merge(result_single, on='index')

        # if len(dd_all) == 0:
        #     dd_all = single_df[['t_date', 'dd']].rename(columns={'dd': i})
        # else:
        dd_all = dd_all.merge(single_df[[date_col, 'dd']].rename(columns={'dd': i}), on=date_col, how='left')

        # if len(ret_all) == 0:
        #     ret_all = single_df[['t_date', 'ret']].rename(columns={'ret': i})
        # else:
        ret_all = ret_all.merge(single_df[[date_col, 'ret']].rename(columns={'ret': i}), on=date_col, how='left')

    return result_all, dd_all, ret_all
