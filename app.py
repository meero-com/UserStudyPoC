from flask import (
    Flask,
    render_template,
    url_for,
    redirect,
    request,
    session,
    send_from_directory,
    flash,
)
import os
from datetime import timedelta

# from userStudyPOC import UserStudyPOC
from userStudyPOC_with_reset import UserStudyPOC_with_reset
from userStudyAppContext import UserStudy_App_context

app = Flask(__name__)
app.secret_key = "user study interface"
app.permanent_session_lifetime = timedelta(days=1)
REF_IMAGE_FOLDER = os.path.join("static", "userStudyData")
app.config["UPLOAD_FOLDER"] = REF_IMAGE_FOLDER
USER_STUDY_APP_CONTEXT = UserStudy_App_context()
# [X] session: look into
# [X] modify structure of buttons trigger (find a better way to trigger)
# [X] update funtions
# [X] clean @ on backend
# [X] make sure image is in same order (binary serach)
# [X] if no more image dataset or grid image: show message to user about it's end of study
# [X] changer user: if same user?
# [X] always hit on left or right, error showing at end of iteration: indes out of range

# handle if no more image in binary research, take the middle score
# dataset_file_name_with_extension and grid_file_name_with_extension need to be handled a better way (see: utils_class: init_user_dataset_file)
# rename buttons
# generic title for user study interface (button name etc bure)


# remarques !!!!!!:

# 1. end binary search: if we are always on left or right side, average score for last 2 images is not correct, because, we havn't seen last image yet
# 2. the logic of average socre works only on when we go and back on left or right side
# 3. average score for when we cross left side to right side ?


@app.route("/", methods=["GET", "POST"])
def index():
    if "user_email_address" not in session:
        return redirect(url_for("login"))
    # check if image is available
    if (
        USER_STUDY_APP_CONTEXT.user_info[
            session["user_email_address"]
        ].current_dataset_image_url
        is None
    ):
        flash("There is not more dataset image, thanks for your work !")
        return redirect(url_for("logout"))
    elif (
        USER_STUDY_APP_CONTEXT.user_info[
            session["user_email_address"]
        ].current_grid_image_url
        is None
    ):
        flash("There is not more grid image, thanks for your work !")
        return redirect(url_for("logout"))
    if request.method == "POST":
        if "left_button" in request.form:
            print(
                "left button before current grid index",
                USER_STUDY_APP_CONTEXT.user_info[
                    session["user_email_address"]
                ].current_grid_image_index,
            )
            grid_im_url_list = USER_STUDY_APP_CONTEXT.user_info[
                session["user_email_address"]
            ].get_grid_url_list_from_left_button()
            (
                USER_STUDY_APP_CONTEXT.user_info[
                    session["user_email_address"]
                ].current_grid_image_url,
                USER_STUDY_APP_CONTEXT.user_info[
                    session["user_email_address"]
                ].current_grid_image_index,
            ) = USER_STUDY_APP_CONTEXT.user_info[
                session["user_email_address"]
            ].update_grid_image(
                grid_im_url_list
            )
            print(
                "left button after current grid index",
                USER_STUDY_APP_CONTEXT.user_info[
                    session["user_email_address"]
                ].current_grid_image_index,
            )
        elif "equal_button" in request.form:
            # TODO
            # [X]compute score
            # [X]write to csv
            # [X]update show image
            USER_STUDY_APP_CONTEXT.user_info[
                session["user_email_address"]
            ].update_image_score(
                USER_STUDY_APP_CONTEXT.user_info[
                    session["user_email_address"]
                ].user_dataset_path
            )

            (
                USER_STUDY_APP_CONTEXT.user_info[
                    session["user_email_address"]
                ].current_dataset_image_url,
                USER_STUDY_APP_CONTEXT.user_info[
                    session["user_email_address"]
                ].current_grid_image_url,
            ) = USER_STUDY_APP_CONTEXT.user_info[
                session["user_email_address"]
            ].update_dataset_image(
                USER_STUDY_APP_CONTEXT.user_info[
                    session["user_email_address"]
                ].user_dataset_path,
                USER_STUDY_APP_CONTEXT.user_info[
                    session["user_email_address"]
                ].grid_file_path,
            )

            return render_template(
                "index.html",
                reference_image_url=USER_STUDY_APP_CONTEXT.user_info[
                    session["user_email_address"]
                ].current_dataset_image_url,
                compare_image_url=USER_STUDY_APP_CONTEXT.user_info[
                    session["user_email_address"]
                ].current_grid_image_url,
            )
        elif "right_button" in request.form:
            # if no more image to switch
            # TODO
            print(
                "right button before: current grid index",
                USER_STUDY_APP_CONTEXT.user_info[
                    session["user_email_address"]
                ].current_grid_image_index,
            )
            grid_im_url_list = USER_STUDY_APP_CONTEXT.user_info[
                session["user_email_address"]
            ].get_grid_url_list_from_right_button()
            (
                USER_STUDY_APP_CONTEXT.user_info[
                    session["user_email_address"]
                ].current_grid_image_url,
                USER_STUDY_APP_CONTEXT.user_info[
                    session["user_email_address"]
                ].current_grid_image_index,
            ) = USER_STUDY_APP_CONTEXT.user_info[
                session["user_email_address"]
            ].update_grid_image(
                grid_im_url_list
            )
            print(
                "right button after: current grid index",
                USER_STUDY_APP_CONTEXT.user_info[
                    session["user_email_address"]
                ].current_grid_image_index,
            )
        elif "logout_button" in request.form:
            return redirect(url_for("logout"))
        elif "reset_button" in request.form:
            return redirect(url_for("user"))

    if USER_STUDY_APP_CONTEXT.user_info[
        session["user_email_address"]
    ].on_left_vertex:
        return render_template(
            "index.html",
            reference_image_url=USER_STUDY_APP_CONTEXT.user_info[
                session["user_email_address"]
            ].current_dataset_image_url,
            compare_image_url=USER_STUDY_APP_CONTEXT.user_info[
                session["user_email_address"]
            ].current_grid_image_url,
            is_left_button_disabled="disabled",
        )
    elif USER_STUDY_APP_CONTEXT.user_info[
        session["user_email_address"]
    ].on_right_vertex:
        return render_template(
            "index.html",
            reference_image_url=USER_STUDY_APP_CONTEXT.user_info[
                session["user_email_address"]
            ].current_dataset_image_url,
            compare_image_url=USER_STUDY_APP_CONTEXT.user_info[
                session["user_email_address"]
            ].current_grid_image_url,
            is_right_button_disabled="disabled",
        )
    return render_template(
        "index.html",
        reference_image_url=USER_STUDY_APP_CONTEXT.user_info[
            session["user_email_address"]
        ].current_dataset_image_url,
        compare_image_url=USER_STUDY_APP_CONTEXT.user_info[
            session["user_email_address"]
        ].current_grid_image_url,
    )


