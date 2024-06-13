import os

def return_all_series_dirs(unzip_dir_path, uhid):
    series_dirs = []
    uhid_path = os.path.join(unzip_dir_path, uhid)
    uhid_path=uhid_path.replace("\\", "/")

    if os.path.isdir(uhid_path):
        
        for date_dir in os.listdir(uhid_path):
            date_path = os.path.join(uhid_path, date_dir)
            date_path=date_path.replace("\\", "/")

            if os.path.isdir(date_path):

                for series_dir in os.listdir(date_path):
                    series_path = os.path.join(date_path, series_dir)
                    series_path=series_path.replace("\\", "/")


                    if os.path.isdir(series_path):
                        series_dirs.append(series_path)
    return series_dirs


# unziped_path = 'C:/Users/EIOT/Desktop/Unziped_dir'
# series_dir=return_all_series_dirs(unziped_path,'123')
# print(series_dir)