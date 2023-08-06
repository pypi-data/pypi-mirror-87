from hbshare.quant.load_data import load_funds_data, load_funds_outperformance
import pandas as pd
import numpy as np
import pyecharts.options as opts
from datetime import datetime, timedelta
from pyecharts.charts import Line, Tab, Grid
import pymysql
from sqlalchemy import create_engine
from hbshare.quant.cons import sql_write_path_hb

pymysql.install_as_MySQLdb()

db_path = sql_write_path_hb['work']
cal_path = sql_write_path_hb['daily']


def nav_lines(fund_list, start_date, end_date, title='', zz=False):

    if zz:
        funds_data = load_funds_outperformance(
            fund_list=fund_list,
            first_date=start_date,
            end_date=end_date,
            db_path=db_path,
            cal_db_path=cal_path
        )['eav']
    else:
        funds_data = load_funds_data(
            fund_list=fund_list,
            first_date=start_date,
            end_date=end_date,
            db_path=db_path,
            cal_db_path=cal_path,
            # freq='',
            # fillna=False
        )

    web = Line(
        init_opts=opts.InitOpts(
            page_title=title,
            width='700px',
            height='500px',
            # theme=ThemeType.DARK
        )
    ).set_global_opts(
        tooltip_opts=opts.TooltipOpts(is_show=True),
        toolbox_opts=opts.ToolboxOpts(is_show=True),
        xaxis_opts=opts.AxisOpts(type_="category"),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ),
    ).add_xaxis(
        xaxis_data=funds_data['t_date'].tolist()
    )
    funds = funds_data.columns.tolist()

    # fund_monthly = ['德劭锐哲中国']
    # for m in fund_monthly:
    #     if m in funds:
    #         fund_data = load_funds_data(
    #             fund_list=pd.read_sql_query(
    #                 'select * from fund_list where `name`="' + m + '"', engine
    #             ),
    #             first_date=start_date,
    #             end_date=end_date,
    #             freq='month'
    #         )
    #         funds_data[m] = fund_data[m]
    funds.remove('t_date')
    for j in funds:
        nav_data = funds_data[j] / funds_data[funds_data[j] > 0][j].tolist()[0]
        web.add_yaxis(
            series_name=j,
            y_axis=nav_data.round(4).tolist(),
            symbol="emptyCircle",
            is_symbol_show=True,
            label_opts=opts.LabelOpts(is_show=False),
        )

    web.set_global_opts(
        xaxis_opts=opts.AxisOpts(
            is_scale=True,
            type_="category", boundary_gap=False
        ),
        yaxis_opts=opts.AxisOpts(
            is_scale=True,
            splitarea_opts=opts.SplitAreaOpts(
                is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
            ),
        ),
        legend_opts=opts.LegendOpts(
            # type_='scroll',
            pos_top='5%'
        ),
        datazoom_opts=[
            opts.DataZoomOpts(range_start=0, range_end=100),
            # opts.DataZoomOpts(pos_left="5%", xaxis_index=0),
            # opts.DataZoomOpts(pos_right="5%", xaxis_index=1),
            opts.DataZoomOpts(type_="inside")
        ],
        title_opts=opts.TitleOpts(title=title),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross")
    )

    return web


def gen_grid(end_date, class0, type0, zz):
    engine = create_engine(sql_write_path_hb['work'])
    start_date = end_date - timedelta(days=365 * 2 + 7)
    start_date2 = end_date - timedelta(days=365 + 7)

    fund_list = pd.read_sql_query(
        'select * from fund_list where `class`="' + class0
        + '" and `type`="' + type0
        + '" and `stopped`!= 1 order by `name`', engine
    )

    grid_nav = Grid(init_opts=opts.InitOpts(width="1200px", height="600px"))

    web = nav_lines(
        fund_list=fund_list,
        start_date=start_date,
        end_date=end_date,
        zz=zz
    )

    web2 = nav_lines(
        fund_list=fund_list,
        start_date=start_date2,
        end_date=end_date,
        zz=zz
    )

    grid_nav.add(
        web.set_global_opts(
            title_opts=opts.TitleOpts(
                title=class0 + ' ' + type0 + ' 近两年: '
                      + start_date.strftime('%Y/%m/%d') + '~' + end_date.strftime('%Y/%m/%d')
                ,
                pos_right="5%"
            ),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            legend_opts=opts.LegendOpts(
                pos_top="8%"
            )
        ),
        grid_opts=opts.GridOpts(pos_left='55%', pos_top="22%")
    ).add(
        web2.set_global_opts(
            title_opts=opts.TitleOpts(
                title=class0 + ' ' + type0 + ' 近一年: '
                      + start_date2.strftime('%Y/%m/%d') + '~' + end_date.strftime('%Y/%m/%d')
                ,
                pos_left="5%"
            ),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            legend_opts=opts.LegendOpts(
                pos_top="8%"
            )
        ),
        grid_opts=opts.GridOpts(pos_right='55%', pos_top="22%")
    )
    return grid_nav