@app.route("/login", methods=["POST", "GET"])
def login():
    if "user_email_address" in session:
        return redirect(url_for("index"))
    elif request.method == "POST":
        user_email_address = request.form["user email address"]
        if user_email_address:
            if "@" in user_email_address:
                user_email_address = user_email_address.replace("@", "_")
            session.permanent = True
            session["user_email_address"] = user_email_address
            return redirect(url_for("user"))
        else:
            return render_template("login.html")
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user_email_address", None)
    # session.pop("userStudy", None)
    return redirect(url_for("login"))


@app.route("/user", methods=["GET", "POST"])
def user():
    # do something when a user is registed (create a csv file for each user ?)
    # check csv fil in static/POC_dataset
    if not USER_STUDY_APP_CONTEXT.is_user_existed(
        session["user_email_address"]
    ):
        user_study_poc = UserStudyPOC_with_reset()
        USER_STUDY_APP_CONTEXT.add_user(
            session["user_email_address"], user_study_poc
        )
    else:
        USER_STUDY_APP_CONTEXT.refresh_current_context(
            session["user_email_address"]
        )

    if USER_STUDY_APP_CONTEXT.user_info[
        session["user_email_address"]
    ].dataset_initiated:
        (
            USER_STUDY_APP_CONTEXT.user_info[
                session["user_email_address"]
            ].current_dataset_image_url,
            USER_STUDY_APP_CONTEXT.user_info[
                session["user_email_address"]
            ].current_grid_image_url,
        ) = USER_STUDY_APP_CONTEXT.user_info[
            session["user_email_address"]
        ].update_dataset_image(
            USER_STUDY_APP_CONTEXT.user_info[
                session["user_email_address"]
            ].user_dataset_path,
            USER_STUDY_APP_CONTEXT.user_info[
                session["user_email_address"]
            ].grid_file_path,
        )
        # session["userStudy"] = USER_STUDY.__dict__
    else:
        return "<p> There is no input dataset csv file </p>"
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8999, debug=True)
