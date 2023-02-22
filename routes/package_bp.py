from flask import Blueprint
from controllers.PackageController import create, delete, get_update_form, update

package_bp = Blueprint('package_bp', __name__)
package_bp.route('/create', methods=['POST','GET'])(create)
package_bp.route('/delete', methods=['POST'])(delete)
package_bp.route('/updateform', methods = ['POST'])(get_update_form)
package_bp.route('/update', methods = ['POST'])(update)