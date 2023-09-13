import requests
import json
import pandas as pd


def download_stock_info():
    """_summary_
    종목의 기본정보를 다운로드하는 함수 -> download_trade_volume의 변수인 ticker 정보를 얻기 위해 사용

    Returns:
        _type_: _description_
    """
    # url 설정
    url = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd"
    # 요청에 필요한 data 설정
    data = {
        "bld": "dbms/MDC/STAT/standard/MDCSTAT01901",
        "locale": "ko_KR",
        "mktId": "ALL",
        "share": "1",
        "csvxls_isNo": "false",
    }
    # post 요청
    response = requests.post(url, data=data)
    stock_info = response.json()["OutBlock_1"]

    return pd.DataFrame(stock_info)


def download_trade_volume(short_code: str, start_date: str, end_date: str) -> json:
    """_summary_
    Args:
        short_code(str): 검색할 주식 티커 # 종목명 사용 못하는 이유: 영어로 표기된 종목들 존재 ex) NAVER, KT&G
        start_date(str): 수급정보 시작일
        end_date(str): 수급정보 종료일

    Returns:
        json: list of dictionaries형태의 수급정보 데이터를 JSON으로 반환
        dictionaries의 key값 설명:
            INVST_TP_NM	: 투자자구분 ex) 연기금, 개인, 외국인 등
            ASK_TRDVOL: 매도거래량
            BID_TRDVOL: 매수거래량
            NETBID_TRDVOL: 순매수거래량
            ASK_TRDVAL: 매도거래량의 거래대금
            BID_TRDVAL: 매수거래량의 거래대금
            NETBID_TRDVAL: 순매수거래량의 거래대금
    """
    # 주식 티커 등 정보를 담고 있는 csv 파일을 load
    stock_info = download_stock_info()
    full_code = stock_info[stock_info["ISU_SRT_CD"] == short_code]["ISU_CD"]
    # url 설정
    url = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd"
    # 요청에 필요한 data 설정
    data = {
        "bld": "dbms/MDC/STAT/standard/MDCSTAT02301",
        "locale": "ko_KR",
        "inqTpCd": "1",
        "trdVolVal": "2",
        "askBid": "3",
        "tboxisuCd_finder_stkisu0_3": short_code,
        "isuCd": full_code,
        "isuCd2": full_code,
        "codeNmisuCd_finder_stkisu0_3": short_code,
        "param1isuCd_finder_stkisu0_3": "ALL",
        "strtDd": start_date,
        "endDd": end_date,
        "share": "1",
        "money": "1",
        "csvxls_isNo": "false",
    }
    # post 요청
    response = requests.post(url, data=data)
    trade_info = response.json()["output"]
    # 불필요 key 제거
    _list = []
    for dict in trade_info:
        del dict["CONV_OBJ_TP_CD"]
        _list.append(dict)
    return json.dumps(trade_info, ensure_ascii=False)


if __name__ == "__main__":
    # stock_info = download_stock_info()
    # stock_info.to_csv('../database/stock_info.csv', index=False)
    print(download_trade_volume("005930", "20230601", "20230711"))
