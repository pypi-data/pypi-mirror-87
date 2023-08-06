import requests
from requests import Response
from tldextract.tldextract import ExtractResult
from tweepy.models import User
from botometer import Botometer
from sourceRank.models.source_credibility_models import (SuffixRankDoc, OpenRankDoc,
                                                         CategoryAnalysisDoc, NewsAPISourceDoc,
                                                         WhoisAnalysisDoc, TwitterRankAnalysisDoc,
                                                         TwitterCredibilityDoc)
from sourceRank.helper.country_domain_list import top_level_country_domains
from sourceRank.helper.settings import logger, default_field
from sourceRank.helper.utils import compute_importance_from_exponential_distribution, relevance_mapping, parse_url
from sourceRank.connectors.news_api_connector import NewsAPIConnector
from sourceRank.connectors.twitter_api_connector import TwitterConnector


class SourceCredibilityAnalysis(object):
    def __init__(self, open_rank_api_key: str, whois_api_key: str, news_api_key: str,
                 consumer_key: str, consumer_secret: str, access_token: str,
                 access_token_secret: str, botometer_api_key: str):
        self.open_rank_api_key: str = open_rank_api_key
        self.whois_api_key: str = whois_api_key
        self.news_api_key: str = news_api_key
        self.news_api_connector: NewsAPIConnector = NewsAPIConnector(
            api_key=self.news_api_key)
        self.botometer_api_key: str = botometer_api_key
        self.botometer_api: Botometer = self.set_up_botometer(
            consumer_key=consumer_key, consumer_secret=consumer_secret,
            access_token=access_token, access_token_secret=access_token_secret)
        self.twitter_connector: TwitterConnector = TwitterConnector(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_token_secret)

    @staticmethod
    def parse_url(url: str) -> ExtractResult:
        return parse_url(url=url)

    def get_open_page_rank(self, domain: str) -> Response:
        response: Response = Response()
        try:
            headers: dict = {"API-OPR": self.open_rank_api_key}
            url: str = "https://openpagerank.com/api/v1.0/getPageRank"
            params: dict = {"domains[]": domain}
            response: Response = requests.get(
                url=url, params=params,
                headers=headers)
        except Exception as e:
            logger.error(e)
        return response

    def get_whois_data_from_domain(self, domain: str) -> Response:
        response: Response = Response()
        try:
            url: str = "https://www.whoisxmlapi.com/whoisserver/WhoisService"
            params: dict = {"apiKey": self.whois_api_key,
                            "domainName": domain,
                            "outputFormat": "JSON"}
            response = requests.get(
                url=url, params=params)
        except Exception as e:
            logger.error(e)
        return response

    @staticmethod
    def get_whois_rank(whois_data) -> float:
        rank: float = 0.0
        try:
            # 1. Relevance age
            relevance_by_age: float = relevance_mapping(
                x=whois_data.get("estimatedDomainAge"))

            # 2. Registered domain
            if whois_data.get("domainName") != default_field:
                x_domain: float = 100
            else:
                x_domain: float = 1

            relevance_by_domain: float = relevance_mapping(
                    x=x_domain)

            # 3. Registered country
            if whois_data.get("registryData").get("registrant").get("country") != default_field:
                x_country: float = 100
            else:
                x_country: float = 1

            relevance_by_country: float = relevance_mapping(
                x=x_country)

            total_relevance: float = float((relevance_by_age + relevance_by_country + relevance_by_domain) / 3)
            rank: float = round(total_relevance, 3)

        except Exception as e:
            logger.error(e)
        return rank

    def get_whois_analysis(self, domain: str) -> WhoisAnalysisDoc:
        whois_analysis: WhoisAnalysisDoc = object.__new__(WhoisAnalysisDoc)
        try:
            response_whois: Response = self.get_whois_data_from_domain(
                domain=domain)

            # If the result is fine
            if response_whois.status_code == 200:
                whois_data: dict = response_whois.json().get("WhoisRecord", {})
                rank: float = self.get_whois_rank(whois_data=whois_data)
                whois_analysis: WhoisAnalysisDoc = WhoisAnalysisDoc(
                    whois_data=whois_data, analysed=True, rank=rank)

        except Exception as e:
            logger.error(e)
        return whois_analysis

    def get_open_rank_analysis(self, domain: str) -> OpenRankDoc:
        open_rank_analysis: OpenRankDoc = OpenRankDoc(
            domain=domain, page_rank_decimal=-1, rank=-1, last_updated="",
            analysed=False)
        try:
            response_open_rank: Response = self.get_open_page_rank(domain=domain)
            if response_open_rank.status_code == 200:
                response_open_rank_dict = response_open_rank.json()
                result_dict: dict = response_open_rank_dict.get("response")[0]

                open_rank_analysis: OpenRankDoc = OpenRankDoc(
                    domain= result_dict.get("domain", domain),
                    page_rank_decimal=result_dict.get(
                        "page_rank_decimal", -1),
                    rank=float(result_dict.get(
                        "rank", -1)),
                    last_updated=response_open_rank_dict.get(
                        "last_updated", ""),
                    analysed=True)

        except Exception as e:
            logger.error(e)
        return open_rank_analysis

    @staticmethod
    def get_suffix_mapping() -> dict:
        suffix_mapping: dict = {"edu": 5, "gov": 5, "org": 3,
                                "mil": 3, "net": 2, "com": 2}

        # Retrieve country domain
        country_domains: dict = dict(zip(
            top_level_country_domains.keys(),
            [4 for i in range(len(top_level_country_domains.keys()))]))

        # Update mapping with country domain
        suffix_mapping.update(country_domains)
        return suffix_mapping

    def get_suffix_analysis(self, suffix: str) -> SuffixRankDoc:
        suffix_analysis: SuffixRankDoc = object.__new__(SuffixRankDoc)
        try:
            suffix_mapping: dict = self.get_suffix_mapping()
            importance: float = suffix_mapping.get(suffix, 1)
            rank: float = round(compute_importance_from_exponential_distribution(
                x=importance), 1)
            suffix_analysis: SuffixRankDoc = SuffixRankDoc(
                suffix=suffix, importance=importance, rank=rank, analysed=True)
        except Exception as e:
            logger.error(e)
        return suffix_analysis

    @staticmethod
    def get_category_mapping() -> dict:
        category_mapping: dict = {'science': 5,
                                  'technology': 4,
                                  'entertainment': 3,
                                  'sports': 3,
                                  'health': 4,
                                  'general': 4,
                                  'business': 4}
        return category_mapping

    def get_category_analysis(self, url: str, category: str = None,
                              country_code: str = None, language: str = None) -> CategoryAnalysisDoc:
        category_analysis: CategoryAnalysisDoc = object.__new__(CategoryAnalysisDoc)
        try:
            candidate: NewsAPISourceDoc = self.news_api_connector.get_source_matching_from_url(
                candidate_source=url,
                category=category,
                country_code=country_code,
                language=language)

            category_mapping: dict = self.get_category_mapping()
            importance: float = category_mapping.get(candidate.category, 1)
            rank: float = round(compute_importance_from_exponential_distribution(
                x=importance), 1)

            # Create output object
            category_analysis: CategoryAnalysisDoc = CategoryAnalysisDoc(
                id=candidate.id,
                name=candidate.name,
                description=candidate.description,
                url=candidate.url,
                category=candidate.category,
                language=candidate.language,
                country_code=candidate.country,
                importance=importance,
                rank=rank,
                analysed=candidate.analysed)
        except Exception as e:
            logger.error(e)
        return category_analysis

    def get_twitter_rank(self, url: str) -> TwitterRankAnalysisDoc:
        twitter_rank_analysis: CategoryAnalysisDoc = object.__new__(CategoryAnalysisDoc)

        try:
            # 1. Start connection
            if self.twitter_connector.api is None:
                self.twitter_connector.set_up_twitter_api_connection()

            # 2. Extract Twitter account
            user_data: User = self.twitter_connector.extract_twitter_account_by_searching(
                api=self.twitter_connector.api, keyword=url)
            response_twitter_credibility: dict = self.twitter_connector.get_credibility_rank_from_user_account(
                user=user_data)

            # 3. Compute Twitter Rank
            twitter_rank_analysis: TwitterRankAnalysisDoc = TwitterRankAnalysisDoc(
                activity=response_twitter_credibility.get("activity"),
                popularity=response_twitter_credibility.get("popularity"),
                influence=response_twitter_credibility.get("influence"),
                rank=response_twitter_credibility.get("credibility"))
        except Exception as e:
            logger.error(e)
        return twitter_rank_analysis

    def set_up_botometer(self, consumer_key: str, consumer_secret: str, access_token: str,
                         access_token_secret: str) -> Botometer:
        botometer_api: Botometer = object.__new__(Botometer)
        try:
            twitter_app_auth: dict = {
                'consumer_key': consumer_key,
                'consumer_secret': consumer_secret,
                'access_token': access_token,
                'access_token_secret': access_token_secret}
            botometer_api: Botometer = Botometer(
                wait_on_ratelimit=True,
                rapidapi_key=self.botometer_api_key,
                **twitter_app_auth)

        except Exception as e:
            logger.error(e)
        return botometer_api

    def analyse_account_by_id(self, user_id: int) -> TwitterCredibilityDoc:
        output: TwitterCredibilityDoc = TwitterCredibilityDoc()
        try:
            # Check a single account by id
            response: dict = self.botometer_api.check_account(user_id)
            if response.get("cap", False):
                output: TwitterCredibilityDoc = TwitterCredibilityDoc(
                    cap=response.get("cap", {}),
                    display_scores=response.get("display_scores", {}),
                    analysed=True)
        except Exception as e:
            logger.warning(e)
        return output

    def get_twitter_credibility_rank(self, url: str) -> TwitterCredibilityDoc:
        twitter_credibility: TwitterCredibilityDoc = TwitterCredibilityDoc()
        try:
            # 1. Parser URL
            tld_res: ExtractResult = self.parse_url(
                url=url)
            domain_url: str = tld_res.fqdn

            # 2. Retrieve user
            if self.twitter_connector.api is None:
                self.twitter_connector.set_up_twitter_api_connection()

            user: User = self.twitter_connector.extract_twitter_account_by_searching(
                api=self.twitter_connector.api, keyword=domain_url)

            user_data: dict = self.twitter_connector.retrieve_user_data(
                user=user)

            # 3. Retrieve analysis
            twitter_credibility: TwitterCredibilityDoc = self.analyse_account_by_id(
                user_id=user_data.get("id"))
        except Exception as e:
            logger.error(e)
        return twitter_credibility

