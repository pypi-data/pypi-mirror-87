import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

def get_ratio_list(input_list):   
    ratio_list = []
    total = sum(input_list)
    for amt in input_list:
        ratio_list.append(round(amt / total, 2))
    return (ratio_list)

def get_color_list(color, elem_num):
    color_list = []
    color_list.append(color)
    for idx in range(elem_num - 1):
        color_list.append(px.colors.sequential.Greys[8 - (idx + 1)])
    return(color_list)

def sort_values(acc_list, ratio_list):
    merged = []
    for idx in range(len(acc_list)):
        merged.append((acc_list[idx], ratio_list[idx]))
    return (sorted(merged, key = lambda tup: tup[1], reverse = True))

def 도넛(최상위계정명, 세부계정리스트, 금액리스트, 색상맵):

    r""" 최상위계정에 속하는 각 세부계정의 비율을 자동으로 계산하고 도넛차트로 시각화합니다.

    :param 최상위계정명(string) : 자산, 부채, 자본 중 최상위계정명
    :param 세부계정리스트(list) : 자산, 부채, 자본에 속하는 세부계정명리스트
    :param 금액리스트(list) : 세부계정금액리스트
    :param 색상맵(list) : 반시계방향으로 적용되는 색상리스트

    :return(figure) : """

    #Get color list
    color_list = []
    if (len(세부계정리스트) <= len(색상맵)):
        for idx in range(len(세부계정리스트)):
            color_list.append(색상맵[idx])
        color_list[-1] = px.colors.sequential.Greys[2]
    else:
        color_list += 색상맵
        grays = []
        for idx in range(len(세부계정리스트) - len(색상맵)):
            grays.append(px.colors.sequential.Greys[idx])
        grays.reverse()
        color_list += grays
    
    #Data tuning
    ratio_list = get_ratio_list(금액리스트)
    sorted_set = sort_values(세부계정리스트, ratio_list)
    final_labs = [acc for (acc, ratio) in sorted_set]
    final_ratio = [ratio for (acc, ratio) in sorted_set]
    final_amt = 금액리스트.copy()
    final_amt.sort(reverse = True)

    #Tracing
    fig = go.Figure()
    fig.add_traces(go.Pie(
        name = "",
        labels = final_labs,
        values = final_ratio,
        hole = 0.7,
        scalegroup = "one",
        marker = dict(colors = color_list), 
        hoverlabel = dict(    
            font = dict(
                family = "Arial",
                size = 12
            ),
            bordercolor = "white"
        ),
        textfont = dict(color = "white", family = "Arial"),
        customdata = final_amt,
        hovertemplate='\t<br>\t<b>%{label} </b> <br> %{customdata[0]}(원)\t<br>\t<br>',
        insidetextorientation = "tangential"
    ))
    
    fig.update_layout(
        uniformtext_minsize = 13,
        uniformtext_mode = "hide",
        width = 700,
        height = 500,
        font = dict(
            size = 13,
            family = "Arial",
            color = "white",
        ),
        paper_bgcolor = "rgba(0,0,0,0)",
        legend = dict(
            font = dict(
                color = "Black",
                family = "Arial",
                size = 13,
            ),
        ) 
    )
    
    fig.add_annotation(
        text = "<b>" + 최상위계정명 + "</br>",
        xref="paper", yref="paper",
        x= 0.5, y = 0.5,
        font = dict(
            color = "Black",
            size = 16,
            family = "Arial"
        ),
        align = "center",
        borderwidth = 8,
        showarrow = False
    )
    return (fig)

def 썬버스트_BS(
    자산세부계정리스트, 부채세부계정리스트, 자본세부계정리스트, 
    자산금액리스트, 부채금액리스트, 자본금액리스트, 색상맵):

    r"""자산, 부채, 자본의 세부계정 비율을 자동으로 계산하고 시각화합니다.

    :param 자산세부계정리스트(list) : 자산의 세부계정명 리스트
    :param 부채세부계정리스트(list) : 부채의 세부계정명 리스트
    :param 자본세부계정리스트(list) : 자본의 세부계정명 리스트
    :param 자산금액리스트(list) : 자산의 각 세부계정 별 금액 리스트
    :param 부채금액리스트(list) : 부채의 각 세부계정 별 금액 리스트
    :param 자본금액리스트(list) : 자본의 각 세부계정 별 금액 리스트
    :param 색상맵(list) : 자산, 부채, 자본 계정의 색상리스트

    :return: (fig)"""
    
    #Data tuning
    total = sum(자산금액리스트) + sum(부채금액리스트) + sum(자본금액리스트)
    amt_list = [total, sum(자산금액리스트), sum(부채금액리스트), sum(자본금액리스트)] + \
                자산금액리스트 + 부채금액리스트 + 자본금액리스트
    
    asset_ratio_list = [round(amt / total, 2) for amt in 자산금액리스트]
    debt_ratio_list = [round(amt / total, 2) for amt in 부채금액리스트]    
    equity_ratio_list = [round(amt / total, 2) for amt in 자본금액리스트]
    total = sum(asset_ratio_list) + sum(debt_ratio_list) + sum(equity_ratio_list)
    
    title = "<b>재무상태표</b>"
    labs = [title, "<b>자산</b>", "<b>부채</b>", "<b>자본</b>"] + \
            자산세부계정리스트 + 부채세부계정리스트 + 자본세부계정리스트
    
    parents = [""] + [title] * 3 +  ["<b>자산</b>"] * len(자산세부계정리스트) + \
              ["<b>부채</b>"] * len(부채세부계정리스트) + ["<b>자본</b>"] * len(자본세부계정리스트)
    
    vals = [total, sum(asset_ratio_list), sum(debt_ratio_list), sum(equity_ratio_list)] + \
            asset_ratio_list + debt_ratio_list + equity_ratio_list
    
    hover_vals = [1, sum(asset_ratio_list), sum(debt_ratio_list), sum(equity_ratio_list)] + \
                  get_ratio_list(자산금액리스트) + get_ratio_list(부채금액리스트) + get_ratio_list(자본금액리스트)
    hover_vals = [round(amt * 100, 2) for amt in hover_vals]
    
    #Tracing
    fig = go.Figure()
    fig.add_traces(go.Sunburst(
        name = "",
        labels = labs,
        parents = parents, 
        values = vals,
        branchvalues = "total",
        hoverlabel = dict(
            font = dict(
                family = "Arial",
                size = 13,
            ),
        ),
        customdata = np.transpose([hover_vals, amt_list]),
        hovertemplate = '\t%{label}<br>\t%{customdata[0]}%<br>\t%{customdata[1]}원\t<br>',
        insidetextorientation = "auto",
        marker = dict(colors = 색상맵)
    ))
        
    fig.update_layout(
        font = dict(
            family = "Arial",
            size = 13,
        ),
        width = 750,
        height = 550,
        uniformtext_minsize = 12.5,
    )    
        
    return fig

