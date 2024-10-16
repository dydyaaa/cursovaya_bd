import datetime
from flask import jsonify

car_brands = {
    'Toyota': {
        'Corolla': 1.2,
        'Camry': 1.3,
        'RAV4': 1.4,
        'default': 1.1
    },
    'BMW': {
        'X5': 1.8,
        '3 Series': 1.7,
        '5 Series': 1.9,
        'default': 1.5
    },
    'Mercedes': {
        'C-Class': 1.6,
        'E-Class': 1.7,
        'GLC': 1.8,
        'default': 1.4
    },
    'Audi': {
        'A4': 1.5,
        'A6': 1.6,
        'Q7': 1.8,
        'default': 1.3
    },
    'Ford': {
        'Focus': 1.2,
        'Mondeo': 1.3,
        'Kuga': 1.4,
        'default': 1.1
    },
    'Nissan': {
        'Altima': 1.2,
        'X-Trail': 1.4,
        'Qashqai': 1.3,
        'default': 1.1
    },
    'Volkswagen': {
        'Golf': 1.3,
        'Passat': 1.4,
        'Tiguan': 1.5,
        'default': 1.2
    },
    'Hyundai': {
        'Elantra': 1.2,
        'Tucson': 1.3,
        'Santa Fe': 1.4,
        'default': 1.1
    },
    'Kia': {
        'Rio': 1.1,
        'Sportage': 1.3,
        'Sorento': 1.4,
        'default': 1.1
    },
    'Mazda': {
        'Mazda3': 1.2,
        'CX-5': 1.4,
        'Mazda6': 1.3,
        'default': 1.2
    },
    'Chevrolet': {
        'Cruze': 1.1,
        'Malibu': 1.3,
        'Tahoe': 1.6,
        'default': 1.2
    },
    'Honda': {
        'Civic': 1.2,
        'Accord': 1.3,
        'CR-V': 1.4,
        'default': 1.1
    },
    'Subaru': {
        'Impreza': 1.2,
        'Outback': 1.4,
        'Forester': 1.5,
        'default': 1.3
    },
    'Volvo': {
        'XC60': 1.5,
        'S90': 1.6,
        'XC90': 1.8,
        'default': 1.4
    },
    'Lexus': {
        'IS': 1.6,
        'ES': 1.7,
        'RX': 1.8,
        'default': 1.5
    },
    'Jaguar': {
        'XE': 1.7,
        'XF': 1.8,
        'F-Pace': 1.9,
        'default': 1.6
    },
    'Land Rover': {
        'Discovery': 1.8,
        'Range Rover': 2.0,
        'Evoque': 1.9,
        'default': 1.7
    },
    'Porsche': {
        'Macan': 2.0,
        'Cayenne': 2.2,
        '911': 2.5,
        'default': 1.9
    },
    'Jeep': {
        'Grand Cherokee': 1.7,
        'Wrangler': 1.8,
        'Cherokee': 1.6,
        'default': 1.5
    },
    'Mitsubishi': {
        'Lancer': 1.2,
        'Outlander': 1.4,
        'Pajero': 1.5,
        'default': 1.3
    },
    'Peugeot': {
        '308': 1.1,
        '3008': 1.3,
        '5008': 1.4,
        'default': 1.2
    },
    'Renault': {
        'Logan': 1.1,
        'Duster': 1.2,
        'Kaptur': 1.3,
        'default': 1.1
    },
    'Skoda': {
        'Octavia': 1.2,
        'Superb': 1.3,
        'Kodiaq': 1.4,
        'default': 1.2
    },
    'Tesla': {
        'Model 3': 2.0,
        'Model S': 2.2,
        'Model X': 2.3,
        'default': 2.0
    },
    'Suzuki': {
        'Vitara': 1.2,
        'SX4': 1.3,
        'Jimny': 1.4,
        'default': 1.2
    },
    'Infiniti': {
        'Q50': 1.5,
        'QX60': 1.7,
        'QX80': 1.9,
        'default': 1.6
    },
    'Acura': {
        'ILX': 1.4,
        'TLX': 1.5,
        'MDX': 1.6,
        'default': 1.4
    },
    'Alfa Romeo': {
        'Giulia': 1.8,
        'Stelvio': 1.9,
        'default': 1.7
    },
    'Ferrari': {
        '488': 2.8,
        'Portofino': 2.9,
        'default': 2.7
    },
    'Lamborghini': {
        'Huracan': 3.0,
        'Urus': 3.2,
        'default': 2.9
    },
    'Bentley': {
        'Bentayga': 3.0,
        'Continental': 3.3,
        'Flying Spur': 3.5,
        'default': 3.0
    },
    'default': 1.0 
}

