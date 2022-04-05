import math
import os
import pandas as pd
import shutil


class UserStudyPOC_with_reset(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.dataset_initiated = False
        self.on_left_vertex = False
        self.on_right_vertex = False
        self.user_dataset_path = ""
        self.dataset_images_name_list = ""

        self.current_dataset_image_url = None
        self.current_grid_image_url = None

        self.grid_file_path = ""
        self.current_grid_image_index = -1

        self.all_grid_im_url_list = []
        # private variable
        self._current_dataset_image_index = -1
        self._init_grid_image_index = -1
        self._upper_boundary = -1
        self._down_boundary = -1
        self._compute_average_score = False

    def init_user_dataset_file(self, user):
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
        if self._is_file_exist(dataset_file_path) and self._is_file_exist(
            grid_file_path
        ):
            file_name = user + "_" + dataset_file_name_with_extension
            file_dir = file_path = os.path.join(
                "static", "userStudyData", "output"
            )
            file_path = os.path.join(file_dir, file_name)
            if not os.path.isdir(file_dir):
                os.makedirs(file_dir)
            if self._is_file_exist(file_path):
                # start from annotated image
                self.dataset_images_name_list = self._extract_im_name_from_csv(
                    file_path
                )
            else:
                shutil.copy(dataset_file_path, file_path)
                self.dataset_images_name_list = self._extract_im_name_from_csv(
                    file_path
                )

            self.dataset_initiated = True
            self.user_dataset_path = file_path
            self.grid_file_path = grid_file_path
        else:
            self.dataset_initiated = False

    def get_grid_url_list_from_left_button(self):
        # go left completely
        if self.current_grid_image_index <= self._init_grid_image_index:
            print()
            print("on left side")
            if self.current_grid_image_index == self._init_grid_image_index:
                self._down_boundary = 0

            self._upper_boundary = self.current_grid_image_index
        # on right part and want to go left
        else:
            print("on right side")
            # we touch the right vertex
            if self.on_right_vertex:
                print(
                    "touched right vertex and we computer average score from here"
                )
                self.on_right_vertex = False
                self._compute_average_score = True
                grid_im_url_list = self.all_grid_im_url_list[
                    len(self.all_grid_im_url_list)
                    - 2 : len(self.all_grid_im_url_list)
                ]
                print("self._down_boundary ", self._down_boundary)
                print("self._upper_boundary ", self._upper_boundary)
                print()
                return grid_im_url_list
            self._upper_boundary = self.current_grid_image_index

        grid_im_url_list = self.all_grid_im_url_list[
            self._down_boundary : self._upper_boundary
        ]
        if self._down_boundary == 0 and self._upper_boundary == 1:
            print("touch left vertex")
            self.on_left_vertex = True
            grid_im_url_list = [self.all_grid_im_url_list[0]]
        if self._down_boundary == self._upper_boundary:
            print("down boundary == upper boundary")
            grid_im_url_list = [self.all_grid_im_url_list[self._down_boundary]]

        # other case then touch the vertex
        if len(grid_im_url_list) == 1 and not self.on_left_vertex:
            self._compute_average_score = True
            grid_im_url_list = self.all_grid_im_url_list[
                self._down_boundary : self._upper_boundary + 1
            ]
        print("self._down_boundary ", self._down_boundary)
        print("self._upper_boundary ", self._upper_boundary)
        print()
        return grid_im_url_list

    def get_grid_url_list_from_right_button(self):
        # go right completely
        if self.current_grid_image_index >= self._init_grid_image_index:
            if self.current_grid_image_index == self._init_grid_image_index:
                self._upper_boundary = len(self.all_grid_im_url_list)
            print()
            print("on right side")
            self._down_boundary = self.current_grid_image_index
            print("self._down_boundary ", self._down_boundary)
            print("self._upper_boundary ", self._upper_boundary)
            print()
        # on left part and want to go right
        else:
            print("left side")
            # we touche left vertex
            if self.on_left_vertex:
                print("on left vertex")
                self.on_left_vertex = False
                self._compute_average_score = True
                grid_im_url_list = self.all_grid_im_url_list[0:2]
                return grid_im_url_list
            # when we cross the _init_grid_image_index from left to right :
            # mean initial choix is not good to go left
            self._down_boundary = self.current_grid_image_index
        grid_im_url_list = self.all_grid_im_url_list[
            self._down_boundary : self._upper_boundary
        ]
        print("len(grid_im_url_list) ", len(grid_im_url_list))
        if self._down_boundary == len(self.all_grid_im_url_list) - 2:
            self.on_right_vertex = True
        if self._down_boundary == self._upper_boundary:
            grid_im_url_list = [self.all_grid_im_url_list[0]]

        # other case than touche the vertex
        if len(grid_im_url_list) == 1 and not self.on_right_vertex:
            self._compute_average_score = True
            grid_im_url_list = self.all_grid_im_url_list[
                self._down_boundary : self._upper_boundary + 1
            ]
            print("only one image left")
        print("self._down_boundary ", self._down_boundary)
        print("self._upper_boundary ", self._upper_boundary)
        print()
        return grid_im_url_list

    def update_image_score(self, csv_file_path):
        im_score = self._compute_image_score(self.current_grid_image_index)
        image_name = self.dataset_images_name_list[
            self._current_dataset_image_index
        ]

        df = pd.read_csv(csv_file_path)
        df.loc[df["imName"] == image_name, "imScore"] = float(im_score[0])
        df.to_csv(csv_file_path, index=False)

    def _update_image_score_end_binary_search(
        self, csv_file_path, grid_im_url_list
    ):
        grid_index_1 = grid_im_url_list.index(grid_im_url_list[0])
        grid_index_2 = grid_im_url_list.index(grid_im_url_list[1])
        im_score_1 = float(self._compute_image_score(grid_index_1)[0])
        im_score_2 = float(self._compute_image_score(grid_index_2)[0])
        image_name = self.dataset_images_name_list[
            self._current_dataset_image_index
        ]
        df = pd.read_csv(csv_file_path)
        df.loc[df["imName"] == image_name, "imScore"] = (
            im_score_1 + im_score_2
        ) / 2.0
        df.to_csv(csv_file_path, index=False)

    def update_dataset_image(self, user_csv_file, grid_csv_file):
        # datasry image index updating
        self._current_dataset_image_index += 1
        # check if there is image to show
        if (
            self._current_dataset_image_index
            > len(self.dataset_images_name_list) - 1
        ):
            return None, None
        # find ref image info(url, sector, sceneType)
        (
            ref_image_url,
            ref_image_sector,
            ref_image_sceneType,
        ) = self._get_dataset_image_info(user_csv_file)

        # get grid images url list from sector and sceneType
        self.all_grid_im_url_list = self._get_im_url_by_sector_sceneType(
            grid_csv_file, ref_image_sector, ref_image_sceneType
        )
        if not self.all_grid_im_url_list:
            return str(ref_image_url), None
        # find compare image url
        (
            grid_image_url,
            self.current_grid_image_index,
        ) = self.update_grid_image(self.all_grid_im_url_list)
        self._init_grid_image_index = self.current_grid_image_index
        return str(ref_image_url), str(grid_image_url)

    def _find_current_grid_image(self, grid_im_url_list):
        # find right image url for show
        ## 1  by image index
        grid_im_list_length = len(grid_im_url_list)
        if grid_im_list_length % 2 == 0:
            grid_idex = int(grid_im_list_length / 2)
            current_grid_url = grid_im_url_list[grid_idex]
            current_grid_idex = self.all_grid_im_url_list.index(
                current_grid_url
            )
            return current_grid_url, current_grid_idex
        else:
            grid_idex = math.floor(grid_im_list_length / 2)
            current_grid_url = grid_im_url_list[grid_idex]
            current_grid_idex = self.all_grid_im_url_list.index(
                current_grid_url
            )
            return current_grid_url, current_grid_idex

    def update_grid_image(self, grid_im_url_list):

        # get grid showing image
        (
            current_grid_url,
            self.current_grid_image_index,
        ) = self._find_current_grid_image(grid_im_url_list)
        self.current_grid_url = self.all_grid_im_url_list.index(
            current_grid_url
        )
        # in this case, end of binary search, we take average score of 2 image
        if self._compute_average_score:
            self._compute_average_score = False
            self.on_left_vertex = False
            self.on_right_vertex = False
            print("end of binary search on left side ")
            for im_url in grid_im_url_list:
                print(
                    "average score from ",
                    self.all_grid_im_url_list.index(im_url),
                )
            print()
            self._update_image_score_end_binary_search(
                self.user_dataset_path, grid_im_url_list
            )
            # when end of binary search
            (
                self.current_dataset_image_url,
                self.current_grid_image_url,
            ) = self.update_dataset_image(
                self.user_dataset_path, self.grid_file_path
            )
            return self.current_grid_image_url, self.current_grid_image_index
        return (
            current_grid_url,
            int(self.current_grid_image_index),
        )

    def _get_dataset_image_info(self, user_csv_file):
        image_name = self.dataset_images_name_list[
            self._current_dataset_image_index
        ]
        # ref image ref
        ref_image_url = self._get_im_url_from_name(user_csv_file, image_name)
        # image sector
        ref_image_sector = self._get_im_sector_from_name(
            user_csv_file, image_name
        )
        # image sceneType
        ref_image_sceneType = self._get_im_sceneType_from_name(
            user_csv_file, image_name
        )
        return ref_image_url, ref_image_sector, ref_image_sceneType

    def _extract_im_name_from_csv(self, user_csv_file):
        df = pd.read_csv(user_csv_file)
        images_name = df.loc[
            pd.isna(df["imScore"]),
            "imName",
        ]
        return images_name.values.tolist()

    def _convert_dataset_to_dict(self, user_csv_file):
        dataset_dict = pd.read_csv(
            user_csv_file, index_col=0, skiprows=0
        ).T.to_dict()
        return dataset_dict

    def _get_im_url_from_name(self, csv_file_path, image_name):
        df = pd.read_csv(csv_file_path)
        image_url = df.loc[
            df["imName"] == image_name,
            "imPath",
        ]
        return image_url.values.tolist()[0]

    def _get_im_url_by_sector_sceneType(self, csv_file_path, sector, sceneType):
        df = pd.read_csv(csv_file_path)
        # filter dataframe by sector and sceneType then sort image_url list by gridNormScore
        images_url = df.loc[
            ((df["sector"] == sector) & (df["sceneType"] == sceneType)),
            ["imPath", "gridNormScore"],
        ].sort_values(by=["gridNormScore"], ascending=True)
        return images_url["imPath"].values.tolist()

    def _get_im_sector_from_name(self, csv_file_path, image_name):
        df = pd.read_csv(csv_file_path)
        image_sector = df.loc[
            df["imName"] == image_name,
            "sector",
        ]
        return image_sector.values.tolist()[0]

    def _get_im_sceneType_from_name(self, csv_file_path, image_name):
        df = pd.read_csv(csv_file_path)
        image_sceneType = df.loc[
            df["imName"] == image_name,
            "sceneType",
        ]
        return image_sceneType.values.tolist()[0]

    def _is_file_exist(self, csv_file_path):
        return os.path.exists(csv_file_path)

    def _get_file_name_from_path(self, file_path):
        return os.path.basename(file_path)

    def _download_image_from_csv(self, csv_file, save_dir):
        image_name_list = self._extract_im_name_from_csv(csv_file)
        for name in image_name_list:
            im_url = self._get_im_url_from_name(csv_file, name)
            if self._is_file_exist(im_url):
                shutil.copy(im_url, save_dir + "/" + name)

    def _compute_image_score(self, grid_image_index):
        gri_url = self.all_grid_im_url_list[grid_image_index]
        df = pd.read_csv(self.grid_file_path)
        gridRefScore = df.loc[
            df["imPath"] == gri_url,
            "gridRefScore",
        ]
        return gridRefScore.values.tolist()


# if __name__ == "__main__":

#     my_list = [0, 1, 2, 3, 4, 5]
#     print(my_list[3])
#     print(my_list[1])
#     print(my_list[1:3])
#     print(my_list[0:3])

#     print(my_list[:3])
#     print(my_list[3:])
# csv_file_path = os.path.join(
#     "static", "userStudyData", "output", "test.csv"
# )
# grid_file_name_with_extension = "interpretationGrid_expo_test.csv"
# grid_file_path = os.path.join(
#     "static",
#     "userStudyData",
#     "POC_grid",
#     grid_file_name_with_extension,
# )
# user_study = UserStudyPOC()
# user_study.init_user_dataset_file("test")
# reference_image_path, compare_image_path = user_study.get_showing_image(
#     user_study.user_dataset_path, user_study.grid_file_path
# )
