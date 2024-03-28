from pydantic import ValidationError
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib


class PropertyDetails(BaseModel):
    state_construction: str
    living_area: float
    bedrooms: int
    bathrooms: int
    has_garden: bool
    kitchen: bool
    fireplace: bool
    swimmingpool: bool
    has_terrace: bool
    has_attic: bool
    has_basement: bool
    epc: str
    area_total: float
    district: str


# Define the list of all district columns from training data
all_districts = [
    'district_aalst', 'district_antwerp', 'district_arlon', 'district_ath',
    'district_bastogne', 'district_brugge', 'district_brussels',
    'district_charleroi', 'district_dendermonde', 'district_diksmuide',
    'district_dinant', 'district_eeklo', 'district_gent',
    'district_halle-vilvoorde', 'district_hasselt', 'district_huy',
    'district_ieper', 'district_kortrijk', 'district_leuven',
    'district_liège', 'district_maaseik', 'district_marche-en-famenne',
    'district_mechelen', 'district_mons', 'district_mouscron',
    'district_namur', 'district_neufchâteau', 'district_nivelles',
    'district_oostend', 'district_oudenaarde', 'district_philippeville',
    'district_roeselare', 'district_sint-niklaas', 'district_soignies',
    'district_thuin', 'district_tielt', 'district_tongeren',
    'district_tournai', 'district_turnhout', 'district_verviers',
    'district_veurne', 'district_virton', 'district_waremme'
]


def transform_new_data(input_data):
    for district in all_districts:
        input_data[district] = 0  # Initialize all district columns to 0

    if 'district' in input_data.columns:
        input_data['district'] = input_data['district'].str.lower()
        for index, row in input_data.iterrows():
            district_col = f"district_{row['district']}"
            if district_col in all_districts:
                input_data.at[index, district_col] = 1
        input_data.drop('district', axis=1, inplace=True)

    return input_data


# Preprocessing class
class DataPreprocessor:
    def encode_columns(self, data):
        # Define mappings for 'epc' and 'state_construction' categories
        epc_mapping = {
            'A+_A++': 1, 'A+': 1, 'A_A+': 1, 'A++': 1, 'A': 1,
            'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'F_E': 8
        }
        state_construction_mapping = {
            'TO_RESTORE': 3, 'TO_RENOVATE': 3, 'TO_BE_DONE_UP': 3,
            'JUST_RENOVATED': 2, 'GOOD': 2, 'AS_NEW': 1
        }

        if 'epc' in data.columns:
            data['epc'] = data['epc'].map(epc_mapping).fillna(-1)
        if 'state_construction' in data.columns:
            data['state_construction'] = data['state_construction'].map(
                state_construction_mapping).fillna(-1)
        return data

    def convert_bool_to_int(self, data):
        # Convert boolean columns to integers
        bool_columns = ['has_garden', 'kitchen', 'fireplace',
                        'swimmingpool', 'has_terrace', 'has_attic', 'has_basement']
        for column in bool_columns:
            if column in data.columns:
                data[column] = data[column].astype(int)
        return data

    def preprocess(self, input_data):
        # Convert the dictionary to a DataFrame
        data_df = pd.DataFrame([input_data])

        # Apply district transformation
        transformed_data = transform_new_data(data_df)

        # Convert boolean columns to integers
        transformed_data = self.convert_bool_to_int(transformed_data)

        # Apply manual encoding
        encoded_data = self.encode_columns(transformed_data)

        return encoded_data


def transform_new_data(input_data):
    # Assuming all_districts list is defined elsewhere in code
    # Initialize all district columns to 0
    for district in all_districts:
        input_data[district] = 0

    if 'district' in input_data.columns:
        input_data['district'] = input_data['district'].str.lower()
        for district in all_districts:
            input_data[district] = input_data.apply(lambda row: 1 if district.endswith(
                '_' + row['district']) else row[district], axis=1)
        input_data.drop('district', axis=1, inplace=True)

    return input_data


app = FastAPI()

# Load trained model
model = joblib.load('random_forest_model.joblib')


@app.post("/predict")
async def predict_price(details: PropertyDetails):
    try:
        preprocessor = DataPreprocessor()
        # Convert the input details into a dictionary for processing
        input_data = details.model_dump()
        processed_data = preprocessor.preprocess(input_data)

        # Reshape the data as necessary for  model, and make a prediction
        prediction = model.predict(processed_data)
        return {"prediction": prediction[0]}

    except ValidationError as e:
        # Custom error handling for validation errors
        custom_errors = []
        for error in e.errors():
            field = "->".join(map(str, error['loc']))
            custom_message = f"Error in field '{field}': {error['msg']}"
            custom_errors.append({"field": field, "message": custom_message})
        raise HTTPException(status_code=422, detail=custom_errors)

    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(status_code=500, detail=str(e))
