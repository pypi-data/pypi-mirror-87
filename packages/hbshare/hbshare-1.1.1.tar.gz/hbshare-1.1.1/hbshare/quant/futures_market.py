import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from hbshare.quant.cons import sql_write_path_hb
from .load_data import load_calendar_extra
import pymysql

pymysql.install_as_MySQLdb()


def wind_product_index_perc(
        start_date, end_date,
        db_path=sql_write_path_hb['daily'],
        table='commodities_index_wind',
        min_volume=10000
):
    engine = create_engine(db_path)
    data = pd.read_sql_query(
        'select `code`, `name`, `t_date`, `close`, `product`, `volume` from ' + table
        + ' where `t_date`<=' + end_date.strftime('%Y%m%d')
        + ' and `t_date`>=' + start_date.strftime('%Y%m%d')
        + ' and `product` not in (\'index\') order by `t_date` desc',
        engine
    )

    products = data.drop_duplicates(['product'])['product'].reset_index(drop=True)

    price_perc = []
    name_list = []
    for i in range(len(products)):
        product_data = data[data['product'] == products[i]].reset_index(drop=True)
        if product_data['volume'][:60].mean() < min_volume:
            continue

        product_price_perc = (
                                product_data['close'][0] - min(product_data['close'])
                             ) / (
                                max(product_data['close']) - min(product_data['close'])
                            )
        price_perc.append(product_price_perc)
        name_list.append(product_data['name'][0].replace('指数', ''))

    result = pd.DataFrame(
        {
            'name': name_list,
            'price_perc': price_perc
        }
    )

    return result.sort_values(by='price_perc', ascending=False).reset_index(drop=True)


def wind_product_index_sigma_xs(
        start_date, end_date,
        db_path=sql_write_path_hb['daily'], table='nh_index_wind', freq=''
):
    engine = create_engine(db_path)
    data_raw = pd.read_sql_query(
        'select `code`, `name`, `t_date`, `close`, `product`, `volume` from ' + table
        + ' where `t_date`<=' + end_date.strftime('%Y%m%d')
        + ' and `t_date`>=' + start_date.strftime('%Y%m%d')
        + ' and `product` not in (\'index\') order by `t_date`',
        engine
    )

    calendar = load_calendar_extra(freq=freq, start_date=start_date, end_date=end_date, db_path=db_path)
    result = calendar.copy()

    products = data_raw.drop_duplicates(['product'])['product'].tolist()
    names = []
    for i in products:
        print(i)
        data = data_raw[data_raw['product'] == i].reset_index(drop=True)
        data_clean = calendar.merge(data[['t_date', 'close']], on='t_date')
        data_clean['ret'] = data_clean['close'] / data_clean['close'].shift(1) - 1
        result = result.merge(
            data_clean[['t_date', 'ret']].rename(
                columns={'ret': data['name'][0].replace('指数', '').replace('南华', '')}
            ),
            on='t_date', how='left'
        )
        names.append(data['name'][0].replace('指数', '').replace('南华', ''))
    result['sigma'] = result[names].apply(lambda x: np.std(x, ddof=1), axis=1)
    result['mean'] = result[names].apply(lambda x: np.nanmean(x), axis=1)
    return result