def 썬버스트_IS(매출원가_판매비와관리비_영업이익금액리스트, 색상맵):

    r"""매출액 대비 매출원가, 매출총이익, 판매비와관리비, 영업이익의 비율의 자동으로 게산하여 시각화합니다.

    :param 매출원가_판매비와관리비_영업이익금액리스트(list) : 매출원가, 판매비와관리비, 영업이익의 금액 리스트
    :param 색상맵(list) : 색상리스트

    :return: (fig)"""
    
    #Data tuning
    매출원가 = 매출원가_판매비와관리비_영업이익금액리스트[0]
    판매비와관리비 = 매출원가_판매비와관리비_영업이익금액리스트[1]
    영업이익 = 매출원가_판매비와관리비_영업이익금액리스트[2]
    
    ratio_list = get_ratio_list([매출원가, 판매비와관리비, 영업이익])
    ratio_list = [sum(ratio_list), ratio_list[0], ratio_list[1] + ratio_list[2], ratio_list[1], ratio_list[2]]
    amt_list = [sum([매출원가, 판매비와관리비, 영업이익]), 매출원가, sum([판매비와관리비 + 영업이익]), 판매비와관리비, 영업이익]
    hover_list = ratio_list[0:3] + [ratio_list[3] / ratio_list[2], ratio_list[4] / ratio_list[2]]
    hover_list = [amt * 100 for amt in hover_list]
    
    for idx in range(len(ratio_list)):
        ratio_list[idx] = round(ratio_list[idx], 2)
        hover_list[idx] = round(hover_list[idx], 2)
    
    title = "<b>매출액</b>"
    labs = ["<b>매출액</b>", "<b>매출원가</b>", "<b>매출총이익</b>", "판매비", "영업이익"]
    parents = ["", "<b>매출액</b>", "<b>매출액</b>", "<b>매출총이익</b>", "<b>매출총이익</b>"]
    
    #Tracing
    fig = go.Figure()
    fig.add_traces(go.Sunburst(
        name = "",
        labels = labs,
        parents = parents, 
        values = ratio_list,
        branchvalues = "total",
        hoverlabel = dict(
            font = dict(
                family = "Arial",
                size = 13,
            ),
        ),
        customdata = np.transpose([hover_list, amt_list]),
        hovertemplate = '\t%{label}<br>\t%{customdata[0]}%<br>\t%{customdata[1]}원\t<br>',
        insidetextorientation = "auto",
        marker = dict(colors = 색상맵)
    ))
        
    fig.update_layout(
        font = dict(
            family = "Arial",
            size = 13,
        ),
        width = 750,
        height = 550,
    )    
        
    return fig

def 비율비교(제목, 기업리스트, 세부계정리스트, 색상맵, 높이, **기업명및금액리스트):

    r"""기업별 세부계정의 비율을 자동으로 계산하여 비교할 수 있도록 시각화합니다.

    :param 제목(string) : 그래프 상단 타이틀
    :param 기업리스트(list) : 기업명 리스트
    :param 세부계정리스트(list) : 세부계정명 리스트
    :param 색상맵(list) : 각 계정별로 적용할 색상 리스트
    :param 기업명및금액리스트(list) : 다음과 같은 형식으로 기업의 금액리스트를 입력합니다. (예 - 기업명 = [10, 20, 30, 40])

    :return: (fig)"""
    
    #Get color list
    color_list = []
    if (len(세부계정리스트) <= len(색상맵)):
        for idx in range(len(세부계정리스트)):
            color_list.append(색상맵[idx])
        #color_list[-1] = px.colors.sequential.Greys[2]
    else:
        color_list += 색상맵
        grays = []
        for idx in range(len(세부계정리스트) - len(색상맵)):
            grays.append(px.colors.sequential.Greys[idx + 3])
        grays.reverse()
        color_list += grays
    
    corp_list = []
    for corp in 기업리스트:
        corp_list.append("<b>" + corp + "</b>\t\t")
        
    #Tracing
    fig = go.Figure()
    for idx in range(len(세부계정리스트)):
        ratio_list = []
        amt_list = []
        for corp_name, val_list in 기업명및금액리스트.items():
            s = sum(val_list)
            amt_list.append(round(val_list[idx]))
            ratio_list.append(round(val_list[idx] / s * 100, 2))
        
        fig.add_trace(go.Bar(
            name = 세부계정리스트[idx],
            x = ratio_list,
            y = corp_list,
            orientation = "h",
            marker = dict(
                color = color_list[idx],
                line = dict(
                    color = "white",
                    width = 2
                )
            ),
            customdata = np.transpose([[세부계정리스트[idx]] * len(amt_list), amt_list]),
            hovertemplate =  "<b>%{customdata[0]}</b><br>%{x}%<br>%{customdata[1]}원",
            hoverlabel = dict(
                font = dict(
                    family = "Arial",
                    size = 13,
                ),            
            ),
        ))
                              
    fig.update_layout( 
        title = dict(
            text = "<b>" + 제목 + "</b>",
            font = dict(
                family = "Arial",
                size = 14,
                color = "Black",
            ),
            x = 0.43,
            y = 0.8
        ),
        paper_bgcolor = "rgba(0,0,0,0)",
        plot_bgcolor = "rgba(0,0,0,0)",
        xaxis = dict(
            title = "비율 (%)",
            tickfont = dict(
                family = "Arial",
                size = 13,
                color = "darkgrey")),
        yaxis = dict(
                tickfont = dict(
                family = "Arial",
                size = 13,
                color = "Black")), 
        width = 800,
        height = 높이,
        legend = dict(
            font = dict(
                color = "Black",
                family = "Arial",
                size = 13,
            ),
        ) 
    )

    fig.update_layout(
        barmode='stack',
    )
    
    return fig

