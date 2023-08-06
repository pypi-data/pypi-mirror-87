from typing import List
from dataclasses import dataclass
from enum import Enum
from typing import List, Union, Optional
from datetime import datetime
from dataclasses import dataclass, field


class AccountType(Enum):
    AMAZON = 'Amazon'
    MICROSOFT_ADVERTISING = 'Microsoft Advertising'
    CRITEO = 'Criteo'
    FACEBOOK = 'Facebook'
    GOOGLE_ADS = 'Google Ads'
    GOOGLE_ANALYTICS = 'Google Analytics'
    MANOMANO = 'Manomano'
    MCT = 'Google Merchant Center'


@dataclass
class Campaign:
    campaign_id: str
    campaign_name: str
    campaign_status: Union[str, None] = None


@dataclass
class Account:
    account_type: AccountType
    account_id: str
    account_name: str
    campaigns: List[Campaign] = field(default_factory=list)


@dataclass
class ParametersMainSetting:
    client_id: str


@dataclass
class ParametersSubSettingPost:
    client_id: str
    scope_id: int
    name: str
    owners: List[str]


@dataclass
class ParametersSubSettingDelete:
    scope_id: int


class ImportType:
    CLUSTERING = "CLUSTERING"
    HTTP = "HTTP"
    SFTP = "SFTP"
    FTP = "FTP"
    GCS = "GCS"
    ORANGE_SFTP = "ORANGE_SFTP"
    GOSPORT_SFTP = "GOSPORT_SFTP"
    SPREADSHEET = "SPREADSHEET"
    BIG_QUERY = "BIG_QUERY"
    ADWORDS_PRODUCT = "ADWORDS_PRODUCT"
    GA_ECOMMERCE = "GA_ECOMMERCE"


class ChannelType(Enum):
    mct = 'mct'
    googleads = 'googleads'
    facebook = 'facebook'
    facebook_flight = 'facebook_flight'
    amazon_home = 'amazon_home'
    bing = 'bing'
    shopping_actions = 'shopping_actions'
    criteo = 'criteo'
    searchads_360 = 'searchads_360'
    leguide_fr = 'leguide_fr'
    kelkoo = 'kelkoo'
    mct_push = 'mct_push'
    pricerunner = 'pricerunner'
    prisjakt = 'prisjakt'
    eperflex = 'eperflex'
    choozen = 'choozen'
    custom = 'custom'
    effinity = 'effinity'
    awin = 'awin'
    pinterest = 'pinterest'
    moebel24 = 'moebel24'
    trovaprezzi = 'trovaprezzi'
    cherchons = 'cherchons'
    stylight = 'stylight'
    shopzilla = 'shopzilla'
    lionshome = 'lionshome'
    touslesprix = 'touslesprix'
    pricingassistant = 'pricingassistant'
    meubles_fr = 'meubles_fr'
    moebel_de = 'moebel_de'
    manomano = 'manomano'
    dsa = 'dsa'
    snapchat = 'snapchat'
    local_inventory_feed = "local_inventory_feed"
    local_inventory_push = "local_inventory_push"
    fitle = "fitle"


class GaParameters(object):
    """ Parameters needed for data ingestion GA ECOMMERCE """

    def __init__(self,
                 file_name: str,
                 sleep_time: int,
                 view_id: str,
                 start_date: str,
                 end_date: str,
                 metrics: List[str],
                 dimensions: Union[None, List[str]] = None):
        self.file_name = file_name
        self.sleep_time = sleep_time
        self.view_id = view_id
        self.start_date = start_date
        self.end_date = end_date
        self.metrics = metrics
        self.dimensions = dimensions if dimensions is not None else []

    @property
    def sleep_time(self) -> int:
        return self._sleep_time

    @sleep_time.setter
    def sleep_time(self, sleep_time: Union[int, float]):
        try:
            int_sleep_time = int(sleep_time)
        except ValueError as e:
            raise ValueError(f'failed to parse sleep time to an int. {str(e)}') from e
        if int_sleep_time < 0:
            raise ValueError(f'sleep_time should be a positive value and not {int_sleep_time}.')
        self._sleep_time = int_sleep_time

    def to_dict(self):
        result = dict(
            file_name=self.file_name,
            sleep_time=self.sleep_time,
            view_id=self.view_id,
            start_date=self.start_date,
            end_date=self.end_date,
            metrics=self.metrics)
        if self.dimensions:
            result.update(dimensions=self.dimensions)
        return result


class BodyGaReportApi(object):
    DATE_FORMAT = '%Y-%m-%d'

    def __init__(self,
                 index: int,  # current query number
                 total_queries: int,  # total number of queries to get entire data range
                 data_ingestion_id: int,
                 start_date: str,  # start date of the data range the cloud function will handle
                 end_date: str,
                 monitoring_id: Optional[str] = None):  # end date of the data range the cloud function will handle
        self.index = index
        self.total_queries = total_queries
        self.data_ingestion_id = data_ingestion_id
        self.start_date = start_date
        self.end_date = end_date
        self.monitoring_id = monitoring_id

    @property
    def start_date(self) -> str:
        return self._start_date

    @start_date.setter
    def start_date(self, start_date: str):
        try:
            datetime.strptime(start_date, self.__class__.DATE_FORMAT)
        except ValueError as e:
            raise ValueError(
                f"start_date has an invalid format : {e}")
        self._start_date = start_date

    @property
    def end_date(self) -> str:
        return self._end_date

    @end_date.setter
    def end_date(self, end_date: str):
        try:
            datetime.strptime(end_date, self.__class__.DATE_FORMAT)
        except ValueError as e:
            raise ValueError(
                f"end_date has an invalid format : {e}")
        self._end_date = end_date

    def to_dict(self):
        output = dict(
            index=self.index,
            total_queries=self.total_queries,
            data_ingestion_id=self.data_ingestion_id,
            start_date=self.start_date,
            end_date=self.end_date
        )

        if self.monitoring_id is not None:
            output['monitoring_id'] = self.monitoring_id

        return output
