import os
import shutil
import pandas as pd


def init_user_dataset_file(user):
    dataset_file_name_with_extension = "POC_dataset_expo_test.csv"
    grid_file_name_with_extension = "interpretationGrid_expo_test.csv"
    dataset_file_path = os.path.join(
        "static",
        "userStudyData",
        "POC_dataset",
        dataset_file_name_with_extension,
    )
    grid_file_path = os.path.join(
        "static",
        "userStudyData",
        "POC_grid",
        grid_file_name_with_extension,
    )
    if is_dataset_csv_exist(dataset_file_path) and is_dataset_csv_exist(
        grid_file_path
    ):
        file_name = user + "_" + dataset_file_name_with_extension
        file_path = os.path.join("static", "userStudyData", "output", file_name)
        shutil.copy(dataset_file_path, file_path)
        dataset_images_name_list = extract_im_name_from_dataset(file_path)
        user_dataset_path = file_path
        dataset_images_name_list = dataset_images_name_list
        return user_dataset_path, grid_file_path, dataset_images_name_list
    else:
        return None, None, None


def update_image_score(csv_file_path, image_name, im_score):
    df = pd.read_csv(csv_file_path)
    df.loc[df["imName"] == image_name, "imScore"] = im_score
    df.to_csv(csv_file_path, index=False)


def get_showing_image(user_csv_file, grid_csv_file, image_name):

    # find ref image info(url, sector, sceneType)
    (
        ref_image_url,
        ref_image_sector,
        ref_image_sceneType,
    ) = update_reference_image(user_csv_file, image_name)
    # find compare image url
    update_compare_image(grid_csv_file, ref_image_sector, ref_image_sceneType)
    return ref_image_url


def update_compare_image(grid_csv_file, ref_image_sector, ref_image_sceneType):
    # get url list
    compare_im_url_list = get_im_url_by_sector_sceneType(
        grid_csv_file, ref_image_sector, ref_image_sceneType
    )
    # find right image url for show from score


def update_reference_image(user_csv_file, image_name):
    # ref image ref
    ref_image_url = get_im_url_from_name(user_csv_file, image_name)
    # image sector
    ref_image_sector = get_im_sector_from_name(user_csv_file, image_name)
    # image sceneType
    ref_image_sceneType = get_im_sceneType_from_name(user_csv_file, image_name)
    return ref_image_url, ref_image_sector, ref_image_sceneType


def extract_im_name_from_dataset(user_csv_file):
    df = pd.read_csv(user_csv_file)
    return df["imName"].values.tolist()


def convert_dataset_to_dict(user_csv_file):
    dataset_dict = pd.read_csv(
        user_csv_file, index_col=0, skiprows=0
    ).T.to_dict()
    return dataset_dict


def get_im_url_from_name(csv_file_path, image_name):
    df = pd.read_csv(csv_file_path)
    image_url = df.loc[
        df["imName"] == image_name,
        "imPath",
    ]
    return image_url.values.tolist()[0]


def get_im_url_by_sector_sceneType(csv_file_path, sector, sceneType):
    df = pd.read_csv(csv_file_path)
    image_url = df.loc[
        ((df["sector"] == sector) & (df["sceneType"] == sceneType)),
        "imPath",
    ]
    return image_url.values.tolist()


def get_im_sector_from_name(csv_file_path, image_name):
    df = pd.read_csv(csv_file_path)
    image_sector = df.loc[
        df["imName"] == image_name,
        "sector",
    ]
    return image_sector.values.tolist()[0]


def get_im_sceneType_from_name(csv_file_path, image_name):
    df = pd.read_csv(csv_file_path)
    image_sceneType = df.loc[
        df["imName"] == image_name,
        "sceneType",
    ]
    return image_sceneType.values.tolist()[0]


def is_dataset_csv_exist(csv_file_path):
    return os.path.exists(csv_file_path)


def get_file_name_from_path(file_path):
    return os.path.basename(file_path)


# if __name__ == "__main__":
#     csv_file_path = os.path.join(
#         "static", "userStudyData", "output", "test.csv"
#     )
#     grid_file_name_with_extension = "interpretationGrid_expo_test.csv"
#     grid_file_path = os.path.join(
#         "static",
#         "userStudyData",
#         "POC_grid",
#         grid_file_name_with_extension,
#     )
#     image_name = "01006640_6206398-standard_2400x1800_72_validated.jpg"
#     a = get_im_url_by_sector_sceneType(grid_file_path, "foodPro", "bright")
#     print(a)
