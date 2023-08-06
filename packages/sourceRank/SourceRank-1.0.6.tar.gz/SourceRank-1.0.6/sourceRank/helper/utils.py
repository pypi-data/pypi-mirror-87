import pycountry
import numpy as np
import hashlib
import more_itertools as mit
from datetime import datetime
from sourceRank.helper.settings import logger, default_field
from restcountries import RestCountryApiV2 as rapi
from tldextract import TLDExtract
from tldextract.tldextract import ExtractResult
from fuzzywuzzy import fuzz, process
from scipy import stats
from dateutil.parser import parse


def parse_url(url: str) -> ExtractResult:
    tld_res: ExtractResult = ExtractResult(
        domain="", subdomain="", suffix="")
    try:
        tld_extract_obj: TLDExtract = TLDExtract(
            include_psl_private_domains=True)
        tld_res: ExtractResult = tld_extract_obj(
            url=url, include_psl_private_domains=True)

    except Exception as e:
        logger.error(e)
    return tld_res


def get_country_name_by_code(country_code: str) -> str:
    country_name: str = default_field
    try:
        res_country_api: dict = pycountry.countries.get(
            alpha_2=country_code.upper()).__dict__
        country_name: str = res_country_api.get("_fields", {}).get("name")
    except Exception as e:
        logger.warning(e)
    return country_name


def get_country_code_by_name(country_name: str) -> str:
    country_code: str = default_field
    try:
        countries_matching: list = pycountry.countries.search_fuzzy(
            country_name)
        country_code: str = countries_matching[0].alpha_2
    except Exception as e:
        logger.error(e)
    return country_code


def get_nationality_from_country_code(country_code: str) -> str:
    nationality: str = default_field
    try:
        country_name: str = get_country_name_by_code(
            country_code=country_code)
        country_list: list = rapi.get_countries_by_name(country_name)
        if country_list:
            nationality: str = country_list[0].demonym
    except Exception as e:
        logger.error(e)
    return nationality


def compute_importance_from_exponential_distribution(x, alpha: int = 0.6) -> float:
    importance: float = 0.0
    try:
        importance: float = stats.expon.cdf(x, scale=1/alpha)
    except Exception as e:
        logger.error(e)
    return importance


def get_datetime_from_str(str_datetime: str, target_format: str = '%Y-%m-%d %H:%M:%S') -> datetime:

    origin_datetime_obj: datetime = parse(str_datetime)
    target_datetime_obj: datetime = datetime.strptime(
        origin_datetime_obj.strftime(target_format), target_format)

    return target_datetime_obj


def get_str_datetime_from_non_formatted_str(str_datetime: str,
                                            target_format: str = '%Y-%m-%d %H:%M:%S') -> str:
    target_datetime_obj: str = "1996-01-01 00:00:00"
    try:
        if len(str_datetime) > 1:
            origin_datetime_obj: datetime = parse(str_datetime)
        else:
            # default date
            origin_datetime_obj: datetime = datetime.now()

        target_datetime_obj: str = origin_datetime_obj.strftime(target_format)
    except Exception as e:
        pass

    return target_datetime_obj


def get_fuzzy_matching_set_ratio(input_query: str, matching_item: str) -> float:
    matching_score: float = 0.0
    try:
        matching_score: float = fuzz.token_set_ratio(input_query, matching_item)

    except Exception as e:
        logger.error(e)
    return matching_score


def get_fuzzy_matching_sort_ratio(input_query: str, matching_item: str) -> float:
    matching_score: float = 0.0
    try:
        matching_score: float = fuzz.token_sort_ratio(input_query, matching_item)
    except Exception as e:
        logger.error(e)
    return matching_score


def get_fuzzy_matching_partial_token_set_ratio(input_query: str, matching_item: str) -> float:
    matching_score: float = 0.0
    try:
        matching_score: float = fuzz.partial_token_set_ratio(input_query, matching_item)
    except Exception as e:
        logger.error(e)
    return matching_score


def get_fuzzy_matching_partial_token_sort_ratio(input_query: str, matching_item: str) -> float:
    matching_score: float = 0.0
    try:
        matching_score: float = fuzz.partial_token_sort_ratio(input_query, matching_item)
    except Exception as e:
        logger.error(e)
    return matching_score


def get_fuzzy_matching_partial_ratio(input_query: str, matching_item: str) -> float:
    matching_score: float = 0.0
    try:
        matching_score: float = fuzz.partial_ratio(input_query, matching_item)
    except Exception as e:
        logger.error(e)
    return matching_score


def get_best_matching_candidate_from_list(candidate: str, matching_options: list) -> tuple:
    res_matching: tuple = ()
    try:
        # 1. Get matching scores
        res_matching: tuple = process.extractOne(
            query=candidate, choices=matching_options)

    except Exception as e:
        logger.error(e)
    return res_matching


def preprocess_date(non_formatted_date: datetime,
                    new_format: str = '%Y/%m/%d %H:%M:%S') -> str:
    return non_formatted_date.strftime(new_format)


def get_average_tweets_per_day(statuses_count: int, created_at: datetime) -> float:
    average_tweets_per_day: float = 0.0
    try:
        account_age_days = get_account_age_in_days(created_at=created_at)
        average_tweets_per_day: float = float(np.round(statuses_count / account_age_days, 3))
    except Exception as e:
        logger.error(e)
    return average_tweets_per_day


def get_datetime_from_date(non_formatted_date: datetime,
                           new_format: str = '%Y/%m/%d %H:%M:%S') -> datetime:
    date_time_str: str = preprocess_date(
        non_formatted_date=non_formatted_date,
        new_format=new_format)
    date_time_obj: datetime = datetime.strptime(
        date_time_str, '%Y/%m/%d %H:%M:%S')
    return date_time_obj


def get_account_age_in_days(created_at: datetime)-> int:
    delta = datetime.utcnow() - created_at
    return delta.days


def generate_128_uuid_from_string(data_uuid: str) -> str:
    identifier: str = ""
    try:
        identifier: str = hashlib.sha512(data_uuid.lower().encode('utf-8')).hexdigest()
    except Exception as e:
        print(e)
    return identifier


def int_to_str_list(data_ls: list):
    return [str(element) for element in data_ls]


def chunks_from_list(data_ls: list, n: int):
    """Yield successive n-sized chunks from lst."""
    split_lst: list = [list(el) for el in mit.divide(n, data_ls)]
    return split_lst


def parameterized_ReLU(x, alpha=0.01) -> float:
    y: float = 0.0
    try:
        if x < 0:
            y: float = alpha*x
        else:
            y: float = x
    except Exception as e:
        logger.error(e)
    return y


def relevance_mapping(x: float, alpha: float = .20) -> float:
    return 1 - (1/(1 + alpha * x))