import xadmin
from xadmin import views

from users.models import User
from xadmin.plugins import auth


class UserAdmin(auth.UserAdmin):
    model_icon = 'fa fa-gift'
    list_display = ['id', 'username', 'mobile']
    search_fields = ['mobile']
    list_export = ['xls', 'csv', 'xml']
    refresh_times = [3, 5]  # 可选以支持按多长时间(秒)刷新页面
    # readonly_fields = ['username']

    # data_charts = {
    #     "user_id": {'title': '用户', "x-field": "id", "y-field": ('mobile',),
    #                 "order": ('id',)},
    #     "user_tag": {'title': '编号', "x-field": "id", "y-field": ('mobile',),
    #                  "order": ('id',)},
    #
    # }

    def get_model_form(self, **kwargs):
        if self.org_obj is None:
            self.fields = ['username', 'password']

        return super().get_model_form(**kwargs)


class GlobalSettings(object):
    # 全局配置，后台管理标题和页脚
    site_title = "仙剑奇侠传"
    site_footer = "turing"
    # 菜单收缩
    menu_style = "accordion"


class BaseSetting(object):
    """xadmin的基本配置"""
    enable_themes = True  # 开启主题切换功能
    use_bootswatch = True


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)

xadmin.site.unregister(User)
xadmin.site.register(User, UserAdmin)


# 属性查询
# list_display
# 控制列表展示的字段
# search_fields
# 控制可以通过搜索框搜索的字段名称，xadmin使用的是模糊查询
# list_filter
# 可以进行过滤操作的列
# ordering
# 默认排序的字段
# readonly_fields
# 在编辑页面的只读字段
# exclude
# 在编辑页面隐藏的字段
# list_editable
# 在列表页可以快速直接编辑的字段
# show_detail_fileds
# 在列表页提供快速显示详情信息
# refresh_times
# 指定列表页的定时刷新
# list_export
# 控制列表页导出数据的可选格式
# data_charts
# 控制显示图标的样式
# model_icon
# 控制菜单的图标


class SKUSpecificationAdmin(object):
    def save_models(self):
        # 保存数据对象
        obj = self.new_obj
        obj.save()

        # 补充自定义行为
        # from celery_tasks.html.tasks import generate_static_sku_detail_html
        # generate_static_sku_detail_html.delay(obj.sku.id)

    def delete_model(self):
        # 删除数据对象
        obj = self.obj
        sku_id = obj.sku.id
        obj.delete()

        # 补充自定义行为
        # from celery_tasks.html.tasks import generate_static_sku_detail_html
        # generate_static_sku_detail_html.delay(sku_id)
