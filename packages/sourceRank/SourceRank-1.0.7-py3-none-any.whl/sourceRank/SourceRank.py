from sourceRank.analysis.source_credibility_analysis import SourceCredibilityAnalysis
from tldextract.tldextract import ExtractResult
from sourceRank.models.source_credibility_models import (SuffixRankDoc, OpenRankDoc,
                                                         CategoryAnalysisDoc,
                                                         WhoisAnalysisDoc,
                                                         TwitterCredibilityDoc)


class SourceRank(object):
    def __init__(self,  open_rank_api_key: str, whois_api_key: str, news_api_key: str,
                 consumer_key: str, consumer_secret: str, access_token: str,
                 access_token_secret: str, botometer_api_key: str):
        self.source_credibility_analyser: SourceCredibilityAnalysis = SourceCredibilityAnalysis(
            open_rank_api_key=open_rank_api_key,
            whois_api_key=whois_api_key,
            news_api_key=news_api_key,
            access_token_secret=access_token_secret,
            access_token=access_token,
            consumer_secret=consumer_secret,
            consumer_key=consumer_key,
            botometer_api_key=botometer_api_key)

    def process_url(self, url: str) -> ExtractResult:
        return self.source_credibility_analyser.parse_url(url=url)

    def get_open_rank_analysis(self, domain: str) -> OpenRankDoc:
        return self.source_credibility_analyser.get_open_rank_analysis(domain=domain)

    def get_suffix_analysis(self, suffix: str) -> SuffixRankDoc:
        return self.source_credibility_analyser.get_suffix_analysis(suffix=suffix)

    def get_whois_analysis(self, domain: str) -> WhoisAnalysisDoc:
        return self.source_credibility_analyser.get_whois_analysis(domain=domain)

    def get_category_analysis(self, url: str, category: str = None,
                              country_code: str = None, language: str = None) -> CategoryAnalysisDoc:
        return self.source_credibility_analyser.get_category_analysis(
            url=url, category=category, country_code=country_code, language=language)

    def get_twitter_analysis(self, url: str) -> TwitterCredibilityDoc:
        return self.source_credibility_analyser.get_twitter_credibility_rank(
            url=url)
