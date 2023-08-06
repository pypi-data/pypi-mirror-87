from newsapi import NewsApiClient
from newsapi.const import categories
from sourceRank.helper.settings import logger, default_field
from sourceRank.helper.utils import (get_best_matching_candidate_from_list,
                                     get_nationality_from_country_code,
                                     get_country_name_by_code, parse_url)
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

            sources_domains = [parse_url(url=i.get("url")).registered_domain for i in sources]

            # Get matching index
            res_source_matching: tuple = get_best_matching_candidate_from_list(
                candidate=candidate_source, matching_options=sources_domains)

            # 2. Retrieve index
            if res_source_matching[1] > 85:
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
                        source_matching_obj.get("country")),
                    analysed=True)
            else:
                source_matching: NewsAPISourceDoc = NewsAPISourceDoc(
                    id=default_field,
                    name=default_field,
                    description=default_field,
                    url=candidate_source,
                    category=default_field,
                    language=default_field,
                    country=get_country_name_by_code(country_code=country_code),
                    nationality=get_nationality_from_country_code(
                        country_code=country_code),
                    analysed=False)

        except Exception as e:
            logger.error(e)
        return source_matching