def 버블(
    제목,
    기업리스트, 
    x축이름, x축리스트, y축이름, y축리스트, 
    크기라벨명, 크기리스트, 색상라벨명, 색상리스트,
    크기최대값, x축범위, y축범위, 색상맵):

    r"""버블 차트를 시각화 합니다.

    :param 제목(string) : 그래프 상단 타이틀
    :param 기업리스트(list) : 기업명 리스트
    :param x축이름(string) : 단위를 포함한 x축 이름 (예 - 영업이익(원))
    :param x축리스트(list) : x축의 수치리스트
    :param y축이름(string) : 단위를 포함한 y축 이름(예 - 매출액(원))
    :param y축리스트(list) : y축의 수치리스트
    :param 크기라벨명(string) :각 plotting point의 크기를 구별할 수치들의 이름
    :param 크기리스트(list) : 각 plotting point의 크기를 구별할 수치 리스트
    :param 색상라벨명(string) : 각 plotting point의 색상을 구별할 라벨들의 이름
    :param 색상리스트(list) : 각 plotting point의 색상을 구별할 라벨 리스트
    :param 크기최대값(int) : plotting points의 크기 최댓값
    :param x축범위(list) : 그래프에 표시할 x축의 범위(예) - [0, 100])
    :param y축범위(list) : 그래프에 표시할 y축의 범위(예) - [-10, 100])
    :param 색상맵(list) : 색상리스트의 값에 따라 적용될 색깔 리스트

    :return: (fig)"""
    
    #Data tuning
    df = pd.DataFrame(columns = ["기업명", x축이름, y축이름, 크기라벨명, 색상라벨명])
    df["기업"] = 기업리스트
    df[x축이름] = x축리스트
    df[y축이름] = y축리스트
    df[크기라벨명] = 크기리스트
    df[색상라벨명] = 색상리스트

    #Tracing
    fig = px.scatter(
        df, x =  x축이름, y = y축이름, size = 크기라벨명, color = 색상라벨명, 
        hover_name = "기업", size_max = 크기최대값, log_x = False, log_y = False, color_discrete_sequence = 색상맵,   
    )
    
    fig.update_layout( 
        title = dict(
            text = "<b>" + 제목 + "</b>",
            font = dict(
                family = "Arial",
                size = 14,
                color = "Black",
            ),
            x = 0.5,
            y = 0.95
        ),
        paper_bgcolor = "rgba(0,0,0,0)",
        plot_bgcolor = "rgba(0,0,0,0)",
        font = dict(size = 13),
        hoverlabel = dict(
            font = dict(
                family = "Arial",
                size = 13,
            ), 
        ),
        xaxis = dict(
            titlefont = dict(
                size = 13,
                family = "Arial",
                color = "Black"
            ),
            tickfont = dict(
                family = "Arial",
                size = 13,
                color = "Black"
            ),
            range = x축범위
        ),
        yaxis = dict(
            titlefont = dict(
                size = 13,
                family = "Arial"
            ),
            tickfont = dict(
                family = "Arial",
                size = 13,
                color = "Black"
            ),
            range = y축범위
        ),
        width = 900,
        height = 500,
        legend = dict(
            title = "  " + 색상라벨명 +"<br>",
            font = dict(
                color = "Black",
                family = "Arial",
                size = 13
            ),
        ) 
    )
    return fig

def 도넛_02(비율명, 분모계정명, 분자계정명, 분모계정금액, 분자계정금액, 색상):

    r"""분자계정금액 / 분모계정금액 비율을 자동으로 계산하여 해당 비율을 시각화 합니다.

    :param 비율명(string) : 비율이름
    :param 분모계정명(string) : 분모계정의 이름
    :param 분자계정명(string) : 분자계정의 이름
    :param 분모계정금액(float) : 분모계정의 금액
    :param 분자계정금액(float) : 분자계정의 금액
    :param 색상(string) : 비율을 표시할 색상

    :return (fig)"""
   
    #Data tuning
    ratio = round(분자계정금액 / 분모계정금액 * 100, 2)
    final_ratio = (100 if (ratio >= 100) else ratio)
    color_list = [색상, px.colors.sequential.Greys[2]]
    
    #Tracing
    fig = go.Figure()
    fig.add_traces(go.Pie(
        name = "",
        labels = ["ratio", "100 - ratio"],
        values = [final_ratio, 100 - final_ratio],
        hole = 0.7,
        scalegroup = "one",
        text = None,
        marker = dict(colors = color_list), 
        hoverinfo = "none",
        insidetextorientation = "tangential"
    ))
    
    fig.update_layout(
        uniformtext_minsize = 13,
        uniformtext_mode = "hide",
        width = 700,
        height = 500,
        paper_bgcolor = "rgba(0,0,0,0)",
        legend = dict(
            font = dict(
                color = "Black",
                family = "Arial",
                size = 13,
            ),
        ) ,
        showlegend = False,
    )
    
    fig.add_annotation(
        text = "<b>" + 비율명 + "</b>",
        xref="paper", yref="paper",
        x= 0.5, y = 0.55,
        font = dict(
            color = "Black",
            size = 16,
            family = "Arial"
        ),
        align = "center",
        borderwidth = 8,
        showarrow = False
    )

    fig.add_annotation(
        text = 분자계정명 + " " +  str(round(분자계정금액)) + "(원)<br>" + 분모계정명 + " " + str(round(분모계정금액)) + "(원)",
        xref="paper", yref="paper",
        x= 0.5, y = 0.45,
        font = dict(
            color = "Black",
            size = 13,
            family = "Arial"
        ),
        align = "center",
        showarrow = False
    )
    
    return fig

def 방사형(제목, 비율이름리스트, 색상맵, **기업및비율리스트):

    r"""기업별 비율 분석 결과를 방사형 그래프로 시각화 합니다.

    :param 제목(string) : 그래프 상단 타이틀
    :param 비율이름리스트(list) : 비율항목의 이름 리스트
    :param 색상맵(list) : 기업별 색상 리스트
    :param 기업및비율리스트(list) :	 각 기업의 비율리스트(예) - 기업명 = [10, 20, 30, 40])

    :return (fig)"""

    #Data tuning
    for idx in range(len(비율이름리스트)):
        비율이름리스트[idx] = "<b>" + 비율이름리스트[idx] + "</b>"
    
    #Tracing
    fig = go.Figure()
    idx = 0
    for corp_name, val_list in 기업및비율리스트.items():
        fig.add_trace(go.Scatterpolar(
            name = "<b>" + corp_name + "</b>",
            r = val_list,
            theta = 비율이름리스트,
            mode = "lines+text",
            fill = "toself",
            fillcolor = 색상맵[idx],
            line = dict(color = 색상맵[idx], width = 2),
            marker_color = "rgba(0, 0, 0, 0)",
            hoverlabel = dict(
                font = dict(
                family = "Arial",
                size = 13)),
            hovertemplate='%{r}%<br>',
        ))
        idx += 1
    
    fig.update_layout(
       title = dict(
            text = "<b>" + 제목 + "</b>",
            font = dict(
                family = "Arial",
                size = 14,
                color = "Black",
            ),
            x = 0.5,
            y = 0.95
        ),  
        width = 700,
        height = 500,
        font = dict(
            size = 13,
            color = "Black",
            family = "Arial"
        ),
        polar = dict(
            radialaxis = dict(
                tickfont = dict(
                    color = "Darkgrey",
                    family = "Arial",
                    size = 12,
                ),
                tickangle = 45,
            ),
            angularaxis = dict(
                rotation=90, 
                direction="counterclockwise"
            )
        ),
        polar_bgcolor = px.colors.sequential.Greys[1],
        paper_bgcolor = "rgba(0,0,0,0)",
        legend = dict(
            font = dict(
            color = "Black",
            family = "Arial",
            size = 13,
            ),
            orientation = "h"
        ),
        margin = dict(pad = 20)
    )

    return fig

