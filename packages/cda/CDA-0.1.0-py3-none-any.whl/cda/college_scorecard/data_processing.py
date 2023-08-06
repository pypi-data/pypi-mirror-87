class DataProcessor:

    def _list_average(self, lists):
        n_lists = len(lists)
        list_length = len(lists[0])
        avg_list = [0.0 for i in range(list_length)]
        for i in range(list_length):
            for j in range(n_lists):
                avg_list[i] += lists[j][i]
            avg_list[i] /= n_lists
        return avg_list

    def _list_merge(self, public, private, ownership):
        list_length = len(public)
        merged_list = [None for i in range(list_length)]
        for i in range(list_length):
            if ownership[i] == ('public' or '1'):
                merged_list[i] = public[i]
            else:
                merged_list[i] = private[i]
        return merged_list

    def _degree_types(self, keys):
        degree_type = {
            '0': "Non-degree-granting",
            '1': "Certificate degree",
            '2': "Associate degree",
            '3': "Bachelor's degree",
            '4': "Graduate degree",
        }
        return [degree_type[key] for key in keys]

    def _ownership_types(self, keys):
        ownership_type = {
            '1': 'public',
            '2': 'private',
            '3': 'private',
        }
        return [ownership_type[key] for key in keys]

    def _is_religious_affiliate(self, keys):
        is_religious_affiliate = [False for i in range(len(keys))]
        for i in range(len(keys)):
            try:
                if (int(keys[i]) > 0):
                    is_religious_affiliate[i] = True
            except:
                pass
        return is_religious_affiliate

    def _is_for_profit(self, keys):
        is_for_profit = {
            '1': False,
            '2': False,
            '3': True,
        }
        return [is_for_profit[key] for key in keys]
