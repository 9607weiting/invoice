import os

class Results():

    def __init__(self,path):
        
        self.path = path


    def file_path(self):

        if os.path.exists(self.path):

            print(f'>>> csv path {self.path} existed.')

        else:

            print(f'>>> csv path {self.path} created.')

            os.makedirs(self.path,exist_ok=True)


    def df_without_header(self,filename,df):
        
        self.file_path()

        path = f'{self.path}\{filename}'

        df.to_csv(path,mode='a',header=False,index=False)


    def df_with_header(self,filename,df):

        self.file_path()

        path = f'{self.path}\{filename}'

        df.to_csv(path,mode='a',header=True,index=False)
