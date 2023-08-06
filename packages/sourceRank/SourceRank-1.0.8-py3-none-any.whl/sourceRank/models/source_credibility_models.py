from sourceRank.helper.utils import get_str_datetime_from_non_formatted_str, get_country_name_by_code
from sourceRank.helper.settings import default_field


class SuffixRankDoc(object):
    def __init__(self, suffix: str = "", importance: float = -1, rank: float = -1, analysed: bool = False):
        self.suffix: str = suffix
        self.importance: float = importance
        self.rank: float = rank
        self.analysed: bool = analysed


class OpenRankDoc(object):
    def __init__(self, domain: str = "", page_rank_decimal: float = 0.0, original_rank: float = 0.0,
                 rank: float = 0.0, last_updated: str = "", analysed: bool = True):
        self.domain: str = domain
        self.page_rank_decimal: float = page_rank_decimal
        self.original_rank: float = original_rank
        self.rank: float = rank
        self.last_updated: str = get_str_datetime_from_non_formatted_str(
            str_datetime=last_updated)
        self.analysed: bool = analysed


class CategoryAnalysisDoc(object):
    def __init__(self, id: str = "", name: str = "", description: str = "", url: str = "",
                 category: str = "", language: str = "", country_code: str = "",
                 importance: float = 0.0, rank: float = 0.0, analysed: bool = False):
        self.id: str = id
        self.name: str = name
        self.description: str = description
        self.url: str = url
        self.category: str = category
        self.language: str = language
        self.country_code: str = country_code
        self.importance: float = importance
        self.rank: float = rank
        self.analysed: bool = analysed


class NewsAPISourceDoc(object):
    def __init__(self, id: str, name: str, description: str, url: str,
                 category: str, language: str, country: str, nationality: str,
                 analysed: bool = False):
        self.id: str = id
        self.name: str = name
        self.description: str = description
        self.url: str = url
        self.category: str = category
        self.language: str = language
        self.country: str = country
        self.nationality: str = nationality
        self.analysed: bool = analysed


class WhoisAnalysisDoc(object):
    def __init__(self, whois_data: dict, rank: float = 0.0, analysed: bool = False):
        self.domain_name: str = whois_data.get("domainName", default_field)
        self.created_date: str = get_str_datetime_from_non_formatted_str(
            str_datetime=whois_data.get("registryData", {}).get(
                "createdDate", default_field))
        self.updated_date: str = get_str_datetime_from_non_formatted_str(
            str_datetime=whois_data.get("registryData", {}).get(
                "updatedDate", default_field))
        self.expired_date: str = get_str_datetime_from_non_formatted_str(
            str_datetime=whois_data.get("registryData", {}).get(
                "updatedDate", default_field))
        self.organization: str = whois_data.get("registryData", {}).get("registrant", {}).get(
            "organization", default_field)
        self.street: str = whois_data.get("registryData", {}).get("registrant", {}).get(
            "street1", default_field)
        self.city: str = whois_data.get("registryData", {}).get("registrant", {}).get(
            "city", default_field)
        self.state: str = whois_data.get("registryData", {}).get("registrant", {}).get(
            "state", default_field)
        self.postal_code: str = whois_data.get("registryData", {}).get("registrant", {}).get(
            "postalCode", default_field)
        self.country_code: str = whois_data.get("registryData", {}).get("registrant", {}).get(
            "countryCode", default_field)
        self.country: str = get_country_name_by_code(
            country_code=self.country_code)
        self.registrar_name: str = whois_data.get("registrarName", default_field)
        self.registrar_ANAID: str = whois_data.get("registrarIANAID", default_field)
        self.estimated_domain_age: int = whois_data.get("estimatedDomainAge", 0)
        self.rank: float = rank
        self.analysed: bool = analysed


class TwitterRankAnalysisDoc(object):
    def __init__(self, popularity: float, influence: float, activity: float, rank: float):
        self.popularity: float = popularity
        self.influence: float = influence
        self.activity: float = activity
        self.rank: float = rank


class TwitterCredibilityDoc(object):
    def __init__(self, cap: dict = None, display_scores: dict = None, analysed: bool = False):
        self.analysed: bool = analysed
        self.english_score: float = cap.get("english", 0.0) if cap is not None else 0.0
        self.universal_score: float = cap.get("universal", 0.0) if cap is not None else 0.0
        self.english_display_scores: dict = display_scores.get("english", {}) if\
            display_scores is not None else {}
        self.universal_display_scores: dict = display_scores.get("universal", {}) if\
            display_scores is not None else {}
        self.rank: float = round(1 - ((self.universal_score + self.english_score) / 2), 3)
