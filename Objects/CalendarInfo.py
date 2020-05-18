from General import Google, Functions


class CalendarInfo:

    def __init__(self):
        self.value_l_l_dict = {sheet.title: Functions.empty_strings_to_none(sheet.get_all_values())
                               for sheet in Google.get_google_sheets("LT Sheets")}
        self.value_list_list = self.value_l_l_dict["Calendar Info"]

        self.split_l_l_l = Functions.split_2d_list_by_vertical_none_list(self.value_list_list)

        self.ip_id_dict = self.get_ip_id_dict()
        self.param_dict = self.get_param_dict()

    def get_ip_id_dict(self):

        ip_id_dict = {}
        for data_list in self.split_l_l_l[0][1:]:
            ip_id_dict[data_list[0]] = data_list[1]
        return ip_id_dict

    def get_param_dict(self):
        param_dict = {}
        for data_list in self.split_l_l_l[1][1:]:
            param_dict[data_list[0]] = data_list[1]
        return param_dict

    def __str__(self):

        ret_str = "CalendarInfo (from the 'LT Sheets -> Calendar Info' Google Sheet" + "\n"
        ret_str += Functions.tab_str(Functions.dict_to_str(self.ip_id_dict)) + "\n"
        ret_str += Functions.tab_str(Functions.dict_to_str(self.param_dict))

        return ret_str
