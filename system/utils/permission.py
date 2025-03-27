import operator

class PermissionUtil:
    def get_tree_permissions(all):
        parentList = [permission for permission in all if permission['type'] == 1 or (permission['type'] == 2 and permission['p_id'] == None)]
        # 遍历一级菜单列表，将对应的二级菜单添加到一级菜单的children属性中
        for permission in parentList:
            pid = permission['id']
            level2List = [permission1 for permission1 in all if permission1['p_id'] == pid]
            permission['children'] = level2List
            # 对一级菜单列表进行排序并返回结果
        return sorted(parentList, key=operator.itemgetter('orders'))

    def children_tree(pid, all_data):
        children_list = []
        for permission in all_data:
            if permission.get('p_id') == pid:
                children = PermissionUtil.children_tree(permission.get('id'), all_data)  # 递归调用
                permission['children'] = children
                children_list.append(permission)
        return children_list