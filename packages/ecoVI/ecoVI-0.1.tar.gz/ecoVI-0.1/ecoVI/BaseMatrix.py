class BaseMatrix:
    
    def __init__(self, df):
        ''' Class to hold the dataframe for the area over which Vulnerability Index has to be calculated 
            and other parameters.
            
            Attributes:
                region representing part of dataframe with columns denoting area
                region_cols representing columns denoting different regions in the area
                indicators representing part of dataframe with columns denoting various indicators of performance
                indicator_cols representing columns of performance indicators of the region
                
        '''
        self.df = df
        self.region = df.select_dtypes(exclude='number')
        self.region_cols = self.region.columns.tolist()
        self.indicators = df.select_dtypes(include='number')
        self.indicator_cols = self.indicators.columns.tolist()
        self.positive_indicators = []
        self.negative_indicators = []
    
    def change_region(self, action, other_region):
        ''' Takes new item(s) of indicators to either replace, append or remove existing indicators 
            
            Args:
                action (string) describing action
                other_indicators (str or list of str) containing new indicators
            
            Returns:
                None
        '''
        if action == 'replace':
            self.region_cols = [other_region]
        elif action == 'append':
            self.region_cols.append(other_region)
        elif action == 'remove':
            self.region_cols.remove(other_region)
        
        
    def change_indicator_cols(self, action, other_indicators):
        ''' Takes new item(s) of indicators to either replace, append or remove existing indicators 
            
            Args:
                action (string) describing action
                other_indicators (str or list of str) containing new indicators
            
            Returns:
                None
        '''
        
        if action == 'replace':
            self.indicator_cols = [other_indicators]
        elif action == 'append':
            self.indicator_cols.append(other_indicators)
        elif action == 'remove':
            self.indicator_cols.remove(other_indicators)
            
        
    def feed_indicator_relations(self, relations):
        ''' Creates a list of performance indicators based on their relationship to effect of vulnerability.

            Args:
             relations
                 (list) Takes in a list of 1s & -1s inidcating the relationship of a indicator col
                  Or   
                 (dict) Takes a dict with cols mapped to relationships   
            Returns:
                None
        '''
        if type(relations) == list:
            if len(relations) != len(self.indicator_cols):
                print("length mismatch; Number of indicators doesn't match number of relations passsed")
            else:
                for col, rel in zip(self.indicator_cols, relations):
                    if rel == 1:
                        self.positive_indicators.append(col)
                    elif rel == -1:
                        self.negative_indicators.append(col)
        elif type(relations) == dict:
            if len(relations) ==  2 and 1 in relations.keys():
                self.positive_indicators = relations[1]
                self.negative_indicators = relations[-1]
            elif len(relations)>2:
                rel_list = list(map(relations.get, self.indicator_cols))
                self.feed_indicator_relations(relations=rel_list)
                

    def calculate_scaled_df(self):
        ''' Creates a df with scaled version of performance indicators.
            
            Args:
                None
            Returns:
                scaled_df (dataframe)
        '''
        scaled_df = self.df.copy()
        scaled_df.set_index(self.region_cols, inplace=True)
        for col in self.indicator_cols:
            scale = scaled_df[col].max() - scaled_df[col].min() 
            if col in self.positive_indicators:
                scaled_df[col] = scaled_df[col].apply(lambda x: (x-scaled_df[col].min())/scale)
            elif col in self.negative_indicators:
                scaled_df[col] = scaled_df[col].apply(lambda x: (scaled_df[col].max()-x)/scale)
        return scaled_df