def gen_tab(end_date, class0):
    engine = create_engine(sql_write_path_hb['work'])
    start_date = end_date - timedelta(days=365 * 2 + 7)
    start_date2 = end_date - timedelta(days=365 + 7)

    fund_list = pd.read_sql_query(
        'select * from fund_list where `class`="' + class0 + '" and `stopped`!= 1 order by `name`', engine
    )
    class_list = fund_list['type'].drop_duplicates().tolist()
    class_dict = {
        class0: class_list,
        # '中性': class_list_zx,
        # '指增': class_list_zz
    }
    tab = Tab(
        page_title=class0 + '量化产品净值' + end_date.strftime('%Y%m%d'),
    )

    for c in class_dict:
        class_list = class_dict[c]
        if c == '指增':
            zz = True
        else:
            zz = False

        for i in range(len(class_list)):
            grid_nav = Grid(init_opts=opts.InitOpts(width="1200px", height="600px"))

            web = nav_lines(
                fund_list=fund_list[
                    np.array(fund_list['type'] == class_list[i]) & np.array(fund_list['class'] == c)
                    ].reset_index(drop=True),
                start_date=start_date,
                end_date=end_date,
                zz=zz
            )

            web2 = nav_lines(
                fund_list=fund_list[
                    np.array(fund_list['type'] == class_list[i]) & np.array(fund_list['class'] == c)
                    ].reset_index(drop=True),
                start_date=start_date2,
                end_date=end_date,
                zz=zz
            )

            grid_nav.add(
                web.set_global_opts(
                    title_opts=opts.TitleOpts(
                        title=class_list[i] + ' 近两年 '
                        + start_date.strftime('%Y/%m/%d') + '~' + end_date.strftime('%Y/%m/%d')
                        ,
                        pos_right="5%"
                    ),
                    tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
                    legend_opts=opts.LegendOpts(
                        pos_top="8%",
                        # pos_right="20%",
                        # pos_left="20%"
                    )
                ),
                grid_opts=opts.GridOpts(pos_left='55%', pos_top="18%")
            ).add(
                web2.set_global_opts(
                    title_opts=opts.TitleOpts(
                        title=class_list[i] + ' 近一年 '
                        + start_date2.strftime('%Y/%m/%d') + '~' + end_date.strftime('%Y/%m/%d')
                        ,
                        pos_left="5%"
                    ),
                    tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
                    legend_opts=opts.LegendOpts(
                        pos_top="8%",
                        # pos_right="20%",
                        # pos_left="20%"
                    )
                ),
                grid_opts=opts.GridOpts(pos_right='55%', pos_top="18%")
            )
            name = c + ':' + class_list[i]
            if c == '指增':
                name += '（超额）'
            tab.add(grid_nav, name)
    return tab


if __name__ == '__main__':

    end_date = datetime(2020, 10, 30).date()
    tab = Tab(page_title='量化产品净值' + end_date.strftime('%Y%m%d'))

    class_dict = {
        'cta': [
            '长周期',
            '短周期',
            '多空',
            '混合',
            '基本面',
            '主观'
        ],
        '中性': [
            '高频',
            '中低频',
            '多空'
        ],
        '指增': [
            '量价',
            '机器学习',
            '基本面'
        ]
    }

    for c in class_dict:
        print(c)
        if c == '指增':
            zz = True
        else:
            zz = False

        for i in class_dict[c]:
            grid_n = gen_grid(end_date=end_date, class0=c, type0=i, zz=zz)

            name = c + ':' + i
            if c == '指增':
                name += '（超额）'
            if c == '中性' and i == '多空':
                name = i

            tab.add(grid_n, name)

    tab.render()