def 막대(제목, 기업리스트, y축이름, 수치리스트, 색상맵, 범례명리스트, 범례색상리스트, 수치선색상):

    r""" x축은 기업, y축은 데이터를 입력하여 기업별 데이터 수치를 막대차트로 시각화 합니다. 분위수와 평균 값을 자동으로 계산하여 옵션으로 제공합니다.
    
    :param 제목(string) : 그래프 상단 타이틀
    :param 기업리스트(list) : 기업명 리스트
    :param y축이름(string) : 단위를 포함한 y축의 이름(예) - "유동비율(원)")
    :param 색상맵(list) : 기업별로 적용할 색상리스트, 기업리스트 사이즈와 색상맵 리스트의 사이즈는 같아야 함
    :param 범례명리스트(list) : 범례의 각 항목별 이름리스트
    :param 범례색상리스트(list) : 범례의 각 항목별로 적용할 색상 리스트
    :param 수치선색상(string) : 분위수, 평균값을 표시하는 수치선의 색상

    :return: (fig)"""

    merged = []
    for idx in range(len(기업리스트)):
        merged.append((기업리스트[idx], 수치리스트[idx], 색상맵[idx]))
    
    merged = sorted(merged, key = lambda tup: tup[1], reverse = True)
    
    기업리스트 = ["<br>" + corp for (corp, ratio, color) in merged]
    수치리스트 = [ratio for (corp, ratio, color) in merged]
    색상맵 = [color for (corp, ratio, color) in merged]

    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x = 기업리스트, 
        y = 수치리스트,
        name = "",
        hoverlabel = dict(
            font = dict(
            family = "Arial",
            size = 13,
        )),
        hovertemplate='%{x}<br>%{y}%\t<br>',
        marker_color = 색상맵
    ))
    
    #quantile 0.25
    fig.add_trace(go.Scatter(
        x = 기업리스트,
        y = [pd.Series(수치리스트).quantile(0.25)] * len(기업리스트),
        name = "Quantile 25%",
        hoverinfo = "none",
        line = dict(color = 수치선색상, dash = "solid", width = 2),
        visible = False,
    ))
    
    #quantile 0.5
    fig.add_trace(go.Scatter(
        x = 기업리스트,
        y = [pd.Series(수치리스트).quantile(0.5)] * len(기업리스트),
        name = "Quantile 50%",
        hoverinfo = "none",
        line = dict(color = 수치선색상, dash = "solid", width = 2),
        visible = False,
    ))

    #quantile 0.75
    fig.add_trace(go.Scatter(
        x = 기업리스트,
        y = [pd.Series(수치리스트).quantile(0.75)] * len(기업리스트),
        name = "Quantile 75%",
        hoverinfo = "none",
        line = dict(color = 수치선색상, dash = "solid", width = 2),
        visible = False
    ))
    
    #mean
    fig.add_trace(go.Scatter(
        x = 기업리스트,
        y = [np.mean(수치리스트)] * len(기업리스트),
        name = "mean",
        hoverinfo = "none",
        line = dict(color = 수치선색상, dash = "solid", width = 2),
        visible = False
    ))
    
    quan_25_annotation = [dict(
                            x = 1,
                            y = pd.Series(수치리스트).quantile(0.25) / max(수치리스트),
                            xref = "paper",
                            yref = "paper",
                            text = "quantile 25%%<br> %.2f" % pd.Series(수치리스트).quantile(0.25),
                            font = dict(color = 수치선색상, size = 13, family = "Arial"),
                            arrowcolor = 수치선색상,
                            ax = 0, ay = -40)]
    
    
    quan_50_annotation = [dict(
                            x = 1,
                            y = pd.Series(수치리스트).quantile(0.5) / max(수치리스트),
                            xref = "paper",
                            yref = "paper",
                            text = "quantile 50%%<br> %.2f" % pd.Series(수치리스트).quantile(0.5),
                            font = dict(color = 수치선색상, size = 13, family = "Arial"), 
                            arrowcolor = 수치선색상,
                            ax = 0, ay = -40)]
    
    quan_75_annotation = [dict(
                            x = 1,
                            y = pd.Series(수치리스트).quantile(0.75) / max(수치리스트),
                            xref = "paper",
                            yref = "paper",
                            text = "quantile 75%%<br> %.2f" % pd.Series(수치리스트).quantile(0.75),
                            font = dict(color = 수치선색상, size = 13, family = "Arial"),
                            arrowcolor = 수치선색상,
                            ax = 0, ay = -40)]
    
    mean_annotation = [dict(
                            x = 1,
                            y = np.mean(수치리스트) / max(수치리스트),
                            xref = "paper",
                            yref = "paper",
                            text = "mean<br> %.2f" % np.mean(수치리스트),
                            font = dict(color = 수치선색상, size = 13, family = "Arial"),
                            arrowcolor = 수치선색상,
                            ax = 0, ay = -40)]
    
    legend_annotations = []
    y_position = 1
    for idx in range(len(범례명리스트)):
        legend_annotations.append(dict(
            text = "<b>" + 범례명리스트[idx] + "</b> " + "<b>■</b>",
            xref="paper", yref="paper",
            x= 1, y = y_position,
            font = dict(
                color =범례색상리스트[idx],
                size = 13,
                family = "Arial"
            ),
            align = "right",
            showarrow = False
        ))
        y_position -= 0.07
    
    fig.update_layout(
        title = dict(
            text = "<b>" + 제목 + "</b>",
            font = dict(
                family = "Arial",
                size = 14,
                color = "Black",
            ),
            x = 0.5,
            y = 0.95,
        ),
        updatemenus = [
            dict(
                type = "buttons",
                direction = "right",
                x = 1,
                y = 1.15,
                buttons = list([
                    dict(
                        label = "None",
                        method = "update",
                        args = [{"visible" : [True, False, False, False, False]},
                                {"annotations" : legend_annotations}]) ,
                    dict(
                        label = "Quantile 25%",
                        method = "update",
                        args = [{"visible" : [True, True, False, False, False]},
                                {"annotations" : legend_annotations + quan_25_annotation}]),
                    
                    dict(
                        label = "Quantile 50%",
                        method = "update",
                        args = [{"visible" : [True, False, True, False, False]},
                                {"annotations" : legend_annotations + quan_50_annotation}]),
                    
                    dict(
                        label = "Quantile 75%",
                        method = "update",
                        args = [{"visible" : [True, False, False, True, False]},
                               {"annotations" : legend_annotations + quan_75_annotation}]),    
                    
                    dict(
                        label = "mean",
                        method = "update",
                        args = [{"visible" : [True, False, False, False, True]},
                               {"annotations" : legend_annotations + mean_annotation}]),       
                ])
            )
        ]
    )
    
    fig.update_layout(
        barmode='relative', 
        showlegend = False,
        paper_bgcolor = "rgba(0,0,0,0)",
        plot_bgcolor = "rgba(0,0,0,0)",
        xaxis = dict(
            tickfont = dict(
                family = "Arial",
                size = 12.5,
                color = "Black")),
        yaxis = dict(
            range = [0, max(수치리스트)],
            title =  y축이름,
            titlefont = dict(color = "Black", family = "Arial", size = 13),
            tickfont = dict(
                family = "Arial",
                size = 12.5,
            color = "Black")),
        margin=dict(pad=10)
    )
    
    y_position = 1
    for idx in range(len(범례명리스트)):
        fig.add_annotation(
            text = "<b>" + 범례명리스트[idx] + "</b> " + "<b>■</b>",
            xref="paper", yref="paper",
            x= 1, y = y_position,
            font = dict(
                color =범례색상리스트[idx],
                size = 13,
                family = "Arial"
            ),
            align = "right",
            showarrow = False
        )
        y_position -= 0.07
    
    return fig

