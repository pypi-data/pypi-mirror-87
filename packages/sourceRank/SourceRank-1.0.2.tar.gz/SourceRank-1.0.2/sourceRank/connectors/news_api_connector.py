from newsapi import NewsApiClient
from newsapi.const import categories
from sourceRank.helper.settings import logger
from sourceRank.helper.utils import get_best_matching_candidate_from_list, get_nationality_from_country_code
from sourceRank.models.source_credibility_models import NewsAPISourceDoc


class NewsAPIConnector(object):
    def __init__(self, api_key: str):
        self.api_key: str = api_key
        self.news_api: NewsApiClient = NewsApiClient(
            api_key=self.api_key)

    @staticmethod
    def get_source_categories() -> list:
        return categories

    def get_sources_from_news_api(self, category: str = None, country_code: str = None,
                                  language: str = None) -> list:
        sources: list = []
        try:
            response_api: dict = self.news_api.get_sources(
                category=category, country=country_code, language=language)
            sources: list = response_api.get("sources", [])
        except Exception as e:
            logger.error(e)
        return sources

    def get_everything_from_news_api(self, q: str,sources: str,
                                     domains: str,from_param: str,
                                     to: str, language: str,
                                     sort_by: str = 'relevancy',
                                     page: int = 2) -> dict:
        all_articles: dict = {}
        try:
            all_articles: dict = self.news_api.get_everything(
                q=q,
                sources=sources,
                domains=domains,
                from_param=from_param,
                to=to,
                language=language,
                sort_by=sort_by,
                page=page)
        except Exception as e:
            logger.error(e)
        return all_articles

    def get_source_matching_from_url(self, candidate_source, category: str = None,
                                     country_code: str = None, language: str = None) -> NewsAPISourceDoc:
        source_matching: NewsAPISourceDoc = object.__new__(NewsAPISourceDoc)
        try:
            sources: list = self.get_sources_from_news_api(
                category=category, country_code=country_code, language=language)

            # Get matching index
            res_source_matching: tuple = get_best_matching_candidate_from_list(
                candidate=candidate_source, matching_options=sources)

            # 2. Retrieve index
            source_matching_obj: dict = res_source_matching[0]

            source_matching: NewsAPISourceDoc = NewsAPISourceDoc(
                id=source_matching_obj.get("id"),
                name=source_matching_obj.get("name"),
                description=source_matching_obj.get("description"),
                url=source_matching_obj.get("url"),
                category=source_matching_obj.get("category"),
                language=source_matching_obj.get("language"),
                country=source_matching_obj.get("country"),
                nationality=get_nationality_from_country_code(
                    source_matching_obj.get("country")))

        except Exception as e:
            logger.error(e)
        return source_matching
