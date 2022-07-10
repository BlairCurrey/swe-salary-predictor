def is_valid_salary(salary: int):
    return 0 < salary < 1_000_000

def format_currency(number_string):
    return "${:,.2f}".format(number_string)

def get_raw_prediction_input(input_dict):
    return {
        "age_first_code": input_dict.age_first_code, 
        "years_code": input_dict.years_code,
        "years_code_pro": input_dict.years_code_pro, 
        "age": input_dict.age, 
        "country": input_dict.country, 
        "dev_type": input_dict.dev_type,
        "languages": input_dict.languages,
        "ed_level": input_dict.ed_level
    }