def 막대_년도별(제목, 항목이름리스트, 년도리스트, 수치단위, 강조색상, 일반색상, 추세선색상, **수치리스트):

    r"""각 항목의 수치를 년도별로 비교할 수 있는 막대차트를 시각화합니다. 각 년도 중에서 가장 큰 값을 가지는 막대는 강조 색상으로, 나머지는 일반 색상으로 표시됩니다.
    
    :param 제목(string) : 그래프 상단 타이틀
    :param 항목이름리스트(list) : 각 항목의 이름 리스트
    :param 년도리스트(list) : 년도 리스트
    :param 수치단위:(string) : y축으로 입력되는 수치들의 단위(예) - 원)
    :param 강조색상(string) : 년도별로 가장 큰 값을 가지는 막대에 적용할 색상
    :param 일반색상(string) : 년도별로 가장 큰 값을 가지는 막대를 제외한 막대들에 적용할 색상
    :param 추세선색상(string) : 추세선에 적용할 색상, 추세선을 표시하고 싶지 않은 경우 "rgba(0,0,0,0)" 입력
    :param 수치리스트(list) : 각 항목별 수치리스트 (예) - 유동비율 = [2015년 수치, 2016년 수치, 2017년 수치, 2018년 수치]

    :return (fig)"""


    #Data tuning
    total_max = 0
    for (idx, ratio_name) in enumerate(항목이름리스트):
        max_ratio = max(list(수치리스트.items())[idx][1])
        if (max_ratio > total_max):
            total_max = max_ratio
    
    #Tracing
    fig = make_subplots(rows = 1, cols = len(항목이름리스트))
    
    for (idx, ratio_name) in enumerate(항목이름리스트):
        
        #Get color list
        color_list = []
        max_ratio = max(list(수치리스트.items())[idx][1])
        for amt in list(수치리스트.items())[idx][1]:
            if (amt == max_ratio):
                color_list.append(강조색상)
            else:
                color_list.append(일반색상)
                
        middle_ratios = [ratio * 0.7 for ratio in list(수치리스트.items())[idx][1]]
        
        fig.add_trace(go.Bar(
            x = 년도리스트,
            y = list(수치리스트.items())[idx][1],
            name = "",
            text = list(수치리스트.items())[idx][1],
            ),
            row = 1, col = idx + 1
        )
        
        fig.update_traces(
            hoverinfo = "none",
            texttemplate = '%{text}%',
            textposition = "outside",
            textfont = dict(
                color = "darkgrey",
                family = "Arial",
                size = 12
            ),
            marker_color = color_list,
            row = 1,
            col = idx + 1
        )
        
        fig.add_trace(go.Scatter(
            x = 년도리스트,
            y = middle_ratios,
            hoverinfo = "none",
            line = dict(
                color = 추세선색상,
                width = 3.5
            ),
            marker = dict(size = 7, line = dict(color = 일반색상, width = 1))),
            row = 1, col = idx + 1
        )
        
        fig.update_xaxes(
            title = "<b>" + 항목이름리스트[idx] + "</b>",
            tickfont = dict(
                family = "Arial",
                size = 12.5,
                color = "Black"),
            titlefont = dict(
                color = "Black",
                family = "Arial",
                size = 13),
            row = 1, 
            col = idx + 1
        )
        
        if (idx == 0):
            y_tick_color = "Black"
        else:
            y_tick_color = "rgba(0,0,0,0)"
        
        fig.update_yaxes(
            tickfont = dict(
                family = "Arial",
                size = 13,
                color = y_tick_color
            ),
            title = 수치단위,
            titlefont = dict(
                family = "Arial",
                size = 13,
                color = y_tick_color
            ),
            range = [0, total_max + 10],
            row = 1, col = idx + 1
        )
       
    fig.update_layout(
        title = dict(
            text = "<b>" + 제목 + "</b>",
            font = dict(
                family = "Arial",
                size = 14,
                color = "Black",
            ),
            x = 0.49,
            y = 0.9,
        ),
        paper_bgcolor = "rgba(0,0,0,0)",
        plot_bgcolor = "rgba(0,0,0,0)",
        showlegend = False,
        margin = dict(pad = 15),
        width = 950,
        height = 500
    )

    return fig

