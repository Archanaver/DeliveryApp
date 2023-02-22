from flask import Blueprint
from controllers.UserController import login, register, get_profile, update, delete

user_bp = Blueprint('user_bp', __name__)
user_bp.route('/', methods=['POST'])(login)
user_bp.route('/register', methods=['GET', 'POST'])(register)
user_bp.route("/profile")(get_profile)
user_bp.route("/update", methods=['POST'])(update)
user_bp.route("/delete", methods=['POST'])(delete)




# user_bp.route('/create', methods=['POST'])(store)
# user_bp.route('/<int:user_id>', methods=['GET'])(show)
# user_bp.route('/<int:user_id>/edit', methods=['POST'])(update)
# user_bp.route('/<int:user_id>', methods=['DELETE'])(destroy)