from userStudyPOC_with_reset import UserStudyPOC_with_reset


class UserStudy_App_context(object):
    def __init__(self):
        self.user_info = {}
        pass

    def add_user(self, user, userStudy):
        if not self.is_user_existed(user):
            self.user_info[user] = userStudy
            userStudy.init_user_dataset_file(user)

    def is_user_existed(self, user):
        if user in self.user_info:
            return True
        else:
            return False

    def refresh_current_context(self, user):
        self.user_info[user].redo_current_comparison()
        self.user_info[user].init_user_dataset_file(user)

    def user_study_image_counter(self, user):
        image_counter = (
            str(self.user_info[user]._current_dataset_image_index)
            + "/"
            + str(len(self.user_info[user].dataset_images_name_list))
            + " images are done "
        )
        return image_counter
