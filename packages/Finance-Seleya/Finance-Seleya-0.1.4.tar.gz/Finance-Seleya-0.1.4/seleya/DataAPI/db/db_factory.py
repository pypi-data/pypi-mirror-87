# -*- coding: utf-8 -*-
import pandas as pd

mapping_name = {'GDOveriewFactory':'gd_overview',
                'GDReviewsFactory':'gd_reviews',
                'GDELTFeedFactory':'gdelt_feed',
                'GDELTGEOFactory':'gdelt_geo',
                'GDELTTimelineToneFactory':'gdelt_timelinetone',
                'GDELTTimelineVolinfoFactory':'gdelt_timelinevolinfo',
                'GDELTTimelineVolrawFactory':'gdelt_timelinevolraw',
                'BDLabelDataFactory':'bd_label_data',
                'ESGFeedFactory':'esg_feed',
                'ESGFactorFactory':'esg_factor'}


class EngineFactory():
    def create_engine(self, engine_class):
        return engine_class()
    
    def __init__(self, engine_class):
        self._fetch_engine = self.create_engine(engine_class)

        
class ShowColumnsFactory(EngineFactory):
    def result(self, name):
        return self._fetch_engine.show_cloumns(mapping_name[name]) if name in mapping_name else pd.DataFrame(
            columns=['name','type'])

class CustomFactory(EngineFactory):
    def result(self, query):
        return self._fetch_engine.custom(query)
    
class GDOveriewFactory(EngineFactory):
    def result(self, codes, key=None, columns=None):
        return self._fetch_engine.gd_overview(codes=codes, key=key, 
                                              columns=columns)

class GDReviewsFactory(EngineFactory):
    def result(self, codes, key=None, begin_date=None, end_date=None,
               columns=None, freq=None,dates=None):
        return self._fetch_engine.gd_reviews(codes=codes, key=key, begin_date=begin_date, 
                                           end_date=end_date, columns=columns, freq=freq, 
                                           dates=dates)
class GDDistributionRatingsFactory(EngineFactory):
    def result(self, codes=None, key=None, columns=None):
        return self._fetch_engine.gd_distribution_ratings(codes=codes, key=key, columns=columns)
    
    
class GDTrendRatingsFactory(EngineFactory):
    def result(self, codes, key=None, begin_date=None, end_date=None,
               columns=None, freq=None,dates=None):
        return self._fetch_engine.gd_trend_ratings(codes=codes, key=key, begin_date=begin_date, 
                                           end_date=end_date, columns=columns, freq=freq, 
                                           dates=dates)
    
class GDELTFeedFactory(EngineFactory):
    def result(self, codes, key=None, begin_date=None, end_date=None,
               columns=None, freq=None,dates=None):
        return self._fetch_engine.gdelt_feed(codes=codes, key=key, begin_date=begin_date, 
                                           end_date=end_date, columns=columns, freq=freq, 
                                           dates=dates)

class GDELTGEOFactory(EngineFactory):
    def result(self, codes, key=None, columns=None):
        return self._fetch_engine.gdelt_geo(codes=codes, key=key, 
                                              columns=columns)
    
class GDELTTimelineToneFactory(EngineFactory):
    def result(self, codes, key=None, begin_date=None, end_date=None,
               columns=None, freq=None,dates=None):
        return self._fetch_engine.gdelt_timelinetone(codes=codes, key=key, begin_date=begin_date, 
                                                     end_date=end_date, columns=columns, freq=freq,
                                                     dates=dates)

class GDELTTimelineVolinfoFactory(EngineFactory):
    def result(self, codes, key=None, begin_date=None, end_date=None,
               columns=None, freq=None,dates=None):
        return self._fetch_engine.gdelt_timelinevolinfo(codes=codes, key=key, begin_date=begin_date, 
                                                     end_date=end_date, columns=columns, freq=freq,
                                                     dates=dates)


class GDELTTimelineVolrawFactory(EngineFactory):
    def result(self, codes, key=None, begin_date=None, end_date=None,
               columns=None, freq=None,dates=None):
        return self._fetch_engine.gdelt_timelinevolraw(codes=codes, key=key, begin_date=begin_date, 
                                                     end_date=end_date, columns=columns, freq=freq,
                                                     dates=dates)
    
class BDLabelDataFactory(EngineFactory):
    def result(self, codes=None, key=None, begin_date=None, end_date=None,
               columns=None, freq=None,dates=None):
        return self._fetch_engine.bd_label_data(codes=codes, key=key, begin_date=begin_date, 
                                                     end_date=end_date, columns=columns, freq=freq,
                                                     dates=dates)
    
    
class BHRFeedFactory(EngineFactory):
    def result(self, codes=None, key=None, begin_date=None, end_date=None,
               columns=None, freq=None,dates=None):
        return self._fetch_engine.bhr_feed(codes=codes, key=key, begin_date=begin_date, 
                                                     end_date=end_date, columns=columns, freq=freq,
                                                     dates=dates)
class BHRLabelFactory(EngineFactory):
    def result(self, key_name, key_value, query_name, query_values, 
                  columns=None, freq=None):
        return self._fetch_engine.bhr_label(key_name=key_name, key_value=key_value, 
                                            query_name=query_name, query_values=query_values, 
                                            columns=columns, freq=freq)
    
class ESGFeedFactory(EngineFactory):
    def result(self, codes=None,  categories=None, begin_date=None, end_date=None,
                columns=None, freq=None, dates=None):
        return self._fetch_engine.esg_feed(codes=codes, categories=categories, 
                                              begin_date=begin_date, end_date=end_date,
                                              columns=columns, freq=freq, dates=dates)
class ESGFactorFactory(EngineFactory):
    def result(self, codes=None,  categories=None, level=None, begin_date=None, end_date=None,
                columns=None, freq=None, dates=None):
        return self._fetch_engine.esg_factor(codes=codes, categories=categories, 
                                             level=level, begin_date=begin_date, 
                                             end_date=end_date, columns=columns, 
                                             freq=freq, dates=dates)
class ESGDetailFactory(EngineFactory):
    def result(self, classify=None, category=None, level=None, columns=None):
        return self._fetch_engine.esg_detail(classify=classify, 
                                             category=category,
                                             level=level,
                                             columns=columns)
    
class UltronGentic(EngineFactory):
    def result(self, rootid=None, fitness=None, classify=None, columns=None):
        return self._fetch_engine.ultron_gentic(rootid=rootid, 
                                             fitness=fitness,
                                             classify=classify,
                                             columns=columns)
        