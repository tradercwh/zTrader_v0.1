'''

    | close price | stock_id | action | action price | date | volume | tax |

'''

def capital_curve_from_action_record():
    pass


def return_curve_from_action_record():
    pass


def csv_to_exel():
    '''
        read the csv as dataframe, then write to excel
    '''

    pass


#generate random number



class Analysis():
    def __init__(self, output):
        self.output = output
        pass

    def analysis(self, metrics, result):
        
        anal_result = {}
        for metric in metrics:
            metric_index = metric(result)
            index_name = metric.__doc__

            anal_result.update(
                {index_name : metric_index}
            )

        return anal_result

    def report(self, result):
        anal_result = self.analysis(result)