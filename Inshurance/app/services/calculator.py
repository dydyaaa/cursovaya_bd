from datetime import datetime
from flask import jsonify
from app.utils import execute_query

region = {
    'Москва': 1.5,
    'Московская область': 1.3,
    'Санкт-Петербург': 1.4,
    'Краснодарский край': 1.2,
    'Татарстан': 1.3,
    'default': 1.1
}

policy_duration_factors = {
    '1 день': 0.1,
    '1 месяц': 0.2,
    '3 месяца': 0.5,
    '6 месяцев': 0.7,
    '1 год': 1.0
}


class Calculator:
    
    @staticmethod
    def calculate_age(birth_year):
        current_year = datetime.now().year
        return current_year - int(birth_year[:4])
    
    @staticmethod
    def calculate_driving_experience(license_year):
        current_year = datetime.now().year
        return current_year - int(license_year[:4])
    
    @staticmethod
    def get_age_coefficient(car_year):
        current_year = datetime.now().year
        car_age = current_year - car_year

        if car_age < 3:
            return 1.2  
        elif 3 <= car_age <= 7:
            return 1.0
        else:
            return 1.2
    
    def calculation(policy_type,
                    policy_region,
                    car_brand: str, 
                    car_model: str, 
                    year: datetime, 
                    duration: str,
                    drivers: list):
        
        query = ''' SELECT coefficient FROM brands
                    WHERE brand = %s AND (model = %s OR model = 'default')
                    LIMIT 1
                '''
        
        params = (car_brand, car_model)
        car_coefficient = float(execute_query(query, params)[0][0])
        
        base_price = 6000 if policy_type == 'ОСАГО' else 20000
        
        duration_coefficient = policy_duration_factors.get(duration, 1)
        
        if len(drivers) == 0 or len(drivers) > 5:
            driver_coefficient = 2
        
        driver_coefficient = 1.0
        for driver in drivers:
            age = Calculator.calculate_age(driver['driver_birth'])
            driving_experience = Calculator.calculate_driving_experience(driver['first_license_date'])
            
            if age < 25:
                driver_coefficient += 0.05  
            if driving_experience < 5:
                driver_coefficient += 0.05
        
        age_coefficient = Calculator.get_age_coefficient(year)
        
        region_coefficient = region.get(policy_region, region['default'])
        
        final_price = base_price * car_coefficient * region_coefficient * duration_coefficient * driver_coefficient * age_coefficient
        
        return int(final_price)