regions = {
    'Москва': 1.5,
    'Московская область': 1.3,
    'Санкт-Петербург': 1.4,
    'Краснодарский край': 1.2,
    'Татарстан': 1.3,
    'default': 1.1
}

duration_dict = {
    'Год': 1,
    'Пол года': 0.7,
    '3 месяца': 0.5,
    '1 месяц': 0.2,
    '1 день': 0.1
}


class Calculator:
    def calculation_osago(brand: str, 
                          model: str, 
                          year: datetime, 
                          duration: str,
                          drivers: list):

        base_price = 5000  

        brand_coef = car_brands.get(brand, car_brands['default'])
        if isinstance(brand_coef, float):
            model_coef = 1.0
        else:
            model_coef = brand_coef.get(model, brand_coef['default'])

        current_year = datetime.datetime.now().year
        car_age = current_year - year
        car_age_coef = 1.0 + (car_age - 10) * 0.05 if car_age > 10 else 1.0

        driver_coef = 1.0
        max_region_coef = regions['default']
        for driver in drivers:
            region = driver.get('region', regions['default'])
            region_coef = regions.get(region, regions['default'])
            max_region_coef = max(max_region_coef, region_coef)

            # Расчет опыта вождения
            issue_date = driver.get('license_issue_date')
            issue_date = datetime.datetime.strptime(issue_date, "%Y-%m-%d")
            driving_experience = current_year - issue_date.year
            if driving_experience < 3:
                driver_coef += 0.2
            elif driving_experience < 5:
                driver_coef += 0.1

        final_cost = base_price * model_coef * car_age_coef * driver_coef * max_region_coef
        
        final_cost = final_cost * duration_dict.get(duration, 1)
        
        final_cost = final_cost if final_cost <= 400000 else 400000
        return jsonify({"result": int(final_cost)}), 200

    def calculation_casco(brand, model, year, car_value, drivers, region, risks):
        
        base_rate = 0.05  

        current_year = datetime.datetime.now().year
        car_age = current_year - year
        car_age_coef = 1.0 + (car_age - 5) * 0.03 if car_age > 5 else 1.0
        
        driver_coef = 1.0
        for driver in drivers:
            issue_date = driver.get('license_issue_date')
            driving_experience = current_year - issue_date.year
            if driving_experience < 3:
                driver_coef += 0.3 
            elif driving_experience < 5:
                driver_coef += 0.2  
                
        region_coef = regions.get(region, regions['default'])

        risk_coef = 1.0
        if 'угон' in risks:
            risk_coef += 0.2  
        if 'стихийные бедствия' in risks:
            risk_coef += 0.15
        if 'повреждения' in risks:
            risk_coef += 0.1
            
        final_cost = car_value * base_rate * car_age_coef * driver_coef * region_coef * risk_coef
        return round(final_cost, 2)

# brand = 'Toyota'
# model = 'Camry'
# year = 2018
# car_value = 1800000  
# drivers = [
#     {'name': 'Иван Иванов', 'license_issue_date': "2024-05-05", region: 'Москва'}
# ]
# risks = ['угон', 'стихийные бедствия']

# casco_cost = Calculator.calculation_casco(brand, model, year, car_value, drivers, region, risks)
# print(f"Стоимость КАСКО: {casco_cost} рублей")
