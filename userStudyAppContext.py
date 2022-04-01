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
        self.user_info[user].reset()
        self.user_info[user].init_user_dataset_file(user)