def 추세선(제목, 항목이름리스트, 년도리스트, y축이름, 색상맵, **항목별수치리스트):

    r"""년도별, 항목별 수치 추세선을 시각화 합니다.

    :param 제목(string) : 그래프 상단 타이틀
    :param 항목이름리스트(list) : 자산, 유동비율, 매출액, 영업이익, 현금흐름 등  항목 이름 리스트
    :param 년도리스트(list) :년도 리스트
    :param y축이름(string) : 단위를 포함한 y축의 이름 (예) - "금액(원)", "비율(%)")
    :param 색상맵(list) : 항목별로 적용될 색상리스트
    :param 항목별수치리스트(list) : 각 항목의 년도별 수치리스트 (예) - 매출액 = [2015년 수치, 2016년 수치, 2017냔 수치, 2018년 수치])
    
    :return (fig)"""
    
    #Get color list
    color_list = []
    if (len(항목이름리스트) <= len(색상맵)):
        for idx in range(len(항목이름리스트)):
            color_list.append(색상맵[idx])
        color_list[-1] = px.colors.sequential.Greys[2]
    else:
        color_list += 색상맵
        grays = []
        for idx in range(len(년도리스트) - len(색상맵)):
            grays.append(px.colors.sequential.Greys[idx + 3])
        grays.reverse()
        color_list += grays
    
    #Tracing
    fig = go.Figure()
    for (idx, (name, val_list)) in enumerate(항목별수치리스트.items()):
        fig.add_trace(go.Scatter(
            name = name,
            x = 년도리스트,
            y = val_list,
            mode = "lines+markers",
            marker = dict(size = 6),
            line = dict(
                color = color_list[idx],
                width = 3,
            ),
            hovertemplate = y축이름 + " %{y}",
            hoverlabel = dict(
                font = dict(
                    family = "Arial",
                    size = 13
                ),
            ),
        ))
        
        fig.update_xaxes(showspikes=True, spikecolor = "Black", spikesnap="cursor", spikemode="across", spikedash = "dot", spikethickness = 0.7)
        fig.update_yaxes(showspikes=True, spikecolor="Black", spikethickness = 0.7, spikedash = "dot")
        fig.update_layout(spikedistance=1000, hoverdistance=100)
        
        fig.update_layout(
            title = dict(
                text = "<b>" + 제목 + "</b>",
                font = dict(
                    family = "Arial",
                    size = 14,
                    color = "Black",
                ),
                x = 0.48,
                y = 0.9,
            ),
            width = 900,
            height = 500,
            showlegend = True,
            paper_bgcolor = "rgba(0,0,0,0)",
            plot_bgcolor = "rgba(0,0,0,0)",
            xaxis = dict(
                title = "년도(년)",
                titlefont = dict(
                    family = "Arial",
                    size = 13,
                    color = "Black"),            
                type = "category",
                tickfont = dict(
                    family = "Arial",
                    size = 13,
                    color = "Black")),
            yaxis = dict(
                title = y축이름,
                titlefont = dict(
                    family = "Arial",
                    size = 13,
                    color = "Black"),
                tickfont = dict(
                    family = "Arial",
                    size = 13,
                    color = "Black")),
            margin = dict(
                pad = 10)
        )
    
    return fig

def 증감률(제목, 항목이름리스트, 년도리스트, y축이름, y축단위, 색상맵, **항목별수치리스트):

    r"""각 항목의 년도별 증감액을 자동으로 계산하여 전년도 대비 증감액을 시각화합니다. 

    :param 제목(string) : 그래프 상단 타이틀
    :param 항목이름리스트(list) : 자산, 유동비율, 매출액, 영업이익, 현금흐름 등  항목 이름 리스트
    :param 년도리스트(list) : 년도 리스트
    :param y축이름(string) : 단위를 포함한 y축의 이름 (예) - "금액(원)", "비율(%)")
    :param 색상맵(list) : 항목별로 적용될 색상리스트
    :param 항목별수치리스트(list) : 각 항목의 년도별 수치리스트 (예) - 매출액 = [2015년 수치, 2016년 수치, 2017냔 수치, 2018년 수치])

     :return (fig)"""
    
    #Data tuning
    total_values = []
    for (idx, (name, val_list)) in enumerate(항목별수치리스트.items()):    
        total_values += val_list
    
    total_min = min(total_values)
    total_max = max(total_values)
    
    #Get color list
    color_list = []
    if (len(년도리스트) <= len(색상맵)):
        for idx in range(len(년도리스트)):
            color_list.append(색상맵[idx])
        color_list[-1] = px.colors.sequential.Greys[2]
    else:
        color_list += 색상맵
        grays = []
        for idx in range(len(년도리스트) - len(색상맵)):
            grays.append(px.colors.sequential.Greys[idx + 3])
        grays.reverse()
        color_list += grays
        
    
    #Tracing
    fig = make_subplots(cols = len(항목이름리스트), rows = 1, shared_yaxes = True, )

    for (idx, (name, val_list)) in enumerate(항목별수치리스트.items()):
        change_list = []
        for val_idx in range(len(val_list) - 1):
            change_list.append(val_list[val_idx + 1] - val_list[val_idx])
        
        fig.add_trace(go.Bar(
            base = 0,
            name = name,
            x = 년도리스트,
            y = change_list,
            hovertemplate = "지난년도 대비 " + "%{y}(원)" + " 증감",
            hoverlabel = dict(
                font = dict(
                    family = "Arial",
                    size = 13
                ),
            ),
            marker = dict(color = color_list[idx])),
            col = idx + 1, row = 1)
        
        fig.update_xaxes(
            zeroline = True,
            type = "category",
            tickfont = dict(
                family = "Arial",
                size = 13,
                color = "Black"),
            col = idx + 1, 
            row = 1
        )
        
        if (idx == 0):
            y_tick_color = "Black"
        else:
            y_tick_color = "rgba(0,0,0,0)"
        
        fig.update_yaxes(
            zeroline = True,
            zerolinecolor = color_list[idx],
            zerolinewidth = 2,
            tickfont = dict(
                family = "Arial",
                size = 13,
                color = y_tick_color
            ),
            title = y축이름 + y축단위,
            titlefont = dict(
                family = "Arial",
                size = 13,
                color = y_tick_color
            ),
            row = 1, col = idx + 1
        )   
        
    fig.update_layout(
        title = dict(
            text = "<b>" + 제목 + "</b>",
            font = dict(
                family = "Arial",
                size = 14,
                color = "Black",
            ),
            x = 0.48,
            y = 0.9,
        ),
        width = 900,
        height = 500,
        showlegend = True,
        paper_bgcolor = "rgba(0,0,0,0)",
        plot_bgcolor = "rgba(0,0,0,0)",
        xaxis = dict(
            type = "category",
            tickfont = dict(
                family = "Arial",
                size = 13,
                color = "Black")),
        yaxis = dict(
            title = y축이름 + y축단위,
            titlefont = dict(
                family = "Arial",
                size = 13,
                color = "Black"),
            tickfont = dict(
                family = "Arial",
                size = 13,
                color = "Black")),
        margin = dict(pad = 20),
        legend = dict(
            font = dict(
                color = "Black",
                family = "Arial",
                size = 13,
            ),
        )
    )
    
    fig.add_annotation(
        text = "년도(년)",
        xref="paper", yref="paper",
        x= 0.5, y = -0.22,
        font = dict(
            color = "Black",
            size = 13,
            family = "Arial"
        ),
        align = "center",
        showarrow = False
    )
        
    return fig

