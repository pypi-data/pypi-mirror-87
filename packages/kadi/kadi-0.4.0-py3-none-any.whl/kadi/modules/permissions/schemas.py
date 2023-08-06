# Copyright 2020 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from marshmallow import fields

from .utils import get_action_description
from kadi.lib.schemas import KadiSchema
from kadi.lib.web import url_for
from kadi.modules.accounts.schemas import UserSchema
from kadi.modules.groups.schemas import GroupSchema


class PermissionSchema(KadiSchema):
    """Schema to represent permissions.

    See :class:`.Permission`.
    """

    action = fields.String(dump_only=True)

    object = fields.String(dump_only=True)

    description = fields.Method("_generate_description")

    def _generate_description(self, obj):
        return get_action_description(obj.action, obj.object)


class RoleSchema(KadiSchema):
    """Schema to represent roles.

    See :class:`.Role`.
    """

    name = fields.String(required=True)

    permissions = fields.Nested(PermissionSchema, many=True, dump_only=True)


class UserRoleSchema(KadiSchema):
    """Schema to represent user roles.

    :param group: (optional) A group that the current user role refers to.
    :param obj: (optional) An object other than a group that the current user role
        refers to.
    """

    user = fields.Nested(UserSchema, required=True)

    role = fields.Nested(RoleSchema, required=True)

    _actions = fields.Method("_generate_actions")

    def __init__(self, group=None, obj=None, **kwargs):
        super().__init__(**kwargs)
        self.group = group
        self.obj = obj

    def dump_from_iterable(self, iterable):
        """Serialize an iterable containing user roles.

        :param iterable: An iterable yielding tuples each containing a user and a
            corresponding role.
        :return: The serialized output.
        """
        user_roles = [{"user": user, "role": role} for user, role in iterable]
        return self.dump(user_roles, many=True)

    def _generate_actions(self, obj):
        actions = {}

        # Only supported when used in tandem with "dump_from_iterable".
        if not isinstance(obj, dict):
            return actions

        if self.group:
            actions["remove_member"] = url_for(
                "api.remove_group_member",
                group_id=self.group.id,
                user_id=obj["user"].id,
            )
            actions["change_member"] = url_for(
                "api.change_group_member",
                group_id=self.group.id,
                user_id=obj["user"].id,
            )

        if self.obj:
            obj_name = self.obj.__tablename__
            kwargs = {f"{obj_name}_id": self.obj.id, "user_id": obj["user"].id}

            actions["remove_role"] = url_for(
                f"api.remove_{obj_name}_user_role", **kwargs
            )
            actions["change_role"] = url_for(
                f"api.change_{obj_name}_user_role", **kwargs
            )

        return actions


class GroupRoleSchema(KadiSchema):
    """Schema to represent group roles.

    :param obj: (optional) An object that the current group role refers to.
    """

    group = fields.Nested(GroupSchema, required=True)

    role = fields.Nested(RoleSchema, required=True)

    _actions = fields.Method("_generate_actions")

    def __init__(self, obj=None, **kwargs):
        super().__init__(**kwargs)
        self.obj = obj

    def dump_from_iterable(self, iterable):
        """Serialize an iterable containing group roles.

        :param iterable: An iterable yielding tuples each containing a group and a
            corresponding role.
        :return: The serialized output.
        """
        group_roles = [{"group": group, "role": role} for group, role in iterable]
        return self.dump(group_roles, many=True)

    def _generate_actions(self, obj):
        actions = {}

        # Only supported when used in tandem with "dump_from_iterable".
        if not isinstance(obj, dict) or not self.obj:
            return actions

        obj_name = self.obj.__tablename__
        kwargs = {f"{obj_name}_id": self.obj.id, "group_id": obj["group"].id}

        actions["remove_role"] = url_for(f"api.remove_{obj_name}_group_role", **kwargs)
        actions["change_role"] = url_for(f"api.change_{obj_name}_group_role", **kwargs)

        return actions
