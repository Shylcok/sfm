#!/usr/bin/env python
# encoding: utf-8

"""
@version: v1.0
@author: suyuan
@license: 
@contact: suyuan@gmail.com
@site: https://github.com/su6838354/sfm
@software: PyCharm
@file: order_service.py
@time: 16/10/14 下午8:03
"""

from base_service import BaseService


class OrderService(BaseService):

    def get_address(self, user_id):
        res = self.context_repos.address_repo.select_by_user_id(user_id)
        return res

    def add_address(self, user_id, address_info):
        name = address_info['name']
        mobile = address_info['mobile']
        address = address_info['address']
        is_default = address_info['is_default']
        if is_default == 1:
            self.context_repos.address_repo.update_by_user_id_set_no_default(user_id)

        res = self.context_repos.address_repo.insert(user_id, name, mobile, address, is_default)
        return {'code': 0, 'msg': '添加地址成功', 'data': res}

    def update_address(self, id, user_id, address_info):
        name = address_info['name']
        mobile = address_info['mobile']
        address = address_info['address']
        is_default = address_info['is_default']
        if is_default == 1:
            self.context_repos.address_repo.update_by_user_id_set_no_default(user_id)

        res = self.context_repos.address_repo.update_by_id(user_id, name, mobile, address, is_default, id)
        return {'code': 0, 'msg': '更新地址成功', 'data': res}

    def delete_address(self, id):
        res = self.context_repos.address_repo.delete_by_id(id)
        return {'code': 0, 'msg': '删除地址成功', 'data': res}

    def set_default(self, user_id, id):
        self.context_repos.address_repo.update_by_user_id_set_no_default(user_id)
        res = self.context_repos.address_repo.update_by_id_set_default(id)
        return {'code': 0, 'msg': '设置默认地址成功', 'data': res}






    def get_user(self, user_id):
        res = self.context_repos.user_repo.select_by_user_id(user_id)
        return res