def 스택(제목, 매출원가리스트, 판매비와관리비리스트, 영업이익리스트, 년도리스트, 색상맵):

    r"""년도별 매출액 대비 매출원가, 판매비와관리비, 영업이익의 구성비율을 그래프 면적을 통해 시각화 합니다.  

    :param 제목(string) : 그래프 상단 타이틀
    :param 매출원가리스트(list) : 년도별 매출원가의 리스트
    :param 판매비와관리비리스트(list) : 년도별 판매비와관리비리스트
    :param 영업이익리스트(list) : 	년도별 영업이익리스트
    :param 년도리스트(list) : 년도리스트
    :param 색상맵(list) : 매출원가, 판매비와관리비, 영업이익 항목에 적용할 색상리스트

    :return (fig)"""

    #Data tuning
    name_list = ["매출원가", "판매비와관리비", "영업이익"]
    판매비와관리비_tuning = []
    영업이익_tuning = []
    for idx in range(len(년도리스트)):
        판매비와관리비_tuning.append(매출원가리스트[idx] + 판매비와관리비리스트[idx])
        영업이익_tuning.append(매출원가리스트[idx] + 판매비와관리비리스트[idx] + 영업이익리스트[idx])
               
    val_list = [매출원가리스트, 판매비와관리비_tuning, 영업이익_tuning]
    fill_list = ["tozeroy", "tonexty", "tonexty"]
    
    #Tracing
    fig = go.Figure()
    
    for idx in range(len(name_list)):
        fig.add_trace(go.Scatter(
            name = name_list[idx],
            x = 년도리스트,
            y = val_list[idx],
            mode = "lines",
            fill = fill_list[idx],
            line = dict(
                color = 색상맵[idx],
                width = 3
            ),
            fillcolor = 색상맵[idx],
            marker = dict(
               color = 색상맵[idx]
            ),
            hovertemplate = "%{y}원",
            hoverlabel = dict(
                font = dict(
                    family = "Arial",
                    size = 13
                ),
            ))
        )
        
        fig.update_xaxes(showspikes=True, spikecolor = "Black", spikesnap="cursor", spikemode="across", spikedash = "dot", spikethickness = 1.4)
        fig.update_yaxes(showspikes=True, spikecolor="Black", spikethickness = 1.4, spikedash = "dot")
        fig.update_layout(spikedistance=1000, hoverdistance=100)
        
        fig.update_layout(
            title = dict(
                text = "<b>" + 제목 + "</b>",
                font = dict(
                    family = "Arial",
                    size = 14,
                    color = "Black",
                ),
                x = 0.47,
                y = 0.9,
            ),
            width = 900,
            height = 500,
            showlegend = True,
            paper_bgcolor = "rgba(0,0,0,0)",
            hovermode = "x",
            plot_bgcolor = "rgba(0,0,0,0)",
            xaxis = dict(
                type = "category",
                title= "년도(년)",
                titlefont = dict(
                    family = "Arial",
                    size = 13,
                    color = "Black"),
                tickfont = dict(
                    family = "Arial",
                    size = 13,
                    color = "Black")),
            yaxis = dict(
                title= "금액(원)",
                titlefont = dict(
                    family = "Arial",
                    size = 13,
                    color = "Black"),
                tickfont = dict(
                    family = "Arial",
                    size = 13,
                    color = "darkgrey")),
            margin = dict(
                pad = 20)
        )
    
    return fig

def 막대_애니메이션(제목, 년도리스트, x축이름, x축리스트, y축이름, y축리스트, 색상맵):

    r"""x축과 y축 데이터를 년도별로 프레임화 하여 애니메이션 형태로 시각화 합니다.

    :param 제목(string) : 그래프 상단 타이틀
    :param 년도리스트(list) : 년도리스트
    :param x축이름(string) : x축에 표시될 라벨
    :param x축리스트(list) : x축의 데이터 리스트
    :param y축이름(string) : y축에 표시될 라벨
    :param y축리스트(list) : y축의 데이터 리스트
    :param 색상맵(list) : x축의 값에 따라 적용될 색상 리스트

    :return: (fig)"""
    
    #Data tuning
    df = pd.DataFrame(columns = [x축이름, "년도", y축이름])
    df[x축이름]  = x축리스트
    df["년도"] = 년도리스트
    df[y축이름] = y축리스트
    y_max = max(y축리스트)
    
    #DataTracing
    fig = px.bar(df, x = x축이름, y = y축이름, animation_frame = "년도", color = x축이름, color_discrete_sequence = 색상맵)
    fig.update_layout(
       title = dict(
            text = "<b>" + 제목 + "</b>",
            font = dict(
                family = "Arial",
                size = 14,
                color = "Black",
            ),
            x = 0.47,
            y = 0.95,
        ),
        width = 900,
        height = 500,
        showlegend = True,
        paper_bgcolor = "rgba(0,0,0,0)",
        plot_bgcolor = "rgba(0,0,0,0)",
        xaxis = dict(
            type = "category",
            title= x축이름,
            titlefont = dict(
                family = "Arial",
                size = 13,
                color = "Black"),
            tickfont = dict(
                family = "Arial",
                size = 13,
                color = "Black")),
        yaxis = dict(
            gridcolor = "lightgrey",
            gridwidth = 1,
            title = y축이름,
            titlefont = dict(
                family = "Arial",
                size = 13,
                color = "Black"),
            tickfont = dict(
                family = "Arial",
                size = 13,
                color = "darkgrey"),
            range = [0, y_max]),
        margin = dict(
        	pad = 20, t = 80,
        ),
    ),
    
    return fig

