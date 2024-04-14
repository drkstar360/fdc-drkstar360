import pandas as pd
from models import Restaurant, Product, Category,engine, get_or_create
from sqlalchemy.orm import sessionmaker
from utils import setup_logger

class ExcelFilePipeline:
    def __init__(self, file_path):
        self.lg = setup_logger()
        self.lg.info('ExcelFilePipeline starting.....')
        self.file_path = file_path
        self.df = self.excel_to_df()
        self.dropped_rows = None
        self.cleaned_df, self.dropped_rows = self.clean_df()

    def excel_to_df(self):
        self.lg.info('Reading Excel file...')
        df = pd.read_excel(io=self.file_path, sheet_name=0, index_col=0, header=0, engine='openpyxl', usecols='A, C, E, H, K, L, M')
        self.lg.info('Excel file read successfully')
        return df

    def clean_df(self):
        self.lg.info('Cleaning dataframe...')
        self.df.rename(columns={'Product Name': 'name',
                                'Ingredients on Product Page': 'ingredients',
                                'Store': 'restaurants',
                                'Allergens and Warnings':'allergens',
                                'Product category': 'category',
                                'URL of primary product picture': 'picture',
                                },
                       inplace=True)
        na_free = self.df.dropna(subset=['name', 'ingredients', 'restaurants'])
        self.dropped_rows = self.df[~self.df.index.isin(na_free.index)]
        # self.df = na_free
        self.df = None # set to None to save memory
        self.lg.info('DataFrame cleaned successfully')
        return na_free, self.dropped_rows

    def upload_to_db(self):
        print("uploading to db....")
        restaurant_df = self.cleaned_df['restaurants'].unique()
        category_df = self.cleaned_df['category'].unique()
        Session = sessionmaker(bind=engine)
        session = Session()

        res_dict = {}
        for res in restaurant_df:
            instance, created = get_or_create(session=session, model=Restaurant, defaults={'name': res}, name=res)
            session.commit()
            res_dict[instance.name] = instance

        cat_dict = {}
        for cat in category_df:
            instance, created = get_or_create(session=session, model=Category, defaults={'name': cat}, name=cat)
            session.commit()
            cat_dict[instance.name] = instance

        for row in self.cleaned_df.itertuples():
            cat = cat_dict[row.category]
            res = res_dict[row.restaurants]

            product_data = get_or_create(session=session, model=Product,
                                         defaults={'name': row.name, 'ingredients': row.ingredients, 'restaurant': res,
                                                   'category': cat, 'picture': row.picture, 'allergens': row.allergens},
                                         name=row.name, category=cat, restaurant=res)

            session.commit()
        session.close()

        self.lg.info('Data uploaded successfully')
        print("done")