def 기업부실예측(
    제목,
    기업리스트, 
    유동자산리스트, 비유동자산리스트, 자산총계리스트,
    유동부채리스트, 비유동부채리스트, 부채총계리스트,
    자본금리스트, 이익잉여금리스트, 자본총계리스트, 
    영업이익리스트, 
    매출액리스트,
    부실가능성낮음_색상, 판단보류_색상, 부실가능성높음_색상
):

    r"""기업의 계정별 데이터를 입력받아 자동으로 Altman Score를 계산하고 부실 기업 예측 결과를 시각화 합니다.

    :param 제목(string) : 그래프 상단 타이틀
    :param 기업리스트(list) : 기업명 리스트
    :param 유동자산리스트(list) : 기업별 유동자산 리스트
    :param 비유동자산리스트(list) : 기업별 비유동자산리스트
    :param 자산총계리스트(list) : 기업별 자산총계리스트
    :param 유동부채리스트(list) : 기업별 유동부채리스트
    :param 비유동부채리스트(list) : 기업별 비유동부채리스트
    :param 부채총계리스트(list) : 기업별 부채총계리스트
    :param 자본금리스트(list) : 기업별 자본금리스트
    :param 이익잉여금리스트(list) : 기업별 이익잉여금리스트
    :param 자본총계리스트(list) : 기업별 자본총계리스트
    :param 당기순이익리스트(list) :기업별 당기순이익리스트
    :param 매출액리스트(list) : 기업별 매출액리스트
    :param 부실가능성낮음_색상(string) : 부실가능성이 낮은 기업에 적용될 색상
    :param 판단보류_색상(string) : 판단보류 대상 기업에 적용될 색상
    :param 부실가능성높음_색상(string) : 부실가능성이 높은 기업에 적용될 색상

    :return: (fig)"""
    
    #Calculating Altman_Z_SCORE
    x1, x2, x3, x4, x5 = [], [], [], [], []
    for idx in range(len(기업리스트)):
        x1.append((유동자산리스트[idx] - 유동부채리스트[idx]) / 자산총계리스트[idx])
        x2.append(이익잉여금리스트[idx] / 자산총계리스트[idx])
        x3.append(영업이익리스트[idx] / 자산총계리스트[idx])
        x4.append(자본총계리스트[idx] / 부채총계리스트[idx])
        x5.append(매출액리스트[idx] / 자산총계리스트[idx])
        
    Altman_ZSCORE = []        
    for idx in range(len(x1)):
        Altman_ZSCORE.append(1.2 * x1[idx] + 1.4 * x2[idx] + 3.3 * x3[idx] + 0.6 * x4[idx] + 0.999 * x5[idx])

    Altman_ZSCORE_판정결과 = []
    for zscore in Altman_ZSCORE:
        if (zscore > 2.99):
            Altman_ZSCORE_판정결과.append("부도 가능성 낮음")
        elif (zscore > 1.81):
            Altman_ZSCORE_판정결과.append("판단 보류")
        else:
            Altman_ZSCORE_판정결과.append("부도 가능성 높음")

    x1, x2, x3, x4 = [], [], [], []
    for idx in range(len(기업리스트)):
        x1.append(np.log(자산총계리스트[idx]))
        x2.append(np.log(매출액리스트[idx] / 자산총계리스트[idx]))
        x3.append(이익잉여금리스트[idx] / 자산총계리스트[idx])
        x4.append(자본총계리스트[idx] / 부채총계리스트[idx])
        
    Altman_z_color_list = []
    for result in Altman_ZSCORE_판정결과:
        if (result == "부도 가능성 낮음"):
            Altman_z_color_list.append(부실가능성낮음_색상)
        elif (result == "판단 보류"):
            Altman_z_color_list.append(판단보류_색상)
        else:
            Altman_z_color_list.append(부실가능성높음_색상)
            
    #Calculating Altman_K2_SCORE
    Altman_K2SCORE = []
    for idx in range(len(x1)):
        Altman_K2SCORE.append(-17.682 + 1.472 * x1[idx] + 3.041 * x2[idx] + 14.839 * x3[idx] + 1.516 * x4[idx])
    
    Altman_K2SCORE_판정결과 = []
    for k2score in Altman_K2SCORE:
        if (0.75 < k2score):
            Altman_K2SCORE_판정결과.append("부실 가능성 없음")
        elif (-2 < k2score):
            Altman_K2SCORE_판정결과.append("판단 유보")
        else:
            Altman_K2SCORE_판정결과.append("부도 가능성 심각")
 
    Altman_k2_color_list = []
    for result in Altman_K2SCORE_판정결과:
        if (result == "부실 가능성 없음"):
            Altman_k2_color_list.append(부실가능성낮음_색상)
        elif (result == "판단 유보"):
            Altman_k2_color_list.append(판단보류_색상)
        else:
            Altman_k2_color_list.append(부실가능성높음_색상)
            
    #Sorting 
    merged1 = []
    for idx in range(len(기업리스트)):
        merged1.append((기업리스트[idx], Altman_ZSCORE[idx], Altman_z_color_list[idx]))
    
    merged2 = []
    for idx in range(len(기업리스트)):
        merged2.append((기업리스트[idx], Altman_K2SCORE[idx], Altman_k2_color_list[idx]))
        
    merged1 = sorted(merged1, key = lambda tup: tup[1], reverse = True)
    merged2 = sorted(merged2, key = lambda tup: tup[1], reverse = True)
    name_list = ["Altman Z-Score", "Altman K2-Score"]
    
    #Tracing
    fig = go.Figure()
    
    for (idx, merged_list) in enumerate([merged1, merged2]):
        기업리스트 = [corp for (corp, value, color) in merged_list]
        수치리스트 = [value for (corp, value, color) in merged_list]
        색상맵 = [color for (corp, value, color) in merged_list]
        
        if (idx == 1):
            visible = False;
        else:
            visible = True;
        
        fig.add_trace(go.Bar(
            base = 0,
            x = 기업리스트,
            y = 수치리스트,
            name = name_list[idx],
            hoverlabel = dict(
                font = dict(
                family = "Arial",
                size = 13,
            )),
            visible = visible,
            hovertemplate="%{x}<br>%{y}\t<br>",
            marker_color = 색상맵           
        ))
        
        fig.update_layout(
            width = 900,
            height = 600,
            barmode='relative', 
            showlegend = False,
            plot_bgcolor = "rgba(0,0,0,0)",
            margin = dict(pad = 3, t = 150),
            xaxis = dict(
                color = "Black",
                tickfont = dict(
                    family = "Arial",
                    size = 12,
                    color = "Black")),
            yaxis = dict(
                zeroline = True,
                zerolinecolor = "Black",
                zerolinewidth = 2,
                gridcolor = "lightgray",
                gridwidth = 1,
                title =  "수치",
                titlefont = dict(color = "Black", family = "Arial", size = 13),
                ticksuffix = "  ",
                tickfont = dict(
                family = "Arial",
                size = 13,
                color = "Black"))
        ),
        
    fig.update_layout(
        title = dict(
            text = "<b>" + 제목 + "</b>",
            font = dict(
                family = "Arial",
                size = 14,
                color = "Black",
            ),
            x = 0.5,
            y = 0.9,
        ),
        updatemenus = [
            dict(
                type = "buttons",
                direction = "right",
                x = 0.3,
                y = 1.2,
                buttons = list([
                    dict(
                        label = "Altman Z-Score",
                        method = "update",
                        args = [{"visible" : [True, False]}]) ,
                    dict(
                        label = "Altman K2-Score",
                        method = "update",
                        args = [{"visible" : [False, True]}]),
                   ])
            )
    ])
    
    #legend annotation
    legend_color_list = [부실가능성낮음_색상, 판단보류_색상, 부실가능성높음_색상]
    legend_list = ["부실 가능성 낮음", "판단 보류", "부실 가능성 높음"]
    x_increase = [0.1, 0.15, 0.1]
    
    x_position = 0.75
    for idx in range(len(legend_list)):
        fig.add_annotation(
            text = legend_list[idx] + "<b>■</b>",
            xref="paper", yref="paper",
            x = x_position, y = + 1.1,
            font = dict(
                color = legend_color_list[idx],
                size = 12.5,
                family = "Arial"
            ),
            align = "right",
            showarrow = False
        )
        x_position += x_increase[idx]
        
    return fig    
